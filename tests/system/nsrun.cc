// Runs a command chrooted into a root filesystem inside fresh, unprivileged
// user/mount/network/PID/IPC/UTS namespaces: a minimal container for system
// tests that needs neither root nor a container engine.
//
// Usage: nsrun ROOTFS [--bind SRC:DST]... -- COMMAND [ARGS...]
//
// The calling user becomes root inside. ROOTFS gets /proc, a recursive bind of
// /dev, sysfs (when permitted), and fresh tmpfs on /run and /tmp. The network
// namespace has only loopback, which is brought up. COMMAND runs as PID 1, so
// everything it starts is killed when it exits; nsrun returns its status.
#include <fcntl.h>
#include <net/if.h>
#include <sched.h>
#include <sys/ioctl.h>
#include <sys/mount.h>
#include <sys/socket.h>
#include <sys/stat.h>
#include <sys/wait.h>
#include <unistd.h>

#include <cerrno>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <string>
#include <utility>
#include <vector>

namespace {

[[noreturn]] void die(const std::string& what) {
    std::fprintf(stderr, "nsrun: %s: %s\n", what.c_str(), std::strerror(errno));
    std::_Exit(125);
}

void write_file(const char* path, const std::string& content) {
    int fd = open(path, O_WRONLY | O_CLOEXEC);
    if (fd < 0 || write(fd, content.data(), content.size()) != static_cast<ssize_t>(content.size())) die(path);
    close(fd);
}

void mkdirs(const std::string& path) {
    for (size_t i = 1; i <= path.size(); ++i) {
        if (i != path.size() && path[i] != '/') continue;
        std::string prefix = path.substr(0, i);
        if (mkdir(prefix.c_str(), 0755) != 0 && errno != EEXIST) die("mkdir " + prefix);
    }
}

// Creates an empty mount point of the same kind (file or directory) as SRC.
void mountpoint_for(const std::string& src, const std::string& dst) {
    struct stat st {};
    if (stat(src.c_str(), &st) != 0) die("stat " + src);
    if (S_ISDIR(st.st_mode)) return mkdirs(dst);
    mkdirs(dst.substr(0, dst.rfind('/')));
    int fd = open(dst.c_str(), O_WRONLY | O_CREAT | O_CLOEXEC, 0644);
    if (fd < 0) die("create " + dst);
    close(fd);
}

void mount_or_die(const char* src, const std::string& dst, const char* type, unsigned long flags) {
    if (mount(src, dst.c_str(), type, flags, nullptr) != 0) die(std::string("mount ") + type + " on " + dst);
}

void loopback_up() {
    int fd = socket(AF_INET, SOCK_DGRAM | SOCK_CLOEXEC, 0);
    if (fd < 0) die("socket");
    ifreq ifr {};
    std::strncpy(ifr.ifr_name, "lo", IFNAMSIZ - 1);
    if (ioctl(fd, SIOCGIFFLAGS, &ifr) != 0) die("SIOCGIFFLAGS lo");
    ifr.ifr_flags |= IFF_UP;
    if (ioctl(fd, SIOCSIFFLAGS, &ifr) != 0) die("SIOCSIFFLAGS lo");
    close(fd);
}

}  // namespace

int main(int argc, char** argv) {
    if (argc < 4) {
        std::fprintf(stderr, "usage: nsrun ROOTFS [--bind SRC:DST]... -- COMMAND [ARGS...]\n");
        return 2;
    }
    char* real = realpath(argv[1], nullptr);
    if (!real) die(argv[1]);
    const std::string root = real;
    std::free(real);
    std::vector<std::pair<std::string, std::string>> binds;
    int i = 2;
    while (i < argc && std::strcmp(argv[i], "--") != 0) {
        const std::string spec = i + 1 < argc ? argv[i + 1] : "";
        const auto colon = spec.find(':');
        if (std::strcmp(argv[i], "--bind") != 0 || colon == std::string::npos || spec[colon + 1] != '/') {
            std::fprintf(stderr, "nsrun: expected --bind SRC:/DST, got %s\n", argv[i]);
            return 2;
        }
        binds.emplace_back(spec.substr(0, colon), spec.substr(colon + 1));
        i += 2;
    }
    if (i + 1 >= argc) {
        std::fprintf(stderr, "nsrun: missing -- COMMAND\n");
        return 2;
    }
    char** command = argv + i + 1;

    const uid_t uid = getuid();
    const gid_t gid = getgid();
    if (unshare(CLONE_NEWUSER | CLONE_NEWNS | CLONE_NEWNET | CLONE_NEWPID | CLONE_NEWIPC | CLONE_NEWUTS) != 0) die("unshare");
    write_file("/proc/self/setgroups", "deny");
    write_file("/proc/self/uid_map", "0 " + std::to_string(uid) + " 1");
    write_file("/proc/self/gid_map", "0 " + std::to_string(gid) + " 1");

    const pid_t child = fork();
    if (child < 0) die("fork");
    if (child == 0) {
        // PID 1 of the new namespace.
        mount_or_die(nullptr, "/", nullptr, MS_REC | MS_PRIVATE);
        for (const char* dir : {"/proc", "/dev", "/sys", "/run", "/tmp"}) mkdirs(root + dir);
        mount_or_die("proc", root + "/proc", "proc", MS_NOSUID | MS_NODEV | MS_NOEXEC);
        mount_or_die("/dev", root + "/dev", nullptr, MS_BIND | MS_REC);
        // sysfs needs an unmasked host sysfs; tests that need it check for it.
        if (mount("sysfs", (root + "/sys").c_str(), "sysfs", MS_NOSUID | MS_NODEV | MS_NOEXEC | MS_RDONLY, nullptr) != 0)
            std::fprintf(stderr, "nsrun: sysfs unavailable (%s); continuing without it\n", std::strerror(errno));
        mount_or_die("tmpfs", root + "/run", "tmpfs", MS_NOSUID | MS_NODEV);
        mount_or_die("tmpfs", root + "/tmp", "tmpfs", MS_NOSUID | MS_NODEV);
        for (const auto& bind : binds) {
            mountpoint_for(bind.first, root + bind.second);
            mount_or_die(bind.first.c_str(), root + bind.second, nullptr, MS_BIND | MS_REC);
        }
        loopback_up();
        if (chroot(root.c_str()) != 0) die("chroot " + root);
        if (chdir("/") != 0) die("chdir /");
        execv(command[0], command);
        die(std::string("exec ") + command[0]);
    }
    int status = 0;
    while (waitpid(child, &status, 0) < 0)
        if (errno != EINTR) die("waitpid");
    if (WIFEXITED(status)) return WEXITSTATUS(status);
    std::fprintf(stderr, "nsrun: command killed by signal %d\n", WTERMSIG(status));
    return 128 + WTERMSIG(status);
}
