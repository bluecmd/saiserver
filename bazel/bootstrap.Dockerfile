# Official Docker Hub library/debian:bookworm, resolved to its Linux/amd64
# manifest (not the multi-platform index). No mutable tag or package installs.
# The apt-capable base supplies Bash, coreutils, and libstdc++.so.6.
FROM --platform=linux/amd64 docker.io/library/debian@sha256:f9c4778ec75d6b054367315b1eb4f3992ee5866b50de6d591a33e8904cba3f17

ADD --checksum=sha256:7f775b54bbec487efaf0f49ccda1d2ed02cd34f582edfdd6aeeec76e39ef585c --chmod=0755 https://releases.bazel.build/9.3.1/release/bazel-9.3.1-linux-x86_64 /usr/local/bin/bazel

ENV PATH=/usr/local/bin:/usr/bin:/bin HOME=/cache/home LANG=C.UTF-8 LC_ALL=C.UTF-8 TZ=UTC
WORKDIR /workspace
ENTRYPOINT ["/usr/local/bin/bazel"]
