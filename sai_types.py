r"""Wrapper for saiacl.h

Generated with:
/home/bluecmd/.local/bin/ctypesgen /home/bluecmd/Downloads/SAI/inc/saiacl.h /home/bluecmd/Downloads/SAI/inc/saiars.h /home/bluecmd/Downloads/SAI/inc/saiarsprofile.h /home/bluecmd/Downloads/SAI/inc/saibfd.h /home/bluecmd/Downloads/SAI/inc/saibridge.h /home/bluecmd/Downloads/SAI/inc/saibuffer.h /home/bluecmd/Downloads/SAI/inc/saicounter.h /home/bluecmd/Downloads/SAI/inc/saidebugcounter.h /home/bluecmd/Downloads/SAI/inc/saidtel.h /home/bluecmd/Downloads/SAI/inc/saifdb.h /home/bluecmd/Downloads/SAI/inc/saigenericprogrammable.h /home/bluecmd/Downloads/SAI/inc/sai.h /home/bluecmd/Downloads/SAI/inc/saihash.h /home/bluecmd/Downloads/SAI/inc/saihostif.h /home/bluecmd/Downloads/SAI/inc/saiipmcgroup.h /home/bluecmd/Downloads/SAI/inc/saiipmc.h /home/bluecmd/Downloads/SAI/inc/saiipsec.h /home/bluecmd/Downloads/SAI/inc/saiisolationgroup.h /home/bluecmd/Downloads/SAI/inc/sail2mcgroup.h /home/bluecmd/Downloads/SAI/inc/sail2mc.h /home/bluecmd/Downloads/SAI/inc/sailag.h /home/bluecmd/Downloads/SAI/inc/saimacsec.h /home/bluecmd/Downloads/SAI/inc/saimcastfdb.h /home/bluecmd/Downloads/SAI/inc/saimirror.h /home/bluecmd/Downloads/SAI/inc/saimpls.h /home/bluecmd/Downloads/SAI/inc/saimymac.h /home/bluecmd/Downloads/SAI/inc/sainat.h /home/bluecmd/Downloads/SAI/inc/saineighbor.h /home/bluecmd/Downloads/SAI/inc/sainexthopgroup.h /home/bluecmd/Downloads/SAI/inc/sainexthop.h /home/bluecmd/Downloads/SAI/inc/saiobject.h /home/bluecmd/Downloads/SAI/inc/saipolicer.h /home/bluecmd/Downloads/SAI/inc/saiport.h /home/bluecmd/Downloads/SAI/inc/saiqosmap.h /home/bluecmd/Downloads/SAI/inc/saiqueue.h /home/bluecmd/Downloads/SAI/inc/sairoute.h /home/bluecmd/Downloads/SAI/inc/sairouterinterface.h /home/bluecmd/Downloads/SAI/inc/sairpfgroup.h /home/bluecmd/Downloads/SAI/inc/saisamplepacket.h /home/bluecmd/Downloads/SAI/inc/saischedulergroup.h /home/bluecmd/Downloads/SAI/inc/saischeduler.h /home/bluecmd/Downloads/SAI/inc/saisrv6.h /home/bluecmd/Downloads/SAI/inc/saistatus.h /home/bluecmd/Downloads/SAI/inc/saistp.h /home/bluecmd/Downloads/SAI/inc/saiswitch.h /home/bluecmd/Downloads/SAI/inc/saisystemport.h /home/bluecmd/Downloads/SAI/inc/saitam.h /home/bluecmd/Downloads/SAI/inc/saitunnel.h /home/bluecmd/Downloads/SAI/inc/saitwamp.h /home/bluecmd/Downloads/SAI/inc/saitypes.h /home/bluecmd/Downloads/SAI/inc/saiudf.h /home/bluecmd/Downloads/SAI/inc/saiversion.h /home/bluecmd/Downloads/SAI/inc/saivirtualrouter.h /home/bluecmd/Downloads/SAI/inc/saivlan.h /home/bluecmd/Downloads/SAI/inc/saiwred.h -I /home/bluecmd/Downloads/SAI/inc -I /home/bluecmd/Downloads/SAI/experimental/ -o sai_types.py

Do not modify this file.
"""

__docformat__ = "restructuredtext"

# Begin preamble for Python

import ctypes
import sys
from ctypes import *  # noqa: F401, F403

_int_types = (ctypes.c_int16, ctypes.c_int32)
if hasattr(ctypes, "c_int64"):
    # Some builds of ctypes apparently do not have ctypes.c_int64
    # defined; it's a pretty good bet that these builds do not
    # have 64-bit pointers.
    _int_types += (ctypes.c_int64,)
for t in _int_types:
    if ctypes.sizeof(t) == ctypes.sizeof(ctypes.c_size_t):
        c_ptrdiff_t = t
del t
del _int_types



class UserString:
    def __init__(self, seq):
        if isinstance(seq, bytes):
            self.data = seq
        elif isinstance(seq, UserString):
            self.data = seq.data[:]
        else:
            self.data = str(seq).encode()

    def __bytes__(self):
        return self.data

    def __str__(self):
        return self.data.decode()

    def __repr__(self):
        return repr(self.data)

    def __int__(self):
        return int(self.data.decode())

    def __long__(self):
        return int(self.data.decode())

    def __float__(self):
        return float(self.data.decode())

    def __complex__(self):
        return complex(self.data.decode())

    def __hash__(self):
        return hash(self.data)

    def __le__(self, string):
        if isinstance(string, UserString):
            return self.data <= string.data
        else:
            return self.data <= string

    def __lt__(self, string):
        if isinstance(string, UserString):
            return self.data < string.data
        else:
            return self.data < string

    def __ge__(self, string):
        if isinstance(string, UserString):
            return self.data >= string.data
        else:
            return self.data >= string

    def __gt__(self, string):
        if isinstance(string, UserString):
            return self.data > string.data
        else:
            return self.data > string

    def __eq__(self, string):
        if isinstance(string, UserString):
            return self.data == string.data
        else:
            return self.data == string

    def __ne__(self, string):
        if isinstance(string, UserString):
            return self.data != string.data
        else:
            return self.data != string

    def __contains__(self, char):
        return char in self.data

    def __len__(self):
        return len(self.data)

    def __getitem__(self, index):
        return self.__class__(self.data[index])

    def __getslice__(self, start, end):
        start = max(start, 0)
        end = max(end, 0)
        return self.__class__(self.data[start:end])

    def __add__(self, other):
        if isinstance(other, UserString):
            return self.__class__(self.data + other.data)
        elif isinstance(other, bytes):
            return self.__class__(self.data + other)
        else:
            return self.__class__(self.data + str(other).encode())

    def __radd__(self, other):
        if isinstance(other, bytes):
            return self.__class__(other + self.data)
        else:
            return self.__class__(str(other).encode() + self.data)

    def __mul__(self, n):
        return self.__class__(self.data * n)

    __rmul__ = __mul__

    def __mod__(self, args):
        return self.__class__(self.data % args)

    # the following methods are defined in alphabetical order:
    def capitalize(self):
        return self.__class__(self.data.capitalize())

    def center(self, width, *args):
        return self.__class__(self.data.center(width, *args))

    def count(self, sub, start=0, end=sys.maxsize):
        return self.data.count(sub, start, end)

    def decode(self, encoding=None, errors=None):  # XXX improve this?
        if encoding:
            if errors:
                return self.__class__(self.data.decode(encoding, errors))
            else:
                return self.__class__(self.data.decode(encoding))
        else:
            return self.__class__(self.data.decode())

    def encode(self, encoding=None, errors=None):  # XXX improve this?
        if encoding:
            if errors:
                return self.__class__(self.data.encode(encoding, errors))
            else:
                return self.__class__(self.data.encode(encoding))
        else:
            return self.__class__(self.data.encode())

    def endswith(self, suffix, start=0, end=sys.maxsize):
        return self.data.endswith(suffix, start, end)

    def expandtabs(self, tabsize=8):
        return self.__class__(self.data.expandtabs(tabsize))

    def find(self, sub, start=0, end=sys.maxsize):
        return self.data.find(sub, start, end)

    def index(self, sub, start=0, end=sys.maxsize):
        return self.data.index(sub, start, end)

    def isalpha(self):
        return self.data.isalpha()

    def isalnum(self):
        return self.data.isalnum()

    def isdecimal(self):
        return self.data.isdecimal()

    def isdigit(self):
        return self.data.isdigit()

    def islower(self):
        return self.data.islower()

    def isnumeric(self):
        return self.data.isnumeric()

    def isspace(self):
        return self.data.isspace()

    def istitle(self):
        return self.data.istitle()

    def isupper(self):
        return self.data.isupper()

    def join(self, seq):
        return self.data.join(seq)

    def ljust(self, width, *args):
        return self.__class__(self.data.ljust(width, *args))

    def lower(self):
        return self.__class__(self.data.lower())

    def lstrip(self, chars=None):
        return self.__class__(self.data.lstrip(chars))

    def partition(self, sep):
        return self.data.partition(sep)

    def replace(self, old, new, maxsplit=-1):
        return self.__class__(self.data.replace(old, new, maxsplit))

    def rfind(self, sub, start=0, end=sys.maxsize):
        return self.data.rfind(sub, start, end)

    def rindex(self, sub, start=0, end=sys.maxsize):
        return self.data.rindex(sub, start, end)

    def rjust(self, width, *args):
        return self.__class__(self.data.rjust(width, *args))

    def rpartition(self, sep):
        return self.data.rpartition(sep)

    def rstrip(self, chars=None):
        return self.__class__(self.data.rstrip(chars))

    def split(self, sep=None, maxsplit=-1):
        return self.data.split(sep, maxsplit)

    def rsplit(self, sep=None, maxsplit=-1):
        return self.data.rsplit(sep, maxsplit)

    def splitlines(self, keepends=0):
        return self.data.splitlines(keepends)

    def startswith(self, prefix, start=0, end=sys.maxsize):
        return self.data.startswith(prefix, start, end)

    def strip(self, chars=None):
        return self.__class__(self.data.strip(chars))

    def swapcase(self):
        return self.__class__(self.data.swapcase())

    def title(self):
        return self.__class__(self.data.title())

    def translate(self, *args):
        return self.__class__(self.data.translate(*args))

    def upper(self):
        return self.__class__(self.data.upper())

    def zfill(self, width):
        return self.__class__(self.data.zfill(width))


class MutableString(UserString):
    """mutable string objects

    Python strings are immutable objects.  This has the advantage, that
    strings may be used as dictionary keys.  If this property isn't needed
    and you insist on changing string values in place instead, you may cheat
    and use MutableString.

    But the purpose of this class is an educational one: to prevent
    people from inventing their own mutable string class derived
    from UserString and than forget thereby to remove (override) the
    __hash__ method inherited from UserString.  This would lead to
    errors that would be very hard to track down.

    A faster and better solution is to rewrite your program using lists."""

    def __init__(self, string=""):
        self.data = string

    def __hash__(self):
        raise TypeError("unhashable type (it is mutable)")

    def __setitem__(self, index, sub):
        if index < 0:
            index += len(self.data)
        if index < 0 or index >= len(self.data):
            raise IndexError
        self.data = self.data[:index] + sub + self.data[index + 1 :]

    def __delitem__(self, index):
        if index < 0:
            index += len(self.data)
        if index < 0 or index >= len(self.data):
            raise IndexError
        self.data = self.data[:index] + self.data[index + 1 :]

    def __setslice__(self, start, end, sub):
        start = max(start, 0)
        end = max(end, 0)
        if isinstance(sub, UserString):
            self.data = self.data[:start] + sub.data + self.data[end:]
        elif isinstance(sub, bytes):
            self.data = self.data[:start] + sub + self.data[end:]
        else:
            self.data = self.data[:start] + str(sub).encode() + self.data[end:]

    def __delslice__(self, start, end):
        start = max(start, 0)
        end = max(end, 0)
        self.data = self.data[:start] + self.data[end:]

    def immutable(self):
        return UserString(self.data)

    def __iadd__(self, other):
        if isinstance(other, UserString):
            self.data += other.data
        elif isinstance(other, bytes):
            self.data += other
        else:
            self.data += str(other).encode()
        return self

    def __imul__(self, n):
        self.data *= n
        return self


class String(MutableString, ctypes.Union):

    _fields_ = [("raw", ctypes.POINTER(ctypes.c_char)), ("data", ctypes.c_char_p)]

    def __init__(self, obj=b""):
        if isinstance(obj, (bytes, UserString)):
            self.data = bytes(obj)
        else:
            self.raw = obj

    def __len__(self):
        return self.data and len(self.data) or 0

    def from_param(cls, obj):
        # Convert None or 0
        if obj is None or obj == 0:
            return cls(ctypes.POINTER(ctypes.c_char)())

        # Convert from String
        elif isinstance(obj, String):
            return obj

        # Convert from bytes
        elif isinstance(obj, bytes):
            return cls(obj)

        # Convert from str
        elif isinstance(obj, str):
            return cls(obj.encode())

        # Convert from c_char_p
        elif isinstance(obj, ctypes.c_char_p):
            return obj

        # Convert from POINTER(ctypes.c_char)
        elif isinstance(obj, ctypes.POINTER(ctypes.c_char)):
            return obj

        # Convert from raw pointer
        elif isinstance(obj, int):
            return cls(ctypes.cast(obj, ctypes.POINTER(ctypes.c_char)))

        # Convert from ctypes.c_char array
        elif isinstance(obj, ctypes.c_char * len(obj)):
            return obj

        # Convert from object
        else:
            return String.from_param(obj._as_parameter_)

    from_param = classmethod(from_param)


def ReturnString(obj, func=None, arguments=None):
    return String.from_param(obj)


# As of ctypes 1.0, ctypes does not support custom error-checking
# functions on callbacks, nor does it support custom datatypes on
# callbacks, so we must ensure that all callbacks return
# primitive datatypes.
#
# Non-primitive return values wrapped with UNCHECKED won't be
# typechecked, and will be converted to ctypes.c_void_p.
def UNCHECKED(type):
    if hasattr(type, "_type_") and isinstance(type._type_, str) and type._type_ != "P":
        return type
    else:
        return ctypes.c_void_p


# ctypes doesn't have direct support for variadic functions, so we have to write
# our own wrapper class
class _variadic_function(object):
    def __init__(self, func, restype, argtypes, errcheck):
        self.func = func
        self.func.restype = restype
        self.argtypes = argtypes
        if errcheck:
            self.func.errcheck = errcheck

    def _as_parameter_(self):
        # So we can pass this variadic function as a function pointer
        return self.func

    def __call__(self, *args):
        fixed_args = []
        i = 0
        for argtype in self.argtypes:
            # Typecheck what we can
            fixed_args.append(argtype.from_param(args[i]))
            i += 1
        return self.func(*fixed_args + list(args[i:]))


def ord_if_char(value):
    """
    Simple helper used for casts to simple builtin types:  if the argument is a
    string type, it will be converted to it's ordinal value.

    This function will raise an exception if the argument is string with more
    than one characters.
    """
    return ord(value) if (isinstance(value, bytes) or isinstance(value, str)) else value

# End preamble

_libs = {}
_libdirs = []

# Begin loader

"""
Load libraries - appropriately for all our supported platforms
"""
# ----------------------------------------------------------------------------
# Copyright (c) 2008 David James
# Copyright (c) 2006-2008 Alex Holkner
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in
#    the documentation and/or other materials provided with the
#    distribution.
#  * Neither the name of pyglet nor the names of its
#    contributors may be used to endorse or promote products
#    derived from this software without specific prior written
#    permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
# ----------------------------------------------------------------------------

import ctypes
import ctypes.util
import glob
import os.path
import platform
import re
import sys


def _environ_path(name):
    """Split an environment variable into a path-like list elements"""
    if name in os.environ:
        return os.environ[name].split(":")
    return []


class LibraryLoader:
    """
    A base class For loading of libraries ;-)
    Subclasses load libraries for specific platforms.
    """

    # library names formatted specifically for platforms
    name_formats = ["%s"]

    class Lookup:
        """Looking up calling conventions for a platform"""

        mode = ctypes.DEFAULT_MODE

        def __init__(self, path):
            super(LibraryLoader.Lookup, self).__init__()
            self.access = dict(cdecl=ctypes.CDLL(path, self.mode))

        def get(self, name, calling_convention="cdecl"):
            """Return the given name according to the selected calling convention"""
            if calling_convention not in self.access:
                raise LookupError(
                    "Unknown calling convention '{}' for function '{}'".format(
                        calling_convention, name
                    )
                )
            return getattr(self.access[calling_convention], name)

        def has(self, name, calling_convention="cdecl"):
            """Return True if this given calling convention finds the given 'name'"""
            if calling_convention not in self.access:
                return False
            return hasattr(self.access[calling_convention], name)

        def __getattr__(self, name):
            return getattr(self.access["cdecl"], name)

    def __init__(self):
        self.other_dirs = []

    def __call__(self, libname):
        """Given the name of a library, load it."""
        paths = self.getpaths(libname)

        for path in paths:
            # noinspection PyBroadException
            try:
                return self.Lookup(path)
            except Exception:  # pylint: disable=broad-except
                pass

        raise ImportError("Could not load %s." % libname)

    def getpaths(self, libname):
        """Return a list of paths where the library might be found."""
        if os.path.isabs(libname):
            yield libname
        else:
            # search through a prioritized series of locations for the library

            # we first search any specific directories identified by user
            for dir_i in self.other_dirs:
                for fmt in self.name_formats:
                    # dir_i should be absolute already
                    yield os.path.join(dir_i, fmt % libname)

            # check if this code is even stored in a physical file
            try:
                this_file = __file__
            except NameError:
                this_file = None

            # then we search the directory where the generated python interface is stored
            if this_file is not None:
                for fmt in self.name_formats:
                    yield os.path.abspath(os.path.join(os.path.dirname(__file__), fmt % libname))

            # now, use the ctypes tools to try to find the library
            for fmt in self.name_formats:
                path = ctypes.util.find_library(fmt % libname)
                if path:
                    yield path

            # then we search all paths identified as platform-specific lib paths
            for path in self.getplatformpaths(libname):
                yield path

            # Finally, we'll try the users current working directory
            for fmt in self.name_formats:
                yield os.path.abspath(os.path.join(os.path.curdir, fmt % libname))

    def getplatformpaths(self, _libname):  # pylint: disable=no-self-use
        """Return all the library paths available in this platform"""
        return []


# Darwin (Mac OS X)


class DarwinLibraryLoader(LibraryLoader):
    """Library loader for MacOS"""

    name_formats = [
        "lib%s.dylib",
        "lib%s.so",
        "lib%s.bundle",
        "%s.dylib",
        "%s.so",
        "%s.bundle",
        "%s",
    ]

    class Lookup(LibraryLoader.Lookup):
        """
        Looking up library files for this platform (Darwin aka MacOS)
        """

        # Darwin requires dlopen to be called with mode RTLD_GLOBAL instead
        # of the default RTLD_LOCAL.  Without this, you end up with
        # libraries not being loadable, resulting in "Symbol not found"
        # errors
        mode = ctypes.RTLD_GLOBAL

    def getplatformpaths(self, libname):
        if os.path.pathsep in libname:
            names = [libname]
        else:
            names = [fmt % libname for fmt in self.name_formats]

        for directory in self.getdirs(libname):
            for name in names:
                yield os.path.join(directory, name)

    @staticmethod
    def getdirs(libname):
        """Implements the dylib search as specified in Apple documentation:

        http://developer.apple.com/documentation/DeveloperTools/Conceptual/
            DynamicLibraries/Articles/DynamicLibraryUsageGuidelines.html

        Before commencing the standard search, the method first checks
        the bundle's ``Frameworks`` directory if the application is running
        within a bundle (OS X .app).
        """

        dyld_fallback_library_path = _environ_path("DYLD_FALLBACK_LIBRARY_PATH")
        if not dyld_fallback_library_path:
            dyld_fallback_library_path = [
                os.path.expanduser("~/lib"),
                "/usr/local/lib",
                "/usr/lib",
            ]

        dirs = []

        if "/" in libname:
            dirs.extend(_environ_path("DYLD_LIBRARY_PATH"))
        else:
            dirs.extend(_environ_path("LD_LIBRARY_PATH"))
            dirs.extend(_environ_path("DYLD_LIBRARY_PATH"))
            dirs.extend(_environ_path("LD_RUN_PATH"))

        if hasattr(sys, "frozen") and getattr(sys, "frozen") == "macosx_app":
            dirs.append(os.path.join(os.environ["RESOURCEPATH"], "..", "Frameworks"))

        dirs.extend(dyld_fallback_library_path)

        return dirs


# Posix


class PosixLibraryLoader(LibraryLoader):
    """Library loader for POSIX-like systems (including Linux)"""

    _ld_so_cache = None

    _include = re.compile(r"^\s*include\s+(?P<pattern>.*)")

    name_formats = ["lib%s.so", "%s.so", "%s"]

    class _Directories(dict):
        """Deal with directories"""

        def __init__(self):
            dict.__init__(self)
            self.order = 0

        def add(self, directory):
            """Add a directory to our current set of directories"""
            if len(directory) > 1:
                directory = directory.rstrip(os.path.sep)
            # only adds and updates order if exists and not already in set
            if not os.path.exists(directory):
                return
            order = self.setdefault(directory, self.order)
            if order == self.order:
                self.order += 1

        def extend(self, directories):
            """Add a list of directories to our set"""
            for a_dir in directories:
                self.add(a_dir)

        def ordered(self):
            """Sort the list of directories"""
            return (i[0] for i in sorted(self.items(), key=lambda d: d[1]))

    def _get_ld_so_conf_dirs(self, conf, dirs):
        """
        Recursive function to help parse all ld.so.conf files, including proper
        handling of the `include` directive.
        """

        try:
            with open(conf) as fileobj:
                for dirname in fileobj:
                    dirname = dirname.strip()
                    if not dirname:
                        continue

                    match = self._include.match(dirname)
                    if not match:
                        dirs.add(dirname)
                    else:
                        for dir2 in glob.glob(match.group("pattern")):
                            self._get_ld_so_conf_dirs(dir2, dirs)
        except IOError:
            pass

    def _create_ld_so_cache(self):
        # Recreate search path followed by ld.so.  This is going to be
        # slow to build, and incorrect (ld.so uses ld.so.cache, which may
        # not be up-to-date).  Used only as fallback for distros without
        # /sbin/ldconfig.
        #
        # We assume the DT_RPATH and DT_RUNPATH binary sections are omitted.

        directories = self._Directories()
        for name in (
            "LD_LIBRARY_PATH",
            "SHLIB_PATH",  # HP-UX
            "LIBPATH",  # OS/2, AIX
            "LIBRARY_PATH",  # BE/OS
        ):
            if name in os.environ:
                directories.extend(os.environ[name].split(os.pathsep))

        self._get_ld_so_conf_dirs("/etc/ld.so.conf", directories)

        bitage = platform.architecture()[0]

        unix_lib_dirs_list = []
        if bitage.startswith("64"):
            # prefer 64 bit if that is our arch
            unix_lib_dirs_list += ["/lib64", "/usr/lib64"]

        # must include standard libs, since those paths are also used by 64 bit
        # installs
        unix_lib_dirs_list += ["/lib", "/usr/lib"]
        if sys.platform.startswith("linux"):
            # Try and support multiarch work in Ubuntu
            # https://wiki.ubuntu.com/MultiarchSpec
            if bitage.startswith("32"):
                # Assume Intel/AMD x86 compat
                unix_lib_dirs_list += ["/lib/i386-linux-gnu", "/usr/lib/i386-linux-gnu"]
            elif bitage.startswith("64"):
                # Assume Intel/AMD x86 compatible
                unix_lib_dirs_list += [
                    "/lib/x86_64-linux-gnu",
                    "/usr/lib/x86_64-linux-gnu",
                ]
            else:
                # guess...
                unix_lib_dirs_list += glob.glob("/lib/*linux-gnu")
        directories.extend(unix_lib_dirs_list)

        cache = {}
        lib_re = re.compile(r"lib(.*)\.s[ol]")
        # ext_re = re.compile(r"\.s[ol]$")
        for our_dir in directories.ordered():
            try:
                for path in glob.glob("%s/*.s[ol]*" % our_dir):
                    file = os.path.basename(path)

                    # Index by filename
                    cache_i = cache.setdefault(file, set())
                    cache_i.add(path)

                    # Index by library name
                    match = lib_re.match(file)
                    if match:
                        library = match.group(1)
                        cache_i = cache.setdefault(library, set())
                        cache_i.add(path)
            except OSError:
                pass

        self._ld_so_cache = cache

    def getplatformpaths(self, libname):
        if self._ld_so_cache is None:
            self._create_ld_so_cache()

        result = self._ld_so_cache.get(libname, set())
        for i in result:
            # we iterate through all found paths for library, since we may have
            # actually found multiple architectures or other library types that
            # may not load
            yield i


# Windows


class WindowsLibraryLoader(LibraryLoader):
    """Library loader for Microsoft Windows"""

    name_formats = ["%s.dll", "lib%s.dll", "%slib.dll", "%s"]

    class Lookup(LibraryLoader.Lookup):
        """Lookup class for Windows libraries..."""

        def __init__(self, path):
            super(WindowsLibraryLoader.Lookup, self).__init__(path)
            self.access["stdcall"] = ctypes.windll.LoadLibrary(path)


# Platform switching

# If your value of sys.platform does not appear in this dict, please contact
# the Ctypesgen maintainers.

loaderclass = {
    "darwin": DarwinLibraryLoader,
    "cygwin": WindowsLibraryLoader,
    "win32": WindowsLibraryLoader,
    "msys": WindowsLibraryLoader,
}

load_library = loaderclass.get(sys.platform, PosixLibraryLoader)()


def add_library_search_dirs(other_dirs):
    """
    Add libraries to search paths.
    If library paths are relative, convert them to absolute with respect to this
    file's directory
    """
    for path in other_dirs:
        if not os.path.isabs(path):
            path = os.path.abspath(path)
        load_library.other_dirs.append(path)


del loaderclass

# End loader

add_library_search_dirs([])

# No libraries

# No modules

__uint8_t = c_ubyte# /usr/include/bits/types.h: 38

__uint16_t = c_ushort# /usr/include/bits/types.h: 40

__uint32_t = c_uint# /usr/include/bits/types.h: 42

__uint64_t = c_ulong# /usr/include/bits/types.h: 45

uint8_t = __uint8_t# /usr/include/bits/stdint-uintn.h: 24

uint16_t = __uint16_t# /usr/include/bits/stdint-uintn.h: 25

uint32_t = __uint32_t# /usr/include/bits/stdint-uintn.h: 26

uint64_t = __uint64_t# /usr/include/bits/stdint-uintn.h: 27

sai_status_t = c_int32# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 92

sai_switch_profile_id_t = uint32_t# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 93

sai_vlan_id_t = uint16_t# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 94

sai_attr_id_t = uint32_t# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 95

sai_cos_t = uint8_t# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 96

sai_queue_index_t = uint8_t# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 97

sai_mac_t = uint8_t * int(6)# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 98

sai_ip4_t = uint32_t# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 99

sai_ip6_t = uint8_t * int(16)# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 100

sai_switch_hash_seed_t = uint32_t# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 101

sai_label_id_t = uint32_t# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 102

sai_stat_id_t = uint32_t# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 103

sai_encrypt_key_t = uint8_t * int(32)# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 104

sai_auth_key_t = uint8_t * int(16)# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 105

sai_macsec_sak_t = uint8_t * int(32)# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 106

sai_macsec_auth_key_t = uint8_t * int(16)# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 107

sai_macsec_salt_t = uint8_t * int(12)# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 108

sai_uint64_t = uint64_t# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 122

sai_int64_t = c_int64# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 123

sai_uint32_t = uint32_t# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 124

sai_int32_t = c_int32# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 125

sai_uint16_t = uint16_t# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 126

sai_int16_t = c_int16# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 127

sai_uint8_t = uint8_t# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 128

sai_int8_t = c_int8# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 129

sai_size_t = c_size_t# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 130

sai_object_id_t = uint64_t# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 131

sai_pointer_t = POINTER(None)# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 132

sai_api_version_t = uint64_t# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 133

# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 139
class struct__sai_timespec_t(Structure):
    pass

struct__sai_timespec_t.__slots__ = [
    'tv_sec',
    'tv_nsec',
]
struct__sai_timespec_t._fields_ = [
    ('tv_sec', uint64_t),
    ('tv_nsec', uint32_t),
]

sai_timespec_t = struct__sai_timespec_t# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 139

# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 167
class struct__sai_object_list_t(Structure):
    pass

struct__sai_object_list_t.__slots__ = [
    'count',
    'list',
]
struct__sai_object_list_t._fields_ = [
    ('count', uint32_t),
    ('list', POINTER(sai_object_id_t)),
]

sai_object_list_t = struct__sai_object_list_t# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 167

enum__sai_common_api_t = c_int# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 183

SAI_COMMON_API_CREATE = 0# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 183

SAI_COMMON_API_REMOVE = 1# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 183

SAI_COMMON_API_SET = 2# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 183

SAI_COMMON_API_GET = 3# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 183

SAI_COMMON_API_BULK_CREATE = 4# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 183

SAI_COMMON_API_BULK_REMOVE = 5# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 183

SAI_COMMON_API_BULK_SET = 6# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 183

SAI_COMMON_API_BULK_GET = 7# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 183

SAI_COMMON_API_MAX = 8# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 183

sai_common_api_t = enum__sai_common_api_t# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 183

enum__sai_object_type_t = c_int# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 307

SAI_OBJECT_TYPE_NULL = 0# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 307

SAI_OBJECT_TYPE_PORT = 1# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 307

SAI_OBJECT_TYPE_LAG = 2# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 307

SAI_OBJECT_TYPE_VIRTUAL_ROUTER = 3# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 307

SAI_OBJECT_TYPE_NEXT_HOP = 4# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 307

SAI_OBJECT_TYPE_NEXT_HOP_GROUP = 5# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 307

SAI_OBJECT_TYPE_ROUTER_INTERFACE = 6# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 307

SAI_OBJECT_TYPE_ACL_TABLE = 7# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 307

SAI_OBJECT_TYPE_ACL_ENTRY = 8# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 307

SAI_OBJECT_TYPE_ACL_COUNTER = 9# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 307

SAI_OBJECT_TYPE_ACL_RANGE = 10# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 307

SAI_OBJECT_TYPE_ACL_TABLE_GROUP = 11# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 307

SAI_OBJECT_TYPE_ACL_TABLE_GROUP_MEMBER = 12# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 307

SAI_OBJECT_TYPE_HOSTIF = 13# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 307

SAI_OBJECT_TYPE_MIRROR_SESSION = 14# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 307

SAI_OBJECT_TYPE_SAMPLEPACKET = 15# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 307

SAI_OBJECT_TYPE_STP = 16# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 307

SAI_OBJECT_TYPE_HOSTIF_TRAP_GROUP = 17# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 307

SAI_OBJECT_TYPE_POLICER = 18# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 307

SAI_OBJECT_TYPE_WRED = 19# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 307

SAI_OBJECT_TYPE_QOS_MAP = 20# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 307

SAI_OBJECT_TYPE_QUEUE = 21# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 307

SAI_OBJECT_TYPE_SCHEDULER = 22# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 307

SAI_OBJECT_TYPE_SCHEDULER_GROUP = 23# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 307

SAI_OBJECT_TYPE_BUFFER_POOL = 24# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 307

SAI_OBJECT_TYPE_BUFFER_PROFILE = 25# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 307

SAI_OBJECT_TYPE_INGRESS_PRIORITY_GROUP = 26# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 307

SAI_OBJECT_TYPE_LAG_MEMBER = 27# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 307

SAI_OBJECT_TYPE_HASH = 28# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 307

SAI_OBJECT_TYPE_UDF = 29# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 307

SAI_OBJECT_TYPE_UDF_MATCH = 30# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 307

SAI_OBJECT_TYPE_UDF_GROUP = 31# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 307

SAI_OBJECT_TYPE_FDB_ENTRY = 32# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 307

SAI_OBJECT_TYPE_SWITCH = 33# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 307

SAI_OBJECT_TYPE_HOSTIF_TRAP = 34# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 307

SAI_OBJECT_TYPE_HOSTIF_TABLE_ENTRY = 35# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 307

SAI_OBJECT_TYPE_NEIGHBOR_ENTRY = 36# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 307

SAI_OBJECT_TYPE_ROUTE_ENTRY = 37# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 307

SAI_OBJECT_TYPE_VLAN = 38# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 307

SAI_OBJECT_TYPE_VLAN_MEMBER = 39# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 307

SAI_OBJECT_TYPE_HOSTIF_PACKET = 40# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 307

SAI_OBJECT_TYPE_TUNNEL_MAP = 41# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 307

SAI_OBJECT_TYPE_TUNNEL = 42# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 307

SAI_OBJECT_TYPE_TUNNEL_TERM_TABLE_ENTRY = 43# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 307

SAI_OBJECT_TYPE_FDB_FLUSH = 44# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 307

SAI_OBJECT_TYPE_NEXT_HOP_GROUP_MEMBER = 45# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 307

SAI_OBJECT_TYPE_STP_PORT = 46# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 307

SAI_OBJECT_TYPE_RPF_GROUP = 47# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 307

SAI_OBJECT_TYPE_RPF_GROUP_MEMBER = 48# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 307

SAI_OBJECT_TYPE_L2MC_GROUP = 49# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 307

SAI_OBJECT_TYPE_L2MC_GROUP_MEMBER = 50# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 307

SAI_OBJECT_TYPE_IPMC_GROUP = 51# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 307

SAI_OBJECT_TYPE_IPMC_GROUP_MEMBER = 52# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 307

SAI_OBJECT_TYPE_L2MC_ENTRY = 53# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 307

SAI_OBJECT_TYPE_IPMC_ENTRY = 54# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 307

SAI_OBJECT_TYPE_MCAST_FDB_ENTRY = 55# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 307

SAI_OBJECT_TYPE_HOSTIF_USER_DEFINED_TRAP = 56# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 307

SAI_OBJECT_TYPE_BRIDGE = 57# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 307

SAI_OBJECT_TYPE_BRIDGE_PORT = 58# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 307

SAI_OBJECT_TYPE_TUNNEL_MAP_ENTRY = 59# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 307

SAI_OBJECT_TYPE_TAM = 60# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 307

SAI_OBJECT_TYPE_SRV6_SIDLIST = 61# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 307

SAI_OBJECT_TYPE_PORT_POOL = 62# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 307

SAI_OBJECT_TYPE_INSEG_ENTRY = 63# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 307

SAI_OBJECT_TYPE_DTEL = 64# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 307

SAI_OBJECT_TYPE_DTEL_QUEUE_REPORT = 65# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 307

SAI_OBJECT_TYPE_DTEL_INT_SESSION = 66# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 307

SAI_OBJECT_TYPE_DTEL_REPORT_SESSION = 67# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 307

SAI_OBJECT_TYPE_DTEL_EVENT = 68# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 307

SAI_OBJECT_TYPE_BFD_SESSION = 69# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 307

SAI_OBJECT_TYPE_ISOLATION_GROUP = 70# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 307

SAI_OBJECT_TYPE_ISOLATION_GROUP_MEMBER = 71# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 307

SAI_OBJECT_TYPE_TAM_MATH_FUNC = 72# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 307

SAI_OBJECT_TYPE_TAM_REPORT = 73# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 307

SAI_OBJECT_TYPE_TAM_EVENT_THRESHOLD = 74# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 307

SAI_OBJECT_TYPE_TAM_TEL_TYPE = 75# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 307

SAI_OBJECT_TYPE_TAM_TRANSPORT = 76# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 307

SAI_OBJECT_TYPE_TAM_TELEMETRY = 77# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 307

SAI_OBJECT_TYPE_TAM_COLLECTOR = 78# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 307

SAI_OBJECT_TYPE_TAM_EVENT_ACTION = 79# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 307

SAI_OBJECT_TYPE_TAM_EVENT = 80# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 307

SAI_OBJECT_TYPE_NAT_ZONE_COUNTER = 81# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 307

SAI_OBJECT_TYPE_NAT_ENTRY = 82# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 307

SAI_OBJECT_TYPE_TAM_INT = 83# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 307

SAI_OBJECT_TYPE_COUNTER = 84# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 307

SAI_OBJECT_TYPE_DEBUG_COUNTER = 85# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 307

SAI_OBJECT_TYPE_PORT_CONNECTOR = 86# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 307

SAI_OBJECT_TYPE_PORT_SERDES = 87# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 307

SAI_OBJECT_TYPE_MACSEC = 88# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 307

SAI_OBJECT_TYPE_MACSEC_PORT = 89# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 307

SAI_OBJECT_TYPE_MACSEC_FLOW = 90# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 307

SAI_OBJECT_TYPE_MACSEC_SC = 91# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 307

SAI_OBJECT_TYPE_MACSEC_SA = 92# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 307

SAI_OBJECT_TYPE_SYSTEM_PORT = 93# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 307

SAI_OBJECT_TYPE_FINE_GRAINED_HASH_FIELD = 94# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 307

SAI_OBJECT_TYPE_SWITCH_TUNNEL = 95# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 307

SAI_OBJECT_TYPE_MY_SID_ENTRY = 96# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 307

SAI_OBJECT_TYPE_MY_MAC = 97# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 307

SAI_OBJECT_TYPE_NEXT_HOP_GROUP_MAP = 98# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 307

SAI_OBJECT_TYPE_IPSEC = 99# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 307

SAI_OBJECT_TYPE_IPSEC_PORT = 100# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 307

SAI_OBJECT_TYPE_IPSEC_SA = 101# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 307

SAI_OBJECT_TYPE_GENERIC_PROGRAMMABLE = 102# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 307

SAI_OBJECT_TYPE_ARS_PROFILE = 103# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 307

SAI_OBJECT_TYPE_ARS = 104# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 307

SAI_OBJECT_TYPE_ACL_TABLE_CHAIN_GROUP = 105# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 307

SAI_OBJECT_TYPE_TWAMP_SESSION = 106# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 307

SAI_OBJECT_TYPE_TAM_COUNTER_SUBSCRIPTION = 107# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 307

SAI_OBJECT_TYPE_MAX = (SAI_OBJECT_TYPE_TAM_COUNTER_SUBSCRIPTION + 1)# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 307

SAI_OBJECT_TYPE_CUSTOM_RANGE_START = 256# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 307

SAI_OBJECT_TYPE_CUSTOM_RANGE_END = (SAI_OBJECT_TYPE_CUSTOM_RANGE_START + 1)# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 307

sai_object_type_t = enum__sai_object_type_t# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 307

# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 313
class struct__sai_u8_list_t(Structure):
    pass

struct__sai_u8_list_t.__slots__ = [
    'count',
    'list',
]
struct__sai_u8_list_t._fields_ = [
    ('count', uint32_t),
    ('list', POINTER(uint8_t)),
]

sai_u8_list_t = struct__sai_u8_list_t# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 313

# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 324
class struct__sai_s8_list_t(Structure):
    pass

struct__sai_s8_list_t.__slots__ = [
    'count',
    'list',
]
struct__sai_s8_list_t._fields_ = [
    ('count', uint32_t),
    ('list', POINTER(c_int8)),
]

sai_s8_list_t = struct__sai_s8_list_t# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 324

# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 330
class struct__sai_u16_list_t(Structure):
    pass

struct__sai_u16_list_t.__slots__ = [
    'count',
    'list',
]
struct__sai_u16_list_t._fields_ = [
    ('count', uint32_t),
    ('list', POINTER(uint16_t)),
]

sai_u16_list_t = struct__sai_u16_list_t# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 330

# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 336
class struct__sai_s16_list_t(Structure):
    pass

struct__sai_s16_list_t.__slots__ = [
    'count',
    'list',
]
struct__sai_s16_list_t._fields_ = [
    ('count', uint32_t),
    ('list', POINTER(c_int16)),
]

sai_s16_list_t = struct__sai_s16_list_t# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 336

# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 342
class struct__sai_u32_list_t(Structure):
    pass

struct__sai_u32_list_t.__slots__ = [
    'count',
    'list',
]
struct__sai_u32_list_t._fields_ = [
    ('count', uint32_t),
    ('list', POINTER(uint32_t)),
]

sai_u32_list_t = struct__sai_u32_list_t# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 342

# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 348
class struct__sai_s32_list_t(Structure):
    pass

struct__sai_s32_list_t.__slots__ = [
    'count',
    'list',
]
struct__sai_s32_list_t._fields_ = [
    ('count', uint32_t),
    ('list', POINTER(c_int32)),
]

sai_s32_list_t = struct__sai_s32_list_t# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 348

# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 354
class struct__sai_u32_range_t(Structure):
    pass

struct__sai_u32_range_t.__slots__ = [
    'min',
    'max',
]
struct__sai_u32_range_t._fields_ = [
    ('min', uint32_t),
    ('max', uint32_t),
]

sai_u32_range_t = struct__sai_u32_range_t# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 354

# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 360
class struct__sai_s32_range_t(Structure):
    pass

struct__sai_s32_range_t.__slots__ = [
    'min',
    'max',
]
struct__sai_s32_range_t._fields_ = [
    ('min', c_int32),
    ('max', c_int32),
]

sai_s32_range_t = struct__sai_s32_range_t# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 360

# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 366
class struct__sai_u16_range_t(Structure):
    pass

struct__sai_u16_range_t.__slots__ = [
    'min',
    'max',
]
struct__sai_u16_range_t._fields_ = [
    ('min', uint16_t),
    ('max', uint16_t),
]

sai_u16_range_t = struct__sai_u16_range_t# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 366

# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 372
class struct__sai_u16_range_list_t(Structure):
    pass

struct__sai_u16_range_list_t.__slots__ = [
    'count',
    'list',
]
struct__sai_u16_range_list_t._fields_ = [
    ('count', uint32_t),
    ('list', POINTER(sai_u16_range_t)),
]

sai_u16_range_list_t = struct__sai_u16_range_list_t# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 372

# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 385
class struct__sai_vlan_list_t(Structure):
    pass

struct__sai_vlan_list_t.__slots__ = [
    'count',
    'list',
]
struct__sai_vlan_list_t._fields_ = [
    ('count', uint32_t),
    ('list', POINTER(sai_vlan_id_t)),
]

sai_vlan_list_t = struct__sai_vlan_list_t# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 385

enum__sai_ip_addr_family_t = c_int# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 393

SAI_IP_ADDR_FAMILY_IPV4 = 0# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 393

SAI_IP_ADDR_FAMILY_IPV6 = (SAI_IP_ADDR_FAMILY_IPV4 + 1)# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 393

sai_ip_addr_family_t = enum__sai_ip_addr_family_t# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 393

# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 405
class union__sai_ip_addr_t(Union):
    pass

union__sai_ip_addr_t.__slots__ = [
    'ip4',
    'ip6',
]
union__sai_ip_addr_t._fields_ = [
    ('ip4', sai_ip4_t),
    ('ip6', sai_ip6_t),
]

sai_ip_addr_t = union__sai_ip_addr_t# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 405

# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 413
class struct__sai_ip_address_t(Structure):
    pass

struct__sai_ip_address_t.__slots__ = [
    'addr_family',
    'addr',
]
struct__sai_ip_address_t._fields_ = [
    ('addr_family', sai_ip_addr_family_t),
    ('addr', sai_ip_addr_t),
]

sai_ip_address_t = struct__sai_ip_address_t# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 413

# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 419
class struct__sai_ip_address_list_t(Structure):
    pass

struct__sai_ip_address_list_t.__slots__ = [
    'count',
    'list',
]
struct__sai_ip_address_list_t._fields_ = [
    ('count', uint32_t),
    ('list', POINTER(sai_ip_address_t)),
]

sai_ip_address_list_t = struct__sai_ip_address_list_t# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 419

# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 430
class struct__sai_ip_prefix_t(Structure):
    pass

struct__sai_ip_prefix_t.__slots__ = [
    'addr_family',
    'addr',
    'mask',
]
struct__sai_ip_prefix_t._fields_ = [
    ('addr_family', sai_ip_addr_family_t),
    ('addr', sai_ip_addr_t),
    ('mask', sai_ip_addr_t),
]

sai_ip_prefix_t = struct__sai_ip_prefix_t# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 430

# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 436
class struct__sai_ip_prefix_list_t(Structure):
    pass

struct__sai_ip_prefix_list_t.__slots__ = [
    'count',
    'list',
]
struct__sai_ip_prefix_list_t._fields_ = [
    ('count', uint32_t),
    ('list', POINTER(sai_ip_prefix_t)),
]

sai_ip_prefix_list_t = struct__sai_ip_prefix_list_t# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 436

enum__sai_port_prbs_rx_status_t = c_int# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 455

SAI_PORT_PRBS_RX_STATUS_OK = 0# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 455

SAI_PORT_PRBS_RX_STATUS_LOCK_WITH_ERRORS = (SAI_PORT_PRBS_RX_STATUS_OK + 1)# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 455

SAI_PORT_PRBS_RX_STATUS_NOT_LOCKED = (SAI_PORT_PRBS_RX_STATUS_LOCK_WITH_ERRORS + 1)# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 455

SAI_PORT_PRBS_RX_STATUS_LOST_LOCK = (SAI_PORT_PRBS_RX_STATUS_NOT_LOCKED + 1)# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 455

sai_port_prbs_rx_status_t = enum__sai_port_prbs_rx_status_t# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 455

# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 462
class struct__sai_prbs_rx_state_t(Structure):
    pass

struct__sai_prbs_rx_state_t.__slots__ = [
    'rx_status',
    'error_count',
]
struct__sai_prbs_rx_state_t._fields_ = [
    ('rx_status', sai_port_prbs_rx_status_t),
    ('error_count', uint32_t),
]

sai_prbs_rx_state_t = struct__sai_prbs_rx_state_t# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 462

# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 471
class struct__sai_latch_status_t(Structure):
    pass

struct__sai_latch_status_t.__slots__ = [
    'current_status',
    'changed',
]
struct__sai_latch_status_t._fields_ = [
    ('current_status', c_bool),
    ('changed', c_bool),
]

sai_latch_status_t = struct__sai_latch_status_t# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 471

# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 477
class struct__sai_port_lane_latch_status_t(Structure):
    pass

struct__sai_port_lane_latch_status_t.__slots__ = [
    'lane',
    'value',
]
struct__sai_port_lane_latch_status_t._fields_ = [
    ('lane', uint32_t),
    ('value', sai_latch_status_t),
]

sai_port_lane_latch_status_t = struct__sai_port_lane_latch_status_t# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 477

# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 483
class struct__sai_port_lane_latch_status_list_t(Structure):
    pass

struct__sai_port_lane_latch_status_list_t.__slots__ = [
    'count',
    'list',
]
struct__sai_port_lane_latch_status_list_t._fields_ = [
    ('count', uint32_t),
    ('list', POINTER(sai_port_lane_latch_status_t)),
]

sai_port_lane_latch_status_list_t = struct__sai_port_lane_latch_status_list_t# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 483

# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 524
class union__sai_acl_field_data_mask_t(Union):
    pass

union__sai_acl_field_data_mask_t.__slots__ = [
    'u8',
    's8',
    'u16',
    's16',
    'u32',
    's32',
    'u64',
    'mac',
    'ip4',
    'ip6',
    'u8list',
]
union__sai_acl_field_data_mask_t._fields_ = [
    ('u8', sai_uint8_t),
    ('s8', sai_int8_t),
    ('u16', sai_uint16_t),
    ('s16', sai_int16_t),
    ('u32', sai_uint32_t),
    ('s32', sai_int32_t),
    ('u64', sai_uint64_t),
    ('mac', sai_mac_t),
    ('ip4', sai_ip4_t),
    ('ip6', sai_ip6_t),
    ('u8list', sai_u8_list_t),
]

sai_acl_field_data_mask_t = union__sai_acl_field_data_mask_t# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 524

# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 578
class union__sai_acl_field_data_data_t(Union):
    pass

union__sai_acl_field_data_data_t.__slots__ = [
    'booldata',
    'u8',
    's8',
    'u16',
    's16',
    'u32',
    's32',
    'u64',
    'mac',
    'ip4',
    'ip6',
    'oid',
    'objlist',
    'u8list',
]
union__sai_acl_field_data_data_t._fields_ = [
    ('booldata', c_bool),
    ('u8', sai_uint8_t),
    ('s8', sai_int8_t),
    ('u16', sai_uint16_t),
    ('s16', sai_int16_t),
    ('u32', sai_uint32_t),
    ('s32', sai_int32_t),
    ('u64', sai_uint64_t),
    ('mac', sai_mac_t),
    ('ip4', sai_ip4_t),
    ('ip6', sai_ip6_t),
    ('oid', sai_object_id_t),
    ('objlist', sai_object_list_t),
    ('u8list', sai_u8_list_t),
]

sai_acl_field_data_data_t = union__sai_acl_field_data_data_t# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 578

# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 613
class struct__sai_acl_field_data_t(Structure):
    pass

struct__sai_acl_field_data_t.__slots__ = [
    'enable',
    'mask',
    'data',
]
struct__sai_acl_field_data_t._fields_ = [
    ('enable', c_bool),
    ('mask', sai_acl_field_data_mask_t),
    ('data', sai_acl_field_data_data_t),
]

sai_acl_field_data_t = struct__sai_acl_field_data_t# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 613

# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 662
class union__sai_acl_action_parameter_t(Union):
    pass

union__sai_acl_action_parameter_t.__slots__ = [
    'booldata',
    'u8',
    's8',
    'u16',
    's16',
    'u32',
    's32',
    'mac',
    'ip4',
    'ip6',
    'oid',
    'objlist',
    'ipaddr',
]
union__sai_acl_action_parameter_t._fields_ = [
    ('booldata', c_bool),
    ('u8', sai_uint8_t),
    ('s8', sai_int8_t),
    ('u16', sai_uint16_t),
    ('s16', sai_int16_t),
    ('u32', sai_uint32_t),
    ('s32', sai_int32_t),
    ('mac', sai_mac_t),
    ('ip4', sai_ip4_t),
    ('ip6', sai_ip6_t),
    ('oid', sai_object_id_t),
    ('objlist', sai_object_list_t),
    ('ipaddr', sai_ip_address_t),
]

sai_acl_action_parameter_t = union__sai_acl_action_parameter_t# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 662

# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 686
class struct__sai_acl_action_data_t(Structure):
    pass

struct__sai_acl_action_data_t.__slots__ = [
    'enable',
    'parameter',
]
struct__sai_acl_action_data_t._fields_ = [
    ('enable', c_bool),
    ('parameter', sai_acl_action_parameter_t),
]

sai_acl_action_data_t = struct__sai_acl_action_data_t# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 686

enum__sai_packet_color_t = c_int# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 708

SAI_PACKET_COLOR_GREEN = 0# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 708

SAI_PACKET_COLOR_YELLOW = (SAI_PACKET_COLOR_GREEN + 1)# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 708

SAI_PACKET_COLOR_RED = (SAI_PACKET_COLOR_YELLOW + 1)# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 708

sai_packet_color_t = enum__sai_packet_color_t# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 708

# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 755
class struct__sai_qos_map_params_t(Structure):
    pass

struct__sai_qos_map_params_t.__slots__ = [
    'tc',
    'dscp',
    'dot1p',
    'prio',
    'pg',
    'queue_index',
    'color',
    'mpls_exp',
    'fc',
]
struct__sai_qos_map_params_t._fields_ = [
    ('tc', sai_cos_t),
    ('dscp', sai_uint8_t),
    ('dot1p', sai_uint8_t),
    ('prio', sai_uint8_t),
    ('pg', sai_uint8_t),
    ('queue_index', sai_queue_index_t),
    ('color', sai_packet_color_t),
    ('mpls_exp', sai_uint8_t),
    ('fc', sai_uint8_t),
]

sai_qos_map_params_t = struct__sai_qos_map_params_t# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 755

# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 765
class struct__sai_qos_map_t(Structure):
    pass

struct__sai_qos_map_t.__slots__ = [
    'key',
    'value',
]
struct__sai_qos_map_t._fields_ = [
    ('key', sai_qos_map_params_t),
    ('value', sai_qos_map_params_t),
]

sai_qos_map_t = struct__sai_qos_map_t# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 765

# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 775
class struct__sai_qos_map_list_t(Structure):
    pass

struct__sai_qos_map_list_t.__slots__ = [
    'count',
    'list',
]
struct__sai_qos_map_list_t._fields_ = [
    ('count', uint32_t),
    ('list', POINTER(sai_qos_map_t)),
]

sai_qos_map_list_t = struct__sai_qos_map_list_t# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 775

# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 785
class struct__sai_map_t(Structure):
    pass

struct__sai_map_t.__slots__ = [
    'key',
    'value',
]
struct__sai_map_t._fields_ = [
    ('key', sai_uint32_t),
    ('value', sai_int32_t),
]

sai_map_t = struct__sai_map_t# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 785

# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 795
class struct__sai_map_list_t(Structure):
    pass

struct__sai_map_list_t.__slots__ = [
    'count',
    'list',
]
struct__sai_map_list_t._fields_ = [
    ('count', uint32_t),
    ('list', POINTER(sai_map_t)),
]

sai_map_list_t = struct__sai_map_list_t# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 795

enum__sai_acl_table_supported_match_type_t = c_int# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 808

SAI_ACL_TABLE_SUPPORTED_MATCH_TYPE_TERNARY = 0# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 808

SAI_ACL_TABLE_SUPPORTED_MATCH_TYPE_EXACT = (SAI_ACL_TABLE_SUPPORTED_MATCH_TYPE_TERNARY + 1)# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 808

sai_acl_table_supported_match_type_t = enum__sai_acl_table_supported_match_type_t# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 808

enum__sai_acl_table_chain_group_stage_t = c_int# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 827

SAI_ACL_TABLE_CHAIN_GROUP_STAGE_0 = 0# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 827

SAI_ACL_TABLE_CHAIN_GROUP_STAGE_1 = (SAI_ACL_TABLE_CHAIN_GROUP_STAGE_0 + 1)# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 827

SAI_ACL_TABLE_CHAIN_GROUP_STAGE_2 = (SAI_ACL_TABLE_CHAIN_GROUP_STAGE_1 + 1)# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 827

SAI_ACL_TABLE_CHAIN_GROUP_STAGE_3 = (SAI_ACL_TABLE_CHAIN_GROUP_STAGE_2 + 1)# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 827

sai_acl_table_chain_group_stage_t = enum__sai_acl_table_chain_group_stage_t# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 827

# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 839
class struct__sai_acl_chain_t(Structure):
    pass

struct__sai_acl_chain_t.__slots__ = [
    'chain_group_stage',
    'supported_match_type',
]
struct__sai_acl_chain_t._fields_ = [
    ('chain_group_stage', sai_acl_table_chain_group_stage_t),
    ('supported_match_type', sai_acl_table_supported_match_type_t),
]

sai_acl_chain_t = struct__sai_acl_chain_t# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 839

# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 849
class struct__sai_acl_chain_list_t(Structure):
    pass

struct__sai_acl_chain_list_t.__slots__ = [
    'count',
    'list',
]
struct__sai_acl_chain_list_t._fields_ = [
    ('count', uint32_t),
    ('list', POINTER(sai_acl_chain_t)),
]

sai_acl_chain_list_t = struct__sai_acl_chain_list_t# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 849

# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 890
class struct__sai_acl_capability_t(Structure):
    pass

struct__sai_acl_capability_t.__slots__ = [
    'is_action_list_mandatory',
    'action_list',
    'supported_match_type',
    'is_non_contiguous_bits_exact_match_supported',
]
struct__sai_acl_capability_t._fields_ = [
    ('is_action_list_mandatory', c_bool),
    ('action_list', sai_s32_list_t),
    ('supported_match_type', sai_acl_table_supported_match_type_t),
    ('is_non_contiguous_bits_exact_match_supported', c_bool),
]

sai_acl_capability_t = struct__sai_acl_capability_t# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 890

enum__sai_acl_stage_t = c_int# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 915

SAI_ACL_STAGE_INGRESS = 0# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 915

SAI_ACL_STAGE_EGRESS = (SAI_ACL_STAGE_INGRESS + 1)# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 915

SAI_ACL_STAGE_INGRESS_MACSEC = (SAI_ACL_STAGE_EGRESS + 1)# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 915

SAI_ACL_STAGE_EGRESS_MACSEC = (SAI_ACL_STAGE_INGRESS_MACSEC + 1)# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 915

SAI_ACL_STAGE_PRE_INGRESS = (SAI_ACL_STAGE_EGRESS_MACSEC + 1)# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 915

SAI_ACL_STAGE_POST_INGRESS = (SAI_ACL_STAGE_PRE_INGRESS + 1)# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 915

sai_acl_stage_t = enum__sai_acl_stage_t# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 915

enum__sai_acl_bind_point_type_t = c_int# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 940

SAI_ACL_BIND_POINT_TYPE_PORT = 0# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 940

SAI_ACL_BIND_POINT_TYPE_LAG = (SAI_ACL_BIND_POINT_TYPE_PORT + 1)# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 940

SAI_ACL_BIND_POINT_TYPE_VLAN = (SAI_ACL_BIND_POINT_TYPE_LAG + 1)# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 940

SAI_ACL_BIND_POINT_TYPE_ROUTER_INTERFACE = (SAI_ACL_BIND_POINT_TYPE_VLAN + 1)# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 940

SAI_ACL_BIND_POINT_TYPE_ROUTER_INTF = SAI_ACL_BIND_POINT_TYPE_ROUTER_INTERFACE# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 940

SAI_ACL_BIND_POINT_TYPE_SWITCH = (SAI_ACL_BIND_POINT_TYPE_ROUTER_INTF + 1)# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 940

sai_acl_bind_point_type_t = enum__sai_acl_bind_point_type_t# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 940

enum__sai_acl_table_match_type_t = c_int# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 953

SAI_ACL_TABLE_MATCH_TYPE_TERNARY = 0# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 953

SAI_ACL_TABLE_MATCH_TYPE_EXACT = (SAI_ACL_TABLE_MATCH_TYPE_TERNARY + 1)# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 953

sai_acl_table_match_type_t = enum__sai_acl_table_match_type_t# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 953

enum__sai_tam_bind_point_type_t = c_int# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 981

SAI_TAM_BIND_POINT_TYPE_QUEUE = 0# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 981

SAI_TAM_BIND_POINT_TYPE_PORT = (SAI_TAM_BIND_POINT_TYPE_QUEUE + 1)# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 981

SAI_TAM_BIND_POINT_TYPE_LAG = (SAI_TAM_BIND_POINT_TYPE_PORT + 1)# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 981

SAI_TAM_BIND_POINT_TYPE_VLAN = (SAI_TAM_BIND_POINT_TYPE_LAG + 1)# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 981

SAI_TAM_BIND_POINT_TYPE_SWITCH = (SAI_TAM_BIND_POINT_TYPE_VLAN + 1)# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 981

SAI_TAM_BIND_POINT_TYPE_IPG = (SAI_TAM_BIND_POINT_TYPE_SWITCH + 1)# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 981

SAI_TAM_BIND_POINT_TYPE_BSP = (SAI_TAM_BIND_POINT_TYPE_IPG + 1)# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 981

sai_tam_bind_point_type_t = enum__sai_tam_bind_point_type_t# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 981

# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 997
class struct__sai_acl_resource_t(Structure):
    pass

struct__sai_acl_resource_t.__slots__ = [
    'stage',
    'bind_point',
    'avail_num',
]
struct__sai_acl_resource_t._fields_ = [
    ('stage', sai_acl_stage_t),
    ('bind_point', sai_acl_bind_point_type_t),
    ('avail_num', sai_uint32_t),
]

sai_acl_resource_t = struct__sai_acl_resource_t# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 997

# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 1013
class struct__sai_acl_resource_list_t(Structure):
    pass

struct__sai_acl_resource_list_t.__slots__ = [
    'count',
    'list',
]
struct__sai_acl_resource_list_t._fields_ = [
    ('count', uint32_t),
    ('list', POINTER(sai_acl_resource_t)),
]

sai_acl_resource_list_t = struct__sai_acl_resource_list_t# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 1013

enum__sai_tlv_type_t = c_int# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 1031

SAI_TLV_TYPE_INGRESS = 0# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 1031

SAI_TLV_TYPE_EGRESS = (SAI_TLV_TYPE_INGRESS + 1)# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 1031

SAI_TLV_TYPE_OPAQUE = (SAI_TLV_TYPE_EGRESS + 1)# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 1031

SAI_TLV_TYPE_HMAC = (SAI_TLV_TYPE_OPAQUE + 1)# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 1031

sai_tlv_type_t = enum__sai_tlv_type_t# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 1031

# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 1041
class struct__sai_hmac_t(Structure):
    pass

struct__sai_hmac_t.__slots__ = [
    'key_id',
    'hmac',
]
struct__sai_hmac_t._fields_ = [
    ('key_id', sai_uint32_t),
    ('hmac', sai_uint32_t * int(8)),
]

sai_hmac_t = struct__sai_hmac_t# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 1041

# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 1059
class union__sai_tlv_entry_t(Union):
    pass

union__sai_tlv_entry_t.__slots__ = [
    'ingress_node',
    'egress_node',
    'opaque_container',
    'hmac',
]
union__sai_tlv_entry_t._fields_ = [
    ('ingress_node', sai_ip6_t),
    ('egress_node', sai_ip6_t),
    ('opaque_container', sai_uint32_t * int(4)),
    ('hmac', sai_hmac_t),
]

sai_tlv_entry_t = union__sai_tlv_entry_t# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 1059

# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 1070
class struct__sai_tlv_t(Structure):
    pass

struct__sai_tlv_t.__slots__ = [
    'tlv_type',
    'entry',
]
struct__sai_tlv_t._fields_ = [
    ('tlv_type', sai_tlv_type_t),
    ('entry', sai_tlv_entry_t),
]

sai_tlv_t = struct__sai_tlv_t# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 1070

# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 1082
class struct__sai_tlv_list_t(Structure):
    pass

struct__sai_tlv_list_t.__slots__ = [
    'count',
    'list',
]
struct__sai_tlv_list_t._fields_ = [
    ('count', uint32_t),
    ('list', POINTER(sai_tlv_t)),
]

sai_tlv_list_t = struct__sai_tlv_list_t# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 1082

# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 1094
class struct__sai_segment_list_t(Structure):
    pass

struct__sai_segment_list_t.__slots__ = [
    'count',
    'list',
]
struct__sai_segment_list_t._fields_ = [
    ('count', uint32_t),
    ('list', POINTER(sai_ip6_t)),
]

sai_segment_list_t = struct__sai_segment_list_t# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 1094

# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 1123
class struct__sai_json_t(Structure):
    pass

struct__sai_json_t.__slots__ = [
    'json',
]
struct__sai_json_t._fields_ = [
    ('json', sai_s8_list_t),
]

sai_json_t = struct__sai_json_t# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 1123

# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 1136
class struct__sai_port_lane_eye_values_t(Structure):
    pass

struct__sai_port_lane_eye_values_t.__slots__ = [
    'lane',
    'left',
    'right',
    'up',
    'down',
]
struct__sai_port_lane_eye_values_t._fields_ = [
    ('lane', uint32_t),
    ('left', c_int32),
    ('right', c_int32),
    ('up', c_int32),
    ('down', c_int32),
]

sai_port_lane_eye_values_t = struct__sai_port_lane_eye_values_t# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 1136

# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 1158
class struct__sai_port_eye_values_list_t(Structure):
    pass

struct__sai_port_eye_values_list_t.__slots__ = [
    'count',
    'list',
]
struct__sai_port_eye_values_list_t._fields_ = [
    ('count', uint32_t),
    ('list', POINTER(sai_port_lane_eye_values_t)),
]

sai_port_eye_values_list_t = struct__sai_port_eye_values_list_t# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 1158

# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 1167
class struct__sai_port_frequency_offset_ppm_values_t(Structure):
    pass

struct__sai_port_frequency_offset_ppm_values_t.__slots__ = [
    'lane',
    'ppm',
]
struct__sai_port_frequency_offset_ppm_values_t._fields_ = [
    ('lane', uint32_t),
    ('ppm', sai_int16_t),
]

sai_port_frequency_offset_ppm_values_t = struct__sai_port_frequency_offset_ppm_values_t# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 1167

# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 1176
class struct__sai_port_frequency_offset_ppm_list_t(Structure):
    pass

struct__sai_port_frequency_offset_ppm_list_t.__slots__ = [
    'count',
    'list',
]
struct__sai_port_frequency_offset_ppm_list_t._fields_ = [
    ('count', uint32_t),
    ('list', POINTER(sai_port_frequency_offset_ppm_values_t)),
]

sai_port_frequency_offset_ppm_list_t = struct__sai_port_frequency_offset_ppm_list_t# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 1176

# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 1188
class struct__sai_port_snr_values_t(Structure):
    pass

struct__sai_port_snr_values_t.__slots__ = [
    'lane',
    'snr',
]
struct__sai_port_snr_values_t._fields_ = [
    ('lane', uint32_t),
    ('snr', sai_uint16_t),
]

sai_port_snr_values_t = struct__sai_port_snr_values_t# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 1188

# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 1197
class struct__sai_port_snr_list_t(Structure):
    pass

struct__sai_port_snr_list_t.__slots__ = [
    'count',
    'list',
]
struct__sai_port_snr_list_t._fields_ = [
    ('count', uint32_t),
    ('list', POINTER(sai_port_snr_values_t)),
]

sai_port_snr_list_t = struct__sai_port_snr_list_t# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 1197

enum__sai_outseg_type_t = c_int# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 1210

SAI_OUTSEG_TYPE_PUSH = 0# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 1210

SAI_OUTSEG_TYPE_SWAP = (SAI_OUTSEG_TYPE_PUSH + 1)# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 1210

sai_outseg_type_t = enum__sai_outseg_type_t# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 1210

enum__sai_outseg_ttl_mode_t = c_int# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 1221

SAI_OUTSEG_TTL_MODE_UNIFORM = 0# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 1221

SAI_OUTSEG_TTL_MODE_PIPE = (SAI_OUTSEG_TTL_MODE_UNIFORM + 1)# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 1221

sai_outseg_ttl_mode_t = enum__sai_outseg_ttl_mode_t# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 1221

enum__sai_outseg_exp_mode_t = c_int# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 1232

SAI_OUTSEG_EXP_MODE_UNIFORM = 0# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 1232

SAI_OUTSEG_EXP_MODE_PIPE = (SAI_OUTSEG_EXP_MODE_UNIFORM + 1)# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 1232

sai_outseg_exp_mode_t = enum__sai_outseg_exp_mode_t# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 1232

# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 1262
class struct__sai_system_port_config_t(Structure):
    pass

struct__sai_system_port_config_t.__slots__ = [
    'port_id',
    'attached_switch_id',
    'attached_core_index',
    'attached_core_port_index',
    'speed',
    'num_voq',
]
struct__sai_system_port_config_t._fields_ = [
    ('port_id', uint32_t),
    ('attached_switch_id', uint32_t),
    ('attached_core_index', uint32_t),
    ('attached_core_port_index', uint32_t),
    ('speed', uint32_t),
    ('num_voq', uint32_t),
]

sai_system_port_config_t = struct__sai_system_port_config_t# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 1262

# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 1274
class struct__sai_system_port_config_list_t(Structure):
    pass

struct__sai_system_port_config_list_t.__slots__ = [
    'count',
    'list',
]
struct__sai_system_port_config_list_t._fields_ = [
    ('count', uint32_t),
    ('list', POINTER(sai_system_port_config_t)),
]

sai_system_port_config_list_t = struct__sai_system_port_config_list_t# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 1274

# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 1286
class struct__sai_fabric_port_reachability_t(Structure):
    pass

struct__sai_fabric_port_reachability_t.__slots__ = [
    'switch_id',
    'reachable',
]
struct__sai_fabric_port_reachability_t._fields_ = [
    ('switch_id', uint32_t),
    ('reachable', c_bool),
]

sai_fabric_port_reachability_t = struct__sai_fabric_port_reachability_t# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 1286

enum__sai_port_err_status_t = c_int# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 1319

SAI_PORT_ERR_STATUS_DATA_UNIT_CRC_ERROR = 0# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 1319

SAI_PORT_ERR_STATUS_DATA_UNIT_SIZE = (SAI_PORT_ERR_STATUS_DATA_UNIT_CRC_ERROR + 1)# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 1319

SAI_PORT_ERR_STATUS_DATA_UNIT_MISALIGNMENT_ERROR = (SAI_PORT_ERR_STATUS_DATA_UNIT_SIZE + 1)# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 1319

SAI_PORT_ERR_STATUS_CODE_GROUP_ERROR = (SAI_PORT_ERR_STATUS_DATA_UNIT_MISALIGNMENT_ERROR + 1)# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 1319

SAI_PORT_ERR_STATUS_SIGNAL_LOCAL_ERROR = (SAI_PORT_ERR_STATUS_CODE_GROUP_ERROR + 1)# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 1319

SAI_PORT_ERR_STATUS_NO_RX_REACHABILITY = (SAI_PORT_ERR_STATUS_SIGNAL_LOCAL_ERROR + 1)# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 1319

SAI_PORT_ERR_STATUS_CRC_RATE = (SAI_PORT_ERR_STATUS_NO_RX_REACHABILITY + 1)# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 1319

SAI_PORT_ERR_STATUS_REMOTE_FAULT_STATUS = (SAI_PORT_ERR_STATUS_CRC_RATE + 1)# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 1319

SAI_PORT_ERR_STATUS_MAX = (SAI_PORT_ERR_STATUS_REMOTE_FAULT_STATUS + 1)# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 1319

sai_port_err_status_t = enum__sai_port_err_status_t# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 1319

# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 1331
class struct__sai_port_err_status_list_t(Structure):
    pass

struct__sai_port_err_status_list_t.__slots__ = [
    'count',
    'list',
]
struct__sai_port_err_status_list_t._fields_ = [
    ('count', uint32_t),
    ('list', POINTER(sai_port_err_status_t)),
]

sai_port_err_status_list_t = struct__sai_port_err_status_list_t# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 1331

# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 1531
class union__sai_attribute_value_t(Union):
    pass

union__sai_attribute_value_t.__slots__ = [
    'booldata',
    'chardata',
    'u8',
    's8',
    'u16',
    's16',
    'u32',
    's32',
    'u64',
    's64',
    'ptr',
    'mac',
    'ip4',
    'ip6',
    'ipaddr',
    'ipprefix',
    'rx_state',
    'oid',
    'objlist',
    'u8list',
    's8list',
    'u16list',
    's16list',
    'u32list',
    's32list',
    'u32range',
    's32range',
    'u16rangelist',
    'vlanlist',
    'qosmap',
    'maplist',
    'aclfield',
    'aclaction',
    'aclmask',
    'aclcapability',
    'aclresource',
    'tlvlist',
    'segmentlist',
    'ipaddrlist',
    'porteyevalues',
    'timespec',
    'encrypt_key',
    'authkey',
    'macsecsak',
    'macsecauthkey',
    'macsecsalt',
    'sysportconfig',
    'sysportconfiglist',
    'reachability',
    'porterror',
    'portlanelatchstatuslist',
    'latchstatus',
    'json',
    'ipprefixlist',
    'aclchainlist',
    'portfrequencyoffsetppmlist',
    'portsnrlist',
]
union__sai_attribute_value_t._fields_ = [
    ('booldata', c_bool),
    ('chardata', c_char * int(32)),
    ('u8', sai_uint8_t),
    ('s8', sai_int8_t),
    ('u16', sai_uint16_t),
    ('s16', sai_int16_t),
    ('u32', sai_uint32_t),
    ('s32', sai_int32_t),
    ('u64', sai_uint64_t),
    ('s64', sai_int64_t),
    ('ptr', sai_pointer_t),
    ('mac', sai_mac_t),
    ('ip4', sai_ip4_t),
    ('ip6', sai_ip6_t),
    ('ipaddr', sai_ip_address_t),
    ('ipprefix', sai_ip_prefix_t),
    ('rx_state', sai_prbs_rx_state_t),
    ('oid', sai_object_id_t),
    ('objlist', sai_object_list_t),
    ('u8list', sai_u8_list_t),
    ('s8list', sai_s8_list_t),
    ('u16list', sai_u16_list_t),
    ('s16list', sai_s16_list_t),
    ('u32list', sai_u32_list_t),
    ('s32list', sai_s32_list_t),
    ('u32range', sai_u32_range_t),
    ('s32range', sai_s32_range_t),
    ('u16rangelist', sai_u16_range_list_t),
    ('vlanlist', sai_vlan_list_t),
    ('qosmap', sai_qos_map_list_t),
    ('maplist', sai_map_list_t),
    ('aclfield', sai_acl_field_data_t),
    ('aclaction', sai_acl_action_data_t),
    ('aclmask', sai_acl_field_data_mask_t),
    ('aclcapability', sai_acl_capability_t),
    ('aclresource', sai_acl_resource_list_t),
    ('tlvlist', sai_tlv_list_t),
    ('segmentlist', sai_segment_list_t),
    ('ipaddrlist', sai_ip_address_list_t),
    ('porteyevalues', sai_port_eye_values_list_t),
    ('timespec', sai_timespec_t),
    ('encrypt_key', sai_encrypt_key_t),
    ('authkey', sai_auth_key_t),
    ('macsecsak', sai_macsec_sak_t),
    ('macsecauthkey', sai_macsec_auth_key_t),
    ('macsecsalt', sai_macsec_salt_t),
    ('sysportconfig', sai_system_port_config_t),
    ('sysportconfiglist', sai_system_port_config_list_t),
    ('reachability', sai_fabric_port_reachability_t),
    ('porterror', sai_port_err_status_list_t),
    ('portlanelatchstatuslist', sai_port_lane_latch_status_list_t),
    ('latchstatus', sai_latch_status_t),
    ('json', sai_json_t),
    ('ipprefixlist', sai_ip_prefix_list_t),
    ('aclchainlist', sai_acl_chain_list_t),
    ('portfrequencyoffsetppmlist', sai_port_frequency_offset_ppm_list_t),
    ('portsnrlist', sai_port_snr_list_t),
]

sai_attribute_value_t = union__sai_attribute_value_t# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 1531

# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 1543
class struct__sai_attribute_t(Structure):
    pass

struct__sai_attribute_t.__slots__ = [
    'id',
    'value',
]
struct__sai_attribute_t._fields_ = [
    ('id', sai_attr_id_t),
    ('value', sai_attribute_value_t),
]

sai_attribute_t = struct__sai_attribute_t# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 1543

enum__sai_bulk_op_error_mode_t = c_int# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 1558

SAI_BULK_OP_ERROR_MODE_STOP_ON_ERROR = 0# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 1558

SAI_BULK_OP_ERROR_MODE_IGNORE_ERROR = (SAI_BULK_OP_ERROR_MODE_STOP_ON_ERROR + 1)# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 1558

sai_bulk_op_error_mode_t = enum__sai_bulk_op_error_mode_t# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 1558

sai_bulk_object_create_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, uint32_t, POINTER(uint32_t), POINTER(POINTER(sai_attribute_t)), sai_bulk_op_error_mode_t, POINTER(sai_object_id_t), POINTER(sai_status_t))# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 1577

sai_bulk_object_remove_fn = CFUNCTYPE(UNCHECKED(sai_status_t), uint32_t, POINTER(sai_object_id_t), sai_bulk_op_error_mode_t, POINTER(sai_status_t))# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 1598

sai_bulk_object_set_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), uint32_t, POINTER(sai_object_id_t), POINTER(sai_attribute_t), sai_bulk_op_error_mode_t, POINTER(sai_status_t))# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 1618

sai_bulk_object_get_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), uint32_t, POINTER(sai_object_id_t), POINTER(uint32_t), POINTER(POINTER(sai_attribute_t)), sai_bulk_op_error_mode_t, POINTER(sai_status_t))# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 1641

enum__sai_stats_mode_t = c_int# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 1683

SAI_STATS_MODE_READ = (1 << 0)# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 1683

SAI_STATS_MODE_READ_AND_CLEAR = (1 << 1)# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 1683

SAI_STATS_MODE_BULK_READ = (1 << 2)# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 1683

SAI_STATS_MODE_BULK_CLEAR = (1 << 3)# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 1683

SAI_STATS_MODE_BULK_READ_AND_CLEAR = (1 << 4)# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 1683

sai_stats_mode_t = enum__sai_stats_mode_t# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 1683

# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 1700
class struct__sai_stat_capability_t(Structure):
    pass

struct__sai_stat_capability_t.__slots__ = [
    'stat_enum',
    'stat_modes',
]
struct__sai_stat_capability_t._fields_ = [
    ('stat_enum', sai_stat_id_t),
    ('stat_modes', uint32_t),
]

sai_stat_capability_t = struct__sai_stat_capability_t# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 1700

# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 1707
class struct__sai_stat_capability_list_t(Structure):
    pass

struct__sai_stat_capability_list_t.__slots__ = [
    'count',
    'list',
]
struct__sai_stat_capability_list_t._fields_ = [
    ('count', uint32_t),
    ('list', POINTER(sai_stat_capability_t)),
]

sai_stat_capability_list_t = struct__sai_stat_capability_list_t# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 1707

enum__sai_object_stage_t = c_int# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 1720

SAI_OBJECT_STAGE_BOTH = 0# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 1720

SAI_OBJECT_STAGE_INGRESS = (SAI_OBJECT_STAGE_BOTH + 1)# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 1720

SAI_OBJECT_STAGE_EGRESS = (SAI_OBJECT_STAGE_INGRESS + 1)# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 1720

sai_object_stage_t = enum__sai_object_stage_t# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 1720

enum__sai_health_data_type_t = c_int# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 1726

SAI_HEALTH_DATA_TYPE_GENERAL = 0# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 1726

sai_health_data_type_t = enum__sai_health_data_type_t# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 1726

# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 1733
class struct__sai_switch_health_data_t(Structure):
    pass

struct__sai_switch_health_data_t.__slots__ = [
    'data_type',
]
struct__sai_switch_health_data_t._fields_ = [
    ('data_type', sai_health_data_type_t),
]

sai_switch_health_data_t = struct__sai_switch_health_data_t# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 1733

enum__sai_acl_ip_type_t = c_int# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 71

SAI_ACL_IP_TYPE_ANY = 0# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 71

SAI_ACL_IP_TYPE_IP = (SAI_ACL_IP_TYPE_ANY + 1)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 71

SAI_ACL_IP_TYPE_NON_IP = (SAI_ACL_IP_TYPE_IP + 1)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 71

SAI_ACL_IP_TYPE_IPV4ANY = (SAI_ACL_IP_TYPE_NON_IP + 1)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 71

SAI_ACL_IP_TYPE_NON_IPV4 = (SAI_ACL_IP_TYPE_IPV4ANY + 1)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 71

SAI_ACL_IP_TYPE_IPV6ANY = (SAI_ACL_IP_TYPE_NON_IPV4 + 1)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 71

SAI_ACL_IP_TYPE_NON_IPV6 = (SAI_ACL_IP_TYPE_IPV6ANY + 1)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 71

SAI_ACL_IP_TYPE_ARP = (SAI_ACL_IP_TYPE_NON_IPV6 + 1)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 71

SAI_ACL_IP_TYPE_ARP_REQUEST = (SAI_ACL_IP_TYPE_ARP + 1)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 71

SAI_ACL_IP_TYPE_ARP_REPLY = (SAI_ACL_IP_TYPE_ARP_REQUEST + 1)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 71

sai_acl_ip_type_t = enum__sai_acl_ip_type_t# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 71

enum__sai_acl_ip_frag_t = c_int# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 93

SAI_ACL_IP_FRAG_ANY = 0# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 93

SAI_ACL_IP_FRAG_NON_FRAG = (SAI_ACL_IP_FRAG_ANY + 1)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 93

SAI_ACL_IP_FRAG_NON_FRAG_OR_HEAD = (SAI_ACL_IP_FRAG_NON_FRAG + 1)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 93

SAI_ACL_IP_FRAG_HEAD = (SAI_ACL_IP_FRAG_NON_FRAG_OR_HEAD + 1)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 93

SAI_ACL_IP_FRAG_NON_HEAD = (SAI_ACL_IP_FRAG_HEAD + 1)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 93

sai_acl_ip_frag_t = enum__sai_acl_ip_frag_t# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 93

enum__sai_acl_dtel_flow_op_t = c_int# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 114

SAI_ACL_DTEL_FLOW_OP_NOP = 0# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 114

SAI_ACL_DTEL_FLOW_OP_INT = (SAI_ACL_DTEL_FLOW_OP_NOP + 1)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 114

SAI_ACL_DTEL_FLOW_OP_IOAM = (SAI_ACL_DTEL_FLOW_OP_INT + 1)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 114

SAI_ACL_DTEL_FLOW_OP_POSTCARD = (SAI_ACL_DTEL_FLOW_OP_IOAM + 1)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 114

sai_acl_dtel_flow_op_t = enum__sai_acl_dtel_flow_op_t# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 114

enum__sai_acl_action_type_t = c_int# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 291

SAI_ACL_ACTION_TYPE_REDIRECT = 0x00000000# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 291

SAI_ACL_ACTION_TYPE_ENDPOINT_IP = 0x00000001# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 291

SAI_ACL_ACTION_TYPE_REDIRECT_LIST = 0x00000002# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 291

SAI_ACL_ACTION_TYPE_PACKET_ACTION = 0x00000003# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 291

SAI_ACL_ACTION_TYPE_FLOOD = 0x00000004# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 291

SAI_ACL_ACTION_TYPE_COUNTER = 0x00000005# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 291

SAI_ACL_ACTION_TYPE_MIRROR_INGRESS = 0x00000006# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 291

SAI_ACL_ACTION_TYPE_MIRROR_EGRESS = 0x00000007# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 291

SAI_ACL_ACTION_TYPE_SET_POLICER = 0x00000008# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 291

SAI_ACL_ACTION_TYPE_DECREMENT_TTL = 0x00000009# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 291

SAI_ACL_ACTION_TYPE_SET_TC = 0x0000000a# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 291

SAI_ACL_ACTION_TYPE_SET_PACKET_COLOR = 0x0000000b# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 291

SAI_ACL_ACTION_TYPE_SET_INNER_VLAN_ID = 0x0000000c# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 291

SAI_ACL_ACTION_TYPE_SET_INNER_VLAN_PRI = 0x0000000d# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 291

SAI_ACL_ACTION_TYPE_SET_OUTER_VLAN_ID = 0x0000000e# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 291

SAI_ACL_ACTION_TYPE_SET_OUTER_VLAN_PRI = 0x0000000f# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 291

SAI_ACL_ACTION_TYPE_ADD_VLAN_ID = 0x00000032# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 291

SAI_ACL_ACTION_TYPE_ADD_VLAN_PRI = 0x00000033# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 291

SAI_ACL_ACTION_TYPE_SET_SRC_MAC = 0x00000010# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 291

SAI_ACL_ACTION_TYPE_SET_DST_MAC = 0x00000011# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 291

SAI_ACL_ACTION_TYPE_SET_SRC_IP = 0x00000012# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 291

SAI_ACL_ACTION_TYPE_SET_DST_IP = 0x00000013# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 291

SAI_ACL_ACTION_TYPE_SET_SRC_IPV6 = 0x00000014# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 291

SAI_ACL_ACTION_TYPE_SET_DST_IPV6 = 0x00000015# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 291

SAI_ACL_ACTION_TYPE_SET_DSCP = 0x00000016# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 291

SAI_ACL_ACTION_TYPE_SET_ECN = 0x00000017# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 291

SAI_ACL_ACTION_TYPE_SET_L4_SRC_PORT = 0x00000018# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 291

SAI_ACL_ACTION_TYPE_SET_L4_DST_PORT = 0x00000019# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 291

SAI_ACL_ACTION_TYPE_INGRESS_SAMPLEPACKET_ENABLE = 0x0000001a# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 291

SAI_ACL_ACTION_TYPE_EGRESS_SAMPLEPACKET_ENABLE = 0x0000001b# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 291

SAI_ACL_ACTION_TYPE_SET_ACL_META_DATA = 0x0000001c# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 291

SAI_ACL_ACTION_TYPE_EGRESS_BLOCK_PORT_LIST = 0x0000001d# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 291

SAI_ACL_ACTION_TYPE_SET_USER_TRAP_ID = 0x0000001e# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 291

SAI_ACL_ACTION_TYPE_SET_DO_NOT_LEARN = 0x0000001f# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 291

SAI_ACL_ACTION_TYPE_ACL_DTEL_FLOW_OP = 0x00000020# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 291

SAI_ACL_ACTION_TYPE_DTEL_INT_SESSION = 0x00000021# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 291

SAI_ACL_ACTION_TYPE_DTEL_DROP_REPORT_ENABLE = 0x00000022# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 291

SAI_ACL_ACTION_TYPE_DTEL_TAIL_DROP_REPORT_ENABLE = 0x00000023# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 291

SAI_ACL_ACTION_TYPE_DTEL_FLOW_SAMPLE_PERCENT = 0x00000024# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 291

SAI_ACL_ACTION_TYPE_DTEL_REPORT_ALL_PACKETS = 0x00000025# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 291

SAI_ACL_ACTION_TYPE_NO_NAT = 0x00000026# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 291

SAI_ACL_ACTION_TYPE_INT_INSERT = 0x00000027# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 291

SAI_ACL_ACTION_TYPE_INT_DELETE = 0x00000028# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 291

SAI_ACL_ACTION_TYPE_INT_REPORT_FLOW = 0x00000029# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 291

SAI_ACL_ACTION_TYPE_INT_REPORT_DROPS = 0x0000002a# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 291

SAI_ACL_ACTION_TYPE_INT_REPORT_TAIL_DROPS = 0x0000002b# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 291

SAI_ACL_ACTION_TYPE_TAM_INT_OBJECT = 0x0000002c# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 291

SAI_ACL_ACTION_TYPE_SET_ISOLATION_GROUP = 0x0000002d# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 291

SAI_ACL_ACTION_TYPE_MACSEC_FLOW = 0x0000002e# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 291

SAI_ACL_ACTION_TYPE_SET_LAG_HASH_ID = 0x0000002f# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 291

SAI_ACL_ACTION_TYPE_SET_ECMP_HASH_ID = 0x00000030# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 291

SAI_ACL_ACTION_TYPE_SET_VRF = 0x00000031# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 291

SAI_ACL_ACTION_TYPE_SET_FORWARDING_CLASS = 0x00000034# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 291

SAI_ACL_ACTION_TYPE_SET_ARS_MONITORING = 0x00000035# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 291

SAI_ACL_ACTION_TYPE_SET_ARS_OBJECT = 0x00000036# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 291

SAI_ACL_ACTION_TYPE_DISABLE_ARS_FORWARDING = 0x00000037# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 291

SAI_ACL_ACTION_TYPE_CHAIN_REDIRECT = 0x00000038# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 291

sai_acl_action_type_t = enum__sai_acl_action_type_t# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 291

enum__sai_acl_table_chain_group_type_t = c_int# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 303

SAI_ACL_TABLE_CHAIN_GROUP_TYPE_SEQUENTIAL = 0# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 303

SAI_ACL_TABLE_CHAIN_GROUP_TYPE_PARALLEL = (SAI_ACL_TABLE_CHAIN_GROUP_TYPE_SEQUENTIAL + 1)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 303

sai_acl_table_chain_group_type_t = enum__sai_acl_table_chain_group_type_t# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 303

enum__sai_acl_table_group_type_t = c_int# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 316

SAI_ACL_TABLE_GROUP_TYPE_SEQUENTIAL = 0# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 316

SAI_ACL_TABLE_GROUP_TYPE_PARALLEL = (SAI_ACL_TABLE_GROUP_TYPE_SEQUENTIAL + 1)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 316

sai_acl_table_group_type_t = enum__sai_acl_table_group_type_t# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 316

enum__sai_acl_table_group_attr_t = c_int# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 404

SAI_ACL_TABLE_GROUP_ATTR_START = 0# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 404

SAI_ACL_TABLE_GROUP_ATTR_ACL_STAGE = SAI_ACL_TABLE_GROUP_ATTR_START# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 404

SAI_ACL_TABLE_GROUP_ATTR_ACL_BIND_POINT_TYPE_LIST = (SAI_ACL_TABLE_GROUP_ATTR_ACL_STAGE + 1)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 404

SAI_ACL_TABLE_GROUP_ATTR_TYPE = (SAI_ACL_TABLE_GROUP_ATTR_ACL_BIND_POINT_TYPE_LIST + 1)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 404

SAI_ACL_TABLE_GROUP_ATTR_MEMBER_LIST = (SAI_ACL_TABLE_GROUP_ATTR_TYPE + 1)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 404

SAI_ACL_TABLE_GROUP_ATTR_CHAIN_GROUP_LIST = (SAI_ACL_TABLE_GROUP_ATTR_MEMBER_LIST + 1)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 404

SAI_ACL_TABLE_GROUP_ATTR_END = (SAI_ACL_TABLE_GROUP_ATTR_CHAIN_GROUP_LIST + 1)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 404

SAI_ACL_TABLE_GROUP_ATTR_CUSTOM_RANGE_START = 0x10000000# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 404

SAI_ACL_TABLE_GROUP_ATTR_CUSTOM_RANGE_END = (SAI_ACL_TABLE_GROUP_ATTR_CUSTOM_RANGE_START + 1)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 404

sai_acl_table_group_attr_t = enum__sai_acl_table_group_attr_t# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 404

enum__sai_acl_table_chain_group_attr_t = c_int# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 463

SAI_ACL_TABLE_CHAIN_GROUP_ATTR_START = 0# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 463

SAI_ACL_TABLE_CHAIN_GROUP_ATTR_TYPE = SAI_ACL_TABLE_CHAIN_GROUP_ATTR_START# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 463

SAI_ACL_TABLE_CHAIN_GROUP_ATTR_STAGE = (SAI_ACL_TABLE_CHAIN_GROUP_ATTR_TYPE + 1)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 463

SAI_ACL_TABLE_CHAIN_GROUP_ATTR_END = (SAI_ACL_TABLE_CHAIN_GROUP_ATTR_STAGE + 1)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 463

SAI_ACL_TABLE_CHAIN_GROUP_ATTR_CUSTOM_RANGE_START = 0x10000000# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 463

SAI_ACL_TABLE_CHAIN_GROUP_ATTR_CUSTOM_RANGE_END = (SAI_ACL_TABLE_CHAIN_GROUP_ATTR_CUSTOM_RANGE_START + 1)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 463

sai_acl_table_chain_group_attr_t = enum__sai_acl_table_chain_group_attr_t# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 463

enum__sai_acl_table_group_member_attr_t = c_int# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 549

SAI_ACL_TABLE_GROUP_MEMBER_ATTR_START = 0# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 549

SAI_ACL_TABLE_GROUP_MEMBER_ATTR_ACL_TABLE_GROUP_ID = SAI_ACL_TABLE_GROUP_MEMBER_ATTR_START# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 549

SAI_ACL_TABLE_GROUP_MEMBER_ATTR_ACL_TABLE_ID = (SAI_ACL_TABLE_GROUP_MEMBER_ATTR_ACL_TABLE_GROUP_ID + 1)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 549

SAI_ACL_TABLE_GROUP_MEMBER_ATTR_PRIORITY = (SAI_ACL_TABLE_GROUP_MEMBER_ATTR_ACL_TABLE_ID + 1)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 549

SAI_ACL_TABLE_GROUP_MEMBER_ATTR_ACL_TABLE_CHAIN_GROUP_ID = (SAI_ACL_TABLE_GROUP_MEMBER_ATTR_PRIORITY + 1)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 549

SAI_ACL_TABLE_GROUP_MEMBER_ATTR_END = (SAI_ACL_TABLE_GROUP_MEMBER_ATTR_ACL_TABLE_CHAIN_GROUP_ID + 1)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 549

SAI_ACL_TABLE_GROUP_MEMBER_ATTR_CUSTOM_RANGE_START = 0x10000000# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 549

SAI_ACL_TABLE_GROUP_MEMBER_ATTR_CUSTOM_RANGE_END = (SAI_ACL_TABLE_GROUP_MEMBER_ATTR_CUSTOM_RANGE_START + 1)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 549

sai_acl_table_group_member_attr_t = enum__sai_acl_table_group_member_attr_t# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 549

enum__sai_acl_table_attr_t = c_int# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 1609

SAI_ACL_TABLE_ATTR_START = 0# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 1609

SAI_ACL_TABLE_ATTR_ACL_STAGE = SAI_ACL_TABLE_ATTR_START# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 1609

SAI_ACL_TABLE_ATTR_ACL_BIND_POINT_TYPE_LIST = (SAI_ACL_TABLE_ATTR_ACL_STAGE + 1)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 1609

SAI_ACL_TABLE_ATTR_SIZE = (SAI_ACL_TABLE_ATTR_ACL_BIND_POINT_TYPE_LIST + 1)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 1609

SAI_ACL_TABLE_ATTR_ACL_ACTION_TYPE_LIST = (SAI_ACL_TABLE_ATTR_SIZE + 1)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 1609

SAI_ACL_TABLE_ATTR_FIELD_START = 0x00001000# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 1609

SAI_ACL_TABLE_ATTR_FIELD_SRC_IPV6 = SAI_ACL_TABLE_ATTR_FIELD_START# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 1609

SAI_ACL_TABLE_ATTR_FIELD_SRC_IPV6_WORD3 = (SAI_ACL_TABLE_ATTR_FIELD_START + 0x153)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 1609

SAI_ACL_TABLE_ATTR_FIELD_SRC_IPV6_WORD2 = (SAI_ACL_TABLE_ATTR_FIELD_START + 0x154)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 1609

SAI_ACL_TABLE_ATTR_FIELD_SRC_IPV6_WORD1 = (SAI_ACL_TABLE_ATTR_FIELD_START + 0x155)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 1609

SAI_ACL_TABLE_ATTR_FIELD_SRC_IPV6_WORD0 = (SAI_ACL_TABLE_ATTR_FIELD_START + 0x156)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 1609

SAI_ACL_TABLE_ATTR_FIELD_DST_IPV6 = (SAI_ACL_TABLE_ATTR_FIELD_START + 0x1)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 1609

SAI_ACL_TABLE_ATTR_FIELD_DST_IPV6_WORD3 = (SAI_ACL_TABLE_ATTR_FIELD_START + 0x157)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 1609

SAI_ACL_TABLE_ATTR_FIELD_DST_IPV6_WORD2 = (SAI_ACL_TABLE_ATTR_FIELD_START + 0x158)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 1609

SAI_ACL_TABLE_ATTR_FIELD_DST_IPV6_WORD1 = (SAI_ACL_TABLE_ATTR_FIELD_START + 0x159)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 1609

SAI_ACL_TABLE_ATTR_FIELD_DST_IPV6_WORD0 = (SAI_ACL_TABLE_ATTR_FIELD_START + 0x15a)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 1609

SAI_ACL_TABLE_ATTR_FIELD_INNER_SRC_IPV6 = (SAI_ACL_TABLE_ATTR_FIELD_START + 0x2)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 1609

SAI_ACL_TABLE_ATTR_FIELD_INNER_DST_IPV6 = (SAI_ACL_TABLE_ATTR_FIELD_START + 0x3)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 1609

SAI_ACL_TABLE_ATTR_FIELD_SRC_MAC = (SAI_ACL_TABLE_ATTR_FIELD_START + 0x4)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 1609

SAI_ACL_TABLE_ATTR_FIELD_DST_MAC = (SAI_ACL_TABLE_ATTR_FIELD_START + 0x5)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 1609

SAI_ACL_TABLE_ATTR_FIELD_SRC_IP = (SAI_ACL_TABLE_ATTR_FIELD_START + 0x6)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 1609

SAI_ACL_TABLE_ATTR_FIELD_DST_IP = (SAI_ACL_TABLE_ATTR_FIELD_START + 0x7)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 1609

SAI_ACL_TABLE_ATTR_FIELD_INNER_SRC_IP = (SAI_ACL_TABLE_ATTR_FIELD_START + 0x8)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 1609

SAI_ACL_TABLE_ATTR_FIELD_INNER_DST_IP = (SAI_ACL_TABLE_ATTR_FIELD_START + 0x9)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 1609

SAI_ACL_TABLE_ATTR_FIELD_IN_PORTS = (SAI_ACL_TABLE_ATTR_FIELD_START + 0xa)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 1609

SAI_ACL_TABLE_ATTR_FIELD_OUT_PORTS = (SAI_ACL_TABLE_ATTR_FIELD_START + 0xb)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 1609

SAI_ACL_TABLE_ATTR_FIELD_IN_PORT = (SAI_ACL_TABLE_ATTR_FIELD_START + 0xc)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 1609

SAI_ACL_TABLE_ATTR_FIELD_OUT_PORT = (SAI_ACL_TABLE_ATTR_FIELD_START + 0xd)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 1609

SAI_ACL_TABLE_ATTR_FIELD_SRC_PORT = (SAI_ACL_TABLE_ATTR_FIELD_START + 0xe)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 1609

SAI_ACL_TABLE_ATTR_FIELD_OUTER_VLAN_ID = (SAI_ACL_TABLE_ATTR_FIELD_START + 0xf)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 1609

SAI_ACL_TABLE_ATTR_FIELD_OUTER_VLAN_PRI = (SAI_ACL_TABLE_ATTR_FIELD_START + 0x10)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 1609

SAI_ACL_TABLE_ATTR_FIELD_OUTER_VLAN_CFI = (SAI_ACL_TABLE_ATTR_FIELD_START + 0x11)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 1609

SAI_ACL_TABLE_ATTR_FIELD_INNER_VLAN_ID = (SAI_ACL_TABLE_ATTR_FIELD_START + 0x12)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 1609

SAI_ACL_TABLE_ATTR_FIELD_INNER_VLAN_PRI = (SAI_ACL_TABLE_ATTR_FIELD_START + 0x13)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 1609

SAI_ACL_TABLE_ATTR_FIELD_INNER_VLAN_CFI = (SAI_ACL_TABLE_ATTR_FIELD_START + 0x14)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 1609

SAI_ACL_TABLE_ATTR_FIELD_L4_SRC_PORT = (SAI_ACL_TABLE_ATTR_FIELD_START + 0x15)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 1609

SAI_ACL_TABLE_ATTR_FIELD_L4_DST_PORT = (SAI_ACL_TABLE_ATTR_FIELD_START + 0x16)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 1609

SAI_ACL_TABLE_ATTR_FIELD_INNER_L4_SRC_PORT = (SAI_ACL_TABLE_ATTR_FIELD_START + 0x17)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 1609

SAI_ACL_TABLE_ATTR_FIELD_INNER_L4_DST_PORT = (SAI_ACL_TABLE_ATTR_FIELD_START + 0x18)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 1609

SAI_ACL_TABLE_ATTR_FIELD_ETHER_TYPE = (SAI_ACL_TABLE_ATTR_FIELD_START + 0x19)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 1609

SAI_ACL_TABLE_ATTR_FIELD_INNER_ETHER_TYPE = (SAI_ACL_TABLE_ATTR_FIELD_START + 0x1a)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 1609

SAI_ACL_TABLE_ATTR_FIELD_IP_PROTOCOL = (SAI_ACL_TABLE_ATTR_FIELD_START + 0x1b)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 1609

SAI_ACL_TABLE_ATTR_FIELD_INNER_IP_PROTOCOL = (SAI_ACL_TABLE_ATTR_FIELD_START + 0x1c)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 1609

SAI_ACL_TABLE_ATTR_FIELD_IP_IDENTIFICATION = (SAI_ACL_TABLE_ATTR_FIELD_START + 0x1d)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 1609

SAI_ACL_TABLE_ATTR_FIELD_DSCP = (SAI_ACL_TABLE_ATTR_FIELD_START + 0x1e)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 1609

SAI_ACL_TABLE_ATTR_FIELD_ECN = (SAI_ACL_TABLE_ATTR_FIELD_START + 0x1f)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 1609

SAI_ACL_TABLE_ATTR_FIELD_TTL = (SAI_ACL_TABLE_ATTR_FIELD_START + 0x20)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 1609

SAI_ACL_TABLE_ATTR_FIELD_TOS = (SAI_ACL_TABLE_ATTR_FIELD_START + 0x21)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 1609

SAI_ACL_TABLE_ATTR_FIELD_IP_FLAGS = (SAI_ACL_TABLE_ATTR_FIELD_START + 0x22)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 1609

SAI_ACL_TABLE_ATTR_FIELD_TCP_FLAGS = (SAI_ACL_TABLE_ATTR_FIELD_START + 0x23)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 1609

SAI_ACL_TABLE_ATTR_FIELD_ACL_IP_TYPE = (SAI_ACL_TABLE_ATTR_FIELD_START + 0x24)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 1609

SAI_ACL_TABLE_ATTR_FIELD_ACL_IP_FRAG = (SAI_ACL_TABLE_ATTR_FIELD_START + 0x25)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 1609

SAI_ACL_TABLE_ATTR_FIELD_IPV6_FLOW_LABEL = (SAI_ACL_TABLE_ATTR_FIELD_START + 0x26)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 1609

SAI_ACL_TABLE_ATTR_FIELD_TC = (SAI_ACL_TABLE_ATTR_FIELD_START + 0x27)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 1609

SAI_ACL_TABLE_ATTR_FIELD_ICMP_TYPE = (SAI_ACL_TABLE_ATTR_FIELD_START + 0x28)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 1609

SAI_ACL_TABLE_ATTR_FIELD_ICMP_CODE = (SAI_ACL_TABLE_ATTR_FIELD_START + 0x29)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 1609

SAI_ACL_TABLE_ATTR_FIELD_ICMPV6_TYPE = (SAI_ACL_TABLE_ATTR_FIELD_START + 0x2a)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 1609

SAI_ACL_TABLE_ATTR_FIELD_ICMPV6_CODE = (SAI_ACL_TABLE_ATTR_FIELD_START + 0x2b)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 1609

SAI_ACL_TABLE_ATTR_FIELD_PACKET_VLAN = (SAI_ACL_TABLE_ATTR_FIELD_START + 0x2c)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 1609

SAI_ACL_TABLE_ATTR_FIELD_TUNNEL_VNI = (SAI_ACL_TABLE_ATTR_FIELD_START + 0x2d)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 1609

SAI_ACL_TABLE_ATTR_FIELD_HAS_VLAN_TAG = (SAI_ACL_TABLE_ATTR_FIELD_START + 0x2e)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 1609

SAI_ACL_TABLE_ATTR_FIELD_MACSEC_SCI = (SAI_ACL_TABLE_ATTR_FIELD_START + 0x2f)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 1609

SAI_ACL_TABLE_ATTR_FIELD_MPLS_LABEL0_LABEL = (SAI_ACL_TABLE_ATTR_FIELD_START + 0x30)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 1609

SAI_ACL_TABLE_ATTR_FIELD_MPLS_LABEL0_TTL = (SAI_ACL_TABLE_ATTR_FIELD_START + 0x31)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 1609

SAI_ACL_TABLE_ATTR_FIELD_MPLS_LABEL0_EXP = (SAI_ACL_TABLE_ATTR_FIELD_START + 0x32)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 1609

SAI_ACL_TABLE_ATTR_FIELD_MPLS_LABEL0_BOS = (SAI_ACL_TABLE_ATTR_FIELD_START + 0x33)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 1609

SAI_ACL_TABLE_ATTR_FIELD_MPLS_LABEL1_LABEL = (SAI_ACL_TABLE_ATTR_FIELD_START + 0x34)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 1609

SAI_ACL_TABLE_ATTR_FIELD_MPLS_LABEL1_TTL = (SAI_ACL_TABLE_ATTR_FIELD_START + 0x35)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 1609

SAI_ACL_TABLE_ATTR_FIELD_MPLS_LABEL1_EXP = (SAI_ACL_TABLE_ATTR_FIELD_START + 0x36)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 1609

SAI_ACL_TABLE_ATTR_FIELD_MPLS_LABEL1_BOS = (SAI_ACL_TABLE_ATTR_FIELD_START + 0x37)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 1609

SAI_ACL_TABLE_ATTR_FIELD_MPLS_LABEL2_LABEL = (SAI_ACL_TABLE_ATTR_FIELD_START + 0x38)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 1609

SAI_ACL_TABLE_ATTR_FIELD_MPLS_LABEL2_TTL = (SAI_ACL_TABLE_ATTR_FIELD_START + 0x39)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 1609

SAI_ACL_TABLE_ATTR_FIELD_MPLS_LABEL2_EXP = (SAI_ACL_TABLE_ATTR_FIELD_START + 0x3a)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 1609

SAI_ACL_TABLE_ATTR_FIELD_MPLS_LABEL2_BOS = (SAI_ACL_TABLE_ATTR_FIELD_START + 0x3b)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 1609

SAI_ACL_TABLE_ATTR_FIELD_MPLS_LABEL3_LABEL = (SAI_ACL_TABLE_ATTR_FIELD_START + 0x3c)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 1609

SAI_ACL_TABLE_ATTR_FIELD_MPLS_LABEL3_TTL = (SAI_ACL_TABLE_ATTR_FIELD_START + 0x3d)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 1609

SAI_ACL_TABLE_ATTR_FIELD_MPLS_LABEL3_EXP = (SAI_ACL_TABLE_ATTR_FIELD_START + 0x3e)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 1609

SAI_ACL_TABLE_ATTR_FIELD_MPLS_LABEL3_BOS = (SAI_ACL_TABLE_ATTR_FIELD_START + 0x3f)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 1609

SAI_ACL_TABLE_ATTR_FIELD_MPLS_LABEL4_LABEL = (SAI_ACL_TABLE_ATTR_FIELD_START + 0x40)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 1609

SAI_ACL_TABLE_ATTR_FIELD_MPLS_LABEL4_TTL = (SAI_ACL_TABLE_ATTR_FIELD_START + 0x41)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 1609

SAI_ACL_TABLE_ATTR_FIELD_MPLS_LABEL4_EXP = (SAI_ACL_TABLE_ATTR_FIELD_START + 0x42)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 1609

SAI_ACL_TABLE_ATTR_FIELD_MPLS_LABEL4_BOS = (SAI_ACL_TABLE_ATTR_FIELD_START + 0x43)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 1609

SAI_ACL_TABLE_ATTR_FIELD_FDB_DST_USER_META = (SAI_ACL_TABLE_ATTR_FIELD_START + 0x44)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 1609

SAI_ACL_TABLE_ATTR_FIELD_ROUTE_DST_USER_META = (SAI_ACL_TABLE_ATTR_FIELD_START + 0x45)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 1609

SAI_ACL_TABLE_ATTR_FIELD_NEIGHBOR_DST_USER_META = (SAI_ACL_TABLE_ATTR_FIELD_START + 0x46)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 1609

SAI_ACL_TABLE_ATTR_FIELD_PORT_USER_META = (SAI_ACL_TABLE_ATTR_FIELD_START + 0x47)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 1609

SAI_ACL_TABLE_ATTR_FIELD_VLAN_USER_META = (SAI_ACL_TABLE_ATTR_FIELD_START + 0x48)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 1609

SAI_ACL_TABLE_ATTR_FIELD_ACL_USER_META = (SAI_ACL_TABLE_ATTR_FIELD_START + 0x49)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 1609

SAI_ACL_TABLE_ATTR_FIELD_FDB_NPU_META_DST_HIT = (SAI_ACL_TABLE_ATTR_FIELD_START + 0x4a)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 1609

SAI_ACL_TABLE_ATTR_FIELD_NEIGHBOR_NPU_META_DST_HIT = (SAI_ACL_TABLE_ATTR_FIELD_START + 0x4b)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 1609

SAI_ACL_TABLE_ATTR_FIELD_ROUTE_NPU_META_DST_HIT = (SAI_ACL_TABLE_ATTR_FIELD_START + 0x4c)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 1609

SAI_ACL_TABLE_ATTR_FIELD_BTH_OPCODE = (SAI_ACL_TABLE_ATTR_FIELD_START + 0x4d)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 1609

SAI_ACL_TABLE_ATTR_FIELD_AETH_SYNDROME = (SAI_ACL_TABLE_ATTR_FIELD_START + 0x4e)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 1609

SAI_ACL_TABLE_ATTR_USER_DEFINED_FIELD_GROUP_MIN = (SAI_ACL_TABLE_ATTR_FIELD_START + 0x4f)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 1609

SAI_ACL_TABLE_ATTR_USER_DEFINED_FIELD_GROUP_MAX = (SAI_ACL_TABLE_ATTR_USER_DEFINED_FIELD_GROUP_MIN + 0xFF)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 1609

SAI_ACL_TABLE_ATTR_FIELD_ACL_RANGE_TYPE = (SAI_ACL_TABLE_ATTR_FIELD_START + 0x14f)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 1609

SAI_ACL_TABLE_ATTR_FIELD_IPV6_NEXT_HEADER = (SAI_ACL_TABLE_ATTR_FIELD_START + 0x150)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 1609

SAI_ACL_TABLE_ATTR_FIELD_GRE_KEY = (SAI_ACL_TABLE_ATTR_FIELD_START + 0x151)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 1609

SAI_ACL_TABLE_ATTR_FIELD_TAM_INT_TYPE = (SAI_ACL_TABLE_ATTR_FIELD_START + 0x152)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 1609

SAI_ACL_TABLE_ATTR_FIELD_INNER_SRC_MAC = (SAI_ACL_TABLE_ATTR_FIELD_START + 0x15b)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 1609

SAI_ACL_TABLE_ATTR_FIELD_INNER_DST_MAC = (SAI_ACL_TABLE_ATTR_FIELD_START + 0x15c)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 1609

SAI_ACL_TABLE_ATTR_FIELD_END = SAI_ACL_TABLE_ATTR_FIELD_INNER_DST_MAC# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 1609

SAI_ACL_TABLE_ATTR_ENTRY_LIST = 0x00002000# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 1609

SAI_ACL_TABLE_ATTR_AVAILABLE_ACL_ENTRY = (SAI_ACL_TABLE_ATTR_ENTRY_LIST + 1)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 1609

SAI_ACL_TABLE_ATTR_AVAILABLE_ACL_COUNTER = (SAI_ACL_TABLE_ATTR_AVAILABLE_ACL_ENTRY + 1)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 1609

SAI_ACL_TABLE_ATTR_ACL_TABLE_MATCH_TYPE = (SAI_ACL_TABLE_ATTR_AVAILABLE_ACL_COUNTER + 1)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 1609

SAI_ACL_TABLE_ATTR_FIELD_VALID_BITS_START = 0x00003000# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 1609

SAI_ACL_TABLE_ATTR_FIELD_VALID_BITS_SRC_IPV6 = SAI_ACL_TABLE_ATTR_FIELD_VALID_BITS_START# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 1609

SAI_ACL_TABLE_ATTR_FIELD_VALID_BITS_DST_IPV6 = (SAI_ACL_TABLE_ATTR_FIELD_VALID_BITS_START + 1)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 1609

SAI_ACL_TABLE_ATTR_FIELD_VALID_BITS_END = SAI_ACL_TABLE_ATTR_FIELD_VALID_BITS_DST_IPV6# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 1609

SAI_ACL_TABLE_ATTR_END = (SAI_ACL_TABLE_ATTR_FIELD_VALID_BITS_END + 1)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 1609

SAI_ACL_TABLE_ATTR_CUSTOM_RANGE_START = 0x10000000# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 1609

SAI_ACL_TABLE_ATTR_CUSTOM_RANGE_END = (SAI_ACL_TABLE_ATTR_CUSTOM_RANGE_START + 1)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 1609

sai_acl_table_attr_t = enum__sai_acl_table_attr_t# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 1609

enum__sai_acl_entry_attr_t = c_int# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3186

SAI_ACL_ENTRY_ATTR_START = 0# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3186

SAI_ACL_ENTRY_ATTR_TABLE_ID = SAI_ACL_ENTRY_ATTR_START# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3186

SAI_ACL_ENTRY_ATTR_PRIORITY = (SAI_ACL_ENTRY_ATTR_TABLE_ID + 1)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3186

SAI_ACL_ENTRY_ATTR_ADMIN_STATE = (SAI_ACL_ENTRY_ATTR_PRIORITY + 1)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3186

SAI_ACL_ENTRY_ATTR_FIELD_START = 0x00001000# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3186

SAI_ACL_ENTRY_ATTR_FIELD_SRC_IPV6 = SAI_ACL_ENTRY_ATTR_FIELD_START# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3186

SAI_ACL_ENTRY_ATTR_FIELD_SRC_IPV6_WORD3 = (SAI_ACL_ENTRY_ATTR_FIELD_START + 0x153)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3186

SAI_ACL_ENTRY_ATTR_FIELD_SRC_IPV6_WORD2 = (SAI_ACL_ENTRY_ATTR_FIELD_START + 0x154)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3186

SAI_ACL_ENTRY_ATTR_FIELD_SRC_IPV6_WORD1 = (SAI_ACL_ENTRY_ATTR_FIELD_START + 0x155)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3186

SAI_ACL_ENTRY_ATTR_FIELD_SRC_IPV6_WORD0 = (SAI_ACL_ENTRY_ATTR_FIELD_START + 0x156)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3186

SAI_ACL_ENTRY_ATTR_FIELD_DST_IPV6 = (SAI_ACL_ENTRY_ATTR_FIELD_START + 0x1)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3186

SAI_ACL_ENTRY_ATTR_FIELD_DST_IPV6_WORD3 = (SAI_ACL_ENTRY_ATTR_FIELD_START + 0x157)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3186

SAI_ACL_ENTRY_ATTR_FIELD_DST_IPV6_WORD2 = (SAI_ACL_ENTRY_ATTR_FIELD_START + 0x158)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3186

SAI_ACL_ENTRY_ATTR_FIELD_DST_IPV6_WORD1 = (SAI_ACL_ENTRY_ATTR_FIELD_START + 0x159)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3186

SAI_ACL_ENTRY_ATTR_FIELD_DST_IPV6_WORD0 = (SAI_ACL_ENTRY_ATTR_FIELD_START + 0x15a)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3186

SAI_ACL_ENTRY_ATTR_FIELD_INNER_SRC_IPV6 = (SAI_ACL_ENTRY_ATTR_FIELD_START + 0x2)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3186

SAI_ACL_ENTRY_ATTR_FIELD_INNER_DST_IPV6 = (SAI_ACL_ENTRY_ATTR_FIELD_START + 0x3)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3186

SAI_ACL_ENTRY_ATTR_FIELD_SRC_MAC = (SAI_ACL_ENTRY_ATTR_FIELD_START + 0x4)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3186

SAI_ACL_ENTRY_ATTR_FIELD_DST_MAC = (SAI_ACL_ENTRY_ATTR_FIELD_START + 0x5)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3186

SAI_ACL_ENTRY_ATTR_FIELD_SRC_IP = (SAI_ACL_ENTRY_ATTR_FIELD_START + 0x6)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3186

SAI_ACL_ENTRY_ATTR_FIELD_DST_IP = (SAI_ACL_ENTRY_ATTR_FIELD_START + 0x7)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3186

SAI_ACL_ENTRY_ATTR_FIELD_INNER_SRC_IP = (SAI_ACL_ENTRY_ATTR_FIELD_START + 0x8)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3186

SAI_ACL_ENTRY_ATTR_FIELD_INNER_DST_IP = (SAI_ACL_ENTRY_ATTR_FIELD_START + 0x9)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3186

SAI_ACL_ENTRY_ATTR_FIELD_IN_PORTS = (SAI_ACL_ENTRY_ATTR_FIELD_START + 0xa)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3186

SAI_ACL_ENTRY_ATTR_FIELD_OUT_PORTS = (SAI_ACL_ENTRY_ATTR_FIELD_START + 0xb)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3186

SAI_ACL_ENTRY_ATTR_FIELD_IN_PORT = (SAI_ACL_ENTRY_ATTR_FIELD_START + 0xc)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3186

SAI_ACL_ENTRY_ATTR_FIELD_OUT_PORT = (SAI_ACL_ENTRY_ATTR_FIELD_START + 0xd)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3186

SAI_ACL_ENTRY_ATTR_FIELD_SRC_PORT = (SAI_ACL_ENTRY_ATTR_FIELD_START + 0xe)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3186

SAI_ACL_ENTRY_ATTR_FIELD_OUTER_VLAN_ID = (SAI_ACL_ENTRY_ATTR_FIELD_START + 0xf)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3186

SAI_ACL_ENTRY_ATTR_FIELD_OUTER_VLAN_PRI = (SAI_ACL_ENTRY_ATTR_FIELD_START + 0x10)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3186

SAI_ACL_ENTRY_ATTR_FIELD_OUTER_VLAN_CFI = (SAI_ACL_ENTRY_ATTR_FIELD_START + 0x11)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3186

SAI_ACL_ENTRY_ATTR_FIELD_INNER_VLAN_ID = (SAI_ACL_ENTRY_ATTR_FIELD_START + 0x12)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3186

SAI_ACL_ENTRY_ATTR_FIELD_INNER_VLAN_PRI = (SAI_ACL_ENTRY_ATTR_FIELD_START + 0x13)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3186

SAI_ACL_ENTRY_ATTR_FIELD_INNER_VLAN_CFI = (SAI_ACL_ENTRY_ATTR_FIELD_START + 0x14)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3186

SAI_ACL_ENTRY_ATTR_FIELD_L4_SRC_PORT = (SAI_ACL_ENTRY_ATTR_FIELD_START + 0x15)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3186

SAI_ACL_ENTRY_ATTR_FIELD_L4_DST_PORT = (SAI_ACL_ENTRY_ATTR_FIELD_START + 0x16)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3186

SAI_ACL_ENTRY_ATTR_FIELD_INNER_L4_SRC_PORT = (SAI_ACL_ENTRY_ATTR_FIELD_START + 0x17)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3186

SAI_ACL_ENTRY_ATTR_FIELD_INNER_L4_DST_PORT = (SAI_ACL_ENTRY_ATTR_FIELD_START + 0x18)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3186

SAI_ACL_ENTRY_ATTR_FIELD_ETHER_TYPE = (SAI_ACL_ENTRY_ATTR_FIELD_START + 0x19)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3186

SAI_ACL_ENTRY_ATTR_FIELD_INNER_ETHER_TYPE = (SAI_ACL_ENTRY_ATTR_FIELD_START + 0x1a)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3186

SAI_ACL_ENTRY_ATTR_FIELD_IP_PROTOCOL = (SAI_ACL_ENTRY_ATTR_FIELD_START + 0x1b)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3186

SAI_ACL_ENTRY_ATTR_FIELD_INNER_IP_PROTOCOL = (SAI_ACL_ENTRY_ATTR_FIELD_START + 0x1c)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3186

SAI_ACL_ENTRY_ATTR_FIELD_IP_IDENTIFICATION = (SAI_ACL_ENTRY_ATTR_FIELD_START + 0x1d)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3186

SAI_ACL_ENTRY_ATTR_FIELD_DSCP = (SAI_ACL_ENTRY_ATTR_FIELD_START + 0x1e)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3186

SAI_ACL_ENTRY_ATTR_FIELD_ECN = (SAI_ACL_ENTRY_ATTR_FIELD_START + 0x1f)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3186

SAI_ACL_ENTRY_ATTR_FIELD_TTL = (SAI_ACL_ENTRY_ATTR_FIELD_START + 0x20)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3186

SAI_ACL_ENTRY_ATTR_FIELD_TOS = (SAI_ACL_ENTRY_ATTR_FIELD_START + 0x21)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3186

SAI_ACL_ENTRY_ATTR_FIELD_IP_FLAGS = (SAI_ACL_ENTRY_ATTR_FIELD_START + 0x22)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3186

SAI_ACL_ENTRY_ATTR_FIELD_TCP_FLAGS = (SAI_ACL_ENTRY_ATTR_FIELD_START + 0x23)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3186

SAI_ACL_ENTRY_ATTR_FIELD_ACL_IP_TYPE = (SAI_ACL_ENTRY_ATTR_FIELD_START + 0x24)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3186

SAI_ACL_ENTRY_ATTR_FIELD_ACL_IP_FRAG = (SAI_ACL_ENTRY_ATTR_FIELD_START + 0x25)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3186

SAI_ACL_ENTRY_ATTR_FIELD_IPV6_FLOW_LABEL = (SAI_ACL_ENTRY_ATTR_FIELD_START + 0x26)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3186

SAI_ACL_ENTRY_ATTR_FIELD_TC = (SAI_ACL_ENTRY_ATTR_FIELD_START + 0x27)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3186

SAI_ACL_ENTRY_ATTR_FIELD_ICMP_TYPE = (SAI_ACL_ENTRY_ATTR_FIELD_START + 0x28)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3186

SAI_ACL_ENTRY_ATTR_FIELD_ICMP_CODE = (SAI_ACL_ENTRY_ATTR_FIELD_START + 0x29)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3186

SAI_ACL_ENTRY_ATTR_FIELD_ICMPV6_TYPE = (SAI_ACL_ENTRY_ATTR_FIELD_START + 0x2a)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3186

SAI_ACL_ENTRY_ATTR_FIELD_ICMPV6_CODE = (SAI_ACL_ENTRY_ATTR_FIELD_START + 0x2b)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3186

SAI_ACL_ENTRY_ATTR_FIELD_PACKET_VLAN = (SAI_ACL_ENTRY_ATTR_FIELD_START + 0x2c)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3186

SAI_ACL_ENTRY_ATTR_FIELD_TUNNEL_VNI = (SAI_ACL_ENTRY_ATTR_FIELD_START + 0x2d)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3186

SAI_ACL_ENTRY_ATTR_FIELD_HAS_VLAN_TAG = (SAI_ACL_ENTRY_ATTR_FIELD_START + 0x2e)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3186

SAI_ACL_ENTRY_ATTR_FIELD_MACSEC_SCI = (SAI_ACL_ENTRY_ATTR_FIELD_START + 0x2f)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3186

SAI_ACL_ENTRY_ATTR_FIELD_MPLS_LABEL0_LABEL = (SAI_ACL_ENTRY_ATTR_FIELD_START + 0x30)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3186

SAI_ACL_ENTRY_ATTR_FIELD_MPLS_LABEL0_TTL = (SAI_ACL_ENTRY_ATTR_FIELD_START + 0x31)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3186

SAI_ACL_ENTRY_ATTR_FIELD_MPLS_LABEL0_EXP = (SAI_ACL_ENTRY_ATTR_FIELD_START + 0x32)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3186

SAI_ACL_ENTRY_ATTR_FIELD_MPLS_LABEL0_BOS = (SAI_ACL_ENTRY_ATTR_FIELD_START + 0x33)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3186

SAI_ACL_ENTRY_ATTR_FIELD_MPLS_LABEL1_LABEL = (SAI_ACL_ENTRY_ATTR_FIELD_START + 0x34)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3186

SAI_ACL_ENTRY_ATTR_FIELD_MPLS_LABEL1_TTL = (SAI_ACL_ENTRY_ATTR_FIELD_START + 0x35)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3186

SAI_ACL_ENTRY_ATTR_FIELD_MPLS_LABEL1_EXP = (SAI_ACL_ENTRY_ATTR_FIELD_START + 0x36)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3186

SAI_ACL_ENTRY_ATTR_FIELD_MPLS_LABEL1_BOS = (SAI_ACL_ENTRY_ATTR_FIELD_START + 0x37)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3186

SAI_ACL_ENTRY_ATTR_FIELD_MPLS_LABEL2_LABEL = (SAI_ACL_ENTRY_ATTR_FIELD_START + 0x38)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3186

SAI_ACL_ENTRY_ATTR_FIELD_MPLS_LABEL2_TTL = (SAI_ACL_ENTRY_ATTR_FIELD_START + 0x39)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3186

SAI_ACL_ENTRY_ATTR_FIELD_MPLS_LABEL2_EXP = (SAI_ACL_ENTRY_ATTR_FIELD_START + 0x3a)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3186

SAI_ACL_ENTRY_ATTR_FIELD_MPLS_LABEL2_BOS = (SAI_ACL_ENTRY_ATTR_FIELD_START + 0x3b)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3186

SAI_ACL_ENTRY_ATTR_FIELD_MPLS_LABEL3_LABEL = (SAI_ACL_ENTRY_ATTR_FIELD_START + 0x3c)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3186

SAI_ACL_ENTRY_ATTR_FIELD_MPLS_LABEL3_TTL = (SAI_ACL_ENTRY_ATTR_FIELD_START + 0x3d)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3186

SAI_ACL_ENTRY_ATTR_FIELD_MPLS_LABEL3_EXP = (SAI_ACL_ENTRY_ATTR_FIELD_START + 0x3e)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3186

SAI_ACL_ENTRY_ATTR_FIELD_MPLS_LABEL3_BOS = (SAI_ACL_ENTRY_ATTR_FIELD_START + 0x3f)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3186

SAI_ACL_ENTRY_ATTR_FIELD_MPLS_LABEL4_LABEL = (SAI_ACL_ENTRY_ATTR_FIELD_START + 0x40)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3186

SAI_ACL_ENTRY_ATTR_FIELD_MPLS_LABEL4_TTL = (SAI_ACL_ENTRY_ATTR_FIELD_START + 0x41)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3186

SAI_ACL_ENTRY_ATTR_FIELD_MPLS_LABEL4_EXP = (SAI_ACL_ENTRY_ATTR_FIELD_START + 0x42)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3186

SAI_ACL_ENTRY_ATTR_FIELD_MPLS_LABEL4_BOS = (SAI_ACL_ENTRY_ATTR_FIELD_START + 0x43)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3186

SAI_ACL_ENTRY_ATTR_FIELD_FDB_DST_USER_META = (SAI_ACL_ENTRY_ATTR_FIELD_START + 0x44)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3186

SAI_ACL_ENTRY_ATTR_FIELD_ROUTE_DST_USER_META = (SAI_ACL_ENTRY_ATTR_FIELD_START + 0x45)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3186

SAI_ACL_ENTRY_ATTR_FIELD_NEIGHBOR_DST_USER_META = (SAI_ACL_ENTRY_ATTR_FIELD_START + 0x46)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3186

SAI_ACL_ENTRY_ATTR_FIELD_PORT_USER_META = (SAI_ACL_ENTRY_ATTR_FIELD_START + 0x47)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3186

SAI_ACL_ENTRY_ATTR_FIELD_VLAN_USER_META = (SAI_ACL_ENTRY_ATTR_FIELD_START + 0x48)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3186

SAI_ACL_ENTRY_ATTR_FIELD_ACL_USER_META = (SAI_ACL_ENTRY_ATTR_FIELD_START + 0x49)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3186

SAI_ACL_ENTRY_ATTR_FIELD_FDB_NPU_META_DST_HIT = (SAI_ACL_ENTRY_ATTR_FIELD_START + 0x4a)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3186

SAI_ACL_ENTRY_ATTR_FIELD_NEIGHBOR_NPU_META_DST_HIT = (SAI_ACL_ENTRY_ATTR_FIELD_START + 0x4b)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3186

SAI_ACL_ENTRY_ATTR_FIELD_ROUTE_NPU_META_DST_HIT = (SAI_ACL_ENTRY_ATTR_FIELD_START + 0x4c)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3186

SAI_ACL_ENTRY_ATTR_FIELD_BTH_OPCODE = (SAI_ACL_ENTRY_ATTR_FIELD_START + 0x4d)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3186

SAI_ACL_ENTRY_ATTR_FIELD_AETH_SYNDROME = (SAI_ACL_ENTRY_ATTR_FIELD_START + 0x4e)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3186

SAI_ACL_ENTRY_ATTR_USER_DEFINED_FIELD_GROUP_MIN = (SAI_ACL_ENTRY_ATTR_FIELD_START + 0x4f)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3186

SAI_ACL_ENTRY_ATTR_USER_DEFINED_FIELD_GROUP_MAX = (SAI_ACL_ENTRY_ATTR_USER_DEFINED_FIELD_GROUP_MIN + 0xFF)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3186

SAI_ACL_ENTRY_ATTR_FIELD_ACL_RANGE_TYPE = (SAI_ACL_ENTRY_ATTR_FIELD_START + 0x14f)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3186

SAI_ACL_ENTRY_ATTR_FIELD_IPV6_NEXT_HEADER = (SAI_ACL_ENTRY_ATTR_FIELD_START + 0x150)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3186

SAI_ACL_ENTRY_ATTR_FIELD_GRE_KEY = (SAI_ACL_ENTRY_ATTR_FIELD_START + 0x151)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3186

SAI_ACL_ENTRY_ATTR_FIELD_TAM_INT_TYPE = (SAI_ACL_ENTRY_ATTR_FIELD_START + 0x152)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3186

SAI_ACL_ENTRY_ATTR_FIELD_INNER_SRC_MAC = (SAI_ACL_ENTRY_ATTR_FIELD_START + 0x15b)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3186

SAI_ACL_ENTRY_ATTR_FIELD_INNER_DST_MAC = (SAI_ACL_ENTRY_ATTR_FIELD_START + 0x15c)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3186

SAI_ACL_ENTRY_ATTR_FIELD_END = SAI_ACL_ENTRY_ATTR_FIELD_INNER_DST_MAC# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3186

SAI_ACL_ENTRY_ATTR_ACTION_START = 0x00002000# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3186

SAI_ACL_ENTRY_ATTR_ACTION_REDIRECT = SAI_ACL_ENTRY_ATTR_ACTION_START# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3186

SAI_ACL_ENTRY_ATTR_ACTION_ENDPOINT_IP = (SAI_ACL_ENTRY_ATTR_ACTION_START + 0x1)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3186

SAI_ACL_ENTRY_ATTR_ACTION_REDIRECT_LIST = (SAI_ACL_ENTRY_ATTR_ACTION_START + 0x2)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3186

SAI_ACL_ENTRY_ATTR_ACTION_PACKET_ACTION = (SAI_ACL_ENTRY_ATTR_ACTION_START + 0x3)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3186

SAI_ACL_ENTRY_ATTR_ACTION_FLOOD = (SAI_ACL_ENTRY_ATTR_ACTION_START + 0x4)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3186

SAI_ACL_ENTRY_ATTR_ACTION_COUNTER = (SAI_ACL_ENTRY_ATTR_ACTION_START + 0x5)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3186

SAI_ACL_ENTRY_ATTR_ACTION_MIRROR_INGRESS = (SAI_ACL_ENTRY_ATTR_ACTION_START + 0x6)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3186

SAI_ACL_ENTRY_ATTR_ACTION_MIRROR_EGRESS = (SAI_ACL_ENTRY_ATTR_ACTION_START + 0x7)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3186

SAI_ACL_ENTRY_ATTR_ACTION_SET_POLICER = (SAI_ACL_ENTRY_ATTR_ACTION_START + 0x8)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3186

SAI_ACL_ENTRY_ATTR_ACTION_DECREMENT_TTL = (SAI_ACL_ENTRY_ATTR_ACTION_START + 0x9)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3186

SAI_ACL_ENTRY_ATTR_ACTION_SET_TC = (SAI_ACL_ENTRY_ATTR_ACTION_START + 0xa)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3186

SAI_ACL_ENTRY_ATTR_ACTION_SET_PACKET_COLOR = (SAI_ACL_ENTRY_ATTR_ACTION_START + 0xb)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3186

SAI_ACL_ENTRY_ATTR_ACTION_SET_INNER_VLAN_ID = (SAI_ACL_ENTRY_ATTR_ACTION_START + 0xc)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3186

SAI_ACL_ENTRY_ATTR_ACTION_SET_INNER_VLAN_PRI = (SAI_ACL_ENTRY_ATTR_ACTION_START + 0xd)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3186

SAI_ACL_ENTRY_ATTR_ACTION_SET_OUTER_VLAN_ID = (SAI_ACL_ENTRY_ATTR_ACTION_START + 0xe)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3186

SAI_ACL_ENTRY_ATTR_ACTION_SET_OUTER_VLAN_PRI = (SAI_ACL_ENTRY_ATTR_ACTION_START + 0xf)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3186

SAI_ACL_ENTRY_ATTR_ACTION_ADD_VLAN_ID = (SAI_ACL_ENTRY_ATTR_ACTION_START + 0x32)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3186

SAI_ACL_ENTRY_ATTR_ACTION_ADD_VLAN_PRI = (SAI_ACL_ENTRY_ATTR_ACTION_START + 0x33)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3186

SAI_ACL_ENTRY_ATTR_ACTION_SET_SRC_MAC = (SAI_ACL_ENTRY_ATTR_ACTION_START + 0x10)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3186

SAI_ACL_ENTRY_ATTR_ACTION_SET_DST_MAC = (SAI_ACL_ENTRY_ATTR_ACTION_START + 0x11)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3186

SAI_ACL_ENTRY_ATTR_ACTION_SET_SRC_IP = (SAI_ACL_ENTRY_ATTR_ACTION_START + 0x12)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3186

SAI_ACL_ENTRY_ATTR_ACTION_SET_DST_IP = (SAI_ACL_ENTRY_ATTR_ACTION_START + 0x13)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3186

SAI_ACL_ENTRY_ATTR_ACTION_SET_SRC_IPV6 = (SAI_ACL_ENTRY_ATTR_ACTION_START + 0x14)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3186

SAI_ACL_ENTRY_ATTR_ACTION_SET_DST_IPV6 = (SAI_ACL_ENTRY_ATTR_ACTION_START + 0x15)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3186

SAI_ACL_ENTRY_ATTR_ACTION_SET_DSCP = (SAI_ACL_ENTRY_ATTR_ACTION_START + 0x16)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3186

SAI_ACL_ENTRY_ATTR_ACTION_SET_ECN = (SAI_ACL_ENTRY_ATTR_ACTION_START + 0x17)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3186

SAI_ACL_ENTRY_ATTR_ACTION_SET_L4_SRC_PORT = (SAI_ACL_ENTRY_ATTR_ACTION_START + 0x18)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3186

SAI_ACL_ENTRY_ATTR_ACTION_SET_L4_DST_PORT = (SAI_ACL_ENTRY_ATTR_ACTION_START + 0x19)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3186

SAI_ACL_ENTRY_ATTR_ACTION_INGRESS_SAMPLEPACKET_ENABLE = (SAI_ACL_ENTRY_ATTR_ACTION_START + 0x1a)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3186

SAI_ACL_ENTRY_ATTR_ACTION_EGRESS_SAMPLEPACKET_ENABLE = (SAI_ACL_ENTRY_ATTR_ACTION_START + 0x1b)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3186

SAI_ACL_ENTRY_ATTR_ACTION_SET_ACL_META_DATA = (SAI_ACL_ENTRY_ATTR_ACTION_START + 0x1c)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3186

SAI_ACL_ENTRY_ATTR_ACTION_EGRESS_BLOCK_PORT_LIST = (SAI_ACL_ENTRY_ATTR_ACTION_START + 0x1d)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3186

SAI_ACL_ENTRY_ATTR_ACTION_SET_USER_TRAP_ID = (SAI_ACL_ENTRY_ATTR_ACTION_START + 0x1e)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3186

SAI_ACL_ENTRY_ATTR_ACTION_SET_DO_NOT_LEARN = (SAI_ACL_ENTRY_ATTR_ACTION_START + 0x1f)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3186

SAI_ACL_ENTRY_ATTR_ACTION_ACL_DTEL_FLOW_OP = (SAI_ACL_ENTRY_ATTR_ACTION_START + 0x20)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3186

SAI_ACL_ENTRY_ATTR_ACTION_DTEL_INT_SESSION = (SAI_ACL_ENTRY_ATTR_ACTION_START + 0x21)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3186

SAI_ACL_ENTRY_ATTR_ACTION_DTEL_DROP_REPORT_ENABLE = (SAI_ACL_ENTRY_ATTR_ACTION_START + 0x22)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3186

SAI_ACL_ENTRY_ATTR_ACTION_DTEL_TAIL_DROP_REPORT_ENABLE = (SAI_ACL_ENTRY_ATTR_ACTION_START + 0x23)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3186

SAI_ACL_ENTRY_ATTR_ACTION_DTEL_FLOW_SAMPLE_PERCENT = (SAI_ACL_ENTRY_ATTR_ACTION_START + 0x24)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3186

SAI_ACL_ENTRY_ATTR_ACTION_DTEL_REPORT_ALL_PACKETS = (SAI_ACL_ENTRY_ATTR_ACTION_START + 0x25)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3186

SAI_ACL_ENTRY_ATTR_ACTION_NO_NAT = (SAI_ACL_ENTRY_ATTR_ACTION_START + 0x26)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3186

SAI_ACL_ENTRY_ATTR_ACTION_INT_INSERT = (SAI_ACL_ENTRY_ATTR_ACTION_START + 0x27)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3186

SAI_ACL_ENTRY_ATTR_ACTION_INT_DELETE = (SAI_ACL_ENTRY_ATTR_ACTION_START + 0x28)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3186

SAI_ACL_ENTRY_ATTR_ACTION_INT_REPORT_FLOW = (SAI_ACL_ENTRY_ATTR_ACTION_START + 0x29)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3186

SAI_ACL_ENTRY_ATTR_ACTION_INT_REPORT_DROPS = (SAI_ACL_ENTRY_ATTR_ACTION_START + 0x2a)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3186

SAI_ACL_ENTRY_ATTR_ACTION_INT_REPORT_TAIL_DROPS = (SAI_ACL_ENTRY_ATTR_ACTION_START + 0x2b)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3186

SAI_ACL_ENTRY_ATTR_ACTION_TAM_INT_OBJECT = (SAI_ACL_ENTRY_ATTR_ACTION_START + 0x2c)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3186

SAI_ACL_ENTRY_ATTR_ACTION_SET_ISOLATION_GROUP = (SAI_ACL_ENTRY_ATTR_ACTION_START + 0x2d)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3186

SAI_ACL_ENTRY_ATTR_ACTION_MACSEC_FLOW = (SAI_ACL_ENTRY_ATTR_ACTION_START + 0x2e)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3186

SAI_ACL_ENTRY_ATTR_ACTION_SET_LAG_HASH_ID = (SAI_ACL_ENTRY_ATTR_ACTION_START + 0x2f)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3186

SAI_ACL_ENTRY_ATTR_ACTION_SET_ECMP_HASH_ID = (SAI_ACL_ENTRY_ATTR_ACTION_START + 0x30)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3186

SAI_ACL_ENTRY_ATTR_ACTION_SET_VRF = (SAI_ACL_ENTRY_ATTR_ACTION_START + 0x31)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3186

SAI_ACL_ENTRY_ATTR_ACTION_SET_FORWARDING_CLASS = (SAI_ACL_ENTRY_ATTR_ACTION_START + 0x34)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3186

SAI_ACL_ENTRY_ATTR_ACTION_SET_ARS_MONITORING = (SAI_ACL_ENTRY_ATTR_ACTION_START + 0x35)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3186

SAI_ACL_ENTRY_ATTR_ACTION_SET_ARS_OBJECT = (SAI_ACL_ENTRY_ATTR_ACTION_START + 0x36)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3186

SAI_ACL_ENTRY_ATTR_ACTION_DISABLE_ARS_FORWARDING = (SAI_ACL_ENTRY_ATTR_ACTION_START + 0x37)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3186

SAI_ACL_ENTRY_ATTR_ACTION_CHAIN_REDIRECT = (SAI_ACL_ENTRY_ATTR_ACTION_START + 0x38)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3186

SAI_ACL_ENTRY_ATTR_ACTION_END = SAI_ACL_ENTRY_ATTR_ACTION_CHAIN_REDIRECT# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3186

SAI_ACL_ENTRY_ATTR_END = (SAI_ACL_ENTRY_ATTR_ACTION_END + 1)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3186

SAI_ACL_ENTRY_ATTR_CUSTOM_RANGE_START = 0x10000000# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3186

SAI_ACL_ENTRY_ATTR_CUSTOM_RANGE_END = (SAI_ACL_ENTRY_ATTR_CUSTOM_RANGE_START + 1)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3186

sai_acl_entry_attr_t = enum__sai_acl_entry_attr_t# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3186

enum__sai_acl_counter_attr_t = c_int# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3271

SAI_ACL_COUNTER_ATTR_START = 0# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3271

SAI_ACL_COUNTER_ATTR_TABLE_ID = SAI_ACL_COUNTER_ATTR_START# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3271

SAI_ACL_COUNTER_ATTR_ENABLE_PACKET_COUNT = (SAI_ACL_COUNTER_ATTR_TABLE_ID + 1)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3271

SAI_ACL_COUNTER_ATTR_ENABLE_BYTE_COUNT = (SAI_ACL_COUNTER_ATTR_ENABLE_PACKET_COUNT + 1)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3271

SAI_ACL_COUNTER_ATTR_PACKETS = (SAI_ACL_COUNTER_ATTR_ENABLE_BYTE_COUNT + 1)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3271

SAI_ACL_COUNTER_ATTR_BYTES = (SAI_ACL_COUNTER_ATTR_PACKETS + 1)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3271

SAI_ACL_COUNTER_ATTR_LABEL = (SAI_ACL_COUNTER_ATTR_BYTES + 1)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3271

SAI_ACL_COUNTER_ATTR_END = (SAI_ACL_COUNTER_ATTR_LABEL + 1)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3271

SAI_ACL_COUNTER_ATTR_CUSTOM_RANGE_START = 0x10000000# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3271

SAI_ACL_COUNTER_ATTR_CUSTOM_RANGE_END = (SAI_ACL_COUNTER_ATTR_CUSTOM_RANGE_START + 1)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3271

sai_acl_counter_attr_t = enum__sai_acl_counter_attr_t# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3271

enum__sai_acl_range_type_t = c_int# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3293

SAI_ACL_RANGE_TYPE_L4_SRC_PORT_RANGE = 0# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3293

SAI_ACL_RANGE_TYPE_L4_DST_PORT_RANGE = (SAI_ACL_RANGE_TYPE_L4_SRC_PORT_RANGE + 1)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3293

SAI_ACL_RANGE_TYPE_OUTER_VLAN = (SAI_ACL_RANGE_TYPE_L4_DST_PORT_RANGE + 1)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3293

SAI_ACL_RANGE_TYPE_INNER_VLAN = (SAI_ACL_RANGE_TYPE_OUTER_VLAN + 1)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3293

SAI_ACL_RANGE_TYPE_PACKET_LENGTH = (SAI_ACL_RANGE_TYPE_INNER_VLAN + 1)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3293

sai_acl_range_type_t = enum__sai_acl_range_type_t# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3293

enum__sai_acl_range_attr_t = c_int# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3339

SAI_ACL_RANGE_ATTR_START = 0# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3339

SAI_ACL_RANGE_ATTR_TYPE = SAI_ACL_RANGE_ATTR_START# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3339

SAI_ACL_RANGE_ATTR_LIMIT = (SAI_ACL_RANGE_ATTR_TYPE + 1)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3339

SAI_ACL_RANGE_ATTR_END = (SAI_ACL_RANGE_ATTR_LIMIT + 1)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3339

SAI_ACL_RANGE_ATTR_CUSTOM_RANGE_START = 0x10000000# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3339

SAI_ACL_RANGE_ATTR_CUSTOM_RANGE_END = (SAI_ACL_RANGE_ATTR_CUSTOM_RANGE_START + 1)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3339

sai_acl_range_attr_t = enum__sai_acl_range_attr_t# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3339

sai_create_acl_table_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3351

sai_remove_acl_table_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3364

sai_set_acl_table_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3375

sai_get_acl_table_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3388

sai_create_acl_entry_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3403

sai_remove_acl_entry_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3416

sai_set_acl_entry_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3427

sai_get_acl_entry_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3440

sai_create_acl_counter_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3455

sai_remove_acl_counter_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3468

sai_set_acl_counter_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3479

sai_get_acl_counter_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3492

sai_create_acl_range_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3507

sai_remove_acl_range_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3520

sai_set_acl_range_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3531

sai_get_acl_range_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3544

sai_create_acl_table_group_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3559

sai_remove_acl_table_group_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3572

sai_set_acl_table_group_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3583

sai_get_acl_table_group_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3596

sai_create_acl_table_group_member_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3611

sai_remove_acl_table_group_member_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3624

sai_set_acl_table_group_member_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3635

sai_get_acl_table_group_member_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3648

sai_create_acl_table_chain_group_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3663

sai_remove_acl_table_chain_group_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t)# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3676

sai_set_acl_table_chain_group_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3687

sai_get_acl_table_chain_group_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3700

# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3738
class struct__sai_acl_api_t(Structure):
    pass

struct__sai_acl_api_t.__slots__ = [
    'create_acl_table',
    'remove_acl_table',
    'set_acl_table_attribute',
    'get_acl_table_attribute',
    'create_acl_entry',
    'remove_acl_entry',
    'set_acl_entry_attribute',
    'get_acl_entry_attribute',
    'create_acl_counter',
    'remove_acl_counter',
    'set_acl_counter_attribute',
    'get_acl_counter_attribute',
    'create_acl_range',
    'remove_acl_range',
    'set_acl_range_attribute',
    'get_acl_range_attribute',
    'create_acl_table_group',
    'remove_acl_table_group',
    'set_acl_table_group_attribute',
    'get_acl_table_group_attribute',
    'create_acl_table_group_member',
    'remove_acl_table_group_member',
    'set_acl_table_group_member_attribute',
    'get_acl_table_group_member_attribute',
    'create_acl_table_chain_group',
    'remove_acl_table_chain_group',
    'set_acl_table_chain_group_attribute',
    'get_acl_table_chain_group_attribute',
]
struct__sai_acl_api_t._fields_ = [
    ('create_acl_table', sai_create_acl_table_fn),
    ('remove_acl_table', sai_remove_acl_table_fn),
    ('set_acl_table_attribute', sai_set_acl_table_attribute_fn),
    ('get_acl_table_attribute', sai_get_acl_table_attribute_fn),
    ('create_acl_entry', sai_create_acl_entry_fn),
    ('remove_acl_entry', sai_remove_acl_entry_fn),
    ('set_acl_entry_attribute', sai_set_acl_entry_attribute_fn),
    ('get_acl_entry_attribute', sai_get_acl_entry_attribute_fn),
    ('create_acl_counter', sai_create_acl_counter_fn),
    ('remove_acl_counter', sai_remove_acl_counter_fn),
    ('set_acl_counter_attribute', sai_set_acl_counter_attribute_fn),
    ('get_acl_counter_attribute', sai_get_acl_counter_attribute_fn),
    ('create_acl_range', sai_create_acl_range_fn),
    ('remove_acl_range', sai_remove_acl_range_fn),
    ('set_acl_range_attribute', sai_set_acl_range_attribute_fn),
    ('get_acl_range_attribute', sai_get_acl_range_attribute_fn),
    ('create_acl_table_group', sai_create_acl_table_group_fn),
    ('remove_acl_table_group', sai_remove_acl_table_group_fn),
    ('set_acl_table_group_attribute', sai_set_acl_table_group_attribute_fn),
    ('get_acl_table_group_attribute', sai_get_acl_table_group_attribute_fn),
    ('create_acl_table_group_member', sai_create_acl_table_group_member_fn),
    ('remove_acl_table_group_member', sai_remove_acl_table_group_member_fn),
    ('set_acl_table_group_member_attribute', sai_set_acl_table_group_member_attribute_fn),
    ('get_acl_table_group_member_attribute', sai_get_acl_table_group_member_attribute_fn),
    ('create_acl_table_chain_group', sai_create_acl_table_chain_group_fn),
    ('remove_acl_table_chain_group', sai_remove_acl_table_chain_group_fn),
    ('set_acl_table_chain_group_attribute', sai_set_acl_table_chain_group_attribute_fn),
    ('get_acl_table_chain_group_attribute', sai_get_acl_table_chain_group_attribute_fn),
]

sai_acl_api_t = struct__sai_acl_api_t# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3738

enum__sai_ars_mode_t = c_int# /home/bluecmd/Downloads/SAI/inc/saiars.h: 56

SAI_ARS_MODE_FLOWLET_QUALITY = 0# /home/bluecmd/Downloads/SAI/inc/saiars.h: 56

SAI_ARS_MODE_FLOWLET_RANDOM = (SAI_ARS_MODE_FLOWLET_QUALITY + 1)# /home/bluecmd/Downloads/SAI/inc/saiars.h: 56

SAI_ARS_MODE_PER_PACKET_QUALITY = (SAI_ARS_MODE_FLOWLET_RANDOM + 1)# /home/bluecmd/Downloads/SAI/inc/saiars.h: 56

SAI_ARS_MODE_PER_PACKET_RANDOM = (SAI_ARS_MODE_PER_PACKET_QUALITY + 1)# /home/bluecmd/Downloads/SAI/inc/saiars.h: 56

SAI_ARS_MODE_FIXED = (SAI_ARS_MODE_PER_PACKET_RANDOM + 1)# /home/bluecmd/Downloads/SAI/inc/saiars.h: 56

sai_ars_mode_t = enum__sai_ars_mode_t# /home/bluecmd/Downloads/SAI/inc/saiars.h: 56

enum__sai_ars_attr_t = c_int# /home/bluecmd/Downloads/SAI/inc/saiars.h: 174

SAI_ARS_ATTR_START = 0# /home/bluecmd/Downloads/SAI/inc/saiars.h: 174

SAI_ARS_ATTR_MODE = SAI_ARS_ATTR_START# /home/bluecmd/Downloads/SAI/inc/saiars.h: 174

SAI_ARS_ATTR_IDLE_TIME = (SAI_ARS_ATTR_MODE + 1)# /home/bluecmd/Downloads/SAI/inc/saiars.h: 174

SAI_ARS_ATTR_MAX_FLOWS = (SAI_ARS_ATTR_IDLE_TIME + 1)# /home/bluecmd/Downloads/SAI/inc/saiars.h: 174

SAI_ARS_ATTR_MON_ENABLE = (SAI_ARS_ATTR_MAX_FLOWS + 1)# /home/bluecmd/Downloads/SAI/inc/saiars.h: 174

SAI_ARS_ATTR_SAMPLEPACKET_ENABLE = (SAI_ARS_ATTR_MON_ENABLE + 1)# /home/bluecmd/Downloads/SAI/inc/saiars.h: 174

SAI_ARS_ATTR_MAX_ALT_MEMEBERS_PER_GROUP = (SAI_ARS_ATTR_SAMPLEPACKET_ENABLE + 1)# /home/bluecmd/Downloads/SAI/inc/saiars.h: 174

SAI_ARS_ATTR_MAX_PRIMARY_MEMEBERS_PER_GROUP = (SAI_ARS_ATTR_MAX_ALT_MEMEBERS_PER_GROUP + 1)# /home/bluecmd/Downloads/SAI/inc/saiars.h: 174

SAI_ARS_ATTR_PRIMARY_PATH_QUALITY_THRESHOLD = (SAI_ARS_ATTR_MAX_PRIMARY_MEMEBERS_PER_GROUP + 1)# /home/bluecmd/Downloads/SAI/inc/saiars.h: 174

SAI_ARS_ATTR_ALTERNATE_PATH_COST = (SAI_ARS_ATTR_PRIMARY_PATH_QUALITY_THRESHOLD + 1)# /home/bluecmd/Downloads/SAI/inc/saiars.h: 174

SAI_ARS_ATTR_ALTERNATE_PATH_BIAS = (SAI_ARS_ATTR_ALTERNATE_PATH_COST + 1)# /home/bluecmd/Downloads/SAI/inc/saiars.h: 174

SAI_ARS_ATTR_END = (SAI_ARS_ATTR_ALTERNATE_PATH_BIAS + 1)# /home/bluecmd/Downloads/SAI/inc/saiars.h: 174

SAI_ARS_ATTR_CUSTOM_RANGE_START = 0x10000000# /home/bluecmd/Downloads/SAI/inc/saiars.h: 174

SAI_ARS_ATTR_CUSTOM_RANGE_END = (SAI_ARS_ATTR_CUSTOM_RANGE_START + 1)# /home/bluecmd/Downloads/SAI/inc/saiars.h: 174

sai_ars_attr_t = enum__sai_ars_attr_t# /home/bluecmd/Downloads/SAI/inc/saiars.h: 174

sai_create_ars_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saiars.h: 186

sai_remove_ars_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t)# /home/bluecmd/Downloads/SAI/inc/saiars.h: 199

sai_set_ars_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saiars.h: 210

sai_get_ars_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saiars.h: 223

# /home/bluecmd/Downloads/SAI/inc/saiars.h: 237
class struct__sai_ars_api_t(Structure):
    pass

struct__sai_ars_api_t.__slots__ = [
    'create_ars',
    'remove_ars',
    'set_ars_attribute',
    'get_ars_attribute',
]
struct__sai_ars_api_t._fields_ = [
    ('create_ars', sai_create_ars_fn),
    ('remove_ars', sai_remove_ars_fn),
    ('set_ars_attribute', sai_set_ars_attribute_fn),
    ('get_ars_attribute', sai_get_ars_attribute_fn),
]

sai_ars_api_t = struct__sai_ars_api_t# /home/bluecmd/Downloads/SAI/inc/saiars.h: 237

enum__sai_ars_profile_algo_t = c_int# /home/bluecmd/Downloads/SAI/inc/saiarsprofile.h: 44

SAI_ARS_PROFILE_ALGO_EWMA = 0# /home/bluecmd/Downloads/SAI/inc/saiarsprofile.h: 44

sai_ars_profile_algo_t = enum__sai_ars_profile_algo_t# /home/bluecmd/Downloads/SAI/inc/saiarsprofile.h: 44

enum__sai_ars_profile_attr_t = c_int# /home/bluecmd/Downloads/SAI/inc/saiarsprofile.h: 340

SAI_ARS_PROFILE_ATTR_START = 0# /home/bluecmd/Downloads/SAI/inc/saiarsprofile.h: 340

SAI_ARS_PROFILE_ATTR_ALGO = SAI_ARS_PROFILE_ATTR_START# /home/bluecmd/Downloads/SAI/inc/saiarsprofile.h: 340

SAI_ARS_PROFILE_ATTR_SAMPLING_INTERVAL = (SAI_ARS_PROFILE_ATTR_ALGO + 1)# /home/bluecmd/Downloads/SAI/inc/saiarsprofile.h: 340

SAI_ARS_PROFILE_ATTR_ARS_RANDOM_SEED = (SAI_ARS_PROFILE_ATTR_SAMPLING_INTERVAL + 1)# /home/bluecmd/Downloads/SAI/inc/saiarsprofile.h: 340

SAI_ARS_PROFILE_ATTR_ECMP_ARS_MAX_GROUPS = (SAI_ARS_PROFILE_ATTR_ARS_RANDOM_SEED + 1)# /home/bluecmd/Downloads/SAI/inc/saiarsprofile.h: 340

SAI_ARS_PROFILE_ATTR_ECMP_ARS_MAX_MEMBERS_PER_GROUP = (SAI_ARS_PROFILE_ATTR_ECMP_ARS_MAX_GROUPS + 1)# /home/bluecmd/Downloads/SAI/inc/saiarsprofile.h: 340

SAI_ARS_PROFILE_ATTR_LAG_ARS_MAX_GROUPS = (SAI_ARS_PROFILE_ATTR_ECMP_ARS_MAX_MEMBERS_PER_GROUP + 1)# /home/bluecmd/Downloads/SAI/inc/saiarsprofile.h: 340

SAI_ARS_PROFILE_ATTR_LAG_ARS_MAX_MEMBERS_PER_GROUP = (SAI_ARS_PROFILE_ATTR_LAG_ARS_MAX_GROUPS + 1)# /home/bluecmd/Downloads/SAI/inc/saiarsprofile.h: 340

SAI_ARS_PROFILE_ATTR_PORT_LOAD_PAST = (SAI_ARS_PROFILE_ATTR_LAG_ARS_MAX_MEMBERS_PER_GROUP + 1)# /home/bluecmd/Downloads/SAI/inc/saiarsprofile.h: 340

SAI_ARS_PROFILE_ATTR_PORT_LOAD_PAST_WEIGHT = (SAI_ARS_PROFILE_ATTR_PORT_LOAD_PAST + 1)# /home/bluecmd/Downloads/SAI/inc/saiarsprofile.h: 340

SAI_ARS_PROFILE_ATTR_PORT_LOAD_FUTURE = (SAI_ARS_PROFILE_ATTR_PORT_LOAD_PAST_WEIGHT + 1)# /home/bluecmd/Downloads/SAI/inc/saiarsprofile.h: 340

SAI_ARS_PROFILE_ATTR_PORT_LOAD_FUTURE_WEIGHT = (SAI_ARS_PROFILE_ATTR_PORT_LOAD_FUTURE + 1)# /home/bluecmd/Downloads/SAI/inc/saiarsprofile.h: 340

SAI_ARS_PROFILE_ATTR_PORT_LOAD_CURRENT = (SAI_ARS_PROFILE_ATTR_PORT_LOAD_FUTURE_WEIGHT + 1)# /home/bluecmd/Downloads/SAI/inc/saiarsprofile.h: 340

SAI_ARS_PROFILE_ATTR_PORT_LOAD_EXPONENT = (SAI_ARS_PROFILE_ATTR_PORT_LOAD_CURRENT + 1)# /home/bluecmd/Downloads/SAI/inc/saiarsprofile.h: 340

SAI_ARS_PROFILE_ATTR_QUANT_BANDS = (SAI_ARS_PROFILE_ATTR_PORT_LOAD_EXPONENT + 1)# /home/bluecmd/Downloads/SAI/inc/saiarsprofile.h: 340

SAI_ARS_PROFILE_ATTR_QUANT_BAND_0_MIN_THRESHOLD = (SAI_ARS_PROFILE_ATTR_QUANT_BANDS + 1)# /home/bluecmd/Downloads/SAI/inc/saiarsprofile.h: 340

SAI_ARS_PROFILE_ATTR_QUANT_BAND_0_MAX_THRESHOLD = (SAI_ARS_PROFILE_ATTR_QUANT_BAND_0_MIN_THRESHOLD + 1)# /home/bluecmd/Downloads/SAI/inc/saiarsprofile.h: 340

SAI_ARS_PROFILE_ATTR_QUANT_BAND_1_MIN_THRESHOLD = (SAI_ARS_PROFILE_ATTR_QUANT_BAND_0_MAX_THRESHOLD + 1)# /home/bluecmd/Downloads/SAI/inc/saiarsprofile.h: 340

SAI_ARS_PROFILE_ATTR_QUANT_BAND_1_MAX_THRESHOLD = (SAI_ARS_PROFILE_ATTR_QUANT_BAND_1_MIN_THRESHOLD + 1)# /home/bluecmd/Downloads/SAI/inc/saiarsprofile.h: 340

SAI_ARS_PROFILE_ATTR_QUANT_BAND_2_MIN_THRESHOLD = (SAI_ARS_PROFILE_ATTR_QUANT_BAND_1_MAX_THRESHOLD + 1)# /home/bluecmd/Downloads/SAI/inc/saiarsprofile.h: 340

SAI_ARS_PROFILE_ATTR_QUANT_BAND_2_MAX_THRESHOLD = (SAI_ARS_PROFILE_ATTR_QUANT_BAND_2_MIN_THRESHOLD + 1)# /home/bluecmd/Downloads/SAI/inc/saiarsprofile.h: 340

SAI_ARS_PROFILE_ATTR_QUANT_BAND_3_MIN_THRESHOLD = (SAI_ARS_PROFILE_ATTR_QUANT_BAND_2_MAX_THRESHOLD + 1)# /home/bluecmd/Downloads/SAI/inc/saiarsprofile.h: 340

SAI_ARS_PROFILE_ATTR_QUANT_BAND_3_MAX_THRESHOLD = (SAI_ARS_PROFILE_ATTR_QUANT_BAND_3_MIN_THRESHOLD + 1)# /home/bluecmd/Downloads/SAI/inc/saiarsprofile.h: 340

SAI_ARS_PROFILE_ATTR_QUANT_BAND_4_MIN_THRESHOLD = (SAI_ARS_PROFILE_ATTR_QUANT_BAND_3_MAX_THRESHOLD + 1)# /home/bluecmd/Downloads/SAI/inc/saiarsprofile.h: 340

SAI_ARS_PROFILE_ATTR_QUANT_BAND_4_MAX_THRESHOLD = (SAI_ARS_PROFILE_ATTR_QUANT_BAND_4_MIN_THRESHOLD + 1)# /home/bluecmd/Downloads/SAI/inc/saiarsprofile.h: 340

SAI_ARS_PROFILE_ATTR_QUANT_BAND_5_MIN_THRESHOLD = (SAI_ARS_PROFILE_ATTR_QUANT_BAND_4_MAX_THRESHOLD + 1)# /home/bluecmd/Downloads/SAI/inc/saiarsprofile.h: 340

SAI_ARS_PROFILE_ATTR_QUANT_BAND_5_MAX_THRESHOLD = (SAI_ARS_PROFILE_ATTR_QUANT_BAND_5_MIN_THRESHOLD + 1)# /home/bluecmd/Downloads/SAI/inc/saiarsprofile.h: 340

SAI_ARS_PROFILE_ATTR_QUANT_BAND_6_MIN_THRESHOLD = (SAI_ARS_PROFILE_ATTR_QUANT_BAND_5_MAX_THRESHOLD + 1)# /home/bluecmd/Downloads/SAI/inc/saiarsprofile.h: 340

SAI_ARS_PROFILE_ATTR_QUANT_BAND_6_MAX_THRESHOLD = (SAI_ARS_PROFILE_ATTR_QUANT_BAND_6_MIN_THRESHOLD + 1)# /home/bluecmd/Downloads/SAI/inc/saiarsprofile.h: 340

SAI_ARS_PROFILE_ATTR_QUANT_BAND_7_MIN_THRESHOLD = (SAI_ARS_PROFILE_ATTR_QUANT_BAND_6_MAX_THRESHOLD + 1)# /home/bluecmd/Downloads/SAI/inc/saiarsprofile.h: 340

SAI_ARS_PROFILE_ATTR_QUANT_BAND_7_MAX_THRESHOLD = (SAI_ARS_PROFILE_ATTR_QUANT_BAND_7_MIN_THRESHOLD + 1)# /home/bluecmd/Downloads/SAI/inc/saiarsprofile.h: 340

SAI_ARS_PROFILE_ATTR_END = (SAI_ARS_PROFILE_ATTR_QUANT_BAND_7_MAX_THRESHOLD + 1)# /home/bluecmd/Downloads/SAI/inc/saiarsprofile.h: 340

SAI_ARS_PROFILE_ATTR_CUSTOM_RANGE_START = 0x10000000# /home/bluecmd/Downloads/SAI/inc/saiarsprofile.h: 340

SAI_ARS_PROFILE_ATTR_CUSTOM_RANGE_END = (SAI_ARS_PROFILE_ATTR_CUSTOM_RANGE_START + 1)# /home/bluecmd/Downloads/SAI/inc/saiarsprofile.h: 340

sai_ars_profile_attr_t = enum__sai_ars_profile_attr_t# /home/bluecmd/Downloads/SAI/inc/saiarsprofile.h: 340

sai_create_ars_profile_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saiarsprofile.h: 352

sai_remove_ars_profile_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t)# /home/bluecmd/Downloads/SAI/inc/saiarsprofile.h: 365

sai_set_ars_profile_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saiarsprofile.h: 376

sai_get_ars_profile_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saiarsprofile.h: 389

# /home/bluecmd/Downloads/SAI/inc/saiarsprofile.h: 404
class struct__sai_ars_profile_api_t(Structure):
    pass

struct__sai_ars_profile_api_t.__slots__ = [
    'create_ars_profile',
    'remove_ars_profile',
    'set_ars_profile_attribute',
    'get_ars_profile_attribute',
]
struct__sai_ars_profile_api_t._fields_ = [
    ('create_ars_profile', sai_create_ars_profile_fn),
    ('remove_ars_profile', sai_remove_ars_profile_fn),
    ('set_ars_profile_attribute', sai_set_ars_profile_attribute_fn),
    ('get_ars_profile_attribute', sai_get_ars_profile_attribute_fn),
]

sai_ars_profile_api_t = struct__sai_ars_profile_api_t# /home/bluecmd/Downloads/SAI/inc/saiarsprofile.h: 404

enum__sai_bfd_session_type_t = c_int# /home/bluecmd/Downloads/SAI/inc/saibfd.h: 53

SAI_BFD_SESSION_TYPE_DEMAND_ACTIVE = 0# /home/bluecmd/Downloads/SAI/inc/saibfd.h: 53

SAI_BFD_SESSION_TYPE_DEMAND_PASSIVE = (SAI_BFD_SESSION_TYPE_DEMAND_ACTIVE + 1)# /home/bluecmd/Downloads/SAI/inc/saibfd.h: 53

SAI_BFD_SESSION_TYPE_ASYNC_ACTIVE = (SAI_BFD_SESSION_TYPE_DEMAND_PASSIVE + 1)# /home/bluecmd/Downloads/SAI/inc/saibfd.h: 53

SAI_BFD_SESSION_TYPE_ASYNC_PASSIVE = (SAI_BFD_SESSION_TYPE_ASYNC_ACTIVE + 1)# /home/bluecmd/Downloads/SAI/inc/saibfd.h: 53

sai_bfd_session_type_t = enum__sai_bfd_session_type_t# /home/bluecmd/Downloads/SAI/inc/saibfd.h: 53

enum__sai_bfd_session_offload_type_t = c_int# /home/bluecmd/Downloads/SAI/inc/saibfd.h: 69

SAI_BFD_SESSION_OFFLOAD_TYPE_NONE = 0# /home/bluecmd/Downloads/SAI/inc/saibfd.h: 69

SAI_BFD_SESSION_OFFLOAD_TYPE_FULL = (SAI_BFD_SESSION_OFFLOAD_TYPE_NONE + 1)# /home/bluecmd/Downloads/SAI/inc/saibfd.h: 69

SAI_BFD_SESSION_OFFLOAD_TYPE_SUSTENANCE = (SAI_BFD_SESSION_OFFLOAD_TYPE_FULL + 1)# /home/bluecmd/Downloads/SAI/inc/saibfd.h: 69

sai_bfd_session_offload_type_t = enum__sai_bfd_session_offload_type_t# /home/bluecmd/Downloads/SAI/inc/saibfd.h: 69

enum__sai_bfd_encapsulation_type_t = c_int# /home/bluecmd/Downloads/SAI/inc/saibfd.h: 96

SAI_BFD_ENCAPSULATION_TYPE_IP_IN_IP = 0# /home/bluecmd/Downloads/SAI/inc/saibfd.h: 96

SAI_BFD_ENCAPSULATION_TYPE_L3_GRE_TUNNEL = (SAI_BFD_ENCAPSULATION_TYPE_IP_IN_IP + 1)# /home/bluecmd/Downloads/SAI/inc/saibfd.h: 96

SAI_BFD_ENCAPSULATION_TYPE_NONE = (SAI_BFD_ENCAPSULATION_TYPE_L3_GRE_TUNNEL + 1)# /home/bluecmd/Downloads/SAI/inc/saibfd.h: 96

SAI_BFD_ENCAPSULATION_TYPE_SRV6 = (SAI_BFD_ENCAPSULATION_TYPE_NONE + 1)# /home/bluecmd/Downloads/SAI/inc/saibfd.h: 96

sai_bfd_encapsulation_type_t = enum__sai_bfd_encapsulation_type_t# /home/bluecmd/Downloads/SAI/inc/saibfd.h: 96

enum__sai_bfd_session_state_t = c_int# /home/bluecmd/Downloads/SAI/inc/saibfd.h: 115

SAI_BFD_SESSION_STATE_ADMIN_DOWN = 0# /home/bluecmd/Downloads/SAI/inc/saibfd.h: 115

SAI_BFD_SESSION_STATE_DOWN = (SAI_BFD_SESSION_STATE_ADMIN_DOWN + 1)# /home/bluecmd/Downloads/SAI/inc/saibfd.h: 115

SAI_BFD_SESSION_STATE_INIT = (SAI_BFD_SESSION_STATE_DOWN + 1)# /home/bluecmd/Downloads/SAI/inc/saibfd.h: 115

SAI_BFD_SESSION_STATE_UP = (SAI_BFD_SESSION_STATE_INIT + 1)# /home/bluecmd/Downloads/SAI/inc/saibfd.h: 115

sai_bfd_session_state_t = enum__sai_bfd_session_state_t# /home/bluecmd/Downloads/SAI/inc/saibfd.h: 115

# /home/bluecmd/Downloads/SAI/inc/saibfd.h: 132
class struct__sai_bfd_session_state_notification_t(Structure):
    pass

struct__sai_bfd_session_state_notification_t.__slots__ = [
    'bfd_session_id',
    'session_state',
]
struct__sai_bfd_session_state_notification_t._fields_ = [
    ('bfd_session_id', sai_object_id_t),
    ('session_state', sai_bfd_session_state_t),
]

sai_bfd_session_state_notification_t = struct__sai_bfd_session_state_notification_t# /home/bluecmd/Downloads/SAI/inc/saibfd.h: 132

enum__sai_bfd_session_attr_t = c_int# /home/bluecmd/Downloads/SAI/inc/saibfd.h: 515

SAI_BFD_SESSION_ATTR_START = 0# /home/bluecmd/Downloads/SAI/inc/saibfd.h: 515

SAI_BFD_SESSION_ATTR_TYPE = SAI_BFD_SESSION_ATTR_START# /home/bluecmd/Downloads/SAI/inc/saibfd.h: 515

SAI_BFD_SESSION_ATTR_HW_LOOKUP_VALID = (SAI_BFD_SESSION_ATTR_TYPE + 1)# /home/bluecmd/Downloads/SAI/inc/saibfd.h: 515

SAI_BFD_SESSION_ATTR_VIRTUAL_ROUTER = (SAI_BFD_SESSION_ATTR_HW_LOOKUP_VALID + 1)# /home/bluecmd/Downloads/SAI/inc/saibfd.h: 515

SAI_BFD_SESSION_ATTR_PORT = (SAI_BFD_SESSION_ATTR_VIRTUAL_ROUTER + 1)# /home/bluecmd/Downloads/SAI/inc/saibfd.h: 515

SAI_BFD_SESSION_ATTR_LOCAL_DISCRIMINATOR = (SAI_BFD_SESSION_ATTR_PORT + 1)# /home/bluecmd/Downloads/SAI/inc/saibfd.h: 515

SAI_BFD_SESSION_ATTR_REMOTE_DISCRIMINATOR = (SAI_BFD_SESSION_ATTR_LOCAL_DISCRIMINATOR + 1)# /home/bluecmd/Downloads/SAI/inc/saibfd.h: 515

SAI_BFD_SESSION_ATTR_UDP_SRC_PORT = (SAI_BFD_SESSION_ATTR_REMOTE_DISCRIMINATOR + 1)# /home/bluecmd/Downloads/SAI/inc/saibfd.h: 515

SAI_BFD_SESSION_ATTR_TC = (SAI_BFD_SESSION_ATTR_UDP_SRC_PORT + 1)# /home/bluecmd/Downloads/SAI/inc/saibfd.h: 515

SAI_BFD_SESSION_ATTR_VLAN_TPID = (SAI_BFD_SESSION_ATTR_TC + 1)# /home/bluecmd/Downloads/SAI/inc/saibfd.h: 515

SAI_BFD_SESSION_ATTR_VLAN_ID = (SAI_BFD_SESSION_ATTR_VLAN_TPID + 1)# /home/bluecmd/Downloads/SAI/inc/saibfd.h: 515

SAI_BFD_SESSION_ATTR_VLAN_PRI = (SAI_BFD_SESSION_ATTR_VLAN_ID + 1)# /home/bluecmd/Downloads/SAI/inc/saibfd.h: 515

SAI_BFD_SESSION_ATTR_VLAN_CFI = (SAI_BFD_SESSION_ATTR_VLAN_PRI + 1)# /home/bluecmd/Downloads/SAI/inc/saibfd.h: 515

SAI_BFD_SESSION_ATTR_VLAN_HEADER_VALID = (SAI_BFD_SESSION_ATTR_VLAN_CFI + 1)# /home/bluecmd/Downloads/SAI/inc/saibfd.h: 515

SAI_BFD_SESSION_ATTR_BFD_ENCAPSULATION_TYPE = (SAI_BFD_SESSION_ATTR_VLAN_HEADER_VALID + 1)# /home/bluecmd/Downloads/SAI/inc/saibfd.h: 515

SAI_BFD_SESSION_ATTR_IPHDR_VERSION = (SAI_BFD_SESSION_ATTR_BFD_ENCAPSULATION_TYPE + 1)# /home/bluecmd/Downloads/SAI/inc/saibfd.h: 515

SAI_BFD_SESSION_ATTR_TOS = (SAI_BFD_SESSION_ATTR_IPHDR_VERSION + 1)# /home/bluecmd/Downloads/SAI/inc/saibfd.h: 515

SAI_BFD_SESSION_ATTR_TTL = (SAI_BFD_SESSION_ATTR_TOS + 1)# /home/bluecmd/Downloads/SAI/inc/saibfd.h: 515

SAI_BFD_SESSION_ATTR_SRC_IP_ADDRESS = (SAI_BFD_SESSION_ATTR_TTL + 1)# /home/bluecmd/Downloads/SAI/inc/saibfd.h: 515

SAI_BFD_SESSION_ATTR_DST_IP_ADDRESS = (SAI_BFD_SESSION_ATTR_SRC_IP_ADDRESS + 1)# /home/bluecmd/Downloads/SAI/inc/saibfd.h: 515

SAI_BFD_SESSION_ATTR_TUNNEL_TOS = (SAI_BFD_SESSION_ATTR_DST_IP_ADDRESS + 1)# /home/bluecmd/Downloads/SAI/inc/saibfd.h: 515

SAI_BFD_SESSION_ATTR_TUNNEL_TTL = (SAI_BFD_SESSION_ATTR_TUNNEL_TOS + 1)# /home/bluecmd/Downloads/SAI/inc/saibfd.h: 515

SAI_BFD_SESSION_ATTR_TUNNEL_SRC_IP_ADDRESS = (SAI_BFD_SESSION_ATTR_TUNNEL_TTL + 1)# /home/bluecmd/Downloads/SAI/inc/saibfd.h: 515

SAI_BFD_SESSION_ATTR_TUNNEL_DST_IP_ADDRESS = (SAI_BFD_SESSION_ATTR_TUNNEL_SRC_IP_ADDRESS + 1)# /home/bluecmd/Downloads/SAI/inc/saibfd.h: 515

SAI_BFD_SESSION_ATTR_SRC_MAC_ADDRESS = (SAI_BFD_SESSION_ATTR_TUNNEL_DST_IP_ADDRESS + 1)# /home/bluecmd/Downloads/SAI/inc/saibfd.h: 515

SAI_BFD_SESSION_ATTR_DST_MAC_ADDRESS = (SAI_BFD_SESSION_ATTR_SRC_MAC_ADDRESS + 1)# /home/bluecmd/Downloads/SAI/inc/saibfd.h: 515

SAI_BFD_SESSION_ATTR_ECHO_ENABLE = (SAI_BFD_SESSION_ATTR_DST_MAC_ADDRESS + 1)# /home/bluecmd/Downloads/SAI/inc/saibfd.h: 515

SAI_BFD_SESSION_ATTR_MULTIHOP = (SAI_BFD_SESSION_ATTR_ECHO_ENABLE + 1)# /home/bluecmd/Downloads/SAI/inc/saibfd.h: 515

SAI_BFD_SESSION_ATTR_CBIT = (SAI_BFD_SESSION_ATTR_MULTIHOP + 1)# /home/bluecmd/Downloads/SAI/inc/saibfd.h: 515

SAI_BFD_SESSION_ATTR_MIN_TX = (SAI_BFD_SESSION_ATTR_CBIT + 1)# /home/bluecmd/Downloads/SAI/inc/saibfd.h: 515

SAI_BFD_SESSION_ATTR_MIN_RX = (SAI_BFD_SESSION_ATTR_MIN_TX + 1)# /home/bluecmd/Downloads/SAI/inc/saibfd.h: 515

SAI_BFD_SESSION_ATTR_MULTIPLIER = (SAI_BFD_SESSION_ATTR_MIN_RX + 1)# /home/bluecmd/Downloads/SAI/inc/saibfd.h: 515

SAI_BFD_SESSION_ATTR_REMOTE_MIN_TX = (SAI_BFD_SESSION_ATTR_MULTIPLIER + 1)# /home/bluecmd/Downloads/SAI/inc/saibfd.h: 515

SAI_BFD_SESSION_ATTR_REMOTE_MIN_RX = (SAI_BFD_SESSION_ATTR_REMOTE_MIN_TX + 1)# /home/bluecmd/Downloads/SAI/inc/saibfd.h: 515

SAI_BFD_SESSION_ATTR_STATE = (SAI_BFD_SESSION_ATTR_REMOTE_MIN_RX + 1)# /home/bluecmd/Downloads/SAI/inc/saibfd.h: 515

SAI_BFD_SESSION_ATTR_OFFLOAD_TYPE = (SAI_BFD_SESSION_ATTR_STATE + 1)# /home/bluecmd/Downloads/SAI/inc/saibfd.h: 515

SAI_BFD_SESSION_ATTR_NEGOTIATED_TX = (SAI_BFD_SESSION_ATTR_OFFLOAD_TYPE + 1)# /home/bluecmd/Downloads/SAI/inc/saibfd.h: 515

SAI_BFD_SESSION_ATTR_NEGOTIATED_RX = (SAI_BFD_SESSION_ATTR_NEGOTIATED_TX + 1)# /home/bluecmd/Downloads/SAI/inc/saibfd.h: 515

SAI_BFD_SESSION_ATTR_LOCAL_DIAG = (SAI_BFD_SESSION_ATTR_NEGOTIATED_RX + 1)# /home/bluecmd/Downloads/SAI/inc/saibfd.h: 515

SAI_BFD_SESSION_ATTR_REMOTE_DIAG = (SAI_BFD_SESSION_ATTR_LOCAL_DIAG + 1)# /home/bluecmd/Downloads/SAI/inc/saibfd.h: 515

SAI_BFD_SESSION_ATTR_REMOTE_MULTIPLIER = (SAI_BFD_SESSION_ATTR_REMOTE_DIAG + 1)# /home/bluecmd/Downloads/SAI/inc/saibfd.h: 515

SAI_BFD_SESSION_ATTR_SRV6_SIDLIST_ID = (SAI_BFD_SESSION_ATTR_REMOTE_MULTIPLIER + 1)# /home/bluecmd/Downloads/SAI/inc/saibfd.h: 515

SAI_BFD_SESSION_ATTR_END = (SAI_BFD_SESSION_ATTR_SRV6_SIDLIST_ID + 1)# /home/bluecmd/Downloads/SAI/inc/saibfd.h: 515

SAI_BFD_SESSION_ATTR_CUSTOM_RANGE_START = 0x10000000# /home/bluecmd/Downloads/SAI/inc/saibfd.h: 515

SAI_BFD_SESSION_ATTR_CUSTOM_RANGE_END = (SAI_BFD_SESSION_ATTR_CUSTOM_RANGE_START + 1)# /home/bluecmd/Downloads/SAI/inc/saibfd.h: 515

sai_bfd_session_attr_t = enum__sai_bfd_session_attr_t# /home/bluecmd/Downloads/SAI/inc/saibfd.h: 515

enum__sai_bfd_session_stat_t = c_int# /home/bluecmd/Downloads/SAI/inc/saibfd.h: 531

SAI_BFD_SESSION_STAT_IN_PACKETS = 0# /home/bluecmd/Downloads/SAI/inc/saibfd.h: 531

SAI_BFD_SESSION_STAT_OUT_PACKETS = (SAI_BFD_SESSION_STAT_IN_PACKETS + 1)# /home/bluecmd/Downloads/SAI/inc/saibfd.h: 531

SAI_BFD_SESSION_STAT_DROP_PACKETS = (SAI_BFD_SESSION_STAT_OUT_PACKETS + 1)# /home/bluecmd/Downloads/SAI/inc/saibfd.h: 531

sai_bfd_session_stat_t = enum__sai_bfd_session_stat_t# /home/bluecmd/Downloads/SAI/inc/saibfd.h: 531

sai_create_bfd_session_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saibfd.h: 544

sai_remove_bfd_session_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t)# /home/bluecmd/Downloads/SAI/inc/saibfd.h: 558

sai_set_bfd_session_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saibfd.h: 570

sai_get_bfd_session_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saibfd.h: 584

sai_get_bfd_session_stats_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, uint32_t, POINTER(sai_stat_id_t), POINTER(uint64_t))# /home/bluecmd/Downloads/SAI/inc/saibfd.h: 599

sai_get_bfd_session_stats_ext_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, uint32_t, POINTER(sai_stat_id_t), sai_stats_mode_t, POINTER(uint64_t))# /home/bluecmd/Downloads/SAI/inc/saibfd.h: 616

sai_clear_bfd_session_stats_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, uint32_t, POINTER(sai_stat_id_t))# /home/bluecmd/Downloads/SAI/inc/saibfd.h: 632

sai_bfd_session_state_change_notification_fn = CFUNCTYPE(UNCHECKED(None), uint32_t, POINTER(sai_bfd_session_state_notification_t))# /home/bluecmd/Downloads/SAI/inc/saibfd.h: 647

# /home/bluecmd/Downloads/SAI/inc/saibfd.h: 664
class struct__sai_bfd_api_t(Structure):
    pass

struct__sai_bfd_api_t.__slots__ = [
    'create_bfd_session',
    'remove_bfd_session',
    'set_bfd_session_attribute',
    'get_bfd_session_attribute',
    'get_bfd_session_stats',
    'get_bfd_session_stats_ext',
    'clear_bfd_session_stats',
]
struct__sai_bfd_api_t._fields_ = [
    ('create_bfd_session', sai_create_bfd_session_fn),
    ('remove_bfd_session', sai_remove_bfd_session_fn),
    ('set_bfd_session_attribute', sai_set_bfd_session_attribute_fn),
    ('get_bfd_session_attribute', sai_get_bfd_session_attribute_fn),
    ('get_bfd_session_stats', sai_get_bfd_session_stats_fn),
    ('get_bfd_session_stats_ext', sai_get_bfd_session_stats_ext_fn),
    ('clear_bfd_session_stats', sai_clear_bfd_session_stats_fn),
]

sai_bfd_api_t = struct__sai_bfd_api_t# /home/bluecmd/Downloads/SAI/inc/saibfd.h: 664

enum__sai_bridge_port_fdb_learning_mode_t = c_int# /home/bluecmd/Downloads/SAI/inc/saibridge.h: 66

SAI_BRIDGE_PORT_FDB_LEARNING_MODE_DROP = 0# /home/bluecmd/Downloads/SAI/inc/saibridge.h: 66

SAI_BRIDGE_PORT_FDB_LEARNING_MODE_DISABLE = (SAI_BRIDGE_PORT_FDB_LEARNING_MODE_DROP + 1)# /home/bluecmd/Downloads/SAI/inc/saibridge.h: 66

SAI_BRIDGE_PORT_FDB_LEARNING_MODE_HW = (SAI_BRIDGE_PORT_FDB_LEARNING_MODE_DISABLE + 1)# /home/bluecmd/Downloads/SAI/inc/saibridge.h: 66

SAI_BRIDGE_PORT_FDB_LEARNING_MODE_CPU_TRAP = (SAI_BRIDGE_PORT_FDB_LEARNING_MODE_HW + 1)# /home/bluecmd/Downloads/SAI/inc/saibridge.h: 66

SAI_BRIDGE_PORT_FDB_LEARNING_MODE_CPU_LOG = (SAI_BRIDGE_PORT_FDB_LEARNING_MODE_CPU_TRAP + 1)# /home/bluecmd/Downloads/SAI/inc/saibridge.h: 66

SAI_BRIDGE_PORT_FDB_LEARNING_MODE_FDB_NOTIFICATION = (SAI_BRIDGE_PORT_FDB_LEARNING_MODE_CPU_LOG + 1)# /home/bluecmd/Downloads/SAI/inc/saibridge.h: 66

sai_bridge_port_fdb_learning_mode_t = enum__sai_bridge_port_fdb_learning_mode_t# /home/bluecmd/Downloads/SAI/inc/saibridge.h: 66

enum__sai_bridge_port_type_t = c_int# /home/bluecmd/Downloads/SAI/inc/saibridge.h: 88

SAI_BRIDGE_PORT_TYPE_PORT = 0# /home/bluecmd/Downloads/SAI/inc/saibridge.h: 88

SAI_BRIDGE_PORT_TYPE_SUB_PORT = (SAI_BRIDGE_PORT_TYPE_PORT + 1)# /home/bluecmd/Downloads/SAI/inc/saibridge.h: 88

SAI_BRIDGE_PORT_TYPE_1Q_ROUTER = (SAI_BRIDGE_PORT_TYPE_SUB_PORT + 1)# /home/bluecmd/Downloads/SAI/inc/saibridge.h: 88

SAI_BRIDGE_PORT_TYPE_1D_ROUTER = (SAI_BRIDGE_PORT_TYPE_1Q_ROUTER + 1)# /home/bluecmd/Downloads/SAI/inc/saibridge.h: 88

SAI_BRIDGE_PORT_TYPE_TUNNEL = (SAI_BRIDGE_PORT_TYPE_1D_ROUTER + 1)# /home/bluecmd/Downloads/SAI/inc/saibridge.h: 88

sai_bridge_port_type_t = enum__sai_bridge_port_type_t# /home/bluecmd/Downloads/SAI/inc/saibridge.h: 88

enum__sai_bridge_port_tagging_mode_t = c_int# /home/bluecmd/Downloads/SAI/inc/saibridge.h: 101

SAI_BRIDGE_PORT_TAGGING_MODE_UNTAGGED = 0# /home/bluecmd/Downloads/SAI/inc/saibridge.h: 101

SAI_BRIDGE_PORT_TAGGING_MODE_TAGGED = (SAI_BRIDGE_PORT_TAGGING_MODE_UNTAGGED + 1)# /home/bluecmd/Downloads/SAI/inc/saibridge.h: 101

sai_bridge_port_tagging_mode_t = enum__sai_bridge_port_tagging_mode_t# /home/bluecmd/Downloads/SAI/inc/saibridge.h: 101

enum__sai_bridge_port_attr_t = c_int# /home/bluecmd/Downloads/SAI/inc/saibridge.h: 273

SAI_BRIDGE_PORT_ATTR_START = 0# /home/bluecmd/Downloads/SAI/inc/saibridge.h: 273

SAI_BRIDGE_PORT_ATTR_TYPE = SAI_BRIDGE_PORT_ATTR_START# /home/bluecmd/Downloads/SAI/inc/saibridge.h: 273

SAI_BRIDGE_PORT_ATTR_PORT_ID = (SAI_BRIDGE_PORT_ATTR_TYPE + 1)# /home/bluecmd/Downloads/SAI/inc/saibridge.h: 273

SAI_BRIDGE_PORT_ATTR_TAGGING_MODE = (SAI_BRIDGE_PORT_ATTR_PORT_ID + 1)# /home/bluecmd/Downloads/SAI/inc/saibridge.h: 273

SAI_BRIDGE_PORT_ATTR_VLAN_ID = (SAI_BRIDGE_PORT_ATTR_TAGGING_MODE + 1)# /home/bluecmd/Downloads/SAI/inc/saibridge.h: 273

SAI_BRIDGE_PORT_ATTR_RIF_ID = (SAI_BRIDGE_PORT_ATTR_VLAN_ID + 1)# /home/bluecmd/Downloads/SAI/inc/saibridge.h: 273

SAI_BRIDGE_PORT_ATTR_TUNNEL_ID = (SAI_BRIDGE_PORT_ATTR_RIF_ID + 1)# /home/bluecmd/Downloads/SAI/inc/saibridge.h: 273

SAI_BRIDGE_PORT_ATTR_BRIDGE_ID = (SAI_BRIDGE_PORT_ATTR_TUNNEL_ID + 1)# /home/bluecmd/Downloads/SAI/inc/saibridge.h: 273

SAI_BRIDGE_PORT_ATTR_FDB_LEARNING_MODE = (SAI_BRIDGE_PORT_ATTR_BRIDGE_ID + 1)# /home/bluecmd/Downloads/SAI/inc/saibridge.h: 273

SAI_BRIDGE_PORT_ATTR_MAX_LEARNED_ADDRESSES = (SAI_BRIDGE_PORT_ATTR_FDB_LEARNING_MODE + 1)# /home/bluecmd/Downloads/SAI/inc/saibridge.h: 273

SAI_BRIDGE_PORT_ATTR_FDB_LEARNING_LIMIT_VIOLATION_PACKET_ACTION = (SAI_BRIDGE_PORT_ATTR_MAX_LEARNED_ADDRESSES + 1)# /home/bluecmd/Downloads/SAI/inc/saibridge.h: 273

SAI_BRIDGE_PORT_ATTR_ADMIN_STATE = (SAI_BRIDGE_PORT_ATTR_FDB_LEARNING_LIMIT_VIOLATION_PACKET_ACTION + 1)# /home/bluecmd/Downloads/SAI/inc/saibridge.h: 273

SAI_BRIDGE_PORT_ATTR_INGRESS_FILTERING = (SAI_BRIDGE_PORT_ATTR_ADMIN_STATE + 1)# /home/bluecmd/Downloads/SAI/inc/saibridge.h: 273

SAI_BRIDGE_PORT_ATTR_EGRESS_FILTERING = (SAI_BRIDGE_PORT_ATTR_INGRESS_FILTERING + 1)# /home/bluecmd/Downloads/SAI/inc/saibridge.h: 273

SAI_BRIDGE_PORT_ATTR_ISOLATION_GROUP = (SAI_BRIDGE_PORT_ATTR_EGRESS_FILTERING + 1)# /home/bluecmd/Downloads/SAI/inc/saibridge.h: 273

SAI_BRIDGE_PORT_ATTR_END = (SAI_BRIDGE_PORT_ATTR_ISOLATION_GROUP + 1)# /home/bluecmd/Downloads/SAI/inc/saibridge.h: 273

SAI_BRIDGE_PORT_ATTR_CUSTOM_RANGE_START = 0x10000000# /home/bluecmd/Downloads/SAI/inc/saibridge.h: 273

SAI_BRIDGE_PORT_ATTR_CUSTOM_RANGE_END = (SAI_BRIDGE_PORT_ATTR_CUSTOM_RANGE_START + 1)# /home/bluecmd/Downloads/SAI/inc/saibridge.h: 273

sai_bridge_port_attr_t = enum__sai_bridge_port_attr_t# /home/bluecmd/Downloads/SAI/inc/saibridge.h: 273

enum__sai_bridge_port_stat_t = c_int# /home/bluecmd/Downloads/SAI/inc/saibridge.h: 292

SAI_BRIDGE_PORT_STAT_IN_OCTETS = 0# /home/bluecmd/Downloads/SAI/inc/saibridge.h: 292

SAI_BRIDGE_PORT_STAT_IN_PACKETS = (SAI_BRIDGE_PORT_STAT_IN_OCTETS + 1)# /home/bluecmd/Downloads/SAI/inc/saibridge.h: 292

SAI_BRIDGE_PORT_STAT_OUT_OCTETS = (SAI_BRIDGE_PORT_STAT_IN_PACKETS + 1)# /home/bluecmd/Downloads/SAI/inc/saibridge.h: 292

SAI_BRIDGE_PORT_STAT_OUT_PACKETS = (SAI_BRIDGE_PORT_STAT_OUT_OCTETS + 1)# /home/bluecmd/Downloads/SAI/inc/saibridge.h: 292

sai_bridge_port_stat_t = enum__sai_bridge_port_stat_t# /home/bluecmd/Downloads/SAI/inc/saibridge.h: 292

sai_create_bridge_port_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saibridge.h: 304

sai_remove_bridge_port_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t)# /home/bluecmd/Downloads/SAI/inc/saibridge.h: 317

sai_set_bridge_port_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saibridge.h: 328

sai_get_bridge_port_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saibridge.h: 341

sai_get_bridge_port_stats_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, uint32_t, POINTER(sai_stat_id_t), POINTER(uint64_t))# /home/bluecmd/Downloads/SAI/inc/saibridge.h: 356

sai_get_bridge_port_stats_ext_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, uint32_t, POINTER(sai_stat_id_t), sai_stats_mode_t, POINTER(uint64_t))# /home/bluecmd/Downloads/SAI/inc/saibridge.h: 373

sai_clear_bridge_port_stats_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, uint32_t, POINTER(sai_stat_id_t))# /home/bluecmd/Downloads/SAI/inc/saibridge.h: 389

enum__sai_bridge_type_t = c_int# /home/bluecmd/Downloads/SAI/inc/saibridge.h: 405

SAI_BRIDGE_TYPE_1Q = 0# /home/bluecmd/Downloads/SAI/inc/saibridge.h: 405

SAI_BRIDGE_TYPE_1D = (SAI_BRIDGE_TYPE_1Q + 1)# /home/bluecmd/Downloads/SAI/inc/saibridge.h: 405

sai_bridge_type_t = enum__sai_bridge_type_t# /home/bluecmd/Downloads/SAI/inc/saibridge.h: 405

enum__sai_bridge_flood_control_type_t = c_int# /home/bluecmd/Downloads/SAI/inc/saibridge.h: 436

SAI_BRIDGE_FLOOD_CONTROL_TYPE_SUB_PORTS = 0# /home/bluecmd/Downloads/SAI/inc/saibridge.h: 436

SAI_BRIDGE_FLOOD_CONTROL_TYPE_NONE = (SAI_BRIDGE_FLOOD_CONTROL_TYPE_SUB_PORTS + 1)# /home/bluecmd/Downloads/SAI/inc/saibridge.h: 436

SAI_BRIDGE_FLOOD_CONTROL_TYPE_L2MC_GROUP = (SAI_BRIDGE_FLOOD_CONTROL_TYPE_NONE + 1)# /home/bluecmd/Downloads/SAI/inc/saibridge.h: 436

SAI_BRIDGE_FLOOD_CONTROL_TYPE_COMBINED = (SAI_BRIDGE_FLOOD_CONTROL_TYPE_L2MC_GROUP + 1)# /home/bluecmd/Downloads/SAI/inc/saibridge.h: 436

sai_bridge_flood_control_type_t = enum__sai_bridge_flood_control_type_t# /home/bluecmd/Downloads/SAI/inc/saibridge.h: 436

enum__sai_bridge_attr_t = c_int# /home/bluecmd/Downloads/SAI/inc/saibridge.h: 577

SAI_BRIDGE_ATTR_START = 0# /home/bluecmd/Downloads/SAI/inc/saibridge.h: 577

SAI_BRIDGE_ATTR_TYPE = SAI_BRIDGE_ATTR_START# /home/bluecmd/Downloads/SAI/inc/saibridge.h: 577

SAI_BRIDGE_ATTR_PORT_LIST = (SAI_BRIDGE_ATTR_TYPE + 1)# /home/bluecmd/Downloads/SAI/inc/saibridge.h: 577

SAI_BRIDGE_ATTR_MAX_LEARNED_ADDRESSES = (SAI_BRIDGE_ATTR_PORT_LIST + 1)# /home/bluecmd/Downloads/SAI/inc/saibridge.h: 577

SAI_BRIDGE_ATTR_LEARN_DISABLE = (SAI_BRIDGE_ATTR_MAX_LEARNED_ADDRESSES + 1)# /home/bluecmd/Downloads/SAI/inc/saibridge.h: 577

SAI_BRIDGE_ATTR_UNKNOWN_UNICAST_FLOOD_CONTROL_TYPE = (SAI_BRIDGE_ATTR_LEARN_DISABLE + 1)# /home/bluecmd/Downloads/SAI/inc/saibridge.h: 577

SAI_BRIDGE_ATTR_UNKNOWN_UNICAST_FLOOD_GROUP = (SAI_BRIDGE_ATTR_UNKNOWN_UNICAST_FLOOD_CONTROL_TYPE + 1)# /home/bluecmd/Downloads/SAI/inc/saibridge.h: 577

SAI_BRIDGE_ATTR_UNKNOWN_MULTICAST_FLOOD_CONTROL_TYPE = (SAI_BRIDGE_ATTR_UNKNOWN_UNICAST_FLOOD_GROUP + 1)# /home/bluecmd/Downloads/SAI/inc/saibridge.h: 577

SAI_BRIDGE_ATTR_UNKNOWN_MULTICAST_FLOOD_GROUP = (SAI_BRIDGE_ATTR_UNKNOWN_MULTICAST_FLOOD_CONTROL_TYPE + 1)# /home/bluecmd/Downloads/SAI/inc/saibridge.h: 577

SAI_BRIDGE_ATTR_BROADCAST_FLOOD_CONTROL_TYPE = (SAI_BRIDGE_ATTR_UNKNOWN_MULTICAST_FLOOD_GROUP + 1)# /home/bluecmd/Downloads/SAI/inc/saibridge.h: 577

SAI_BRIDGE_ATTR_BROADCAST_FLOOD_GROUP = (SAI_BRIDGE_ATTR_BROADCAST_FLOOD_CONTROL_TYPE + 1)# /home/bluecmd/Downloads/SAI/inc/saibridge.h: 577

SAI_BRIDGE_ATTR_END = (SAI_BRIDGE_ATTR_BROADCAST_FLOOD_GROUP + 1)# /home/bluecmd/Downloads/SAI/inc/saibridge.h: 577

SAI_BRIDGE_ATTR_CUSTOM_RANGE_START = 0x10000000# /home/bluecmd/Downloads/SAI/inc/saibridge.h: 577

SAI_BRIDGE_ATTR_CUSTOM_RANGE_END = (SAI_BRIDGE_ATTR_CUSTOM_RANGE_START + 1)# /home/bluecmd/Downloads/SAI/inc/saibridge.h: 577

sai_bridge_attr_t = enum__sai_bridge_attr_t# /home/bluecmd/Downloads/SAI/inc/saibridge.h: 577

enum__sai_bridge_stat_t = c_int# /home/bluecmd/Downloads/SAI/inc/saibridge.h: 596

SAI_BRIDGE_STAT_IN_OCTETS = 0# /home/bluecmd/Downloads/SAI/inc/saibridge.h: 596

SAI_BRIDGE_STAT_IN_PACKETS = (SAI_BRIDGE_STAT_IN_OCTETS + 1)# /home/bluecmd/Downloads/SAI/inc/saibridge.h: 596

SAI_BRIDGE_STAT_OUT_OCTETS = (SAI_BRIDGE_STAT_IN_PACKETS + 1)# /home/bluecmd/Downloads/SAI/inc/saibridge.h: 596

SAI_BRIDGE_STAT_OUT_PACKETS = (SAI_BRIDGE_STAT_OUT_OCTETS + 1)# /home/bluecmd/Downloads/SAI/inc/saibridge.h: 596

sai_bridge_stat_t = enum__sai_bridge_stat_t# /home/bluecmd/Downloads/SAI/inc/saibridge.h: 596

sai_create_bridge_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saibridge.h: 608

sai_remove_bridge_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t)# /home/bluecmd/Downloads/SAI/inc/saibridge.h: 621

sai_set_bridge_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saibridge.h: 632

sai_get_bridge_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saibridge.h: 645

sai_get_bridge_stats_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, uint32_t, POINTER(sai_stat_id_t), POINTER(uint64_t))# /home/bluecmd/Downloads/SAI/inc/saibridge.h: 660

sai_get_bridge_stats_ext_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, uint32_t, POINTER(sai_stat_id_t), sai_stats_mode_t, POINTER(uint64_t))# /home/bluecmd/Downloads/SAI/inc/saibridge.h: 677

sai_clear_bridge_stats_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, uint32_t, POINTER(sai_stat_id_t))# /home/bluecmd/Downloads/SAI/inc/saibridge.h: 693

# /home/bluecmd/Downloads/SAI/inc/saibridge.h: 717
class struct__sai_bridge_api_t(Structure):
    pass

struct__sai_bridge_api_t.__slots__ = [
    'create_bridge',
    'remove_bridge',
    'set_bridge_attribute',
    'get_bridge_attribute',
    'get_bridge_stats',
    'get_bridge_stats_ext',
    'clear_bridge_stats',
    'create_bridge_port',
    'remove_bridge_port',
    'set_bridge_port_attribute',
    'get_bridge_port_attribute',
    'get_bridge_port_stats',
    'get_bridge_port_stats_ext',
    'clear_bridge_port_stats',
]
struct__sai_bridge_api_t._fields_ = [
    ('create_bridge', sai_create_bridge_fn),
    ('remove_bridge', sai_remove_bridge_fn),
    ('set_bridge_attribute', sai_set_bridge_attribute_fn),
    ('get_bridge_attribute', sai_get_bridge_attribute_fn),
    ('get_bridge_stats', sai_get_bridge_stats_fn),
    ('get_bridge_stats_ext', sai_get_bridge_stats_ext_fn),
    ('clear_bridge_stats', sai_clear_bridge_stats_fn),
    ('create_bridge_port', sai_create_bridge_port_fn),
    ('remove_bridge_port', sai_remove_bridge_port_fn),
    ('set_bridge_port_attribute', sai_set_bridge_port_attribute_fn),
    ('get_bridge_port_attribute', sai_get_bridge_port_attribute_fn),
    ('get_bridge_port_stats', sai_get_bridge_port_stats_fn),
    ('get_bridge_port_stats_ext', sai_get_bridge_port_stats_ext_fn),
    ('clear_bridge_port_stats', sai_clear_bridge_port_stats_fn),
]

sai_bridge_api_t = struct__sai_bridge_api_t# /home/bluecmd/Downloads/SAI/inc/saibridge.h: 717

enum__sai_ingress_priority_group_attr_t = c_int# /home/bluecmd/Downloads/SAI/inc/saibuffer.h: 97

SAI_INGRESS_PRIORITY_GROUP_ATTR_START = 0# /home/bluecmd/Downloads/SAI/inc/saibuffer.h: 97

SAI_INGRESS_PRIORITY_GROUP_ATTR_BUFFER_PROFILE = SAI_INGRESS_PRIORITY_GROUP_ATTR_START# /home/bluecmd/Downloads/SAI/inc/saibuffer.h: 97

SAI_INGRESS_PRIORITY_GROUP_ATTR_PORT = (SAI_INGRESS_PRIORITY_GROUP_ATTR_BUFFER_PROFILE + 1)# /home/bluecmd/Downloads/SAI/inc/saibuffer.h: 97

SAI_INGRESS_PRIORITY_GROUP_ATTR_TAM = (SAI_INGRESS_PRIORITY_GROUP_ATTR_PORT + 1)# /home/bluecmd/Downloads/SAI/inc/saibuffer.h: 97

SAI_INGRESS_PRIORITY_GROUP_ATTR_INDEX = (SAI_INGRESS_PRIORITY_GROUP_ATTR_TAM + 1)# /home/bluecmd/Downloads/SAI/inc/saibuffer.h: 97

SAI_INGRESS_PRIORITY_GROUP_ATTR_END = (SAI_INGRESS_PRIORITY_GROUP_ATTR_INDEX + 1)# /home/bluecmd/Downloads/SAI/inc/saibuffer.h: 97

SAI_INGRESS_PRIORITY_GROUP_ATTR_CUSTOM_RANGE_START = 0x10000000# /home/bluecmd/Downloads/SAI/inc/saibuffer.h: 97

SAI_INGRESS_PRIORITY_GROUP_ATTR_CUSTOM_RANGE_END = (SAI_INGRESS_PRIORITY_GROUP_ATTR_CUSTOM_RANGE_START + 1)# /home/bluecmd/Downloads/SAI/inc/saibuffer.h: 97

sai_ingress_priority_group_attr_t = enum__sai_ingress_priority_group_attr_t# /home/bluecmd/Downloads/SAI/inc/saibuffer.h: 97

enum__sai_ingress_priority_group_stat_t = c_int# /home/bluecmd/Downloads/SAI/inc/saibuffer.h: 134

SAI_INGRESS_PRIORITY_GROUP_STAT_PACKETS = 0x00000000# /home/bluecmd/Downloads/SAI/inc/saibuffer.h: 134

SAI_INGRESS_PRIORITY_GROUP_STAT_BYTES = 0x00000001# /home/bluecmd/Downloads/SAI/inc/saibuffer.h: 134

SAI_INGRESS_PRIORITY_GROUP_STAT_CURR_OCCUPANCY_BYTES = 0x00000002# /home/bluecmd/Downloads/SAI/inc/saibuffer.h: 134

SAI_INGRESS_PRIORITY_GROUP_STAT_WATERMARK_BYTES = 0x00000003# /home/bluecmd/Downloads/SAI/inc/saibuffer.h: 134

SAI_INGRESS_PRIORITY_GROUP_STAT_SHARED_CURR_OCCUPANCY_BYTES = 0x00000004# /home/bluecmd/Downloads/SAI/inc/saibuffer.h: 134

SAI_INGRESS_PRIORITY_GROUP_STAT_SHARED_WATERMARK_BYTES = 0x00000005# /home/bluecmd/Downloads/SAI/inc/saibuffer.h: 134

SAI_INGRESS_PRIORITY_GROUP_STAT_XOFF_ROOM_CURR_OCCUPANCY_BYTES = 0x00000006# /home/bluecmd/Downloads/SAI/inc/saibuffer.h: 134

SAI_INGRESS_PRIORITY_GROUP_STAT_XOFF_ROOM_WATERMARK_BYTES = 0x00000007# /home/bluecmd/Downloads/SAI/inc/saibuffer.h: 134

SAI_INGRESS_PRIORITY_GROUP_STAT_DROPPED_PACKETS = 0x00000008# /home/bluecmd/Downloads/SAI/inc/saibuffer.h: 134

SAI_INGRESS_PRIORITY_GROUP_STAT_CUSTOM_RANGE_BASE = 0x10000000# /home/bluecmd/Downloads/SAI/inc/saibuffer.h: 134

sai_ingress_priority_group_stat_t = enum__sai_ingress_priority_group_stat_t# /home/bluecmd/Downloads/SAI/inc/saibuffer.h: 134

sai_create_ingress_priority_group_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saibuffer.h: 146

sai_remove_ingress_priority_group_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t)# /home/bluecmd/Downloads/SAI/inc/saibuffer.h: 159

sai_set_ingress_priority_group_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saibuffer.h: 170

sai_get_ingress_priority_group_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saibuffer.h: 183

sai_get_ingress_priority_group_stats_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, uint32_t, POINTER(sai_stat_id_t), POINTER(uint64_t))# /home/bluecmd/Downloads/SAI/inc/saibuffer.h: 198

sai_get_ingress_priority_group_stats_ext_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, uint32_t, POINTER(sai_stat_id_t), sai_stats_mode_t, POINTER(uint64_t))# /home/bluecmd/Downloads/SAI/inc/saibuffer.h: 215

sai_clear_ingress_priority_group_stats_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, uint32_t, POINTER(sai_stat_id_t))# /home/bluecmd/Downloads/SAI/inc/saibuffer.h: 231

enum__sai_buffer_pool_type_t = c_int# /home/bluecmd/Downloads/SAI/inc/saibuffer.h: 250

SAI_BUFFER_POOL_TYPE_INGRESS = 0# /home/bluecmd/Downloads/SAI/inc/saibuffer.h: 250

SAI_BUFFER_POOL_TYPE_EGRESS = (SAI_BUFFER_POOL_TYPE_INGRESS + 1)# /home/bluecmd/Downloads/SAI/inc/saibuffer.h: 250

SAI_BUFFER_POOL_TYPE_BOTH = (SAI_BUFFER_POOL_TYPE_EGRESS + 1)# /home/bluecmd/Downloads/SAI/inc/saibuffer.h: 250

sai_buffer_pool_type_t = enum__sai_buffer_pool_type_t# /home/bluecmd/Downloads/SAI/inc/saibuffer.h: 250

enum__sai_buffer_pool_threshold_mode_t = c_int# /home/bluecmd/Downloads/SAI/inc/saibuffer.h: 263

SAI_BUFFER_POOL_THRESHOLD_MODE_STATIC = 0# /home/bluecmd/Downloads/SAI/inc/saibuffer.h: 263

SAI_BUFFER_POOL_THRESHOLD_MODE_DYNAMIC = (SAI_BUFFER_POOL_THRESHOLD_MODE_STATIC + 1)# /home/bluecmd/Downloads/SAI/inc/saibuffer.h: 263

sai_buffer_pool_threshold_mode_t = enum__sai_buffer_pool_threshold_mode_t# /home/bluecmd/Downloads/SAI/inc/saibuffer.h: 263

enum__sai_buffer_pool_attr_t = c_int# /home/bluecmd/Downloads/SAI/inc/saibuffer.h: 361

SAI_BUFFER_POOL_ATTR_START = 0# /home/bluecmd/Downloads/SAI/inc/saibuffer.h: 361

SAI_BUFFER_POOL_ATTR_SHARED_SIZE = SAI_BUFFER_POOL_ATTR_START# /home/bluecmd/Downloads/SAI/inc/saibuffer.h: 361

SAI_BUFFER_POOL_ATTR_TYPE = (SAI_BUFFER_POOL_ATTR_SHARED_SIZE + 1)# /home/bluecmd/Downloads/SAI/inc/saibuffer.h: 361

SAI_BUFFER_POOL_ATTR_SIZE = (SAI_BUFFER_POOL_ATTR_TYPE + 1)# /home/bluecmd/Downloads/SAI/inc/saibuffer.h: 361

SAI_BUFFER_POOL_ATTR_THRESHOLD_MODE = (SAI_BUFFER_POOL_ATTR_SIZE + 1)# /home/bluecmd/Downloads/SAI/inc/saibuffer.h: 361

SAI_BUFFER_POOL_ATTR_TAM = (SAI_BUFFER_POOL_ATTR_THRESHOLD_MODE + 1)# /home/bluecmd/Downloads/SAI/inc/saibuffer.h: 361

SAI_BUFFER_POOL_ATTR_XOFF_SIZE = (SAI_BUFFER_POOL_ATTR_TAM + 1)# /home/bluecmd/Downloads/SAI/inc/saibuffer.h: 361

SAI_BUFFER_POOL_ATTR_WRED_PROFILE_ID = (SAI_BUFFER_POOL_ATTR_XOFF_SIZE + 1)# /home/bluecmd/Downloads/SAI/inc/saibuffer.h: 361

SAI_BUFFER_POOL_ATTR_END = (SAI_BUFFER_POOL_ATTR_WRED_PROFILE_ID + 1)# /home/bluecmd/Downloads/SAI/inc/saibuffer.h: 361

SAI_BUFFER_POOL_ATTR_CUSTOM_RANGE_START = 0x10000000# /home/bluecmd/Downloads/SAI/inc/saibuffer.h: 361

SAI_BUFFER_POOL_ATTR_CUSTOM_RANGE_END = (SAI_BUFFER_POOL_ATTR_CUSTOM_RANGE_START + 1)# /home/bluecmd/Downloads/SAI/inc/saibuffer.h: 361

sai_buffer_pool_attr_t = enum__sai_buffer_pool_attr_t# /home/bluecmd/Downloads/SAI/inc/saibuffer.h: 361

enum__sai_buffer_pool_stat_t = c_int# /home/bluecmd/Downloads/SAI/inc/saibuffer.h: 434

SAI_BUFFER_POOL_STAT_CURR_OCCUPANCY_BYTES = 0x00000000# /home/bluecmd/Downloads/SAI/inc/saibuffer.h: 434

SAI_BUFFER_POOL_STAT_WATERMARK_BYTES = 0x00000001# /home/bluecmd/Downloads/SAI/inc/saibuffer.h: 434

SAI_BUFFER_POOL_STAT_DROPPED_PACKETS = 0x00000002# /home/bluecmd/Downloads/SAI/inc/saibuffer.h: 434

SAI_BUFFER_POOL_STAT_GREEN_WRED_DROPPED_PACKETS = 0x00000003# /home/bluecmd/Downloads/SAI/inc/saibuffer.h: 434

SAI_BUFFER_POOL_STAT_GREEN_WRED_DROPPED_BYTES = 0x00000004# /home/bluecmd/Downloads/SAI/inc/saibuffer.h: 434

SAI_BUFFER_POOL_STAT_YELLOW_WRED_DROPPED_PACKETS = 0x00000005# /home/bluecmd/Downloads/SAI/inc/saibuffer.h: 434

SAI_BUFFER_POOL_STAT_YELLOW_WRED_DROPPED_BYTES = 0x00000006# /home/bluecmd/Downloads/SAI/inc/saibuffer.h: 434

SAI_BUFFER_POOL_STAT_RED_WRED_DROPPED_PACKETS = 0x00000007# /home/bluecmd/Downloads/SAI/inc/saibuffer.h: 434

SAI_BUFFER_POOL_STAT_RED_WRED_DROPPED_BYTES = 0x00000008# /home/bluecmd/Downloads/SAI/inc/saibuffer.h: 434

SAI_BUFFER_POOL_STAT_WRED_DROPPED_PACKETS = 0x00000009# /home/bluecmd/Downloads/SAI/inc/saibuffer.h: 434

SAI_BUFFER_POOL_STAT_WRED_DROPPED_BYTES = 0x0000000a# /home/bluecmd/Downloads/SAI/inc/saibuffer.h: 434

SAI_BUFFER_POOL_STAT_GREEN_WRED_ECN_MARKED_PACKETS = 0x0000000b# /home/bluecmd/Downloads/SAI/inc/saibuffer.h: 434

SAI_BUFFER_POOL_STAT_GREEN_WRED_ECN_MARKED_BYTES = 0x0000000c# /home/bluecmd/Downloads/SAI/inc/saibuffer.h: 434

SAI_BUFFER_POOL_STAT_YELLOW_WRED_ECN_MARKED_PACKETS = 0x0000000d# /home/bluecmd/Downloads/SAI/inc/saibuffer.h: 434

SAI_BUFFER_POOL_STAT_YELLOW_WRED_ECN_MARKED_BYTES = 0x0000000e# /home/bluecmd/Downloads/SAI/inc/saibuffer.h: 434

SAI_BUFFER_POOL_STAT_RED_WRED_ECN_MARKED_PACKETS = 0x0000000f# /home/bluecmd/Downloads/SAI/inc/saibuffer.h: 434

SAI_BUFFER_POOL_STAT_RED_WRED_ECN_MARKED_BYTES = 0x00000010# /home/bluecmd/Downloads/SAI/inc/saibuffer.h: 434

SAI_BUFFER_POOL_STAT_WRED_ECN_MARKED_PACKETS = 0x00000011# /home/bluecmd/Downloads/SAI/inc/saibuffer.h: 434

SAI_BUFFER_POOL_STAT_WRED_ECN_MARKED_BYTES = 0x00000012# /home/bluecmd/Downloads/SAI/inc/saibuffer.h: 434

SAI_BUFFER_POOL_STAT_XOFF_ROOM_CURR_OCCUPANCY_BYTES = 0x00000013# /home/bluecmd/Downloads/SAI/inc/saibuffer.h: 434

SAI_BUFFER_POOL_STAT_XOFF_ROOM_WATERMARK_BYTES = 0x00000014# /home/bluecmd/Downloads/SAI/inc/saibuffer.h: 434

SAI_BUFFER_POOL_STAT_CUSTOM_RANGE_BASE = 0x10000000# /home/bluecmd/Downloads/SAI/inc/saibuffer.h: 434

sai_buffer_pool_stat_t = enum__sai_buffer_pool_stat_t# /home/bluecmd/Downloads/SAI/inc/saibuffer.h: 434

sai_create_buffer_pool_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saibuffer.h: 446

sai_remove_buffer_pool_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t)# /home/bluecmd/Downloads/SAI/inc/saibuffer.h: 459

sai_set_buffer_pool_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saibuffer.h: 470

sai_get_buffer_pool_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saibuffer.h: 483

sai_get_buffer_pool_stats_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, uint32_t, POINTER(sai_stat_id_t), POINTER(uint64_t))# /home/bluecmd/Downloads/SAI/inc/saibuffer.h: 498

sai_get_buffer_pool_stats_ext_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, uint32_t, POINTER(sai_stat_id_t), sai_stats_mode_t, POINTER(uint64_t))# /home/bluecmd/Downloads/SAI/inc/saibuffer.h: 515

sai_clear_buffer_pool_stats_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, uint32_t, POINTER(sai_stat_id_t))# /home/bluecmd/Downloads/SAI/inc/saibuffer.h: 531

enum__sai_buffer_profile_threshold_mode_t = c_int# /home/bluecmd/Downloads/SAI/inc/saibuffer.h: 547

SAI_BUFFER_PROFILE_THRESHOLD_MODE_STATIC = 0# /home/bluecmd/Downloads/SAI/inc/saibuffer.h: 547

SAI_BUFFER_PROFILE_THRESHOLD_MODE_DYNAMIC = (SAI_BUFFER_PROFILE_THRESHOLD_MODE_STATIC + 1)# /home/bluecmd/Downloads/SAI/inc/saibuffer.h: 547

sai_buffer_profile_threshold_mode_t = enum__sai_buffer_profile_threshold_mode_t# /home/bluecmd/Downloads/SAI/inc/saibuffer.h: 547

enum__sai_buffer_profile_attr_t = c_int# /home/bluecmd/Downloads/SAI/inc/saibuffer.h: 681

SAI_BUFFER_PROFILE_ATTR_START = 0# /home/bluecmd/Downloads/SAI/inc/saibuffer.h: 681

SAI_BUFFER_PROFILE_ATTR_POOL_ID = SAI_BUFFER_PROFILE_ATTR_START# /home/bluecmd/Downloads/SAI/inc/saibuffer.h: 681

SAI_BUFFER_PROFILE_ATTR_RESERVED_BUFFER_SIZE = (SAI_BUFFER_PROFILE_ATTR_POOL_ID + 1)# /home/bluecmd/Downloads/SAI/inc/saibuffer.h: 681

SAI_BUFFER_PROFILE_ATTR_BUFFER_SIZE = SAI_BUFFER_PROFILE_ATTR_RESERVED_BUFFER_SIZE# /home/bluecmd/Downloads/SAI/inc/saibuffer.h: 681

SAI_BUFFER_PROFILE_ATTR_THRESHOLD_MODE = (SAI_BUFFER_PROFILE_ATTR_BUFFER_SIZE + 1)# /home/bluecmd/Downloads/SAI/inc/saibuffer.h: 681

SAI_BUFFER_PROFILE_ATTR_SHARED_DYNAMIC_TH = (SAI_BUFFER_PROFILE_ATTR_THRESHOLD_MODE + 1)# /home/bluecmd/Downloads/SAI/inc/saibuffer.h: 681

SAI_BUFFER_PROFILE_ATTR_SHARED_STATIC_TH = (SAI_BUFFER_PROFILE_ATTR_SHARED_DYNAMIC_TH + 1)# /home/bluecmd/Downloads/SAI/inc/saibuffer.h: 681

SAI_BUFFER_PROFILE_ATTR_XOFF_TH = (SAI_BUFFER_PROFILE_ATTR_SHARED_STATIC_TH + 1)# /home/bluecmd/Downloads/SAI/inc/saibuffer.h: 681

SAI_BUFFER_PROFILE_ATTR_XON_TH = (SAI_BUFFER_PROFILE_ATTR_XOFF_TH + 1)# /home/bluecmd/Downloads/SAI/inc/saibuffer.h: 681

SAI_BUFFER_PROFILE_ATTR_XON_OFFSET_TH = (SAI_BUFFER_PROFILE_ATTR_XON_TH + 1)# /home/bluecmd/Downloads/SAI/inc/saibuffer.h: 681

SAI_BUFFER_PROFILE_ATTR_END = (SAI_BUFFER_PROFILE_ATTR_XON_OFFSET_TH + 1)# /home/bluecmd/Downloads/SAI/inc/saibuffer.h: 681

SAI_BUFFER_PROFILE_ATTR_CUSTOM_RANGE_START = 0x10000000# /home/bluecmd/Downloads/SAI/inc/saibuffer.h: 681

SAI_BUFFER_PROFILE_ATTR_CUSTOM_RANGE_END = (SAI_BUFFER_PROFILE_ATTR_CUSTOM_RANGE_START + 1)# /home/bluecmd/Downloads/SAI/inc/saibuffer.h: 681

sai_buffer_profile_attr_t = enum__sai_buffer_profile_attr_t# /home/bluecmd/Downloads/SAI/inc/saibuffer.h: 681

sai_create_buffer_profile_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saibuffer.h: 693

sai_remove_buffer_profile_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t)# /home/bluecmd/Downloads/SAI/inc/saibuffer.h: 706

sai_set_buffer_profile_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saibuffer.h: 717

sai_get_buffer_profile_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saibuffer.h: 730

# /home/bluecmd/Downloads/SAI/inc/saibuffer.h: 758
class struct__sai_buffer_api_t(Structure):
    pass

struct__sai_buffer_api_t.__slots__ = [
    'create_buffer_pool',
    'remove_buffer_pool',
    'set_buffer_pool_attribute',
    'get_buffer_pool_attribute',
    'get_buffer_pool_stats',
    'get_buffer_pool_stats_ext',
    'clear_buffer_pool_stats',
    'create_ingress_priority_group',
    'remove_ingress_priority_group',
    'set_ingress_priority_group_attribute',
    'get_ingress_priority_group_attribute',
    'get_ingress_priority_group_stats',
    'get_ingress_priority_group_stats_ext',
    'clear_ingress_priority_group_stats',
    'create_buffer_profile',
    'remove_buffer_profile',
    'set_buffer_profile_attribute',
    'get_buffer_profile_attribute',
]
struct__sai_buffer_api_t._fields_ = [
    ('create_buffer_pool', sai_create_buffer_pool_fn),
    ('remove_buffer_pool', sai_remove_buffer_pool_fn),
    ('set_buffer_pool_attribute', sai_set_buffer_pool_attribute_fn),
    ('get_buffer_pool_attribute', sai_get_buffer_pool_attribute_fn),
    ('get_buffer_pool_stats', sai_get_buffer_pool_stats_fn),
    ('get_buffer_pool_stats_ext', sai_get_buffer_pool_stats_ext_fn),
    ('clear_buffer_pool_stats', sai_clear_buffer_pool_stats_fn),
    ('create_ingress_priority_group', sai_create_ingress_priority_group_fn),
    ('remove_ingress_priority_group', sai_remove_ingress_priority_group_fn),
    ('set_ingress_priority_group_attribute', sai_set_ingress_priority_group_attribute_fn),
    ('get_ingress_priority_group_attribute', sai_get_ingress_priority_group_attribute_fn),
    ('get_ingress_priority_group_stats', sai_get_ingress_priority_group_stats_fn),
    ('get_ingress_priority_group_stats_ext', sai_get_ingress_priority_group_stats_ext_fn),
    ('clear_ingress_priority_group_stats', sai_clear_ingress_priority_group_stats_fn),
    ('create_buffer_profile', sai_create_buffer_profile_fn),
    ('remove_buffer_profile', sai_remove_buffer_profile_fn),
    ('set_buffer_profile_attribute', sai_set_buffer_profile_attribute_fn),
    ('get_buffer_profile_attribute', sai_get_buffer_profile_attribute_fn),
]

sai_buffer_api_t = struct__sai_buffer_api_t# /home/bluecmd/Downloads/SAI/inc/saibuffer.h: 758

enum__sai_counter_type_t = c_int# /home/bluecmd/Downloads/SAI/inc/saicounter.h: 48

SAI_COUNTER_TYPE_REGULAR = 0# /home/bluecmd/Downloads/SAI/inc/saicounter.h: 48

sai_counter_type_t = enum__sai_counter_type_t# /home/bluecmd/Downloads/SAI/inc/saicounter.h: 48

enum__sai_counter_attr_t = c_int# /home/bluecmd/Downloads/SAI/inc/saicounter.h: 92

SAI_COUNTER_ATTR_START = 0# /home/bluecmd/Downloads/SAI/inc/saicounter.h: 92

SAI_COUNTER_ATTR_TYPE = SAI_COUNTER_ATTR_START# /home/bluecmd/Downloads/SAI/inc/saicounter.h: 92

SAI_COUNTER_ATTR_LABEL = (SAI_COUNTER_ATTR_TYPE + 1)# /home/bluecmd/Downloads/SAI/inc/saicounter.h: 92

SAI_COUNTER_ATTR_END = (SAI_COUNTER_ATTR_LABEL + 1)# /home/bluecmd/Downloads/SAI/inc/saicounter.h: 92

SAI_COUNTER_ATTR_CUSTOM_RANGE_START = 0x10000000# /home/bluecmd/Downloads/SAI/inc/saicounter.h: 92

SAI_COUNTER_ATTR_CUSTOM_RANGE_END = (SAI_COUNTER_ATTR_CUSTOM_RANGE_START + 1)# /home/bluecmd/Downloads/SAI/inc/saicounter.h: 92

sai_counter_attr_t = enum__sai_counter_attr_t# /home/bluecmd/Downloads/SAI/inc/saicounter.h: 92

sai_create_counter_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saicounter.h: 104

sai_remove_counter_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t)# /home/bluecmd/Downloads/SAI/inc/saicounter.h: 117

sai_set_counter_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saicounter.h: 128

sai_get_counter_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saicounter.h: 141

enum__sai_counter_stat_t = c_int# /home/bluecmd/Downloads/SAI/inc/saicounter.h: 160

SAI_COUNTER_STAT_PACKETS = 0x00000000# /home/bluecmd/Downloads/SAI/inc/saicounter.h: 160

SAI_COUNTER_STAT_BYTES = 0x00000001# /home/bluecmd/Downloads/SAI/inc/saicounter.h: 160

SAI_COUNTER_STAT_CUSTOM_RANGE_BASE = 0x10000000# /home/bluecmd/Downloads/SAI/inc/saicounter.h: 160

sai_counter_stat_t = enum__sai_counter_stat_t# /home/bluecmd/Downloads/SAI/inc/saicounter.h: 160

sai_get_counter_stats_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, uint32_t, POINTER(sai_stat_id_t), POINTER(uint64_t))# /home/bluecmd/Downloads/SAI/inc/saicounter.h: 172

sai_get_counter_stats_ext_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, uint32_t, POINTER(sai_stat_id_t), sai_stats_mode_t, POINTER(uint64_t))# /home/bluecmd/Downloads/SAI/inc/saicounter.h: 189

sai_clear_counter_stats_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, uint32_t, POINTER(sai_stat_id_t))# /home/bluecmd/Downloads/SAI/inc/saicounter.h: 205

# /home/bluecmd/Downloads/SAI/inc/saicounter.h: 223
class struct__sai_counter_api_t(Structure):
    pass

struct__sai_counter_api_t.__slots__ = [
    'create_counter',
    'remove_counter',
    'set_counter_attribute',
    'get_counter_attribute',
    'get_counter_stats',
    'get_counter_stats_ext',
    'clear_counter_stats',
]
struct__sai_counter_api_t._fields_ = [
    ('create_counter', sai_create_counter_fn),
    ('remove_counter', sai_remove_counter_fn),
    ('set_counter_attribute', sai_set_counter_attribute_fn),
    ('get_counter_attribute', sai_get_counter_attribute_fn),
    ('get_counter_stats', sai_get_counter_stats_fn),
    ('get_counter_stats_ext', sai_get_counter_stats_ext_fn),
    ('clear_counter_stats', sai_clear_counter_stats_fn),
]

sai_counter_api_t = struct__sai_counter_api_t# /home/bluecmd/Downloads/SAI/inc/saicounter.h: 223

enum__sai_debug_counter_type_t = c_int# /home/bluecmd/Downloads/SAI/inc/saidebugcounter.h: 67

SAI_DEBUG_COUNTER_TYPE_PORT_IN_DROP_REASONS = 0# /home/bluecmd/Downloads/SAI/inc/saidebugcounter.h: 67

SAI_DEBUG_COUNTER_TYPE_PORT_OUT_DROP_REASONS = (SAI_DEBUG_COUNTER_TYPE_PORT_IN_DROP_REASONS + 1)# /home/bluecmd/Downloads/SAI/inc/saidebugcounter.h: 67

SAI_DEBUG_COUNTER_TYPE_SWITCH_IN_DROP_REASONS = (SAI_DEBUG_COUNTER_TYPE_PORT_OUT_DROP_REASONS + 1)# /home/bluecmd/Downloads/SAI/inc/saidebugcounter.h: 67

SAI_DEBUG_COUNTER_TYPE_SWITCH_OUT_DROP_REASONS = (SAI_DEBUG_COUNTER_TYPE_SWITCH_IN_DROP_REASONS + 1)# /home/bluecmd/Downloads/SAI/inc/saidebugcounter.h: 67

sai_debug_counter_type_t = enum__sai_debug_counter_type_t# /home/bluecmd/Downloads/SAI/inc/saidebugcounter.h: 67

enum__sai_debug_counter_bind_method_t = c_int# /home/bluecmd/Downloads/SAI/inc/saidebugcounter.h: 77

SAI_DEBUG_COUNTER_BIND_METHOD_AUTOMATIC = 0# /home/bluecmd/Downloads/SAI/inc/saidebugcounter.h: 77

sai_debug_counter_bind_method_t = enum__sai_debug_counter_bind_method_t# /home/bluecmd/Downloads/SAI/inc/saidebugcounter.h: 77

enum__sai_in_drop_reason_t = c_int# /home/bluecmd/Downloads/SAI/inc/saidebugcounter.h: 334

SAI_IN_DROP_REASON_START = 0# /home/bluecmd/Downloads/SAI/inc/saidebugcounter.h: 334

SAI_IN_DROP_REASON_L2_ANY = SAI_IN_DROP_REASON_START# /home/bluecmd/Downloads/SAI/inc/saidebugcounter.h: 334

SAI_IN_DROP_REASON_SMAC_MULTICAST = (SAI_IN_DROP_REASON_L2_ANY + 1)# /home/bluecmd/Downloads/SAI/inc/saidebugcounter.h: 334

SAI_IN_DROP_REASON_SMAC_EQUALS_DMAC = (SAI_IN_DROP_REASON_SMAC_MULTICAST + 1)# /home/bluecmd/Downloads/SAI/inc/saidebugcounter.h: 334

SAI_IN_DROP_REASON_DMAC_RESERVED = (SAI_IN_DROP_REASON_SMAC_EQUALS_DMAC + 1)# /home/bluecmd/Downloads/SAI/inc/saidebugcounter.h: 334

SAI_IN_DROP_REASON_VLAN_TAG_NOT_ALLOWED = (SAI_IN_DROP_REASON_DMAC_RESERVED + 1)# /home/bluecmd/Downloads/SAI/inc/saidebugcounter.h: 334

SAI_IN_DROP_REASON_INGRESS_VLAN_FILTER = (SAI_IN_DROP_REASON_VLAN_TAG_NOT_ALLOWED + 1)# /home/bluecmd/Downloads/SAI/inc/saidebugcounter.h: 334

SAI_IN_DROP_REASON_INGRESS_STP_FILTER = (SAI_IN_DROP_REASON_INGRESS_VLAN_FILTER + 1)# /home/bluecmd/Downloads/SAI/inc/saidebugcounter.h: 334

SAI_IN_DROP_REASON_FDB_UC_DISCARD = (SAI_IN_DROP_REASON_INGRESS_STP_FILTER + 1)# /home/bluecmd/Downloads/SAI/inc/saidebugcounter.h: 334

SAI_IN_DROP_REASON_FDB_MC_DISCARD = (SAI_IN_DROP_REASON_FDB_UC_DISCARD + 1)# /home/bluecmd/Downloads/SAI/inc/saidebugcounter.h: 334

SAI_IN_DROP_REASON_L2_LOOPBACK_FILTER = (SAI_IN_DROP_REASON_FDB_MC_DISCARD + 1)# /home/bluecmd/Downloads/SAI/inc/saidebugcounter.h: 334

SAI_IN_DROP_REASON_EXCEEDS_L2_MTU = (SAI_IN_DROP_REASON_L2_LOOPBACK_FILTER + 1)# /home/bluecmd/Downloads/SAI/inc/saidebugcounter.h: 334

SAI_IN_DROP_REASON_L3_ANY = (SAI_IN_DROP_REASON_EXCEEDS_L2_MTU + 1)# /home/bluecmd/Downloads/SAI/inc/saidebugcounter.h: 334

SAI_IN_DROP_REASON_EXCEEDS_L3_MTU = (SAI_IN_DROP_REASON_L3_ANY + 1)# /home/bluecmd/Downloads/SAI/inc/saidebugcounter.h: 334

SAI_IN_DROP_REASON_TTL = (SAI_IN_DROP_REASON_EXCEEDS_L3_MTU + 1)# /home/bluecmd/Downloads/SAI/inc/saidebugcounter.h: 334

SAI_IN_DROP_REASON_L3_LOOPBACK_FILTER = (SAI_IN_DROP_REASON_TTL + 1)# /home/bluecmd/Downloads/SAI/inc/saidebugcounter.h: 334

SAI_IN_DROP_REASON_NON_ROUTABLE = (SAI_IN_DROP_REASON_L3_LOOPBACK_FILTER + 1)# /home/bluecmd/Downloads/SAI/inc/saidebugcounter.h: 334

SAI_IN_DROP_REASON_NO_L3_HEADER = (SAI_IN_DROP_REASON_NON_ROUTABLE + 1)# /home/bluecmd/Downloads/SAI/inc/saidebugcounter.h: 334

SAI_IN_DROP_REASON_IP_HEADER_ERROR = (SAI_IN_DROP_REASON_NO_L3_HEADER + 1)# /home/bluecmd/Downloads/SAI/inc/saidebugcounter.h: 334

SAI_IN_DROP_REASON_UC_DIP_MC_DMAC = (SAI_IN_DROP_REASON_IP_HEADER_ERROR + 1)# /home/bluecmd/Downloads/SAI/inc/saidebugcounter.h: 334

SAI_IN_DROP_REASON_DIP_LOOPBACK = (SAI_IN_DROP_REASON_UC_DIP_MC_DMAC + 1)# /home/bluecmd/Downloads/SAI/inc/saidebugcounter.h: 334

SAI_IN_DROP_REASON_SIP_LOOPBACK = (SAI_IN_DROP_REASON_DIP_LOOPBACK + 1)# /home/bluecmd/Downloads/SAI/inc/saidebugcounter.h: 334

SAI_IN_DROP_REASON_SIP_MC = (SAI_IN_DROP_REASON_SIP_LOOPBACK + 1)# /home/bluecmd/Downloads/SAI/inc/saidebugcounter.h: 334

SAI_IN_DROP_REASON_SIP_CLASS_E = (SAI_IN_DROP_REASON_SIP_MC + 1)# /home/bluecmd/Downloads/SAI/inc/saidebugcounter.h: 334

SAI_IN_DROP_REASON_SIP_UNSPECIFIED = (SAI_IN_DROP_REASON_SIP_CLASS_E + 1)# /home/bluecmd/Downloads/SAI/inc/saidebugcounter.h: 334

SAI_IN_DROP_REASON_MC_DMAC_MISMATCH = (SAI_IN_DROP_REASON_SIP_UNSPECIFIED + 1)# /home/bluecmd/Downloads/SAI/inc/saidebugcounter.h: 334

SAI_IN_DROP_REASON_SIP_EQUALS_DIP = (SAI_IN_DROP_REASON_MC_DMAC_MISMATCH + 1)# /home/bluecmd/Downloads/SAI/inc/saidebugcounter.h: 334

SAI_IN_DROP_REASON_SIP_BC = (SAI_IN_DROP_REASON_SIP_EQUALS_DIP + 1)# /home/bluecmd/Downloads/SAI/inc/saidebugcounter.h: 334

SAI_IN_DROP_REASON_DIP_LOCAL = (SAI_IN_DROP_REASON_SIP_BC + 1)# /home/bluecmd/Downloads/SAI/inc/saidebugcounter.h: 334

SAI_IN_DROP_REASON_DIP_LINK_LOCAL = (SAI_IN_DROP_REASON_DIP_LOCAL + 1)# /home/bluecmd/Downloads/SAI/inc/saidebugcounter.h: 334

SAI_IN_DROP_REASON_SIP_LINK_LOCAL = (SAI_IN_DROP_REASON_DIP_LINK_LOCAL + 1)# /home/bluecmd/Downloads/SAI/inc/saidebugcounter.h: 334

SAI_IN_DROP_REASON_IPV6_MC_SCOPE0 = (SAI_IN_DROP_REASON_SIP_LINK_LOCAL + 1)# /home/bluecmd/Downloads/SAI/inc/saidebugcounter.h: 334

SAI_IN_DROP_REASON_IPV6_MC_SCOPE1 = (SAI_IN_DROP_REASON_IPV6_MC_SCOPE0 + 1)# /home/bluecmd/Downloads/SAI/inc/saidebugcounter.h: 334

SAI_IN_DROP_REASON_IRIF_DISABLED = (SAI_IN_DROP_REASON_IPV6_MC_SCOPE1 + 1)# /home/bluecmd/Downloads/SAI/inc/saidebugcounter.h: 334

SAI_IN_DROP_REASON_ERIF_DISABLED = (SAI_IN_DROP_REASON_IRIF_DISABLED + 1)# /home/bluecmd/Downloads/SAI/inc/saidebugcounter.h: 334

SAI_IN_DROP_REASON_LPM4_MISS = (SAI_IN_DROP_REASON_ERIF_DISABLED + 1)# /home/bluecmd/Downloads/SAI/inc/saidebugcounter.h: 334

SAI_IN_DROP_REASON_LPM6_MISS = (SAI_IN_DROP_REASON_LPM4_MISS + 1)# /home/bluecmd/Downloads/SAI/inc/saidebugcounter.h: 334

SAI_IN_DROP_REASON_BLACKHOLE_ROUTE = (SAI_IN_DROP_REASON_LPM6_MISS + 1)# /home/bluecmd/Downloads/SAI/inc/saidebugcounter.h: 334

SAI_IN_DROP_REASON_BLACKHOLE_ARP = (SAI_IN_DROP_REASON_BLACKHOLE_ROUTE + 1)# /home/bluecmd/Downloads/SAI/inc/saidebugcounter.h: 334

SAI_IN_DROP_REASON_UNRESOLVED_NEXT_HOP = (SAI_IN_DROP_REASON_BLACKHOLE_ARP + 1)# /home/bluecmd/Downloads/SAI/inc/saidebugcounter.h: 334

SAI_IN_DROP_REASON_L3_EGRESS_LINK_DOWN = (SAI_IN_DROP_REASON_UNRESOLVED_NEXT_HOP + 1)# /home/bluecmd/Downloads/SAI/inc/saidebugcounter.h: 334

SAI_IN_DROP_REASON_DECAP_ERROR = (SAI_IN_DROP_REASON_L3_EGRESS_LINK_DOWN + 1)# /home/bluecmd/Downloads/SAI/inc/saidebugcounter.h: 334

SAI_IN_DROP_REASON_ACL_ANY = (SAI_IN_DROP_REASON_DECAP_ERROR + 1)# /home/bluecmd/Downloads/SAI/inc/saidebugcounter.h: 334

SAI_IN_DROP_REASON_ACL_INGRESS_PORT = (SAI_IN_DROP_REASON_ACL_ANY + 1)# /home/bluecmd/Downloads/SAI/inc/saidebugcounter.h: 334

SAI_IN_DROP_REASON_ACL_INGRESS_LAG = (SAI_IN_DROP_REASON_ACL_INGRESS_PORT + 1)# /home/bluecmd/Downloads/SAI/inc/saidebugcounter.h: 334

SAI_IN_DROP_REASON_ACL_INGRESS_VLAN = (SAI_IN_DROP_REASON_ACL_INGRESS_LAG + 1)# /home/bluecmd/Downloads/SAI/inc/saidebugcounter.h: 334

SAI_IN_DROP_REASON_ACL_INGRESS_RIF = (SAI_IN_DROP_REASON_ACL_INGRESS_VLAN + 1)# /home/bluecmd/Downloads/SAI/inc/saidebugcounter.h: 334

SAI_IN_DROP_REASON_ACL_INGRESS_SWITCH = (SAI_IN_DROP_REASON_ACL_INGRESS_RIF + 1)# /home/bluecmd/Downloads/SAI/inc/saidebugcounter.h: 334

SAI_IN_DROP_REASON_ACL_EGRESS_PORT = (SAI_IN_DROP_REASON_ACL_INGRESS_SWITCH + 1)# /home/bluecmd/Downloads/SAI/inc/saidebugcounter.h: 334

SAI_IN_DROP_REASON_ACL_EGRESS_LAG = (SAI_IN_DROP_REASON_ACL_EGRESS_PORT + 1)# /home/bluecmd/Downloads/SAI/inc/saidebugcounter.h: 334

SAI_IN_DROP_REASON_ACL_EGRESS_VLAN = (SAI_IN_DROP_REASON_ACL_EGRESS_LAG + 1)# /home/bluecmd/Downloads/SAI/inc/saidebugcounter.h: 334

SAI_IN_DROP_REASON_ACL_EGRESS_RIF = (SAI_IN_DROP_REASON_ACL_EGRESS_VLAN + 1)# /home/bluecmd/Downloads/SAI/inc/saidebugcounter.h: 334

SAI_IN_DROP_REASON_ACL_EGRESS_SWITCH = (SAI_IN_DROP_REASON_ACL_EGRESS_RIF + 1)# /home/bluecmd/Downloads/SAI/inc/saidebugcounter.h: 334

SAI_IN_DROP_REASON_FDB_AND_BLACKHOLE_DISCARDS = (SAI_IN_DROP_REASON_ACL_EGRESS_SWITCH + 1)# /home/bluecmd/Downloads/SAI/inc/saidebugcounter.h: 334

SAI_IN_DROP_REASON_MPLS_MISS = (SAI_IN_DROP_REASON_FDB_AND_BLACKHOLE_DISCARDS + 1)# /home/bluecmd/Downloads/SAI/inc/saidebugcounter.h: 334

SAI_IN_DROP_REASON_SRV6_LOCAL_SID_DROP = (SAI_IN_DROP_REASON_MPLS_MISS + 1)# /home/bluecmd/Downloads/SAI/inc/saidebugcounter.h: 334

SAI_IN_DROP_REASON_END = (SAI_IN_DROP_REASON_SRV6_LOCAL_SID_DROP + 1)# /home/bluecmd/Downloads/SAI/inc/saidebugcounter.h: 334

SAI_IN_DROP_REASON_CUSTOM_RANGE_BASE = 0x10000000# /home/bluecmd/Downloads/SAI/inc/saidebugcounter.h: 334

SAI_IN_DROP_REASON_CUSTOM_RANGE_END = (SAI_IN_DROP_REASON_CUSTOM_RANGE_BASE + 1)# /home/bluecmd/Downloads/SAI/inc/saidebugcounter.h: 334

sai_in_drop_reason_t = enum__sai_in_drop_reason_t# /home/bluecmd/Downloads/SAI/inc/saidebugcounter.h: 334

enum__sai_out_drop_reason_t = c_int# /home/bluecmd/Downloads/SAI/inc/saidebugcounter.h: 380

SAI_OUT_DROP_REASON_START = 0# /home/bluecmd/Downloads/SAI/inc/saidebugcounter.h: 380

SAI_OUT_DROP_REASON_L2_ANY = SAI_OUT_DROP_REASON_START# /home/bluecmd/Downloads/SAI/inc/saidebugcounter.h: 380

SAI_OUT_DROP_REASON_EGRESS_VLAN_FILTER = (SAI_OUT_DROP_REASON_L2_ANY + 1)# /home/bluecmd/Downloads/SAI/inc/saidebugcounter.h: 380

SAI_OUT_DROP_REASON_L3_ANY = (SAI_OUT_DROP_REASON_EGRESS_VLAN_FILTER + 1)# /home/bluecmd/Downloads/SAI/inc/saidebugcounter.h: 380

SAI_OUT_DROP_REASON_L3_EGRESS_LINK_DOWN = (SAI_OUT_DROP_REASON_L3_ANY + 1)# /home/bluecmd/Downloads/SAI/inc/saidebugcounter.h: 380

SAI_OUT_DROP_REASON_TUNNEL_LOOPBACK_PACKET_DROP = (SAI_OUT_DROP_REASON_L3_EGRESS_LINK_DOWN + 1)# /home/bluecmd/Downloads/SAI/inc/saidebugcounter.h: 380

SAI_OUT_DROP_REASON_END = (SAI_OUT_DROP_REASON_TUNNEL_LOOPBACK_PACKET_DROP + 1)# /home/bluecmd/Downloads/SAI/inc/saidebugcounter.h: 380

SAI_OUT_DROP_REASON_CUSTOM_RANGE_BASE = 0x10000000# /home/bluecmd/Downloads/SAI/inc/saidebugcounter.h: 380

SAI_OUT_DROP_REASON_CUSTOM_RANGE_END = (SAI_OUT_DROP_REASON_CUSTOM_RANGE_BASE + 1)# /home/bluecmd/Downloads/SAI/inc/saidebugcounter.h: 380

sai_out_drop_reason_t = enum__sai_out_drop_reason_t# /home/bluecmd/Downloads/SAI/inc/saidebugcounter.h: 380

enum__sai_debug_counter_attr_t = c_int# /home/bluecmd/Downloads/SAI/inc/saidebugcounter.h: 455

SAI_DEBUG_COUNTER_ATTR_START = 0# /home/bluecmd/Downloads/SAI/inc/saidebugcounter.h: 455

SAI_DEBUG_COUNTER_ATTR_INDEX = SAI_DEBUG_COUNTER_ATTR_START# /home/bluecmd/Downloads/SAI/inc/saidebugcounter.h: 455

SAI_DEBUG_COUNTER_ATTR_TYPE = (SAI_DEBUG_COUNTER_ATTR_INDEX + 1)# /home/bluecmd/Downloads/SAI/inc/saidebugcounter.h: 455

SAI_DEBUG_COUNTER_ATTR_BIND_METHOD = (SAI_DEBUG_COUNTER_ATTR_TYPE + 1)# /home/bluecmd/Downloads/SAI/inc/saidebugcounter.h: 455

SAI_DEBUG_COUNTER_ATTR_IN_DROP_REASON_LIST = (SAI_DEBUG_COUNTER_ATTR_BIND_METHOD + 1)# /home/bluecmd/Downloads/SAI/inc/saidebugcounter.h: 455

SAI_DEBUG_COUNTER_ATTR_OUT_DROP_REASON_LIST = (SAI_DEBUG_COUNTER_ATTR_IN_DROP_REASON_LIST + 1)# /home/bluecmd/Downloads/SAI/inc/saidebugcounter.h: 455

SAI_DEBUG_COUNTER_ATTR_END = (SAI_DEBUG_COUNTER_ATTR_OUT_DROP_REASON_LIST + 1)# /home/bluecmd/Downloads/SAI/inc/saidebugcounter.h: 455

SAI_DEBUG_COUNTER_ATTR_CUSTOM_RANGE_START = 0x10000000# /home/bluecmd/Downloads/SAI/inc/saidebugcounter.h: 455

SAI_DEBUG_COUNTER_ATTR_CUSTOM_RANGE_END = (SAI_DEBUG_COUNTER_ATTR_CUSTOM_RANGE_START + 1)# /home/bluecmd/Downloads/SAI/inc/saidebugcounter.h: 455

sai_debug_counter_attr_t = enum__sai_debug_counter_attr_t# /home/bluecmd/Downloads/SAI/inc/saidebugcounter.h: 455

sai_create_debug_counter_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saidebugcounter.h: 467

sai_remove_debug_counter_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t)# /home/bluecmd/Downloads/SAI/inc/saidebugcounter.h: 480

sai_set_debug_counter_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saidebugcounter.h: 491

sai_get_debug_counter_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saidebugcounter.h: 504

# /home/bluecmd/Downloads/SAI/inc/saidebugcounter.h: 519
class struct__sai_debug_counter_api_t(Structure):
    pass

struct__sai_debug_counter_api_t.__slots__ = [
    'create_debug_counter',
    'remove_debug_counter',
    'set_debug_counter_attribute',
    'get_debug_counter_attribute',
]
struct__sai_debug_counter_api_t._fields_ = [
    ('create_debug_counter', sai_create_debug_counter_fn),
    ('remove_debug_counter', sai_remove_debug_counter_fn),
    ('set_debug_counter_attribute', sai_set_debug_counter_attribute_fn),
    ('get_debug_counter_attribute', sai_get_debug_counter_attribute_fn),
]

sai_debug_counter_api_t = struct__sai_debug_counter_api_t# /home/bluecmd/Downloads/SAI/inc/saidebugcounter.h: 519

enum__sai_dtel_attr_t = c_int# /home/bluecmd/Downloads/SAI/inc/saidtel.h: 179

SAI_DTEL_ATTR_START = 0# /home/bluecmd/Downloads/SAI/inc/saidtel.h: 179

SAI_DTEL_ATTR_INT_ENDPOINT_ENABLE = SAI_DTEL_ATTR_START# /home/bluecmd/Downloads/SAI/inc/saidtel.h: 179

SAI_DTEL_ATTR_INT_TRANSIT_ENABLE = (SAI_DTEL_ATTR_INT_ENDPOINT_ENABLE + 1)# /home/bluecmd/Downloads/SAI/inc/saidtel.h: 179

SAI_DTEL_ATTR_POSTCARD_ENABLE = (SAI_DTEL_ATTR_INT_TRANSIT_ENABLE + 1)# /home/bluecmd/Downloads/SAI/inc/saidtel.h: 179

SAI_DTEL_ATTR_DROP_REPORT_ENABLE = (SAI_DTEL_ATTR_POSTCARD_ENABLE + 1)# /home/bluecmd/Downloads/SAI/inc/saidtel.h: 179

SAI_DTEL_ATTR_QUEUE_REPORT_ENABLE = (SAI_DTEL_ATTR_DROP_REPORT_ENABLE + 1)# /home/bluecmd/Downloads/SAI/inc/saidtel.h: 179

SAI_DTEL_ATTR_SWITCH_ID = (SAI_DTEL_ATTR_QUEUE_REPORT_ENABLE + 1)# /home/bluecmd/Downloads/SAI/inc/saidtel.h: 179

SAI_DTEL_ATTR_FLOW_STATE_CLEAR_CYCLE = (SAI_DTEL_ATTR_SWITCH_ID + 1)# /home/bluecmd/Downloads/SAI/inc/saidtel.h: 179

SAI_DTEL_ATTR_LATENCY_SENSITIVITY = (SAI_DTEL_ATTR_FLOW_STATE_CLEAR_CYCLE + 1)# /home/bluecmd/Downloads/SAI/inc/saidtel.h: 179

SAI_DTEL_ATTR_SINK_PORT_LIST = (SAI_DTEL_ATTR_LATENCY_SENSITIVITY + 1)# /home/bluecmd/Downloads/SAI/inc/saidtel.h: 179

SAI_DTEL_ATTR_INT_L4_DSCP = (SAI_DTEL_ATTR_SINK_PORT_LIST + 1)# /home/bluecmd/Downloads/SAI/inc/saidtel.h: 179

SAI_DTEL_ATTR_END = (SAI_DTEL_ATTR_INT_L4_DSCP + 1)# /home/bluecmd/Downloads/SAI/inc/saidtel.h: 179

SAI_DTEL_ATTR_CUSTOM_RANGE_START = 0x10000000# /home/bluecmd/Downloads/SAI/inc/saidtel.h: 179

SAI_DTEL_ATTR_CUSTOM_RANGE_END = (SAI_DTEL_ATTR_CUSTOM_RANGE_START + 1)# /home/bluecmd/Downloads/SAI/inc/saidtel.h: 179

sai_dtel_attr_t = enum__sai_dtel_attr_t# /home/bluecmd/Downloads/SAI/inc/saidtel.h: 179

enum__sai_dtel_queue_report_attr_t = c_int# /home/bluecmd/Downloads/SAI/inc/saidtel.h: 263

SAI_DTEL_QUEUE_REPORT_ATTR_START = 0# /home/bluecmd/Downloads/SAI/inc/saidtel.h: 263

SAI_DTEL_QUEUE_REPORT_ATTR_QUEUE_ID = SAI_DTEL_QUEUE_REPORT_ATTR_START# /home/bluecmd/Downloads/SAI/inc/saidtel.h: 263

SAI_DTEL_QUEUE_REPORT_ATTR_DEPTH_THRESHOLD = (SAI_DTEL_QUEUE_REPORT_ATTR_QUEUE_ID + 1)# /home/bluecmd/Downloads/SAI/inc/saidtel.h: 263

SAI_DTEL_QUEUE_REPORT_ATTR_LATENCY_THRESHOLD = (SAI_DTEL_QUEUE_REPORT_ATTR_DEPTH_THRESHOLD + 1)# /home/bluecmd/Downloads/SAI/inc/saidtel.h: 263

SAI_DTEL_QUEUE_REPORT_ATTR_BREACH_QUOTA = (SAI_DTEL_QUEUE_REPORT_ATTR_LATENCY_THRESHOLD + 1)# /home/bluecmd/Downloads/SAI/inc/saidtel.h: 263

SAI_DTEL_QUEUE_REPORT_ATTR_TAIL_DROP = (SAI_DTEL_QUEUE_REPORT_ATTR_BREACH_QUOTA + 1)# /home/bluecmd/Downloads/SAI/inc/saidtel.h: 263

SAI_DTEL_QUEUE_REPORT_ATTR_END = (SAI_DTEL_QUEUE_REPORT_ATTR_TAIL_DROP + 1)# /home/bluecmd/Downloads/SAI/inc/saidtel.h: 263

SAI_DTEL_QUEUE_REPORT_ATTR_CUSTOM_RANGE_START = 0x10000000# /home/bluecmd/Downloads/SAI/inc/saidtel.h: 263

SAI_DTEL_QUEUE_REPORT_ATTR_CUSTOM_RANGE_END = (SAI_DTEL_QUEUE_REPORT_ATTR_CUSTOM_RANGE_START + 1)# /home/bluecmd/Downloads/SAI/inc/saidtel.h: 263

sai_dtel_queue_report_attr_t = enum__sai_dtel_queue_report_attr_t# /home/bluecmd/Downloads/SAI/inc/saidtel.h: 263

enum__sai_dtel_int_session_attr_t = c_int# /home/bluecmd/Downloads/SAI/inc/saidtel.h: 361

SAI_DTEL_INT_SESSION_ATTR_START = 0# /home/bluecmd/Downloads/SAI/inc/saidtel.h: 361

SAI_DTEL_INT_SESSION_ATTR_MAX_HOP_COUNT = SAI_DTEL_INT_SESSION_ATTR_START# /home/bluecmd/Downloads/SAI/inc/saidtel.h: 361

SAI_DTEL_INT_SESSION_ATTR_COLLECT_SWITCH_ID = (SAI_DTEL_INT_SESSION_ATTR_MAX_HOP_COUNT + 1)# /home/bluecmd/Downloads/SAI/inc/saidtel.h: 361

SAI_DTEL_INT_SESSION_ATTR_COLLECT_SWITCH_PORTS = (SAI_DTEL_INT_SESSION_ATTR_COLLECT_SWITCH_ID + 1)# /home/bluecmd/Downloads/SAI/inc/saidtel.h: 361

SAI_DTEL_INT_SESSION_ATTR_COLLECT_INGRESS_TIMESTAMP = (SAI_DTEL_INT_SESSION_ATTR_COLLECT_SWITCH_PORTS + 1)# /home/bluecmd/Downloads/SAI/inc/saidtel.h: 361

SAI_DTEL_INT_SESSION_ATTR_COLLECT_EGRESS_TIMESTAMP = (SAI_DTEL_INT_SESSION_ATTR_COLLECT_INGRESS_TIMESTAMP + 1)# /home/bluecmd/Downloads/SAI/inc/saidtel.h: 361

SAI_DTEL_INT_SESSION_ATTR_COLLECT_QUEUE_INFO = (SAI_DTEL_INT_SESSION_ATTR_COLLECT_EGRESS_TIMESTAMP + 1)# /home/bluecmd/Downloads/SAI/inc/saidtel.h: 361

SAI_DTEL_INT_SESSION_ATTR_END = (SAI_DTEL_INT_SESSION_ATTR_COLLECT_QUEUE_INFO + 1)# /home/bluecmd/Downloads/SAI/inc/saidtel.h: 361

SAI_DTEL_INT_SESSION_ATTR_CUSTOM_RANGE_START = 0x10000000# /home/bluecmd/Downloads/SAI/inc/saidtel.h: 361

SAI_DTEL_INT_SESSION_ATTR_CUSTOM_RANGE_END = (SAI_DTEL_INT_SESSION_ATTR_CUSTOM_RANGE_START + 1)# /home/bluecmd/Downloads/SAI/inc/saidtel.h: 361

sai_dtel_int_session_attr_t = enum__sai_dtel_int_session_attr_t# /home/bluecmd/Downloads/SAI/inc/saidtel.h: 361

enum__sai_dtel_report_session_attr_t = c_int# /home/bluecmd/Downloads/SAI/inc/saidtel.h: 449

SAI_DTEL_REPORT_SESSION_ATTR_START = 0# /home/bluecmd/Downloads/SAI/inc/saidtel.h: 449

SAI_DTEL_REPORT_SESSION_ATTR_SRC_IP = SAI_DTEL_REPORT_SESSION_ATTR_START# /home/bluecmd/Downloads/SAI/inc/saidtel.h: 449

SAI_DTEL_REPORT_SESSION_ATTR_DST_IP_LIST = (SAI_DTEL_REPORT_SESSION_ATTR_SRC_IP + 1)# /home/bluecmd/Downloads/SAI/inc/saidtel.h: 449

SAI_DTEL_REPORT_SESSION_ATTR_VIRTUAL_ROUTER_ID = (SAI_DTEL_REPORT_SESSION_ATTR_DST_IP_LIST + 1)# /home/bluecmd/Downloads/SAI/inc/saidtel.h: 449

SAI_DTEL_REPORT_SESSION_ATTR_TRUNCATE_SIZE = (SAI_DTEL_REPORT_SESSION_ATTR_VIRTUAL_ROUTER_ID + 1)# /home/bluecmd/Downloads/SAI/inc/saidtel.h: 449

SAI_DTEL_REPORT_SESSION_ATTR_UDP_DST_PORT = (SAI_DTEL_REPORT_SESSION_ATTR_TRUNCATE_SIZE + 1)# /home/bluecmd/Downloads/SAI/inc/saidtel.h: 449

SAI_DTEL_REPORT_SESSION_ATTR_END = (SAI_DTEL_REPORT_SESSION_ATTR_UDP_DST_PORT + 1)# /home/bluecmd/Downloads/SAI/inc/saidtel.h: 449

SAI_DTEL_REPORT_SESSION_ATTR_CUSTOM_RANGE_START = 0x10000000# /home/bluecmd/Downloads/SAI/inc/saidtel.h: 449

SAI_DTEL_REPORT_SESSION_ATTR_CUSTOM_RANGE_END = (SAI_DTEL_REPORT_SESSION_ATTR_CUSTOM_RANGE_START + 1)# /home/bluecmd/Downloads/SAI/inc/saidtel.h: 449

sai_dtel_report_session_attr_t = enum__sai_dtel_report_session_attr_t# /home/bluecmd/Downloads/SAI/inc/saidtel.h: 449

enum__sai_dtel_event_type_t = c_int# /home/bluecmd/Downloads/SAI/inc/saidtel.h: 478

SAI_DTEL_EVENT_TYPE_FLOW_STATE = 0# /home/bluecmd/Downloads/SAI/inc/saidtel.h: 478

SAI_DTEL_EVENT_TYPE_FLOW_REPORT_ALL_PACKETS = (SAI_DTEL_EVENT_TYPE_FLOW_STATE + 1)# /home/bluecmd/Downloads/SAI/inc/saidtel.h: 478

SAI_DTEL_EVENT_TYPE_FLOW_TCPFLAG = (SAI_DTEL_EVENT_TYPE_FLOW_REPORT_ALL_PACKETS + 1)# /home/bluecmd/Downloads/SAI/inc/saidtel.h: 478

SAI_DTEL_EVENT_TYPE_QUEUE_REPORT_THRESHOLD_BREACH = (SAI_DTEL_EVENT_TYPE_FLOW_TCPFLAG + 1)# /home/bluecmd/Downloads/SAI/inc/saidtel.h: 478

SAI_DTEL_EVENT_TYPE_QUEUE_REPORT_TAIL_DROP = (SAI_DTEL_EVENT_TYPE_QUEUE_REPORT_THRESHOLD_BREACH + 1)# /home/bluecmd/Downloads/SAI/inc/saidtel.h: 478

SAI_DTEL_EVENT_TYPE_DROP_REPORT = (SAI_DTEL_EVENT_TYPE_QUEUE_REPORT_TAIL_DROP + 1)# /home/bluecmd/Downloads/SAI/inc/saidtel.h: 478

SAI_DTEL_EVENT_TYPE_MAX = (SAI_DTEL_EVENT_TYPE_DROP_REPORT + 1)# /home/bluecmd/Downloads/SAI/inc/saidtel.h: 478

sai_dtel_event_type_t = enum__sai_dtel_event_type_t# /home/bluecmd/Downloads/SAI/inc/saidtel.h: 478

enum__sai_dtel_event_attr_t = c_int# /home/bluecmd/Downloads/SAI/inc/saidtel.h: 541

SAI_DTEL_EVENT_ATTR_START = 0# /home/bluecmd/Downloads/SAI/inc/saidtel.h: 541

SAI_DTEL_EVENT_ATTR_TYPE = SAI_DTEL_EVENT_ATTR_START# /home/bluecmd/Downloads/SAI/inc/saidtel.h: 541

SAI_DTEL_EVENT_ATTR_REPORT_SESSION = (SAI_DTEL_EVENT_ATTR_TYPE + 1)# /home/bluecmd/Downloads/SAI/inc/saidtel.h: 541

SAI_DTEL_EVENT_ATTR_DSCP_VALUE = (SAI_DTEL_EVENT_ATTR_REPORT_SESSION + 1)# /home/bluecmd/Downloads/SAI/inc/saidtel.h: 541

SAI_DTEL_EVENT_ATTR_END = (SAI_DTEL_EVENT_ATTR_DSCP_VALUE + 1)# /home/bluecmd/Downloads/SAI/inc/saidtel.h: 541

SAI_DTEL_EVENT_ATTR_CUSTOM_RANGE_START = 0x10000000# /home/bluecmd/Downloads/SAI/inc/saidtel.h: 541

SAI_DTEL_EVENT_ATTR_CUSTOM_RANGE_END = (SAI_DTEL_EVENT_ATTR_CUSTOM_RANGE_START + 1)# /home/bluecmd/Downloads/SAI/inc/saidtel.h: 541

sai_dtel_event_attr_t = enum__sai_dtel_event_attr_t# /home/bluecmd/Downloads/SAI/inc/saidtel.h: 541

sai_create_dtel_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saidtel.h: 555

sai_remove_dtel_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t)# /home/bluecmd/Downloads/SAI/inc/saidtel.h: 570

sai_set_dtel_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saidtel.h: 583

sai_get_dtel_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saidtel.h: 598

sai_create_dtel_queue_report_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saidtel.h: 615

sai_remove_dtel_queue_report_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t)# /home/bluecmd/Downloads/SAI/inc/saidtel.h: 630

sai_set_dtel_queue_report_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saidtel.h: 643

sai_get_dtel_queue_report_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saidtel.h: 658

sai_create_dtel_int_session_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saidtel.h: 675

sai_remove_dtel_int_session_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t)# /home/bluecmd/Downloads/SAI/inc/saidtel.h: 690

sai_set_dtel_int_session_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saidtel.h: 703

sai_get_dtel_int_session_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saidtel.h: 718

sai_create_dtel_report_session_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saidtel.h: 735

sai_remove_dtel_report_session_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t)# /home/bluecmd/Downloads/SAI/inc/saidtel.h: 750

sai_set_dtel_report_session_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saidtel.h: 763

sai_get_dtel_report_session_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saidtel.h: 778

sai_create_dtel_event_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saidtel.h: 795

sai_remove_dtel_event_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t)# /home/bluecmd/Downloads/SAI/inc/saidtel.h: 810

sai_set_dtel_event_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saidtel.h: 823

sai_get_dtel_event_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saidtel.h: 838

# /home/bluecmd/Downloads/SAI/inc/saidtel.h: 870
class struct__sai_dtel_api_t(Structure):
    pass

struct__sai_dtel_api_t.__slots__ = [
    'create_dtel',
    'remove_dtel',
    'set_dtel_attribute',
    'get_dtel_attribute',
    'create_dtel_queue_report',
    'remove_dtel_queue_report',
    'set_dtel_queue_report_attribute',
    'get_dtel_queue_report_attribute',
    'create_dtel_int_session',
    'remove_dtel_int_session',
    'set_dtel_int_session_attribute',
    'get_dtel_int_session_attribute',
    'create_dtel_report_session',
    'remove_dtel_report_session',
    'set_dtel_report_session_attribute',
    'get_dtel_report_session_attribute',
    'create_dtel_event',
    'remove_dtel_event',
    'set_dtel_event_attribute',
    'get_dtel_event_attribute',
]
struct__sai_dtel_api_t._fields_ = [
    ('create_dtel', sai_create_dtel_fn),
    ('remove_dtel', sai_remove_dtel_fn),
    ('set_dtel_attribute', sai_set_dtel_attribute_fn),
    ('get_dtel_attribute', sai_get_dtel_attribute_fn),
    ('create_dtel_queue_report', sai_create_dtel_queue_report_fn),
    ('remove_dtel_queue_report', sai_remove_dtel_queue_report_fn),
    ('set_dtel_queue_report_attribute', sai_set_dtel_queue_report_attribute_fn),
    ('get_dtel_queue_report_attribute', sai_get_dtel_queue_report_attribute_fn),
    ('create_dtel_int_session', sai_create_dtel_int_session_fn),
    ('remove_dtel_int_session', sai_remove_dtel_int_session_fn),
    ('set_dtel_int_session_attribute', sai_set_dtel_int_session_attribute_fn),
    ('get_dtel_int_session_attribute', sai_get_dtel_int_session_attribute_fn),
    ('create_dtel_report_session', sai_create_dtel_report_session_fn),
    ('remove_dtel_report_session', sai_remove_dtel_report_session_fn),
    ('set_dtel_report_session_attribute', sai_set_dtel_report_session_attribute_fn),
    ('get_dtel_report_session_attribute', sai_get_dtel_report_session_attribute_fn),
    ('create_dtel_event', sai_create_dtel_event_fn),
    ('remove_dtel_event', sai_remove_dtel_event_fn),
    ('set_dtel_event_attribute', sai_set_dtel_event_attribute_fn),
    ('get_dtel_event_attribute', sai_get_dtel_event_attribute_fn),
]

sai_dtel_api_t = struct__sai_dtel_api_t# /home/bluecmd/Downloads/SAI/inc/saidtel.h: 870

enum__sai_fdb_entry_type_t = c_int# /home/bluecmd/Downloads/SAI/inc/saifdb.h: 47

SAI_FDB_ENTRY_TYPE_DYNAMIC = 0# /home/bluecmd/Downloads/SAI/inc/saifdb.h: 47

SAI_FDB_ENTRY_TYPE_STATIC = (SAI_FDB_ENTRY_TYPE_DYNAMIC + 1)# /home/bluecmd/Downloads/SAI/inc/saifdb.h: 47

sai_fdb_entry_type_t = enum__sai_fdb_entry_type_t# /home/bluecmd/Downloads/SAI/inc/saifdb.h: 47

# /home/bluecmd/Downloads/SAI/inc/saifdb.h: 71
class struct__sai_fdb_entry_t(Structure):
    pass

struct__sai_fdb_entry_t.__slots__ = [
    'switch_id',
    'mac_address',
    'bv_id',
]
struct__sai_fdb_entry_t._fields_ = [
    ('switch_id', sai_object_id_t),
    ('mac_address', sai_mac_t),
    ('bv_id', sai_object_id_t),
]

sai_fdb_entry_t = struct__sai_fdb_entry_t# /home/bluecmd/Downloads/SAI/inc/saifdb.h: 71

enum__sai_fdb_event_t = c_int# /home/bluecmd/Downloads/SAI/inc/saifdb.h: 90

SAI_FDB_EVENT_LEARNED = 0# /home/bluecmd/Downloads/SAI/inc/saifdb.h: 90

SAI_FDB_EVENT_AGED = (SAI_FDB_EVENT_LEARNED + 1)# /home/bluecmd/Downloads/SAI/inc/saifdb.h: 90

SAI_FDB_EVENT_MOVE = (SAI_FDB_EVENT_AGED + 1)# /home/bluecmd/Downloads/SAI/inc/saifdb.h: 90

SAI_FDB_EVENT_FLUSHED = (SAI_FDB_EVENT_MOVE + 1)# /home/bluecmd/Downloads/SAI/inc/saifdb.h: 90

sai_fdb_event_t = enum__sai_fdb_event_t# /home/bluecmd/Downloads/SAI/inc/saifdb.h: 90

enum__sai_fdb_entry_attr_t = c_int# /home/bluecmd/Downloads/SAI/inc/saifdb.h: 204

SAI_FDB_ENTRY_ATTR_START = 0# /home/bluecmd/Downloads/SAI/inc/saifdb.h: 204

SAI_FDB_ENTRY_ATTR_TYPE = SAI_FDB_ENTRY_ATTR_START# /home/bluecmd/Downloads/SAI/inc/saifdb.h: 204

SAI_FDB_ENTRY_ATTR_PACKET_ACTION = (SAI_FDB_ENTRY_ATTR_TYPE + 1)# /home/bluecmd/Downloads/SAI/inc/saifdb.h: 204

SAI_FDB_ENTRY_ATTR_USER_TRAP_ID = (SAI_FDB_ENTRY_ATTR_PACKET_ACTION + 1)# /home/bluecmd/Downloads/SAI/inc/saifdb.h: 204

SAI_FDB_ENTRY_ATTR_BRIDGE_PORT_ID = (SAI_FDB_ENTRY_ATTR_USER_TRAP_ID + 1)# /home/bluecmd/Downloads/SAI/inc/saifdb.h: 204

SAI_FDB_ENTRY_ATTR_META_DATA = (SAI_FDB_ENTRY_ATTR_BRIDGE_PORT_ID + 1)# /home/bluecmd/Downloads/SAI/inc/saifdb.h: 204

SAI_FDB_ENTRY_ATTR_ENDPOINT_IP = (SAI_FDB_ENTRY_ATTR_META_DATA + 1)# /home/bluecmd/Downloads/SAI/inc/saifdb.h: 204

SAI_FDB_ENTRY_ATTR_COUNTER_ID = (SAI_FDB_ENTRY_ATTR_ENDPOINT_IP + 1)# /home/bluecmd/Downloads/SAI/inc/saifdb.h: 204

SAI_FDB_ENTRY_ATTR_ALLOW_MAC_MOVE = (SAI_FDB_ENTRY_ATTR_COUNTER_ID + 1)# /home/bluecmd/Downloads/SAI/inc/saifdb.h: 204

SAI_FDB_ENTRY_ATTR_END = (SAI_FDB_ENTRY_ATTR_ALLOW_MAC_MOVE + 1)# /home/bluecmd/Downloads/SAI/inc/saifdb.h: 204

SAI_FDB_ENTRY_ATTR_CUSTOM_RANGE_START = 0x10000000# /home/bluecmd/Downloads/SAI/inc/saifdb.h: 204

SAI_FDB_ENTRY_ATTR_CUSTOM_RANGE_END = (SAI_FDB_ENTRY_ATTR_CUSTOM_RANGE_START + 1)# /home/bluecmd/Downloads/SAI/inc/saifdb.h: 204

sai_fdb_entry_attr_t = enum__sai_fdb_entry_attr_t# /home/bluecmd/Downloads/SAI/inc/saifdb.h: 204

enum__sai_fdb_flush_entry_type_t = c_int# /home/bluecmd/Downloads/SAI/inc/saifdb.h: 220

SAI_FDB_FLUSH_ENTRY_TYPE_DYNAMIC = 0# /home/bluecmd/Downloads/SAI/inc/saifdb.h: 220

SAI_FDB_FLUSH_ENTRY_TYPE_STATIC = (SAI_FDB_FLUSH_ENTRY_TYPE_DYNAMIC + 1)# /home/bluecmd/Downloads/SAI/inc/saifdb.h: 220

SAI_FDB_FLUSH_ENTRY_TYPE_ALL = (SAI_FDB_FLUSH_ENTRY_TYPE_STATIC + 1)# /home/bluecmd/Downloads/SAI/inc/saifdb.h: 220

sai_fdb_flush_entry_type_t = enum__sai_fdb_flush_entry_type_t# /home/bluecmd/Downloads/SAI/inc/saifdb.h: 220

enum__sai_fdb_flush_attr_t = c_int# /home/bluecmd/Downloads/SAI/inc/saifdb.h: 290

SAI_FDB_FLUSH_ATTR_START = 0# /home/bluecmd/Downloads/SAI/inc/saifdb.h: 290

SAI_FDB_FLUSH_ATTR_BRIDGE_PORT_ID = SAI_FDB_FLUSH_ATTR_START# /home/bluecmd/Downloads/SAI/inc/saifdb.h: 290

SAI_FDB_FLUSH_ATTR_BV_ID = (SAI_FDB_FLUSH_ATTR_BRIDGE_PORT_ID + 1)# /home/bluecmd/Downloads/SAI/inc/saifdb.h: 290

SAI_FDB_FLUSH_ATTR_ENTRY_TYPE = (SAI_FDB_FLUSH_ATTR_BV_ID + 1)# /home/bluecmd/Downloads/SAI/inc/saifdb.h: 290

SAI_FDB_FLUSH_ATTR_END = (SAI_FDB_FLUSH_ATTR_ENTRY_TYPE + 1)# /home/bluecmd/Downloads/SAI/inc/saifdb.h: 290

SAI_FDB_FLUSH_ATTR_CUSTOM_RANGE_START = 0x10000000# /home/bluecmd/Downloads/SAI/inc/saifdb.h: 290

SAI_FDB_FLUSH_ATTR_CUSTOM_RANGE_END = (SAI_FDB_FLUSH_ATTR_CUSTOM_RANGE_START + 1)# /home/bluecmd/Downloads/SAI/inc/saifdb.h: 290

sai_fdb_flush_attr_t = enum__sai_fdb_flush_attr_t# /home/bluecmd/Downloads/SAI/inc/saifdb.h: 290

# /home/bluecmd/Downloads/SAI/inc/saifdb.h: 346
class struct__sai_fdb_event_notification_data_t(Structure):
    pass

struct__sai_fdb_event_notification_data_t.__slots__ = [
    'event_type',
    'fdb_entry',
    'attr_count',
    'attr',
]
struct__sai_fdb_event_notification_data_t._fields_ = [
    ('event_type', sai_fdb_event_t),
    ('fdb_entry', sai_fdb_entry_t),
    ('attr_count', uint32_t),
    ('attr', POINTER(sai_attribute_t)),
]

sai_fdb_event_notification_data_t = struct__sai_fdb_event_notification_data_t# /home/bluecmd/Downloads/SAI/inc/saifdb.h: 346

sai_create_fdb_entry_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_fdb_entry_t), uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saifdb.h: 357

sai_remove_fdb_entry_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_fdb_entry_t))# /home/bluecmd/Downloads/SAI/inc/saifdb.h: 369

sai_set_fdb_entry_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_fdb_entry_t), POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saifdb.h: 380

sai_get_fdb_entry_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_fdb_entry_t), uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saifdb.h: 393

sai_flush_fdb_entries_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saifdb.h: 407

sai_fdb_event_notification_fn = CFUNCTYPE(UNCHECKED(None), uint32_t, POINTER(sai_fdb_event_notification_data_t))# /home/bluecmd/Downloads/SAI/inc/saifdb.h: 420

sai_bulk_create_fdb_entry_fn = CFUNCTYPE(UNCHECKED(sai_status_t), uint32_t, POINTER(sai_fdb_entry_t), POINTER(uint32_t), POINTER(POINTER(sai_attribute_t)), sai_bulk_op_error_mode_t, POINTER(sai_status_t))# /home/bluecmd/Downloads/SAI/inc/saifdb.h: 441

sai_bulk_remove_fdb_entry_fn = CFUNCTYPE(UNCHECKED(sai_status_t), uint32_t, POINTER(sai_fdb_entry_t), sai_bulk_op_error_mode_t, POINTER(sai_status_t))# /home/bluecmd/Downloads/SAI/inc/saifdb.h: 463

sai_bulk_set_fdb_entry_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), uint32_t, POINTER(sai_fdb_entry_t), POINTER(sai_attribute_t), sai_bulk_op_error_mode_t, POINTER(sai_status_t))# /home/bluecmd/Downloads/SAI/inc/saifdb.h: 484

sai_bulk_get_fdb_entry_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), uint32_t, POINTER(sai_fdb_entry_t), POINTER(uint32_t), POINTER(POINTER(sai_attribute_t)), sai_bulk_op_error_mode_t, POINTER(sai_status_t))# /home/bluecmd/Downloads/SAI/inc/saifdb.h: 508

# /home/bluecmd/Downloads/SAI/inc/saifdb.h: 531
class struct__sai_fdb_api_t(Structure):
    pass

struct__sai_fdb_api_t.__slots__ = [
    'create_fdb_entry',
    'remove_fdb_entry',
    'set_fdb_entry_attribute',
    'get_fdb_entry_attribute',
    'flush_fdb_entries',
    'create_fdb_entries',
    'remove_fdb_entries',
    'set_fdb_entries_attribute',
    'get_fdb_entries_attribute',
]
struct__sai_fdb_api_t._fields_ = [
    ('create_fdb_entry', sai_create_fdb_entry_fn),
    ('remove_fdb_entry', sai_remove_fdb_entry_fn),
    ('set_fdb_entry_attribute', sai_set_fdb_entry_attribute_fn),
    ('get_fdb_entry_attribute', sai_get_fdb_entry_attribute_fn),
    ('flush_fdb_entries', sai_flush_fdb_entries_fn),
    ('create_fdb_entries', sai_bulk_create_fdb_entry_fn),
    ('remove_fdb_entries', sai_bulk_remove_fdb_entry_fn),
    ('set_fdb_entries_attribute', sai_bulk_set_fdb_entry_attribute_fn),
    ('get_fdb_entries_attribute', sai_bulk_get_fdb_entry_attribute_fn),
]

sai_fdb_api_t = struct__sai_fdb_api_t# /home/bluecmd/Downloads/SAI/inc/saifdb.h: 531

enum__sai_generic_programmable_attr_t = c_int# /home/bluecmd/Downloads/SAI/inc/saigenericprogrammable.h: 87

SAI_GENERIC_PROGRAMMABLE_ATTR_START = 0# /home/bluecmd/Downloads/SAI/inc/saigenericprogrammable.h: 87

SAI_GENERIC_PROGRAMMABLE_ATTR_OBJECT_NAME = SAI_GENERIC_PROGRAMMABLE_ATTR_START# /home/bluecmd/Downloads/SAI/inc/saigenericprogrammable.h: 87

SAI_GENERIC_PROGRAMMABLE_ATTR_ENTRY = (SAI_GENERIC_PROGRAMMABLE_ATTR_OBJECT_NAME + 1)# /home/bluecmd/Downloads/SAI/inc/saigenericprogrammable.h: 87

SAI_GENERIC_PROGRAMMABLE_ATTR_COUNTER_ID = (SAI_GENERIC_PROGRAMMABLE_ATTR_ENTRY + 1)# /home/bluecmd/Downloads/SAI/inc/saigenericprogrammable.h: 87

SAI_GENERIC_PROGRAMMABLE_ATTR_END = (SAI_GENERIC_PROGRAMMABLE_ATTR_COUNTER_ID + 1)# /home/bluecmd/Downloads/SAI/inc/saigenericprogrammable.h: 87

SAI_GENERIC_PROGRAMMABLE_ATTR_CUSTOM_RANGE_START = 0x10000000# /home/bluecmd/Downloads/SAI/inc/saigenericprogrammable.h: 87

SAI_GENERIC_PROGRAMMABLE_ATTR_CUSTOM_RANGE_END = (SAI_GENERIC_PROGRAMMABLE_ATTR_CUSTOM_RANGE_START + 1)# /home/bluecmd/Downloads/SAI/inc/saigenericprogrammable.h: 87

sai_generic_programmable_attr_t = enum__sai_generic_programmable_attr_t# /home/bluecmd/Downloads/SAI/inc/saigenericprogrammable.h: 87

sai_create_generic_programmable_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saigenericprogrammable.h: 99

sai_remove_generic_programmable_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t)# /home/bluecmd/Downloads/SAI/inc/saigenericprogrammable.h: 112

sai_set_generic_programmable_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saigenericprogrammable.h: 123

sai_get_generic_programmable_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saigenericprogrammable.h: 136

# /home/bluecmd/Downloads/SAI/inc/saigenericprogrammable.h: 150
class struct__sai_generic_programmable_api_t(Structure):
    pass

struct__sai_generic_programmable_api_t.__slots__ = [
    'create_generic_programmable',
    'remove_generic_programmable',
    'set_generic_programmable_attribute',
    'get_generic_programmable_attribute',
]
struct__sai_generic_programmable_api_t._fields_ = [
    ('create_generic_programmable', sai_create_generic_programmable_fn),
    ('remove_generic_programmable', sai_remove_generic_programmable_fn),
    ('set_generic_programmable_attribute', sai_set_generic_programmable_attribute_fn),
    ('get_generic_programmable_attribute', sai_get_generic_programmable_attribute_fn),
]

sai_generic_programmable_api_t = struct__sai_generic_programmable_api_t# /home/bluecmd/Downloads/SAI/inc/saigenericprogrammable.h: 150

enum__sai_native_hash_field_t = c_int# /home/bluecmd/Downloads/SAI/inc/saihash.h: 175

SAI_NATIVE_HASH_FIELD_SRC_IP = 0x00000000# /home/bluecmd/Downloads/SAI/inc/saihash.h: 175

SAI_NATIVE_HASH_FIELD_DST_IP = 0x00000001# /home/bluecmd/Downloads/SAI/inc/saihash.h: 175

SAI_NATIVE_HASH_FIELD_INNER_SRC_IP = 0x00000002# /home/bluecmd/Downloads/SAI/inc/saihash.h: 175

SAI_NATIVE_HASH_FIELD_INNER_DST_IP = 0x00000003# /home/bluecmd/Downloads/SAI/inc/saihash.h: 175

SAI_NATIVE_HASH_FIELD_SRC_IPV4 = 0x00000019# /home/bluecmd/Downloads/SAI/inc/saihash.h: 175

SAI_NATIVE_HASH_FIELD_DST_IPV4 = 0x0000001a# /home/bluecmd/Downloads/SAI/inc/saihash.h: 175

SAI_NATIVE_HASH_FIELD_SRC_IPV6 = 0x0000001b# /home/bluecmd/Downloads/SAI/inc/saihash.h: 175

SAI_NATIVE_HASH_FIELD_DST_IPV6 = 0x0000001c# /home/bluecmd/Downloads/SAI/inc/saihash.h: 175

SAI_NATIVE_HASH_FIELD_INNER_SRC_IPV4 = 0x0000001d# /home/bluecmd/Downloads/SAI/inc/saihash.h: 175

SAI_NATIVE_HASH_FIELD_INNER_DST_IPV4 = 0x0000001e# /home/bluecmd/Downloads/SAI/inc/saihash.h: 175

SAI_NATIVE_HASH_FIELD_INNER_SRC_IPV6 = 0x0000001f# /home/bluecmd/Downloads/SAI/inc/saihash.h: 175

SAI_NATIVE_HASH_FIELD_INNER_DST_IPV6 = 0x00000020# /home/bluecmd/Downloads/SAI/inc/saihash.h: 175

SAI_NATIVE_HASH_FIELD_VLAN_ID = 0x00000004# /home/bluecmd/Downloads/SAI/inc/saihash.h: 175

SAI_NATIVE_HASH_FIELD_IP_PROTOCOL = 0x00000005# /home/bluecmd/Downloads/SAI/inc/saihash.h: 175

SAI_NATIVE_HASH_FIELD_ETHERTYPE = 0x00000006# /home/bluecmd/Downloads/SAI/inc/saihash.h: 175

SAI_NATIVE_HASH_FIELD_L4_SRC_PORT = 0x00000007# /home/bluecmd/Downloads/SAI/inc/saihash.h: 175

SAI_NATIVE_HASH_FIELD_L4_DST_PORT = 0x00000008# /home/bluecmd/Downloads/SAI/inc/saihash.h: 175

SAI_NATIVE_HASH_FIELD_SRC_MAC = 0x00000009# /home/bluecmd/Downloads/SAI/inc/saihash.h: 175

SAI_NATIVE_HASH_FIELD_DST_MAC = 0x0000000a# /home/bluecmd/Downloads/SAI/inc/saihash.h: 175

SAI_NATIVE_HASH_FIELD_IN_PORT = 0x0000000b# /home/bluecmd/Downloads/SAI/inc/saihash.h: 175

SAI_NATIVE_HASH_FIELD_INNER_IP_PROTOCOL = 0x0000000c# /home/bluecmd/Downloads/SAI/inc/saihash.h: 175

SAI_NATIVE_HASH_FIELD_INNER_ETHERTYPE = 0x0000000d# /home/bluecmd/Downloads/SAI/inc/saihash.h: 175

SAI_NATIVE_HASH_FIELD_INNER_L4_SRC_PORT = 0x0000000e# /home/bluecmd/Downloads/SAI/inc/saihash.h: 175

SAI_NATIVE_HASH_FIELD_INNER_L4_DST_PORT = 0x0000000f# /home/bluecmd/Downloads/SAI/inc/saihash.h: 175

SAI_NATIVE_HASH_FIELD_INNER_SRC_MAC = 0x00000010# /home/bluecmd/Downloads/SAI/inc/saihash.h: 175

SAI_NATIVE_HASH_FIELD_INNER_DST_MAC = 0x00000011# /home/bluecmd/Downloads/SAI/inc/saihash.h: 175

SAI_NATIVE_HASH_FIELD_MPLS_LABEL_ALL = 0x00000012# /home/bluecmd/Downloads/SAI/inc/saihash.h: 175

SAI_NATIVE_HASH_FIELD_MPLS_LABEL_0 = 0x00000013# /home/bluecmd/Downloads/SAI/inc/saihash.h: 175

SAI_NATIVE_HASH_FIELD_MPLS_LABEL_1 = 0x00000014# /home/bluecmd/Downloads/SAI/inc/saihash.h: 175

SAI_NATIVE_HASH_FIELD_MPLS_LABEL_2 = 0x00000015# /home/bluecmd/Downloads/SAI/inc/saihash.h: 175

SAI_NATIVE_HASH_FIELD_MPLS_LABEL_3 = 0x00000016# /home/bluecmd/Downloads/SAI/inc/saihash.h: 175

SAI_NATIVE_HASH_FIELD_MPLS_LABEL_4 = 0x00000017# /home/bluecmd/Downloads/SAI/inc/saihash.h: 175

SAI_NATIVE_HASH_FIELD_IPV6_FLOW_LABEL = 0x00000018# /home/bluecmd/Downloads/SAI/inc/saihash.h: 175

SAI_NATIVE_HASH_FIELD_NONE = 0x00000021# /home/bluecmd/Downloads/SAI/inc/saihash.h: 175

sai_native_hash_field_t = enum__sai_native_hash_field_t# /home/bluecmd/Downloads/SAI/inc/saihash.h: 175

enum__sai_fine_grained_hash_field_attr_t = c_int# /home/bluecmd/Downloads/SAI/inc/saihash.h: 238

SAI_FINE_GRAINED_HASH_FIELD_ATTR_START = 0# /home/bluecmd/Downloads/SAI/inc/saihash.h: 238

SAI_FINE_GRAINED_HASH_FIELD_ATTR_NATIVE_HASH_FIELD = SAI_FINE_GRAINED_HASH_FIELD_ATTR_START# /home/bluecmd/Downloads/SAI/inc/saihash.h: 238

SAI_FINE_GRAINED_HASH_FIELD_ATTR_IPV4_MASK = (SAI_FINE_GRAINED_HASH_FIELD_ATTR_NATIVE_HASH_FIELD + 1)# /home/bluecmd/Downloads/SAI/inc/saihash.h: 238

SAI_FINE_GRAINED_HASH_FIELD_ATTR_IPV6_MASK = (SAI_FINE_GRAINED_HASH_FIELD_ATTR_IPV4_MASK + 1)# /home/bluecmd/Downloads/SAI/inc/saihash.h: 238

SAI_FINE_GRAINED_HASH_FIELD_ATTR_SEQUENCE_ID = (SAI_FINE_GRAINED_HASH_FIELD_ATTR_IPV6_MASK + 1)# /home/bluecmd/Downloads/SAI/inc/saihash.h: 238

SAI_FINE_GRAINED_HASH_FIELD_ATTR_END = (SAI_FINE_GRAINED_HASH_FIELD_ATTR_SEQUENCE_ID + 1)# /home/bluecmd/Downloads/SAI/inc/saihash.h: 238

SAI_FINE_GRAINED_HASH_FIELD_ATTR_CUSTOM_RANGE_START = 0x10000000# /home/bluecmd/Downloads/SAI/inc/saihash.h: 238

SAI_FINE_GRAINED_HASH_FIELD_ATTR_CUSTOM_RANGE_END = (SAI_FINE_GRAINED_HASH_FIELD_ATTR_CUSTOM_RANGE_START + 1)# /home/bluecmd/Downloads/SAI/inc/saihash.h: 238

sai_fine_grained_hash_field_attr_t = enum__sai_fine_grained_hash_field_attr_t# /home/bluecmd/Downloads/SAI/inc/saihash.h: 238

enum__sai_hash_attr_t = c_int# /home/bluecmd/Downloads/SAI/inc/saihash.h: 290

SAI_HASH_ATTR_START = 0# /home/bluecmd/Downloads/SAI/inc/saihash.h: 290

SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST = SAI_HASH_ATTR_START# /home/bluecmd/Downloads/SAI/inc/saihash.h: 290

SAI_HASH_ATTR_UDF_GROUP_LIST = (SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST + 1)# /home/bluecmd/Downloads/SAI/inc/saihash.h: 290

SAI_HASH_ATTR_FINE_GRAINED_HASH_FIELD_LIST = (SAI_HASH_ATTR_UDF_GROUP_LIST + 1)# /home/bluecmd/Downloads/SAI/inc/saihash.h: 290

SAI_HASH_ATTR_END = (SAI_HASH_ATTR_FINE_GRAINED_HASH_FIELD_LIST + 1)# /home/bluecmd/Downloads/SAI/inc/saihash.h: 290

SAI_HASH_ATTR_CUSTOM_RANGE_START = 0x10000000# /home/bluecmd/Downloads/SAI/inc/saihash.h: 290

SAI_HASH_ATTR_CUSTOM_RANGE_END = (SAI_HASH_ATTR_CUSTOM_RANGE_START + 1)# /home/bluecmd/Downloads/SAI/inc/saihash.h: 290

sai_hash_attr_t = enum__sai_hash_attr_t# /home/bluecmd/Downloads/SAI/inc/saihash.h: 290

sai_create_fine_grained_hash_field_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saihash.h: 302

sai_remove_fine_grained_hash_field_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t)# /home/bluecmd/Downloads/SAI/inc/saihash.h: 315

sai_set_fine_grained_hash_field_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saihash.h: 326

sai_get_fine_grained_hash_field_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saihash.h: 339

sai_create_hash_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saihash.h: 354

sai_remove_hash_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t)# /home/bluecmd/Downloads/SAI/inc/saihash.h: 367

sai_set_hash_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saihash.h: 378

sai_get_hash_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saihash.h: 391

# /home/bluecmd/Downloads/SAI/inc/saihash.h: 410
class struct__sai_hash_api_t(Structure):
    pass

struct__sai_hash_api_t.__slots__ = [
    'create_hash',
    'remove_hash',
    'set_hash_attribute',
    'get_hash_attribute',
    'create_fine_grained_hash_field',
    'remove_fine_grained_hash_field',
    'set_fine_grained_hash_field_attribute',
    'get_fine_grained_hash_field_attribute',
]
struct__sai_hash_api_t._fields_ = [
    ('create_hash', sai_create_hash_fn),
    ('remove_hash', sai_remove_hash_fn),
    ('set_hash_attribute', sai_set_hash_attribute_fn),
    ('get_hash_attribute', sai_get_hash_attribute_fn),
    ('create_fine_grained_hash_field', sai_create_fine_grained_hash_field_fn),
    ('remove_fine_grained_hash_field', sai_remove_fine_grained_hash_field_fn),
    ('set_fine_grained_hash_field_attribute', sai_set_fine_grained_hash_field_attribute_fn),
    ('get_fine_grained_hash_field_attribute', sai_get_fine_grained_hash_field_attribute_fn),
]

sai_hash_api_t = struct__sai_hash_api_t# /home/bluecmd/Downloads/SAI/inc/saihash.h: 410

enum__sai_hostif_trap_group_attr_t = c_int# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 112

SAI_HOSTIF_TRAP_GROUP_ATTR_START = 0# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 112

SAI_HOSTIF_TRAP_GROUP_ATTR_ADMIN_STATE = SAI_HOSTIF_TRAP_GROUP_ATTR_START# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 112

SAI_HOSTIF_TRAP_GROUP_ATTR_QUEUE = (SAI_HOSTIF_TRAP_GROUP_ATTR_ADMIN_STATE + 1)# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 112

SAI_HOSTIF_TRAP_GROUP_ATTR_POLICER = (SAI_HOSTIF_TRAP_GROUP_ATTR_QUEUE + 1)# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 112

SAI_HOSTIF_TRAP_GROUP_ATTR_OBJECT_STAGE = (SAI_HOSTIF_TRAP_GROUP_ATTR_POLICER + 1)# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 112

SAI_HOSTIF_TRAP_GROUP_ATTR_END = (SAI_HOSTIF_TRAP_GROUP_ATTR_OBJECT_STAGE + 1)# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 112

SAI_HOSTIF_TRAP_GROUP_ATTR_CUSTOM_RANGE_START = 0x10000000# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 112

SAI_HOSTIF_TRAP_GROUP_ATTR_CUSTOM_RANGE_END = (SAI_HOSTIF_TRAP_GROUP_ATTR_CUSTOM_RANGE_START + 1)# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 112

sai_hostif_trap_group_attr_t = enum__sai_hostif_trap_group_attr_t# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 112

sai_create_hostif_trap_group_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 124

sai_remove_hostif_trap_group_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t)# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 137

sai_set_hostif_trap_group_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 148

sai_get_hostif_trap_group_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 161

enum__sai_hostif_trap_type_t = c_int# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 520

SAI_HOSTIF_TRAP_TYPE_START = 0x00000000# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 520

SAI_HOSTIF_TRAP_TYPE_STP = SAI_HOSTIF_TRAP_TYPE_START# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 520

SAI_HOSTIF_TRAP_TYPE_LACP = 0x00000001# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 520

SAI_HOSTIF_TRAP_TYPE_EAPOL = 0x00000002# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 520

SAI_HOSTIF_TRAP_TYPE_LLDP = 0x00000003# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 520

SAI_HOSTIF_TRAP_TYPE_PVRST = 0x00000004# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 520

SAI_HOSTIF_TRAP_TYPE_IGMP_TYPE_QUERY = 0x00000005# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 520

SAI_HOSTIF_TRAP_TYPE_IGMP_TYPE_LEAVE = 0x00000006# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 520

SAI_HOSTIF_TRAP_TYPE_IGMP_TYPE_V1_REPORT = 0x00000007# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 520

SAI_HOSTIF_TRAP_TYPE_IGMP_TYPE_V2_REPORT = 0x00000008# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 520

SAI_HOSTIF_TRAP_TYPE_IGMP_TYPE_V3_REPORT = 0x00000009# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 520

SAI_HOSTIF_TRAP_TYPE_SAMPLEPACKET = 0x0000000a# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 520

SAI_HOSTIF_TRAP_TYPE_UDLD = 0x0000000b# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 520

SAI_HOSTIF_TRAP_TYPE_CDP = 0x0000000c# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 520

SAI_HOSTIF_TRAP_TYPE_VTP = 0x0000000d# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 520

SAI_HOSTIF_TRAP_TYPE_DTP = 0x0000000e# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 520

SAI_HOSTIF_TRAP_TYPE_PAGP = 0x0000000f# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 520

SAI_HOSTIF_TRAP_TYPE_PTP = 0x00000010# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 520

SAI_HOSTIF_TRAP_TYPE_PTP_TX_EVENT = 0x00000011# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 520

SAI_HOSTIF_TRAP_TYPE_DHCP_L2 = 0x00000012# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 520

SAI_HOSTIF_TRAP_TYPE_DHCPV6_L2 = 0x00000013# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 520

SAI_HOSTIF_TRAP_TYPE_SWITCH_CUSTOM_RANGE_BASE = 0x00001000# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 520

SAI_HOSTIF_TRAP_TYPE_ARP_REQUEST = 0x00002000# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 520

SAI_HOSTIF_TRAP_TYPE_ARP_RESPONSE = 0x00002001# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 520

SAI_HOSTIF_TRAP_TYPE_DHCP = 0x00002002# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 520

SAI_HOSTIF_TRAP_TYPE_OSPF = 0x00002003# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 520

SAI_HOSTIF_TRAP_TYPE_PIM = 0x00002004# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 520

SAI_HOSTIF_TRAP_TYPE_VRRP = 0x00002005# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 520

SAI_HOSTIF_TRAP_TYPE_DHCPV6 = 0x00002006# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 520

SAI_HOSTIF_TRAP_TYPE_OSPFV6 = 0x00002007# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 520

SAI_HOSTIF_TRAP_TYPE_VRRPV6 = 0x00002008# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 520

SAI_HOSTIF_TRAP_TYPE_IPV6_NEIGHBOR_DISCOVERY = 0x00002009# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 520

SAI_HOSTIF_TRAP_TYPE_IPV6_MLD_V1_V2 = 0x0000200a# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 520

SAI_HOSTIF_TRAP_TYPE_IPV6_MLD_V1_REPORT = 0x0000200b# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 520

SAI_HOSTIF_TRAP_TYPE_IPV6_MLD_V1_DONE = 0x0000200c# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 520

SAI_HOSTIF_TRAP_TYPE_MLD_V2_REPORT = 0x0000200d# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 520

SAI_HOSTIF_TRAP_TYPE_UNKNOWN_L3_MULTICAST = 0x0000200e# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 520

SAI_HOSTIF_TRAP_TYPE_SNAT_MISS = 0x0000200f# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 520

SAI_HOSTIF_TRAP_TYPE_DNAT_MISS = 0x00002010# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 520

SAI_HOSTIF_TRAP_TYPE_NAT_HAIRPIN = 0x00002011# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 520

SAI_HOSTIF_TRAP_TYPE_IPV6_NEIGHBOR_SOLICITATION = 0x00002012# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 520

SAI_HOSTIF_TRAP_TYPE_IPV6_NEIGHBOR_ADVERTISEMENT = 0x00002013# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 520

SAI_HOSTIF_TRAP_TYPE_ISIS = 0x00002014# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 520

SAI_HOSTIF_TRAP_TYPE_ROUTER_CUSTOM_RANGE_BASE = 0x00003000# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 520

SAI_HOSTIF_TRAP_TYPE_IP2ME = 0x00004000# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 520

SAI_HOSTIF_TRAP_TYPE_SSH = 0x00004001# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 520

SAI_HOSTIF_TRAP_TYPE_SNMP = 0x00004002# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 520

SAI_HOSTIF_TRAP_TYPE_BGP = 0x00004003# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 520

SAI_HOSTIF_TRAP_TYPE_BGPV6 = 0x00004004# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 520

SAI_HOSTIF_TRAP_TYPE_BFD = 0x00004005# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 520

SAI_HOSTIF_TRAP_TYPE_BFDV6 = 0x00004006# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 520

SAI_HOSTIF_TRAP_TYPE_BFD_MICRO = 0x00004007# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 520

SAI_HOSTIF_TRAP_TYPE_BFDV6_MICRO = 0x00004008# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 520

SAI_HOSTIF_TRAP_TYPE_LDP = 0x00004009# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 520

SAI_HOSTIF_TRAP_TYPE_GNMI = 0x0000400a# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 520

SAI_HOSTIF_TRAP_TYPE_P4RT = 0x0000400b# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 520

SAI_HOSTIF_TRAP_TYPE_NTPCLIENT = 0x0000400c# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 520

SAI_HOSTIF_TRAP_TYPE_NTPSERVER = 0x0000400d# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 520

SAI_HOSTIF_TRAP_TYPE_HTTPCLIENT = 0x0000400e# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 520

SAI_HOSTIF_TRAP_TYPE_HTTPSERVER = 0x0000400f# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 520

SAI_HOSTIF_TRAP_TYPE_LOCAL_IP_CUSTOM_RANGE_BASE = 0x00005000# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 520

SAI_HOSTIF_TRAP_TYPE_L3_MTU_ERROR = 0x00006000# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 520

SAI_HOSTIF_TRAP_TYPE_TTL_ERROR = 0x00006001# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 520

SAI_HOSTIF_TRAP_TYPE_STATIC_FDB_MOVE = 0x00006002# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 520

SAI_HOSTIF_TRAP_TYPE_PIPELINE_DISCARD_EGRESS_BUFFER = 0x00007000# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 520

SAI_HOSTIF_TRAP_TYPE_PIPELINE_DISCARD_WRED = 0x00007001# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 520

SAI_HOSTIF_TRAP_TYPE_PIPELINE_DISCARD_ROUTER = 0x00007002# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 520

SAI_HOSTIF_TRAP_TYPE_MPLS_TTL_ERROR = 0x00008000# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 520

SAI_HOSTIF_TRAP_TYPE_MPLS_ROUTER_ALERT_LABEL = 0x00008001# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 520

SAI_HOSTIF_TRAP_TYPE_MPLS_LABEL_LOOKUP_MISS = 0x00008002# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 520

SAI_HOSTIF_TRAP_TYPE_CUSTOM_EXCEPTION_RANGE_BASE = 0x00009000# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 520

SAI_HOSTIF_TRAP_TYPE_END = 0x0000a000# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 520

sai_hostif_trap_type_t = enum__sai_hostif_trap_type_t# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 520

enum__sai_hostif_trap_attr_t = c_int# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 616

SAI_HOSTIF_TRAP_ATTR_START = 0# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 616

SAI_HOSTIF_TRAP_ATTR_TRAP_TYPE = SAI_HOSTIF_TRAP_ATTR_START# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 616

SAI_HOSTIF_TRAP_ATTR_PACKET_ACTION = (SAI_HOSTIF_TRAP_ATTR_TRAP_TYPE + 1)# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 616

SAI_HOSTIF_TRAP_ATTR_TRAP_PRIORITY = (SAI_HOSTIF_TRAP_ATTR_PACKET_ACTION + 1)# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 616

SAI_HOSTIF_TRAP_ATTR_EXCLUDE_PORT_LIST = (SAI_HOSTIF_TRAP_ATTR_TRAP_PRIORITY + 1)# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 616

SAI_HOSTIF_TRAP_ATTR_TRAP_GROUP = (SAI_HOSTIF_TRAP_ATTR_EXCLUDE_PORT_LIST + 1)# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 616

SAI_HOSTIF_TRAP_ATTR_MIRROR_SESSION = (SAI_HOSTIF_TRAP_ATTR_TRAP_GROUP + 1)# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 616

SAI_HOSTIF_TRAP_ATTR_COUNTER_ID = (SAI_HOSTIF_TRAP_ATTR_MIRROR_SESSION + 1)# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 616

SAI_HOSTIF_TRAP_ATTR_END = (SAI_HOSTIF_TRAP_ATTR_COUNTER_ID + 1)# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 616

SAI_HOSTIF_TRAP_ATTR_CUSTOM_RANGE_START = 0x10000000# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 616

SAI_HOSTIF_TRAP_ATTR_CUSTOM_RANGE_END = (SAI_HOSTIF_TRAP_ATTR_CUSTOM_RANGE_START + 1)# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 616

sai_hostif_trap_attr_t = enum__sai_hostif_trap_attr_t# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 616

sai_create_hostif_trap_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 628

sai_remove_hostif_trap_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t)# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 641

sai_set_hostif_trap_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 652

sai_get_hostif_trap_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 665

enum__sai_hostif_user_defined_trap_type_t = c_int# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 713

SAI_HOSTIF_USER_DEFINED_TRAP_TYPE_START = 0x00000000# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 713

SAI_HOSTIF_USER_DEFINED_TRAP_TYPE_ROUTER = SAI_HOSTIF_USER_DEFINED_TRAP_TYPE_START# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 713

SAI_HOSTIF_USER_DEFINED_TRAP_TYPE_NEIGHBOR = (SAI_HOSTIF_USER_DEFINED_TRAP_TYPE_ROUTER + 1)# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 713

SAI_HOSTIF_USER_DEFINED_TRAP_TYPE_NEIGH = SAI_HOSTIF_USER_DEFINED_TRAP_TYPE_NEIGHBOR# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 713

SAI_HOSTIF_USER_DEFINED_TRAP_TYPE_ACL = (SAI_HOSTIF_USER_DEFINED_TRAP_TYPE_NEIGH + 1)# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 713

SAI_HOSTIF_USER_DEFINED_TRAP_TYPE_FDB = (SAI_HOSTIF_USER_DEFINED_TRAP_TYPE_ACL + 1)# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 713

SAI_HOSTIF_USER_DEFINED_TRAP_TYPE_INSEG_ENTRY = (SAI_HOSTIF_USER_DEFINED_TRAP_TYPE_FDB + 1)# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 713

SAI_HOSTIF_USER_DEFINED_TRAP_TYPE_CUSTOM_RANGE_BASE = 0x00001000# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 713

SAI_HOSTIF_USER_DEFINED_TRAP_TYPE_END = (SAI_HOSTIF_USER_DEFINED_TRAP_TYPE_CUSTOM_RANGE_BASE + 1)# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 713

sai_hostif_user_defined_trap_type_t = enum__sai_hostif_user_defined_trap_type_t# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 713

enum__sai_hostif_user_defined_trap_attr_t = c_int# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 766

SAI_HOSTIF_USER_DEFINED_TRAP_ATTR_START = 0# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 766

SAI_HOSTIF_USER_DEFINED_TRAP_ATTR_TYPE = SAI_HOSTIF_USER_DEFINED_TRAP_ATTR_START# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 766

SAI_HOSTIF_USER_DEFINED_TRAP_ATTR_TRAP_PRIORITY = (SAI_HOSTIF_USER_DEFINED_TRAP_ATTR_TYPE + 1)# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 766

SAI_HOSTIF_USER_DEFINED_TRAP_ATTR_TRAP_GROUP = (SAI_HOSTIF_USER_DEFINED_TRAP_ATTR_TRAP_PRIORITY + 1)# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 766

SAI_HOSTIF_USER_DEFINED_TRAP_ATTR_END = (SAI_HOSTIF_USER_DEFINED_TRAP_ATTR_TRAP_GROUP + 1)# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 766

SAI_HOSTIF_USER_DEFINED_TRAP_ATTR_CUSTOM_RANGE_START = 0x10000000# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 766

SAI_HOSTIF_USER_DEFINED_TRAP_ATTR_CUSTOM_RANGE_END = (SAI_HOSTIF_USER_DEFINED_TRAP_ATTR_CUSTOM_RANGE_START + 1)# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 766

sai_hostif_user_defined_trap_attr_t = enum__sai_hostif_user_defined_trap_attr_t# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 766

sai_create_hostif_user_defined_trap_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 778

sai_remove_hostif_user_defined_trap_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t)# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 791

sai_set_hostif_user_defined_trap_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 802

sai_get_hostif_user_defined_trap_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 815

enum__sai_hostif_type_t = c_int# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 834

SAI_HOSTIF_TYPE_NETDEV = 0# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 834

SAI_HOSTIF_TYPE_FD = (SAI_HOSTIF_TYPE_NETDEV + 1)# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 834

SAI_HOSTIF_TYPE_GENETLINK = (SAI_HOSTIF_TYPE_FD + 1)# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 834

sai_hostif_type_t = enum__sai_hostif_type_t# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 834

enum__sai_hostif_vlan_tag_t = c_int# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 865

SAI_HOSTIF_VLAN_TAG_STRIP = 0# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 865

SAI_HOSTIF_VLAN_TAG_KEEP = (SAI_HOSTIF_VLAN_TAG_STRIP + 1)# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 865

SAI_HOSTIF_VLAN_TAG_ORIGINAL = (SAI_HOSTIF_VLAN_TAG_KEEP + 1)# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 865

sai_hostif_vlan_tag_t = enum__sai_hostif_vlan_tag_t# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 865

enum__sai_hostif_attr_t = c_int# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 966

SAI_HOSTIF_ATTR_START = 0# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 966

SAI_HOSTIF_ATTR_TYPE = SAI_HOSTIF_ATTR_START# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 966

SAI_HOSTIF_ATTR_OBJ_ID = (SAI_HOSTIF_ATTR_TYPE + 1)# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 966

SAI_HOSTIF_ATTR_NAME = (SAI_HOSTIF_ATTR_OBJ_ID + 1)# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 966

SAI_HOSTIF_ATTR_OPER_STATUS = (SAI_HOSTIF_ATTR_NAME + 1)# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 966

SAI_HOSTIF_ATTR_QUEUE = (SAI_HOSTIF_ATTR_OPER_STATUS + 1)# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 966

SAI_HOSTIF_ATTR_VLAN_TAG = (SAI_HOSTIF_ATTR_QUEUE + 1)# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 966

SAI_HOSTIF_ATTR_GENETLINK_MCGRP_NAME = (SAI_HOSTIF_ATTR_VLAN_TAG + 1)# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 966

SAI_HOSTIF_ATTR_END = (SAI_HOSTIF_ATTR_GENETLINK_MCGRP_NAME + 1)# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 966

SAI_HOSTIF_ATTR_CUSTOM_RANGE_START = 0x10000000# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 966

SAI_HOSTIF_ATTR_CUSTOM_RANGE_END = (SAI_HOSTIF_ATTR_CUSTOM_RANGE_START + 1)# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 966

sai_hostif_attr_t = enum__sai_hostif_attr_t# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 966

sai_create_hostif_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 978

sai_remove_hostif_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t)# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 991

sai_set_hostif_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 1002

sai_get_hostif_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 1015

enum__sai_hostif_table_entry_type_t = c_int# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 1040

SAI_HOSTIF_TABLE_ENTRY_TYPE_PORT = 0# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 1040

SAI_HOSTIF_TABLE_ENTRY_TYPE_LAG = (SAI_HOSTIF_TABLE_ENTRY_TYPE_PORT + 1)# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 1040

SAI_HOSTIF_TABLE_ENTRY_TYPE_VLAN = (SAI_HOSTIF_TABLE_ENTRY_TYPE_LAG + 1)# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 1040

SAI_HOSTIF_TABLE_ENTRY_TYPE_TRAP_ID = (SAI_HOSTIF_TABLE_ENTRY_TYPE_VLAN + 1)# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 1040

SAI_HOSTIF_TABLE_ENTRY_TYPE_WILDCARD = (SAI_HOSTIF_TABLE_ENTRY_TYPE_TRAP_ID + 1)# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 1040

sai_hostif_table_entry_type_t = enum__sai_hostif_table_entry_type_t# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 1040

enum__sai_hostif_table_entry_channel_type_t = c_int# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 1065

SAI_HOSTIF_TABLE_ENTRY_CHANNEL_TYPE_CB = 0# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 1065

SAI_HOSTIF_TABLE_ENTRY_CHANNEL_TYPE_FD = (SAI_HOSTIF_TABLE_ENTRY_CHANNEL_TYPE_CB + 1)# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 1065

SAI_HOSTIF_TABLE_ENTRY_CHANNEL_TYPE_NETDEV_PHYSICAL_PORT = (SAI_HOSTIF_TABLE_ENTRY_CHANNEL_TYPE_FD + 1)# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 1065

SAI_HOSTIF_TABLE_ENTRY_CHANNEL_TYPE_NETDEV_LOGICAL_PORT = (SAI_HOSTIF_TABLE_ENTRY_CHANNEL_TYPE_NETDEV_PHYSICAL_PORT + 1)# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 1065

SAI_HOSTIF_TABLE_ENTRY_CHANNEL_TYPE_NETDEV_L3 = (SAI_HOSTIF_TABLE_ENTRY_CHANNEL_TYPE_NETDEV_LOGICAL_PORT + 1)# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 1065

SAI_HOSTIF_TABLE_ENTRY_CHANNEL_TYPE_GENETLINK = (SAI_HOSTIF_TABLE_ENTRY_CHANNEL_TYPE_NETDEV_L3 + 1)# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 1065

sai_hostif_table_entry_channel_type_t = enum__sai_hostif_table_entry_channel_type_t# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 1065

enum__sai_hostif_table_entry_attr_t = c_int# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 1138

SAI_HOSTIF_TABLE_ENTRY_ATTR_START = 0# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 1138

SAI_HOSTIF_TABLE_ENTRY_ATTR_TYPE = SAI_HOSTIF_TABLE_ENTRY_ATTR_START# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 1138

SAI_HOSTIF_TABLE_ENTRY_ATTR_OBJ_ID = (SAI_HOSTIF_TABLE_ENTRY_ATTR_TYPE + 1)# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 1138

SAI_HOSTIF_TABLE_ENTRY_ATTR_TRAP_ID = (SAI_HOSTIF_TABLE_ENTRY_ATTR_OBJ_ID + 1)# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 1138

SAI_HOSTIF_TABLE_ENTRY_ATTR_CHANNEL_TYPE = (SAI_HOSTIF_TABLE_ENTRY_ATTR_TRAP_ID + 1)# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 1138

SAI_HOSTIF_TABLE_ENTRY_ATTR_HOST_IF = (SAI_HOSTIF_TABLE_ENTRY_ATTR_CHANNEL_TYPE + 1)# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 1138

SAI_HOSTIF_TABLE_ENTRY_ATTR_END = (SAI_HOSTIF_TABLE_ENTRY_ATTR_HOST_IF + 1)# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 1138

SAI_HOSTIF_TABLE_ENTRY_ATTR_CUSTOM_RANGE_START = 0x10000000# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 1138

SAI_HOSTIF_TABLE_ENTRY_ATTR_CUSTOM_RANGE_END = (SAI_HOSTIF_TABLE_ENTRY_ATTR_CUSTOM_RANGE_START + 1)# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 1138

sai_hostif_table_entry_attr_t = enum__sai_hostif_table_entry_attr_t# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 1138

sai_create_hostif_table_entry_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 1150

sai_remove_hostif_table_entry_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t)# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 1163

sai_set_hostif_table_entry_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 1174

sai_get_hostif_table_entry_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 1187

enum__sai_hostif_tx_type_t = c_int# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 1209

SAI_HOSTIF_TX_TYPE_PIPELINE_BYPASS = 0# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 1209

SAI_HOSTIF_TX_TYPE_PIPELINE_LOOKUP = (SAI_HOSTIF_TX_TYPE_PIPELINE_BYPASS + 1)# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 1209

SAI_HOSTIF_TX_TYPE_CUSTOM_RANGE_BASE = 0x10000000# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 1209

sai_hostif_tx_type_t = enum__sai_hostif_tx_type_t# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 1209

enum__sai_hostif_packet_attr_t = c_int# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 1324

SAI_HOSTIF_PACKET_ATTR_START = 0# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 1324

SAI_HOSTIF_PACKET_ATTR_HOSTIF_TRAP_ID = SAI_HOSTIF_PACKET_ATTR_START# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 1324

SAI_HOSTIF_PACKET_ATTR_INGRESS_PORT = (SAI_HOSTIF_PACKET_ATTR_HOSTIF_TRAP_ID + 1)# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 1324

SAI_HOSTIF_PACKET_ATTR_INGRESS_LAG = (SAI_HOSTIF_PACKET_ATTR_INGRESS_PORT + 1)# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 1324

SAI_HOSTIF_PACKET_ATTR_HOSTIF_TX_TYPE = (SAI_HOSTIF_PACKET_ATTR_INGRESS_LAG + 1)# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 1324

SAI_HOSTIF_PACKET_ATTR_EGRESS_PORT_OR_LAG = (SAI_HOSTIF_PACKET_ATTR_HOSTIF_TX_TYPE + 1)# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 1324

SAI_HOSTIF_PACKET_ATTR_BRIDGE_ID = (SAI_HOSTIF_PACKET_ATTR_EGRESS_PORT_OR_LAG + 1)# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 1324

SAI_HOSTIF_PACKET_ATTR_TIMESTAMP = (SAI_HOSTIF_PACKET_ATTR_BRIDGE_ID + 1)# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 1324

SAI_HOSTIF_PACKET_ATTR_EGRESS_QUEUE_INDEX = (SAI_HOSTIF_PACKET_ATTR_TIMESTAMP + 1)# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 1324

SAI_HOSTIF_PACKET_ATTR_ZERO_COPY_TX = (SAI_HOSTIF_PACKET_ATTR_EGRESS_QUEUE_INDEX + 1)# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 1324

SAI_HOSTIF_PACKET_ATTR_END = (SAI_HOSTIF_PACKET_ATTR_ZERO_COPY_TX + 1)# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 1324

SAI_HOSTIF_PACKET_ATTR_CUSTOM_RANGE_START = 0x10000000# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 1324

SAI_HOSTIF_PACKET_ATTR_CUSTOM_RANGE_END = (SAI_HOSTIF_PACKET_ATTR_CUSTOM_RANGE_START + 1)# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 1324

sai_hostif_packet_attr_t = enum__sai_hostif_packet_attr_t# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 1324

sai_recv_hostif_packet_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_size_t), POINTER(None), POINTER(uint32_t), POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 1340

sai_send_hostif_packet_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, sai_size_t, POINTER(None), uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 1360

sai_allocate_hostif_packet_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, sai_size_t, POINTER(POINTER(None)), uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 1382

sai_free_hostif_packet_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(None))# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 1399

sai_packet_event_notification_fn = CFUNCTYPE(UNCHECKED(None), sai_object_id_t, sai_size_t, POINTER(None), uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 1417

# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 1453
class struct__sai_hostif_api_t(Structure):
    pass

struct__sai_hostif_api_t.__slots__ = [
    'create_hostif',
    'remove_hostif',
    'set_hostif_attribute',
    'get_hostif_attribute',
    'create_hostif_table_entry',
    'remove_hostif_table_entry',
    'set_hostif_table_entry_attribute',
    'get_hostif_table_entry_attribute',
    'create_hostif_trap_group',
    'remove_hostif_trap_group',
    'set_hostif_trap_group_attribute',
    'get_hostif_trap_group_attribute',
    'create_hostif_trap',
    'remove_hostif_trap',
    'set_hostif_trap_attribute',
    'get_hostif_trap_attribute',
    'create_hostif_user_defined_trap',
    'remove_hostif_user_defined_trap',
    'set_hostif_user_defined_trap_attribute',
    'get_hostif_user_defined_trap_attribute',
    'recv_hostif_packet',
    'send_hostif_packet',
    'allocate_hostif_packet',
    'free_hostif_packet',
]
struct__sai_hostif_api_t._fields_ = [
    ('create_hostif', sai_create_hostif_fn),
    ('remove_hostif', sai_remove_hostif_fn),
    ('set_hostif_attribute', sai_set_hostif_attribute_fn),
    ('get_hostif_attribute', sai_get_hostif_attribute_fn),
    ('create_hostif_table_entry', sai_create_hostif_table_entry_fn),
    ('remove_hostif_table_entry', sai_remove_hostif_table_entry_fn),
    ('set_hostif_table_entry_attribute', sai_set_hostif_table_entry_attribute_fn),
    ('get_hostif_table_entry_attribute', sai_get_hostif_table_entry_attribute_fn),
    ('create_hostif_trap_group', sai_create_hostif_trap_group_fn),
    ('remove_hostif_trap_group', sai_remove_hostif_trap_group_fn),
    ('set_hostif_trap_group_attribute', sai_set_hostif_trap_group_attribute_fn),
    ('get_hostif_trap_group_attribute', sai_get_hostif_trap_group_attribute_fn),
    ('create_hostif_trap', sai_create_hostif_trap_fn),
    ('remove_hostif_trap', sai_remove_hostif_trap_fn),
    ('set_hostif_trap_attribute', sai_set_hostif_trap_attribute_fn),
    ('get_hostif_trap_attribute', sai_get_hostif_trap_attribute_fn),
    ('create_hostif_user_defined_trap', sai_create_hostif_user_defined_trap_fn),
    ('remove_hostif_user_defined_trap', sai_remove_hostif_user_defined_trap_fn),
    ('set_hostif_user_defined_trap_attribute', sai_set_hostif_user_defined_trap_attribute_fn),
    ('get_hostif_user_defined_trap_attribute', sai_get_hostif_user_defined_trap_attribute_fn),
    ('recv_hostif_packet', sai_recv_hostif_packet_fn),
    ('send_hostif_packet', sai_send_hostif_packet_fn),
    ('allocate_hostif_packet', sai_allocate_hostif_packet_fn),
    ('free_hostif_packet', sai_free_hostif_packet_fn),
]

sai_hostif_api_t = struct__sai_hostif_api_t# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 1453

enum__sai_ipmc_group_attr_t = c_int# /home/bluecmd/Downloads/SAI/inc/saiipmcgroup.h: 74

SAI_IPMC_GROUP_ATTR_START = 0# /home/bluecmd/Downloads/SAI/inc/saiipmcgroup.h: 74

SAI_IPMC_GROUP_ATTR_IPMC_OUTPUT_COUNT = SAI_IPMC_GROUP_ATTR_START# /home/bluecmd/Downloads/SAI/inc/saiipmcgroup.h: 74

SAI_IPMC_GROUP_ATTR_IPMC_MEMBER_LIST = (SAI_IPMC_GROUP_ATTR_IPMC_OUTPUT_COUNT + 1)# /home/bluecmd/Downloads/SAI/inc/saiipmcgroup.h: 74

SAI_IPMC_GROUP_ATTR_END = (SAI_IPMC_GROUP_ATTR_IPMC_MEMBER_LIST + 1)# /home/bluecmd/Downloads/SAI/inc/saiipmcgroup.h: 74

SAI_IPMC_GROUP_ATTR_CUSTOM_RANGE_START = 0x10000000# /home/bluecmd/Downloads/SAI/inc/saiipmcgroup.h: 74

SAI_IPMC_GROUP_ATTR_CUSTOM_RANGE_END = (SAI_IPMC_GROUP_ATTR_CUSTOM_RANGE_START + 1)# /home/bluecmd/Downloads/SAI/inc/saiipmcgroup.h: 74

sai_ipmc_group_attr_t = enum__sai_ipmc_group_attr_t# /home/bluecmd/Downloads/SAI/inc/saiipmcgroup.h: 74

enum__sai_ipmc_group_member_attr_t = c_int# /home/bluecmd/Downloads/SAI/inc/saiipmcgroup.h: 112

SAI_IPMC_GROUP_MEMBER_ATTR_START = 0# /home/bluecmd/Downloads/SAI/inc/saiipmcgroup.h: 112

SAI_IPMC_GROUP_MEMBER_ATTR_IPMC_GROUP_ID = SAI_IPMC_GROUP_MEMBER_ATTR_START# /home/bluecmd/Downloads/SAI/inc/saiipmcgroup.h: 112

SAI_IPMC_GROUP_MEMBER_ATTR_IPMC_OUTPUT_ID = (SAI_IPMC_GROUP_MEMBER_ATTR_IPMC_GROUP_ID + 1)# /home/bluecmd/Downloads/SAI/inc/saiipmcgroup.h: 112

SAI_IPMC_GROUP_MEMBER_ATTR_END = (SAI_IPMC_GROUP_MEMBER_ATTR_IPMC_OUTPUT_ID + 1)# /home/bluecmd/Downloads/SAI/inc/saiipmcgroup.h: 112

SAI_IPMC_GROUP_MEMBER_ATTR_CUSTOM_RANGE_START = 0x10000000# /home/bluecmd/Downloads/SAI/inc/saiipmcgroup.h: 112

SAI_IPMC_GROUP_MEMBER_ATTR_CUSTOM_RANGE_END = (SAI_IPMC_GROUP_MEMBER_ATTR_CUSTOM_RANGE_START + 1)# /home/bluecmd/Downloads/SAI/inc/saiipmcgroup.h: 112

sai_ipmc_group_member_attr_t = enum__sai_ipmc_group_member_attr_t# /home/bluecmd/Downloads/SAI/inc/saiipmcgroup.h: 112

sai_create_ipmc_group_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saiipmcgroup.h: 124

sai_remove_ipmc_group_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t)# /home/bluecmd/Downloads/SAI/inc/saiipmcgroup.h: 137

sai_set_ipmc_group_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saiipmcgroup.h: 148

sai_get_ipmc_group_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saiipmcgroup.h: 161

sai_create_ipmc_group_member_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saiipmcgroup.h: 176

sai_remove_ipmc_group_member_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t)# /home/bluecmd/Downloads/SAI/inc/saiipmcgroup.h: 189

sai_set_ipmc_group_member_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saiipmcgroup.h: 200

sai_get_ipmc_group_member_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saiipmcgroup.h: 213

# /home/bluecmd/Downloads/SAI/inc/saiipmcgroup.h: 232
class struct__sai_ipmc_group_api_t(Structure):
    pass

struct__sai_ipmc_group_api_t.__slots__ = [
    'create_ipmc_group',
    'remove_ipmc_group',
    'set_ipmc_group_attribute',
    'get_ipmc_group_attribute',
    'create_ipmc_group_member',
    'remove_ipmc_group_member',
    'set_ipmc_group_member_attribute',
    'get_ipmc_group_member_attribute',
]
struct__sai_ipmc_group_api_t._fields_ = [
    ('create_ipmc_group', sai_create_ipmc_group_fn),
    ('remove_ipmc_group', sai_remove_ipmc_group_fn),
    ('set_ipmc_group_attribute', sai_set_ipmc_group_attribute_fn),
    ('get_ipmc_group_attribute', sai_get_ipmc_group_attribute_fn),
    ('create_ipmc_group_member', sai_create_ipmc_group_member_fn),
    ('remove_ipmc_group_member', sai_remove_ipmc_group_member_fn),
    ('set_ipmc_group_member_attribute', sai_set_ipmc_group_member_attribute_fn),
    ('get_ipmc_group_member_attribute', sai_get_ipmc_group_member_attribute_fn),
]

sai_ipmc_group_api_t = struct__sai_ipmc_group_api_t# /home/bluecmd/Downloads/SAI/inc/saiipmcgroup.h: 232

enum__sai_ipmc_entry_type_t = c_int# /home/bluecmd/Downloads/SAI/inc/saiipmc.h: 47

SAI_IPMC_ENTRY_TYPE_SG = 0# /home/bluecmd/Downloads/SAI/inc/saiipmc.h: 47

SAI_IPMC_ENTRY_TYPE_XG = (SAI_IPMC_ENTRY_TYPE_SG + 1)# /home/bluecmd/Downloads/SAI/inc/saiipmc.h: 47

sai_ipmc_entry_type_t = enum__sai_ipmc_entry_type_t# /home/bluecmd/Downloads/SAI/inc/saiipmc.h: 47

# /home/bluecmd/Downloads/SAI/inc/saiipmc.h: 76
class struct__sai_ipmc_entry_t(Structure):
    pass

struct__sai_ipmc_entry_t.__slots__ = [
    'switch_id',
    'vr_id',
    'type',
    'destination',
    'source',
]
struct__sai_ipmc_entry_t._fields_ = [
    ('switch_id', sai_object_id_t),
    ('vr_id', sai_object_id_t),
    ('type', sai_ipmc_entry_type_t),
    ('destination', sai_ip_address_t),
    ('source', sai_ip_address_t),
]

sai_ipmc_entry_t = struct__sai_ipmc_entry_t# /home/bluecmd/Downloads/SAI/inc/saiipmc.h: 76

enum__sai_ipmc_entry_attr_t = c_int# /home/bluecmd/Downloads/SAI/inc/saiipmc.h: 146

SAI_IPMC_ENTRY_ATTR_START = 0# /home/bluecmd/Downloads/SAI/inc/saiipmc.h: 146

SAI_IPMC_ENTRY_ATTR_PACKET_ACTION = SAI_IPMC_ENTRY_ATTR_START# /home/bluecmd/Downloads/SAI/inc/saiipmc.h: 146

SAI_IPMC_ENTRY_ATTR_OUTPUT_GROUP_ID = (SAI_IPMC_ENTRY_ATTR_PACKET_ACTION + 1)# /home/bluecmd/Downloads/SAI/inc/saiipmc.h: 146

SAI_IPMC_ENTRY_ATTR_RPF_GROUP_ID = (SAI_IPMC_ENTRY_ATTR_OUTPUT_GROUP_ID + 1)# /home/bluecmd/Downloads/SAI/inc/saiipmc.h: 146

SAI_IPMC_ENTRY_ATTR_COUNTER_ID = (SAI_IPMC_ENTRY_ATTR_RPF_GROUP_ID + 1)# /home/bluecmd/Downloads/SAI/inc/saiipmc.h: 146

SAI_IPMC_ENTRY_ATTR_END = (SAI_IPMC_ENTRY_ATTR_COUNTER_ID + 1)# /home/bluecmd/Downloads/SAI/inc/saiipmc.h: 146

SAI_IPMC_ENTRY_ATTR_CUSTOM_RANGE_START = 0x10000000# /home/bluecmd/Downloads/SAI/inc/saiipmc.h: 146

SAI_IPMC_ENTRY_ATTR_CUSTOM_RANGE_END = (SAI_IPMC_ENTRY_ATTR_CUSTOM_RANGE_START + 1)# /home/bluecmd/Downloads/SAI/inc/saiipmc.h: 146

sai_ipmc_entry_attr_t = enum__sai_ipmc_entry_attr_t# /home/bluecmd/Downloads/SAI/inc/saiipmc.h: 146

sai_create_ipmc_entry_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_ipmc_entry_t), uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saiipmc.h: 157

sai_remove_ipmc_entry_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_ipmc_entry_t))# /home/bluecmd/Downloads/SAI/inc/saiipmc.h: 169

sai_set_ipmc_entry_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_ipmc_entry_t), POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saiipmc.h: 180

sai_get_ipmc_entry_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_ipmc_entry_t), uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saiipmc.h: 193

# /home/bluecmd/Downloads/SAI/inc/saiipmc.h: 208
class struct__sai_ipmc_api_t(Structure):
    pass

struct__sai_ipmc_api_t.__slots__ = [
    'create_ipmc_entry',
    'remove_ipmc_entry',
    'set_ipmc_entry_attribute',
    'get_ipmc_entry_attribute',
]
struct__sai_ipmc_api_t._fields_ = [
    ('create_ipmc_entry', sai_create_ipmc_entry_fn),
    ('remove_ipmc_entry', sai_remove_ipmc_entry_fn),
    ('set_ipmc_entry_attribute', sai_set_ipmc_entry_attribute_fn),
    ('get_ipmc_entry_attribute', sai_get_ipmc_entry_attribute_fn),
]

sai_ipmc_api_t = struct__sai_ipmc_api_t# /home/bluecmd/Downloads/SAI/inc/saiipmc.h: 208

enum__sai_ipsec_direction_t = c_int# /home/bluecmd/Downloads/SAI/inc/saiipsec.h: 44

SAI_IPSEC_DIRECTION_EGRESS = 0# /home/bluecmd/Downloads/SAI/inc/saiipsec.h: 44

SAI_IPSEC_DIRECTION_INGRESS = (SAI_IPSEC_DIRECTION_EGRESS + 1)# /home/bluecmd/Downloads/SAI/inc/saiipsec.h: 44

sai_ipsec_direction_t = enum__sai_ipsec_direction_t# /home/bluecmd/Downloads/SAI/inc/saiipsec.h: 44

enum__sai_ipsec_cipher_t = c_int# /home/bluecmd/Downloads/SAI/inc/saiipsec.h: 55

SAI_IPSEC_CIPHER_AES128_GCM16 = 0# /home/bluecmd/Downloads/SAI/inc/saiipsec.h: 55

SAI_IPSEC_CIPHER_AES256_GCM16 = (SAI_IPSEC_CIPHER_AES128_GCM16 + 1)# /home/bluecmd/Downloads/SAI/inc/saiipsec.h: 55

SAI_IPSEC_CIPHER_AES128_GMAC = (SAI_IPSEC_CIPHER_AES256_GCM16 + 1)# /home/bluecmd/Downloads/SAI/inc/saiipsec.h: 55

SAI_IPSEC_CIPHER_AES256_GMAC = (SAI_IPSEC_CIPHER_AES128_GMAC + 1)# /home/bluecmd/Downloads/SAI/inc/saiipsec.h: 55

sai_ipsec_cipher_t = enum__sai_ipsec_cipher_t# /home/bluecmd/Downloads/SAI/inc/saiipsec.h: 55

enum__sai_ipsec_sa_octet_count_status_t = c_int# /home/bluecmd/Downloads/SAI/inc/saiipsec.h: 71

SAI_IPSEC_SA_OCTET_COUNT_STATUS_BELOW_LOW_WATERMARK = 0# /home/bluecmd/Downloads/SAI/inc/saiipsec.h: 71

SAI_IPSEC_SA_OCTET_COUNT_STATUS_BELOW_HIGH_WATERMARK = (SAI_IPSEC_SA_OCTET_COUNT_STATUS_BELOW_LOW_WATERMARK + 1)# /home/bluecmd/Downloads/SAI/inc/saiipsec.h: 71

SAI_IPSEC_SA_OCTET_COUNT_STATUS_ABOVE_HIGH_WATERMARK = (SAI_IPSEC_SA_OCTET_COUNT_STATUS_BELOW_HIGH_WATERMARK + 1)# /home/bluecmd/Downloads/SAI/inc/saiipsec.h: 71

sai_ipsec_sa_octet_count_status_t = enum__sai_ipsec_sa_octet_count_status_t# /home/bluecmd/Downloads/SAI/inc/saiipsec.h: 71

# /home/bluecmd/Downloads/SAI/inc/saiipsec.h: 95
class struct__sai_ipsec_sa_status_notification_t(Structure):
    pass

struct__sai_ipsec_sa_status_notification_t.__slots__ = [
    'ipsec_sa_id',
    'ipsec_sa_octet_count_status',
    'ipsec_egress_sn_at_max_limit',
]
struct__sai_ipsec_sa_status_notification_t._fields_ = [
    ('ipsec_sa_id', sai_object_id_t),
    ('ipsec_sa_octet_count_status', sai_ipsec_sa_octet_count_status_t),
    ('ipsec_egress_sn_at_max_limit', c_bool),
]

sai_ipsec_sa_status_notification_t = struct__sai_ipsec_sa_status_notification_t# /home/bluecmd/Downloads/SAI/inc/saiipsec.h: 95

enum__sai_ipsec_attr_t = c_int# /home/bluecmd/Downloads/SAI/inc/saiipsec.h: 304

SAI_IPSEC_ATTR_START = 0# /home/bluecmd/Downloads/SAI/inc/saiipsec.h: 304

SAI_IPSEC_ATTR_TERM_REMOTE_IP_MATCH_SUPPORTED = SAI_IPSEC_ATTR_START# /home/bluecmd/Downloads/SAI/inc/saiipsec.h: 304

SAI_IPSEC_ATTR_SWITCHING_MODE_CUT_THROUGH_SUPPORTED = (SAI_IPSEC_ATTR_TERM_REMOTE_IP_MATCH_SUPPORTED + 1)# /home/bluecmd/Downloads/SAI/inc/saiipsec.h: 304

SAI_IPSEC_ATTR_SWITCHING_MODE_STORE_AND_FORWARD_SUPPORTED = (SAI_IPSEC_ATTR_SWITCHING_MODE_CUT_THROUGH_SUPPORTED + 1)# /home/bluecmd/Downloads/SAI/inc/saiipsec.h: 304

SAI_IPSEC_ATTR_STATS_MODE_READ_SUPPORTED = (SAI_IPSEC_ATTR_SWITCHING_MODE_STORE_AND_FORWARD_SUPPORTED + 1)# /home/bluecmd/Downloads/SAI/inc/saiipsec.h: 304

SAI_IPSEC_ATTR_STATS_MODE_READ_CLEAR_SUPPORTED = (SAI_IPSEC_ATTR_STATS_MODE_READ_SUPPORTED + 1)# /home/bluecmd/Downloads/SAI/inc/saiipsec.h: 304

SAI_IPSEC_ATTR_SN_32BIT_SUPPORTED = (SAI_IPSEC_ATTR_STATS_MODE_READ_CLEAR_SUPPORTED + 1)# /home/bluecmd/Downloads/SAI/inc/saiipsec.h: 304

SAI_IPSEC_ATTR_ESN_64BIT_SUPPORTED = (SAI_IPSEC_ATTR_SN_32BIT_SUPPORTED + 1)# /home/bluecmd/Downloads/SAI/inc/saiipsec.h: 304

SAI_IPSEC_ATTR_SUPPORTED_CIPHER_LIST = (SAI_IPSEC_ATTR_ESN_64BIT_SUPPORTED + 1)# /home/bluecmd/Downloads/SAI/inc/saiipsec.h: 304

SAI_IPSEC_ATTR_SYSTEM_SIDE_MTU = (SAI_IPSEC_ATTR_SUPPORTED_CIPHER_LIST + 1)# /home/bluecmd/Downloads/SAI/inc/saiipsec.h: 304

SAI_IPSEC_ATTR_WARM_BOOT_SUPPORTED = (SAI_IPSEC_ATTR_SYSTEM_SIDE_MTU + 1)# /home/bluecmd/Downloads/SAI/inc/saiipsec.h: 304

SAI_IPSEC_ATTR_WARM_BOOT_ENABLE = (SAI_IPSEC_ATTR_WARM_BOOT_SUPPORTED + 1)# /home/bluecmd/Downloads/SAI/inc/saiipsec.h: 304

SAI_IPSEC_ATTR_EXTERNAL_SA_INDEX_ENABLE = (SAI_IPSEC_ATTR_WARM_BOOT_ENABLE + 1)# /home/bluecmd/Downloads/SAI/inc/saiipsec.h: 304

SAI_IPSEC_ATTR_CTAG_TPID = (SAI_IPSEC_ATTR_EXTERNAL_SA_INDEX_ENABLE + 1)# /home/bluecmd/Downloads/SAI/inc/saiipsec.h: 304

SAI_IPSEC_ATTR_STAG_TPID = (SAI_IPSEC_ATTR_CTAG_TPID + 1)# /home/bluecmd/Downloads/SAI/inc/saiipsec.h: 304

SAI_IPSEC_ATTR_MAX_VLAN_TAGS_PARSED = (SAI_IPSEC_ATTR_STAG_TPID + 1)# /home/bluecmd/Downloads/SAI/inc/saiipsec.h: 304

SAI_IPSEC_ATTR_OCTET_COUNT_HIGH_WATERMARK = (SAI_IPSEC_ATTR_MAX_VLAN_TAGS_PARSED + 1)# /home/bluecmd/Downloads/SAI/inc/saiipsec.h: 304

SAI_IPSEC_ATTR_OCTET_COUNT_LOW_WATERMARK = (SAI_IPSEC_ATTR_OCTET_COUNT_HIGH_WATERMARK + 1)# /home/bluecmd/Downloads/SAI/inc/saiipsec.h: 304

SAI_IPSEC_ATTR_STATS_MODE = (SAI_IPSEC_ATTR_OCTET_COUNT_LOW_WATERMARK + 1)# /home/bluecmd/Downloads/SAI/inc/saiipsec.h: 304

SAI_IPSEC_ATTR_AVAILABLE_IPSEC_SA = (SAI_IPSEC_ATTR_STATS_MODE + 1)# /home/bluecmd/Downloads/SAI/inc/saiipsec.h: 304

SAI_IPSEC_ATTR_SA_LIST = (SAI_IPSEC_ATTR_AVAILABLE_IPSEC_SA + 1)# /home/bluecmd/Downloads/SAI/inc/saiipsec.h: 304

SAI_IPSEC_ATTR_END = (SAI_IPSEC_ATTR_SA_LIST + 1)# /home/bluecmd/Downloads/SAI/inc/saiipsec.h: 304

SAI_IPSEC_ATTR_CUSTOM_RANGE_START = 0x10000000# /home/bluecmd/Downloads/SAI/inc/saiipsec.h: 304

SAI_IPSEC_ATTR_CUSTOM_RANGE_END = (SAI_IPSEC_ATTR_CUSTOM_RANGE_START + 1)# /home/bluecmd/Downloads/SAI/inc/saiipsec.h: 304

sai_ipsec_attr_t = enum__sai_ipsec_attr_t# /home/bluecmd/Downloads/SAI/inc/saiipsec.h: 304

enum__sai_ipsec_port_attr_t = c_int# /home/bluecmd/Downloads/SAI/inc/saiipsec.h: 389

SAI_IPSEC_PORT_ATTR_START = 0# /home/bluecmd/Downloads/SAI/inc/saiipsec.h: 389

SAI_IPSEC_PORT_ATTR_PORT_ID = SAI_IPSEC_PORT_ATTR_START# /home/bluecmd/Downloads/SAI/inc/saiipsec.h: 389

SAI_IPSEC_PORT_ATTR_CTAG_ENABLE = (SAI_IPSEC_PORT_ATTR_PORT_ID + 1)# /home/bluecmd/Downloads/SAI/inc/saiipsec.h: 389

SAI_IPSEC_PORT_ATTR_STAG_ENABLE = (SAI_IPSEC_PORT_ATTR_CTAG_ENABLE + 1)# /home/bluecmd/Downloads/SAI/inc/saiipsec.h: 389

SAI_IPSEC_PORT_ATTR_NATIVE_VLAN_ID = (SAI_IPSEC_PORT_ATTR_STAG_ENABLE + 1)# /home/bluecmd/Downloads/SAI/inc/saiipsec.h: 389

SAI_IPSEC_PORT_ATTR_VRF_FROM_PACKET_VLAN_ENABLE = (SAI_IPSEC_PORT_ATTR_NATIVE_VLAN_ID + 1)# /home/bluecmd/Downloads/SAI/inc/saiipsec.h: 389

SAI_IPSEC_PORT_ATTR_SWITCH_SWITCHING_MODE = (SAI_IPSEC_PORT_ATTR_VRF_FROM_PACKET_VLAN_ENABLE + 1)# /home/bluecmd/Downloads/SAI/inc/saiipsec.h: 389

SAI_IPSEC_PORT_ATTR_END = (SAI_IPSEC_PORT_ATTR_SWITCH_SWITCHING_MODE + 1)# /home/bluecmd/Downloads/SAI/inc/saiipsec.h: 389

SAI_IPSEC_PORT_ATTR_CUSTOM_RANGE_START = 0x10000000# /home/bluecmd/Downloads/SAI/inc/saiipsec.h: 389

SAI_IPSEC_PORT_ATTR_CUSTOM_RANGE_END = (SAI_IPSEC_PORT_ATTR_CUSTOM_RANGE_START + 1)# /home/bluecmd/Downloads/SAI/inc/saiipsec.h: 389

sai_ipsec_port_attr_t = enum__sai_ipsec_port_attr_t# /home/bluecmd/Downloads/SAI/inc/saiipsec.h: 389

enum__sai_ipsec_port_stat_t = c_int# /home/bluecmd/Downloads/SAI/inc/saiipsec.h: 427

SAI_IPSEC_PORT_STAT_TX_ERROR_PKTS = 0# /home/bluecmd/Downloads/SAI/inc/saiipsec.h: 427

SAI_IPSEC_PORT_STAT_TX_IPSEC_PKTS = (SAI_IPSEC_PORT_STAT_TX_ERROR_PKTS + 1)# /home/bluecmd/Downloads/SAI/inc/saiipsec.h: 427

SAI_IPSEC_PORT_STAT_TX_NON_IPSEC_PKTS = (SAI_IPSEC_PORT_STAT_TX_IPSEC_PKTS + 1)# /home/bluecmd/Downloads/SAI/inc/saiipsec.h: 427

SAI_IPSEC_PORT_STAT_RX_ERROR_PKTS = (SAI_IPSEC_PORT_STAT_TX_NON_IPSEC_PKTS + 1)# /home/bluecmd/Downloads/SAI/inc/saiipsec.h: 427

SAI_IPSEC_PORT_STAT_RX_IPSEC_PKTS = (SAI_IPSEC_PORT_STAT_RX_ERROR_PKTS + 1)# /home/bluecmd/Downloads/SAI/inc/saiipsec.h: 427

SAI_IPSEC_PORT_STAT_RX_NON_IPSEC_PKTS = (SAI_IPSEC_PORT_STAT_RX_IPSEC_PKTS + 1)# /home/bluecmd/Downloads/SAI/inc/saiipsec.h: 427

sai_ipsec_port_stat_t = enum__sai_ipsec_port_stat_t# /home/bluecmd/Downloads/SAI/inc/saiipsec.h: 427

enum__sai_ipsec_sa_attr_t = c_int# /home/bluecmd/Downloads/SAI/inc/saiipsec.h: 648

SAI_IPSEC_SA_ATTR_START = 0# /home/bluecmd/Downloads/SAI/inc/saiipsec.h: 648

SAI_IPSEC_SA_ATTR_IPSEC_DIRECTION = SAI_IPSEC_SA_ATTR_START# /home/bluecmd/Downloads/SAI/inc/saiipsec.h: 648

SAI_IPSEC_SA_ATTR_IPSEC_ID = (SAI_IPSEC_SA_ATTR_IPSEC_DIRECTION + 1)# /home/bluecmd/Downloads/SAI/inc/saiipsec.h: 648

SAI_IPSEC_SA_ATTR_OCTET_COUNT_STATUS = (SAI_IPSEC_SA_ATTR_IPSEC_ID + 1)# /home/bluecmd/Downloads/SAI/inc/saiipsec.h: 648

SAI_IPSEC_SA_ATTR_EXTERNAL_SA_INDEX = (SAI_IPSEC_SA_ATTR_OCTET_COUNT_STATUS + 1)# /home/bluecmd/Downloads/SAI/inc/saiipsec.h: 648

SAI_IPSEC_SA_ATTR_SA_INDEX = (SAI_IPSEC_SA_ATTR_EXTERNAL_SA_INDEX + 1)# /home/bluecmd/Downloads/SAI/inc/saiipsec.h: 648

SAI_IPSEC_SA_ATTR_IPSEC_PORT_LIST = (SAI_IPSEC_SA_ATTR_SA_INDEX + 1)# /home/bluecmd/Downloads/SAI/inc/saiipsec.h: 648

SAI_IPSEC_SA_ATTR_IPSEC_SPI = (SAI_IPSEC_SA_ATTR_IPSEC_PORT_LIST + 1)# /home/bluecmd/Downloads/SAI/inc/saiipsec.h: 648

SAI_IPSEC_SA_ATTR_IPSEC_ESN_ENABLE = (SAI_IPSEC_SA_ATTR_IPSEC_SPI + 1)# /home/bluecmd/Downloads/SAI/inc/saiipsec.h: 648

SAI_IPSEC_SA_ATTR_IPSEC_CIPHER = (SAI_IPSEC_SA_ATTR_IPSEC_ESN_ENABLE + 1)# /home/bluecmd/Downloads/SAI/inc/saiipsec.h: 648

SAI_IPSEC_SA_ATTR_ENCRYPT_KEY = (SAI_IPSEC_SA_ATTR_IPSEC_CIPHER + 1)# /home/bluecmd/Downloads/SAI/inc/saiipsec.h: 648

SAI_IPSEC_SA_ATTR_SALT = (SAI_IPSEC_SA_ATTR_ENCRYPT_KEY + 1)# /home/bluecmd/Downloads/SAI/inc/saiipsec.h: 648

SAI_IPSEC_SA_ATTR_AUTH_KEY = (SAI_IPSEC_SA_ATTR_SALT + 1)# /home/bluecmd/Downloads/SAI/inc/saiipsec.h: 648

SAI_IPSEC_SA_ATTR_IPSEC_REPLAY_PROTECTION_ENABLE = (SAI_IPSEC_SA_ATTR_AUTH_KEY + 1)# /home/bluecmd/Downloads/SAI/inc/saiipsec.h: 648

SAI_IPSEC_SA_ATTR_IPSEC_REPLAY_PROTECTION_WINDOW = (SAI_IPSEC_SA_ATTR_IPSEC_REPLAY_PROTECTION_ENABLE + 1)# /home/bluecmd/Downloads/SAI/inc/saiipsec.h: 648

SAI_IPSEC_SA_ATTR_TERM_DST_IP = (SAI_IPSEC_SA_ATTR_IPSEC_REPLAY_PROTECTION_WINDOW + 1)# /home/bluecmd/Downloads/SAI/inc/saiipsec.h: 648

SAI_IPSEC_SA_ATTR_TERM_VLAN_ID_ENABLE = (SAI_IPSEC_SA_ATTR_TERM_DST_IP + 1)# /home/bluecmd/Downloads/SAI/inc/saiipsec.h: 648

SAI_IPSEC_SA_ATTR_TERM_VLAN_ID = (SAI_IPSEC_SA_ATTR_TERM_VLAN_ID_ENABLE + 1)# /home/bluecmd/Downloads/SAI/inc/saiipsec.h: 648

SAI_IPSEC_SA_ATTR_TERM_SRC_IP_ENABLE = (SAI_IPSEC_SA_ATTR_TERM_VLAN_ID + 1)# /home/bluecmd/Downloads/SAI/inc/saiipsec.h: 648

SAI_IPSEC_SA_ATTR_TERM_SRC_IP = (SAI_IPSEC_SA_ATTR_TERM_SRC_IP_ENABLE + 1)# /home/bluecmd/Downloads/SAI/inc/saiipsec.h: 648

SAI_IPSEC_SA_ATTR_EGRESS_ESN = (SAI_IPSEC_SA_ATTR_TERM_SRC_IP + 1)# /home/bluecmd/Downloads/SAI/inc/saiipsec.h: 648

SAI_IPSEC_SA_ATTR_MINIMUM_INGRESS_ESN = (SAI_IPSEC_SA_ATTR_EGRESS_ESN + 1)# /home/bluecmd/Downloads/SAI/inc/saiipsec.h: 648

SAI_IPSEC_SA_ATTR_END = (SAI_IPSEC_SA_ATTR_MINIMUM_INGRESS_ESN + 1)# /home/bluecmd/Downloads/SAI/inc/saiipsec.h: 648

SAI_IPSEC_SA_ATTR_CUSTOM_RANGE_START = 0x10000000# /home/bluecmd/Downloads/SAI/inc/saiipsec.h: 648

SAI_IPSEC_SA_ATTR_CUSTOM_RANGE_END = (SAI_IPSEC_SA_ATTR_CUSTOM_RANGE_START + 1)# /home/bluecmd/Downloads/SAI/inc/saiipsec.h: 648

sai_ipsec_sa_attr_t = enum__sai_ipsec_sa_attr_t# /home/bluecmd/Downloads/SAI/inc/saiipsec.h: 648

enum__sai_ipsec_sa_stat_t = c_int# /home/bluecmd/Downloads/SAI/inc/saiipsec.h: 724

SAI_IPSEC_SA_STAT_PROTECTED_OCTETS = 0# /home/bluecmd/Downloads/SAI/inc/saiipsec.h: 724

SAI_IPSEC_SA_STAT_PROTECTED_PKTS = (SAI_IPSEC_SA_STAT_PROTECTED_OCTETS + 1)# /home/bluecmd/Downloads/SAI/inc/saiipsec.h: 724

SAI_IPSEC_SA_STAT_GOOD_PKTS = (SAI_IPSEC_SA_STAT_PROTECTED_PKTS + 1)# /home/bluecmd/Downloads/SAI/inc/saiipsec.h: 724

SAI_IPSEC_SA_STAT_BAD_HEADER_PKTS_IN = (SAI_IPSEC_SA_STAT_GOOD_PKTS + 1)# /home/bluecmd/Downloads/SAI/inc/saiipsec.h: 724

SAI_IPSEC_SA_STAT_REPLAYED_PKTS_IN = (SAI_IPSEC_SA_STAT_BAD_HEADER_PKTS_IN + 1)# /home/bluecmd/Downloads/SAI/inc/saiipsec.h: 724

SAI_IPSEC_SA_STAT_LATE_PKTS_IN = (SAI_IPSEC_SA_STAT_REPLAYED_PKTS_IN + 1)# /home/bluecmd/Downloads/SAI/inc/saiipsec.h: 724

SAI_IPSEC_SA_STAT_BAD_TRAILER_PKTS_IN = (SAI_IPSEC_SA_STAT_LATE_PKTS_IN + 1)# /home/bluecmd/Downloads/SAI/inc/saiipsec.h: 724

SAI_IPSEC_SA_STAT_AUTH_FAIL_PKTS_IN = (SAI_IPSEC_SA_STAT_BAD_TRAILER_PKTS_IN + 1)# /home/bluecmd/Downloads/SAI/inc/saiipsec.h: 724

SAI_IPSEC_SA_STAT_DUMMY_DROPPED_PKTS_IN = (SAI_IPSEC_SA_STAT_AUTH_FAIL_PKTS_IN + 1)# /home/bluecmd/Downloads/SAI/inc/saiipsec.h: 724

SAI_IPSEC_SA_STAT_OTHER_DROPPED_PKTS = (SAI_IPSEC_SA_STAT_DUMMY_DROPPED_PKTS_IN + 1)# /home/bluecmd/Downloads/SAI/inc/saiipsec.h: 724

sai_ipsec_sa_stat_t = enum__sai_ipsec_sa_stat_t# /home/bluecmd/Downloads/SAI/inc/saiipsec.h: 724

sai_create_ipsec_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saiipsec.h: 736

sai_remove_ipsec_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t)# /home/bluecmd/Downloads/SAI/inc/saiipsec.h: 749

sai_set_ipsec_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saiipsec.h: 760

sai_get_ipsec_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saiipsec.h: 773

sai_create_ipsec_port_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saiipsec.h: 788

sai_remove_ipsec_port_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t)# /home/bluecmd/Downloads/SAI/inc/saiipsec.h: 801

sai_set_ipsec_port_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saiipsec.h: 812

sai_get_ipsec_port_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saiipsec.h: 825

sai_get_ipsec_port_stats_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, uint32_t, POINTER(sai_stat_id_t), POINTER(uint64_t))# /home/bluecmd/Downloads/SAI/inc/saiipsec.h: 840

sai_get_ipsec_port_stats_ext_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, uint32_t, POINTER(sai_stat_id_t), sai_stats_mode_t, POINTER(uint64_t))# /home/bluecmd/Downloads/SAI/inc/saiipsec.h: 857

sai_clear_ipsec_port_stats_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, uint32_t, POINTER(sai_stat_id_t))# /home/bluecmd/Downloads/SAI/inc/saiipsec.h: 873

sai_create_ipsec_sa_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saiipsec.h: 888

sai_remove_ipsec_sa_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t)# /home/bluecmd/Downloads/SAI/inc/saiipsec.h: 901

sai_set_ipsec_sa_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saiipsec.h: 912

sai_get_ipsec_sa_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saiipsec.h: 925

sai_get_ipsec_sa_stats_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, uint32_t, POINTER(sai_stat_id_t), POINTER(uint64_t))# /home/bluecmd/Downloads/SAI/inc/saiipsec.h: 940

sai_get_ipsec_sa_stats_ext_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, uint32_t, POINTER(sai_stat_id_t), sai_stats_mode_t, POINTER(uint64_t))# /home/bluecmd/Downloads/SAI/inc/saiipsec.h: 957

sai_clear_ipsec_sa_stats_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, uint32_t, POINTER(sai_stat_id_t))# /home/bluecmd/Downloads/SAI/inc/saiipsec.h: 973

sai_ipsec_sa_status_change_notification_fn = CFUNCTYPE(UNCHECKED(None), uint32_t, POINTER(sai_ipsec_sa_status_notification_t))# /home/bluecmd/Downloads/SAI/inc/saiipsec.h: 988

# /home/bluecmd/Downloads/SAI/inc/saiipsec.h: 1015
class struct__sai_ipsec_api_t(Structure):
    pass

struct__sai_ipsec_api_t.__slots__ = [
    'create_ipsec',
    'remove_ipsec',
    'set_ipsec_attribute',
    'get_ipsec_attribute',
    'create_ipsec_port',
    'remove_ipsec_port',
    'set_ipsec_port_attribute',
    'get_ipsec_port_attribute',
    'get_ipsec_port_stats',
    'get_ipsec_port_stats_ext',
    'clear_ipsec_port_stats',
    'create_ipsec_sa',
    'remove_ipsec_sa',
    'set_ipsec_sa_attribute',
    'get_ipsec_sa_attribute',
    'get_ipsec_sa_stats',
    'get_ipsec_sa_stats_ext',
    'clear_ipsec_sa_stats',
]
struct__sai_ipsec_api_t._fields_ = [
    ('create_ipsec', sai_create_ipsec_fn),
    ('remove_ipsec', sai_remove_ipsec_fn),
    ('set_ipsec_attribute', sai_set_ipsec_attribute_fn),
    ('get_ipsec_attribute', sai_get_ipsec_attribute_fn),
    ('create_ipsec_port', sai_create_ipsec_port_fn),
    ('remove_ipsec_port', sai_remove_ipsec_port_fn),
    ('set_ipsec_port_attribute', sai_set_ipsec_port_attribute_fn),
    ('get_ipsec_port_attribute', sai_get_ipsec_port_attribute_fn),
    ('get_ipsec_port_stats', sai_get_ipsec_port_stats_fn),
    ('get_ipsec_port_stats_ext', sai_get_ipsec_port_stats_ext_fn),
    ('clear_ipsec_port_stats', sai_clear_ipsec_port_stats_fn),
    ('create_ipsec_sa', sai_create_ipsec_sa_fn),
    ('remove_ipsec_sa', sai_remove_ipsec_sa_fn),
    ('set_ipsec_sa_attribute', sai_set_ipsec_sa_attribute_fn),
    ('get_ipsec_sa_attribute', sai_get_ipsec_sa_attribute_fn),
    ('get_ipsec_sa_stats', sai_get_ipsec_sa_stats_fn),
    ('get_ipsec_sa_stats_ext', sai_get_ipsec_sa_stats_ext_fn),
    ('clear_ipsec_sa_stats', sai_clear_ipsec_sa_stats_fn),
]

sai_ipsec_api_t = struct__sai_ipsec_api_t# /home/bluecmd/Downloads/SAI/inc/saiipsec.h: 1015

enum__sai_l2mc_group_attr_t = c_int# /home/bluecmd/Downloads/SAI/inc/sail2mcgroup.h: 74

SAI_L2MC_GROUP_ATTR_START = 0# /home/bluecmd/Downloads/SAI/inc/sail2mcgroup.h: 74

SAI_L2MC_GROUP_ATTR_L2MC_OUTPUT_COUNT = SAI_L2MC_GROUP_ATTR_START# /home/bluecmd/Downloads/SAI/inc/sail2mcgroup.h: 74

SAI_L2MC_GROUP_ATTR_L2MC_MEMBER_LIST = (SAI_L2MC_GROUP_ATTR_L2MC_OUTPUT_COUNT + 1)# /home/bluecmd/Downloads/SAI/inc/sail2mcgroup.h: 74

SAI_L2MC_GROUP_ATTR_END = (SAI_L2MC_GROUP_ATTR_L2MC_MEMBER_LIST + 1)# /home/bluecmd/Downloads/SAI/inc/sail2mcgroup.h: 74

SAI_L2MC_GROUP_ATTR_CUSTOM_RANGE_START = 0x10000000# /home/bluecmd/Downloads/SAI/inc/sail2mcgroup.h: 74

SAI_L2MC_GROUP_ATTR_CUSTOM_RANGE_END = (SAI_L2MC_GROUP_ATTR_CUSTOM_RANGE_START + 1)# /home/bluecmd/Downloads/SAI/inc/sail2mcgroup.h: 74

sai_l2mc_group_attr_t = enum__sai_l2mc_group_attr_t# /home/bluecmd/Downloads/SAI/inc/sail2mcgroup.h: 74

enum__sai_l2mc_group_member_attr_t = c_int# /home/bluecmd/Downloads/SAI/inc/sail2mcgroup.h: 122

SAI_L2MC_GROUP_MEMBER_ATTR_START = 0# /home/bluecmd/Downloads/SAI/inc/sail2mcgroup.h: 122

SAI_L2MC_GROUP_MEMBER_ATTR_L2MC_GROUP_ID = SAI_L2MC_GROUP_MEMBER_ATTR_START# /home/bluecmd/Downloads/SAI/inc/sail2mcgroup.h: 122

SAI_L2MC_GROUP_MEMBER_ATTR_L2MC_OUTPUT_ID = (SAI_L2MC_GROUP_MEMBER_ATTR_L2MC_GROUP_ID + 1)# /home/bluecmd/Downloads/SAI/inc/sail2mcgroup.h: 122

SAI_L2MC_GROUP_MEMBER_ATTR_L2MC_ENDPOINT_IP = (SAI_L2MC_GROUP_MEMBER_ATTR_L2MC_OUTPUT_ID + 1)# /home/bluecmd/Downloads/SAI/inc/sail2mcgroup.h: 122

SAI_L2MC_GROUP_MEMBER_ATTR_END = (SAI_L2MC_GROUP_MEMBER_ATTR_L2MC_ENDPOINT_IP + 1)# /home/bluecmd/Downloads/SAI/inc/sail2mcgroup.h: 122

SAI_L2MC_GROUP_MEMBER_ATTR_CUSTOM_RANGE_START = 0x10000000# /home/bluecmd/Downloads/SAI/inc/sail2mcgroup.h: 122

SAI_L2MC_GROUP_MEMBER_ATTR_CUSTOM_RANGE_END = (SAI_L2MC_GROUP_MEMBER_ATTR_CUSTOM_RANGE_START + 1)# /home/bluecmd/Downloads/SAI/inc/sail2mcgroup.h: 122

sai_l2mc_group_member_attr_t = enum__sai_l2mc_group_member_attr_t# /home/bluecmd/Downloads/SAI/inc/sail2mcgroup.h: 122

sai_create_l2mc_group_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/sail2mcgroup.h: 134

sai_remove_l2mc_group_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t)# /home/bluecmd/Downloads/SAI/inc/sail2mcgroup.h: 147

sai_set_l2mc_group_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/sail2mcgroup.h: 158

sai_get_l2mc_group_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/sail2mcgroup.h: 171

sai_create_l2mc_group_member_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/sail2mcgroup.h: 186

sai_remove_l2mc_group_member_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t)# /home/bluecmd/Downloads/SAI/inc/sail2mcgroup.h: 199

sai_set_l2mc_group_member_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/sail2mcgroup.h: 210

sai_get_l2mc_group_member_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/sail2mcgroup.h: 223

# /home/bluecmd/Downloads/SAI/inc/sail2mcgroup.h: 242
class struct__sai_l2mc_group_api_t(Structure):
    pass

struct__sai_l2mc_group_api_t.__slots__ = [
    'create_l2mc_group',
    'remove_l2mc_group',
    'set_l2mc_group_attribute',
    'get_l2mc_group_attribute',
    'create_l2mc_group_member',
    'remove_l2mc_group_member',
    'set_l2mc_group_member_attribute',
    'get_l2mc_group_member_attribute',
]
struct__sai_l2mc_group_api_t._fields_ = [
    ('create_l2mc_group', sai_create_l2mc_group_fn),
    ('remove_l2mc_group', sai_remove_l2mc_group_fn),
    ('set_l2mc_group_attribute', sai_set_l2mc_group_attribute_fn),
    ('get_l2mc_group_attribute', sai_get_l2mc_group_attribute_fn),
    ('create_l2mc_group_member', sai_create_l2mc_group_member_fn),
    ('remove_l2mc_group_member', sai_remove_l2mc_group_member_fn),
    ('set_l2mc_group_member_attribute', sai_set_l2mc_group_member_attribute_fn),
    ('get_l2mc_group_member_attribute', sai_get_l2mc_group_member_attribute_fn),
]

sai_l2mc_group_api_t = struct__sai_l2mc_group_api_t# /home/bluecmd/Downloads/SAI/inc/sail2mcgroup.h: 242

enum__sai_l2mc_entry_type_t = c_int# /home/bluecmd/Downloads/SAI/inc/sail2mc.h: 47

SAI_L2MC_ENTRY_TYPE_SG = 0# /home/bluecmd/Downloads/SAI/inc/sail2mc.h: 47

SAI_L2MC_ENTRY_TYPE_XG = (SAI_L2MC_ENTRY_TYPE_SG + 1)# /home/bluecmd/Downloads/SAI/inc/sail2mc.h: 47

sai_l2mc_entry_type_t = enum__sai_l2mc_entry_type_t# /home/bluecmd/Downloads/SAI/inc/sail2mc.h: 47

# /home/bluecmd/Downloads/SAI/inc/sail2mc.h: 76
class struct__sai_l2mc_entry_t(Structure):
    pass

struct__sai_l2mc_entry_t.__slots__ = [
    'switch_id',
    'bv_id',
    'type',
    'destination',
    'source',
]
struct__sai_l2mc_entry_t._fields_ = [
    ('switch_id', sai_object_id_t),
    ('bv_id', sai_object_id_t),
    ('type', sai_l2mc_entry_type_t),
    ('destination', sai_ip_address_t),
    ('source', sai_ip_address_t),
]

sai_l2mc_entry_t = struct__sai_l2mc_entry_t# /home/bluecmd/Downloads/SAI/inc/sail2mc.h: 76

enum__sai_l2mc_entry_attr_t = c_int# /home/bluecmd/Downloads/SAI/inc/sail2mc.h: 122

SAI_L2MC_ENTRY_ATTR_START = 0# /home/bluecmd/Downloads/SAI/inc/sail2mc.h: 122

SAI_L2MC_ENTRY_ATTR_PACKET_ACTION = SAI_L2MC_ENTRY_ATTR_START# /home/bluecmd/Downloads/SAI/inc/sail2mc.h: 122

SAI_L2MC_ENTRY_ATTR_OUTPUT_GROUP_ID = (SAI_L2MC_ENTRY_ATTR_PACKET_ACTION + 1)# /home/bluecmd/Downloads/SAI/inc/sail2mc.h: 122

SAI_L2MC_ENTRY_ATTR_END = (SAI_L2MC_ENTRY_ATTR_OUTPUT_GROUP_ID + 1)# /home/bluecmd/Downloads/SAI/inc/sail2mc.h: 122

SAI_L2MC_ENTRY_ATTR_CUSTOM_RANGE_START = 0x10000000# /home/bluecmd/Downloads/SAI/inc/sail2mc.h: 122

SAI_L2MC_ENTRY_ATTR_CUSTOM_RANGE_END = (SAI_L2MC_ENTRY_ATTR_CUSTOM_RANGE_START + 1)# /home/bluecmd/Downloads/SAI/inc/sail2mc.h: 122

sai_l2mc_entry_attr_t = enum__sai_l2mc_entry_attr_t# /home/bluecmd/Downloads/SAI/inc/sail2mc.h: 122

sai_create_l2mc_entry_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_l2mc_entry_t), uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/sail2mc.h: 133

sai_remove_l2mc_entry_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_l2mc_entry_t))# /home/bluecmd/Downloads/SAI/inc/sail2mc.h: 145

sai_set_l2mc_entry_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_l2mc_entry_t), POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/sail2mc.h: 156

sai_get_l2mc_entry_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_l2mc_entry_t), uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/sail2mc.h: 169

# /home/bluecmd/Downloads/SAI/inc/sail2mc.h: 184
class struct__sai_l2mc_api_t(Structure):
    pass

struct__sai_l2mc_api_t.__slots__ = [
    'create_l2mc_entry',
    'remove_l2mc_entry',
    'set_l2mc_entry_attribute',
    'get_l2mc_entry_attribute',
]
struct__sai_l2mc_api_t._fields_ = [
    ('create_l2mc_entry', sai_create_l2mc_entry_fn),
    ('remove_l2mc_entry', sai_remove_l2mc_entry_fn),
    ('set_l2mc_entry_attribute', sai_set_l2mc_entry_attribute_fn),
    ('get_l2mc_entry_attribute', sai_get_l2mc_entry_attribute_fn),
]

sai_l2mc_api_t = struct__sai_l2mc_api_t# /home/bluecmd/Downloads/SAI/inc/sail2mc.h: 184

enum__sai_lag_attr_t = c_int# /home/bluecmd/Downloads/SAI/inc/sailag.h: 217

SAI_LAG_ATTR_START = 0# /home/bluecmd/Downloads/SAI/inc/sailag.h: 217

SAI_LAG_ATTR_PORT_LIST = SAI_LAG_ATTR_START# /home/bluecmd/Downloads/SAI/inc/sailag.h: 217

SAI_LAG_ATTR_INGRESS_ACL = (SAI_LAG_ATTR_PORT_LIST + 1)# /home/bluecmd/Downloads/SAI/inc/sailag.h: 217

SAI_LAG_ATTR_EGRESS_ACL = (SAI_LAG_ATTR_INGRESS_ACL + 1)# /home/bluecmd/Downloads/SAI/inc/sailag.h: 217

SAI_LAG_ATTR_PORT_VLAN_ID = (SAI_LAG_ATTR_EGRESS_ACL + 1)# /home/bluecmd/Downloads/SAI/inc/sailag.h: 217

SAI_LAG_ATTR_DEFAULT_VLAN_PRIORITY = (SAI_LAG_ATTR_PORT_VLAN_ID + 1)# /home/bluecmd/Downloads/SAI/inc/sailag.h: 217

SAI_LAG_ATTR_DROP_UNTAGGED = (SAI_LAG_ATTR_DEFAULT_VLAN_PRIORITY + 1)# /home/bluecmd/Downloads/SAI/inc/sailag.h: 217

SAI_LAG_ATTR_DROP_TAGGED = (SAI_LAG_ATTR_DROP_UNTAGGED + 1)# /home/bluecmd/Downloads/SAI/inc/sailag.h: 217

SAI_LAG_ATTR_TPID = (SAI_LAG_ATTR_DROP_TAGGED + 1)# /home/bluecmd/Downloads/SAI/inc/sailag.h: 217

SAI_LAG_ATTR_SYSTEM_PORT_AGGREGATE_ID = (SAI_LAG_ATTR_TPID + 1)# /home/bluecmd/Downloads/SAI/inc/sailag.h: 217

SAI_LAG_ATTR_LABEL = (SAI_LAG_ATTR_SYSTEM_PORT_AGGREGATE_ID + 1)# /home/bluecmd/Downloads/SAI/inc/sailag.h: 217

SAI_LAG_ATTR_ARS_OBJECT_ID = (SAI_LAG_ATTR_LABEL + 1)# /home/bluecmd/Downloads/SAI/inc/sailag.h: 217

SAI_LAG_ATTR_ARS_PACKET_DROPS = (SAI_LAG_ATTR_ARS_OBJECT_ID + 1)# /home/bluecmd/Downloads/SAI/inc/sailag.h: 217

SAI_LAG_ATTR_ARS_PORT_REASSIGNMENTS = (SAI_LAG_ATTR_ARS_PACKET_DROPS + 1)# /home/bluecmd/Downloads/SAI/inc/sailag.h: 217

SAI_LAG_ATTR_END = (SAI_LAG_ATTR_ARS_PORT_REASSIGNMENTS + 1)# /home/bluecmd/Downloads/SAI/inc/sailag.h: 217

SAI_LAG_ATTR_CUSTOM_RANGE_START = 0x10000000# /home/bluecmd/Downloads/SAI/inc/sailag.h: 217

SAI_LAG_ATTR_CUSTOM_RANGE_END = (SAI_LAG_ATTR_CUSTOM_RANGE_START + 1)# /home/bluecmd/Downloads/SAI/inc/sailag.h: 217

sai_lag_attr_t = enum__sai_lag_attr_t# /home/bluecmd/Downloads/SAI/inc/sailag.h: 217

sai_create_lag_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/sailag.h: 229

sai_remove_lag_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t)# /home/bluecmd/Downloads/SAI/inc/sailag.h: 242

sai_set_lag_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/sailag.h: 253

sai_get_lag_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/sailag.h: 266

enum__sai_lag_member_attr_t = c_int# /home/bluecmd/Downloads/SAI/inc/sailag.h: 328

SAI_LAG_MEMBER_ATTR_START = 0# /home/bluecmd/Downloads/SAI/inc/sailag.h: 328

SAI_LAG_MEMBER_ATTR_LAG_ID = SAI_LAG_MEMBER_ATTR_START# /home/bluecmd/Downloads/SAI/inc/sailag.h: 328

SAI_LAG_MEMBER_ATTR_PORT_ID = (SAI_LAG_MEMBER_ATTR_LAG_ID + 1)# /home/bluecmd/Downloads/SAI/inc/sailag.h: 328

SAI_LAG_MEMBER_ATTR_EGRESS_DISABLE = (SAI_LAG_MEMBER_ATTR_PORT_ID + 1)# /home/bluecmd/Downloads/SAI/inc/sailag.h: 328

SAI_LAG_MEMBER_ATTR_INGRESS_DISABLE = (SAI_LAG_MEMBER_ATTR_EGRESS_DISABLE + 1)# /home/bluecmd/Downloads/SAI/inc/sailag.h: 328

SAI_LAG_MEMBER_ATTR_END = (SAI_LAG_MEMBER_ATTR_INGRESS_DISABLE + 1)# /home/bluecmd/Downloads/SAI/inc/sailag.h: 328

SAI_LAG_MEMBER_ATTR_CUSTOM_RANGE_START = 0x10000000# /home/bluecmd/Downloads/SAI/inc/sailag.h: 328

SAI_LAG_MEMBER_ATTR_CUSTOM_RANGE_END = (SAI_LAG_MEMBER_ATTR_CUSTOM_RANGE_START + 1)# /home/bluecmd/Downloads/SAI/inc/sailag.h: 328

sai_lag_member_attr_t = enum__sai_lag_member_attr_t# /home/bluecmd/Downloads/SAI/inc/sailag.h: 328

sai_create_lag_member_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/sailag.h: 340

sai_remove_lag_member_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t)# /home/bluecmd/Downloads/SAI/inc/sailag.h: 353

sai_set_lag_member_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/sailag.h: 364

sai_get_lag_member_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/sailag.h: 377

# /home/bluecmd/Downloads/SAI/inc/sailag.h: 397
class struct__sai_lag_api_t(Structure):
    pass

struct__sai_lag_api_t.__slots__ = [
    'create_lag',
    'remove_lag',
    'set_lag_attribute',
    'get_lag_attribute',
    'create_lag_member',
    'remove_lag_member',
    'set_lag_member_attribute',
    'get_lag_member_attribute',
    'create_lag_members',
    'remove_lag_members',
]
struct__sai_lag_api_t._fields_ = [
    ('create_lag', sai_create_lag_fn),
    ('remove_lag', sai_remove_lag_fn),
    ('set_lag_attribute', sai_set_lag_attribute_fn),
    ('get_lag_attribute', sai_get_lag_attribute_fn),
    ('create_lag_member', sai_create_lag_member_fn),
    ('remove_lag_member', sai_remove_lag_member_fn),
    ('set_lag_member_attribute', sai_set_lag_member_attribute_fn),
    ('get_lag_member_attribute', sai_get_lag_member_attribute_fn),
    ('create_lag_members', sai_bulk_object_create_fn),
    ('remove_lag_members', sai_bulk_object_remove_fn),
]

sai_lag_api_t = struct__sai_lag_api_t# /home/bluecmd/Downloads/SAI/inc/sailag.h: 397

enum__sai_macsec_direction_t = c_int# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 44

SAI_MACSEC_DIRECTION_EGRESS = 0# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 44

SAI_MACSEC_DIRECTION_INGRESS = (SAI_MACSEC_DIRECTION_EGRESS + 1)# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 44

sai_macsec_direction_t = enum__sai_macsec_direction_t# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 44

enum__sai_macsec_cipher_suite_t = c_int# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 55

SAI_MACSEC_CIPHER_SUITE_GCM_AES_128 = 0# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 55

SAI_MACSEC_CIPHER_SUITE_GCM_AES_256 = (SAI_MACSEC_CIPHER_SUITE_GCM_AES_128 + 1)# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 55

SAI_MACSEC_CIPHER_SUITE_GCM_AES_XPN_128 = (SAI_MACSEC_CIPHER_SUITE_GCM_AES_256 + 1)# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 55

SAI_MACSEC_CIPHER_SUITE_GCM_AES_XPN_256 = (SAI_MACSEC_CIPHER_SUITE_GCM_AES_XPN_128 + 1)# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 55

sai_macsec_cipher_suite_t = enum__sai_macsec_cipher_suite_t# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 55

enum__sai_macsec_max_secure_associations_per_sc_t = c_int# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 68

SAI_MACSEC_MAX_SECURE_ASSOCIATIONS_PER_SC_TWO = 0# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 68

SAI_MACSEC_MAX_SECURE_ASSOCIATIONS_PER_SC_FOUR = (SAI_MACSEC_MAX_SECURE_ASSOCIATIONS_PER_SC_TWO + 1)# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 68

sai_macsec_max_secure_associations_per_sc_t = enum__sai_macsec_max_secure_associations_per_sc_t# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 68

enum__sai_macsec_attr_t = c_int# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 330

SAI_MACSEC_ATTR_START = 0# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 330

SAI_MACSEC_ATTR_DIRECTION = SAI_MACSEC_ATTR_START# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 330

SAI_MACSEC_ATTR_SWITCHING_MODE_CUT_THROUGH_SUPPORTED = (SAI_MACSEC_ATTR_DIRECTION + 1)# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 330

SAI_MACSEC_ATTR_SWITCHING_MODE_STORE_AND_FORWARD_SUPPORTED = (SAI_MACSEC_ATTR_SWITCHING_MODE_CUT_THROUGH_SUPPORTED + 1)# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 330

SAI_MACSEC_ATTR_STATS_MODE_READ_SUPPORTED = (SAI_MACSEC_ATTR_SWITCHING_MODE_STORE_AND_FORWARD_SUPPORTED + 1)# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 330

SAI_MACSEC_ATTR_STATS_MODE_READ_CLEAR_SUPPORTED = (SAI_MACSEC_ATTR_STATS_MODE_READ_SUPPORTED + 1)# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 330

SAI_MACSEC_ATTR_SCI_IN_INGRESS_MACSEC_ACL = (SAI_MACSEC_ATTR_STATS_MODE_READ_CLEAR_SUPPORTED + 1)# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 330

SAI_MACSEC_ATTR_SUPPORTED_CIPHER_SUITE_LIST = (SAI_MACSEC_ATTR_SCI_IN_INGRESS_MACSEC_ACL + 1)# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 330

SAI_MACSEC_ATTR_PN_32BIT_SUPPORTED = (SAI_MACSEC_ATTR_SUPPORTED_CIPHER_SUITE_LIST + 1)# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 330

SAI_MACSEC_ATTR_XPN_64BIT_SUPPORTED = (SAI_MACSEC_ATTR_PN_32BIT_SUPPORTED + 1)# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 330

SAI_MACSEC_ATTR_GCM_AES128_SUPPORTED = (SAI_MACSEC_ATTR_XPN_64BIT_SUPPORTED + 1)# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 330

SAI_MACSEC_ATTR_GCM_AES256_SUPPORTED = (SAI_MACSEC_ATTR_GCM_AES128_SUPPORTED + 1)# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 330

SAI_MACSEC_ATTR_SECTAG_OFFSETS_SUPPORTED = (SAI_MACSEC_ATTR_GCM_AES256_SUPPORTED + 1)# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 330

SAI_MACSEC_ATTR_SYSTEM_SIDE_MTU = (SAI_MACSEC_ATTR_SECTAG_OFFSETS_SUPPORTED + 1)# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 330

SAI_MACSEC_ATTR_WARM_BOOT_SUPPORTED = (SAI_MACSEC_ATTR_SYSTEM_SIDE_MTU + 1)# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 330

SAI_MACSEC_ATTR_WARM_BOOT_ENABLE = (SAI_MACSEC_ATTR_WARM_BOOT_SUPPORTED + 1)# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 330

SAI_MACSEC_ATTR_CTAG_TPID = (SAI_MACSEC_ATTR_WARM_BOOT_ENABLE + 1)# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 330

SAI_MACSEC_ATTR_STAG_TPID = (SAI_MACSEC_ATTR_CTAG_TPID + 1)# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 330

SAI_MACSEC_ATTR_MAX_VLAN_TAGS_PARSED = (SAI_MACSEC_ATTR_STAG_TPID + 1)# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 330

SAI_MACSEC_ATTR_STATS_MODE = (SAI_MACSEC_ATTR_MAX_VLAN_TAGS_PARSED + 1)# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 330

SAI_MACSEC_ATTR_PHYSICAL_BYPASS_ENABLE = (SAI_MACSEC_ATTR_STATS_MODE + 1)# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 330

SAI_MACSEC_ATTR_SUPPORTED_PORT_LIST = (SAI_MACSEC_ATTR_PHYSICAL_BYPASS_ENABLE + 1)# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 330

SAI_MACSEC_ATTR_AVAILABLE_MACSEC_FLOW = (SAI_MACSEC_ATTR_SUPPORTED_PORT_LIST + 1)# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 330

SAI_MACSEC_ATTR_FLOW_LIST = (SAI_MACSEC_ATTR_AVAILABLE_MACSEC_FLOW + 1)# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 330

SAI_MACSEC_ATTR_AVAILABLE_MACSEC_SC = (SAI_MACSEC_ATTR_FLOW_LIST + 1)# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 330

SAI_MACSEC_ATTR_AVAILABLE_MACSEC_SA = (SAI_MACSEC_ATTR_AVAILABLE_MACSEC_SC + 1)# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 330

SAI_MACSEC_ATTR_MAX_SECURE_ASSOCIATIONS_PER_SC = (SAI_MACSEC_ATTR_AVAILABLE_MACSEC_SA + 1)# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 330

SAI_MACSEC_ATTR_END = (SAI_MACSEC_ATTR_MAX_SECURE_ASSOCIATIONS_PER_SC + 1)# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 330

SAI_MACSEC_ATTR_CUSTOM_RANGE_START = 0x10000000# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 330

SAI_MACSEC_ATTR_CUSTOM_RANGE_END = (SAI_MACSEC_ATTR_CUSTOM_RANGE_START + 1)# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 330

sai_macsec_attr_t = enum__sai_macsec_attr_t# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 330

enum__sai_macsec_port_attr_t = c_int# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 402

SAI_MACSEC_PORT_ATTR_START = 0# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 402

SAI_MACSEC_PORT_ATTR_MACSEC_DIRECTION = SAI_MACSEC_PORT_ATTR_START# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 402

SAI_MACSEC_PORT_ATTR_PORT_ID = (SAI_MACSEC_PORT_ATTR_MACSEC_DIRECTION + 1)# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 402

SAI_MACSEC_PORT_ATTR_CTAG_ENABLE = (SAI_MACSEC_PORT_ATTR_PORT_ID + 1)# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 402

SAI_MACSEC_PORT_ATTR_STAG_ENABLE = (SAI_MACSEC_PORT_ATTR_CTAG_ENABLE + 1)# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 402

SAI_MACSEC_PORT_ATTR_SWITCH_SWITCHING_MODE = (SAI_MACSEC_PORT_ATTR_STAG_ENABLE + 1)# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 402

SAI_MACSEC_PORT_ATTR_END = (SAI_MACSEC_PORT_ATTR_SWITCH_SWITCHING_MODE + 1)# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 402

SAI_MACSEC_PORT_ATTR_CUSTOM_RANGE_START = 0x10000000# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 402

SAI_MACSEC_PORT_ATTR_CUSTOM_RANGE_END = (SAI_MACSEC_PORT_ATTR_CUSTOM_RANGE_START + 1)# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 402

sai_macsec_port_attr_t = enum__sai_macsec_port_attr_t# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 402

enum__sai_macsec_port_stat_t = c_int# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 423

SAI_MACSEC_PORT_STAT_PRE_MACSEC_DROP_PKTS = 0# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 423

SAI_MACSEC_PORT_STAT_CONTROL_PKTS = (SAI_MACSEC_PORT_STAT_PRE_MACSEC_DROP_PKTS + 1)# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 423

SAI_MACSEC_PORT_STAT_DATA_PKTS = (SAI_MACSEC_PORT_STAT_CONTROL_PKTS + 1)# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 423

sai_macsec_port_stat_t = enum__sai_macsec_port_stat_t# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 423

enum__sai_macsec_flow_attr_t = c_int# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 475

SAI_MACSEC_FLOW_ATTR_START = 0# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 475

SAI_MACSEC_FLOW_ATTR_MACSEC_DIRECTION = SAI_MACSEC_FLOW_ATTR_START# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 475

SAI_MACSEC_FLOW_ATTR_ACL_ENTRY_LIST = (SAI_MACSEC_FLOW_ATTR_MACSEC_DIRECTION + 1)# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 475

SAI_MACSEC_FLOW_ATTR_SC_LIST = (SAI_MACSEC_FLOW_ATTR_ACL_ENTRY_LIST + 1)# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 475

SAI_MACSEC_FLOW_ATTR_END = (SAI_MACSEC_FLOW_ATTR_SC_LIST + 1)# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 475

SAI_MACSEC_FLOW_ATTR_CUSTOM_RANGE_START = 0x10000000# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 475

SAI_MACSEC_FLOW_ATTR_CUSTOM_RANGE_END = (SAI_MACSEC_FLOW_ATTR_CUSTOM_RANGE_START + 1)# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 475

sai_macsec_flow_attr_t = enum__sai_macsec_flow_attr_t# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 475

enum__sai_macsec_flow_stat_t = c_int# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 584

SAI_MACSEC_FLOW_STAT_OTHER_ERR = 0# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 584

SAI_MACSEC_FLOW_STAT_OCTETS_UNCONTROLLED = (SAI_MACSEC_FLOW_STAT_OTHER_ERR + 1)# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 584

SAI_MACSEC_FLOW_STAT_OCTETS_CONTROLLED = (SAI_MACSEC_FLOW_STAT_OCTETS_UNCONTROLLED + 1)# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 584

SAI_MACSEC_FLOW_STAT_OUT_OCTETS_COMMON = (SAI_MACSEC_FLOW_STAT_OCTETS_CONTROLLED + 1)# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 584

SAI_MACSEC_FLOW_STAT_UCAST_PKTS_UNCONTROLLED = (SAI_MACSEC_FLOW_STAT_OUT_OCTETS_COMMON + 1)# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 584

SAI_MACSEC_FLOW_STAT_UCAST_PKTS_CONTROLLED = (SAI_MACSEC_FLOW_STAT_UCAST_PKTS_UNCONTROLLED + 1)# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 584

SAI_MACSEC_FLOW_STAT_MULTICAST_PKTS_UNCONTROLLED = (SAI_MACSEC_FLOW_STAT_UCAST_PKTS_CONTROLLED + 1)# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 584

SAI_MACSEC_FLOW_STAT_MULTICAST_PKTS_CONTROLLED = (SAI_MACSEC_FLOW_STAT_MULTICAST_PKTS_UNCONTROLLED + 1)# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 584

SAI_MACSEC_FLOW_STAT_BROADCAST_PKTS_UNCONTROLLED = (SAI_MACSEC_FLOW_STAT_MULTICAST_PKTS_CONTROLLED + 1)# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 584

SAI_MACSEC_FLOW_STAT_BROADCAST_PKTS_CONTROLLED = (SAI_MACSEC_FLOW_STAT_BROADCAST_PKTS_UNCONTROLLED + 1)# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 584

SAI_MACSEC_FLOW_STAT_CONTROL_PKTS = (SAI_MACSEC_FLOW_STAT_BROADCAST_PKTS_CONTROLLED + 1)# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 584

SAI_MACSEC_FLOW_STAT_PKTS_UNTAGGED = (SAI_MACSEC_FLOW_STAT_CONTROL_PKTS + 1)# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 584

SAI_MACSEC_FLOW_STAT_IN_TAGGED_CONTROL_PKTS = (SAI_MACSEC_FLOW_STAT_PKTS_UNTAGGED + 1)# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 584

SAI_MACSEC_FLOW_STAT_OUT_PKTS_TOO_LONG = (SAI_MACSEC_FLOW_STAT_IN_TAGGED_CONTROL_PKTS + 1)# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 584

SAI_MACSEC_FLOW_STAT_IN_PKTS_NO_TAG = (SAI_MACSEC_FLOW_STAT_OUT_PKTS_TOO_LONG + 1)# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 584

SAI_MACSEC_FLOW_STAT_IN_PKTS_BAD_TAG = (SAI_MACSEC_FLOW_STAT_IN_PKTS_NO_TAG + 1)# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 584

SAI_MACSEC_FLOW_STAT_IN_PKTS_NO_SCI = (SAI_MACSEC_FLOW_STAT_IN_PKTS_BAD_TAG + 1)# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 584

SAI_MACSEC_FLOW_STAT_IN_PKTS_UNKNOWN_SCI = (SAI_MACSEC_FLOW_STAT_IN_PKTS_NO_SCI + 1)# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 584

SAI_MACSEC_FLOW_STAT_IN_PKTS_OVERRUN = (SAI_MACSEC_FLOW_STAT_IN_PKTS_UNKNOWN_SCI + 1)# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 584

sai_macsec_flow_stat_t = enum__sai_macsec_flow_stat_t# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 584

enum__sai_macsec_sc_attr_t = c_int# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 712

SAI_MACSEC_SC_ATTR_START = 0# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 712

SAI_MACSEC_SC_ATTR_MACSEC_DIRECTION = SAI_MACSEC_SC_ATTR_START# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 712

SAI_MACSEC_SC_ATTR_FLOW_ID = (SAI_MACSEC_SC_ATTR_MACSEC_DIRECTION + 1)# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 712

SAI_MACSEC_SC_ATTR_MACSEC_SCI = (SAI_MACSEC_SC_ATTR_FLOW_ID + 1)# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 712

SAI_MACSEC_SC_ATTR_MACSEC_EXPLICIT_SCI_ENABLE = (SAI_MACSEC_SC_ATTR_MACSEC_SCI + 1)# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 712

SAI_MACSEC_SC_ATTR_MACSEC_SECTAG_OFFSET = (SAI_MACSEC_SC_ATTR_MACSEC_EXPLICIT_SCI_ENABLE + 1)# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 712

SAI_MACSEC_SC_ATTR_ACTIVE_EGRESS_SA_ID = (SAI_MACSEC_SC_ATTR_MACSEC_SECTAG_OFFSET + 1)# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 712

SAI_MACSEC_SC_ATTR_MACSEC_REPLAY_PROTECTION_ENABLE = (SAI_MACSEC_SC_ATTR_ACTIVE_EGRESS_SA_ID + 1)# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 712

SAI_MACSEC_SC_ATTR_MACSEC_REPLAY_PROTECTION_WINDOW = (SAI_MACSEC_SC_ATTR_MACSEC_REPLAY_PROTECTION_ENABLE + 1)# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 712

SAI_MACSEC_SC_ATTR_SA_LIST = (SAI_MACSEC_SC_ATTR_MACSEC_REPLAY_PROTECTION_WINDOW + 1)# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 712

SAI_MACSEC_SC_ATTR_MACSEC_CIPHER_SUITE = (SAI_MACSEC_SC_ATTR_SA_LIST + 1)# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 712

SAI_MACSEC_SC_ATTR_ENCRYPTION_ENABLE = (SAI_MACSEC_SC_ATTR_MACSEC_CIPHER_SUITE + 1)# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 712

SAI_MACSEC_SC_ATTR_END = (SAI_MACSEC_SC_ATTR_ENCRYPTION_ENABLE + 1)# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 712

SAI_MACSEC_SC_ATTR_CUSTOM_RANGE_START = 0x10000000# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 712

SAI_MACSEC_SC_ATTR_CUSTOM_RANGE_END = (SAI_MACSEC_SC_ATTR_CUSTOM_RANGE_START + 1)# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 712

sai_macsec_sc_attr_t = enum__sai_macsec_sc_attr_t# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 712

enum__sai_macsec_sc_stat_t = c_int# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 725

SAI_MACSEC_SC_STAT_SA_NOT_IN_USE = 0# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 725

sai_macsec_sc_stat_t = enum__sai_macsec_sc_stat_t# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 725

enum__sai_macsec_sa_attr_t = c_int# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 853

SAI_MACSEC_SA_ATTR_START = 0# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 853

SAI_MACSEC_SA_ATTR_MACSEC_DIRECTION = SAI_MACSEC_SA_ATTR_START# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 853

SAI_MACSEC_SA_ATTR_SC_ID = (SAI_MACSEC_SA_ATTR_MACSEC_DIRECTION + 1)# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 853

SAI_MACSEC_SA_ATTR_AN = (SAI_MACSEC_SA_ATTR_SC_ID + 1)# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 853

SAI_MACSEC_SA_ATTR_SAK = (SAI_MACSEC_SA_ATTR_AN + 1)# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 853

SAI_MACSEC_SA_ATTR_SALT = (SAI_MACSEC_SA_ATTR_SAK + 1)# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 853

SAI_MACSEC_SA_ATTR_AUTH_KEY = (SAI_MACSEC_SA_ATTR_SALT + 1)# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 853

SAI_MACSEC_SA_ATTR_CONFIGURED_EGRESS_XPN = (SAI_MACSEC_SA_ATTR_AUTH_KEY + 1)# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 853

SAI_MACSEC_SA_ATTR_CURRENT_XPN = (SAI_MACSEC_SA_ATTR_CONFIGURED_EGRESS_XPN + 1)# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 853

SAI_MACSEC_SA_ATTR_XPN = SAI_MACSEC_SA_ATTR_CURRENT_XPN# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 853

SAI_MACSEC_SA_ATTR_MINIMUM_INGRESS_XPN = (SAI_MACSEC_SA_ATTR_XPN + 1)# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 853

SAI_MACSEC_SA_ATTR_MINIMUM_XPN = SAI_MACSEC_SA_ATTR_MINIMUM_INGRESS_XPN# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 853

SAI_MACSEC_SA_ATTR_MACSEC_SSCI = (SAI_MACSEC_SA_ATTR_MINIMUM_XPN + 1)# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 853

SAI_MACSEC_SA_ATTR_END = (SAI_MACSEC_SA_ATTR_MACSEC_SSCI + 1)# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 853

SAI_MACSEC_SA_ATTR_CUSTOM_RANGE_START = 0x10000000# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 853

SAI_MACSEC_SA_ATTR_CUSTOM_RANGE_END = (SAI_MACSEC_SA_ATTR_CUSTOM_RANGE_START + 1)# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 853

sai_macsec_sa_attr_t = enum__sai_macsec_sa_attr_t# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 853

enum__sai_macsec_sa_stat_t = c_int# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 940

SAI_MACSEC_SA_STAT_OCTETS_ENCRYPTED = 0# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 940

SAI_MACSEC_SA_STAT_OCTETS_PROTECTED = (SAI_MACSEC_SA_STAT_OCTETS_ENCRYPTED + 1)# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 940

SAI_MACSEC_SA_STAT_OUT_PKTS_ENCRYPTED = (SAI_MACSEC_SA_STAT_OCTETS_PROTECTED + 1)# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 940

SAI_MACSEC_SA_STAT_OUT_PKTS_PROTECTED = (SAI_MACSEC_SA_STAT_OUT_PKTS_ENCRYPTED + 1)# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 940

SAI_MACSEC_SA_STAT_IN_PKTS_UNCHECKED = (SAI_MACSEC_SA_STAT_OUT_PKTS_PROTECTED + 1)# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 940

SAI_MACSEC_SA_STAT_IN_PKTS_DELAYED = (SAI_MACSEC_SA_STAT_IN_PKTS_UNCHECKED + 1)# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 940

SAI_MACSEC_SA_STAT_IN_PKTS_LATE = (SAI_MACSEC_SA_STAT_IN_PKTS_DELAYED + 1)# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 940

SAI_MACSEC_SA_STAT_IN_PKTS_INVALID = (SAI_MACSEC_SA_STAT_IN_PKTS_LATE + 1)# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 940

SAI_MACSEC_SA_STAT_IN_PKTS_NOT_VALID = (SAI_MACSEC_SA_STAT_IN_PKTS_INVALID + 1)# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 940

SAI_MACSEC_SA_STAT_IN_PKTS_NOT_USING_SA = (SAI_MACSEC_SA_STAT_IN_PKTS_NOT_VALID + 1)# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 940

SAI_MACSEC_SA_STAT_IN_PKTS_UNUSED_SA = (SAI_MACSEC_SA_STAT_IN_PKTS_NOT_USING_SA + 1)# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 940

SAI_MACSEC_SA_STAT_IN_PKTS_OK = (SAI_MACSEC_SA_STAT_IN_PKTS_UNUSED_SA + 1)# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 940

sai_macsec_sa_stat_t = enum__sai_macsec_sa_stat_t# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 940

sai_create_macsec_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 952

sai_remove_macsec_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t)# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 965

sai_set_macsec_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 976

sai_get_macsec_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 989

sai_create_macsec_port_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 1004

sai_remove_macsec_port_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t)# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 1017

sai_set_macsec_port_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 1028

sai_get_macsec_port_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 1041

sai_get_macsec_port_stats_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, uint32_t, POINTER(sai_stat_id_t), POINTER(uint64_t))# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 1056

sai_get_macsec_port_stats_ext_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, uint32_t, POINTER(sai_stat_id_t), sai_stats_mode_t, POINTER(uint64_t))# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 1073

sai_clear_macsec_port_stats_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, uint32_t, POINTER(sai_stat_id_t))# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 1089

sai_create_macsec_flow_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 1104

sai_remove_macsec_flow_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t)# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 1117

sai_set_macsec_flow_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 1128

sai_get_macsec_flow_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 1141

sai_get_macsec_flow_stats_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, uint32_t, POINTER(sai_stat_id_t), POINTER(uint64_t))# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 1156

sai_get_macsec_flow_stats_ext_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, uint32_t, POINTER(sai_stat_id_t), sai_stats_mode_t, POINTER(uint64_t))# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 1173

sai_clear_macsec_flow_stats_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, uint32_t, POINTER(sai_stat_id_t))# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 1189

sai_create_macsec_sc_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 1204

sai_remove_macsec_sc_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t)# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 1217

sai_set_macsec_sc_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 1228

sai_get_macsec_sc_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 1241

sai_get_macsec_sc_stats_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, uint32_t, POINTER(sai_stat_id_t), POINTER(uint64_t))# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 1256

sai_get_macsec_sc_stats_ext_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, uint32_t, POINTER(sai_stat_id_t), sai_stats_mode_t, POINTER(uint64_t))# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 1273

sai_clear_macsec_sc_stats_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, uint32_t, POINTER(sai_stat_id_t))# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 1289

sai_create_macsec_sa_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 1304

sai_remove_macsec_sa_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t)# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 1317

sai_set_macsec_sa_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 1328

sai_get_macsec_sa_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 1341

sai_get_macsec_sa_stats_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, uint32_t, POINTER(sai_stat_id_t), POINTER(uint64_t))# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 1356

sai_get_macsec_sa_stats_ext_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, uint32_t, POINTER(sai_stat_id_t), sai_stats_mode_t, POINTER(uint64_t))# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 1373

sai_clear_macsec_sa_stats_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, uint32_t, POINTER(sai_stat_id_t))# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 1389

# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 1431
class struct__sai_macsec_api_t(Structure):
    pass

struct__sai_macsec_api_t.__slots__ = [
    'create_macsec',
    'remove_macsec',
    'set_macsec_attribute',
    'get_macsec_attribute',
    'create_macsec_port',
    'remove_macsec_port',
    'set_macsec_port_attribute',
    'get_macsec_port_attribute',
    'get_macsec_port_stats',
    'get_macsec_port_stats_ext',
    'clear_macsec_port_stats',
    'create_macsec_flow',
    'remove_macsec_flow',
    'set_macsec_flow_attribute',
    'get_macsec_flow_attribute',
    'get_macsec_flow_stats',
    'get_macsec_flow_stats_ext',
    'clear_macsec_flow_stats',
    'create_macsec_sc',
    'remove_macsec_sc',
    'set_macsec_sc_attribute',
    'get_macsec_sc_attribute',
    'get_macsec_sc_stats',
    'get_macsec_sc_stats_ext',
    'clear_macsec_sc_stats',
    'create_macsec_sa',
    'remove_macsec_sa',
    'set_macsec_sa_attribute',
    'get_macsec_sa_attribute',
    'get_macsec_sa_stats',
    'get_macsec_sa_stats_ext',
    'clear_macsec_sa_stats',
]
struct__sai_macsec_api_t._fields_ = [
    ('create_macsec', sai_create_macsec_fn),
    ('remove_macsec', sai_remove_macsec_fn),
    ('set_macsec_attribute', sai_set_macsec_attribute_fn),
    ('get_macsec_attribute', sai_get_macsec_attribute_fn),
    ('create_macsec_port', sai_create_macsec_port_fn),
    ('remove_macsec_port', sai_remove_macsec_port_fn),
    ('set_macsec_port_attribute', sai_set_macsec_port_attribute_fn),
    ('get_macsec_port_attribute', sai_get_macsec_port_attribute_fn),
    ('get_macsec_port_stats', sai_get_macsec_port_stats_fn),
    ('get_macsec_port_stats_ext', sai_get_macsec_port_stats_ext_fn),
    ('clear_macsec_port_stats', sai_clear_macsec_port_stats_fn),
    ('create_macsec_flow', sai_create_macsec_flow_fn),
    ('remove_macsec_flow', sai_remove_macsec_flow_fn),
    ('set_macsec_flow_attribute', sai_set_macsec_flow_attribute_fn),
    ('get_macsec_flow_attribute', sai_get_macsec_flow_attribute_fn),
    ('get_macsec_flow_stats', sai_get_macsec_flow_stats_fn),
    ('get_macsec_flow_stats_ext', sai_get_macsec_flow_stats_ext_fn),
    ('clear_macsec_flow_stats', sai_clear_macsec_flow_stats_fn),
    ('create_macsec_sc', sai_create_macsec_sc_fn),
    ('remove_macsec_sc', sai_remove_macsec_sc_fn),
    ('set_macsec_sc_attribute', sai_set_macsec_sc_attribute_fn),
    ('get_macsec_sc_attribute', sai_get_macsec_sc_attribute_fn),
    ('get_macsec_sc_stats', sai_get_macsec_sc_stats_fn),
    ('get_macsec_sc_stats_ext', sai_get_macsec_sc_stats_ext_fn),
    ('clear_macsec_sc_stats', sai_clear_macsec_sc_stats_fn),
    ('create_macsec_sa', sai_create_macsec_sa_fn),
    ('remove_macsec_sa', sai_remove_macsec_sa_fn),
    ('set_macsec_sa_attribute', sai_set_macsec_sa_attribute_fn),
    ('get_macsec_sa_attribute', sai_get_macsec_sa_attribute_fn),
    ('get_macsec_sa_stats', sai_get_macsec_sa_stats_fn),
    ('get_macsec_sa_stats_ext', sai_get_macsec_sa_stats_ext_fn),
    ('clear_macsec_sa_stats', sai_clear_macsec_sa_stats_fn),
]

sai_macsec_api_t = struct__sai_macsec_api_t# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 1431

# /home/bluecmd/Downloads/SAI/inc/saimcastfdb.h: 58
class struct__sai_mcast_fdb_entry_t(Structure):
    pass

struct__sai_mcast_fdb_entry_t.__slots__ = [
    'switch_id',
    'mac_address',
    'bv_id',
]
struct__sai_mcast_fdb_entry_t._fields_ = [
    ('switch_id', sai_object_id_t),
    ('mac_address', sai_mac_t),
    ('bv_id', sai_object_id_t),
]

sai_mcast_fdb_entry_t = struct__sai_mcast_fdb_entry_t# /home/bluecmd/Downloads/SAI/inc/saimcastfdb.h: 58

enum__sai_mcast_fdb_entry_attr_t = c_int# /home/bluecmd/Downloads/SAI/inc/saimcastfdb.h: 112

SAI_MCAST_FDB_ENTRY_ATTR_START = 0# /home/bluecmd/Downloads/SAI/inc/saimcastfdb.h: 112

SAI_MCAST_FDB_ENTRY_ATTR_GROUP_ID = SAI_MCAST_FDB_ENTRY_ATTR_START# /home/bluecmd/Downloads/SAI/inc/saimcastfdb.h: 112

SAI_MCAST_FDB_ENTRY_ATTR_PACKET_ACTION = (SAI_MCAST_FDB_ENTRY_ATTR_GROUP_ID + 1)# /home/bluecmd/Downloads/SAI/inc/saimcastfdb.h: 112

SAI_MCAST_FDB_ENTRY_ATTR_META_DATA = (SAI_MCAST_FDB_ENTRY_ATTR_PACKET_ACTION + 1)# /home/bluecmd/Downloads/SAI/inc/saimcastfdb.h: 112

SAI_MCAST_FDB_ENTRY_ATTR_END = (SAI_MCAST_FDB_ENTRY_ATTR_META_DATA + 1)# /home/bluecmd/Downloads/SAI/inc/saimcastfdb.h: 112

SAI_MCAST_FDB_ENTRY_ATTR_CUSTOM_RANGE_START = 0x10000000# /home/bluecmd/Downloads/SAI/inc/saimcastfdb.h: 112

SAI_MCAST_FDB_ENTRY_ATTR_CUSTOM_RANGE_END = (SAI_MCAST_FDB_ENTRY_ATTR_CUSTOM_RANGE_START + 1)# /home/bluecmd/Downloads/SAI/inc/saimcastfdb.h: 112

sai_mcast_fdb_entry_attr_t = enum__sai_mcast_fdb_entry_attr_t# /home/bluecmd/Downloads/SAI/inc/saimcastfdb.h: 112

sai_create_mcast_fdb_entry_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_mcast_fdb_entry_t), uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saimcastfdb.h: 123

sai_remove_mcast_fdb_entry_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_mcast_fdb_entry_t))# /home/bluecmd/Downloads/SAI/inc/saimcastfdb.h: 135

sai_set_mcast_fdb_entry_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_mcast_fdb_entry_t), POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saimcastfdb.h: 146

sai_get_mcast_fdb_entry_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_mcast_fdb_entry_t), uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saimcastfdb.h: 159

# /home/bluecmd/Downloads/SAI/inc/saimcastfdb.h: 174
class struct__sai_mcast_fdb_api_t(Structure):
    pass

struct__sai_mcast_fdb_api_t.__slots__ = [
    'create_mcast_fdb_entry',
    'remove_mcast_fdb_entry',
    'set_mcast_fdb_entry_attribute',
    'get_mcast_fdb_entry_attribute',
]
struct__sai_mcast_fdb_api_t._fields_ = [
    ('create_mcast_fdb_entry', sai_create_mcast_fdb_entry_fn),
    ('remove_mcast_fdb_entry', sai_remove_mcast_fdb_entry_fn),
    ('set_mcast_fdb_entry_attribute', sai_set_mcast_fdb_entry_attribute_fn),
    ('get_mcast_fdb_entry_attribute', sai_get_mcast_fdb_entry_attribute_fn),
]

sai_mcast_fdb_api_t = struct__sai_mcast_fdb_api_t# /home/bluecmd/Downloads/SAI/inc/saimcastfdb.h: 174

enum__sai_mirror_session_type_t = c_int# /home/bluecmd/Downloads/SAI/inc/saimirror.h: 53

SAI_MIRROR_SESSION_TYPE_LOCAL = 0# /home/bluecmd/Downloads/SAI/inc/saimirror.h: 53

SAI_MIRROR_SESSION_TYPE_REMOTE = (SAI_MIRROR_SESSION_TYPE_LOCAL + 1)# /home/bluecmd/Downloads/SAI/inc/saimirror.h: 53

SAI_MIRROR_SESSION_TYPE_ENHANCED_REMOTE = (SAI_MIRROR_SESSION_TYPE_REMOTE + 1)# /home/bluecmd/Downloads/SAI/inc/saimirror.h: 53

SAI_MIRROR_SESSION_TYPE_SFLOW = (SAI_MIRROR_SESSION_TYPE_ENHANCED_REMOTE + 1)# /home/bluecmd/Downloads/SAI/inc/saimirror.h: 53

sai_mirror_session_type_t = enum__sai_mirror_session_type_t# /home/bluecmd/Downloads/SAI/inc/saimirror.h: 53

enum__sai_erspan_encapsulation_type_t = c_int# /home/bluecmd/Downloads/SAI/inc/saimirror.h: 65

SAI_ERSPAN_ENCAPSULATION_TYPE_MIRROR_L3_GRE_TUNNEL = 0# /home/bluecmd/Downloads/SAI/inc/saimirror.h: 65

sai_erspan_encapsulation_type_t = enum__sai_erspan_encapsulation_type_t# /home/bluecmd/Downloads/SAI/inc/saimirror.h: 65

enum__sai_mirror_session_congestion_mode_t = c_int# /home/bluecmd/Downloads/SAI/inc/saimirror.h: 78

SAI_MIRROR_SESSION_CONGESTION_MODE_INDEPENDENT = 0# /home/bluecmd/Downloads/SAI/inc/saimirror.h: 78

SAI_MIRROR_SESSION_CONGESTION_MODE_CORRELATED = (SAI_MIRROR_SESSION_CONGESTION_MODE_INDEPENDENT + 1)# /home/bluecmd/Downloads/SAI/inc/saimirror.h: 78

sai_mirror_session_congestion_mode_t = enum__sai_mirror_session_congestion_mode_t# /home/bluecmd/Downloads/SAI/inc/saimirror.h: 78

enum__sai_mirror_session_attr_t = c_int# /home/bluecmd/Downloads/SAI/inc/saimirror.h: 376

SAI_MIRROR_SESSION_ATTR_START = 0# /home/bluecmd/Downloads/SAI/inc/saimirror.h: 376

SAI_MIRROR_SESSION_ATTR_TYPE = SAI_MIRROR_SESSION_ATTR_START# /home/bluecmd/Downloads/SAI/inc/saimirror.h: 376

SAI_MIRROR_SESSION_ATTR_MONITOR_PORT = (SAI_MIRROR_SESSION_ATTR_TYPE + 1)# /home/bluecmd/Downloads/SAI/inc/saimirror.h: 376

SAI_MIRROR_SESSION_ATTR_TRUNCATE_SIZE = (SAI_MIRROR_SESSION_ATTR_MONITOR_PORT + 1)# /home/bluecmd/Downloads/SAI/inc/saimirror.h: 376

SAI_MIRROR_SESSION_ATTR_SAMPLE_RATE = (SAI_MIRROR_SESSION_ATTR_TRUNCATE_SIZE + 1)# /home/bluecmd/Downloads/SAI/inc/saimirror.h: 376

SAI_MIRROR_SESSION_ATTR_CONGESTION_MODE = (SAI_MIRROR_SESSION_ATTR_SAMPLE_RATE + 1)# /home/bluecmd/Downloads/SAI/inc/saimirror.h: 376

SAI_MIRROR_SESSION_ATTR_TC = (SAI_MIRROR_SESSION_ATTR_CONGESTION_MODE + 1)# /home/bluecmd/Downloads/SAI/inc/saimirror.h: 376

SAI_MIRROR_SESSION_ATTR_VLAN_TPID = (SAI_MIRROR_SESSION_ATTR_TC + 1)# /home/bluecmd/Downloads/SAI/inc/saimirror.h: 376

SAI_MIRROR_SESSION_ATTR_VLAN_ID = (SAI_MIRROR_SESSION_ATTR_VLAN_TPID + 1)# /home/bluecmd/Downloads/SAI/inc/saimirror.h: 376

SAI_MIRROR_SESSION_ATTR_VLAN_PRI = (SAI_MIRROR_SESSION_ATTR_VLAN_ID + 1)# /home/bluecmd/Downloads/SAI/inc/saimirror.h: 376

SAI_MIRROR_SESSION_ATTR_VLAN_CFI = (SAI_MIRROR_SESSION_ATTR_VLAN_PRI + 1)# /home/bluecmd/Downloads/SAI/inc/saimirror.h: 376

SAI_MIRROR_SESSION_ATTR_VLAN_HEADER_VALID = (SAI_MIRROR_SESSION_ATTR_VLAN_CFI + 1)# /home/bluecmd/Downloads/SAI/inc/saimirror.h: 376

SAI_MIRROR_SESSION_ATTR_ERSPAN_ENCAPSULATION_TYPE = (SAI_MIRROR_SESSION_ATTR_VLAN_HEADER_VALID + 1)# /home/bluecmd/Downloads/SAI/inc/saimirror.h: 376

SAI_MIRROR_SESSION_ATTR_IPHDR_VERSION = (SAI_MIRROR_SESSION_ATTR_ERSPAN_ENCAPSULATION_TYPE + 1)# /home/bluecmd/Downloads/SAI/inc/saimirror.h: 376

SAI_MIRROR_SESSION_ATTR_TOS = (SAI_MIRROR_SESSION_ATTR_IPHDR_VERSION + 1)# /home/bluecmd/Downloads/SAI/inc/saimirror.h: 376

SAI_MIRROR_SESSION_ATTR_TTL = (SAI_MIRROR_SESSION_ATTR_TOS + 1)# /home/bluecmd/Downloads/SAI/inc/saimirror.h: 376

SAI_MIRROR_SESSION_ATTR_SRC_IP_ADDRESS = (SAI_MIRROR_SESSION_ATTR_TTL + 1)# /home/bluecmd/Downloads/SAI/inc/saimirror.h: 376

SAI_MIRROR_SESSION_ATTR_DST_IP_ADDRESS = (SAI_MIRROR_SESSION_ATTR_SRC_IP_ADDRESS + 1)# /home/bluecmd/Downloads/SAI/inc/saimirror.h: 376

SAI_MIRROR_SESSION_ATTR_SRC_MAC_ADDRESS = (SAI_MIRROR_SESSION_ATTR_DST_IP_ADDRESS + 1)# /home/bluecmd/Downloads/SAI/inc/saimirror.h: 376

SAI_MIRROR_SESSION_ATTR_DST_MAC_ADDRESS = (SAI_MIRROR_SESSION_ATTR_SRC_MAC_ADDRESS + 1)# /home/bluecmd/Downloads/SAI/inc/saimirror.h: 376

SAI_MIRROR_SESSION_ATTR_GRE_PROTOCOL_TYPE = (SAI_MIRROR_SESSION_ATTR_DST_MAC_ADDRESS + 1)# /home/bluecmd/Downloads/SAI/inc/saimirror.h: 376

SAI_MIRROR_SESSION_ATTR_MONITOR_PORTLIST_VALID = (SAI_MIRROR_SESSION_ATTR_GRE_PROTOCOL_TYPE + 1)# /home/bluecmd/Downloads/SAI/inc/saimirror.h: 376

SAI_MIRROR_SESSION_ATTR_MONITOR_PORTLIST = (SAI_MIRROR_SESSION_ATTR_MONITOR_PORTLIST_VALID + 1)# /home/bluecmd/Downloads/SAI/inc/saimirror.h: 376

SAI_MIRROR_SESSION_ATTR_POLICER = (SAI_MIRROR_SESSION_ATTR_MONITOR_PORTLIST + 1)# /home/bluecmd/Downloads/SAI/inc/saimirror.h: 376

SAI_MIRROR_SESSION_ATTR_UDP_SRC_PORT = (SAI_MIRROR_SESSION_ATTR_POLICER + 1)# /home/bluecmd/Downloads/SAI/inc/saimirror.h: 376

SAI_MIRROR_SESSION_ATTR_UDP_DST_PORT = (SAI_MIRROR_SESSION_ATTR_UDP_SRC_PORT + 1)# /home/bluecmd/Downloads/SAI/inc/saimirror.h: 376

SAI_MIRROR_SESSION_ATTR_COUNTER_ID = (SAI_MIRROR_SESSION_ATTR_UDP_DST_PORT + 1)# /home/bluecmd/Downloads/SAI/inc/saimirror.h: 376

SAI_MIRROR_SESSION_ATTR_END = (SAI_MIRROR_SESSION_ATTR_COUNTER_ID + 1)# /home/bluecmd/Downloads/SAI/inc/saimirror.h: 376

SAI_MIRROR_SESSION_ATTR_CUSTOM_RANGE_START = 0x10000000# /home/bluecmd/Downloads/SAI/inc/saimirror.h: 376

SAI_MIRROR_SESSION_ATTR_CUSTOM_RANGE_END = (SAI_MIRROR_SESSION_ATTR_CUSTOM_RANGE_START + 1)# /home/bluecmd/Downloads/SAI/inc/saimirror.h: 376

sai_mirror_session_attr_t = enum__sai_mirror_session_attr_t# /home/bluecmd/Downloads/SAI/inc/saimirror.h: 376

sai_create_mirror_session_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saimirror.h: 389

sai_remove_mirror_session_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t)# /home/bluecmd/Downloads/SAI/inc/saimirror.h: 403

sai_set_mirror_session_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saimirror.h: 415

sai_get_mirror_session_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saimirror.h: 429

# /home/bluecmd/Downloads/SAI/inc/saimirror.h: 444
class struct__sai_mirror_api_t(Structure):
    pass

struct__sai_mirror_api_t.__slots__ = [
    'create_mirror_session',
    'remove_mirror_session',
    'set_mirror_session_attribute',
    'get_mirror_session_attribute',
]
struct__sai_mirror_api_t._fields_ = [
    ('create_mirror_session', sai_create_mirror_session_fn),
    ('remove_mirror_session', sai_remove_mirror_session_fn),
    ('set_mirror_session_attribute', sai_set_mirror_session_attribute_fn),
    ('get_mirror_session_attribute', sai_get_mirror_session_attribute_fn),
]

sai_mirror_api_t = struct__sai_mirror_api_t# /home/bluecmd/Downloads/SAI/inc/saimirror.h: 444

enum__sai_inseg_entry_psc_type_t = c_int# /home/bluecmd/Downloads/SAI/inc/saimpls.h: 46

SAI_INSEG_ENTRY_PSC_TYPE_ELSP = 0# /home/bluecmd/Downloads/SAI/inc/saimpls.h: 46

SAI_INSEG_ENTRY_PSC_TYPE_LLSP = (SAI_INSEG_ENTRY_PSC_TYPE_ELSP + 1)# /home/bluecmd/Downloads/SAI/inc/saimpls.h: 46

sai_inseg_entry_psc_type_t = enum__sai_inseg_entry_psc_type_t# /home/bluecmd/Downloads/SAI/inc/saimpls.h: 46

enum__sai_inseg_entry_pop_ttl_mode_t = c_int# /home/bluecmd/Downloads/SAI/inc/saimpls.h: 63

SAI_INSEG_ENTRY_POP_TTL_MODE_UNIFORM = 0# /home/bluecmd/Downloads/SAI/inc/saimpls.h: 63

SAI_INSEG_ENTRY_POP_TTL_MODE_PIPE = (SAI_INSEG_ENTRY_POP_TTL_MODE_UNIFORM + 1)# /home/bluecmd/Downloads/SAI/inc/saimpls.h: 63

sai_inseg_entry_pop_ttl_mode_t = enum__sai_inseg_entry_pop_ttl_mode_t# /home/bluecmd/Downloads/SAI/inc/saimpls.h: 63

enum__sai_inseg_entry_pop_qos_mode_t = c_int# /home/bluecmd/Downloads/SAI/inc/saimpls.h: 80

SAI_INSEG_ENTRY_POP_QOS_MODE_UNIFORM = 0# /home/bluecmd/Downloads/SAI/inc/saimpls.h: 80

SAI_INSEG_ENTRY_POP_QOS_MODE_PIPE = (SAI_INSEG_ENTRY_POP_QOS_MODE_UNIFORM + 1)# /home/bluecmd/Downloads/SAI/inc/saimpls.h: 80

sai_inseg_entry_pop_qos_mode_t = enum__sai_inseg_entry_pop_qos_mode_t# /home/bluecmd/Downloads/SAI/inc/saimpls.h: 80

enum__sai_inseg_entry_attr_t = c_int# /home/bluecmd/Downloads/SAI/inc/saimpls.h: 226

SAI_INSEG_ENTRY_ATTR_START = 0# /home/bluecmd/Downloads/SAI/inc/saimpls.h: 226

SAI_INSEG_ENTRY_ATTR_NUM_OF_POP = SAI_INSEG_ENTRY_ATTR_START# /home/bluecmd/Downloads/SAI/inc/saimpls.h: 226

SAI_INSEG_ENTRY_ATTR_PACKET_ACTION = (SAI_INSEG_ENTRY_ATTR_NUM_OF_POP + 1)# /home/bluecmd/Downloads/SAI/inc/saimpls.h: 226

SAI_INSEG_ENTRY_ATTR_TRAP_PRIORITY = (SAI_INSEG_ENTRY_ATTR_PACKET_ACTION + 1)# /home/bluecmd/Downloads/SAI/inc/saimpls.h: 226

SAI_INSEG_ENTRY_ATTR_NEXT_HOP_ID = (SAI_INSEG_ENTRY_ATTR_TRAP_PRIORITY + 1)# /home/bluecmd/Downloads/SAI/inc/saimpls.h: 226

SAI_INSEG_ENTRY_ATTR_PSC_TYPE = (SAI_INSEG_ENTRY_ATTR_NEXT_HOP_ID + 1)# /home/bluecmd/Downloads/SAI/inc/saimpls.h: 226

SAI_INSEG_ENTRY_ATTR_QOS_TC = (SAI_INSEG_ENTRY_ATTR_PSC_TYPE + 1)# /home/bluecmd/Downloads/SAI/inc/saimpls.h: 226

SAI_INSEG_ENTRY_ATTR_MPLS_EXP_TO_TC_MAP = (SAI_INSEG_ENTRY_ATTR_QOS_TC + 1)# /home/bluecmd/Downloads/SAI/inc/saimpls.h: 226

SAI_INSEG_ENTRY_ATTR_MPLS_EXP_TO_COLOR_MAP = (SAI_INSEG_ENTRY_ATTR_MPLS_EXP_TO_TC_MAP + 1)# /home/bluecmd/Downloads/SAI/inc/saimpls.h: 226

SAI_INSEG_ENTRY_ATTR_POP_TTL_MODE = (SAI_INSEG_ENTRY_ATTR_MPLS_EXP_TO_COLOR_MAP + 1)# /home/bluecmd/Downloads/SAI/inc/saimpls.h: 226

SAI_INSEG_ENTRY_ATTR_POP_QOS_MODE = (SAI_INSEG_ENTRY_ATTR_POP_TTL_MODE + 1)# /home/bluecmd/Downloads/SAI/inc/saimpls.h: 226

SAI_INSEG_ENTRY_ATTR_COUNTER_ID = (SAI_INSEG_ENTRY_ATTR_POP_QOS_MODE + 1)# /home/bluecmd/Downloads/SAI/inc/saimpls.h: 226

SAI_INSEG_ENTRY_ATTR_END = (SAI_INSEG_ENTRY_ATTR_COUNTER_ID + 1)# /home/bluecmd/Downloads/SAI/inc/saimpls.h: 226

SAI_INSEG_ENTRY_ATTR_CUSTOM_RANGE_START = 0x10000000# /home/bluecmd/Downloads/SAI/inc/saimpls.h: 226

SAI_INSEG_ENTRY_ATTR_CUSTOM_RANGE_END = (SAI_INSEG_ENTRY_ATTR_CUSTOM_RANGE_START + 1)# /home/bluecmd/Downloads/SAI/inc/saimpls.h: 226

sai_inseg_entry_attr_t = enum__sai_inseg_entry_attr_t# /home/bluecmd/Downloads/SAI/inc/saimpls.h: 226

# /home/bluecmd/Downloads/SAI/inc/saimpls.h: 245
class struct__sai_inseg_entry_t(Structure):
    pass

struct__sai_inseg_entry_t.__slots__ = [
    'switch_id',
    'label',
]
struct__sai_inseg_entry_t._fields_ = [
    ('switch_id', sai_object_id_t),
    ('label', sai_label_id_t),
]

sai_inseg_entry_t = struct__sai_inseg_entry_t# /home/bluecmd/Downloads/SAI/inc/saimpls.h: 245

sai_create_inseg_entry_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_inseg_entry_t), uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saimpls.h: 256

sai_remove_inseg_entry_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_inseg_entry_t))# /home/bluecmd/Downloads/SAI/inc/saimpls.h: 268

sai_set_inseg_entry_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_inseg_entry_t), POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saimpls.h: 279

sai_get_inseg_entry_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_inseg_entry_t), uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saimpls.h: 292

sai_bulk_create_inseg_entry_fn = CFUNCTYPE(UNCHECKED(sai_status_t), uint32_t, POINTER(sai_inseg_entry_t), POINTER(uint32_t), POINTER(POINTER(sai_attribute_t)), sai_bulk_op_error_mode_t, POINTER(sai_status_t))# /home/bluecmd/Downloads/SAI/inc/saimpls.h: 314

sai_bulk_remove_inseg_entry_fn = CFUNCTYPE(UNCHECKED(sai_status_t), uint32_t, POINTER(sai_inseg_entry_t), sai_bulk_op_error_mode_t, POINTER(sai_status_t))# /home/bluecmd/Downloads/SAI/inc/saimpls.h: 336

sai_bulk_set_inseg_entry_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), uint32_t, POINTER(sai_inseg_entry_t), POINTER(sai_attribute_t), sai_bulk_op_error_mode_t, POINTER(sai_status_t))# /home/bluecmd/Downloads/SAI/inc/saimpls.h: 357

sai_bulk_get_inseg_entry_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), uint32_t, POINTER(sai_inseg_entry_t), POINTER(uint32_t), POINTER(POINTER(sai_attribute_t)), sai_bulk_op_error_mode_t, POINTER(sai_status_t))# /home/bluecmd/Downloads/SAI/inc/saimpls.h: 381

# /home/bluecmd/Downloads/SAI/inc/saimpls.h: 404
class struct__sai_mpls_api_t(Structure):
    pass

struct__sai_mpls_api_t.__slots__ = [
    'create_inseg_entry',
    'remove_inseg_entry',
    'set_inseg_entry_attribute',
    'get_inseg_entry_attribute',
    'create_inseg_entries',
    'remove_inseg_entries',
    'set_inseg_entries_attribute',
    'get_inseg_entries_attribute',
]
struct__sai_mpls_api_t._fields_ = [
    ('create_inseg_entry', sai_create_inseg_entry_fn),
    ('remove_inseg_entry', sai_remove_inseg_entry_fn),
    ('set_inseg_entry_attribute', sai_set_inseg_entry_attribute_fn),
    ('get_inseg_entry_attribute', sai_get_inseg_entry_attribute_fn),
    ('create_inseg_entries', sai_bulk_create_inseg_entry_fn),
    ('remove_inseg_entries', sai_bulk_remove_inseg_entry_fn),
    ('set_inseg_entries_attribute', sai_bulk_set_inseg_entry_attribute_fn),
    ('get_inseg_entries_attribute', sai_bulk_get_inseg_entry_attribute_fn),
]

sai_mpls_api_t = struct__sai_mpls_api_t# /home/bluecmd/Downloads/SAI/inc/saimpls.h: 404

enum__sai_neighbor_entry_attr_t = c_int# /home/bluecmd/Downloads/SAI/inc/saineighbor.h: 180

SAI_NEIGHBOR_ENTRY_ATTR_START = 0# /home/bluecmd/Downloads/SAI/inc/saineighbor.h: 180

SAI_NEIGHBOR_ENTRY_ATTR_DST_MAC_ADDRESS = SAI_NEIGHBOR_ENTRY_ATTR_START# /home/bluecmd/Downloads/SAI/inc/saineighbor.h: 180

SAI_NEIGHBOR_ENTRY_ATTR_PACKET_ACTION = (SAI_NEIGHBOR_ENTRY_ATTR_DST_MAC_ADDRESS + 1)# /home/bluecmd/Downloads/SAI/inc/saineighbor.h: 180

SAI_NEIGHBOR_ENTRY_ATTR_USER_TRAP_ID = (SAI_NEIGHBOR_ENTRY_ATTR_PACKET_ACTION + 1)# /home/bluecmd/Downloads/SAI/inc/saineighbor.h: 180

SAI_NEIGHBOR_ENTRY_ATTR_NO_HOST_ROUTE = (SAI_NEIGHBOR_ENTRY_ATTR_USER_TRAP_ID + 1)# /home/bluecmd/Downloads/SAI/inc/saineighbor.h: 180

SAI_NEIGHBOR_ENTRY_ATTR_META_DATA = (SAI_NEIGHBOR_ENTRY_ATTR_NO_HOST_ROUTE + 1)# /home/bluecmd/Downloads/SAI/inc/saineighbor.h: 180

SAI_NEIGHBOR_ENTRY_ATTR_COUNTER_ID = (SAI_NEIGHBOR_ENTRY_ATTR_META_DATA + 1)# /home/bluecmd/Downloads/SAI/inc/saineighbor.h: 180

SAI_NEIGHBOR_ENTRY_ATTR_ENCAP_INDEX = (SAI_NEIGHBOR_ENTRY_ATTR_COUNTER_ID + 1)# /home/bluecmd/Downloads/SAI/inc/saineighbor.h: 180

SAI_NEIGHBOR_ENTRY_ATTR_ENCAP_IMPOSE_INDEX = (SAI_NEIGHBOR_ENTRY_ATTR_ENCAP_INDEX + 1)# /home/bluecmd/Downloads/SAI/inc/saineighbor.h: 180

SAI_NEIGHBOR_ENTRY_ATTR_IS_LOCAL = (SAI_NEIGHBOR_ENTRY_ATTR_ENCAP_IMPOSE_INDEX + 1)# /home/bluecmd/Downloads/SAI/inc/saineighbor.h: 180

SAI_NEIGHBOR_ENTRY_ATTR_IP_ADDR_FAMILY = (SAI_NEIGHBOR_ENTRY_ATTR_IS_LOCAL + 1)# /home/bluecmd/Downloads/SAI/inc/saineighbor.h: 180

SAI_NEIGHBOR_ENTRY_ATTR_END = (SAI_NEIGHBOR_ENTRY_ATTR_IP_ADDR_FAMILY + 1)# /home/bluecmd/Downloads/SAI/inc/saineighbor.h: 180

SAI_NEIGHBOR_ENTRY_ATTR_CUSTOM_RANGE_START = 0x10000000# /home/bluecmd/Downloads/SAI/inc/saineighbor.h: 180

SAI_NEIGHBOR_ENTRY_ATTR_CUSTOM_RANGE_END = (SAI_NEIGHBOR_ENTRY_ATTR_CUSTOM_RANGE_START + 1)# /home/bluecmd/Downloads/SAI/inc/saineighbor.h: 180

sai_neighbor_entry_attr_t = enum__sai_neighbor_entry_attr_t# /home/bluecmd/Downloads/SAI/inc/saineighbor.h: 180

# /home/bluecmd/Downloads/SAI/inc/saineighbor.h: 206
class struct__sai_neighbor_entry_t(Structure):
    pass

struct__sai_neighbor_entry_t.__slots__ = [
    'switch_id',
    'rif_id',
    'ip_address',
]
struct__sai_neighbor_entry_t._fields_ = [
    ('switch_id', sai_object_id_t),
    ('rif_id', sai_object_id_t),
    ('ip_address', sai_ip_address_t),
]

sai_neighbor_entry_t = struct__sai_neighbor_entry_t# /home/bluecmd/Downloads/SAI/inc/saineighbor.h: 206

sai_create_neighbor_entry_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_neighbor_entry_t), uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saineighbor.h: 219

sai_remove_neighbor_entry_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_neighbor_entry_t))# /home/bluecmd/Downloads/SAI/inc/saineighbor.h: 233

sai_set_neighbor_entry_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_neighbor_entry_t), POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saineighbor.h: 244

sai_get_neighbor_entry_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_neighbor_entry_t), uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saineighbor.h: 257

sai_remove_all_neighbor_entries_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t)# /home/bluecmd/Downloads/SAI/inc/saineighbor.h: 269

sai_bulk_create_neighbor_entry_fn = CFUNCTYPE(UNCHECKED(sai_status_t), uint32_t, POINTER(sai_neighbor_entry_t), POINTER(uint32_t), POINTER(POINTER(sai_attribute_t)), sai_bulk_op_error_mode_t, POINTER(sai_status_t))# /home/bluecmd/Downloads/SAI/inc/saineighbor.h: 289

sai_bulk_remove_neighbor_entry_fn = CFUNCTYPE(UNCHECKED(sai_status_t), uint32_t, POINTER(sai_neighbor_entry_t), sai_bulk_op_error_mode_t, POINTER(sai_status_t))# /home/bluecmd/Downloads/SAI/inc/saineighbor.h: 311

sai_bulk_set_neighbor_entry_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), uint32_t, POINTER(sai_neighbor_entry_t), POINTER(sai_attribute_t), sai_bulk_op_error_mode_t, POINTER(sai_status_t))# /home/bluecmd/Downloads/SAI/inc/saineighbor.h: 332

sai_bulk_get_neighbor_entry_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), uint32_t, POINTER(sai_neighbor_entry_t), POINTER(uint32_t), POINTER(POINTER(sai_attribute_t)), sai_bulk_op_error_mode_t, POINTER(sai_status_t))# /home/bluecmd/Downloads/SAI/inc/saineighbor.h: 356

# /home/bluecmd/Downloads/SAI/inc/saineighbor.h: 380
class struct__sai_neighbor_api_t(Structure):
    pass

struct__sai_neighbor_api_t.__slots__ = [
    'create_neighbor_entry',
    'remove_neighbor_entry',
    'set_neighbor_entry_attribute',
    'get_neighbor_entry_attribute',
    'remove_all_neighbor_entries',
    'create_neighbor_entries',
    'remove_neighbor_entries',
    'set_neighbor_entries_attribute',
    'get_neighbor_entries_attribute',
]
struct__sai_neighbor_api_t._fields_ = [
    ('create_neighbor_entry', sai_create_neighbor_entry_fn),
    ('remove_neighbor_entry', sai_remove_neighbor_entry_fn),
    ('set_neighbor_entry_attribute', sai_set_neighbor_entry_attribute_fn),
    ('get_neighbor_entry_attribute', sai_get_neighbor_entry_attribute_fn),
    ('remove_all_neighbor_entries', sai_remove_all_neighbor_entries_fn),
    ('create_neighbor_entries', sai_bulk_create_neighbor_entry_fn),
    ('remove_neighbor_entries', sai_bulk_remove_neighbor_entry_fn),
    ('set_neighbor_entries_attribute', sai_bulk_set_neighbor_entry_attribute_fn),
    ('get_neighbor_entries_attribute', sai_bulk_get_neighbor_entry_attribute_fn),
]

sai_neighbor_api_t = struct__sai_neighbor_api_t# /home/bluecmd/Downloads/SAI/inc/saineighbor.h: 380

enum__sai_next_hop_group_type_t = c_int# /home/bluecmd/Downloads/SAI/inc/sainexthopgroup.h: 61

SAI_NEXT_HOP_GROUP_TYPE_DYNAMIC_UNORDERED_ECMP = 0# /home/bluecmd/Downloads/SAI/inc/sainexthopgroup.h: 61

SAI_NEXT_HOP_GROUP_TYPE_ECMP = SAI_NEXT_HOP_GROUP_TYPE_DYNAMIC_UNORDERED_ECMP# /home/bluecmd/Downloads/SAI/inc/sainexthopgroup.h: 61

SAI_NEXT_HOP_GROUP_TYPE_DYNAMIC_ORDERED_ECMP = (SAI_NEXT_HOP_GROUP_TYPE_ECMP + 1)# /home/bluecmd/Downloads/SAI/inc/sainexthopgroup.h: 61

SAI_NEXT_HOP_GROUP_TYPE_FINE_GRAIN_ECMP = (SAI_NEXT_HOP_GROUP_TYPE_DYNAMIC_ORDERED_ECMP + 1)# /home/bluecmd/Downloads/SAI/inc/sainexthopgroup.h: 61

SAI_NEXT_HOP_GROUP_TYPE_PROTECTION = (SAI_NEXT_HOP_GROUP_TYPE_FINE_GRAIN_ECMP + 1)# /home/bluecmd/Downloads/SAI/inc/sainexthopgroup.h: 61

SAI_NEXT_HOP_GROUP_TYPE_CLASS_BASED = (SAI_NEXT_HOP_GROUP_TYPE_PROTECTION + 1)# /home/bluecmd/Downloads/SAI/inc/sainexthopgroup.h: 61

sai_next_hop_group_type_t = enum__sai_next_hop_group_type_t# /home/bluecmd/Downloads/SAI/inc/sainexthopgroup.h: 61

enum__sai_next_hop_group_member_configured_role_t = c_int# /home/bluecmd/Downloads/SAI/inc/sainexthopgroup.h: 74

SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_PRIMARY = 0# /home/bluecmd/Downloads/SAI/inc/sainexthopgroup.h: 74

SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_STANDBY = (SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_PRIMARY + 1)# /home/bluecmd/Downloads/SAI/inc/sainexthopgroup.h: 74

sai_next_hop_group_member_configured_role_t = enum__sai_next_hop_group_member_configured_role_t# /home/bluecmd/Downloads/SAI/inc/sainexthopgroup.h: 74

enum__sai_next_hop_group_member_observed_role_t = c_int# /home/bluecmd/Downloads/SAI/inc/sainexthopgroup.h: 87

SAI_NEXT_HOP_GROUP_MEMBER_OBSERVED_ROLE_ACTIVE = 0# /home/bluecmd/Downloads/SAI/inc/sainexthopgroup.h: 87

SAI_NEXT_HOP_GROUP_MEMBER_OBSERVED_ROLE_INACTIVE = (SAI_NEXT_HOP_GROUP_MEMBER_OBSERVED_ROLE_ACTIVE + 1)# /home/bluecmd/Downloads/SAI/inc/sainexthopgroup.h: 87

sai_next_hop_group_member_observed_role_t = enum__sai_next_hop_group_member_observed_role_t# /home/bluecmd/Downloads/SAI/inc/sainexthopgroup.h: 87

enum__sai_next_hop_group_attr_t = c_int# /home/bluecmd/Downloads/SAI/inc/sainexthopgroup.h: 246

SAI_NEXT_HOP_GROUP_ATTR_START = 0# /home/bluecmd/Downloads/SAI/inc/sainexthopgroup.h: 246

SAI_NEXT_HOP_GROUP_ATTR_NEXT_HOP_COUNT = SAI_NEXT_HOP_GROUP_ATTR_START# /home/bluecmd/Downloads/SAI/inc/sainexthopgroup.h: 246

SAI_NEXT_HOP_GROUP_ATTR_NEXT_HOP_MEMBER_LIST = (SAI_NEXT_HOP_GROUP_ATTR_NEXT_HOP_COUNT + 1)# /home/bluecmd/Downloads/SAI/inc/sainexthopgroup.h: 246

SAI_NEXT_HOP_GROUP_ATTR_TYPE = (SAI_NEXT_HOP_GROUP_ATTR_NEXT_HOP_MEMBER_LIST + 1)# /home/bluecmd/Downloads/SAI/inc/sainexthopgroup.h: 246

SAI_NEXT_HOP_GROUP_ATTR_SET_SWITCHOVER = (SAI_NEXT_HOP_GROUP_ATTR_TYPE + 1)# /home/bluecmd/Downloads/SAI/inc/sainexthopgroup.h: 246

SAI_NEXT_HOP_GROUP_ATTR_COUNTER_ID = (SAI_NEXT_HOP_GROUP_ATTR_SET_SWITCHOVER + 1)# /home/bluecmd/Downloads/SAI/inc/sainexthopgroup.h: 246

SAI_NEXT_HOP_GROUP_ATTR_CONFIGURED_SIZE = (SAI_NEXT_HOP_GROUP_ATTR_COUNTER_ID + 1)# /home/bluecmd/Downloads/SAI/inc/sainexthopgroup.h: 246

SAI_NEXT_HOP_GROUP_ATTR_REAL_SIZE = (SAI_NEXT_HOP_GROUP_ATTR_CONFIGURED_SIZE + 1)# /home/bluecmd/Downloads/SAI/inc/sainexthopgroup.h: 246

SAI_NEXT_HOP_GROUP_ATTR_SELECTION_MAP = (SAI_NEXT_HOP_GROUP_ATTR_REAL_SIZE + 1)# /home/bluecmd/Downloads/SAI/inc/sainexthopgroup.h: 246

SAI_NEXT_HOP_GROUP_ATTR_HIERARCHICAL_NEXTHOP = (SAI_NEXT_HOP_GROUP_ATTR_SELECTION_MAP + 1)# /home/bluecmd/Downloads/SAI/inc/sainexthopgroup.h: 246

SAI_NEXT_HOP_GROUP_ATTR_ARS_OBJECT_ID = (SAI_NEXT_HOP_GROUP_ATTR_HIERARCHICAL_NEXTHOP + 1)# /home/bluecmd/Downloads/SAI/inc/sainexthopgroup.h: 246

SAI_NEXT_HOP_GROUP_ATTR_ARS_PACKET_DROPS = (SAI_NEXT_HOP_GROUP_ATTR_ARS_OBJECT_ID + 1)# /home/bluecmd/Downloads/SAI/inc/sainexthopgroup.h: 246

SAI_NEXT_HOP_GROUP_ATTR_ARS_NEXT_HOP_REASSIGNMENTS = (SAI_NEXT_HOP_GROUP_ATTR_ARS_PACKET_DROPS + 1)# /home/bluecmd/Downloads/SAI/inc/sainexthopgroup.h: 246

SAI_NEXT_HOP_GROUP_ATTR_ARS_PORT_REASSIGNMENTS = (SAI_NEXT_HOP_GROUP_ATTR_ARS_NEXT_HOP_REASSIGNMENTS + 1)# /home/bluecmd/Downloads/SAI/inc/sainexthopgroup.h: 246

SAI_NEXT_HOP_GROUP_ATTR_END = (SAI_NEXT_HOP_GROUP_ATTR_ARS_PORT_REASSIGNMENTS + 1)# /home/bluecmd/Downloads/SAI/inc/sainexthopgroup.h: 246

SAI_NEXT_HOP_GROUP_ATTR_CUSTOM_RANGE_START = 0x10000000# /home/bluecmd/Downloads/SAI/inc/sainexthopgroup.h: 246

SAI_NEXT_HOP_GROUP_ATTR_CUSTOM_RANGE_END = (SAI_NEXT_HOP_GROUP_ATTR_CUSTOM_RANGE_START + 1)# /home/bluecmd/Downloads/SAI/inc/sainexthopgroup.h: 246

sai_next_hop_group_attr_t = enum__sai_next_hop_group_attr_t# /home/bluecmd/Downloads/SAI/inc/sainexthopgroup.h: 246

enum__sai_next_hop_group_member_attr_t = c_int# /home/bluecmd/Downloads/SAI/inc/sainexthopgroup.h: 387

SAI_NEXT_HOP_GROUP_MEMBER_ATTR_START = 0# /home/bluecmd/Downloads/SAI/inc/sainexthopgroup.h: 387

SAI_NEXT_HOP_GROUP_MEMBER_ATTR_NEXT_HOP_GROUP_ID = SAI_NEXT_HOP_GROUP_MEMBER_ATTR_START# /home/bluecmd/Downloads/SAI/inc/sainexthopgroup.h: 387

SAI_NEXT_HOP_GROUP_MEMBER_ATTR_NEXT_HOP_ID = (SAI_NEXT_HOP_GROUP_MEMBER_ATTR_NEXT_HOP_GROUP_ID + 1)# /home/bluecmd/Downloads/SAI/inc/sainexthopgroup.h: 387

SAI_NEXT_HOP_GROUP_MEMBER_ATTR_WEIGHT = (SAI_NEXT_HOP_GROUP_MEMBER_ATTR_NEXT_HOP_ID + 1)# /home/bluecmd/Downloads/SAI/inc/sainexthopgroup.h: 387

SAI_NEXT_HOP_GROUP_MEMBER_ATTR_CONFIGURED_ROLE = (SAI_NEXT_HOP_GROUP_MEMBER_ATTR_WEIGHT + 1)# /home/bluecmd/Downloads/SAI/inc/sainexthopgroup.h: 387

SAI_NEXT_HOP_GROUP_MEMBER_ATTR_OBSERVED_ROLE = (SAI_NEXT_HOP_GROUP_MEMBER_ATTR_CONFIGURED_ROLE + 1)# /home/bluecmd/Downloads/SAI/inc/sainexthopgroup.h: 387

SAI_NEXT_HOP_GROUP_MEMBER_ATTR_MONITORED_OBJECT = (SAI_NEXT_HOP_GROUP_MEMBER_ATTR_OBSERVED_ROLE + 1)# /home/bluecmd/Downloads/SAI/inc/sainexthopgroup.h: 387

SAI_NEXT_HOP_GROUP_MEMBER_ATTR_INDEX = (SAI_NEXT_HOP_GROUP_MEMBER_ATTR_MONITORED_OBJECT + 1)# /home/bluecmd/Downloads/SAI/inc/sainexthopgroup.h: 387

SAI_NEXT_HOP_GROUP_MEMBER_ATTR_SEQUENCE_ID = (SAI_NEXT_HOP_GROUP_MEMBER_ATTR_INDEX + 1)# /home/bluecmd/Downloads/SAI/inc/sainexthopgroup.h: 387

SAI_NEXT_HOP_GROUP_MEMBER_ATTR_COUNTER_ID = (SAI_NEXT_HOP_GROUP_MEMBER_ATTR_SEQUENCE_ID + 1)# /home/bluecmd/Downloads/SAI/inc/sainexthopgroup.h: 387

SAI_NEXT_HOP_GROUP_MEMBER_ATTR_ARS_ALTERNATE_PATH = (SAI_NEXT_HOP_GROUP_MEMBER_ATTR_COUNTER_ID + 1)# /home/bluecmd/Downloads/SAI/inc/sainexthopgroup.h: 387

SAI_NEXT_HOP_GROUP_MEMBER_ATTR_END = (SAI_NEXT_HOP_GROUP_MEMBER_ATTR_ARS_ALTERNATE_PATH + 1)# /home/bluecmd/Downloads/SAI/inc/sainexthopgroup.h: 387

SAI_NEXT_HOP_GROUP_MEMBER_ATTR_CUSTOM_RANGE_START = 0x10000000# /home/bluecmd/Downloads/SAI/inc/sainexthopgroup.h: 387

SAI_NEXT_HOP_GROUP_MEMBER_ATTR_CUSTOM_RANGE_END = (SAI_NEXT_HOP_GROUP_MEMBER_ATTR_CUSTOM_RANGE_START + 1)# /home/bluecmd/Downloads/SAI/inc/sainexthopgroup.h: 387

sai_next_hop_group_member_attr_t = enum__sai_next_hop_group_member_attr_t# /home/bluecmd/Downloads/SAI/inc/sainexthopgroup.h: 387

enum__sai_next_hop_group_map_type_t = c_int# /home/bluecmd/Downloads/SAI/inc/sainexthopgroup.h: 394

SAI_NEXT_HOP_GROUP_MAP_TYPE_FORWARDING_CLASS_TO_INDEX = 0# /home/bluecmd/Downloads/SAI/inc/sainexthopgroup.h: 394

sai_next_hop_group_map_type_t = enum__sai_next_hop_group_map_type_t# /home/bluecmd/Downloads/SAI/inc/sainexthopgroup.h: 394

enum__sai_next_hop_group_map_attr_t = c_int# /home/bluecmd/Downloads/SAI/inc/sainexthopgroup.h: 431

SAI_NEXT_HOP_GROUP_MAP_ATTR_START = 0# /home/bluecmd/Downloads/SAI/inc/sainexthopgroup.h: 431

SAI_NEXT_HOP_GROUP_MAP_ATTR_TYPE = SAI_NEXT_HOP_GROUP_MAP_ATTR_START# /home/bluecmd/Downloads/SAI/inc/sainexthopgroup.h: 431

SAI_NEXT_HOP_GROUP_MAP_ATTR_MAP_TO_VALUE_LIST = (SAI_NEXT_HOP_GROUP_MAP_ATTR_TYPE + 1)# /home/bluecmd/Downloads/SAI/inc/sainexthopgroup.h: 431

SAI_NEXT_HOP_GROUP_MAP_ATTR_END = (SAI_NEXT_HOP_GROUP_MAP_ATTR_MAP_TO_VALUE_LIST + 1)# /home/bluecmd/Downloads/SAI/inc/sainexthopgroup.h: 431

SAI_NEXT_HOP_GROUP_MAP_ATTR_CUSTOM_RANGE_START = 0x10000000# /home/bluecmd/Downloads/SAI/inc/sainexthopgroup.h: 431

SAI_NEXT_HOP_GROUP_MAP_ATTR_CUSTOM_RANGE_END = (SAI_NEXT_HOP_GROUP_MAP_ATTR_CUSTOM_RANGE_START + 1)# /home/bluecmd/Downloads/SAI/inc/sainexthopgroup.h: 431

sai_next_hop_group_map_attr_t = enum__sai_next_hop_group_map_attr_t# /home/bluecmd/Downloads/SAI/inc/sainexthopgroup.h: 431

sai_create_next_hop_group_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/sainexthopgroup.h: 443

sai_remove_next_hop_group_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t)# /home/bluecmd/Downloads/SAI/inc/sainexthopgroup.h: 456

sai_set_next_hop_group_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/sainexthopgroup.h: 467

sai_get_next_hop_group_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/sainexthopgroup.h: 480

sai_create_next_hop_group_member_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/sainexthopgroup.h: 495

sai_remove_next_hop_group_member_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t)# /home/bluecmd/Downloads/SAI/inc/sainexthopgroup.h: 508

sai_set_next_hop_group_member_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/sainexthopgroup.h: 519

sai_get_next_hop_group_member_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/sainexthopgroup.h: 532

sai_create_next_hop_group_map_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/sainexthopgroup.h: 547

sai_remove_next_hop_group_map_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t)# /home/bluecmd/Downloads/SAI/inc/sainexthopgroup.h: 560

sai_set_next_hop_group_map_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/sainexthopgroup.h: 571

sai_get_next_hop_group_map_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/sainexthopgroup.h: 584

# /home/bluecmd/Downloads/SAI/inc/sainexthopgroup.h: 610
class struct__sai_next_hop_group_api_t(Structure):
    pass

struct__sai_next_hop_group_api_t.__slots__ = [
    'create_next_hop_group',
    'remove_next_hop_group',
    'set_next_hop_group_attribute',
    'get_next_hop_group_attribute',
    'create_next_hop_group_member',
    'remove_next_hop_group_member',
    'set_next_hop_group_member_attribute',
    'get_next_hop_group_member_attribute',
    'create_next_hop_group_members',
    'remove_next_hop_group_members',
    'create_next_hop_group_map',
    'remove_next_hop_group_map',
    'set_next_hop_group_map_attribute',
    'get_next_hop_group_map_attribute',
    'set_next_hop_group_members_attribute',
    'get_next_hop_group_members_attribute',
]
struct__sai_next_hop_group_api_t._fields_ = [
    ('create_next_hop_group', sai_create_next_hop_group_fn),
    ('remove_next_hop_group', sai_remove_next_hop_group_fn),
    ('set_next_hop_group_attribute', sai_set_next_hop_group_attribute_fn),
    ('get_next_hop_group_attribute', sai_get_next_hop_group_attribute_fn),
    ('create_next_hop_group_member', sai_create_next_hop_group_member_fn),
    ('remove_next_hop_group_member', sai_remove_next_hop_group_member_fn),
    ('set_next_hop_group_member_attribute', sai_set_next_hop_group_member_attribute_fn),
    ('get_next_hop_group_member_attribute', sai_get_next_hop_group_member_attribute_fn),
    ('create_next_hop_group_members', sai_bulk_object_create_fn),
    ('remove_next_hop_group_members', sai_bulk_object_remove_fn),
    ('create_next_hop_group_map', sai_create_next_hop_group_map_fn),
    ('remove_next_hop_group_map', sai_remove_next_hop_group_map_fn),
    ('set_next_hop_group_map_attribute', sai_set_next_hop_group_map_attribute_fn),
    ('get_next_hop_group_map_attribute', sai_get_next_hop_group_map_attribute_fn),
    ('set_next_hop_group_members_attribute', sai_bulk_object_set_attribute_fn),
    ('get_next_hop_group_members_attribute', sai_bulk_object_get_attribute_fn),
]

sai_next_hop_group_api_t = struct__sai_next_hop_group_api_t# /home/bluecmd/Downloads/SAI/inc/sainexthopgroup.h: 610

enum__sai_next_hop_type_t = c_int# /home/bluecmd/Downloads/SAI/inc/sainexthop.h: 53

SAI_NEXT_HOP_TYPE_IP = 0# /home/bluecmd/Downloads/SAI/inc/sainexthop.h: 53

SAI_NEXT_HOP_TYPE_MPLS = (SAI_NEXT_HOP_TYPE_IP + 1)# /home/bluecmd/Downloads/SAI/inc/sainexthop.h: 53

SAI_NEXT_HOP_TYPE_TUNNEL_ENCAP = (SAI_NEXT_HOP_TYPE_MPLS + 1)# /home/bluecmd/Downloads/SAI/inc/sainexthop.h: 53

SAI_NEXT_HOP_TYPE_SRV6_SIDLIST = (SAI_NEXT_HOP_TYPE_TUNNEL_ENCAP + 1)# /home/bluecmd/Downloads/SAI/inc/sainexthop.h: 53

sai_next_hop_type_t = enum__sai_next_hop_type_t# /home/bluecmd/Downloads/SAI/inc/sainexthop.h: 53

enum__sai_next_hop_attr_t = c_int# /home/bluecmd/Downloads/SAI/inc/sainexthop.h: 267

SAI_NEXT_HOP_ATTR_START = 0# /home/bluecmd/Downloads/SAI/inc/sainexthop.h: 267

SAI_NEXT_HOP_ATTR_TYPE = SAI_NEXT_HOP_ATTR_START# /home/bluecmd/Downloads/SAI/inc/sainexthop.h: 267

SAI_NEXT_HOP_ATTR_IP = (SAI_NEXT_HOP_ATTR_TYPE + 1)# /home/bluecmd/Downloads/SAI/inc/sainexthop.h: 267

SAI_NEXT_HOP_ATTR_ROUTER_INTERFACE_ID = (SAI_NEXT_HOP_ATTR_IP + 1)# /home/bluecmd/Downloads/SAI/inc/sainexthop.h: 267

SAI_NEXT_HOP_ATTR_TUNNEL_ID = (SAI_NEXT_HOP_ATTR_ROUTER_INTERFACE_ID + 1)# /home/bluecmd/Downloads/SAI/inc/sainexthop.h: 267

SAI_NEXT_HOP_ATTR_TUNNEL_VNI = (SAI_NEXT_HOP_ATTR_TUNNEL_ID + 1)# /home/bluecmd/Downloads/SAI/inc/sainexthop.h: 267

SAI_NEXT_HOP_ATTR_TUNNEL_MAC = (SAI_NEXT_HOP_ATTR_TUNNEL_VNI + 1)# /home/bluecmd/Downloads/SAI/inc/sainexthop.h: 267

SAI_NEXT_HOP_ATTR_SRV6_SIDLIST_ID = (SAI_NEXT_HOP_ATTR_TUNNEL_MAC + 1)# /home/bluecmd/Downloads/SAI/inc/sainexthop.h: 267

SAI_NEXT_HOP_ATTR_LABELSTACK = (SAI_NEXT_HOP_ATTR_SRV6_SIDLIST_ID + 1)# /home/bluecmd/Downloads/SAI/inc/sainexthop.h: 267

SAI_NEXT_HOP_ATTR_COUNTER_ID = (SAI_NEXT_HOP_ATTR_LABELSTACK + 1)# /home/bluecmd/Downloads/SAI/inc/sainexthop.h: 267

SAI_NEXT_HOP_ATTR_DISABLE_DECREMENT_TTL = (SAI_NEXT_HOP_ATTR_COUNTER_ID + 1)# /home/bluecmd/Downloads/SAI/inc/sainexthop.h: 267

SAI_NEXT_HOP_ATTR_OUTSEG_TYPE = (SAI_NEXT_HOP_ATTR_DISABLE_DECREMENT_TTL + 1)# /home/bluecmd/Downloads/SAI/inc/sainexthop.h: 267

SAI_NEXT_HOP_ATTR_OUTSEG_TTL_MODE = (SAI_NEXT_HOP_ATTR_OUTSEG_TYPE + 1)# /home/bluecmd/Downloads/SAI/inc/sainexthop.h: 267

SAI_NEXT_HOP_ATTR_OUTSEG_TTL_VALUE = (SAI_NEXT_HOP_ATTR_OUTSEG_TTL_MODE + 1)# /home/bluecmd/Downloads/SAI/inc/sainexthop.h: 267

SAI_NEXT_HOP_ATTR_OUTSEG_EXP_MODE = (SAI_NEXT_HOP_ATTR_OUTSEG_TTL_VALUE + 1)# /home/bluecmd/Downloads/SAI/inc/sainexthop.h: 267

SAI_NEXT_HOP_ATTR_OUTSEG_EXP_VALUE = (SAI_NEXT_HOP_ATTR_OUTSEG_EXP_MODE + 1)# /home/bluecmd/Downloads/SAI/inc/sainexthop.h: 267

SAI_NEXT_HOP_ATTR_QOS_TC_AND_COLOR_TO_MPLS_EXP_MAP = (SAI_NEXT_HOP_ATTR_OUTSEG_EXP_VALUE + 1)# /home/bluecmd/Downloads/SAI/inc/sainexthop.h: 267

SAI_NEXT_HOP_ATTR_DISABLE_SRC_MAC_REWRITE = (SAI_NEXT_HOP_ATTR_QOS_TC_AND_COLOR_TO_MPLS_EXP_MAP + 1)# /home/bluecmd/Downloads/SAI/inc/sainexthop.h: 267

SAI_NEXT_HOP_ATTR_DISABLE_DST_MAC_REWRITE = (SAI_NEXT_HOP_ATTR_DISABLE_SRC_MAC_REWRITE + 1)# /home/bluecmd/Downloads/SAI/inc/sainexthop.h: 267

SAI_NEXT_HOP_ATTR_DISABLE_VLAN_REWRITE = (SAI_NEXT_HOP_ATTR_DISABLE_DST_MAC_REWRITE + 1)# /home/bluecmd/Downloads/SAI/inc/sainexthop.h: 267

SAI_NEXT_HOP_ATTR_END = (SAI_NEXT_HOP_ATTR_DISABLE_VLAN_REWRITE + 1)# /home/bluecmd/Downloads/SAI/inc/sainexthop.h: 267

SAI_NEXT_HOP_ATTR_CUSTOM_RANGE_START = 0x10000000# /home/bluecmd/Downloads/SAI/inc/sainexthop.h: 267

SAI_NEXT_HOP_ATTR_CUSTOM_RANGE_END = (SAI_NEXT_HOP_ATTR_CUSTOM_RANGE_START + 1)# /home/bluecmd/Downloads/SAI/inc/sainexthop.h: 267

sai_next_hop_attr_t = enum__sai_next_hop_attr_t# /home/bluecmd/Downloads/SAI/inc/sainexthop.h: 267

sai_create_next_hop_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/sainexthop.h: 281

sai_remove_next_hop_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t)# /home/bluecmd/Downloads/SAI/inc/sainexthop.h: 294

sai_set_next_hop_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/sainexthop.h: 305

sai_get_next_hop_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/sainexthop.h: 318

# /home/bluecmd/Downloads/SAI/inc/sainexthop.h: 337
class struct__sai_next_hop_api_t(Structure):
    pass

struct__sai_next_hop_api_t.__slots__ = [
    'create_next_hop',
    'remove_next_hop',
    'set_next_hop_attribute',
    'get_next_hop_attribute',
    'create_next_hops',
    'remove_next_hops',
    'set_next_hops_attribute',
    'get_next_hops_attribute',
]
struct__sai_next_hop_api_t._fields_ = [
    ('create_next_hop', sai_create_next_hop_fn),
    ('remove_next_hop', sai_remove_next_hop_fn),
    ('set_next_hop_attribute', sai_set_next_hop_attribute_fn),
    ('get_next_hop_attribute', sai_get_next_hop_attribute_fn),
    ('create_next_hops', sai_bulk_object_create_fn),
    ('remove_next_hops', sai_bulk_object_remove_fn),
    ('set_next_hops_attribute', sai_bulk_object_set_attribute_fn),
    ('get_next_hops_attribute', sai_bulk_object_get_attribute_fn),
]

sai_next_hop_api_t = struct__sai_next_hop_api_t# /home/bluecmd/Downloads/SAI/inc/sainexthop.h: 337

enum__sai_route_entry_attr_t = c_int# /home/bluecmd/Downloads/SAI/inc/sairoute.h: 156

SAI_ROUTE_ENTRY_ATTR_START = 0# /home/bluecmd/Downloads/SAI/inc/sairoute.h: 156

SAI_ROUTE_ENTRY_ATTR_PACKET_ACTION = SAI_ROUTE_ENTRY_ATTR_START# /home/bluecmd/Downloads/SAI/inc/sairoute.h: 156

SAI_ROUTE_ENTRY_ATTR_USER_TRAP_ID = (SAI_ROUTE_ENTRY_ATTR_PACKET_ACTION + 1)# /home/bluecmd/Downloads/SAI/inc/sairoute.h: 156

SAI_ROUTE_ENTRY_ATTR_NEXT_HOP_ID = (SAI_ROUTE_ENTRY_ATTR_USER_TRAP_ID + 1)# /home/bluecmd/Downloads/SAI/inc/sairoute.h: 156

SAI_ROUTE_ENTRY_ATTR_META_DATA = (SAI_ROUTE_ENTRY_ATTR_NEXT_HOP_ID + 1)# /home/bluecmd/Downloads/SAI/inc/sairoute.h: 156

SAI_ROUTE_ENTRY_ATTR_IP_ADDR_FAMILY = (SAI_ROUTE_ENTRY_ATTR_META_DATA + 1)# /home/bluecmd/Downloads/SAI/inc/sairoute.h: 156

SAI_ROUTE_ENTRY_ATTR_COUNTER_ID = (SAI_ROUTE_ENTRY_ATTR_IP_ADDR_FAMILY + 1)# /home/bluecmd/Downloads/SAI/inc/sairoute.h: 156

SAI_ROUTE_ENTRY_ATTR_PREFIX_AGG_ID = (SAI_ROUTE_ENTRY_ATTR_COUNTER_ID + 1)# /home/bluecmd/Downloads/SAI/inc/sairoute.h: 156

SAI_ROUTE_ENTRY_ATTR_END = (SAI_ROUTE_ENTRY_ATTR_PREFIX_AGG_ID + 1)# /home/bluecmd/Downloads/SAI/inc/sairoute.h: 156

SAI_ROUTE_ENTRY_ATTR_CUSTOM_RANGE_START = 0x10000000# /home/bluecmd/Downloads/SAI/inc/sairoute.h: 156

SAI_ROUTE_ENTRY_ATTR_CUSTOM_RANGE_END = (SAI_ROUTE_ENTRY_ATTR_CUSTOM_RANGE_START + 1)# /home/bluecmd/Downloads/SAI/inc/sairoute.h: 156

sai_route_entry_attr_t = enum__sai_route_entry_attr_t# /home/bluecmd/Downloads/SAI/inc/sairoute.h: 156

# /home/bluecmd/Downloads/SAI/inc/sairoute.h: 182
class struct__sai_route_entry_t(Structure):
    pass

struct__sai_route_entry_t.__slots__ = [
    'switch_id',
    'vr_id',
    'destination',
]
struct__sai_route_entry_t._fields_ = [
    ('switch_id', sai_object_id_t),
    ('vr_id', sai_object_id_t),
    ('destination', sai_ip_prefix_t),
]

sai_route_entry_t = struct__sai_route_entry_t# /home/bluecmd/Downloads/SAI/inc/sairoute.h: 182

sai_create_route_entry_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_route_entry_t), uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/sairoute.h: 195

sai_remove_route_entry_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_route_entry_t))# /home/bluecmd/Downloads/SAI/inc/sairoute.h: 209

sai_set_route_entry_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_route_entry_t), POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/sairoute.h: 220

sai_get_route_entry_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_route_entry_t), uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/sairoute.h: 233

sai_bulk_create_route_entry_fn = CFUNCTYPE(UNCHECKED(sai_status_t), uint32_t, POINTER(sai_route_entry_t), POINTER(uint32_t), POINTER(POINTER(sai_attribute_t)), sai_bulk_op_error_mode_t, POINTER(sai_status_t))# /home/bluecmd/Downloads/SAI/inc/sairoute.h: 255

sai_bulk_remove_route_entry_fn = CFUNCTYPE(UNCHECKED(sai_status_t), uint32_t, POINTER(sai_route_entry_t), sai_bulk_op_error_mode_t, POINTER(sai_status_t))# /home/bluecmd/Downloads/SAI/inc/sairoute.h: 277

sai_bulk_set_route_entry_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), uint32_t, POINTER(sai_route_entry_t), POINTER(sai_attribute_t), sai_bulk_op_error_mode_t, POINTER(sai_status_t))# /home/bluecmd/Downloads/SAI/inc/sairoute.h: 298

sai_bulk_get_route_entry_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), uint32_t, POINTER(sai_route_entry_t), POINTER(uint32_t), POINTER(POINTER(sai_attribute_t)), sai_bulk_op_error_mode_t, POINTER(sai_status_t))# /home/bluecmd/Downloads/SAI/inc/sairoute.h: 322

# /home/bluecmd/Downloads/SAI/inc/sairoute.h: 345
class struct__sai_route_api_t(Structure):
    pass

struct__sai_route_api_t.__slots__ = [
    'create_route_entry',
    'remove_route_entry',
    'set_route_entry_attribute',
    'get_route_entry_attribute',
    'create_route_entries',
    'remove_route_entries',
    'set_route_entries_attribute',
    'get_route_entries_attribute',
]
struct__sai_route_api_t._fields_ = [
    ('create_route_entry', sai_create_route_entry_fn),
    ('remove_route_entry', sai_remove_route_entry_fn),
    ('set_route_entry_attribute', sai_set_route_entry_attribute_fn),
    ('get_route_entry_attribute', sai_get_route_entry_attribute_fn),
    ('create_route_entries', sai_bulk_create_route_entry_fn),
    ('remove_route_entries', sai_bulk_remove_route_entry_fn),
    ('set_route_entries_attribute', sai_bulk_set_route_entry_attribute_fn),
    ('get_route_entries_attribute', sai_bulk_get_route_entry_attribute_fn),
]

sai_route_api_t = struct__sai_route_api_t# /home/bluecmd/Downloads/SAI/inc/sairoute.h: 345

enum__sai_nat_type_t = c_int# /home/bluecmd/Downloads/SAI/inc/sainat.h: 56

SAI_NAT_TYPE_NONE = 0# /home/bluecmd/Downloads/SAI/inc/sainat.h: 56

SAI_NAT_TYPE_SOURCE_NAT = (SAI_NAT_TYPE_NONE + 1)# /home/bluecmd/Downloads/SAI/inc/sainat.h: 56

SAI_NAT_TYPE_DESTINATION_NAT = (SAI_NAT_TYPE_SOURCE_NAT + 1)# /home/bluecmd/Downloads/SAI/inc/sainat.h: 56

SAI_NAT_TYPE_DOUBLE_NAT = (SAI_NAT_TYPE_DESTINATION_NAT + 1)# /home/bluecmd/Downloads/SAI/inc/sainat.h: 56

SAI_NAT_TYPE_DESTINATION_NAT_POOL = (SAI_NAT_TYPE_DOUBLE_NAT + 1)# /home/bluecmd/Downloads/SAI/inc/sainat.h: 56

sai_nat_type_t = enum__sai_nat_type_t# /home/bluecmd/Downloads/SAI/inc/sainat.h: 56

enum__sai_nat_entry_attr_t = c_int# /home/bluecmd/Downloads/SAI/inc/sainat.h: 234

SAI_NAT_ENTRY_ATTR_START = 0# /home/bluecmd/Downloads/SAI/inc/sainat.h: 234

SAI_NAT_ENTRY_ATTR_NAT_TYPE = SAI_NAT_ENTRY_ATTR_START# /home/bluecmd/Downloads/SAI/inc/sainat.h: 234

SAI_NAT_ENTRY_ATTR_SRC_IP = (SAI_NAT_ENTRY_ATTR_NAT_TYPE + 1)# /home/bluecmd/Downloads/SAI/inc/sainat.h: 234

SAI_NAT_ENTRY_ATTR_SRC_IP_MASK = (SAI_NAT_ENTRY_ATTR_SRC_IP + 1)# /home/bluecmd/Downloads/SAI/inc/sainat.h: 234

SAI_NAT_ENTRY_ATTR_VR_ID = (SAI_NAT_ENTRY_ATTR_SRC_IP_MASK + 1)# /home/bluecmd/Downloads/SAI/inc/sainat.h: 234

SAI_NAT_ENTRY_ATTR_DST_IP = (SAI_NAT_ENTRY_ATTR_VR_ID + 1)# /home/bluecmd/Downloads/SAI/inc/sainat.h: 234

SAI_NAT_ENTRY_ATTR_DST_IP_MASK = (SAI_NAT_ENTRY_ATTR_DST_IP + 1)# /home/bluecmd/Downloads/SAI/inc/sainat.h: 234

SAI_NAT_ENTRY_ATTR_L4_SRC_PORT = (SAI_NAT_ENTRY_ATTR_DST_IP_MASK + 1)# /home/bluecmd/Downloads/SAI/inc/sainat.h: 234

SAI_NAT_ENTRY_ATTR_L4_DST_PORT = (SAI_NAT_ENTRY_ATTR_L4_SRC_PORT + 1)# /home/bluecmd/Downloads/SAI/inc/sainat.h: 234

SAI_NAT_ENTRY_ATTR_ENABLE_PACKET_COUNT = (SAI_NAT_ENTRY_ATTR_L4_DST_PORT + 1)# /home/bluecmd/Downloads/SAI/inc/sainat.h: 234

SAI_NAT_ENTRY_ATTR_PACKET_COUNT = (SAI_NAT_ENTRY_ATTR_ENABLE_PACKET_COUNT + 1)# /home/bluecmd/Downloads/SAI/inc/sainat.h: 234

SAI_NAT_ENTRY_ATTR_ENABLE_BYTE_COUNT = (SAI_NAT_ENTRY_ATTR_PACKET_COUNT + 1)# /home/bluecmd/Downloads/SAI/inc/sainat.h: 234

SAI_NAT_ENTRY_ATTR_BYTE_COUNT = (SAI_NAT_ENTRY_ATTR_ENABLE_BYTE_COUNT + 1)# /home/bluecmd/Downloads/SAI/inc/sainat.h: 234

SAI_NAT_ENTRY_ATTR_HIT_BIT_COR = (SAI_NAT_ENTRY_ATTR_BYTE_COUNT + 1)# /home/bluecmd/Downloads/SAI/inc/sainat.h: 234

SAI_NAT_ENTRY_ATTR_HIT_BIT = (SAI_NAT_ENTRY_ATTR_HIT_BIT_COR + 1)# /home/bluecmd/Downloads/SAI/inc/sainat.h: 234

SAI_NAT_ENTRY_ATTR_AGING_TIME = (SAI_NAT_ENTRY_ATTR_HIT_BIT + 1)# /home/bluecmd/Downloads/SAI/inc/sainat.h: 234

SAI_NAT_ENTRY_ATTR_END = (SAI_NAT_ENTRY_ATTR_AGING_TIME + 1)# /home/bluecmd/Downloads/SAI/inc/sainat.h: 234

SAI_NAT_ENTRY_ATTR_CUSTOM_RANGE_START = 0x10000000# /home/bluecmd/Downloads/SAI/inc/sainat.h: 234

SAI_NAT_ENTRY_ATTR_CUSTOM_RANGE_END = (SAI_NAT_ENTRY_ATTR_CUSTOM_RANGE_START + 1)# /home/bluecmd/Downloads/SAI/inc/sainat.h: 234

sai_nat_entry_attr_t = enum__sai_nat_entry_attr_t# /home/bluecmd/Downloads/SAI/inc/sainat.h: 234

# /home/bluecmd/Downloads/SAI/inc/sainat.h: 269
class struct__sai_nat_entry_key_t(Structure):
    pass

struct__sai_nat_entry_key_t.__slots__ = [
    'src_ip',
    'dst_ip',
    'proto',
    'l4_src_port',
    'l4_dst_port',
]
struct__sai_nat_entry_key_t._fields_ = [
    ('src_ip', sai_ip4_t),
    ('dst_ip', sai_ip4_t),
    ('proto', sai_uint8_t),
    ('l4_src_port', sai_uint16_t),
    ('l4_dst_port', sai_uint16_t),
]

sai_nat_entry_key_t = struct__sai_nat_entry_key_t# /home/bluecmd/Downloads/SAI/inc/sainat.h: 269

# /home/bluecmd/Downloads/SAI/inc/sainat.h: 301
class struct__sai_nat_entry_mask_t(Structure):
    pass

struct__sai_nat_entry_mask_t.__slots__ = [
    'src_ip',
    'dst_ip',
    'proto',
    'l4_src_port',
    'l4_dst_port',
]
struct__sai_nat_entry_mask_t._fields_ = [
    ('src_ip', sai_ip4_t),
    ('dst_ip', sai_ip4_t),
    ('proto', sai_uint8_t),
    ('l4_src_port', sai_uint16_t),
    ('l4_dst_port', sai_uint16_t),
]

sai_nat_entry_mask_t = struct__sai_nat_entry_mask_t# /home/bluecmd/Downloads/SAI/inc/sainat.h: 301

# /home/bluecmd/Downloads/SAI/inc/sainat.h: 315
class struct__sai_nat_entry_data_t(Structure):
    pass

struct__sai_nat_entry_data_t.__slots__ = [
    'key',
    'mask',
]
struct__sai_nat_entry_data_t._fields_ = [
    ('key', sai_nat_entry_key_t),
    ('mask', sai_nat_entry_mask_t),
]

sai_nat_entry_data_t = struct__sai_nat_entry_data_t# /home/bluecmd/Downloads/SAI/inc/sainat.h: 315

# /home/bluecmd/Downloads/SAI/inc/sainat.h: 346
class struct__sai_nat_entry_t(Structure):
    pass

struct__sai_nat_entry_t.__slots__ = [
    'switch_id',
    'vr_id',
    'nat_type',
    'data',
]
struct__sai_nat_entry_t._fields_ = [
    ('switch_id', sai_object_id_t),
    ('vr_id', sai_object_id_t),
    ('nat_type', sai_nat_type_t),
    ('data', sai_nat_entry_data_t),
]

sai_nat_entry_t = struct__sai_nat_entry_t# /home/bluecmd/Downloads/SAI/inc/sainat.h: 346

enum__sai_nat_event_t = c_int# /home/bluecmd/Downloads/SAI/inc/sainat.h: 359

SAI_NAT_EVENT_NONE = 0# /home/bluecmd/Downloads/SAI/inc/sainat.h: 359

SAI_NAT_EVENT_AGED = (SAI_NAT_EVENT_NONE + 1)# /home/bluecmd/Downloads/SAI/inc/sainat.h: 359

sai_nat_event_t = enum__sai_nat_event_t# /home/bluecmd/Downloads/SAI/inc/sainat.h: 359

# /home/bluecmd/Downloads/SAI/inc/sainat.h: 374
class struct__sai_nat_event_notification_data_t(Structure):
    pass

struct__sai_nat_event_notification_data_t.__slots__ = [
    'event_type',
    'nat_entry',
]
struct__sai_nat_event_notification_data_t._fields_ = [
    ('event_type', sai_nat_event_t),
    ('nat_entry', sai_nat_entry_t),
]

sai_nat_event_notification_data_t = struct__sai_nat_event_notification_data_t# /home/bluecmd/Downloads/SAI/inc/sainat.h: 374

sai_create_nat_entry_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_nat_entry_t), uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/sainat.h: 385

sai_remove_nat_entry_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_nat_entry_t))# /home/bluecmd/Downloads/SAI/inc/sainat.h: 397

sai_set_nat_entry_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_nat_entry_t), POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/sainat.h: 408

sai_get_nat_entry_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_nat_entry_t), uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/sainat.h: 421

sai_nat_event_notification_fn = CFUNCTYPE(UNCHECKED(None), uint32_t, POINTER(sai_nat_event_notification_data_t))# /home/bluecmd/Downloads/SAI/inc/sainat.h: 434

sai_bulk_create_nat_entry_fn = CFUNCTYPE(UNCHECKED(sai_status_t), uint32_t, POINTER(sai_nat_entry_t), POINTER(uint32_t), POINTER(POINTER(sai_attribute_t)), sai_bulk_op_error_mode_t, POINTER(sai_status_t))# /home/bluecmd/Downloads/SAI/inc/sainat.h: 455

sai_bulk_remove_nat_entry_fn = CFUNCTYPE(UNCHECKED(sai_status_t), uint32_t, POINTER(sai_nat_entry_t), sai_bulk_op_error_mode_t, POINTER(sai_status_t))# /home/bluecmd/Downloads/SAI/inc/sainat.h: 477

sai_bulk_set_nat_entry_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), uint32_t, POINTER(sai_nat_entry_t), POINTER(sai_attribute_t), sai_bulk_op_error_mode_t, POINTER(sai_status_t))# /home/bluecmd/Downloads/SAI/inc/sainat.h: 498

sai_bulk_get_nat_entry_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), uint32_t, POINTER(sai_nat_entry_t), POINTER(uint32_t), POINTER(POINTER(sai_attribute_t)), sai_bulk_op_error_mode_t, POINTER(sai_status_t))# /home/bluecmd/Downloads/SAI/inc/sainat.h: 522

enum__sai_nat_zone_counter_attr_t = c_int# /home/bluecmd/Downloads/SAI/inc/sainat.h: 623

SAI_NAT_ZONE_COUNTER_ATTR_START = 0# /home/bluecmd/Downloads/SAI/inc/sainat.h: 623

SAI_NAT_ZONE_COUNTER_ATTR_NAT_TYPE = SAI_NAT_ZONE_COUNTER_ATTR_START# /home/bluecmd/Downloads/SAI/inc/sainat.h: 623

SAI_NAT_ZONE_COUNTER_ATTR_ZONE_ID = (SAI_NAT_ZONE_COUNTER_ATTR_NAT_TYPE + 1)# /home/bluecmd/Downloads/SAI/inc/sainat.h: 623

SAI_NAT_ZONE_COUNTER_ATTR_ENABLE_DISCARD = (SAI_NAT_ZONE_COUNTER_ATTR_ZONE_ID + 1)# /home/bluecmd/Downloads/SAI/inc/sainat.h: 623

SAI_NAT_ZONE_COUNTER_ATTR_DISCARD_PACKET_COUNT = (SAI_NAT_ZONE_COUNTER_ATTR_ENABLE_DISCARD + 1)# /home/bluecmd/Downloads/SAI/inc/sainat.h: 623

SAI_NAT_ZONE_COUNTER_ATTR_ENABLE_TRANSLATION_NEEDED = (SAI_NAT_ZONE_COUNTER_ATTR_DISCARD_PACKET_COUNT + 1)# /home/bluecmd/Downloads/SAI/inc/sainat.h: 623

SAI_NAT_ZONE_COUNTER_ATTR_TRANSLATION_NEEDED_PACKET_COUNT = (SAI_NAT_ZONE_COUNTER_ATTR_ENABLE_TRANSLATION_NEEDED + 1)# /home/bluecmd/Downloads/SAI/inc/sainat.h: 623

SAI_NAT_ZONE_COUNTER_ATTR_ENABLE_TRANSLATIONS = (SAI_NAT_ZONE_COUNTER_ATTR_TRANSLATION_NEEDED_PACKET_COUNT + 1)# /home/bluecmd/Downloads/SAI/inc/sainat.h: 623

SAI_NAT_ZONE_COUNTER_ATTR_TRANSLATIONS_PACKET_COUNT = (SAI_NAT_ZONE_COUNTER_ATTR_ENABLE_TRANSLATIONS + 1)# /home/bluecmd/Downloads/SAI/inc/sainat.h: 623

SAI_NAT_ZONE_COUNTER_ATTR_END = (SAI_NAT_ZONE_COUNTER_ATTR_TRANSLATIONS_PACKET_COUNT + 1)# /home/bluecmd/Downloads/SAI/inc/sainat.h: 623

SAI_NAT_ZONE_COUNTER_ATTR_CUSTOM_RANGE_START = 0x10000000# /home/bluecmd/Downloads/SAI/inc/sainat.h: 623

SAI_NAT_ZONE_COUNTER_ATTR_CUSTOM_RANGE_END = (SAI_NAT_ZONE_COUNTER_ATTR_CUSTOM_RANGE_START + 1)# /home/bluecmd/Downloads/SAI/inc/sainat.h: 623

sai_nat_zone_counter_attr_t = enum__sai_nat_zone_counter_attr_t# /home/bluecmd/Downloads/SAI/inc/sainat.h: 623

sai_create_nat_zone_counter_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/sainat.h: 635

sai_remove_nat_zone_counter_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t)# /home/bluecmd/Downloads/SAI/inc/sainat.h: 650

sai_set_nat_zone_counter_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/sainat.h: 661

sai_get_nat_zone_counter_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/sainat.h: 674

# /home/bluecmd/Downloads/SAI/inc/sainat.h: 701
class struct__sai_nat_api_t(Structure):
    pass

struct__sai_nat_api_t.__slots__ = [
    'create_nat_entry',
    'remove_nat_entry',
    'set_nat_entry_attribute',
    'get_nat_entry_attribute',
    'create_nat_entries',
    'remove_nat_entries',
    'set_nat_entries_attribute',
    'get_nat_entries_attribute',
    'create_nat_zone_counter',
    'remove_nat_zone_counter',
    'set_nat_zone_counter_attribute',
    'get_nat_zone_counter_attribute',
]
struct__sai_nat_api_t._fields_ = [
    ('create_nat_entry', sai_create_nat_entry_fn),
    ('remove_nat_entry', sai_remove_nat_entry_fn),
    ('set_nat_entry_attribute', sai_set_nat_entry_attribute_fn),
    ('get_nat_entry_attribute', sai_get_nat_entry_attribute_fn),
    ('create_nat_entries', sai_bulk_create_nat_entry_fn),
    ('remove_nat_entries', sai_bulk_remove_nat_entry_fn),
    ('set_nat_entries_attribute', sai_bulk_set_nat_entry_attribute_fn),
    ('get_nat_entries_attribute', sai_bulk_get_nat_entry_attribute_fn),
    ('create_nat_zone_counter', sai_create_nat_zone_counter_fn),
    ('remove_nat_zone_counter', sai_remove_nat_zone_counter_fn),
    ('set_nat_zone_counter_attribute', sai_set_nat_zone_counter_attribute_fn),
    ('get_nat_zone_counter_attribute', sai_get_nat_zone_counter_attribute_fn),
]

sai_nat_api_t = struct__sai_nat_api_t# /home/bluecmd/Downloads/SAI/inc/sainat.h: 701

enum__sai_srv6_sidlist_type_t = c_int# /home/bluecmd/Downloads/SAI/inc/saisrv6.h: 56

SAI_SRV6_SIDLIST_TYPE_INSERT = 0# /home/bluecmd/Downloads/SAI/inc/saisrv6.h: 56

SAI_SRV6_SIDLIST_TYPE_INSERT_RED = (SAI_SRV6_SIDLIST_TYPE_INSERT + 1)# /home/bluecmd/Downloads/SAI/inc/saisrv6.h: 56

SAI_SRV6_SIDLIST_TYPE_ENCAPS = (SAI_SRV6_SIDLIST_TYPE_INSERT_RED + 1)# /home/bluecmd/Downloads/SAI/inc/saisrv6.h: 56

SAI_SRV6_SIDLIST_TYPE_ENCAPS_RED = (SAI_SRV6_SIDLIST_TYPE_ENCAPS + 1)# /home/bluecmd/Downloads/SAI/inc/saisrv6.h: 56

SAI_SRV6_SIDLIST_TYPE_CUSTOM_RANGE_BASE = 0x10000000# /home/bluecmd/Downloads/SAI/inc/saisrv6.h: 56

sai_srv6_sidlist_type_t = enum__sai_srv6_sidlist_type_t# /home/bluecmd/Downloads/SAI/inc/saisrv6.h: 56

enum__sai_my_sid_entry_endpoint_behavior_t = c_int# /home/bluecmd/Downloads/SAI/inc/saisrv6.h: 111

SAI_MY_SID_ENTRY_ENDPOINT_BEHAVIOR_E = 0# /home/bluecmd/Downloads/SAI/inc/saisrv6.h: 111

SAI_MY_SID_ENTRY_ENDPOINT_BEHAVIOR_X = (SAI_MY_SID_ENTRY_ENDPOINT_BEHAVIOR_E + 1)# /home/bluecmd/Downloads/SAI/inc/saisrv6.h: 111

SAI_MY_SID_ENTRY_ENDPOINT_BEHAVIOR_T = (SAI_MY_SID_ENTRY_ENDPOINT_BEHAVIOR_X + 1)# /home/bluecmd/Downloads/SAI/inc/saisrv6.h: 111

SAI_MY_SID_ENTRY_ENDPOINT_BEHAVIOR_DX6 = (SAI_MY_SID_ENTRY_ENDPOINT_BEHAVIOR_T + 1)# /home/bluecmd/Downloads/SAI/inc/saisrv6.h: 111

SAI_MY_SID_ENTRY_ENDPOINT_BEHAVIOR_DX4 = (SAI_MY_SID_ENTRY_ENDPOINT_BEHAVIOR_DX6 + 1)# /home/bluecmd/Downloads/SAI/inc/saisrv6.h: 111

SAI_MY_SID_ENTRY_ENDPOINT_BEHAVIOR_DT6 = (SAI_MY_SID_ENTRY_ENDPOINT_BEHAVIOR_DX4 + 1)# /home/bluecmd/Downloads/SAI/inc/saisrv6.h: 111

SAI_MY_SID_ENTRY_ENDPOINT_BEHAVIOR_DT4 = (SAI_MY_SID_ENTRY_ENDPOINT_BEHAVIOR_DT6 + 1)# /home/bluecmd/Downloads/SAI/inc/saisrv6.h: 111

SAI_MY_SID_ENTRY_ENDPOINT_BEHAVIOR_DT46 = (SAI_MY_SID_ENTRY_ENDPOINT_BEHAVIOR_DT4 + 1)# /home/bluecmd/Downloads/SAI/inc/saisrv6.h: 111

SAI_MY_SID_ENTRY_ENDPOINT_BEHAVIOR_B6_ENCAPS = (SAI_MY_SID_ENTRY_ENDPOINT_BEHAVIOR_DT46 + 1)# /home/bluecmd/Downloads/SAI/inc/saisrv6.h: 111

SAI_MY_SID_ENTRY_ENDPOINT_BEHAVIOR_B6_ENCAPS_RED = (SAI_MY_SID_ENTRY_ENDPOINT_BEHAVIOR_B6_ENCAPS + 1)# /home/bluecmd/Downloads/SAI/inc/saisrv6.h: 111

SAI_MY_SID_ENTRY_ENDPOINT_BEHAVIOR_B6_INSERT = (SAI_MY_SID_ENTRY_ENDPOINT_BEHAVIOR_B6_ENCAPS_RED + 1)# /home/bluecmd/Downloads/SAI/inc/saisrv6.h: 111

SAI_MY_SID_ENTRY_ENDPOINT_BEHAVIOR_B6_INSERT_RED = (SAI_MY_SID_ENTRY_ENDPOINT_BEHAVIOR_B6_INSERT + 1)# /home/bluecmd/Downloads/SAI/inc/saisrv6.h: 111

SAI_MY_SID_ENTRY_ENDPOINT_BEHAVIOR_UN = (SAI_MY_SID_ENTRY_ENDPOINT_BEHAVIOR_B6_INSERT_RED + 1)# /home/bluecmd/Downloads/SAI/inc/saisrv6.h: 111

SAI_MY_SID_ENTRY_ENDPOINT_BEHAVIOR_UA = (SAI_MY_SID_ENTRY_ENDPOINT_BEHAVIOR_UN + 1)# /home/bluecmd/Downloads/SAI/inc/saisrv6.h: 111

SAI_MY_SID_ENTRY_ENDPOINT_BEHAVIOR_CUSTOM_RANGE_START = 0x10000000# /home/bluecmd/Downloads/SAI/inc/saisrv6.h: 111

SAI_MY_SID_ENTRY_ENDPOINT_BEHAVIOR_CUSTOM_RANGE_END = (SAI_MY_SID_ENTRY_ENDPOINT_BEHAVIOR_CUSTOM_RANGE_START + 1)# /home/bluecmd/Downloads/SAI/inc/saisrv6.h: 111

sai_my_sid_entry_endpoint_behavior_t = enum__sai_my_sid_entry_endpoint_behavior_t# /home/bluecmd/Downloads/SAI/inc/saisrv6.h: 111

enum__sai_my_sid_entry_endpoint_behavior_flavor_t = c_int# /home/bluecmd/Downloads/SAI/inc/saisrv6.h: 142

SAI_MY_SID_ENTRY_ENDPOINT_BEHAVIOR_FLAVOR_NONE = 0# /home/bluecmd/Downloads/SAI/inc/saisrv6.h: 142

SAI_MY_SID_ENTRY_ENDPOINT_BEHAVIOR_FLAVOR_PSP = (SAI_MY_SID_ENTRY_ENDPOINT_BEHAVIOR_FLAVOR_NONE + 1)# /home/bluecmd/Downloads/SAI/inc/saisrv6.h: 142

SAI_MY_SID_ENTRY_ENDPOINT_BEHAVIOR_FLAVOR_USP = (SAI_MY_SID_ENTRY_ENDPOINT_BEHAVIOR_FLAVOR_PSP + 1)# /home/bluecmd/Downloads/SAI/inc/saisrv6.h: 142

SAI_MY_SID_ENTRY_ENDPOINT_BEHAVIOR_FLAVOR_USD = (SAI_MY_SID_ENTRY_ENDPOINT_BEHAVIOR_FLAVOR_USP + 1)# /home/bluecmd/Downloads/SAI/inc/saisrv6.h: 142

SAI_MY_SID_ENTRY_ENDPOINT_BEHAVIOR_FLAVOR_PSP_AND_USP = (SAI_MY_SID_ENTRY_ENDPOINT_BEHAVIOR_FLAVOR_USD + 1)# /home/bluecmd/Downloads/SAI/inc/saisrv6.h: 142

SAI_MY_SID_ENTRY_ENDPOINT_BEHAVIOR_FLAVOR_USD_AND_USP = (SAI_MY_SID_ENTRY_ENDPOINT_BEHAVIOR_FLAVOR_PSP_AND_USP + 1)# /home/bluecmd/Downloads/SAI/inc/saisrv6.h: 142

SAI_MY_SID_ENTRY_ENDPOINT_BEHAVIOR_FLAVOR_PSP_AND_USD = (SAI_MY_SID_ENTRY_ENDPOINT_BEHAVIOR_FLAVOR_USD_AND_USP + 1)# /home/bluecmd/Downloads/SAI/inc/saisrv6.h: 142

SAI_MY_SID_ENTRY_ENDPOINT_BEHAVIOR_FLAVOR_PSP_AND_USP_AND_USD = (SAI_MY_SID_ENTRY_ENDPOINT_BEHAVIOR_FLAVOR_PSP_AND_USD + 1)# /home/bluecmd/Downloads/SAI/inc/saisrv6.h: 142

sai_my_sid_entry_endpoint_behavior_flavor_t = enum__sai_my_sid_entry_endpoint_behavior_flavor_t# /home/bluecmd/Downloads/SAI/inc/saisrv6.h: 142

enum__sai_srv6_sidlist_attr_t = c_int# /home/bluecmd/Downloads/SAI/inc/saisrv6.h: 201

SAI_SRV6_SIDLIST_ATTR_START = 0x00000000# /home/bluecmd/Downloads/SAI/inc/saisrv6.h: 201

SAI_SRV6_SIDLIST_ATTR_TYPE = SAI_SRV6_SIDLIST_ATTR_START# /home/bluecmd/Downloads/SAI/inc/saisrv6.h: 201

SAI_SRV6_SIDLIST_ATTR_TLV_LIST = (SAI_SRV6_SIDLIST_ATTR_TYPE + 1)# /home/bluecmd/Downloads/SAI/inc/saisrv6.h: 201

SAI_SRV6_SIDLIST_ATTR_SEGMENT_LIST = (SAI_SRV6_SIDLIST_ATTR_TLV_LIST + 1)# /home/bluecmd/Downloads/SAI/inc/saisrv6.h: 201

SAI_SRV6_SIDLIST_ATTR_NEXT_HOP_ID = (SAI_SRV6_SIDLIST_ATTR_SEGMENT_LIST + 1)# /home/bluecmd/Downloads/SAI/inc/saisrv6.h: 201

SAI_SRV6_SIDLIST_ATTR_END = (SAI_SRV6_SIDLIST_ATTR_NEXT_HOP_ID + 1)# /home/bluecmd/Downloads/SAI/inc/saisrv6.h: 201

SAI_SRV6_SIDLIST_ATTR_CUSTOM_RANGE_START = 0x10000000# /home/bluecmd/Downloads/SAI/inc/saisrv6.h: 201

SAI_SRV6_SIDLIST_ATTR_CUSTOM_RANGE_END = (SAI_SRV6_SIDLIST_ATTR_CUSTOM_RANGE_START + 1)# /home/bluecmd/Downloads/SAI/inc/saisrv6.h: 201

sai_srv6_sidlist_attr_t = enum__sai_srv6_sidlist_attr_t# /home/bluecmd/Downloads/SAI/inc/saisrv6.h: 201

enum__sai_srv6_sidlist_stat_t = c_int# /home/bluecmd/Downloads/SAI/inc/saisrv6.h: 213

SAI_SRV6_SIDLIST_STAT_OUT_PACKETS = 0# /home/bluecmd/Downloads/SAI/inc/saisrv6.h: 213

SAI_SRV6_SIDLIST_STAT_OUT_OCTETS = (SAI_SRV6_SIDLIST_STAT_OUT_PACKETS + 1)# /home/bluecmd/Downloads/SAI/inc/saisrv6.h: 213

sai_srv6_sidlist_stat_t = enum__sai_srv6_sidlist_stat_t# /home/bluecmd/Downloads/SAI/inc/saisrv6.h: 213

sai_create_srv6_sidlist_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saisrv6.h: 225

sai_remove_srv6_sidlist_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t)# /home/bluecmd/Downloads/SAI/inc/saisrv6.h: 238

sai_set_srv6_sidlist_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saisrv6.h: 249

sai_get_srv6_sidlist_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saisrv6.h: 262

sai_get_srv6_sidlist_stats_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, uint32_t, POINTER(sai_stat_id_t), POINTER(uint64_t))# /home/bluecmd/Downloads/SAI/inc/saisrv6.h: 277

sai_get_srv6_sidlist_stats_ext_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, uint32_t, POINTER(sai_stat_id_t), sai_stats_mode_t, POINTER(uint64_t))# /home/bluecmd/Downloads/SAI/inc/saisrv6.h: 294

sai_clear_srv6_sidlist_stats_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, uint32_t, POINTER(sai_stat_id_t))# /home/bluecmd/Downloads/SAI/inc/saisrv6.h: 310

enum__sai_my_sid_entry_attr_t = c_int# /home/bluecmd/Downloads/SAI/inc/saisrv6.h: 421

SAI_MY_SID_ENTRY_ATTR_START = 0# /home/bluecmd/Downloads/SAI/inc/saisrv6.h: 421

SAI_MY_SID_ENTRY_ATTR_ENDPOINT_BEHAVIOR = SAI_MY_SID_ENTRY_ATTR_START# /home/bluecmd/Downloads/SAI/inc/saisrv6.h: 421

SAI_MY_SID_ENTRY_ATTR_ENDPOINT_BEHAVIOR_FLAVOR = (SAI_MY_SID_ENTRY_ATTR_ENDPOINT_BEHAVIOR + 1)# /home/bluecmd/Downloads/SAI/inc/saisrv6.h: 421

SAI_MY_SID_ENTRY_ATTR_PACKET_ACTION = (SAI_MY_SID_ENTRY_ATTR_ENDPOINT_BEHAVIOR_FLAVOR + 1)# /home/bluecmd/Downloads/SAI/inc/saisrv6.h: 421

SAI_MY_SID_ENTRY_ATTR_TRAP_PRIORITY = (SAI_MY_SID_ENTRY_ATTR_PACKET_ACTION + 1)# /home/bluecmd/Downloads/SAI/inc/saisrv6.h: 421

SAI_MY_SID_ENTRY_ATTR_NEXT_HOP_ID = (SAI_MY_SID_ENTRY_ATTR_TRAP_PRIORITY + 1)# /home/bluecmd/Downloads/SAI/inc/saisrv6.h: 421

SAI_MY_SID_ENTRY_ATTR_TUNNEL_ID = (SAI_MY_SID_ENTRY_ATTR_NEXT_HOP_ID + 1)# /home/bluecmd/Downloads/SAI/inc/saisrv6.h: 421

SAI_MY_SID_ENTRY_ATTR_VRF = (SAI_MY_SID_ENTRY_ATTR_TUNNEL_ID + 1)# /home/bluecmd/Downloads/SAI/inc/saisrv6.h: 421

SAI_MY_SID_ENTRY_ATTR_COUNTER_ID = (SAI_MY_SID_ENTRY_ATTR_VRF + 1)# /home/bluecmd/Downloads/SAI/inc/saisrv6.h: 421

SAI_MY_SID_ENTRY_ATTR_END = (SAI_MY_SID_ENTRY_ATTR_COUNTER_ID + 1)# /home/bluecmd/Downloads/SAI/inc/saisrv6.h: 421

SAI_MY_SID_ENTRY_ATTR_CUSTOM_RANGE_START = 0x10000000# /home/bluecmd/Downloads/SAI/inc/saisrv6.h: 421

SAI_MY_SID_ENTRY_ATTR_CUSTOM_RANGE_END = (SAI_MY_SID_ENTRY_ATTR_CUSTOM_RANGE_START + 1)# /home/bluecmd/Downloads/SAI/inc/saisrv6.h: 421

sai_my_sid_entry_attr_t = enum__sai_my_sid_entry_attr_t# /home/bluecmd/Downloads/SAI/inc/saisrv6.h: 421

# /home/bluecmd/Downloads/SAI/inc/saisrv6.h: 467
class struct__sai_my_sid_entry_t(Structure):
    pass

struct__sai_my_sid_entry_t.__slots__ = [
    'switch_id',
    'vr_id',
    'locator_block_len',
    'locator_node_len',
    'function_len',
    'args_len',
    'sid',
]
struct__sai_my_sid_entry_t._fields_ = [
    ('switch_id', sai_object_id_t),
    ('vr_id', sai_object_id_t),
    ('locator_block_len', sai_uint8_t),
    ('locator_node_len', sai_uint8_t),
    ('function_len', sai_uint8_t),
    ('args_len', sai_uint8_t),
    ('sid', sai_ip6_t),
]

sai_my_sid_entry_t = struct__sai_my_sid_entry_t# /home/bluecmd/Downloads/SAI/inc/saisrv6.h: 467

sai_create_my_sid_entry_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_my_sid_entry_t), uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saisrv6.h: 478

sai_remove_my_sid_entry_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_my_sid_entry_t))# /home/bluecmd/Downloads/SAI/inc/saisrv6.h: 490

sai_set_my_sid_entry_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_my_sid_entry_t), POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saisrv6.h: 501

sai_get_my_sid_entry_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_my_sid_entry_t), uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saisrv6.h: 514

sai_bulk_create_my_sid_entry_fn = CFUNCTYPE(UNCHECKED(sai_status_t), uint32_t, POINTER(sai_my_sid_entry_t), POINTER(uint32_t), POINTER(POINTER(sai_attribute_t)), sai_bulk_op_error_mode_t, POINTER(sai_status_t))# /home/bluecmd/Downloads/SAI/inc/saisrv6.h: 536

sai_bulk_remove_my_sid_entry_fn = CFUNCTYPE(UNCHECKED(sai_status_t), uint32_t, POINTER(sai_my_sid_entry_t), sai_bulk_op_error_mode_t, POINTER(sai_status_t))# /home/bluecmd/Downloads/SAI/inc/saisrv6.h: 558

sai_bulk_set_my_sid_entry_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), uint32_t, POINTER(sai_my_sid_entry_t), POINTER(sai_attribute_t), sai_bulk_op_error_mode_t, POINTER(sai_status_t))# /home/bluecmd/Downloads/SAI/inc/saisrv6.h: 579

sai_bulk_get_my_sid_entry_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), uint32_t, POINTER(sai_my_sid_entry_t), POINTER(uint32_t), POINTER(POINTER(sai_attribute_t)), sai_bulk_op_error_mode_t, POINTER(sai_status_t))# /home/bluecmd/Downloads/SAI/inc/saisrv6.h: 603

# /home/bluecmd/Downloads/SAI/inc/saisrv6.h: 637
class struct__sai_srv6_api_t(Structure):
    pass

struct__sai_srv6_api_t.__slots__ = [
    'create_srv6_sidlist',
    'remove_srv6_sidlist',
    'set_srv6_sidlist_attribute',
    'get_srv6_sidlist_attribute',
    'create_srv6_sidlists',
    'remove_srv6_sidlists',
    'get_srv6_sidlist_stats',
    'get_srv6_sidlist_stats_ext',
    'clear_srv6_sidlist_stats',
    'create_my_sid_entry',
    'remove_my_sid_entry',
    'set_my_sid_entry_attribute',
    'get_my_sid_entry_attribute',
    'create_my_sid_entries',
    'remove_my_sid_entries',
    'set_my_sid_entries_attribute',
    'get_my_sid_entries_attribute',
]
struct__sai_srv6_api_t._fields_ = [
    ('create_srv6_sidlist', sai_create_srv6_sidlist_fn),
    ('remove_srv6_sidlist', sai_remove_srv6_sidlist_fn),
    ('set_srv6_sidlist_attribute', sai_set_srv6_sidlist_attribute_fn),
    ('get_srv6_sidlist_attribute', sai_get_srv6_sidlist_attribute_fn),
    ('create_srv6_sidlists', sai_bulk_object_create_fn),
    ('remove_srv6_sidlists', sai_bulk_object_remove_fn),
    ('get_srv6_sidlist_stats', sai_get_srv6_sidlist_stats_fn),
    ('get_srv6_sidlist_stats_ext', sai_get_srv6_sidlist_stats_ext_fn),
    ('clear_srv6_sidlist_stats', sai_clear_srv6_sidlist_stats_fn),
    ('create_my_sid_entry', sai_create_my_sid_entry_fn),
    ('remove_my_sid_entry', sai_remove_my_sid_entry_fn),
    ('set_my_sid_entry_attribute', sai_set_my_sid_entry_attribute_fn),
    ('get_my_sid_entry_attribute', sai_get_my_sid_entry_attribute_fn),
    ('create_my_sid_entries', sai_bulk_create_my_sid_entry_fn),
    ('remove_my_sid_entries', sai_bulk_remove_my_sid_entry_fn),
    ('set_my_sid_entries_attribute', sai_bulk_set_my_sid_entry_attribute_fn),
    ('get_my_sid_entries_attribute', sai_bulk_get_my_sid_entry_attribute_fn),
]

sai_srv6_api_t = struct__sai_srv6_api_t# /home/bluecmd/Downloads/SAI/inc/saisrv6.h: 637

# /home/bluecmd/Downloads/SAI/experimental/saiexperimentaldashvip.h: 62
class struct__sai_vip_entry_t(Structure):
    pass

struct__sai_vip_entry_t.__slots__ = [
    'switch_id',
    'vip',
]
struct__sai_vip_entry_t._fields_ = [
    ('switch_id', sai_object_id_t),
    ('vip', sai_ip_address_t),
]

sai_vip_entry_t = struct__sai_vip_entry_t# /home/bluecmd/Downloads/SAI/experimental/saiexperimentaldashvip.h: 62

# /home/bluecmd/Downloads/SAI/experimental/saiexperimentaldashpavalidation.h: 69
class struct__sai_pa_validation_entry_t(Structure):
    pass

struct__sai_pa_validation_entry_t.__slots__ = [
    'switch_id',
    'vnet_id',
    'sip',
]
struct__sai_pa_validation_entry_t._fields_ = [
    ('switch_id', sai_object_id_t),
    ('vnet_id', sai_object_id_t),
    ('sip', sai_ip_address_t),
]

sai_pa_validation_entry_t = struct__sai_pa_validation_entry_t# /home/bluecmd/Downloads/SAI/experimental/saiexperimentaldashpavalidation.h: 69

# /home/bluecmd/Downloads/SAI/experimental/saiexperimentaldashoutboundrouting.h: 77
class struct__sai_outbound_routing_entry_t(Structure):
    pass

struct__sai_outbound_routing_entry_t.__slots__ = [
    'switch_id',
    'eni_id',
    'destination',
]
struct__sai_outbound_routing_entry_t._fields_ = [
    ('switch_id', sai_object_id_t),
    ('eni_id', sai_object_id_t),
    ('destination', sai_ip_prefix_t),
]

sai_outbound_routing_entry_t = struct__sai_outbound_routing_entry_t# /home/bluecmd/Downloads/SAI/experimental/saiexperimentaldashoutboundrouting.h: 77

# /home/bluecmd/Downloads/SAI/experimental/saiexperimentaldashoutboundcatopa.h: 71
class struct__sai_outbound_ca_to_pa_entry_t(Structure):
    pass

struct__sai_outbound_ca_to_pa_entry_t.__slots__ = [
    'switch_id',
    'dst_vnet_id',
    'dip',
]
struct__sai_outbound_ca_to_pa_entry_t._fields_ = [
    ('switch_id', sai_object_id_t),
    ('dst_vnet_id', sai_object_id_t),
    ('dip', sai_ip_address_t),
]

sai_outbound_ca_to_pa_entry_t = struct__sai_outbound_ca_to_pa_entry_t# /home/bluecmd/Downloads/SAI/experimental/saiexperimentaldashoutboundcatopa.h: 71

# /home/bluecmd/Downloads/SAI/experimental/saiexperimentaldashinboundrouting.h: 86
class struct__sai_inbound_routing_entry_t(Structure):
    pass

struct__sai_inbound_routing_entry_t.__slots__ = [
    'switch_id',
    'eni_id',
    'vni',
    'sip',
    'sip_mask',
    'priority',
]
struct__sai_inbound_routing_entry_t._fields_ = [
    ('switch_id', sai_object_id_t),
    ('eni_id', sai_object_id_t),
    ('vni', sai_uint32_t),
    ('sip', sai_ip_address_t),
    ('sip_mask', sai_ip_address_t),
    ('priority', sai_uint32_t),
]

sai_inbound_routing_entry_t = struct__sai_inbound_routing_entry_t# /home/bluecmd/Downloads/SAI/experimental/saiexperimentaldashinboundrouting.h: 86

# /home/bluecmd/Downloads/SAI/experimental/saiexperimentaldasheni.h: 53
class struct__sai_eni_ether_address_map_entry_t(Structure):
    pass

struct__sai_eni_ether_address_map_entry_t.__slots__ = [
    'switch_id',
    'address',
]
struct__sai_eni_ether_address_map_entry_t._fields_ = [
    ('switch_id', sai_object_id_t),
    ('address', sai_mac_t),
]

sai_eni_ether_address_map_entry_t = struct__sai_eni_ether_address_map_entry_t# /home/bluecmd/Downloads/SAI/experimental/saiexperimentaldasheni.h: 53

# /home/bluecmd/Downloads/SAI/experimental/saiexperimentaldashdirectionlookup.h: 62
class struct__sai_direction_lookup_entry_t(Structure):
    pass

struct__sai_direction_lookup_entry_t.__slots__ = [
    'switch_id',
    'vni',
]
struct__sai_direction_lookup_entry_t._fields_ = [
    ('switch_id', sai_object_id_t),
    ('vni', sai_uint32_t),
]

sai_direction_lookup_entry_t = struct__sai_direction_lookup_entry_t# /home/bluecmd/Downloads/SAI/experimental/saiexperimentaldashdirectionlookup.h: 62

# /home/bluecmd/Downloads/SAI/inc/saiobject.h: 119
class union__sai_object_key_entry_t(Union):
    pass

union__sai_object_key_entry_t.__slots__ = [
    'object_id',
    'fdb_entry',
    'neighbor_entry',
    'route_entry',
    'mcast_fdb_entry',
    'l2mc_entry',
    'ipmc_entry',
    'inseg_entry',
    'nat_entry',
    'my_sid_entry',
    'direction_lookup_entry',
    'eni_ether_address_map_entry',
    'inbound_routing_entry',
    'outbound_ca_to_pa_entry',
    'outbound_routing_entry',
    'pa_validation_entry',
    'vip_entry',
]
union__sai_object_key_entry_t._fields_ = [
    ('object_id', sai_object_id_t),
    ('fdb_entry', sai_fdb_entry_t),
    ('neighbor_entry', sai_neighbor_entry_t),
    ('route_entry', sai_route_entry_t),
    ('mcast_fdb_entry', sai_mcast_fdb_entry_t),
    ('l2mc_entry', sai_l2mc_entry_t),
    ('ipmc_entry', sai_ipmc_entry_t),
    ('inseg_entry', sai_inseg_entry_t),
    ('nat_entry', sai_nat_entry_t),
    ('my_sid_entry', sai_my_sid_entry_t),
    ('direction_lookup_entry', sai_direction_lookup_entry_t),
    ('eni_ether_address_map_entry', sai_eni_ether_address_map_entry_t),
    ('inbound_routing_entry', sai_inbound_routing_entry_t),
    ('outbound_ca_to_pa_entry', sai_outbound_ca_to_pa_entry_t),
    ('outbound_routing_entry', sai_outbound_routing_entry_t),
    ('pa_validation_entry', sai_pa_validation_entry_t),
    ('vip_entry', sai_vip_entry_t),
]

sai_object_key_entry_t = union__sai_object_key_entry_t# /home/bluecmd/Downloads/SAI/inc/saiobject.h: 119

# /home/bluecmd/Downloads/SAI/inc/saiobject.h: 133
class struct__sai_object_key_t(Structure):
    pass

struct__sai_object_key_t.__slots__ = [
    'key',
]
struct__sai_object_key_t._fields_ = [
    ('key', sai_object_key_entry_t),
]

sai_object_key_t = struct__sai_object_key_t# /home/bluecmd/Downloads/SAI/inc/saiobject.h: 133

# /home/bluecmd/Downloads/SAI/inc/saiobject.h: 155
class struct__sai_attr_capability_t(Structure):
    pass

struct__sai_attr_capability_t.__slots__ = [
    'create_implemented',
    'set_implemented',
    'get_implemented',
]
struct__sai_attr_capability_t._fields_ = [
    ('create_implemented', c_bool),
    ('set_implemented', c_bool),
    ('get_implemented', c_bool),
]

sai_attr_capability_t = struct__sai_attr_capability_t# /home/bluecmd/Downloads/SAI/inc/saiobject.h: 155

# /home/bluecmd/Downloads/SAI/inc/saiobject.h: 166
for _lib in _libs.values():
    if not _lib.has("sai_get_maximum_attribute_count", "cdecl"):
        continue
    sai_get_maximum_attribute_count = _lib.get("sai_get_maximum_attribute_count", "cdecl")
    sai_get_maximum_attribute_count.argtypes = [sai_object_id_t, sai_object_type_t, POINTER(uint32_t)]
    sai_get_maximum_attribute_count.restype = sai_status_t
    break

# /home/bluecmd/Downloads/SAI/inc/saiobject.h: 180
for _lib in _libs.values():
    if not _lib.has("sai_get_object_count", "cdecl"):
        continue
    sai_get_object_count = _lib.get("sai_get_object_count", "cdecl")
    sai_get_object_count.argtypes = [sai_object_id_t, sai_object_type_t, POINTER(uint32_t)]
    sai_get_object_count.restype = sai_status_t
    break

# /home/bluecmd/Downloads/SAI/inc/saiobject.h: 196
for _lib in _libs.values():
    if not _lib.has("sai_get_object_key", "cdecl"):
        continue
    sai_get_object_key = _lib.get("sai_get_object_key", "cdecl")
    sai_get_object_key.argtypes = [sai_object_id_t, sai_object_type_t, POINTER(uint32_t), POINTER(sai_object_key_t)]
    sai_get_object_key.restype = sai_status_t
    break

# /home/bluecmd/Downloads/SAI/inc/saiobject.h: 233
for _lib in _libs.values():
    if not _lib.has("sai_bulk_get_attribute", "cdecl"):
        continue
    sai_bulk_get_attribute = _lib.get("sai_bulk_get_attribute", "cdecl")
    sai_bulk_get_attribute.argtypes = [sai_object_id_t, sai_object_type_t, uint32_t, POINTER(sai_object_key_t), POINTER(uint32_t), POINTER(POINTER(sai_attribute_t)), POINTER(sai_status_t)]
    sai_bulk_get_attribute.restype = sai_status_t
    break

# /home/bluecmd/Downloads/SAI/inc/saiobject.h: 252
for _lib in _libs.values():
    if not _lib.has("sai_query_attribute_capability", "cdecl"):
        continue
    sai_query_attribute_capability = _lib.get("sai_query_attribute_capability", "cdecl")
    sai_query_attribute_capability.argtypes = [sai_object_id_t, sai_object_type_t, sai_attr_id_t, POINTER(sai_attr_capability_t)]
    sai_query_attribute_capability.restype = sai_status_t
    break

# /home/bluecmd/Downloads/SAI/inc/saiobject.h: 268
for _lib in _libs.values():
    if not _lib.has("sai_query_attribute_enum_values_capability", "cdecl"):
        continue
    sai_query_attribute_enum_values_capability = _lib.get("sai_query_attribute_enum_values_capability", "cdecl")
    sai_query_attribute_enum_values_capability.argtypes = [sai_object_id_t, sai_object_type_t, sai_attr_id_t, POINTER(sai_s32_list_t)]
    sai_query_attribute_enum_values_capability.restype = sai_status_t
    break

# /home/bluecmd/Downloads/SAI/inc/saiobject.h: 283
for _lib in _libs.values():
    if not _lib.has("sai_query_stats_capability", "cdecl"):
        continue
    sai_query_stats_capability = _lib.get("sai_query_stats_capability", "cdecl")
    sai_query_stats_capability.argtypes = [sai_object_id_t, sai_object_type_t, POINTER(sai_stat_capability_list_t)]
    sai_query_stats_capability.restype = sai_status_t
    break

# /home/bluecmd/Downloads/SAI/inc/saiobject.h: 305
for _lib in _libs.values():
    if not _lib.has("sai_bulk_object_get_stats", "cdecl"):
        continue
    sai_bulk_object_get_stats = _lib.get("sai_bulk_object_get_stats", "cdecl")
    sai_bulk_object_get_stats.argtypes = [sai_object_id_t, sai_object_type_t, uint32_t, POINTER(sai_object_key_t), uint32_t, POINTER(sai_stat_id_t), sai_stats_mode_t, POINTER(sai_status_t), POINTER(uint64_t)]
    sai_bulk_object_get_stats.restype = sai_status_t
    break

# /home/bluecmd/Downloads/SAI/inc/saiobject.h: 330
for _lib in _libs.values():
    if not _lib.has("sai_bulk_object_clear_stats", "cdecl"):
        continue
    sai_bulk_object_clear_stats = _lib.get("sai_bulk_object_clear_stats", "cdecl")
    sai_bulk_object_clear_stats.argtypes = [sai_object_id_t, sai_object_type_t, uint32_t, POINTER(sai_object_key_t), uint32_t, POINTER(sai_stat_id_t), sai_stats_mode_t, POINTER(sai_status_t)]
    sai_bulk_object_clear_stats.restype = sai_status_t
    break

# /home/bluecmd/Downloads/SAI/inc/saiobject.h: 351
for _lib in _libs.values():
    if not _lib.has("sai_query_object_stage", "cdecl"):
        continue
    sai_query_object_stage = _lib.get("sai_query_object_stage", "cdecl")
    sai_query_object_stage.argtypes = [sai_object_id_t, sai_object_type_t, uint32_t, POINTER(sai_attribute_t), POINTER(sai_object_stage_t)]
    sai_query_object_stage.restype = sai_status_t
    break

enum__sai_meter_type_t = c_int# /home/bluecmd/Downloads/SAI/inc/saipolicer.h: 50

SAI_METER_TYPE_PACKETS = 0x00000000# /home/bluecmd/Downloads/SAI/inc/saipolicer.h: 50

SAI_METER_TYPE_BYTES = 0x00000001# /home/bluecmd/Downloads/SAI/inc/saipolicer.h: 50

SAI_METER_TYPE_CUSTOM_RANGE_BASE = 0x10000000# /home/bluecmd/Downloads/SAI/inc/saipolicer.h: 50

sai_meter_type_t = enum__sai_meter_type_t# /home/bluecmd/Downloads/SAI/inc/saipolicer.h: 50

enum__sai_policer_mode_t = c_int# /home/bluecmd/Downloads/SAI/inc/saipolicer.h: 69

SAI_POLICER_MODE_SR_TCM = 0x00000000# /home/bluecmd/Downloads/SAI/inc/saipolicer.h: 69

SAI_POLICER_MODE_TR_TCM = 0x00000001# /home/bluecmd/Downloads/SAI/inc/saipolicer.h: 69

SAI_POLICER_MODE_STORM_CONTROL = 0x00000002# /home/bluecmd/Downloads/SAI/inc/saipolicer.h: 69

SAI_POLICER_MODE_CUSTOM_RANGE_BASE = 0x10000000# /home/bluecmd/Downloads/SAI/inc/saipolicer.h: 69

sai_policer_mode_t = enum__sai_policer_mode_t# /home/bluecmd/Downloads/SAI/inc/saipolicer.h: 69

enum__sai_policer_color_source_t = c_int# /home/bluecmd/Downloads/SAI/inc/saipolicer.h: 85

SAI_POLICER_COLOR_SOURCE_BLIND = 0x00000000# /home/bluecmd/Downloads/SAI/inc/saipolicer.h: 85

SAI_POLICER_COLOR_SOURCE_AWARE = 0x00000001# /home/bluecmd/Downloads/SAI/inc/saipolicer.h: 85

SAI_POLICER_COLOR_SOURCE_CUSTOM_RANGE_BASE = 0x10000000# /home/bluecmd/Downloads/SAI/inc/saipolicer.h: 85

sai_policer_color_source_t = enum__sai_policer_color_source_t# /home/bluecmd/Downloads/SAI/inc/saipolicer.h: 85

enum__sai_policer_attr_t = c_int# /home/bluecmd/Downloads/SAI/inc/saipolicer.h: 223

SAI_POLICER_ATTR_START = 0x00000000# /home/bluecmd/Downloads/SAI/inc/saipolicer.h: 223

SAI_POLICER_ATTR_METER_TYPE = SAI_POLICER_ATTR_START# /home/bluecmd/Downloads/SAI/inc/saipolicer.h: 223

SAI_POLICER_ATTR_MODE = 0x00000001# /home/bluecmd/Downloads/SAI/inc/saipolicer.h: 223

SAI_POLICER_ATTR_COLOR_SOURCE = 0x00000002# /home/bluecmd/Downloads/SAI/inc/saipolicer.h: 223

SAI_POLICER_ATTR_CBS = 0x00000003# /home/bluecmd/Downloads/SAI/inc/saipolicer.h: 223

SAI_POLICER_ATTR_CIR = 0x00000004# /home/bluecmd/Downloads/SAI/inc/saipolicer.h: 223

SAI_POLICER_ATTR_PBS = 0x00000005# /home/bluecmd/Downloads/SAI/inc/saipolicer.h: 223

SAI_POLICER_ATTR_PIR = 0x00000006# /home/bluecmd/Downloads/SAI/inc/saipolicer.h: 223

SAI_POLICER_ATTR_GREEN_PACKET_ACTION = 0x00000007# /home/bluecmd/Downloads/SAI/inc/saipolicer.h: 223

SAI_POLICER_ATTR_YELLOW_PACKET_ACTION = 0x00000008# /home/bluecmd/Downloads/SAI/inc/saipolicer.h: 223

SAI_POLICER_ATTR_RED_PACKET_ACTION = 0x00000009# /home/bluecmd/Downloads/SAI/inc/saipolicer.h: 223

SAI_POLICER_ATTR_ENABLE_COUNTER_PACKET_ACTION_LIST = 0x0000000a# /home/bluecmd/Downloads/SAI/inc/saipolicer.h: 223

SAI_POLICER_ATTR_OBJECT_STAGE = 0x0000000b# /home/bluecmd/Downloads/SAI/inc/saipolicer.h: 223

SAI_POLICER_ATTR_END = (SAI_POLICER_ATTR_OBJECT_STAGE + 1)# /home/bluecmd/Downloads/SAI/inc/saipolicer.h: 223

SAI_POLICER_ATTR_CUSTOM_RANGE_START = 0x10000000# /home/bluecmd/Downloads/SAI/inc/saipolicer.h: 223

SAI_POLICER_ATTR_CUSTOM_RANGE_END = (SAI_POLICER_ATTR_CUSTOM_RANGE_START + 1)# /home/bluecmd/Downloads/SAI/inc/saipolicer.h: 223

sai_policer_attr_t = enum__sai_policer_attr_t# /home/bluecmd/Downloads/SAI/inc/saipolicer.h: 223

enum__sai_policer_stat_t = c_int# /home/bluecmd/Downloads/SAI/inc/saipolicer.h: 257

SAI_POLICER_STAT_PACKETS = 0x00000000# /home/bluecmd/Downloads/SAI/inc/saipolicer.h: 257

SAI_POLICER_STAT_ATTR_BYTES = 0x00000001# /home/bluecmd/Downloads/SAI/inc/saipolicer.h: 257

SAI_POLICER_STAT_GREEN_PACKETS = 0x00000002# /home/bluecmd/Downloads/SAI/inc/saipolicer.h: 257

SAI_POLICER_STAT_GREEN_BYTES = 0x00000003# /home/bluecmd/Downloads/SAI/inc/saipolicer.h: 257

SAI_POLICER_STAT_YELLOW_PACKETS = 0x00000004# /home/bluecmd/Downloads/SAI/inc/saipolicer.h: 257

SAI_POLICER_STAT_YELLOW_BYTES = 0x00000005# /home/bluecmd/Downloads/SAI/inc/saipolicer.h: 257

SAI_POLICER_STAT_RED_PACKETS = 0x00000006# /home/bluecmd/Downloads/SAI/inc/saipolicer.h: 257

SAI_POLICER_STAT_RED_BYTES = 0x00000007# /home/bluecmd/Downloads/SAI/inc/saipolicer.h: 257

SAI_POLICER_STAT_CUSTOM_RANGE_BASE = 0x10000000# /home/bluecmd/Downloads/SAI/inc/saipolicer.h: 257

sai_policer_stat_t = enum__sai_policer_stat_t# /home/bluecmd/Downloads/SAI/inc/saipolicer.h: 257

sai_create_policer_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saipolicer.h: 269

sai_remove_policer_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t)# /home/bluecmd/Downloads/SAI/inc/saipolicer.h: 282

sai_set_policer_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saipolicer.h: 293

sai_get_policer_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saipolicer.h: 306

sai_get_policer_stats_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, uint32_t, POINTER(sai_stat_id_t), POINTER(uint64_t))# /home/bluecmd/Downloads/SAI/inc/saipolicer.h: 321

sai_get_policer_stats_ext_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, uint32_t, POINTER(sai_stat_id_t), sai_stats_mode_t, POINTER(uint64_t))# /home/bluecmd/Downloads/SAI/inc/saipolicer.h: 338

sai_clear_policer_stats_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, uint32_t, POINTER(sai_stat_id_t))# /home/bluecmd/Downloads/SAI/inc/saipolicer.h: 354

# /home/bluecmd/Downloads/SAI/inc/saipolicer.h: 372
class struct__sai_policer_api_t(Structure):
    pass

struct__sai_policer_api_t.__slots__ = [
    'create_policer',
    'remove_policer',
    'set_policer_attribute',
    'get_policer_attribute',
    'get_policer_stats',
    'get_policer_stats_ext',
    'clear_policer_stats',
]
struct__sai_policer_api_t._fields_ = [
    ('create_policer', sai_create_policer_fn),
    ('remove_policer', sai_remove_policer_fn),
    ('set_policer_attribute', sai_set_policer_attribute_fn),
    ('get_policer_attribute', sai_get_policer_attribute_fn),
    ('get_policer_stats', sai_get_policer_stats_fn),
    ('get_policer_stats_ext', sai_get_policer_stats_ext_fn),
    ('clear_policer_stats', sai_clear_policer_stats_fn),
]

sai_policer_api_t = struct__sai_policer_api_t# /home/bluecmd/Downloads/SAI/inc/saipolicer.h: 372

enum__sai_port_type_t = c_int# /home/bluecmd/Downloads/SAI/inc/saiport.h: 53

SAI_PORT_TYPE_LOGICAL = 0# /home/bluecmd/Downloads/SAI/inc/saiport.h: 53

SAI_PORT_TYPE_CPU = (SAI_PORT_TYPE_LOGICAL + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 53

SAI_PORT_TYPE_FABRIC = (SAI_PORT_TYPE_CPU + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 53

SAI_PORT_TYPE_RECYCLE = (SAI_PORT_TYPE_FABRIC + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 53

sai_port_type_t = enum__sai_port_type_t# /home/bluecmd/Downloads/SAI/inc/saiport.h: 53

enum__sai_port_oper_status_t = c_int# /home/bluecmd/Downloads/SAI/inc/saiport.h: 75

SAI_PORT_OPER_STATUS_UNKNOWN = 0# /home/bluecmd/Downloads/SAI/inc/saiport.h: 75

SAI_PORT_OPER_STATUS_UP = (SAI_PORT_OPER_STATUS_UNKNOWN + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 75

SAI_PORT_OPER_STATUS_DOWN = (SAI_PORT_OPER_STATUS_UP + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 75

SAI_PORT_OPER_STATUS_TESTING = (SAI_PORT_OPER_STATUS_DOWN + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 75

SAI_PORT_OPER_STATUS_NOT_PRESENT = (SAI_PORT_OPER_STATUS_TESTING + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 75

sai_port_oper_status_t = enum__sai_port_oper_status_t# /home/bluecmd/Downloads/SAI/inc/saiport.h: 75

# /home/bluecmd/Downloads/SAI/inc/saiport.h: 92
class struct__sai_port_oper_status_notification_t(Structure):
    pass

struct__sai_port_oper_status_notification_t.__slots__ = [
    'port_id',
    'port_state',
]
struct__sai_port_oper_status_notification_t._fields_ = [
    ('port_id', sai_object_id_t),
    ('port_state', sai_port_oper_status_t),
]

sai_port_oper_status_notification_t = struct__sai_port_oper_status_notification_t# /home/bluecmd/Downloads/SAI/inc/saiport.h: 92

enum__sai_port_flow_control_mode_t = c_int# /home/bluecmd/Downloads/SAI/inc/saiport.h: 111

SAI_PORT_FLOW_CONTROL_MODE_DISABLE = 0# /home/bluecmd/Downloads/SAI/inc/saiport.h: 111

SAI_PORT_FLOW_CONTROL_MODE_TX_ONLY = (SAI_PORT_FLOW_CONTROL_MODE_DISABLE + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 111

SAI_PORT_FLOW_CONTROL_MODE_RX_ONLY = (SAI_PORT_FLOW_CONTROL_MODE_TX_ONLY + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 111

SAI_PORT_FLOW_CONTROL_MODE_BOTH_ENABLE = (SAI_PORT_FLOW_CONTROL_MODE_RX_ONLY + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 111

sai_port_flow_control_mode_t = enum__sai_port_flow_control_mode_t# /home/bluecmd/Downloads/SAI/inc/saiport.h: 111

enum__sai_port_internal_loopback_mode_t = c_int# /home/bluecmd/Downloads/SAI/inc/saiport.h: 128

SAI_PORT_INTERNAL_LOOPBACK_MODE_NONE = 0# /home/bluecmd/Downloads/SAI/inc/saiport.h: 128

SAI_PORT_INTERNAL_LOOPBACK_MODE_PHY = (SAI_PORT_INTERNAL_LOOPBACK_MODE_NONE + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 128

SAI_PORT_INTERNAL_LOOPBACK_MODE_MAC = (SAI_PORT_INTERNAL_LOOPBACK_MODE_PHY + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 128

sai_port_internal_loopback_mode_t = enum__sai_port_internal_loopback_mode_t# /home/bluecmd/Downloads/SAI/inc/saiport.h: 128

enum__sai_port_loopback_mode_t = c_int# /home/bluecmd/Downloads/SAI/inc/saiport.h: 149

SAI_PORT_LOOPBACK_MODE_NONE = 0# /home/bluecmd/Downloads/SAI/inc/saiport.h: 149

SAI_PORT_LOOPBACK_MODE_PHY = (SAI_PORT_LOOPBACK_MODE_NONE + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 149

SAI_PORT_LOOPBACK_MODE_MAC = (SAI_PORT_LOOPBACK_MODE_PHY + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 149

SAI_PORT_LOOPBACK_MODE_PHY_REMOTE = (SAI_PORT_LOOPBACK_MODE_MAC + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 149

SAI_PORT_LOOPBACK_MODE_MAC_REMOTE = (SAI_PORT_LOOPBACK_MODE_PHY_REMOTE + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 149

sai_port_loopback_mode_t = enum__sai_port_loopback_mode_t# /home/bluecmd/Downloads/SAI/inc/saiport.h: 149

enum__sai_port_media_type_t = c_int# /home/bluecmd/Downloads/SAI/inc/saiport.h: 170

SAI_PORT_MEDIA_TYPE_NOT_PRESENT = 0# /home/bluecmd/Downloads/SAI/inc/saiport.h: 170

SAI_PORT_MEDIA_TYPE_UNKNOWN = (SAI_PORT_MEDIA_TYPE_NOT_PRESENT + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 170

SAI_PORT_MEDIA_TYPE_FIBER = (SAI_PORT_MEDIA_TYPE_UNKNOWN + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 170

SAI_PORT_MEDIA_TYPE_COPPER = (SAI_PORT_MEDIA_TYPE_FIBER + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 170

SAI_PORT_MEDIA_TYPE_BACKPLANE = (SAI_PORT_MEDIA_TYPE_COPPER + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 170

sai_port_media_type_t = enum__sai_port_media_type_t# /home/bluecmd/Downloads/SAI/inc/saiport.h: 170

enum__sai_port_cable_pair_state_t = c_int# /home/bluecmd/Downloads/SAI/inc/saiport.h: 192

SAI_PORT_CABLE_PAIR_STATE_OK = 0# /home/bluecmd/Downloads/SAI/inc/saiport.h: 192

SAI_PORT_CABLE_PAIR_STATE_OPEN = (SAI_PORT_CABLE_PAIR_STATE_OK + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 192

SAI_PORT_CABLE_PAIR_STATE_SHORT = (SAI_PORT_CABLE_PAIR_STATE_OPEN + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 192

SAI_PORT_CABLE_PAIR_STATE_CROSSTALK = (SAI_PORT_CABLE_PAIR_STATE_SHORT + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 192

SAI_PORT_CABLE_PAIR_STATE_UNKNOWN = (SAI_PORT_CABLE_PAIR_STATE_CROSSTALK + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 192

sai_port_cable_pair_state_t = enum__sai_port_cable_pair_state_t# /home/bluecmd/Downloads/SAI/inc/saiport.h: 192

enum__sai_port_cable_type_t = c_int# /home/bluecmd/Downloads/SAI/inc/saiport.h: 217

SAI_PORT_CABLE_TYPE_UNKNOWN = 0# /home/bluecmd/Downloads/SAI/inc/saiport.h: 217

SAI_PORT_CABLE_TYPE_CAT5 = (SAI_PORT_CABLE_TYPE_UNKNOWN + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 217

SAI_PORT_CABLE_TYPE_CAT5E = (SAI_PORT_CABLE_TYPE_CAT5 + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 217

SAI_PORT_CABLE_TYPE_CAT6 = (SAI_PORT_CABLE_TYPE_CAT5E + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 217

SAI_PORT_CABLE_TYPE_CAT6A = (SAI_PORT_CABLE_TYPE_CAT6 + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 217

SAI_PORT_CABLE_TYPE_CAT7 = (SAI_PORT_CABLE_TYPE_CAT6A + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 217

sai_port_cable_type_t = enum__sai_port_cable_type_t# /home/bluecmd/Downloads/SAI/inc/saiport.h: 217

enum__sai_port_breakout_mode_type_t = c_int# /home/bluecmd/Downloads/SAI/inc/saiport.h: 236

SAI_PORT_BREAKOUT_MODE_TYPE_1_LANE = 0# /home/bluecmd/Downloads/SAI/inc/saiport.h: 236

SAI_PORT_BREAKOUT_MODE_TYPE_2_LANE = 1# /home/bluecmd/Downloads/SAI/inc/saiport.h: 236

SAI_PORT_BREAKOUT_MODE_TYPE_4_LANE = 2# /home/bluecmd/Downloads/SAI/inc/saiport.h: 236

SAI_PORT_BREAKOUT_MODE_TYPE_MAX = (SAI_PORT_BREAKOUT_MODE_TYPE_4_LANE + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 236

sai_port_breakout_mode_type_t = enum__sai_port_breakout_mode_type_t# /home/bluecmd/Downloads/SAI/inc/saiport.h: 236

enum__sai_port_fec_mode_t = c_int# /home/bluecmd/Downloads/SAI/inc/saiport.h: 251

SAI_PORT_FEC_MODE_NONE = 0# /home/bluecmd/Downloads/SAI/inc/saiport.h: 251

SAI_PORT_FEC_MODE_RS = (SAI_PORT_FEC_MODE_NONE + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 251

SAI_PORT_FEC_MODE_FC = (SAI_PORT_FEC_MODE_RS + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 251

sai_port_fec_mode_t = enum__sai_port_fec_mode_t# /home/bluecmd/Downloads/SAI/inc/saiport.h: 251

enum__sai_port_fec_mode_extended_t = c_int# /home/bluecmd/Downloads/SAI/inc/saiport.h: 272

SAI_PORT_FEC_MODE_EXTENDED_NONE = 0# /home/bluecmd/Downloads/SAI/inc/saiport.h: 272

SAI_PORT_FEC_MODE_EXTENDED_RS528 = (SAI_PORT_FEC_MODE_EXTENDED_NONE + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 272

SAI_PORT_FEC_MODE_EXTENDED_RS544 = (SAI_PORT_FEC_MODE_EXTENDED_RS528 + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 272

SAI_PORT_FEC_MODE_EXTENDED_RS544_INTERLEAVED = (SAI_PORT_FEC_MODE_EXTENDED_RS544 + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 272

SAI_PORT_FEC_MODE_EXTENDED_FC = (SAI_PORT_FEC_MODE_EXTENDED_RS544_INTERLEAVED + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 272

sai_port_fec_mode_extended_t = enum__sai_port_fec_mode_extended_t# /home/bluecmd/Downloads/SAI/inc/saiport.h: 272

enum__sai_port_datapath_enable_t = c_int# /home/bluecmd/Downloads/SAI/inc/saiport.h: 285

SAI_PORT_DATAPATH_ENABLE_PASS_THROUGH_MODE = 0# /home/bluecmd/Downloads/SAI/inc/saiport.h: 285

SAI_PORT_DATAPATH_ENABLE_PCS_IEEE_MODE = (SAI_PORT_DATAPATH_ENABLE_PASS_THROUGH_MODE + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 285

sai_port_datapath_enable_t = enum__sai_port_datapath_enable_t# /home/bluecmd/Downloads/SAI/inc/saiport.h: 285

enum__sai_port_priority_flow_control_mode_t = c_int# /home/bluecmd/Downloads/SAI/inc/saiport.h: 298

SAI_PORT_PRIORITY_FLOW_CONTROL_MODE_COMBINED = 0# /home/bluecmd/Downloads/SAI/inc/saiport.h: 298

SAI_PORT_PRIORITY_FLOW_CONTROL_MODE_SEPARATE = (SAI_PORT_PRIORITY_FLOW_CONTROL_MODE_COMBINED + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 298

sai_port_priority_flow_control_mode_t = enum__sai_port_priority_flow_control_mode_t# /home/bluecmd/Downloads/SAI/inc/saiport.h: 298

enum__sai_port_ptp_mode_t = c_int# /home/bluecmd/Downloads/SAI/inc/saiport.h: 314

SAI_PORT_PTP_MODE_NONE = 0# /home/bluecmd/Downloads/SAI/inc/saiport.h: 314

SAI_PORT_PTP_MODE_SINGLE_STEP_TIMESTAMP = (SAI_PORT_PTP_MODE_NONE + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 314

SAI_PORT_PTP_MODE_TWO_STEP_TIMESTAMP = (SAI_PORT_PTP_MODE_SINGLE_STEP_TIMESTAMP + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 314

sai_port_ptp_mode_t = enum__sai_port_ptp_mode_t# /home/bluecmd/Downloads/SAI/inc/saiport.h: 314

enum__sai_port_interface_type_t = c_int# /home/bluecmd/Downloads/SAI/inc/saiport.h: 400

SAI_PORT_INTERFACE_TYPE_NONE = 0# /home/bluecmd/Downloads/SAI/inc/saiport.h: 400

SAI_PORT_INTERFACE_TYPE_CR = (SAI_PORT_INTERFACE_TYPE_NONE + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 400

SAI_PORT_INTERFACE_TYPE_CR2 = (SAI_PORT_INTERFACE_TYPE_CR + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 400

SAI_PORT_INTERFACE_TYPE_CR4 = (SAI_PORT_INTERFACE_TYPE_CR2 + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 400

SAI_PORT_INTERFACE_TYPE_SR = (SAI_PORT_INTERFACE_TYPE_CR4 + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 400

SAI_PORT_INTERFACE_TYPE_SR2 = (SAI_PORT_INTERFACE_TYPE_SR + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 400

SAI_PORT_INTERFACE_TYPE_SR4 = (SAI_PORT_INTERFACE_TYPE_SR2 + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 400

SAI_PORT_INTERFACE_TYPE_LR = (SAI_PORT_INTERFACE_TYPE_SR4 + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 400

SAI_PORT_INTERFACE_TYPE_LR4 = (SAI_PORT_INTERFACE_TYPE_LR + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 400

SAI_PORT_INTERFACE_TYPE_KR = (SAI_PORT_INTERFACE_TYPE_LR4 + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 400

SAI_PORT_INTERFACE_TYPE_KR4 = (SAI_PORT_INTERFACE_TYPE_KR + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 400

SAI_PORT_INTERFACE_TYPE_CAUI = (SAI_PORT_INTERFACE_TYPE_KR4 + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 400

SAI_PORT_INTERFACE_TYPE_GMII = (SAI_PORT_INTERFACE_TYPE_CAUI + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 400

SAI_PORT_INTERFACE_TYPE_SFI = (SAI_PORT_INTERFACE_TYPE_GMII + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 400

SAI_PORT_INTERFACE_TYPE_XLAUI = (SAI_PORT_INTERFACE_TYPE_SFI + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 400

SAI_PORT_INTERFACE_TYPE_KR2 = (SAI_PORT_INTERFACE_TYPE_XLAUI + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 400

SAI_PORT_INTERFACE_TYPE_CAUI4 = (SAI_PORT_INTERFACE_TYPE_KR2 + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 400

SAI_PORT_INTERFACE_TYPE_XAUI = (SAI_PORT_INTERFACE_TYPE_CAUI4 + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 400

SAI_PORT_INTERFACE_TYPE_XFI = (SAI_PORT_INTERFACE_TYPE_XAUI + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 400

SAI_PORT_INTERFACE_TYPE_XGMII = (SAI_PORT_INTERFACE_TYPE_XFI + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 400

SAI_PORT_INTERFACE_TYPE_CR8 = (SAI_PORT_INTERFACE_TYPE_XGMII + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 400

SAI_PORT_INTERFACE_TYPE_KR8 = (SAI_PORT_INTERFACE_TYPE_CR8 + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 400

SAI_PORT_INTERFACE_TYPE_SR8 = (SAI_PORT_INTERFACE_TYPE_KR8 + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 400

SAI_PORT_INTERFACE_TYPE_LR8 = (SAI_PORT_INTERFACE_TYPE_SR8 + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 400

SAI_PORT_INTERFACE_TYPE_USXGMII = (SAI_PORT_INTERFACE_TYPE_LR8 + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 400

SAI_PORT_INTERFACE_TYPE_MAX = (SAI_PORT_INTERFACE_TYPE_USXGMII + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 400

sai_port_interface_type_t = enum__sai_port_interface_type_t# /home/bluecmd/Downloads/SAI/inc/saiport.h: 400

enum__sai_port_link_training_failure_status_t = c_int# /home/bluecmd/Downloads/SAI/inc/saiport.h: 419

SAI_PORT_LINK_TRAINING_FAILURE_STATUS_NO_ERROR = 0# /home/bluecmd/Downloads/SAI/inc/saiport.h: 419

SAI_PORT_LINK_TRAINING_FAILURE_STATUS_FRAME_LOCK_ERROR = (SAI_PORT_LINK_TRAINING_FAILURE_STATUS_NO_ERROR + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 419

SAI_PORT_LINK_TRAINING_FAILURE_STATUS_SNR_LOWER_THRESHOLD = (SAI_PORT_LINK_TRAINING_FAILURE_STATUS_FRAME_LOCK_ERROR + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 419

SAI_PORT_LINK_TRAINING_FAILURE_STATUS_TIME_OUT = (SAI_PORT_LINK_TRAINING_FAILURE_STATUS_SNR_LOWER_THRESHOLD + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 419

sai_port_link_training_failure_status_t = enum__sai_port_link_training_failure_status_t# /home/bluecmd/Downloads/SAI/inc/saiport.h: 419

enum__sai_port_link_training_rx_status_t = c_int# /home/bluecmd/Downloads/SAI/inc/saiport.h: 432

SAI_PORT_LINK_TRAINING_RX_STATUS_NOT_TRAINED = 0# /home/bluecmd/Downloads/SAI/inc/saiport.h: 432

SAI_PORT_LINK_TRAINING_RX_STATUS_TRAINED = (SAI_PORT_LINK_TRAINING_RX_STATUS_NOT_TRAINED + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 432

sai_port_link_training_rx_status_t = enum__sai_port_link_training_rx_status_t# /home/bluecmd/Downloads/SAI/inc/saiport.h: 432

enum__sai_port_prbs_config_t = c_int# /home/bluecmd/Downloads/SAI/inc/saiport.h: 451

SAI_PORT_PRBS_CONFIG_DISABLE = 0# /home/bluecmd/Downloads/SAI/inc/saiport.h: 451

SAI_PORT_PRBS_CONFIG_ENABLE_TX_RX = (SAI_PORT_PRBS_CONFIG_DISABLE + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 451

SAI_PORT_PRBS_CONFIG_ENABLE_RX = (SAI_PORT_PRBS_CONFIG_ENABLE_TX_RX + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 451

SAI_PORT_PRBS_CONFIG_ENABLE_TX = (SAI_PORT_PRBS_CONFIG_ENABLE_RX + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 451

sai_port_prbs_config_t = enum__sai_port_prbs_config_t# /home/bluecmd/Downloads/SAI/inc/saiport.h: 451

enum__sai_port_connector_failover_mode_t = c_int# /home/bluecmd/Downloads/SAI/inc/saiport.h: 467

SAI_PORT_CONNECTOR_FAILOVER_MODE_DISABLE = 0# /home/bluecmd/Downloads/SAI/inc/saiport.h: 467

SAI_PORT_CONNECTOR_FAILOVER_MODE_PRIMARY = (SAI_PORT_CONNECTOR_FAILOVER_MODE_DISABLE + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 467

SAI_PORT_CONNECTOR_FAILOVER_MODE_SECONDARY = (SAI_PORT_CONNECTOR_FAILOVER_MODE_PRIMARY + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 467

sai_port_connector_failover_mode_t = enum__sai_port_connector_failover_mode_t# /home/bluecmd/Downloads/SAI/inc/saiport.h: 467

enum__sai_port_mdix_mode_status_t = c_int# /home/bluecmd/Downloads/SAI/inc/saiport.h: 480

SAI_PORT_MDIX_MODE_STATUS_STRAIGHT = 0# /home/bluecmd/Downloads/SAI/inc/saiport.h: 480

SAI_PORT_MDIX_MODE_STATUS_CROSSOVER = (SAI_PORT_MDIX_MODE_STATUS_STRAIGHT + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 480

sai_port_mdix_mode_status_t = enum__sai_port_mdix_mode_status_t# /home/bluecmd/Downloads/SAI/inc/saiport.h: 480

enum__sai_port_mdix_mode_config_t = c_int# /home/bluecmd/Downloads/SAI/inc/saiport.h: 496

SAI_PORT_MDIX_MODE_CONFIG_AUTO = 0# /home/bluecmd/Downloads/SAI/inc/saiport.h: 496

SAI_PORT_MDIX_MODE_CONFIG_STRAIGHT = (SAI_PORT_MDIX_MODE_CONFIG_AUTO + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 496

SAI_PORT_MDIX_MODE_CONFIG_CROSSOVER = (SAI_PORT_MDIX_MODE_CONFIG_STRAIGHT + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 496

sai_port_mdix_mode_config_t = enum__sai_port_mdix_mode_config_t# /home/bluecmd/Downloads/SAI/inc/saiport.h: 496

enum__sai_port_auto_neg_config_mode_t = c_int# /home/bluecmd/Downloads/SAI/inc/saiport.h: 515

SAI_PORT_AUTO_NEG_CONFIG_MODE_DISABLED = 0# /home/bluecmd/Downloads/SAI/inc/saiport.h: 515

SAI_PORT_AUTO_NEG_CONFIG_MODE_AUTO = (SAI_PORT_AUTO_NEG_CONFIG_MODE_DISABLED + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 515

SAI_PORT_AUTO_NEG_CONFIG_MODE_SLAVE = (SAI_PORT_AUTO_NEG_CONFIG_MODE_AUTO + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 515

SAI_PORT_AUTO_NEG_CONFIG_MODE_MASTER = (SAI_PORT_AUTO_NEG_CONFIG_MODE_SLAVE + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 515

sai_port_auto_neg_config_mode_t = enum__sai_port_auto_neg_config_mode_t# /home/bluecmd/Downloads/SAI/inc/saiport.h: 515

enum__sai_port_module_type_t = c_int# /home/bluecmd/Downloads/SAI/inc/saiport.h: 531

SAI_PORT_MODULE_TYPE_1000BASE_X = 0# /home/bluecmd/Downloads/SAI/inc/saiport.h: 531

SAI_PORT_MODULE_TYPE_100FX = (SAI_PORT_MODULE_TYPE_1000BASE_X + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 531

SAI_PORT_MODULE_TYPE_SGMII_SLAVE = (SAI_PORT_MODULE_TYPE_100FX + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 531

sai_port_module_type_t = enum__sai_port_module_type_t# /home/bluecmd/Downloads/SAI/inc/saiport.h: 531

enum__sai_port_dual_media_t = c_int# /home/bluecmd/Downloads/SAI/inc/saiport.h: 553

SAI_PORT_DUAL_MEDIA_NONE = 0# /home/bluecmd/Downloads/SAI/inc/saiport.h: 553

SAI_PORT_DUAL_MEDIA_COPPER_ONLY = (SAI_PORT_DUAL_MEDIA_NONE + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 553

SAI_PORT_DUAL_MEDIA_FIBER_ONLY = (SAI_PORT_DUAL_MEDIA_COPPER_ONLY + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 553

SAI_PORT_DUAL_MEDIA_COPPER_PREFERRED = (SAI_PORT_DUAL_MEDIA_FIBER_ONLY + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 553

SAI_PORT_DUAL_MEDIA_FIBER_PREFERRED = (SAI_PORT_DUAL_MEDIA_COPPER_PREFERRED + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 553

sai_port_dual_media_t = enum__sai_port_dual_media_t# /home/bluecmd/Downloads/SAI/inc/saiport.h: 553

enum__sai_port_host_tx_ready_status_t = c_int# /home/bluecmd/Downloads/SAI/inc/saiport.h: 565

SAI_PORT_HOST_TX_READY_STATUS_NOT_READY = 0# /home/bluecmd/Downloads/SAI/inc/saiport.h: 565

SAI_PORT_HOST_TX_READY_STATUS_READY = (SAI_PORT_HOST_TX_READY_STATUS_NOT_READY + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 565

sai_port_host_tx_ready_status_t = enum__sai_port_host_tx_ready_status_t# /home/bluecmd/Downloads/SAI/inc/saiport.h: 565

enum__sai_port_path_tracing_timestamp_type_t = c_int# /home/bluecmd/Downloads/SAI/inc/saiport.h: 584

SAI_PORT_PATH_TRACING_TIMESTAMP_TYPE_8_15 = 0# /home/bluecmd/Downloads/SAI/inc/saiport.h: 584

SAI_PORT_PATH_TRACING_TIMESTAMP_TYPE_12_19 = (SAI_PORT_PATH_TRACING_TIMESTAMP_TYPE_8_15 + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 584

SAI_PORT_PATH_TRACING_TIMESTAMP_TYPE_16_23 = (SAI_PORT_PATH_TRACING_TIMESTAMP_TYPE_12_19 + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 584

SAI_PORT_PATH_TRACING_TIMESTAMP_TYPE_20_27 = (SAI_PORT_PATH_TRACING_TIMESTAMP_TYPE_16_23 + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 584

sai_port_path_tracing_timestamp_type_t = enum__sai_port_path_tracing_timestamp_type_t# /home/bluecmd/Downloads/SAI/inc/saiport.h: 584

enum__sai_port_attr_t = c_int# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_START = 0# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_TYPE = SAI_PORT_ATTR_START# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_OPER_STATUS = (SAI_PORT_ATTR_TYPE + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_SUPPORTED_BREAKOUT_MODE_TYPE = (SAI_PORT_ATTR_OPER_STATUS + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_CURRENT_BREAKOUT_MODE_TYPE = (SAI_PORT_ATTR_SUPPORTED_BREAKOUT_MODE_TYPE + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_QOS_NUMBER_OF_QUEUES = (SAI_PORT_ATTR_CURRENT_BREAKOUT_MODE_TYPE + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_QOS_QUEUE_LIST = (SAI_PORT_ATTR_QOS_NUMBER_OF_QUEUES + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_QOS_NUMBER_OF_SCHEDULER_GROUPS = (SAI_PORT_ATTR_QOS_QUEUE_LIST + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_QOS_SCHEDULER_GROUP_LIST = (SAI_PORT_ATTR_QOS_NUMBER_OF_SCHEDULER_GROUPS + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_QOS_MAXIMUM_HEADROOM_SIZE = (SAI_PORT_ATTR_QOS_SCHEDULER_GROUP_LIST + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_SUPPORTED_SPEED = (SAI_PORT_ATTR_QOS_MAXIMUM_HEADROOM_SIZE + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_SUPPORTED_FEC_MODE = (SAI_PORT_ATTR_SUPPORTED_SPEED + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_SUPPORTED_FEC_MODE_EXTENDED = (SAI_PORT_ATTR_SUPPORTED_FEC_MODE + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_SUPPORTED_HALF_DUPLEX_SPEED = (SAI_PORT_ATTR_SUPPORTED_FEC_MODE_EXTENDED + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_SUPPORTED_AUTO_NEG_MODE = (SAI_PORT_ATTR_SUPPORTED_HALF_DUPLEX_SPEED + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_SUPPORTED_FLOW_CONTROL_MODE = (SAI_PORT_ATTR_SUPPORTED_AUTO_NEG_MODE + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_SUPPORTED_ASYMMETRIC_PAUSE_MODE = (SAI_PORT_ATTR_SUPPORTED_FLOW_CONTROL_MODE + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_SUPPORTED_MEDIA_TYPE = (SAI_PORT_ATTR_SUPPORTED_ASYMMETRIC_PAUSE_MODE + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_REMOTE_ADVERTISED_SPEED = (SAI_PORT_ATTR_SUPPORTED_MEDIA_TYPE + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_REMOTE_ADVERTISED_FEC_MODE = (SAI_PORT_ATTR_REMOTE_ADVERTISED_SPEED + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_REMOTE_ADVERTISED_FEC_MODE_EXTENDED = (SAI_PORT_ATTR_REMOTE_ADVERTISED_FEC_MODE + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_REMOTE_ADVERTISED_HALF_DUPLEX_SPEED = (SAI_PORT_ATTR_REMOTE_ADVERTISED_FEC_MODE_EXTENDED + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_REMOTE_ADVERTISED_AUTO_NEG_MODE = (SAI_PORT_ATTR_REMOTE_ADVERTISED_HALF_DUPLEX_SPEED + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_REMOTE_ADVERTISED_FLOW_CONTROL_MODE = (SAI_PORT_ATTR_REMOTE_ADVERTISED_AUTO_NEG_MODE + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_REMOTE_ADVERTISED_ASYMMETRIC_PAUSE_MODE = (SAI_PORT_ATTR_REMOTE_ADVERTISED_FLOW_CONTROL_MODE + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_REMOTE_ADVERTISED_MEDIA_TYPE = (SAI_PORT_ATTR_REMOTE_ADVERTISED_ASYMMETRIC_PAUSE_MODE + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_REMOTE_ADVERTISED_OUI_CODE = (SAI_PORT_ATTR_REMOTE_ADVERTISED_MEDIA_TYPE + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_NUMBER_OF_INGRESS_PRIORITY_GROUPS = (SAI_PORT_ATTR_REMOTE_ADVERTISED_OUI_CODE + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_INGRESS_PRIORITY_GROUP_LIST = (SAI_PORT_ATTR_NUMBER_OF_INGRESS_PRIORITY_GROUPS + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_EYE_VALUES = (SAI_PORT_ATTR_INGRESS_PRIORITY_GROUP_LIST + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_OPER_SPEED = (SAI_PORT_ATTR_EYE_VALUES + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_HW_LANE_LIST = (SAI_PORT_ATTR_OPER_SPEED + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_SPEED = (SAI_PORT_ATTR_HW_LANE_LIST + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_FULL_DUPLEX_MODE = (SAI_PORT_ATTR_SPEED + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_AUTO_NEG_MODE = (SAI_PORT_ATTR_FULL_DUPLEX_MODE + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_ADMIN_STATE = (SAI_PORT_ATTR_AUTO_NEG_MODE + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_MEDIA_TYPE = (SAI_PORT_ATTR_ADMIN_STATE + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_ADVERTISED_SPEED = (SAI_PORT_ATTR_MEDIA_TYPE + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_ADVERTISED_FEC_MODE = (SAI_PORT_ATTR_ADVERTISED_SPEED + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_ADVERTISED_FEC_MODE_EXTENDED = (SAI_PORT_ATTR_ADVERTISED_FEC_MODE + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_ADVERTISED_HALF_DUPLEX_SPEED = (SAI_PORT_ATTR_ADVERTISED_FEC_MODE_EXTENDED + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_ADVERTISED_AUTO_NEG_MODE = (SAI_PORT_ATTR_ADVERTISED_HALF_DUPLEX_SPEED + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_ADVERTISED_FLOW_CONTROL_MODE = (SAI_PORT_ATTR_ADVERTISED_AUTO_NEG_MODE + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_ADVERTISED_ASYMMETRIC_PAUSE_MODE = (SAI_PORT_ATTR_ADVERTISED_FLOW_CONTROL_MODE + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_ADVERTISED_MEDIA_TYPE = (SAI_PORT_ATTR_ADVERTISED_ASYMMETRIC_PAUSE_MODE + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_ADVERTISED_OUI_CODE = (SAI_PORT_ATTR_ADVERTISED_MEDIA_TYPE + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_PORT_VLAN_ID = (SAI_PORT_ATTR_ADVERTISED_OUI_CODE + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_DEFAULT_VLAN_PRIORITY = (SAI_PORT_ATTR_PORT_VLAN_ID + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_DROP_UNTAGGED = (SAI_PORT_ATTR_DEFAULT_VLAN_PRIORITY + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_DROP_TAGGED = (SAI_PORT_ATTR_DROP_UNTAGGED + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_INTERNAL_LOOPBACK_MODE = (SAI_PORT_ATTR_DROP_TAGGED + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_USE_EXTENDED_FEC = (SAI_PORT_ATTR_INTERNAL_LOOPBACK_MODE + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_FEC_MODE = (SAI_PORT_ATTR_USE_EXTENDED_FEC + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_FEC_MODE_EXTENDED = (SAI_PORT_ATTR_FEC_MODE + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_UPDATE_DSCP = (SAI_PORT_ATTR_FEC_MODE_EXTENDED + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_MTU = (SAI_PORT_ATTR_UPDATE_DSCP + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_FLOOD_STORM_CONTROL_POLICER_ID = (SAI_PORT_ATTR_MTU + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_BROADCAST_STORM_CONTROL_POLICER_ID = (SAI_PORT_ATTR_FLOOD_STORM_CONTROL_POLICER_ID + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_MULTICAST_STORM_CONTROL_POLICER_ID = (SAI_PORT_ATTR_BROADCAST_STORM_CONTROL_POLICER_ID + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_GLOBAL_FLOW_CONTROL_MODE = (SAI_PORT_ATTR_MULTICAST_STORM_CONTROL_POLICER_ID + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_INGRESS_ACL = (SAI_PORT_ATTR_GLOBAL_FLOW_CONTROL_MODE + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_EGRESS_ACL = (SAI_PORT_ATTR_INGRESS_ACL + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_INGRESS_MACSEC_ACL = (SAI_PORT_ATTR_EGRESS_ACL + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_EGRESS_MACSEC_ACL = (SAI_PORT_ATTR_INGRESS_MACSEC_ACL + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_MACSEC_PORT_LIST = (SAI_PORT_ATTR_EGRESS_MACSEC_ACL + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_INGRESS_MIRROR_SESSION = (SAI_PORT_ATTR_MACSEC_PORT_LIST + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_EGRESS_MIRROR_SESSION = (SAI_PORT_ATTR_INGRESS_MIRROR_SESSION + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_INGRESS_SAMPLEPACKET_ENABLE = (SAI_PORT_ATTR_EGRESS_MIRROR_SESSION + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_EGRESS_SAMPLEPACKET_ENABLE = (SAI_PORT_ATTR_INGRESS_SAMPLEPACKET_ENABLE + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_INGRESS_SAMPLE_MIRROR_SESSION = (SAI_PORT_ATTR_EGRESS_SAMPLEPACKET_ENABLE + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_EGRESS_SAMPLE_MIRROR_SESSION = (SAI_PORT_ATTR_INGRESS_SAMPLE_MIRROR_SESSION + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_POLICER_ID = (SAI_PORT_ATTR_EGRESS_SAMPLE_MIRROR_SESSION + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_QOS_DEFAULT_TC = (SAI_PORT_ATTR_POLICER_ID + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_QOS_DOT1P_TO_TC_MAP = (SAI_PORT_ATTR_QOS_DEFAULT_TC + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_QOS_DOT1P_TO_COLOR_MAP = (SAI_PORT_ATTR_QOS_DOT1P_TO_TC_MAP + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_QOS_DSCP_TO_TC_MAP = (SAI_PORT_ATTR_QOS_DOT1P_TO_COLOR_MAP + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_QOS_DSCP_TO_COLOR_MAP = (SAI_PORT_ATTR_QOS_DSCP_TO_TC_MAP + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_QOS_TC_TO_QUEUE_MAP = (SAI_PORT_ATTR_QOS_DSCP_TO_COLOR_MAP + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_QOS_TC_AND_COLOR_TO_DOT1P_MAP = (SAI_PORT_ATTR_QOS_TC_TO_QUEUE_MAP + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP = (SAI_PORT_ATTR_QOS_TC_AND_COLOR_TO_DOT1P_MAP + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_QOS_TC_TO_PRIORITY_GROUP_MAP = (SAI_PORT_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_QOS_PFC_PRIORITY_TO_PRIORITY_GROUP_MAP = (SAI_PORT_ATTR_QOS_TC_TO_PRIORITY_GROUP_MAP + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_QOS_PFC_PRIORITY_TO_QUEUE_MAP = (SAI_PORT_ATTR_QOS_PFC_PRIORITY_TO_PRIORITY_GROUP_MAP + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_QOS_SCHEDULER_PROFILE_ID = (SAI_PORT_ATTR_QOS_PFC_PRIORITY_TO_QUEUE_MAP + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_QOS_INGRESS_BUFFER_PROFILE_LIST = (SAI_PORT_ATTR_QOS_SCHEDULER_PROFILE_ID + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_QOS_EGRESS_BUFFER_PROFILE_LIST = (SAI_PORT_ATTR_QOS_INGRESS_BUFFER_PROFILE_LIST + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_PRIORITY_FLOW_CONTROL_MODE = (SAI_PORT_ATTR_QOS_EGRESS_BUFFER_PROFILE_LIST + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_PRIORITY_FLOW_CONTROL = (SAI_PORT_ATTR_PRIORITY_FLOW_CONTROL_MODE + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_PRIORITY_FLOW_CONTROL_RX = (SAI_PORT_ATTR_PRIORITY_FLOW_CONTROL + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_PRIORITY_FLOW_CONTROL_TX = (SAI_PORT_ATTR_PRIORITY_FLOW_CONTROL_RX + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_META_DATA = (SAI_PORT_ATTR_PRIORITY_FLOW_CONTROL_TX + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_EGRESS_BLOCK_PORT_LIST = (SAI_PORT_ATTR_META_DATA + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_HW_PROFILE_ID = (SAI_PORT_ATTR_EGRESS_BLOCK_PORT_LIST + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_EEE_ENABLE = (SAI_PORT_ATTR_HW_PROFILE_ID + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_EEE_IDLE_TIME = (SAI_PORT_ATTR_EEE_ENABLE + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_EEE_WAKE_TIME = (SAI_PORT_ATTR_EEE_IDLE_TIME + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_PORT_POOL_LIST = (SAI_PORT_ATTR_EEE_WAKE_TIME + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_ISOLATION_GROUP = (SAI_PORT_ATTR_PORT_POOL_LIST + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_PKT_TX_ENABLE = (SAI_PORT_ATTR_ISOLATION_GROUP + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_TAM_OBJECT = (SAI_PORT_ATTR_PKT_TX_ENABLE + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_SERDES_PREEMPHASIS = (SAI_PORT_ATTR_TAM_OBJECT + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_SERDES_IDRIVER = (SAI_PORT_ATTR_SERDES_PREEMPHASIS + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_SERDES_IPREDRIVER = (SAI_PORT_ATTR_SERDES_IDRIVER + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_LINK_TRAINING_ENABLE = (SAI_PORT_ATTR_SERDES_IPREDRIVER + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_PTP_MODE = (SAI_PORT_ATTR_LINK_TRAINING_ENABLE + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_INTERFACE_TYPE = (SAI_PORT_ATTR_PTP_MODE + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_ADVERTISED_INTERFACE_TYPE = (SAI_PORT_ATTR_INTERFACE_TYPE + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_REFERENCE_CLOCK = (SAI_PORT_ATTR_ADVERTISED_INTERFACE_TYPE + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_PRBS_POLYNOMIAL = (SAI_PORT_ATTR_REFERENCE_CLOCK + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_PORT_SERDES_ID = (SAI_PORT_ATTR_PRBS_POLYNOMIAL + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_LINK_TRAINING_FAILURE_STATUS = (SAI_PORT_ATTR_PORT_SERDES_ID + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_LINK_TRAINING_RX_STATUS = (SAI_PORT_ATTR_LINK_TRAINING_FAILURE_STATUS + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_PRBS_CONFIG = (SAI_PORT_ATTR_LINK_TRAINING_RX_STATUS + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_PRBS_LOCK_STATUS = (SAI_PORT_ATTR_PRBS_CONFIG + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_PRBS_LOCK_LOSS_STATUS = (SAI_PORT_ATTR_PRBS_LOCK_STATUS + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_PRBS_RX_STATUS = (SAI_PORT_ATTR_PRBS_LOCK_LOSS_STATUS + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_PRBS_RX_STATE = (SAI_PORT_ATTR_PRBS_RX_STATUS + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_AUTO_NEG_STATUS = (SAI_PORT_ATTR_PRBS_RX_STATE + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_DISABLE_DECREMENT_TTL = (SAI_PORT_ATTR_AUTO_NEG_STATUS + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_QOS_MPLS_EXP_TO_TC_MAP = (SAI_PORT_ATTR_DISABLE_DECREMENT_TTL + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_QOS_MPLS_EXP_TO_COLOR_MAP = (SAI_PORT_ATTR_QOS_MPLS_EXP_TO_TC_MAP + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_QOS_TC_AND_COLOR_TO_MPLS_EXP_MAP = (SAI_PORT_ATTR_QOS_MPLS_EXP_TO_COLOR_MAP + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_TPID = (SAI_PORT_ATTR_QOS_TC_AND_COLOR_TO_MPLS_EXP_MAP + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_ERR_STATUS_LIST = (SAI_PORT_ATTR_TPID + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_FABRIC_ATTACHED = (SAI_PORT_ATTR_ERR_STATUS_LIST + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_FABRIC_ATTACHED_SWITCH_TYPE = (SAI_PORT_ATTR_FABRIC_ATTACHED + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_FABRIC_ATTACHED_SWITCH_ID = (SAI_PORT_ATTR_FABRIC_ATTACHED_SWITCH_TYPE + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_FABRIC_ATTACHED_PORT_INDEX = (SAI_PORT_ATTR_FABRIC_ATTACHED_SWITCH_ID + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_FABRIC_REACHABILITY = (SAI_PORT_ATTR_FABRIC_ATTACHED_PORT_INDEX + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_SYSTEM_PORT = (SAI_PORT_ATTR_FABRIC_REACHABILITY + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_AUTO_NEG_FEC_MODE_OVERRIDE = (SAI_PORT_ATTR_SYSTEM_PORT + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_LOOPBACK_MODE = (SAI_PORT_ATTR_AUTO_NEG_FEC_MODE_OVERRIDE + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_MDIX_MODE_STATUS = (SAI_PORT_ATTR_LOOPBACK_MODE + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_MDIX_MODE_CONFIG = (SAI_PORT_ATTR_MDIX_MODE_STATUS + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_AUTO_NEG_CONFIG_MODE = (SAI_PORT_ATTR_MDIX_MODE_CONFIG + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_1000X_SGMII_SLAVE_AUTODETECT = (SAI_PORT_ATTR_AUTO_NEG_CONFIG_MODE + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_MODULE_TYPE = (SAI_PORT_ATTR_1000X_SGMII_SLAVE_AUTODETECT + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_DUAL_MEDIA = (SAI_PORT_ATTR_MODULE_TYPE + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_AUTO_NEG_FEC_MODE_EXTENDED = (SAI_PORT_ATTR_DUAL_MEDIA + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_IPG = (SAI_PORT_ATTR_AUTO_NEG_FEC_MODE_EXTENDED + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_GLOBAL_FLOW_CONTROL_FORWARD = (SAI_PORT_ATTR_IPG + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_PRIORITY_FLOW_CONTROL_FORWARD = (SAI_PORT_ATTR_GLOBAL_FLOW_CONTROL_FORWARD + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_QOS_DSCP_TO_FORWARDING_CLASS_MAP = (SAI_PORT_ATTR_PRIORITY_FLOW_CONTROL_FORWARD + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_QOS_MPLS_EXP_TO_FORWARDING_CLASS_MAP = (SAI_PORT_ATTR_QOS_DSCP_TO_FORWARDING_CLASS_MAP + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_IPSEC_PORT = (SAI_PORT_ATTR_QOS_MPLS_EXP_TO_FORWARDING_CLASS_MAP + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_PFC_TC_DLD_INTERVAL_RANGE = (SAI_PORT_ATTR_IPSEC_PORT + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_PFC_TC_DLD_INTERVAL = (SAI_PORT_ATTR_PFC_TC_DLD_INTERVAL_RANGE + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_PFC_TC_DLR_INTERVAL_RANGE = (SAI_PORT_ATTR_PFC_TC_DLD_INTERVAL + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_PFC_TC_DLR_INTERVAL = (SAI_PORT_ATTR_PFC_TC_DLR_INTERVAL_RANGE + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_SUPPORTED_LINK_TRAINING_MODE = (SAI_PORT_ATTR_PFC_TC_DLR_INTERVAL + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_RX_SIGNAL_DETECT = (SAI_PORT_ATTR_SUPPORTED_LINK_TRAINING_MODE + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_RX_LOCK_STATUS = (SAI_PORT_ATTR_RX_SIGNAL_DETECT + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_PCS_RX_LINK_STATUS = (SAI_PORT_ATTR_RX_LOCK_STATUS + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_FEC_ALIGNMENT_LOCK = (SAI_PORT_ATTR_PCS_RX_LINK_STATUS + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_FABRIC_ISOLATE = (SAI_PORT_ATTR_FEC_ALIGNMENT_LOCK + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_MAX_FEC_SYMBOL_ERRORS_DETECTABLE = (SAI_PORT_ATTR_FABRIC_ISOLATE + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_ARS_ENABLE = (SAI_PORT_ATTR_MAX_FEC_SYMBOL_ERRORS_DETECTABLE + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_ARS_PORT_LOAD_SCALING_FACTOR = (SAI_PORT_ATTR_ARS_ENABLE + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_ARS_PORT_LOAD_PAST_ENABLE = (SAI_PORT_ATTR_ARS_PORT_LOAD_SCALING_FACTOR + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_ARS_PORT_LOAD_FUTURE_ENABLE = (SAI_PORT_ATTR_ARS_PORT_LOAD_PAST_ENABLE + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_ARS_ALTERNATE_PATH = (SAI_PORT_ATTR_ARS_PORT_LOAD_FUTURE_ENABLE + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_JSON_FORMATTED_DEBUG_DATA = (SAI_PORT_ATTR_ARS_ALTERNATE_PATH + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_ECMP_HASH_ALGORITHM = (SAI_PORT_ATTR_JSON_FORMATTED_DEBUG_DATA + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_ECMP_HASH_SEED = (SAI_PORT_ATTR_ECMP_HASH_ALGORITHM + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_ECMP_HASH_OFFSET = (SAI_PORT_ATTR_ECMP_HASH_SEED + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_OPER_PORT_FEC_MODE = (SAI_PORT_ATTR_ECMP_HASH_OFFSET + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_HOST_TX_SIGNAL_ENABLE = (SAI_PORT_ATTR_OPER_PORT_FEC_MODE + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_HOST_TX_READY_STATUS = (SAI_PORT_ATTR_HOST_TX_SIGNAL_ENABLE + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_PATH_TRACING_INTF = (SAI_PORT_ATTR_HOST_TX_READY_STATUS + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_PATH_TRACING_TIMESTAMP_TYPE = (SAI_PORT_ATTR_PATH_TRACING_INTF + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_RX_FREQUENCY_OFFSET_PPM = (SAI_PORT_ATTR_PATH_TRACING_TIMESTAMP_TYPE + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_RX_SNR = (SAI_PORT_ATTR_RX_FREQUENCY_OFFSET_PPM + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_DATAPATH_ENABLE = (SAI_PORT_ATTR_RX_SNR + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_CABLE_PAIR_STATE = (SAI_PORT_ATTR_DATAPATH_ENABLE + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_CABLE_PAIR_LENGTH = (SAI_PORT_ATTR_CABLE_PAIR_STATE + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_CABLE_TYPE = (SAI_PORT_ATTR_CABLE_PAIR_LENGTH + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_END = (SAI_PORT_ATTR_CABLE_TYPE + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_CUSTOM_RANGE_START = 0x10000000# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

SAI_PORT_ATTR_CUSTOM_RANGE_END = (SAI_PORT_ATTR_CUSTOM_RANGE_START + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

sai_port_attr_t = enum__sai_port_attr_t# /home/bluecmd/Downloads/SAI/inc/saiport.h: 2499

enum__sai_port_stat_t = c_int# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_START = 0# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_IF_IN_OCTETS = SAI_PORT_STAT_START# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_IF_IN_UCAST_PKTS = (SAI_PORT_STAT_IF_IN_OCTETS + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_IF_IN_NON_UCAST_PKTS = (SAI_PORT_STAT_IF_IN_UCAST_PKTS + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_IF_IN_DISCARDS = (SAI_PORT_STAT_IF_IN_NON_UCAST_PKTS + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_IF_IN_ERRORS = (SAI_PORT_STAT_IF_IN_DISCARDS + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_IF_IN_UNKNOWN_PROTOS = (SAI_PORT_STAT_IF_IN_ERRORS + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_IF_IN_BROADCAST_PKTS = (SAI_PORT_STAT_IF_IN_UNKNOWN_PROTOS + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_IF_IN_MULTICAST_PKTS = (SAI_PORT_STAT_IF_IN_BROADCAST_PKTS + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_IF_IN_VLAN_DISCARDS = (SAI_PORT_STAT_IF_IN_MULTICAST_PKTS + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_IF_OUT_OCTETS = (SAI_PORT_STAT_IF_IN_VLAN_DISCARDS + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_IF_OUT_UCAST_PKTS = (SAI_PORT_STAT_IF_OUT_OCTETS + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_IF_OUT_NON_UCAST_PKTS = (SAI_PORT_STAT_IF_OUT_UCAST_PKTS + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_IF_OUT_DISCARDS = (SAI_PORT_STAT_IF_OUT_NON_UCAST_PKTS + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_IF_OUT_ERRORS = (SAI_PORT_STAT_IF_OUT_DISCARDS + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_IF_OUT_QLEN = (SAI_PORT_STAT_IF_OUT_ERRORS + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_IF_OUT_BROADCAST_PKTS = (SAI_PORT_STAT_IF_OUT_QLEN + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_IF_OUT_MULTICAST_PKTS = (SAI_PORT_STAT_IF_OUT_BROADCAST_PKTS + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_ETHER_STATS_DROP_EVENTS = (SAI_PORT_STAT_IF_OUT_MULTICAST_PKTS + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_ETHER_STATS_MULTICAST_PKTS = (SAI_PORT_STAT_ETHER_STATS_DROP_EVENTS + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_ETHER_STATS_BROADCAST_PKTS = (SAI_PORT_STAT_ETHER_STATS_MULTICAST_PKTS + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_ETHER_STATS_UNDERSIZE_PKTS = (SAI_PORT_STAT_ETHER_STATS_BROADCAST_PKTS + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_ETHER_STATS_FRAGMENTS = (SAI_PORT_STAT_ETHER_STATS_UNDERSIZE_PKTS + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_ETHER_STATS_PKTS_64_OCTETS = (SAI_PORT_STAT_ETHER_STATS_FRAGMENTS + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_ETHER_STATS_PKTS_65_TO_127_OCTETS = (SAI_PORT_STAT_ETHER_STATS_PKTS_64_OCTETS + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_ETHER_STATS_PKTS_128_TO_255_OCTETS = (SAI_PORT_STAT_ETHER_STATS_PKTS_65_TO_127_OCTETS + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_ETHER_STATS_PKTS_256_TO_511_OCTETS = (SAI_PORT_STAT_ETHER_STATS_PKTS_128_TO_255_OCTETS + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_ETHER_STATS_PKTS_512_TO_1023_OCTETS = (SAI_PORT_STAT_ETHER_STATS_PKTS_256_TO_511_OCTETS + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_ETHER_STATS_PKTS_1024_TO_1518_OCTETS = (SAI_PORT_STAT_ETHER_STATS_PKTS_512_TO_1023_OCTETS + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_ETHER_STATS_PKTS_1519_TO_2047_OCTETS = (SAI_PORT_STAT_ETHER_STATS_PKTS_1024_TO_1518_OCTETS + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_ETHER_STATS_PKTS_2048_TO_4095_OCTETS = (SAI_PORT_STAT_ETHER_STATS_PKTS_1519_TO_2047_OCTETS + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_ETHER_STATS_PKTS_4096_TO_9216_OCTETS = (SAI_PORT_STAT_ETHER_STATS_PKTS_2048_TO_4095_OCTETS + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_ETHER_STATS_PKTS_9217_TO_16383_OCTETS = (SAI_PORT_STAT_ETHER_STATS_PKTS_4096_TO_9216_OCTETS + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_ETHER_STATS_OVERSIZE_PKTS = (SAI_PORT_STAT_ETHER_STATS_PKTS_9217_TO_16383_OCTETS + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_ETHER_RX_OVERSIZE_PKTS = (SAI_PORT_STAT_ETHER_STATS_OVERSIZE_PKTS + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_ETHER_TX_OVERSIZE_PKTS = (SAI_PORT_STAT_ETHER_RX_OVERSIZE_PKTS + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_ETHER_STATS_JABBERS = (SAI_PORT_STAT_ETHER_TX_OVERSIZE_PKTS + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_ETHER_STATS_OCTETS = (SAI_PORT_STAT_ETHER_STATS_JABBERS + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_ETHER_STATS_PKTS = (SAI_PORT_STAT_ETHER_STATS_OCTETS + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_ETHER_STATS_COLLISIONS = (SAI_PORT_STAT_ETHER_STATS_PKTS + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_ETHER_STATS_CRC_ALIGN_ERRORS = (SAI_PORT_STAT_ETHER_STATS_COLLISIONS + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_ETHER_STATS_TX_NO_ERRORS = (SAI_PORT_STAT_ETHER_STATS_CRC_ALIGN_ERRORS + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_ETHER_STATS_RX_NO_ERRORS = (SAI_PORT_STAT_ETHER_STATS_TX_NO_ERRORS + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_IP_IN_RECEIVES = (SAI_PORT_STAT_ETHER_STATS_RX_NO_ERRORS + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_IP_IN_OCTETS = (SAI_PORT_STAT_IP_IN_RECEIVES + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_IP_IN_UCAST_PKTS = (SAI_PORT_STAT_IP_IN_OCTETS + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_IP_IN_NON_UCAST_PKTS = (SAI_PORT_STAT_IP_IN_UCAST_PKTS + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_IP_IN_DISCARDS = (SAI_PORT_STAT_IP_IN_NON_UCAST_PKTS + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_IP_OUT_OCTETS = (SAI_PORT_STAT_IP_IN_DISCARDS + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_IP_OUT_UCAST_PKTS = (SAI_PORT_STAT_IP_OUT_OCTETS + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_IP_OUT_NON_UCAST_PKTS = (SAI_PORT_STAT_IP_OUT_UCAST_PKTS + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_IP_OUT_DISCARDS = (SAI_PORT_STAT_IP_OUT_NON_UCAST_PKTS + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_IPV6_IN_RECEIVES = (SAI_PORT_STAT_IP_OUT_DISCARDS + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_IPV6_IN_OCTETS = (SAI_PORT_STAT_IPV6_IN_RECEIVES + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_IPV6_IN_UCAST_PKTS = (SAI_PORT_STAT_IPV6_IN_OCTETS + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_IPV6_IN_NON_UCAST_PKTS = (SAI_PORT_STAT_IPV6_IN_UCAST_PKTS + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_IPV6_IN_MCAST_PKTS = (SAI_PORT_STAT_IPV6_IN_NON_UCAST_PKTS + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_IPV6_IN_DISCARDS = (SAI_PORT_STAT_IPV6_IN_MCAST_PKTS + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_IPV6_OUT_OCTETS = (SAI_PORT_STAT_IPV6_IN_DISCARDS + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_IPV6_OUT_UCAST_PKTS = (SAI_PORT_STAT_IPV6_OUT_OCTETS + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_IPV6_OUT_NON_UCAST_PKTS = (SAI_PORT_STAT_IPV6_OUT_UCAST_PKTS + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_IPV6_OUT_MCAST_PKTS = (SAI_PORT_STAT_IPV6_OUT_NON_UCAST_PKTS + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_IPV6_OUT_DISCARDS = (SAI_PORT_STAT_IPV6_OUT_MCAST_PKTS + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_GREEN_WRED_DROPPED_PACKETS = (SAI_PORT_STAT_IPV6_OUT_DISCARDS + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_GREEN_WRED_DROPPED_BYTES = (SAI_PORT_STAT_GREEN_WRED_DROPPED_PACKETS + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_YELLOW_WRED_DROPPED_PACKETS = (SAI_PORT_STAT_GREEN_WRED_DROPPED_BYTES + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_YELLOW_WRED_DROPPED_BYTES = (SAI_PORT_STAT_YELLOW_WRED_DROPPED_PACKETS + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_RED_WRED_DROPPED_PACKETS = (SAI_PORT_STAT_YELLOW_WRED_DROPPED_BYTES + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_RED_WRED_DROPPED_BYTES = (SAI_PORT_STAT_RED_WRED_DROPPED_PACKETS + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_WRED_DROPPED_PACKETS = (SAI_PORT_STAT_RED_WRED_DROPPED_BYTES + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_WRED_DROPPED_BYTES = (SAI_PORT_STAT_WRED_DROPPED_PACKETS + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_ECN_MARKED_PACKETS = (SAI_PORT_STAT_WRED_DROPPED_BYTES + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_ETHER_IN_PKTS_64_OCTETS = (SAI_PORT_STAT_ECN_MARKED_PACKETS + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_ETHER_IN_PKTS_65_TO_127_OCTETS = (SAI_PORT_STAT_ETHER_IN_PKTS_64_OCTETS + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_ETHER_IN_PKTS_128_TO_255_OCTETS = (SAI_PORT_STAT_ETHER_IN_PKTS_65_TO_127_OCTETS + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_ETHER_IN_PKTS_256_TO_511_OCTETS = (SAI_PORT_STAT_ETHER_IN_PKTS_128_TO_255_OCTETS + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_ETHER_IN_PKTS_512_TO_1023_OCTETS = (SAI_PORT_STAT_ETHER_IN_PKTS_256_TO_511_OCTETS + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_ETHER_IN_PKTS_1024_TO_1518_OCTETS = (SAI_PORT_STAT_ETHER_IN_PKTS_512_TO_1023_OCTETS + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_ETHER_IN_PKTS_1519_TO_2047_OCTETS = (SAI_PORT_STAT_ETHER_IN_PKTS_1024_TO_1518_OCTETS + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_ETHER_IN_PKTS_2048_TO_4095_OCTETS = (SAI_PORT_STAT_ETHER_IN_PKTS_1519_TO_2047_OCTETS + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_ETHER_IN_PKTS_4096_TO_9216_OCTETS = (SAI_PORT_STAT_ETHER_IN_PKTS_2048_TO_4095_OCTETS + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_ETHER_IN_PKTS_9217_TO_16383_OCTETS = (SAI_PORT_STAT_ETHER_IN_PKTS_4096_TO_9216_OCTETS + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_ETHER_OUT_PKTS_64_OCTETS = (SAI_PORT_STAT_ETHER_IN_PKTS_9217_TO_16383_OCTETS + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_ETHER_OUT_PKTS_65_TO_127_OCTETS = (SAI_PORT_STAT_ETHER_OUT_PKTS_64_OCTETS + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_ETHER_OUT_PKTS_128_TO_255_OCTETS = (SAI_PORT_STAT_ETHER_OUT_PKTS_65_TO_127_OCTETS + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_ETHER_OUT_PKTS_256_TO_511_OCTETS = (SAI_PORT_STAT_ETHER_OUT_PKTS_128_TO_255_OCTETS + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_ETHER_OUT_PKTS_512_TO_1023_OCTETS = (SAI_PORT_STAT_ETHER_OUT_PKTS_256_TO_511_OCTETS + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_ETHER_OUT_PKTS_1024_TO_1518_OCTETS = (SAI_PORT_STAT_ETHER_OUT_PKTS_512_TO_1023_OCTETS + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_ETHER_OUT_PKTS_1519_TO_2047_OCTETS = (SAI_PORT_STAT_ETHER_OUT_PKTS_1024_TO_1518_OCTETS + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_ETHER_OUT_PKTS_2048_TO_4095_OCTETS = (SAI_PORT_STAT_ETHER_OUT_PKTS_1519_TO_2047_OCTETS + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_ETHER_OUT_PKTS_4096_TO_9216_OCTETS = (SAI_PORT_STAT_ETHER_OUT_PKTS_2048_TO_4095_OCTETS + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_ETHER_OUT_PKTS_9217_TO_16383_OCTETS = (SAI_PORT_STAT_ETHER_OUT_PKTS_4096_TO_9216_OCTETS + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_IN_CURR_OCCUPANCY_BYTES = (SAI_PORT_STAT_ETHER_OUT_PKTS_9217_TO_16383_OCTETS + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_IN_WATERMARK_BYTES = (SAI_PORT_STAT_IN_CURR_OCCUPANCY_BYTES + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_IN_SHARED_CURR_OCCUPANCY_BYTES = (SAI_PORT_STAT_IN_WATERMARK_BYTES + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_IN_SHARED_WATERMARK_BYTES = (SAI_PORT_STAT_IN_SHARED_CURR_OCCUPANCY_BYTES + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_OUT_CURR_OCCUPANCY_BYTES = (SAI_PORT_STAT_IN_SHARED_WATERMARK_BYTES + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_OUT_WATERMARK_BYTES = (SAI_PORT_STAT_OUT_CURR_OCCUPANCY_BYTES + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_OUT_SHARED_CURR_OCCUPANCY_BYTES = (SAI_PORT_STAT_OUT_WATERMARK_BYTES + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_OUT_SHARED_WATERMARK_BYTES = (SAI_PORT_STAT_OUT_SHARED_CURR_OCCUPANCY_BYTES + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_IN_DROPPED_PKTS = (SAI_PORT_STAT_OUT_SHARED_WATERMARK_BYTES + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_OUT_DROPPED_PKTS = (SAI_PORT_STAT_IN_DROPPED_PKTS + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_PAUSE_RX_PKTS = (SAI_PORT_STAT_OUT_DROPPED_PKTS + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_PAUSE_TX_PKTS = (SAI_PORT_STAT_PAUSE_RX_PKTS + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_PFC_0_RX_PKTS = (SAI_PORT_STAT_PAUSE_TX_PKTS + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_PFC_0_TX_PKTS = (SAI_PORT_STAT_PFC_0_RX_PKTS + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_PFC_1_RX_PKTS = (SAI_PORT_STAT_PFC_0_TX_PKTS + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_PFC_1_TX_PKTS = (SAI_PORT_STAT_PFC_1_RX_PKTS + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_PFC_2_RX_PKTS = (SAI_PORT_STAT_PFC_1_TX_PKTS + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_PFC_2_TX_PKTS = (SAI_PORT_STAT_PFC_2_RX_PKTS + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_PFC_3_RX_PKTS = (SAI_PORT_STAT_PFC_2_TX_PKTS + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_PFC_3_TX_PKTS = (SAI_PORT_STAT_PFC_3_RX_PKTS + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_PFC_4_RX_PKTS = (SAI_PORT_STAT_PFC_3_TX_PKTS + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_PFC_4_TX_PKTS = (SAI_PORT_STAT_PFC_4_RX_PKTS + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_PFC_5_RX_PKTS = (SAI_PORT_STAT_PFC_4_TX_PKTS + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_PFC_5_TX_PKTS = (SAI_PORT_STAT_PFC_5_RX_PKTS + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_PFC_6_RX_PKTS = (SAI_PORT_STAT_PFC_5_TX_PKTS + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_PFC_6_TX_PKTS = (SAI_PORT_STAT_PFC_6_RX_PKTS + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_PFC_7_RX_PKTS = (SAI_PORT_STAT_PFC_6_TX_PKTS + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_PFC_7_TX_PKTS = (SAI_PORT_STAT_PFC_7_RX_PKTS + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_PFC_0_RX_PAUSE_DURATION = (SAI_PORT_STAT_PFC_7_TX_PKTS + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_PFC_0_TX_PAUSE_DURATION = (SAI_PORT_STAT_PFC_0_RX_PAUSE_DURATION + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_PFC_1_RX_PAUSE_DURATION = (SAI_PORT_STAT_PFC_0_TX_PAUSE_DURATION + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_PFC_1_TX_PAUSE_DURATION = (SAI_PORT_STAT_PFC_1_RX_PAUSE_DURATION + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_PFC_2_RX_PAUSE_DURATION = (SAI_PORT_STAT_PFC_1_TX_PAUSE_DURATION + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_PFC_2_TX_PAUSE_DURATION = (SAI_PORT_STAT_PFC_2_RX_PAUSE_DURATION + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_PFC_3_RX_PAUSE_DURATION = (SAI_PORT_STAT_PFC_2_TX_PAUSE_DURATION + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_PFC_3_TX_PAUSE_DURATION = (SAI_PORT_STAT_PFC_3_RX_PAUSE_DURATION + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_PFC_4_RX_PAUSE_DURATION = (SAI_PORT_STAT_PFC_3_TX_PAUSE_DURATION + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_PFC_4_TX_PAUSE_DURATION = (SAI_PORT_STAT_PFC_4_RX_PAUSE_DURATION + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_PFC_5_RX_PAUSE_DURATION = (SAI_PORT_STAT_PFC_4_TX_PAUSE_DURATION + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_PFC_5_TX_PAUSE_DURATION = (SAI_PORT_STAT_PFC_5_RX_PAUSE_DURATION + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_PFC_6_RX_PAUSE_DURATION = (SAI_PORT_STAT_PFC_5_TX_PAUSE_DURATION + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_PFC_6_TX_PAUSE_DURATION = (SAI_PORT_STAT_PFC_6_RX_PAUSE_DURATION + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_PFC_7_RX_PAUSE_DURATION = (SAI_PORT_STAT_PFC_6_TX_PAUSE_DURATION + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_PFC_7_TX_PAUSE_DURATION = (SAI_PORT_STAT_PFC_7_RX_PAUSE_DURATION + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_PFC_0_RX_PAUSE_DURATION_US = (SAI_PORT_STAT_PFC_7_TX_PAUSE_DURATION + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_PFC_0_TX_PAUSE_DURATION_US = (SAI_PORT_STAT_PFC_0_RX_PAUSE_DURATION_US + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_PFC_1_RX_PAUSE_DURATION_US = (SAI_PORT_STAT_PFC_0_TX_PAUSE_DURATION_US + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_PFC_1_TX_PAUSE_DURATION_US = (SAI_PORT_STAT_PFC_1_RX_PAUSE_DURATION_US + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_PFC_2_RX_PAUSE_DURATION_US = (SAI_PORT_STAT_PFC_1_TX_PAUSE_DURATION_US + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_PFC_2_TX_PAUSE_DURATION_US = (SAI_PORT_STAT_PFC_2_RX_PAUSE_DURATION_US + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_PFC_3_RX_PAUSE_DURATION_US = (SAI_PORT_STAT_PFC_2_TX_PAUSE_DURATION_US + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_PFC_3_TX_PAUSE_DURATION_US = (SAI_PORT_STAT_PFC_3_RX_PAUSE_DURATION_US + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_PFC_4_RX_PAUSE_DURATION_US = (SAI_PORT_STAT_PFC_3_TX_PAUSE_DURATION_US + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_PFC_4_TX_PAUSE_DURATION_US = (SAI_PORT_STAT_PFC_4_RX_PAUSE_DURATION_US + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_PFC_5_RX_PAUSE_DURATION_US = (SAI_PORT_STAT_PFC_4_TX_PAUSE_DURATION_US + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_PFC_5_TX_PAUSE_DURATION_US = (SAI_PORT_STAT_PFC_5_RX_PAUSE_DURATION_US + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_PFC_6_RX_PAUSE_DURATION_US = (SAI_PORT_STAT_PFC_5_TX_PAUSE_DURATION_US + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_PFC_6_TX_PAUSE_DURATION_US = (SAI_PORT_STAT_PFC_6_RX_PAUSE_DURATION_US + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_PFC_7_RX_PAUSE_DURATION_US = (SAI_PORT_STAT_PFC_6_TX_PAUSE_DURATION_US + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_PFC_7_TX_PAUSE_DURATION_US = (SAI_PORT_STAT_PFC_7_RX_PAUSE_DURATION_US + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_PFC_0_ON2OFF_RX_PKTS = (SAI_PORT_STAT_PFC_7_TX_PAUSE_DURATION_US + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_PFC_1_ON2OFF_RX_PKTS = (SAI_PORT_STAT_PFC_0_ON2OFF_RX_PKTS + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_PFC_2_ON2OFF_RX_PKTS = (SAI_PORT_STAT_PFC_1_ON2OFF_RX_PKTS + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_PFC_3_ON2OFF_RX_PKTS = (SAI_PORT_STAT_PFC_2_ON2OFF_RX_PKTS + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_PFC_4_ON2OFF_RX_PKTS = (SAI_PORT_STAT_PFC_3_ON2OFF_RX_PKTS + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_PFC_5_ON2OFF_RX_PKTS = (SAI_PORT_STAT_PFC_4_ON2OFF_RX_PKTS + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_PFC_6_ON2OFF_RX_PKTS = (SAI_PORT_STAT_PFC_5_ON2OFF_RX_PKTS + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_PFC_7_ON2OFF_RX_PKTS = (SAI_PORT_STAT_PFC_6_ON2OFF_RX_PKTS + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_DOT3_STATS_ALIGNMENT_ERRORS = (SAI_PORT_STAT_PFC_7_ON2OFF_RX_PKTS + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_DOT3_STATS_FCS_ERRORS = (SAI_PORT_STAT_DOT3_STATS_ALIGNMENT_ERRORS + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_DOT3_STATS_SINGLE_COLLISION_FRAMES = (SAI_PORT_STAT_DOT3_STATS_FCS_ERRORS + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_DOT3_STATS_MULTIPLE_COLLISION_FRAMES = (SAI_PORT_STAT_DOT3_STATS_SINGLE_COLLISION_FRAMES + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_DOT3_STATS_SQE_TEST_ERRORS = (SAI_PORT_STAT_DOT3_STATS_MULTIPLE_COLLISION_FRAMES + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_DOT3_STATS_DEFERRED_TRANSMISSIONS = (SAI_PORT_STAT_DOT3_STATS_SQE_TEST_ERRORS + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_DOT3_STATS_LATE_COLLISIONS = (SAI_PORT_STAT_DOT3_STATS_DEFERRED_TRANSMISSIONS + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_DOT3_STATS_EXCESSIVE_COLLISIONS = (SAI_PORT_STAT_DOT3_STATS_LATE_COLLISIONS + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_DOT3_STATS_INTERNAL_MAC_TRANSMIT_ERRORS = (SAI_PORT_STAT_DOT3_STATS_EXCESSIVE_COLLISIONS + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_DOT3_STATS_CARRIER_SENSE_ERRORS = (SAI_PORT_STAT_DOT3_STATS_INTERNAL_MAC_TRANSMIT_ERRORS + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_DOT3_STATS_FRAME_TOO_LONGS = (SAI_PORT_STAT_DOT3_STATS_CARRIER_SENSE_ERRORS + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_DOT3_STATS_INTERNAL_MAC_RECEIVE_ERRORS = (SAI_PORT_STAT_DOT3_STATS_FRAME_TOO_LONGS + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_DOT3_STATS_SYMBOL_ERRORS = (SAI_PORT_STAT_DOT3_STATS_INTERNAL_MAC_RECEIVE_ERRORS + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_DOT3_CONTROL_IN_UNKNOWN_OPCODES = (SAI_PORT_STAT_DOT3_STATS_SYMBOL_ERRORS + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_EEE_TX_EVENT_COUNT = (SAI_PORT_STAT_DOT3_CONTROL_IN_UNKNOWN_OPCODES + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_EEE_RX_EVENT_COUNT = (SAI_PORT_STAT_EEE_TX_EVENT_COUNT + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_EEE_TX_DURATION = (SAI_PORT_STAT_EEE_RX_EVENT_COUNT + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_EEE_RX_DURATION = (SAI_PORT_STAT_EEE_TX_DURATION + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_PRBS_ERROR_COUNT = (SAI_PORT_STAT_EEE_RX_DURATION + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_IF_IN_FEC_CORRECTABLE_FRAMES = (SAI_PORT_STAT_PRBS_ERROR_COUNT + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_IF_IN_FEC_NOT_CORRECTABLE_FRAMES = (SAI_PORT_STAT_IF_IN_FEC_CORRECTABLE_FRAMES + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_IF_IN_FEC_SYMBOL_ERRORS = (SAI_PORT_STAT_IF_IN_FEC_NOT_CORRECTABLE_FRAMES + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_IF_IN_FABRIC_DATA_UNITS = (SAI_PORT_STAT_IF_IN_FEC_SYMBOL_ERRORS + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_IF_OUT_FABRIC_DATA_UNITS = (SAI_PORT_STAT_IF_IN_FABRIC_DATA_UNITS + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_IF_IN_FEC_CODEWORD_ERRORS_S0 = (SAI_PORT_STAT_IF_OUT_FABRIC_DATA_UNITS + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_IF_IN_FEC_CODEWORD_ERRORS_S1 = (SAI_PORT_STAT_IF_IN_FEC_CODEWORD_ERRORS_S0 + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_IF_IN_FEC_CODEWORD_ERRORS_S2 = (SAI_PORT_STAT_IF_IN_FEC_CODEWORD_ERRORS_S1 + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_IF_IN_FEC_CODEWORD_ERRORS_S3 = (SAI_PORT_STAT_IF_IN_FEC_CODEWORD_ERRORS_S2 + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_IF_IN_FEC_CODEWORD_ERRORS_S4 = (SAI_PORT_STAT_IF_IN_FEC_CODEWORD_ERRORS_S3 + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_IF_IN_FEC_CODEWORD_ERRORS_S5 = (SAI_PORT_STAT_IF_IN_FEC_CODEWORD_ERRORS_S4 + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_IF_IN_FEC_CODEWORD_ERRORS_S6 = (SAI_PORT_STAT_IF_IN_FEC_CODEWORD_ERRORS_S5 + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_IF_IN_FEC_CODEWORD_ERRORS_S7 = (SAI_PORT_STAT_IF_IN_FEC_CODEWORD_ERRORS_S6 + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_IF_IN_FEC_CODEWORD_ERRORS_S8 = (SAI_PORT_STAT_IF_IN_FEC_CODEWORD_ERRORS_S7 + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_IF_IN_FEC_CODEWORD_ERRORS_S9 = (SAI_PORT_STAT_IF_IN_FEC_CODEWORD_ERRORS_S8 + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_IF_IN_FEC_CODEWORD_ERRORS_S10 = (SAI_PORT_STAT_IF_IN_FEC_CODEWORD_ERRORS_S9 + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_IF_IN_FEC_CODEWORD_ERRORS_S11 = (SAI_PORT_STAT_IF_IN_FEC_CODEWORD_ERRORS_S10 + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_IF_IN_FEC_CODEWORD_ERRORS_S12 = (SAI_PORT_STAT_IF_IN_FEC_CODEWORD_ERRORS_S11 + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_IF_IN_FEC_CODEWORD_ERRORS_S13 = (SAI_PORT_STAT_IF_IN_FEC_CODEWORD_ERRORS_S12 + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_IF_IN_FEC_CODEWORD_ERRORS_S14 = (SAI_PORT_STAT_IF_IN_FEC_CODEWORD_ERRORS_S13 + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_IF_IN_FEC_CODEWORD_ERRORS_S15 = (SAI_PORT_STAT_IF_IN_FEC_CODEWORD_ERRORS_S14 + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_IF_IN_FEC_CODEWORD_ERRORS_S16 = (SAI_PORT_STAT_IF_IN_FEC_CODEWORD_ERRORS_S15 + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_IF_IN_FEC_CORRECTED_BITS = (SAI_PORT_STAT_IF_IN_FEC_CODEWORD_ERRORS_S16 + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_IN_DROP_REASON_RANGE_BASE = 0x00001000# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_IN_CONFIGURED_DROP_REASONS_0_DROPPED_PKTS = SAI_PORT_STAT_IN_DROP_REASON_RANGE_BASE# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_IN_CONFIGURED_DROP_REASONS_1_DROPPED_PKTS = (SAI_PORT_STAT_IN_CONFIGURED_DROP_REASONS_0_DROPPED_PKTS + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_IN_CONFIGURED_DROP_REASONS_2_DROPPED_PKTS = (SAI_PORT_STAT_IN_CONFIGURED_DROP_REASONS_1_DROPPED_PKTS + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_IN_CONFIGURED_DROP_REASONS_3_DROPPED_PKTS = (SAI_PORT_STAT_IN_CONFIGURED_DROP_REASONS_2_DROPPED_PKTS + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_IN_CONFIGURED_DROP_REASONS_4_DROPPED_PKTS = (SAI_PORT_STAT_IN_CONFIGURED_DROP_REASONS_3_DROPPED_PKTS + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_IN_CONFIGURED_DROP_REASONS_5_DROPPED_PKTS = (SAI_PORT_STAT_IN_CONFIGURED_DROP_REASONS_4_DROPPED_PKTS + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_IN_CONFIGURED_DROP_REASONS_6_DROPPED_PKTS = (SAI_PORT_STAT_IN_CONFIGURED_DROP_REASONS_5_DROPPED_PKTS + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_IN_CONFIGURED_DROP_REASONS_7_DROPPED_PKTS = (SAI_PORT_STAT_IN_CONFIGURED_DROP_REASONS_6_DROPPED_PKTS + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_IN_DROP_REASON_RANGE_END = 0x00001fff# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_OUT_DROP_REASON_RANGE_BASE = 0x00002000# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_OUT_CONFIGURED_DROP_REASONS_0_DROPPED_PKTS = SAI_PORT_STAT_OUT_DROP_REASON_RANGE_BASE# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_OUT_CONFIGURED_DROP_REASONS_1_DROPPED_PKTS = (SAI_PORT_STAT_OUT_CONFIGURED_DROP_REASONS_0_DROPPED_PKTS + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_OUT_CONFIGURED_DROP_REASONS_2_DROPPED_PKTS = (SAI_PORT_STAT_OUT_CONFIGURED_DROP_REASONS_1_DROPPED_PKTS + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_OUT_CONFIGURED_DROP_REASONS_3_DROPPED_PKTS = (SAI_PORT_STAT_OUT_CONFIGURED_DROP_REASONS_2_DROPPED_PKTS + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_OUT_CONFIGURED_DROP_REASONS_4_DROPPED_PKTS = (SAI_PORT_STAT_OUT_CONFIGURED_DROP_REASONS_3_DROPPED_PKTS + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_OUT_CONFIGURED_DROP_REASONS_5_DROPPED_PKTS = (SAI_PORT_STAT_OUT_CONFIGURED_DROP_REASONS_4_DROPPED_PKTS + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_OUT_CONFIGURED_DROP_REASONS_6_DROPPED_PKTS = (SAI_PORT_STAT_OUT_CONFIGURED_DROP_REASONS_5_DROPPED_PKTS + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_OUT_CONFIGURED_DROP_REASONS_7_DROPPED_PKTS = (SAI_PORT_STAT_OUT_CONFIGURED_DROP_REASONS_6_DROPPED_PKTS + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_OUT_DROP_REASON_RANGE_END = 0x00002fff# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

SAI_PORT_STAT_END = (SAI_PORT_STAT_OUT_DROP_REASON_RANGE_END + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

sai_port_stat_t = enum__sai_port_stat_t# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3226

sai_create_port_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3238

sai_remove_port_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3251

sai_set_port_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3262

sai_get_port_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3275

sai_get_port_stats_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, uint32_t, POINTER(sai_stat_id_t), POINTER(uint64_t))# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3290

sai_get_port_stats_ext_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, uint32_t, POINTER(sai_stat_id_t), sai_stats_mode_t, POINTER(uint64_t))# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3307

sai_clear_port_stats_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, uint32_t, POINTER(sai_stat_id_t))# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3323

sai_clear_port_all_stats_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3335

sai_port_state_change_notification_fn = CFUNCTYPE(UNCHECKED(None), uint32_t, POINTER(sai_port_oper_status_notification_t))# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3348

sai_port_host_tx_ready_notification_fn = CFUNCTYPE(UNCHECKED(None), sai_object_id_t, sai_object_id_t, sai_port_host_tx_ready_status_t)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3364

enum__sai_port_pool_attr_t = c_int# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3426

SAI_PORT_POOL_ATTR_START = 0# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3426

SAI_PORT_POOL_ATTR_PORT_ID = SAI_PORT_POOL_ATTR_START# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3426

SAI_PORT_POOL_ATTR_BUFFER_POOL_ID = (SAI_PORT_POOL_ATTR_PORT_ID + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3426

SAI_PORT_POOL_ATTR_QOS_WRED_PROFILE_ID = (SAI_PORT_POOL_ATTR_BUFFER_POOL_ID + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3426

SAI_PORT_POOL_ATTR_END = (SAI_PORT_POOL_ATTR_QOS_WRED_PROFILE_ID + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3426

SAI_PORT_POOL_ATTR_CUSTOM_RANGE_START = 0x10000000# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3426

SAI_PORT_POOL_ATTR_CUSTOM_RANGE_END = (SAI_PORT_POOL_ATTR_CUSTOM_RANGE_START + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3426

sai_port_pool_attr_t = enum__sai_port_pool_attr_t# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3426

enum__sai_port_pool_stat_t = c_int# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3499

SAI_PORT_POOL_STAT_IF_OCTETS = 0# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3499

SAI_PORT_POOL_STAT_GREEN_WRED_DROPPED_PACKETS = (SAI_PORT_POOL_STAT_IF_OCTETS + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3499

SAI_PORT_POOL_STAT_GREEN_WRED_DROPPED_BYTES = (SAI_PORT_POOL_STAT_GREEN_WRED_DROPPED_PACKETS + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3499

SAI_PORT_POOL_STAT_YELLOW_WRED_DROPPED_PACKETS = (SAI_PORT_POOL_STAT_GREEN_WRED_DROPPED_BYTES + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3499

SAI_PORT_POOL_STAT_YELLOW_WRED_DROPPED_BYTES = (SAI_PORT_POOL_STAT_YELLOW_WRED_DROPPED_PACKETS + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3499

SAI_PORT_POOL_STAT_RED_WRED_DROPPED_PACKETS = (SAI_PORT_POOL_STAT_YELLOW_WRED_DROPPED_BYTES + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3499

SAI_PORT_POOL_STAT_RED_WRED_DROPPED_BYTES = (SAI_PORT_POOL_STAT_RED_WRED_DROPPED_PACKETS + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3499

SAI_PORT_POOL_STAT_WRED_DROPPED_PACKETS = (SAI_PORT_POOL_STAT_RED_WRED_DROPPED_BYTES + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3499

SAI_PORT_POOL_STAT_WRED_DROPPED_BYTES = (SAI_PORT_POOL_STAT_WRED_DROPPED_PACKETS + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3499

SAI_PORT_POOL_STAT_GREEN_WRED_ECN_MARKED_PACKETS = (SAI_PORT_POOL_STAT_WRED_DROPPED_BYTES + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3499

SAI_PORT_POOL_STAT_GREEN_WRED_ECN_MARKED_BYTES = (SAI_PORT_POOL_STAT_GREEN_WRED_ECN_MARKED_PACKETS + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3499

SAI_PORT_POOL_STAT_YELLOW_WRED_ECN_MARKED_PACKETS = (SAI_PORT_POOL_STAT_GREEN_WRED_ECN_MARKED_BYTES + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3499

SAI_PORT_POOL_STAT_YELLOW_WRED_ECN_MARKED_BYTES = (SAI_PORT_POOL_STAT_YELLOW_WRED_ECN_MARKED_PACKETS + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3499

SAI_PORT_POOL_STAT_RED_WRED_ECN_MARKED_PACKETS = (SAI_PORT_POOL_STAT_YELLOW_WRED_ECN_MARKED_BYTES + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3499

SAI_PORT_POOL_STAT_RED_WRED_ECN_MARKED_BYTES = (SAI_PORT_POOL_STAT_RED_WRED_ECN_MARKED_PACKETS + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3499

SAI_PORT_POOL_STAT_WRED_ECN_MARKED_PACKETS = (SAI_PORT_POOL_STAT_RED_WRED_ECN_MARKED_BYTES + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3499

SAI_PORT_POOL_STAT_WRED_ECN_MARKED_BYTES = (SAI_PORT_POOL_STAT_WRED_ECN_MARKED_PACKETS + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3499

SAI_PORT_POOL_STAT_CURR_OCCUPANCY_BYTES = (SAI_PORT_POOL_STAT_WRED_ECN_MARKED_BYTES + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3499

SAI_PORT_POOL_STAT_WATERMARK_BYTES = (SAI_PORT_POOL_STAT_CURR_OCCUPANCY_BYTES + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3499

SAI_PORT_POOL_STAT_SHARED_CURR_OCCUPANCY_BYTES = (SAI_PORT_POOL_STAT_WATERMARK_BYTES + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3499

SAI_PORT_POOL_STAT_SHARED_WATERMARK_BYTES = (SAI_PORT_POOL_STAT_SHARED_CURR_OCCUPANCY_BYTES + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3499

SAI_PORT_POOL_STAT_DROPPED_PKTS = (SAI_PORT_POOL_STAT_SHARED_WATERMARK_BYTES + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3499

sai_port_pool_stat_t = enum__sai_port_pool_stat_t# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3499

sai_create_port_pool_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3511

sai_remove_port_pool_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3524

sai_set_port_pool_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3535

sai_get_port_pool_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3548

sai_get_port_pool_stats_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, uint32_t, POINTER(sai_stat_id_t), POINTER(uint64_t))# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3563

sai_get_port_pool_stats_ext_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, uint32_t, POINTER(sai_stat_id_t), sai_stats_mode_t, POINTER(uint64_t))# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3580

sai_clear_port_pool_stats_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, uint32_t, POINTER(sai_stat_id_t))# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3596

enum__sai_port_serdes_attr_t = c_int# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3878

SAI_PORT_SERDES_ATTR_START = 0# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3878

SAI_PORT_SERDES_ATTR_PORT_ID = SAI_PORT_SERDES_ATTR_START# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3878

SAI_PORT_SERDES_ATTR_PREEMPHASIS = (SAI_PORT_SERDES_ATTR_PORT_ID + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3878

SAI_PORT_SERDES_ATTR_IDRIVER = (SAI_PORT_SERDES_ATTR_PREEMPHASIS + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3878

SAI_PORT_SERDES_ATTR_IPREDRIVER = (SAI_PORT_SERDES_ATTR_IDRIVER + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3878

SAI_PORT_SERDES_ATTR_TX_FIR_PRE1 = (SAI_PORT_SERDES_ATTR_IPREDRIVER + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3878

SAI_PORT_SERDES_ATTR_TX_FIR_PRE2 = (SAI_PORT_SERDES_ATTR_TX_FIR_PRE1 + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3878

SAI_PORT_SERDES_ATTR_TX_FIR_PRE3 = (SAI_PORT_SERDES_ATTR_TX_FIR_PRE2 + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3878

SAI_PORT_SERDES_ATTR_TX_FIR_MAIN = (SAI_PORT_SERDES_ATTR_TX_FIR_PRE3 + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3878

SAI_PORT_SERDES_ATTR_TX_FIR_POST1 = (SAI_PORT_SERDES_ATTR_TX_FIR_MAIN + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3878

SAI_PORT_SERDES_ATTR_TX_FIR_POST2 = (SAI_PORT_SERDES_ATTR_TX_FIR_POST1 + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3878

SAI_PORT_SERDES_ATTR_TX_FIR_POST3 = (SAI_PORT_SERDES_ATTR_TX_FIR_POST2 + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3878

SAI_PORT_SERDES_ATTR_TX_FIR_ATTN = (SAI_PORT_SERDES_ATTR_TX_FIR_POST3 + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3878

SAI_PORT_SERDES_ATTR_TX_PAM4_RATIO = (SAI_PORT_SERDES_ATTR_TX_FIR_ATTN + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3878

SAI_PORT_SERDES_ATTR_TX_OUT_COMMON_MODE = (SAI_PORT_SERDES_ATTR_TX_PAM4_RATIO + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3878

SAI_PORT_SERDES_ATTR_TX_PMOS_COMMON_MODE = (SAI_PORT_SERDES_ATTR_TX_OUT_COMMON_MODE + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3878

SAI_PORT_SERDES_ATTR_TX_NMOS_COMMON_MODE = (SAI_PORT_SERDES_ATTR_TX_PMOS_COMMON_MODE + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3878

SAI_PORT_SERDES_ATTR_TX_PMOS_VLTG_REG = (SAI_PORT_SERDES_ATTR_TX_NMOS_COMMON_MODE + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3878

SAI_PORT_SERDES_ATTR_TX_NMOS_VLTG_REG = (SAI_PORT_SERDES_ATTR_TX_PMOS_VLTG_REG + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3878

SAI_PORT_SERDES_ATTR_TX_PRECODING = (SAI_PORT_SERDES_ATTR_TX_NMOS_VLTG_REG + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3878

SAI_PORT_SERDES_ATTR_RX_PRECODING = (SAI_PORT_SERDES_ATTR_TX_PRECODING + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3878

SAI_PORT_SERDES_ATTR_END = (SAI_PORT_SERDES_ATTR_RX_PRECODING + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3878

SAI_PORT_SERDES_ATTR_CUSTOM_RANGE_START = 0x10000000# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3878

SAI_PORT_SERDES_ATTR_CUSTOM_RANGE_END = (SAI_PORT_SERDES_ATTR_CUSTOM_RANGE_START + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3878

sai_port_serdes_attr_t = enum__sai_port_serdes_attr_t# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3878

sai_create_port_serdes_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3890

sai_remove_port_serdes_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3903

sai_set_port_serdes_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3914

sai_get_port_serdes_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saiport.h: 3927

enum__sai_port_connector_attr_t = c_int# /home/bluecmd/Downloads/SAI/inc/saiport.h: 4002

SAI_PORT_CONNECTOR_ATTR_START = 0# /home/bluecmd/Downloads/SAI/inc/saiport.h: 4002

SAI_PORT_CONNECTOR_ATTR_SYSTEM_SIDE_PORT_ID = SAI_PORT_CONNECTOR_ATTR_START# /home/bluecmd/Downloads/SAI/inc/saiport.h: 4002

SAI_PORT_CONNECTOR_ATTR_LINE_SIDE_PORT_ID = (SAI_PORT_CONNECTOR_ATTR_SYSTEM_SIDE_PORT_ID + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 4002

SAI_PORT_CONNECTOR_ATTR_SYSTEM_SIDE_FAILOVER_PORT_ID = (SAI_PORT_CONNECTOR_ATTR_LINE_SIDE_PORT_ID + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 4002

SAI_PORT_CONNECTOR_ATTR_LINE_SIDE_FAILOVER_PORT_ID = (SAI_PORT_CONNECTOR_ATTR_SYSTEM_SIDE_FAILOVER_PORT_ID + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 4002

SAI_PORT_CONNECTOR_ATTR_FAILOVER_MODE = (SAI_PORT_CONNECTOR_ATTR_LINE_SIDE_FAILOVER_PORT_ID + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 4002

SAI_PORT_CONNECTOR_ATTR_END = (SAI_PORT_CONNECTOR_ATTR_FAILOVER_MODE + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 4002

SAI_PORT_CONNECTOR_ATTR_CUSTOM_RANGE_START = 0x10000000# /home/bluecmd/Downloads/SAI/inc/saiport.h: 4002

SAI_PORT_CONNECTOR_ATTR_CUSTOM_RANGE_END = (SAI_PORT_CONNECTOR_ATTR_CUSTOM_RANGE_START + 1)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 4002

sai_port_connector_attr_t = enum__sai_port_connector_attr_t# /home/bluecmd/Downloads/SAI/inc/saiport.h: 4002

sai_create_port_connector_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saiport.h: 4015

sai_remove_port_connector_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t)# /home/bluecmd/Downloads/SAI/inc/saiport.h: 4028

sai_set_port_connector_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saiport.h: 4039

sai_get_port_connector_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saiport.h: 4052

# /home/bluecmd/Downloads/SAI/inc/saiport.h: 4093
class struct__sai_port_api_t(Structure):
    pass

struct__sai_port_api_t.__slots__ = [
    'create_port',
    'remove_port',
    'set_port_attribute',
    'get_port_attribute',
    'get_port_stats',
    'get_port_stats_ext',
    'clear_port_stats',
    'clear_port_all_stats',
    'create_port_pool',
    'remove_port_pool',
    'set_port_pool_attribute',
    'get_port_pool_attribute',
    'get_port_pool_stats',
    'get_port_pool_stats_ext',
    'clear_port_pool_stats',
    'create_port_connector',
    'remove_port_connector',
    'set_port_connector_attribute',
    'get_port_connector_attribute',
    'create_port_serdes',
    'remove_port_serdes',
    'set_port_serdes_attribute',
    'get_port_serdes_attribute',
    'create_ports',
    'remove_ports',
    'set_ports_attribute',
    'get_ports_attribute',
    'create_port_serdess',
    'remove_port_serdess',
    'set_port_serdess_attribute',
    'get_port_serdess_attribute',
]
struct__sai_port_api_t._fields_ = [
    ('create_port', sai_create_port_fn),
    ('remove_port', sai_remove_port_fn),
    ('set_port_attribute', sai_set_port_attribute_fn),
    ('get_port_attribute', sai_get_port_attribute_fn),
    ('get_port_stats', sai_get_port_stats_fn),
    ('get_port_stats_ext', sai_get_port_stats_ext_fn),
    ('clear_port_stats', sai_clear_port_stats_fn),
    ('clear_port_all_stats', sai_clear_port_all_stats_fn),
    ('create_port_pool', sai_create_port_pool_fn),
    ('remove_port_pool', sai_remove_port_pool_fn),
    ('set_port_pool_attribute', sai_set_port_pool_attribute_fn),
    ('get_port_pool_attribute', sai_get_port_pool_attribute_fn),
    ('get_port_pool_stats', sai_get_port_pool_stats_fn),
    ('get_port_pool_stats_ext', sai_get_port_pool_stats_ext_fn),
    ('clear_port_pool_stats', sai_clear_port_pool_stats_fn),
    ('create_port_connector', sai_create_port_connector_fn),
    ('remove_port_connector', sai_remove_port_connector_fn),
    ('set_port_connector_attribute', sai_set_port_connector_attribute_fn),
    ('get_port_connector_attribute', sai_get_port_connector_attribute_fn),
    ('create_port_serdes', sai_create_port_serdes_fn),
    ('remove_port_serdes', sai_remove_port_serdes_fn),
    ('set_port_serdes_attribute', sai_set_port_serdes_attribute_fn),
    ('get_port_serdes_attribute', sai_get_port_serdes_attribute_fn),
    ('create_ports', sai_bulk_object_create_fn),
    ('remove_ports', sai_bulk_object_remove_fn),
    ('set_ports_attribute', sai_bulk_object_set_attribute_fn),
    ('get_ports_attribute', sai_bulk_object_get_attribute_fn),
    ('create_port_serdess', sai_bulk_object_create_fn),
    ('remove_port_serdess', sai_bulk_object_remove_fn),
    ('set_port_serdess_attribute', sai_bulk_object_set_attribute_fn),
    ('get_port_serdess_attribute', sai_bulk_object_get_attribute_fn),
]

sai_port_api_t = struct__sai_port_api_t# /home/bluecmd/Downloads/SAI/inc/saiport.h: 4093

enum__sai_qos_map_type_t = c_int# /home/bluecmd/Downloads/SAI/inc/saiqosmap.h: 89

SAI_QOS_MAP_TYPE_DOT1P_TO_TC = 0x00000000# /home/bluecmd/Downloads/SAI/inc/saiqosmap.h: 89

SAI_QOS_MAP_TYPE_DOT1P_TO_COLOR = 0x00000001# /home/bluecmd/Downloads/SAI/inc/saiqosmap.h: 89

SAI_QOS_MAP_TYPE_DSCP_TO_TC = 0x00000002# /home/bluecmd/Downloads/SAI/inc/saiqosmap.h: 89

SAI_QOS_MAP_TYPE_DSCP_TO_COLOR = 0x00000003# /home/bluecmd/Downloads/SAI/inc/saiqosmap.h: 89

SAI_QOS_MAP_TYPE_TC_TO_QUEUE = 0x00000004# /home/bluecmd/Downloads/SAI/inc/saiqosmap.h: 89

SAI_QOS_MAP_TYPE_TC_AND_COLOR_TO_DSCP = 0x00000005# /home/bluecmd/Downloads/SAI/inc/saiqosmap.h: 89

SAI_QOS_MAP_TYPE_TC_AND_COLOR_TO_DOT1P = 0x00000006# /home/bluecmd/Downloads/SAI/inc/saiqosmap.h: 89

SAI_QOS_MAP_TYPE_TC_TO_PRIORITY_GROUP = 0x00000007# /home/bluecmd/Downloads/SAI/inc/saiqosmap.h: 89

SAI_QOS_MAP_TYPE_PFC_PRIORITY_TO_PRIORITY_GROUP = 0x00000008# /home/bluecmd/Downloads/SAI/inc/saiqosmap.h: 89

SAI_QOS_MAP_TYPE_PFC_PRIORITY_TO_QUEUE = 0x00000009# /home/bluecmd/Downloads/SAI/inc/saiqosmap.h: 89

SAI_QOS_MAP_TYPE_MPLS_EXP_TO_TC = 0x0000000a# /home/bluecmd/Downloads/SAI/inc/saiqosmap.h: 89

SAI_QOS_MAP_TYPE_MPLS_EXP_TO_COLOR = 0x0000000b# /home/bluecmd/Downloads/SAI/inc/saiqosmap.h: 89

SAI_QOS_MAP_TYPE_TC_AND_COLOR_TO_MPLS_EXP = 0x0000000c# /home/bluecmd/Downloads/SAI/inc/saiqosmap.h: 89

SAI_QOS_MAP_TYPE_DSCP_TO_FORWARDING_CLASS = 0x0000000d# /home/bluecmd/Downloads/SAI/inc/saiqosmap.h: 89

SAI_QOS_MAP_TYPE_MPLS_EXP_TO_FORWARDING_CLASS = 0x0000000e# /home/bluecmd/Downloads/SAI/inc/saiqosmap.h: 89

SAI_QOS_MAP_TYPE_CUSTOM_RANGE_BASE = 0x10000000# /home/bluecmd/Downloads/SAI/inc/saiqosmap.h: 89

sai_qos_map_type_t = enum__sai_qos_map_type_t# /home/bluecmd/Downloads/SAI/inc/saiqosmap.h: 89

enum__sai_qos_map_attr_t = c_int# /home/bluecmd/Downloads/SAI/inc/saiqosmap.h: 133

SAI_QOS_MAP_ATTR_START = 0# /home/bluecmd/Downloads/SAI/inc/saiqosmap.h: 133

SAI_QOS_MAP_ATTR_TYPE = SAI_QOS_MAP_ATTR_START# /home/bluecmd/Downloads/SAI/inc/saiqosmap.h: 133

SAI_QOS_MAP_ATTR_MAP_TO_VALUE_LIST = 0x00000001# /home/bluecmd/Downloads/SAI/inc/saiqosmap.h: 133

SAI_QOS_MAP_ATTR_END = (SAI_QOS_MAP_ATTR_MAP_TO_VALUE_LIST + 1)# /home/bluecmd/Downloads/SAI/inc/saiqosmap.h: 133

SAI_QOS_MAP_ATTR_CUSTOM_RANGE_START = 0x10000000# /home/bluecmd/Downloads/SAI/inc/saiqosmap.h: 133

SAI_QOS_MAP_ATTR_CUSTOM_RANGE_END = (SAI_QOS_MAP_ATTR_CUSTOM_RANGE_START + 1)# /home/bluecmd/Downloads/SAI/inc/saiqosmap.h: 133

sai_qos_map_attr_t = enum__sai_qos_map_attr_t# /home/bluecmd/Downloads/SAI/inc/saiqosmap.h: 133

sai_create_qos_map_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saiqosmap.h: 145

sai_remove_qos_map_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t)# /home/bluecmd/Downloads/SAI/inc/saiqosmap.h: 158

sai_set_qos_map_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saiqosmap.h: 169

sai_get_qos_map_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saiqosmap.h: 182

# /home/bluecmd/Downloads/SAI/inc/saiqosmap.h: 197
class struct__sai_qos_map_api_t(Structure):
    pass

struct__sai_qos_map_api_t.__slots__ = [
    'create_qos_map',
    'remove_qos_map',
    'set_qos_map_attribute',
    'get_qos_map_attribute',
]
struct__sai_qos_map_api_t._fields_ = [
    ('create_qos_map', sai_create_qos_map_fn),
    ('remove_qos_map', sai_remove_qos_map_fn),
    ('set_qos_map_attribute', sai_set_qos_map_attribute_fn),
    ('get_qos_map_attribute', sai_get_qos_map_attribute_fn),
]

sai_qos_map_api_t = struct__sai_qos_map_api_t# /home/bluecmd/Downloads/SAI/inc/saiqosmap.h: 197

enum__sai_queue_type_t = c_int# /home/bluecmd/Downloads/SAI/inc/saiqueue.h: 62

SAI_QUEUE_TYPE_ALL = 0x00000000# /home/bluecmd/Downloads/SAI/inc/saiqueue.h: 62

SAI_QUEUE_TYPE_UNICAST = 0x00000001# /home/bluecmd/Downloads/SAI/inc/saiqueue.h: 62

SAI_QUEUE_TYPE_MULTICAST = 0x00000002# /home/bluecmd/Downloads/SAI/inc/saiqueue.h: 62

SAI_QUEUE_TYPE_UNICAST_VOQ = 0x00000003# /home/bluecmd/Downloads/SAI/inc/saiqueue.h: 62

SAI_QUEUE_TYPE_MULTICAST_VOQ = 0x00000004# /home/bluecmd/Downloads/SAI/inc/saiqueue.h: 62

SAI_QUEUE_TYPE_FABRIC_TX = 0x00000005# /home/bluecmd/Downloads/SAI/inc/saiqueue.h: 62

SAI_QUEUE_TYPE_CUSTOM_RANGE_BASE = 0x10000000# /home/bluecmd/Downloads/SAI/inc/saiqueue.h: 62

sai_queue_type_t = enum__sai_queue_type_t# /home/bluecmd/Downloads/SAI/inc/saiqueue.h: 62

enum__sai_queue_pfc_continuous_deadlock_state_t = c_int# /home/bluecmd/Downloads/SAI/inc/saiqueue.h: 97

SAI_QUEUE_PFC_CONTINUOUS_DEADLOCK_STATE_NOT_PAUSED = 0x00000000# /home/bluecmd/Downloads/SAI/inc/saiqueue.h: 97

SAI_QUEUE_PFC_CONTINUOUS_DEADLOCK_STATE_PAUSED = 0x00000001# /home/bluecmd/Downloads/SAI/inc/saiqueue.h: 97

SAI_QUEUE_PFC_CONTINUOUS_DEADLOCK_STATE_PAUSED_NOT_CONTINUOUS = 0x00000002# /home/bluecmd/Downloads/SAI/inc/saiqueue.h: 97

sai_queue_pfc_continuous_deadlock_state_t = enum__sai_queue_pfc_continuous_deadlock_state_t# /home/bluecmd/Downloads/SAI/inc/saiqueue.h: 97

enum__sai_queue_attr_t = c_int# /home/bluecmd/Downloads/SAI/inc/saiqueue.h: 272

SAI_QUEUE_ATTR_START = 0x00000000# /home/bluecmd/Downloads/SAI/inc/saiqueue.h: 272

SAI_QUEUE_ATTR_TYPE = SAI_QUEUE_ATTR_START# /home/bluecmd/Downloads/SAI/inc/saiqueue.h: 272

SAI_QUEUE_ATTR_PORT = 0x00000001# /home/bluecmd/Downloads/SAI/inc/saiqueue.h: 272

SAI_QUEUE_ATTR_INDEX = 0x00000002# /home/bluecmd/Downloads/SAI/inc/saiqueue.h: 272

SAI_QUEUE_ATTR_PARENT_SCHEDULER_NODE = 0x00000003# /home/bluecmd/Downloads/SAI/inc/saiqueue.h: 272

SAI_QUEUE_ATTR_WRED_PROFILE_ID = 0x00000004# /home/bluecmd/Downloads/SAI/inc/saiqueue.h: 272

SAI_QUEUE_ATTR_BUFFER_PROFILE_ID = 0x00000005# /home/bluecmd/Downloads/SAI/inc/saiqueue.h: 272

SAI_QUEUE_ATTR_SCHEDULER_PROFILE_ID = 0x00000006# /home/bluecmd/Downloads/SAI/inc/saiqueue.h: 272

SAI_QUEUE_ATTR_PAUSE_STATUS = 0x00000007# /home/bluecmd/Downloads/SAI/inc/saiqueue.h: 272

SAI_QUEUE_ATTR_ENABLE_PFC_DLDR = 0x00000008# /home/bluecmd/Downloads/SAI/inc/saiqueue.h: 272

SAI_QUEUE_ATTR_PFC_DLR_INIT = 0x00000009# /home/bluecmd/Downloads/SAI/inc/saiqueue.h: 272

SAI_QUEUE_ATTR_TAM_OBJECT = (SAI_QUEUE_ATTR_PFC_DLR_INIT + 1)# /home/bluecmd/Downloads/SAI/inc/saiqueue.h: 272

SAI_QUEUE_ATTR_PFC_DLR_PACKET_ACTION = (SAI_QUEUE_ATTR_TAM_OBJECT + 1)# /home/bluecmd/Downloads/SAI/inc/saiqueue.h: 272

SAI_QUEUE_ATTR_PFC_CONTINUOUS_DEADLOCK_STATE = (SAI_QUEUE_ATTR_PFC_DLR_PACKET_ACTION + 1)# /home/bluecmd/Downloads/SAI/inc/saiqueue.h: 272

SAI_QUEUE_ATTR_END = (SAI_QUEUE_ATTR_PFC_CONTINUOUS_DEADLOCK_STATE + 1)# /home/bluecmd/Downloads/SAI/inc/saiqueue.h: 272

SAI_QUEUE_ATTR_CUSTOM_RANGE_START = 0x10000000# /home/bluecmd/Downloads/SAI/inc/saiqueue.h: 272

SAI_QUEUE_ATTR_CUSTOM_RANGE_END = (SAI_QUEUE_ATTR_CUSTOM_RANGE_START + 1)# /home/bluecmd/Downloads/SAI/inc/saiqueue.h: 272

sai_queue_attr_t = enum__sai_queue_attr_t# /home/bluecmd/Downloads/SAI/inc/saiqueue.h: 272

enum__sai_queue_stat_t = c_int# /home/bluecmd/Downloads/SAI/inc/saiqueue.h: 399

SAI_QUEUE_STAT_PACKETS = 0x00000000# /home/bluecmd/Downloads/SAI/inc/saiqueue.h: 399

SAI_QUEUE_STAT_BYTES = 0x00000001# /home/bluecmd/Downloads/SAI/inc/saiqueue.h: 399

SAI_QUEUE_STAT_DROPPED_PACKETS = 0x00000002# /home/bluecmd/Downloads/SAI/inc/saiqueue.h: 399

SAI_QUEUE_STAT_DROPPED_BYTES = 0x00000003# /home/bluecmd/Downloads/SAI/inc/saiqueue.h: 399

SAI_QUEUE_STAT_GREEN_PACKETS = 0x00000004# /home/bluecmd/Downloads/SAI/inc/saiqueue.h: 399

SAI_QUEUE_STAT_GREEN_BYTES = 0x00000005# /home/bluecmd/Downloads/SAI/inc/saiqueue.h: 399

SAI_QUEUE_STAT_GREEN_DROPPED_PACKETS = 0x00000006# /home/bluecmd/Downloads/SAI/inc/saiqueue.h: 399

SAI_QUEUE_STAT_GREEN_DROPPED_BYTES = 0x00000007# /home/bluecmd/Downloads/SAI/inc/saiqueue.h: 399

SAI_QUEUE_STAT_YELLOW_PACKETS = 0x00000008# /home/bluecmd/Downloads/SAI/inc/saiqueue.h: 399

SAI_QUEUE_STAT_YELLOW_BYTES = 0x00000009# /home/bluecmd/Downloads/SAI/inc/saiqueue.h: 399

SAI_QUEUE_STAT_YELLOW_DROPPED_PACKETS = 0x0000000a# /home/bluecmd/Downloads/SAI/inc/saiqueue.h: 399

SAI_QUEUE_STAT_YELLOW_DROPPED_BYTES = 0x0000000b# /home/bluecmd/Downloads/SAI/inc/saiqueue.h: 399

SAI_QUEUE_STAT_RED_PACKETS = 0x0000000c# /home/bluecmd/Downloads/SAI/inc/saiqueue.h: 399

SAI_QUEUE_STAT_RED_BYTES = 0x0000000d# /home/bluecmd/Downloads/SAI/inc/saiqueue.h: 399

SAI_QUEUE_STAT_RED_DROPPED_PACKETS = 0x0000000e# /home/bluecmd/Downloads/SAI/inc/saiqueue.h: 399

SAI_QUEUE_STAT_RED_DROPPED_BYTES = 0x0000000f# /home/bluecmd/Downloads/SAI/inc/saiqueue.h: 399

SAI_QUEUE_STAT_GREEN_WRED_DROPPED_PACKETS = 0x00000010# /home/bluecmd/Downloads/SAI/inc/saiqueue.h: 399

SAI_QUEUE_STAT_GREEN_WRED_DROPPED_BYTES = 0x00000011# /home/bluecmd/Downloads/SAI/inc/saiqueue.h: 399

SAI_QUEUE_STAT_YELLOW_WRED_DROPPED_PACKETS = 0x00000012# /home/bluecmd/Downloads/SAI/inc/saiqueue.h: 399

SAI_QUEUE_STAT_YELLOW_WRED_DROPPED_BYTES = 0x00000013# /home/bluecmd/Downloads/SAI/inc/saiqueue.h: 399

SAI_QUEUE_STAT_RED_WRED_DROPPED_PACKETS = 0x00000014# /home/bluecmd/Downloads/SAI/inc/saiqueue.h: 399

SAI_QUEUE_STAT_RED_WRED_DROPPED_BYTES = 0x00000015# /home/bluecmd/Downloads/SAI/inc/saiqueue.h: 399

SAI_QUEUE_STAT_WRED_DROPPED_PACKETS = 0x00000016# /home/bluecmd/Downloads/SAI/inc/saiqueue.h: 399

SAI_QUEUE_STAT_WRED_DROPPED_BYTES = 0x00000017# /home/bluecmd/Downloads/SAI/inc/saiqueue.h: 399

SAI_QUEUE_STAT_CURR_OCCUPANCY_BYTES = 0x00000018# /home/bluecmd/Downloads/SAI/inc/saiqueue.h: 399

SAI_QUEUE_STAT_WATERMARK_BYTES = 0x00000019# /home/bluecmd/Downloads/SAI/inc/saiqueue.h: 399

SAI_QUEUE_STAT_SHARED_CURR_OCCUPANCY_BYTES = 0x0000001a# /home/bluecmd/Downloads/SAI/inc/saiqueue.h: 399

SAI_QUEUE_STAT_SHARED_WATERMARK_BYTES = 0x0000001b# /home/bluecmd/Downloads/SAI/inc/saiqueue.h: 399

SAI_QUEUE_STAT_GREEN_WRED_ECN_MARKED_PACKETS = 0x0000001c# /home/bluecmd/Downloads/SAI/inc/saiqueue.h: 399

SAI_QUEUE_STAT_GREEN_WRED_ECN_MARKED_BYTES = 0x0000001d# /home/bluecmd/Downloads/SAI/inc/saiqueue.h: 399

SAI_QUEUE_STAT_YELLOW_WRED_ECN_MARKED_PACKETS = 0x0000001e# /home/bluecmd/Downloads/SAI/inc/saiqueue.h: 399

SAI_QUEUE_STAT_YELLOW_WRED_ECN_MARKED_BYTES = 0x0000001f# /home/bluecmd/Downloads/SAI/inc/saiqueue.h: 399

SAI_QUEUE_STAT_RED_WRED_ECN_MARKED_PACKETS = 0x00000020# /home/bluecmd/Downloads/SAI/inc/saiqueue.h: 399

SAI_QUEUE_STAT_RED_WRED_ECN_MARKED_BYTES = 0x00000021# /home/bluecmd/Downloads/SAI/inc/saiqueue.h: 399

SAI_QUEUE_STAT_WRED_ECN_MARKED_PACKETS = 0x00000022# /home/bluecmd/Downloads/SAI/inc/saiqueue.h: 399

SAI_QUEUE_STAT_WRED_ECN_MARKED_BYTES = 0x00000023# /home/bluecmd/Downloads/SAI/inc/saiqueue.h: 399

SAI_QUEUE_STAT_CURR_OCCUPANCY_LEVEL = 0x00000024# /home/bluecmd/Downloads/SAI/inc/saiqueue.h: 399

SAI_QUEUE_STAT_WATERMARK_LEVEL = 0x00000025# /home/bluecmd/Downloads/SAI/inc/saiqueue.h: 399

SAI_QUEUE_STAT_CREDIT_WD_DELETED_PACKETS = 0x00000026# /home/bluecmd/Downloads/SAI/inc/saiqueue.h: 399

SAI_QUEUE_STAT_CUSTOM_RANGE_BASE = 0x10000000# /home/bluecmd/Downloads/SAI/inc/saiqueue.h: 399

sai_queue_stat_t = enum__sai_queue_stat_t# /home/bluecmd/Downloads/SAI/inc/saiqueue.h: 399

enum__sai_queue_pfc_deadlock_event_type_t = c_int# /home/bluecmd/Downloads/SAI/inc/saiqueue.h: 412

SAI_QUEUE_PFC_DEADLOCK_EVENT_TYPE_DETECTED = 0# /home/bluecmd/Downloads/SAI/inc/saiqueue.h: 412

SAI_QUEUE_PFC_DEADLOCK_EVENT_TYPE_RECOVERED = (SAI_QUEUE_PFC_DEADLOCK_EVENT_TYPE_DETECTED + 1)# /home/bluecmd/Downloads/SAI/inc/saiqueue.h: 412

sai_queue_pfc_deadlock_event_type_t = enum__sai_queue_pfc_deadlock_event_type_t# /home/bluecmd/Downloads/SAI/inc/saiqueue.h: 412

# /home/bluecmd/Downloads/SAI/inc/saiqueue.h: 440
class struct__sai_queue_deadlock_notification_data_t(Structure):
    pass

struct__sai_queue_deadlock_notification_data_t.__slots__ = [
    'queue_id',
    'event',
    'app_managed_recovery',
]
struct__sai_queue_deadlock_notification_data_t._fields_ = [
    ('queue_id', sai_object_id_t),
    ('event', sai_queue_pfc_deadlock_event_type_t),
    ('app_managed_recovery', c_bool),
]

sai_queue_deadlock_notification_data_t = struct__sai_queue_deadlock_notification_data_t# /home/bluecmd/Downloads/SAI/inc/saiqueue.h: 440

sai_create_queue_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saiqueue.h: 452

sai_remove_queue_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t)# /home/bluecmd/Downloads/SAI/inc/saiqueue.h: 465

sai_set_queue_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saiqueue.h: 476

sai_get_queue_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saiqueue.h: 489

sai_get_queue_stats_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, uint32_t, POINTER(sai_stat_id_t), POINTER(uint64_t))# /home/bluecmd/Downloads/SAI/inc/saiqueue.h: 504

sai_get_queue_stats_ext_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, uint32_t, POINTER(sai_stat_id_t), sai_stats_mode_t, POINTER(uint64_t))# /home/bluecmd/Downloads/SAI/inc/saiqueue.h: 521

sai_clear_queue_stats_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, uint32_t, POINTER(sai_stat_id_t))# /home/bluecmd/Downloads/SAI/inc/saiqueue.h: 537

sai_queue_pfc_deadlock_notification_fn = CFUNCTYPE(UNCHECKED(None), uint32_t, POINTER(sai_queue_deadlock_notification_data_t))# /home/bluecmd/Downloads/SAI/inc/saiqueue.h: 552

# /home/bluecmd/Downloads/SAI/inc/saiqueue.h: 569
class struct__sai_queue_api_t(Structure):
    pass

struct__sai_queue_api_t.__slots__ = [
    'create_queue',
    'remove_queue',
    'set_queue_attribute',
    'get_queue_attribute',
    'get_queue_stats',
    'get_queue_stats_ext',
    'clear_queue_stats',
]
struct__sai_queue_api_t._fields_ = [
    ('create_queue', sai_create_queue_fn),
    ('remove_queue', sai_remove_queue_fn),
    ('set_queue_attribute', sai_set_queue_attribute_fn),
    ('get_queue_attribute', sai_get_queue_attribute_fn),
    ('get_queue_stats', sai_get_queue_stats_fn),
    ('get_queue_stats_ext', sai_get_queue_stats_ext_fn),
    ('clear_queue_stats', sai_clear_queue_stats_fn),
]

sai_queue_api_t = struct__sai_queue_api_t# /home/bluecmd/Downloads/SAI/inc/saiqueue.h: 569

enum__sai_router_interface_type_t = c_int# /home/bluecmd/Downloads/SAI/inc/sairouterinterface.h: 62

SAI_ROUTER_INTERFACE_TYPE_PORT = 0# /home/bluecmd/Downloads/SAI/inc/sairouterinterface.h: 62

SAI_ROUTER_INTERFACE_TYPE_VLAN = (SAI_ROUTER_INTERFACE_TYPE_PORT + 1)# /home/bluecmd/Downloads/SAI/inc/sairouterinterface.h: 62

SAI_ROUTER_INTERFACE_TYPE_LOOPBACK = (SAI_ROUTER_INTERFACE_TYPE_VLAN + 1)# /home/bluecmd/Downloads/SAI/inc/sairouterinterface.h: 62

SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER = (SAI_ROUTER_INTERFACE_TYPE_LOOPBACK + 1)# /home/bluecmd/Downloads/SAI/inc/sairouterinterface.h: 62

SAI_ROUTER_INTERFACE_TYPE_SUB_PORT = (SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER + 1)# /home/bluecmd/Downloads/SAI/inc/sairouterinterface.h: 62

SAI_ROUTER_INTERFACE_TYPE_BRIDGE = (SAI_ROUTER_INTERFACE_TYPE_SUB_PORT + 1)# /home/bluecmd/Downloads/SAI/inc/sairouterinterface.h: 62

SAI_ROUTER_INTERFACE_TYPE_QINQ_PORT = (SAI_ROUTER_INTERFACE_TYPE_BRIDGE + 1)# /home/bluecmd/Downloads/SAI/inc/sairouterinterface.h: 62

sai_router_interface_type_t = enum__sai_router_interface_type_t# /home/bluecmd/Downloads/SAI/inc/sairouterinterface.h: 62

enum__sai_router_interface_attr_t = c_int# /home/bluecmd/Downloads/SAI/inc/sairouterinterface.h: 308

SAI_ROUTER_INTERFACE_ATTR_START = 0# /home/bluecmd/Downloads/SAI/inc/sairouterinterface.h: 308

SAI_ROUTER_INTERFACE_ATTR_VIRTUAL_ROUTER_ID = SAI_ROUTER_INTERFACE_ATTR_START# /home/bluecmd/Downloads/SAI/inc/sairouterinterface.h: 308

SAI_ROUTER_INTERFACE_ATTR_TYPE = (SAI_ROUTER_INTERFACE_ATTR_VIRTUAL_ROUTER_ID + 1)# /home/bluecmd/Downloads/SAI/inc/sairouterinterface.h: 308

SAI_ROUTER_INTERFACE_ATTR_PORT_ID = (SAI_ROUTER_INTERFACE_ATTR_TYPE + 1)# /home/bluecmd/Downloads/SAI/inc/sairouterinterface.h: 308

SAI_ROUTER_INTERFACE_ATTR_VLAN_ID = (SAI_ROUTER_INTERFACE_ATTR_PORT_ID + 1)# /home/bluecmd/Downloads/SAI/inc/sairouterinterface.h: 308

SAI_ROUTER_INTERFACE_ATTR_OUTER_VLAN_ID = (SAI_ROUTER_INTERFACE_ATTR_VLAN_ID + 1)# /home/bluecmd/Downloads/SAI/inc/sairouterinterface.h: 308

SAI_ROUTER_INTERFACE_ATTR_INNER_VLAN_ID = (SAI_ROUTER_INTERFACE_ATTR_OUTER_VLAN_ID + 1)# /home/bluecmd/Downloads/SAI/inc/sairouterinterface.h: 308

SAI_ROUTER_INTERFACE_ATTR_BRIDGE_ID = (SAI_ROUTER_INTERFACE_ATTR_INNER_VLAN_ID + 1)# /home/bluecmd/Downloads/SAI/inc/sairouterinterface.h: 308

SAI_ROUTER_INTERFACE_ATTR_SRC_MAC_ADDRESS = (SAI_ROUTER_INTERFACE_ATTR_BRIDGE_ID + 1)# /home/bluecmd/Downloads/SAI/inc/sairouterinterface.h: 308

SAI_ROUTER_INTERFACE_ATTR_ADMIN_V4_STATE = (SAI_ROUTER_INTERFACE_ATTR_SRC_MAC_ADDRESS + 1)# /home/bluecmd/Downloads/SAI/inc/sairouterinterface.h: 308

SAI_ROUTER_INTERFACE_ATTR_ADMIN_V6_STATE = (SAI_ROUTER_INTERFACE_ATTR_ADMIN_V4_STATE + 1)# /home/bluecmd/Downloads/SAI/inc/sairouterinterface.h: 308

SAI_ROUTER_INTERFACE_ATTR_MTU = (SAI_ROUTER_INTERFACE_ATTR_ADMIN_V6_STATE + 1)# /home/bluecmd/Downloads/SAI/inc/sairouterinterface.h: 308

SAI_ROUTER_INTERFACE_ATTR_INGRESS_ACL = (SAI_ROUTER_INTERFACE_ATTR_MTU + 1)# /home/bluecmd/Downloads/SAI/inc/sairouterinterface.h: 308

SAI_ROUTER_INTERFACE_ATTR_EGRESS_ACL = (SAI_ROUTER_INTERFACE_ATTR_INGRESS_ACL + 1)# /home/bluecmd/Downloads/SAI/inc/sairouterinterface.h: 308

SAI_ROUTER_INTERFACE_ATTR_NEIGHBOR_MISS_PACKET_ACTION = (SAI_ROUTER_INTERFACE_ATTR_EGRESS_ACL + 1)# /home/bluecmd/Downloads/SAI/inc/sairouterinterface.h: 308

SAI_ROUTER_INTERFACE_ATTR_V4_MCAST_ENABLE = (SAI_ROUTER_INTERFACE_ATTR_NEIGHBOR_MISS_PACKET_ACTION + 1)# /home/bluecmd/Downloads/SAI/inc/sairouterinterface.h: 308

SAI_ROUTER_INTERFACE_ATTR_V6_MCAST_ENABLE = (SAI_ROUTER_INTERFACE_ATTR_V4_MCAST_ENABLE + 1)# /home/bluecmd/Downloads/SAI/inc/sairouterinterface.h: 308

SAI_ROUTER_INTERFACE_ATTR_LOOPBACK_PACKET_ACTION = (SAI_ROUTER_INTERFACE_ATTR_V6_MCAST_ENABLE + 1)# /home/bluecmd/Downloads/SAI/inc/sairouterinterface.h: 308

SAI_ROUTER_INTERFACE_ATTR_IS_VIRTUAL = (SAI_ROUTER_INTERFACE_ATTR_LOOPBACK_PACKET_ACTION + 1)# /home/bluecmd/Downloads/SAI/inc/sairouterinterface.h: 308

SAI_ROUTER_INTERFACE_ATTR_NAT_ZONE_ID = (SAI_ROUTER_INTERFACE_ATTR_IS_VIRTUAL + 1)# /home/bluecmd/Downloads/SAI/inc/sairouterinterface.h: 308

SAI_ROUTER_INTERFACE_ATTR_DISABLE_DECREMENT_TTL = (SAI_ROUTER_INTERFACE_ATTR_NAT_ZONE_ID + 1)# /home/bluecmd/Downloads/SAI/inc/sairouterinterface.h: 308

SAI_ROUTER_INTERFACE_ATTR_ADMIN_MPLS_STATE = (SAI_ROUTER_INTERFACE_ATTR_DISABLE_DECREMENT_TTL + 1)# /home/bluecmd/Downloads/SAI/inc/sairouterinterface.h: 308

SAI_ROUTER_INTERFACE_ATTR_END = (SAI_ROUTER_INTERFACE_ATTR_ADMIN_MPLS_STATE + 1)# /home/bluecmd/Downloads/SAI/inc/sairouterinterface.h: 308

SAI_ROUTER_INTERFACE_ATTR_CUSTOM_RANGE_START = 0x10000000# /home/bluecmd/Downloads/SAI/inc/sairouterinterface.h: 308

SAI_ROUTER_INTERFACE_ATTR_CUSTOM_RANGE_END = (SAI_ROUTER_INTERFACE_ATTR_CUSTOM_RANGE_START + 1)# /home/bluecmd/Downloads/SAI/inc/sairouterinterface.h: 308

sai_router_interface_attr_t = enum__sai_router_interface_attr_t# /home/bluecmd/Downloads/SAI/inc/sairouterinterface.h: 308

enum__sai_router_interface_stat_t = c_int# /home/bluecmd/Downloads/SAI/inc/sairouterinterface.h: 339

SAI_ROUTER_INTERFACE_STAT_IN_OCTETS = 0# /home/bluecmd/Downloads/SAI/inc/sairouterinterface.h: 339

SAI_ROUTER_INTERFACE_STAT_IN_PACKETS = (SAI_ROUTER_INTERFACE_STAT_IN_OCTETS + 1)# /home/bluecmd/Downloads/SAI/inc/sairouterinterface.h: 339

SAI_ROUTER_INTERFACE_STAT_OUT_OCTETS = (SAI_ROUTER_INTERFACE_STAT_IN_PACKETS + 1)# /home/bluecmd/Downloads/SAI/inc/sairouterinterface.h: 339

SAI_ROUTER_INTERFACE_STAT_OUT_PACKETS = (SAI_ROUTER_INTERFACE_STAT_OUT_OCTETS + 1)# /home/bluecmd/Downloads/SAI/inc/sairouterinterface.h: 339

SAI_ROUTER_INTERFACE_STAT_IN_ERROR_OCTETS = (SAI_ROUTER_INTERFACE_STAT_OUT_PACKETS + 1)# /home/bluecmd/Downloads/SAI/inc/sairouterinterface.h: 339

SAI_ROUTER_INTERFACE_STAT_IN_ERROR_PACKETS = (SAI_ROUTER_INTERFACE_STAT_IN_ERROR_OCTETS + 1)# /home/bluecmd/Downloads/SAI/inc/sairouterinterface.h: 339

SAI_ROUTER_INTERFACE_STAT_OUT_ERROR_OCTETS = (SAI_ROUTER_INTERFACE_STAT_IN_ERROR_PACKETS + 1)# /home/bluecmd/Downloads/SAI/inc/sairouterinterface.h: 339

SAI_ROUTER_INTERFACE_STAT_OUT_ERROR_PACKETS = (SAI_ROUTER_INTERFACE_STAT_OUT_ERROR_OCTETS + 1)# /home/bluecmd/Downloads/SAI/inc/sairouterinterface.h: 339

sai_router_interface_stat_t = enum__sai_router_interface_stat_t# /home/bluecmd/Downloads/SAI/inc/sairouterinterface.h: 339

sai_create_router_interface_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/sairouterinterface.h: 351

sai_remove_router_interface_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t)# /home/bluecmd/Downloads/SAI/inc/sairouterinterface.h: 364

sai_set_router_interface_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/sairouterinterface.h: 375

sai_get_router_interface_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/sairouterinterface.h: 388

sai_get_router_interface_stats_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, uint32_t, POINTER(sai_stat_id_t), POINTER(uint64_t))# /home/bluecmd/Downloads/SAI/inc/sairouterinterface.h: 403

sai_get_router_interface_stats_ext_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, uint32_t, POINTER(sai_stat_id_t), sai_stats_mode_t, POINTER(uint64_t))# /home/bluecmd/Downloads/SAI/inc/sairouterinterface.h: 420

sai_clear_router_interface_stats_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, uint32_t, POINTER(sai_stat_id_t))# /home/bluecmd/Downloads/SAI/inc/sairouterinterface.h: 436

# /home/bluecmd/Downloads/SAI/inc/sairouterinterface.h: 459
class struct__sai_router_interface_api_t(Structure):
    pass

struct__sai_router_interface_api_t.__slots__ = [
    'create_router_interface',
    'remove_router_interface',
    'set_router_interface_attribute',
    'get_router_interface_attribute',
    'get_router_interface_stats',
    'get_router_interface_stats_ext',
    'clear_router_interface_stats',
    'create_router_interfaces',
    'remove_router_interfaces',
    'set_router_interfaces_attribute',
    'get_router_interfaces_attribute',
]
struct__sai_router_interface_api_t._fields_ = [
    ('create_router_interface', sai_create_router_interface_fn),
    ('remove_router_interface', sai_remove_router_interface_fn),
    ('set_router_interface_attribute', sai_set_router_interface_attribute_fn),
    ('get_router_interface_attribute', sai_get_router_interface_attribute_fn),
    ('get_router_interface_stats', sai_get_router_interface_stats_fn),
    ('get_router_interface_stats_ext', sai_get_router_interface_stats_ext_fn),
    ('clear_router_interface_stats', sai_clear_router_interface_stats_fn),
    ('create_router_interfaces', sai_bulk_object_create_fn),
    ('remove_router_interfaces', sai_bulk_object_remove_fn),
    ('set_router_interfaces_attribute', sai_bulk_object_set_attribute_fn),
    ('get_router_interfaces_attribute', sai_bulk_object_get_attribute_fn),
]

sai_router_interface_api_t = struct__sai_router_interface_api_t# /home/bluecmd/Downloads/SAI/inc/sairouterinterface.h: 459

enum__sai_rpf_group_attr_t = c_int# /home/bluecmd/Downloads/SAI/inc/sairpfgroup.h: 74

SAI_RPF_GROUP_ATTR_START = 0# /home/bluecmd/Downloads/SAI/inc/sairpfgroup.h: 74

SAI_RPF_GROUP_ATTR_RPF_INTERFACE_COUNT = SAI_RPF_GROUP_ATTR_START# /home/bluecmd/Downloads/SAI/inc/sairpfgroup.h: 74

SAI_RPF_GROUP_ATTR_RPF_MEMBER_LIST = (SAI_RPF_GROUP_ATTR_RPF_INTERFACE_COUNT + 1)# /home/bluecmd/Downloads/SAI/inc/sairpfgroup.h: 74

SAI_RPF_GROUP_ATTR_END = (SAI_RPF_GROUP_ATTR_RPF_MEMBER_LIST + 1)# /home/bluecmd/Downloads/SAI/inc/sairpfgroup.h: 74

SAI_RPF_GROUP_ATTR_CUSTOM_RANGE_START = 0x10000000# /home/bluecmd/Downloads/SAI/inc/sairpfgroup.h: 74

SAI_RPF_GROUP_ATTR_CUSTOM_RANGE_END = (SAI_RPF_GROUP_ATTR_CUSTOM_RANGE_START + 1)# /home/bluecmd/Downloads/SAI/inc/sairpfgroup.h: 74

sai_rpf_group_attr_t = enum__sai_rpf_group_attr_t# /home/bluecmd/Downloads/SAI/inc/sairpfgroup.h: 74

enum__sai_rpf_group_member_attr_t = c_int# /home/bluecmd/Downloads/SAI/inc/sairpfgroup.h: 112

SAI_RPF_GROUP_MEMBER_ATTR_START = 0# /home/bluecmd/Downloads/SAI/inc/sairpfgroup.h: 112

SAI_RPF_GROUP_MEMBER_ATTR_RPF_GROUP_ID = SAI_RPF_GROUP_MEMBER_ATTR_START# /home/bluecmd/Downloads/SAI/inc/sairpfgroup.h: 112

SAI_RPF_GROUP_MEMBER_ATTR_RPF_INTERFACE_ID = (SAI_RPF_GROUP_MEMBER_ATTR_RPF_GROUP_ID + 1)# /home/bluecmd/Downloads/SAI/inc/sairpfgroup.h: 112

SAI_RPF_GROUP_MEMBER_ATTR_END = (SAI_RPF_GROUP_MEMBER_ATTR_RPF_INTERFACE_ID + 1)# /home/bluecmd/Downloads/SAI/inc/sairpfgroup.h: 112

SAI_RPF_GROUP_MEMBER_ATTR_CUSTOM_RANGE_START = 0x10000000# /home/bluecmd/Downloads/SAI/inc/sairpfgroup.h: 112

SAI_RPF_GROUP_MEMBER_ATTR_CUSTOM_RANGE_END = (SAI_RPF_GROUP_MEMBER_ATTR_CUSTOM_RANGE_START + 1)# /home/bluecmd/Downloads/SAI/inc/sairpfgroup.h: 112

sai_rpf_group_member_attr_t = enum__sai_rpf_group_member_attr_t# /home/bluecmd/Downloads/SAI/inc/sairpfgroup.h: 112

sai_create_rpf_group_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/sairpfgroup.h: 124

sai_remove_rpf_group_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t)# /home/bluecmd/Downloads/SAI/inc/sairpfgroup.h: 137

sai_set_rpf_group_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/sairpfgroup.h: 148

sai_get_rpf_group_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/sairpfgroup.h: 161

sai_create_rpf_group_member_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/sairpfgroup.h: 176

sai_remove_rpf_group_member_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t)# /home/bluecmd/Downloads/SAI/inc/sairpfgroup.h: 189

sai_set_rpf_group_member_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/sairpfgroup.h: 200

sai_get_rpf_group_member_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/sairpfgroup.h: 213

# /home/bluecmd/Downloads/SAI/inc/sairpfgroup.h: 232
class struct__sai_rpf_group_api_t(Structure):
    pass

struct__sai_rpf_group_api_t.__slots__ = [
    'create_rpf_group',
    'remove_rpf_group',
    'set_rpf_group_attribute',
    'get_rpf_group_attribute',
    'create_rpf_group_member',
    'remove_rpf_group_member',
    'set_rpf_group_member_attribute',
    'get_rpf_group_member_attribute',
]
struct__sai_rpf_group_api_t._fields_ = [
    ('create_rpf_group', sai_create_rpf_group_fn),
    ('remove_rpf_group', sai_remove_rpf_group_fn),
    ('set_rpf_group_attribute', sai_set_rpf_group_attribute_fn),
    ('get_rpf_group_attribute', sai_get_rpf_group_attribute_fn),
    ('create_rpf_group_member', sai_create_rpf_group_member_fn),
    ('remove_rpf_group_member', sai_remove_rpf_group_member_fn),
    ('set_rpf_group_member_attribute', sai_set_rpf_group_member_attribute_fn),
    ('get_rpf_group_member_attribute', sai_get_rpf_group_member_attribute_fn),
]

sai_rpf_group_api_t = struct__sai_rpf_group_api_t# /home/bluecmd/Downloads/SAI/inc/sairpfgroup.h: 232

enum__sai_samplepacket_type_t = c_int# /home/bluecmd/Downloads/SAI/inc/saisamplepacket.h: 47

SAI_SAMPLEPACKET_TYPE_SLOW_PATH = 0# /home/bluecmd/Downloads/SAI/inc/saisamplepacket.h: 47

SAI_SAMPLEPACKET_TYPE_MIRROR_SESSION = (SAI_SAMPLEPACKET_TYPE_SLOW_PATH + 1)# /home/bluecmd/Downloads/SAI/inc/saisamplepacket.h: 47

sai_samplepacket_type_t = enum__sai_samplepacket_type_t# /home/bluecmd/Downloads/SAI/inc/saisamplepacket.h: 47

enum__sai_samplepacket_mode_t = c_int# /home/bluecmd/Downloads/SAI/inc/saisamplepacket.h: 74

SAI_SAMPLEPACKET_MODE_EXCLUSIVE = 0# /home/bluecmd/Downloads/SAI/inc/saisamplepacket.h: 74

SAI_SAMPLEPACKET_MODE_SHARED = (SAI_SAMPLEPACKET_MODE_EXCLUSIVE + 1)# /home/bluecmd/Downloads/SAI/inc/saisamplepacket.h: 74

sai_samplepacket_mode_t = enum__sai_samplepacket_mode_t# /home/bluecmd/Downloads/SAI/inc/saisamplepacket.h: 74

enum__sai_samplepacket_attr_t = c_int# /home/bluecmd/Downloads/SAI/inc/saisamplepacket.h: 128

SAI_SAMPLEPACKET_ATTR_START = 0# /home/bluecmd/Downloads/SAI/inc/saisamplepacket.h: 128

SAI_SAMPLEPACKET_ATTR_SAMPLE_RATE = SAI_SAMPLEPACKET_ATTR_START# /home/bluecmd/Downloads/SAI/inc/saisamplepacket.h: 128

SAI_SAMPLEPACKET_ATTR_TYPE = (SAI_SAMPLEPACKET_ATTR_SAMPLE_RATE + 1)# /home/bluecmd/Downloads/SAI/inc/saisamplepacket.h: 128

SAI_SAMPLEPACKET_ATTR_MODE = (SAI_SAMPLEPACKET_ATTR_TYPE + 1)# /home/bluecmd/Downloads/SAI/inc/saisamplepacket.h: 128

SAI_SAMPLEPACKET_ATTR_END = (SAI_SAMPLEPACKET_ATTR_MODE + 1)# /home/bluecmd/Downloads/SAI/inc/saisamplepacket.h: 128

SAI_SAMPLEPACKET_ATTR_CUSTOM_RANGE_START = 0x10000000# /home/bluecmd/Downloads/SAI/inc/saisamplepacket.h: 128

SAI_SAMPLEPACKET_ATTR_CUSTOM_RANGE_END = (SAI_SAMPLEPACKET_ATTR_CUSTOM_RANGE_START + 1)# /home/bluecmd/Downloads/SAI/inc/saisamplepacket.h: 128

sai_samplepacket_attr_t = enum__sai_samplepacket_attr_t# /home/bluecmd/Downloads/SAI/inc/saisamplepacket.h: 128

sai_create_samplepacket_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saisamplepacket.h: 141

sai_remove_samplepacket_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t)# /home/bluecmd/Downloads/SAI/inc/saisamplepacket.h: 155

sai_set_samplepacket_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saisamplepacket.h: 167

sai_get_samplepacket_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saisamplepacket.h: 181

# /home/bluecmd/Downloads/SAI/inc/saisamplepacket.h: 196
class struct__sai_samplepacket_api_t(Structure):
    pass

struct__sai_samplepacket_api_t.__slots__ = [
    'create_samplepacket',
    'remove_samplepacket',
    'set_samplepacket_attribute',
    'get_samplepacket_attribute',
]
struct__sai_samplepacket_api_t._fields_ = [
    ('create_samplepacket', sai_create_samplepacket_fn),
    ('remove_samplepacket', sai_remove_samplepacket_fn),
    ('set_samplepacket_attribute', sai_set_samplepacket_attribute_fn),
    ('get_samplepacket_attribute', sai_get_samplepacket_attribute_fn),
]

sai_samplepacket_api_t = struct__sai_samplepacket_api_t# /home/bluecmd/Downloads/SAI/inc/saisamplepacket.h: 196

enum__sai_scheduler_group_attr_t = c_int# /home/bluecmd/Downloads/SAI/inc/saischedulergroup.h: 121

SAI_SCHEDULER_GROUP_ATTR_START = 0x00000000# /home/bluecmd/Downloads/SAI/inc/saischedulergroup.h: 121

SAI_SCHEDULER_GROUP_ATTR_CHILD_COUNT = SAI_SCHEDULER_GROUP_ATTR_START# /home/bluecmd/Downloads/SAI/inc/saischedulergroup.h: 121

SAI_SCHEDULER_GROUP_ATTR_CHILD_LIST = 0x00000001# /home/bluecmd/Downloads/SAI/inc/saischedulergroup.h: 121

SAI_SCHEDULER_GROUP_ATTR_PORT_ID = 0x00000002# /home/bluecmd/Downloads/SAI/inc/saischedulergroup.h: 121

SAI_SCHEDULER_GROUP_ATTR_LEVEL = 0x00000003# /home/bluecmd/Downloads/SAI/inc/saischedulergroup.h: 121

SAI_SCHEDULER_GROUP_ATTR_MAX_CHILDS = 0x00000004# /home/bluecmd/Downloads/SAI/inc/saischedulergroup.h: 121

SAI_SCHEDULER_GROUP_ATTR_SCHEDULER_PROFILE_ID = 0x00000005# /home/bluecmd/Downloads/SAI/inc/saischedulergroup.h: 121

SAI_SCHEDULER_GROUP_ATTR_PARENT_NODE = 0x00000006# /home/bluecmd/Downloads/SAI/inc/saischedulergroup.h: 121

SAI_SCHEDULER_GROUP_ATTR_END = (SAI_SCHEDULER_GROUP_ATTR_PARENT_NODE + 1)# /home/bluecmd/Downloads/SAI/inc/saischedulergroup.h: 121

SAI_SCHEDULER_GROUP_ATTR_CUSTOM_RANGE_START = 0x10000000# /home/bluecmd/Downloads/SAI/inc/saischedulergroup.h: 121

SAI_SCHEDULER_GROUP_ATTR_CUSTOM_RANGE_END = (SAI_SCHEDULER_GROUP_ATTR_CUSTOM_RANGE_START + 1)# /home/bluecmd/Downloads/SAI/inc/saischedulergroup.h: 121

sai_scheduler_group_attr_t = enum__sai_scheduler_group_attr_t# /home/bluecmd/Downloads/SAI/inc/saischedulergroup.h: 121

sai_create_scheduler_group_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saischedulergroup.h: 133

sai_remove_scheduler_group_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t)# /home/bluecmd/Downloads/SAI/inc/saischedulergroup.h: 146

sai_set_scheduler_group_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saischedulergroup.h: 157

sai_get_scheduler_group_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saischedulergroup.h: 170

# /home/bluecmd/Downloads/SAI/inc/saischedulergroup.h: 185
class struct__sai_scheduler_group_api_t(Structure):
    pass

struct__sai_scheduler_group_api_t.__slots__ = [
    'create_scheduler_group',
    'remove_scheduler_group',
    'set_scheduler_group_attribute',
    'get_scheduler_group_attribute',
]
struct__sai_scheduler_group_api_t._fields_ = [
    ('create_scheduler_group', sai_create_scheduler_group_fn),
    ('remove_scheduler_group', sai_remove_scheduler_group_fn),
    ('set_scheduler_group_attribute', sai_set_scheduler_group_attribute_fn),
    ('get_scheduler_group_attribute', sai_get_scheduler_group_attribute_fn),
]

sai_scheduler_group_api_t = struct__sai_scheduler_group_api_t# /home/bluecmd/Downloads/SAI/inc/saischedulergroup.h: 185

enum__sai_scheduling_type_t = c_int# /home/bluecmd/Downloads/SAI/inc/saischeduler.h: 50

SAI_SCHEDULING_TYPE_STRICT = 0x00000000# /home/bluecmd/Downloads/SAI/inc/saischeduler.h: 50

SAI_SCHEDULING_TYPE_WRR = 0x00000001# /home/bluecmd/Downloads/SAI/inc/saischeduler.h: 50

SAI_SCHEDULING_TYPE_DWRR = 0x00000002# /home/bluecmd/Downloads/SAI/inc/saischeduler.h: 50

sai_scheduling_type_t = enum__sai_scheduling_type_t# /home/bluecmd/Downloads/SAI/inc/saischeduler.h: 50

enum__sai_scheduler_attr_t = c_int# /home/bluecmd/Downloads/SAI/inc/saischeduler.h: 143

SAI_SCHEDULER_ATTR_START = 0x00000000# /home/bluecmd/Downloads/SAI/inc/saischeduler.h: 143

SAI_SCHEDULER_ATTR_SCHEDULING_TYPE = SAI_SCHEDULER_ATTR_START# /home/bluecmd/Downloads/SAI/inc/saischeduler.h: 143

SAI_SCHEDULER_ATTR_SCHEDULING_WEIGHT = 0x00000001# /home/bluecmd/Downloads/SAI/inc/saischeduler.h: 143

SAI_SCHEDULER_ATTR_METER_TYPE = 0x00000002# /home/bluecmd/Downloads/SAI/inc/saischeduler.h: 143

SAI_SCHEDULER_ATTR_MIN_BANDWIDTH_RATE = 0x00000003# /home/bluecmd/Downloads/SAI/inc/saischeduler.h: 143

SAI_SCHEDULER_ATTR_MIN_BANDWIDTH_BURST_RATE = 0x00000004# /home/bluecmd/Downloads/SAI/inc/saischeduler.h: 143

SAI_SCHEDULER_ATTR_MAX_BANDWIDTH_RATE = 0x00000005# /home/bluecmd/Downloads/SAI/inc/saischeduler.h: 143

SAI_SCHEDULER_ATTR_MAX_BANDWIDTH_BURST_RATE = 0x00000006# /home/bluecmd/Downloads/SAI/inc/saischeduler.h: 143

SAI_SCHEDULER_ATTR_END = (SAI_SCHEDULER_ATTR_MAX_BANDWIDTH_BURST_RATE + 1)# /home/bluecmd/Downloads/SAI/inc/saischeduler.h: 143

SAI_SCHEDULER_ATTR_CUSTOM_RANGE_START = 0x10000000# /home/bluecmd/Downloads/SAI/inc/saischeduler.h: 143

SAI_SCHEDULER_ATTR_CUSTOM_RANGE_END = (SAI_SCHEDULER_ATTR_CUSTOM_RANGE_START + 1)# /home/bluecmd/Downloads/SAI/inc/saischeduler.h: 143

sai_scheduler_attr_t = enum__sai_scheduler_attr_t# /home/bluecmd/Downloads/SAI/inc/saischeduler.h: 143

sai_create_scheduler_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saischeduler.h: 155

sai_remove_scheduler_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t)# /home/bluecmd/Downloads/SAI/inc/saischeduler.h: 168

sai_set_scheduler_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saischeduler.h: 179

sai_get_scheduler_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saischeduler.h: 192

# /home/bluecmd/Downloads/SAI/inc/saischeduler.h: 207
class struct__sai_scheduler_api_t(Structure):
    pass

struct__sai_scheduler_api_t.__slots__ = [
    'create_scheduler',
    'remove_scheduler',
    'set_scheduler_attribute',
    'get_scheduler_attribute',
]
struct__sai_scheduler_api_t._fields_ = [
    ('create_scheduler', sai_create_scheduler_fn),
    ('remove_scheduler', sai_remove_scheduler_fn),
    ('set_scheduler_attribute', sai_set_scheduler_attribute_fn),
    ('get_scheduler_attribute', sai_get_scheduler_attribute_fn),
]

sai_scheduler_api_t = struct__sai_scheduler_api_t# /home/bluecmd/Downloads/SAI/inc/saischeduler.h: 207

enum__sai_stp_port_state_t = c_int# /home/bluecmd/Downloads/SAI/inc/saistp.h: 50

SAI_STP_PORT_STATE_LEARNING = 0# /home/bluecmd/Downloads/SAI/inc/saistp.h: 50

SAI_STP_PORT_STATE_FORWARDING = (SAI_STP_PORT_STATE_LEARNING + 1)# /home/bluecmd/Downloads/SAI/inc/saistp.h: 50

SAI_STP_PORT_STATE_BLOCKING = (SAI_STP_PORT_STATE_FORWARDING + 1)# /home/bluecmd/Downloads/SAI/inc/saistp.h: 50

sai_stp_port_state_t = enum__sai_stp_port_state_t# /home/bluecmd/Downloads/SAI/inc/saistp.h: 50

enum__sai_stp_attr_t = c_int# /home/bluecmd/Downloads/SAI/inc/saistp.h: 101

SAI_STP_ATTR_START = 0# /home/bluecmd/Downloads/SAI/inc/saistp.h: 101

SAI_STP_ATTR_VLAN_LIST = SAI_STP_ATTR_START# /home/bluecmd/Downloads/SAI/inc/saistp.h: 101

SAI_STP_ATTR_BRIDGE_ID = (SAI_STP_ATTR_VLAN_LIST + 1)# /home/bluecmd/Downloads/SAI/inc/saistp.h: 101

SAI_STP_ATTR_PORT_LIST = (SAI_STP_ATTR_BRIDGE_ID + 1)# /home/bluecmd/Downloads/SAI/inc/saistp.h: 101

SAI_STP_ATTR_END = (SAI_STP_ATTR_PORT_LIST + 1)# /home/bluecmd/Downloads/SAI/inc/saistp.h: 101

SAI_STP_ATTR_CUSTOM_RANGE_START = 0x10000000# /home/bluecmd/Downloads/SAI/inc/saistp.h: 101

SAI_STP_ATTR_CUSTOM_RANGE_END = (SAI_STP_ATTR_CUSTOM_RANGE_START + 1)# /home/bluecmd/Downloads/SAI/inc/saistp.h: 101

sai_stp_attr_t = enum__sai_stp_attr_t# /home/bluecmd/Downloads/SAI/inc/saistp.h: 101

enum__sai_stp_port_attr_t = c_int# /home/bluecmd/Downloads/SAI/inc/saistp.h: 150

SAI_STP_PORT_ATTR_START = 0# /home/bluecmd/Downloads/SAI/inc/saistp.h: 150

SAI_STP_PORT_ATTR_STP = SAI_STP_PORT_ATTR_START# /home/bluecmd/Downloads/SAI/inc/saistp.h: 150

SAI_STP_PORT_ATTR_BRIDGE_PORT = (SAI_STP_PORT_ATTR_STP + 1)# /home/bluecmd/Downloads/SAI/inc/saistp.h: 150

SAI_STP_PORT_ATTR_STATE = (SAI_STP_PORT_ATTR_BRIDGE_PORT + 1)# /home/bluecmd/Downloads/SAI/inc/saistp.h: 150

SAI_STP_PORT_ATTR_END = (SAI_STP_PORT_ATTR_STATE + 1)# /home/bluecmd/Downloads/SAI/inc/saistp.h: 150

SAI_STP_PORT_ATTR_CUSTOM_RANGE_START = 0x10000000# /home/bluecmd/Downloads/SAI/inc/saistp.h: 150

SAI_STP_PORT_ATTR_CUSTOM_RANGE_END = (SAI_STP_PORT_ATTR_CUSTOM_RANGE_START + 1)# /home/bluecmd/Downloads/SAI/inc/saistp.h: 150

sai_stp_port_attr_t = enum__sai_stp_port_attr_t# /home/bluecmd/Downloads/SAI/inc/saistp.h: 150

sai_create_stp_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saistp.h: 163

sai_remove_stp_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t)# /home/bluecmd/Downloads/SAI/inc/saistp.h: 177

sai_set_stp_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saistp.h: 189

sai_get_stp_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saistp.h: 203

sai_create_stp_port_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saistp.h: 219

sai_remove_stp_port_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t)# /home/bluecmd/Downloads/SAI/inc/saistp.h: 233

sai_set_stp_port_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saistp.h: 245

sai_get_stp_port_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saistp.h: 259

# /home/bluecmd/Downloads/SAI/inc/saistp.h: 279
class struct__sai_stp_api_t(Structure):
    pass

struct__sai_stp_api_t.__slots__ = [
    'create_stp',
    'remove_stp',
    'set_stp_attribute',
    'get_stp_attribute',
    'create_stp_port',
    'remove_stp_port',
    'set_stp_port_attribute',
    'get_stp_port_attribute',
    'create_stp_ports',
    'remove_stp_ports',
]
struct__sai_stp_api_t._fields_ = [
    ('create_stp', sai_create_stp_fn),
    ('remove_stp', sai_remove_stp_fn),
    ('set_stp_attribute', sai_set_stp_attribute_fn),
    ('get_stp_attribute', sai_get_stp_attribute_fn),
    ('create_stp_port', sai_create_stp_port_fn),
    ('remove_stp_port', sai_remove_stp_port_fn),
    ('set_stp_port_attribute', sai_set_stp_port_attribute_fn),
    ('get_stp_port_attribute', sai_get_stp_port_attribute_fn),
    ('create_stp_ports', sai_bulk_object_create_fn),
    ('remove_stp_ports', sai_bulk_object_remove_fn),
]

sai_stp_api_t = struct__sai_stp_api_t# /home/bluecmd/Downloads/SAI/inc/saistp.h: 279

enum__sai_switch_oper_status_t = c_int# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 63

SAI_SWITCH_OPER_STATUS_UNKNOWN = 0# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 63

SAI_SWITCH_OPER_STATUS_UP = (SAI_SWITCH_OPER_STATUS_UNKNOWN + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 63

SAI_SWITCH_OPER_STATUS_DOWN = (SAI_SWITCH_OPER_STATUS_UP + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 63

SAI_SWITCH_OPER_STATUS_FAILED = (SAI_SWITCH_OPER_STATUS_DOWN + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 63

sai_switch_oper_status_t = enum__sai_switch_oper_status_t# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 63

enum__sai_packet_action_t = c_int# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 139

SAI_PACKET_ACTION_DROP = 0# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 139

SAI_PACKET_ACTION_FORWARD = (SAI_PACKET_ACTION_DROP + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 139

SAI_PACKET_ACTION_COPY = (SAI_PACKET_ACTION_FORWARD + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 139

SAI_PACKET_ACTION_COPY_CANCEL = (SAI_PACKET_ACTION_COPY + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 139

SAI_PACKET_ACTION_TRAP = (SAI_PACKET_ACTION_COPY_CANCEL + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 139

SAI_PACKET_ACTION_LOG = (SAI_PACKET_ACTION_TRAP + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 139

SAI_PACKET_ACTION_DENY = (SAI_PACKET_ACTION_LOG + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 139

SAI_PACKET_ACTION_TRANSIT = (SAI_PACKET_ACTION_DENY + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 139

SAI_PACKET_ACTION_DONOTDROP = (SAI_PACKET_ACTION_TRANSIT + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 139

sai_packet_action_t = enum__sai_packet_action_t# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 139

enum__sai_packet_vlan_t = c_int# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 169

SAI_PACKET_VLAN_UNTAG = 0# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 169

SAI_PACKET_VLAN_SINGLE_OUTER_TAG = (SAI_PACKET_VLAN_UNTAG + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 169

SAI_PACKET_VLAN_DOUBLE_TAG = (SAI_PACKET_VLAN_SINGLE_OUTER_TAG + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 169

sai_packet_vlan_t = enum__sai_packet_vlan_t# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 169

enum__sai_switch_switching_mode_t = c_int# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 182

SAI_SWITCH_SWITCHING_MODE_CUT_THROUGH = 0# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 182

SAI_SWITCH_SWITCHING_MODE_STORE_AND_FORWARD = (SAI_SWITCH_SWITCHING_MODE_CUT_THROUGH + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 182

sai_switch_switching_mode_t = enum__sai_switch_switching_mode_t# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 182

enum__sai_hash_algorithm_t = c_int# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 211

SAI_HASH_ALGORITHM_CRC = 0# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 211

SAI_HASH_ALGORITHM_XOR = 1# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 211

SAI_HASH_ALGORITHM_RANDOM = 2# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 211

SAI_HASH_ALGORITHM_CRC_32LO = 3# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 211

SAI_HASH_ALGORITHM_CRC_32HI = 4# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 211

SAI_HASH_ALGORITHM_CRC_CCITT = 5# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 211

SAI_HASH_ALGORITHM_CRC_XOR = 6# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 211

sai_hash_algorithm_t = enum__sai_hash_algorithm_t# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 211

enum__sai_switch_restart_type_t = c_int# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 227

SAI_SWITCH_RESTART_TYPE_NONE = 0# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 227

SAI_SWITCH_RESTART_TYPE_PLANNED = 1# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 227

SAI_SWITCH_RESTART_TYPE_ANY = 2# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 227

sai_switch_restart_type_t = enum__sai_switch_restart_type_t# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 227

enum__sai_switch_mcast_snooping_capability_t = c_int# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 246

SAI_SWITCH_MCAST_SNOOPING_CAPABILITY_NONE = 0# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 246

SAI_SWITCH_MCAST_SNOOPING_CAPABILITY_XG = 1# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 246

SAI_SWITCH_MCAST_SNOOPING_CAPABILITY_SG = 2# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 246

SAI_SWITCH_MCAST_SNOOPING_CAPABILITY_XG_AND_SG = 3# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 246

sai_switch_mcast_snooping_capability_t = enum__sai_switch_mcast_snooping_capability_t# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 246

enum__sai_switch_hardware_access_bus_t = c_int# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 262

SAI_SWITCH_HARDWARE_ACCESS_BUS_MDIO = 0# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 262

SAI_SWITCH_HARDWARE_ACCESS_BUS_I2C = (SAI_SWITCH_HARDWARE_ACCESS_BUS_MDIO + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 262

SAI_SWITCH_HARDWARE_ACCESS_BUS_CPLD = (SAI_SWITCH_HARDWARE_ACCESS_BUS_I2C + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 262

sai_switch_hardware_access_bus_t = enum__sai_switch_hardware_access_bus_t# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 262

enum__sai_switch_firmware_load_method_t = c_int# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 278

SAI_SWITCH_FIRMWARE_LOAD_METHOD_NONE = 0# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 278

SAI_SWITCH_FIRMWARE_LOAD_METHOD_INTERNAL = (SAI_SWITCH_FIRMWARE_LOAD_METHOD_NONE + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 278

SAI_SWITCH_FIRMWARE_LOAD_METHOD_EEPROM = (SAI_SWITCH_FIRMWARE_LOAD_METHOD_INTERNAL + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 278

sai_switch_firmware_load_method_t = enum__sai_switch_firmware_load_method_t# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 278

enum__sai_switch_firmware_load_type_t = c_int# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 294

SAI_SWITCH_FIRMWARE_LOAD_TYPE_SKIP = 0# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 294

SAI_SWITCH_FIRMWARE_LOAD_TYPE_FORCE = (SAI_SWITCH_FIRMWARE_LOAD_TYPE_SKIP + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 294

SAI_SWITCH_FIRMWARE_LOAD_TYPE_AUTO = (SAI_SWITCH_FIRMWARE_LOAD_TYPE_FORCE + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 294

sai_switch_firmware_load_type_t = enum__sai_switch_firmware_load_type_t# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 294

enum__sai_switch_type_t = c_int# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 313

SAI_SWITCH_TYPE_NPU = 0# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 313

SAI_SWITCH_TYPE_PHY = (SAI_SWITCH_TYPE_NPU + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 313

SAI_SWITCH_TYPE_VOQ = (SAI_SWITCH_TYPE_PHY + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 313

SAI_SWITCH_TYPE_FABRIC = (SAI_SWITCH_TYPE_VOQ + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 313

sai_switch_type_t = enum__sai_switch_type_t# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 313

enum__sai_switch_failover_config_mode_t = c_int# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 329

SAI_SWITCH_FAILOVER_CONFIG_MODE_NO_HITLESS = 0# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 329

SAI_SWITCH_FAILOVER_CONFIG_MODE_HITLESS = (SAI_SWITCH_FAILOVER_CONFIG_MODE_NO_HITLESS + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 329

sai_switch_failover_config_mode_t = enum__sai_switch_failover_config_mode_t# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 329

enum__sai_tunnel_type_t = c_int# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 354

SAI_TUNNEL_TYPE_IPINIP = 0# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 354

SAI_TUNNEL_TYPE_IPINIP_GRE = (SAI_TUNNEL_TYPE_IPINIP + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 354

SAI_TUNNEL_TYPE_VXLAN = (SAI_TUNNEL_TYPE_IPINIP_GRE + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 354

SAI_TUNNEL_TYPE_MPLS = (SAI_TUNNEL_TYPE_VXLAN + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 354

SAI_TUNNEL_TYPE_SRV6 = (SAI_TUNNEL_TYPE_MPLS + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 354

SAI_TUNNEL_TYPE_NVGRE = (SAI_TUNNEL_TYPE_SRV6 + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 354

SAI_TUNNEL_TYPE_IPINIP_ESP = (SAI_TUNNEL_TYPE_NVGRE + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 354

SAI_TUNNEL_TYPE_IPINIP_UDP_ESP = (SAI_TUNNEL_TYPE_IPINIP_ESP + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 354

SAI_TUNNEL_TYPE_VXLAN_UDP_ESP = (SAI_TUNNEL_TYPE_IPINIP_UDP_ESP + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 354

sai_tunnel_type_t = enum__sai_tunnel_type_t# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 354

enum__sai_tunnel_vxlan_udp_sport_mode_t = c_int# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 370

SAI_TUNNEL_VXLAN_UDP_SPORT_MODE_USER_DEFINED = 0# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 370

SAI_TUNNEL_VXLAN_UDP_SPORT_MODE_EPHEMERAL = (SAI_TUNNEL_VXLAN_UDP_SPORT_MODE_USER_DEFINED + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 370

sai_tunnel_vxlan_udp_sport_mode_t = enum__sai_tunnel_vxlan_udp_sport_mode_t# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 370

enum__sai_tunnel_encap_ecn_mode_t = c_int# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 388

SAI_TUNNEL_ENCAP_ECN_MODE_STANDARD = 0# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 388

SAI_TUNNEL_ENCAP_ECN_MODE_USER_DEFINED = (SAI_TUNNEL_ENCAP_ECN_MODE_STANDARD + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 388

sai_tunnel_encap_ecn_mode_t = enum__sai_tunnel_encap_ecn_mode_t# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 388

enum__sai_tunnel_decap_ecn_mode_t = c_int# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 410

SAI_TUNNEL_DECAP_ECN_MODE_STANDARD = 0# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 410

SAI_TUNNEL_DECAP_ECN_MODE_COPY_FROM_OUTER = (SAI_TUNNEL_DECAP_ECN_MODE_STANDARD + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 410

SAI_TUNNEL_DECAP_ECN_MODE_USER_DEFINED = (SAI_TUNNEL_DECAP_ECN_MODE_COPY_FROM_OUTER + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 410

sai_tunnel_decap_ecn_mode_t = enum__sai_tunnel_decap_ecn_mode_t# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 410

enum__sai_switch_tunnel_attr_t = c_int# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 581

SAI_SWITCH_TUNNEL_ATTR_START = 0# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 581

SAI_SWITCH_TUNNEL_ATTR_TUNNEL_TYPE = SAI_SWITCH_TUNNEL_ATTR_START# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 581

SAI_SWITCH_TUNNEL_ATTR_LOOPBACK_PACKET_ACTION = (SAI_SWITCH_TUNNEL_ATTR_TUNNEL_TYPE + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 581

SAI_SWITCH_TUNNEL_ATTR_TUNNEL_ENCAP_ECN_MODE = (SAI_SWITCH_TUNNEL_ATTR_LOOPBACK_PACKET_ACTION + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 581

SAI_SWITCH_TUNNEL_ATTR_ENCAP_MAPPERS = (SAI_SWITCH_TUNNEL_ATTR_TUNNEL_ENCAP_ECN_MODE + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 581

SAI_SWITCH_TUNNEL_ATTR_TUNNEL_DECAP_ECN_MODE = (SAI_SWITCH_TUNNEL_ATTR_ENCAP_MAPPERS + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 581

SAI_SWITCH_TUNNEL_ATTR_DECAP_MAPPERS = (SAI_SWITCH_TUNNEL_ATTR_TUNNEL_DECAP_ECN_MODE + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 581

SAI_SWITCH_TUNNEL_ATTR_TUNNEL_VXLAN_UDP_SPORT_MODE = (SAI_SWITCH_TUNNEL_ATTR_DECAP_MAPPERS + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 581

SAI_SWITCH_TUNNEL_ATTR_VXLAN_UDP_SPORT = (SAI_SWITCH_TUNNEL_ATTR_TUNNEL_VXLAN_UDP_SPORT_MODE + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 581

SAI_SWITCH_TUNNEL_ATTR_VXLAN_UDP_SPORT_MASK = (SAI_SWITCH_TUNNEL_ATTR_VXLAN_UDP_SPORT + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 581

SAI_SWITCH_TUNNEL_ATTR_ENCAP_QOS_TC_AND_COLOR_TO_DSCP_MAP = (SAI_SWITCH_TUNNEL_ATTR_VXLAN_UDP_SPORT_MASK + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 581

SAI_SWITCH_TUNNEL_ATTR_ENCAP_QOS_TC_TO_QUEUE_MAP = (SAI_SWITCH_TUNNEL_ATTR_ENCAP_QOS_TC_AND_COLOR_TO_DSCP_MAP + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 581

SAI_SWITCH_TUNNEL_ATTR_DECAP_QOS_DSCP_TO_TC_MAP = (SAI_SWITCH_TUNNEL_ATTR_ENCAP_QOS_TC_TO_QUEUE_MAP + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 581

SAI_SWITCH_TUNNEL_ATTR_DECAP_QOS_TC_TO_PRIORITY_GROUP_MAP = (SAI_SWITCH_TUNNEL_ATTR_DECAP_QOS_DSCP_TO_TC_MAP + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 581

SAI_SWITCH_TUNNEL_ATTR_END = (SAI_SWITCH_TUNNEL_ATTR_DECAP_QOS_TC_TO_PRIORITY_GROUP_MAP + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 581

SAI_SWITCH_TUNNEL_ATTR_CUSTOM_RANGE_START = 0x10000000# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 581

SAI_SWITCH_TUNNEL_ATTR_CUSTOM_RANGE_END = (SAI_SWITCH_TUNNEL_ATTR_CUSTOM_RANGE_START + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 581

sai_switch_tunnel_attr_t = enum__sai_switch_tunnel_attr_t# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 581

enum__sai_switch_hostif_oper_status_update_mode_t = c_int# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 608

SAI_SWITCH_HOSTIF_OPER_STATUS_UPDATE_MODE_APPLICATION = 0# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 608

SAI_SWITCH_HOSTIF_OPER_STATUS_UPDATE_MODE_SAI_ADAPTER = 1# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 608

sai_switch_hostif_oper_status_update_mode_t = enum__sai_switch_hostif_oper_status_update_mode_t# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 608

enum__sai_switch_attr_t = c_int# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_START = 0# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_NUMBER_OF_ACTIVE_PORTS = SAI_SWITCH_ATTR_START# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_PORT_NUMBER = SAI_SWITCH_ATTR_NUMBER_OF_ACTIVE_PORTS# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_MAX_NUMBER_OF_SUPPORTED_PORTS = (SAI_SWITCH_ATTR_PORT_NUMBER + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_PORT_LIST = (SAI_SWITCH_ATTR_MAX_NUMBER_OF_SUPPORTED_PORTS + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_PORT_MAX_MTU = (SAI_SWITCH_ATTR_PORT_LIST + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_CPU_PORT = (SAI_SWITCH_ATTR_PORT_MAX_MTU + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_MAX_VIRTUAL_ROUTERS = (SAI_SWITCH_ATTR_CPU_PORT + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_FDB_TABLE_SIZE = (SAI_SWITCH_ATTR_MAX_VIRTUAL_ROUTERS + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_L3_NEIGHBOR_TABLE_SIZE = (SAI_SWITCH_ATTR_FDB_TABLE_SIZE + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_L3_ROUTE_TABLE_SIZE = (SAI_SWITCH_ATTR_L3_NEIGHBOR_TABLE_SIZE + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_LAG_MEMBERS = (SAI_SWITCH_ATTR_L3_ROUTE_TABLE_SIZE + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_NUMBER_OF_LAGS = (SAI_SWITCH_ATTR_LAG_MEMBERS + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_ECMP_MEMBERS = (SAI_SWITCH_ATTR_NUMBER_OF_LAGS + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_NUMBER_OF_ECMP_GROUPS = (SAI_SWITCH_ATTR_ECMP_MEMBERS + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_NUMBER_OF_UNICAST_QUEUES = (SAI_SWITCH_ATTR_NUMBER_OF_ECMP_GROUPS + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_NUMBER_OF_MULTICAST_QUEUES = (SAI_SWITCH_ATTR_NUMBER_OF_UNICAST_QUEUES + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_NUMBER_OF_QUEUES = (SAI_SWITCH_ATTR_NUMBER_OF_MULTICAST_QUEUES + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_NUMBER_OF_CPU_QUEUES = (SAI_SWITCH_ATTR_NUMBER_OF_QUEUES + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_ON_LINK_ROUTE_SUPPORTED = (SAI_SWITCH_ATTR_NUMBER_OF_CPU_QUEUES + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_OPER_STATUS = (SAI_SWITCH_ATTR_ON_LINK_ROUTE_SUPPORTED + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_MAX_NUMBER_OF_TEMP_SENSORS = (SAI_SWITCH_ATTR_OPER_STATUS + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_TEMP_LIST = (SAI_SWITCH_ATTR_MAX_NUMBER_OF_TEMP_SENSORS + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_MAX_TEMP = (SAI_SWITCH_ATTR_TEMP_LIST + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_AVERAGE_TEMP = (SAI_SWITCH_ATTR_MAX_TEMP + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_ACL_TABLE_MINIMUM_PRIORITY = (SAI_SWITCH_ATTR_AVERAGE_TEMP + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_ACL_TABLE_MAXIMUM_PRIORITY = (SAI_SWITCH_ATTR_ACL_TABLE_MINIMUM_PRIORITY + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_ACL_ENTRY_MINIMUM_PRIORITY = (SAI_SWITCH_ATTR_ACL_TABLE_MAXIMUM_PRIORITY + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_ACL_ENTRY_MAXIMUM_PRIORITY = (SAI_SWITCH_ATTR_ACL_ENTRY_MINIMUM_PRIORITY + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_ACL_TABLE_GROUP_MINIMUM_PRIORITY = (SAI_SWITCH_ATTR_ACL_ENTRY_MAXIMUM_PRIORITY + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_ACL_TABLE_GROUP_MAXIMUM_PRIORITY = (SAI_SWITCH_ATTR_ACL_TABLE_GROUP_MINIMUM_PRIORITY + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_FDB_DST_USER_META_DATA_RANGE = (SAI_SWITCH_ATTR_ACL_TABLE_GROUP_MAXIMUM_PRIORITY + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_ROUTE_DST_USER_META_DATA_RANGE = (SAI_SWITCH_ATTR_FDB_DST_USER_META_DATA_RANGE + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_NEIGHBOR_DST_USER_META_DATA_RANGE = (SAI_SWITCH_ATTR_ROUTE_DST_USER_META_DATA_RANGE + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_PORT_USER_META_DATA_RANGE = (SAI_SWITCH_ATTR_NEIGHBOR_DST_USER_META_DATA_RANGE + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_VLAN_USER_META_DATA_RANGE = (SAI_SWITCH_ATTR_PORT_USER_META_DATA_RANGE + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_ACL_USER_META_DATA_RANGE = (SAI_SWITCH_ATTR_VLAN_USER_META_DATA_RANGE + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_ACL_USER_TRAP_ID_RANGE = (SAI_SWITCH_ATTR_ACL_USER_META_DATA_RANGE + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_DEFAULT_VLAN_ID = (SAI_SWITCH_ATTR_ACL_USER_TRAP_ID_RANGE + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_DEFAULT_STP_INST_ID = (SAI_SWITCH_ATTR_DEFAULT_VLAN_ID + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_MAX_STP_INSTANCE = (SAI_SWITCH_ATTR_DEFAULT_STP_INST_ID + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_DEFAULT_VIRTUAL_ROUTER_ID = (SAI_SWITCH_ATTR_MAX_STP_INSTANCE + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_DEFAULT_OVERRIDE_VIRTUAL_ROUTER_ID = (SAI_SWITCH_ATTR_DEFAULT_VIRTUAL_ROUTER_ID + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_DEFAULT_1Q_BRIDGE_ID = (SAI_SWITCH_ATTR_DEFAULT_OVERRIDE_VIRTUAL_ROUTER_ID + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_INGRESS_ACL = (SAI_SWITCH_ATTR_DEFAULT_1Q_BRIDGE_ID + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_EGRESS_ACL = (SAI_SWITCH_ATTR_INGRESS_ACL + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_QOS_MAX_NUMBER_OF_TRAFFIC_CLASSES = (SAI_SWITCH_ATTR_EGRESS_ACL + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_QOS_MAX_NUMBER_OF_SCHEDULER_GROUP_HIERARCHY_LEVELS = (SAI_SWITCH_ATTR_QOS_MAX_NUMBER_OF_TRAFFIC_CLASSES + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_QOS_MAX_NUMBER_OF_SCHEDULER_GROUPS_PER_HIERARCHY_LEVEL = (SAI_SWITCH_ATTR_QOS_MAX_NUMBER_OF_SCHEDULER_GROUP_HIERARCHY_LEVELS + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_QOS_MAX_NUMBER_OF_CHILDS_PER_SCHEDULER_GROUP = (SAI_SWITCH_ATTR_QOS_MAX_NUMBER_OF_SCHEDULER_GROUPS_PER_HIERARCHY_LEVEL + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_TOTAL_BUFFER_SIZE = (SAI_SWITCH_ATTR_QOS_MAX_NUMBER_OF_CHILDS_PER_SCHEDULER_GROUP + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_INGRESS_BUFFER_POOL_NUM = (SAI_SWITCH_ATTR_TOTAL_BUFFER_SIZE + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_EGRESS_BUFFER_POOL_NUM = (SAI_SWITCH_ATTR_INGRESS_BUFFER_POOL_NUM + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_AVAILABLE_IPV4_ROUTE_ENTRY = (SAI_SWITCH_ATTR_EGRESS_BUFFER_POOL_NUM + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_AVAILABLE_IPV6_ROUTE_ENTRY = (SAI_SWITCH_ATTR_AVAILABLE_IPV4_ROUTE_ENTRY + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_AVAILABLE_IPV4_NEXTHOP_ENTRY = (SAI_SWITCH_ATTR_AVAILABLE_IPV6_ROUTE_ENTRY + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_AVAILABLE_IPV6_NEXTHOP_ENTRY = (SAI_SWITCH_ATTR_AVAILABLE_IPV4_NEXTHOP_ENTRY + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_AVAILABLE_IPV4_NEIGHBOR_ENTRY = (SAI_SWITCH_ATTR_AVAILABLE_IPV6_NEXTHOP_ENTRY + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_AVAILABLE_IPV6_NEIGHBOR_ENTRY = (SAI_SWITCH_ATTR_AVAILABLE_IPV4_NEIGHBOR_ENTRY + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_AVAILABLE_NEXT_HOP_GROUP_ENTRY = (SAI_SWITCH_ATTR_AVAILABLE_IPV6_NEIGHBOR_ENTRY + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_AVAILABLE_NEXT_HOP_GROUP_MEMBER_ENTRY = (SAI_SWITCH_ATTR_AVAILABLE_NEXT_HOP_GROUP_ENTRY + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_AVAILABLE_FDB_ENTRY = (SAI_SWITCH_ATTR_AVAILABLE_NEXT_HOP_GROUP_MEMBER_ENTRY + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_AVAILABLE_L2MC_ENTRY = (SAI_SWITCH_ATTR_AVAILABLE_FDB_ENTRY + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_AVAILABLE_IPMC_ENTRY = (SAI_SWITCH_ATTR_AVAILABLE_L2MC_ENTRY + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_AVAILABLE_SNAT_ENTRY = (SAI_SWITCH_ATTR_AVAILABLE_IPMC_ENTRY + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_AVAILABLE_DNAT_ENTRY = (SAI_SWITCH_ATTR_AVAILABLE_SNAT_ENTRY + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_AVAILABLE_DOUBLE_NAT_ENTRY = (SAI_SWITCH_ATTR_AVAILABLE_DNAT_ENTRY + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_AVAILABLE_ACL_TABLE = (SAI_SWITCH_ATTR_AVAILABLE_DOUBLE_NAT_ENTRY + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_AVAILABLE_ACL_TABLE_GROUP = (SAI_SWITCH_ATTR_AVAILABLE_ACL_TABLE + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_AVAILABLE_MY_SID_ENTRY = (SAI_SWITCH_ATTR_AVAILABLE_ACL_TABLE_GROUP + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_DEFAULT_TRAP_GROUP = (SAI_SWITCH_ATTR_AVAILABLE_MY_SID_ENTRY + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_ECMP_HASH = (SAI_SWITCH_ATTR_DEFAULT_TRAP_GROUP + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_LAG_HASH = (SAI_SWITCH_ATTR_ECMP_HASH + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_RESTART_WARM = (SAI_SWITCH_ATTR_LAG_HASH + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_WARM_RECOVER = (SAI_SWITCH_ATTR_RESTART_WARM + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_RESTART_TYPE = (SAI_SWITCH_ATTR_WARM_RECOVER + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_MIN_PLANNED_RESTART_INTERVAL = (SAI_SWITCH_ATTR_RESTART_TYPE + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_NV_STORAGE_SIZE = (SAI_SWITCH_ATTR_MIN_PLANNED_RESTART_INTERVAL + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_MAX_ACL_ACTION_COUNT = (SAI_SWITCH_ATTR_NV_STORAGE_SIZE + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_MAX_ACL_RANGE_COUNT = (SAI_SWITCH_ATTR_MAX_ACL_ACTION_COUNT + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_ACL_CAPABILITY = (SAI_SWITCH_ATTR_MAX_ACL_RANGE_COUNT + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_MCAST_SNOOPING_CAPABILITY = (SAI_SWITCH_ATTR_ACL_CAPABILITY + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_SWITCHING_MODE = (SAI_SWITCH_ATTR_MCAST_SNOOPING_CAPABILITY + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_BCAST_CPU_FLOOD_ENABLE = (SAI_SWITCH_ATTR_SWITCHING_MODE + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_MCAST_CPU_FLOOD_ENABLE = (SAI_SWITCH_ATTR_BCAST_CPU_FLOOD_ENABLE + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_SRC_MAC_ADDRESS = (SAI_SWITCH_ATTR_MCAST_CPU_FLOOD_ENABLE + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_MAX_LEARNED_ADDRESSES = (SAI_SWITCH_ATTR_SRC_MAC_ADDRESS + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_FDB_AGING_TIME = (SAI_SWITCH_ATTR_MAX_LEARNED_ADDRESSES + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_FDB_UNICAST_MISS_PACKET_ACTION = (SAI_SWITCH_ATTR_FDB_AGING_TIME + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_FDB_BROADCAST_MISS_PACKET_ACTION = (SAI_SWITCH_ATTR_FDB_UNICAST_MISS_PACKET_ACTION + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_FDB_MULTICAST_MISS_PACKET_ACTION = (SAI_SWITCH_ATTR_FDB_BROADCAST_MISS_PACKET_ACTION + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_ECMP_DEFAULT_HASH_ALGORITHM = (SAI_SWITCH_ATTR_FDB_MULTICAST_MISS_PACKET_ACTION + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_ECMP_DEFAULT_HASH_SEED = (SAI_SWITCH_ATTR_ECMP_DEFAULT_HASH_ALGORITHM + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_ECMP_DEFAULT_HASH_OFFSET = (SAI_SWITCH_ATTR_ECMP_DEFAULT_HASH_SEED + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_ECMP_DEFAULT_SYMMETRIC_HASH = (SAI_SWITCH_ATTR_ECMP_DEFAULT_HASH_OFFSET + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_ECMP_HASH_IPV4 = (SAI_SWITCH_ATTR_ECMP_DEFAULT_SYMMETRIC_HASH + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_ECMP_HASH_IPV4_IN_IPV4 = (SAI_SWITCH_ATTR_ECMP_HASH_IPV4 + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_ECMP_HASH_IPV6 = (SAI_SWITCH_ATTR_ECMP_HASH_IPV4_IN_IPV4 + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_LAG_DEFAULT_HASH_ALGORITHM = (SAI_SWITCH_ATTR_ECMP_HASH_IPV6 + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_LAG_DEFAULT_HASH_SEED = (SAI_SWITCH_ATTR_LAG_DEFAULT_HASH_ALGORITHM + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_LAG_DEFAULT_HASH_OFFSET = (SAI_SWITCH_ATTR_LAG_DEFAULT_HASH_SEED + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_LAG_DEFAULT_SYMMETRIC_HASH = (SAI_SWITCH_ATTR_LAG_DEFAULT_HASH_OFFSET + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_LAG_HASH_IPV4 = (SAI_SWITCH_ATTR_LAG_DEFAULT_SYMMETRIC_HASH + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_LAG_HASH_IPV4_IN_IPV4 = (SAI_SWITCH_ATTR_LAG_HASH_IPV4 + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_LAG_HASH_IPV6 = (SAI_SWITCH_ATTR_LAG_HASH_IPV4_IN_IPV4 + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_COUNTER_REFRESH_INTERVAL = (SAI_SWITCH_ATTR_LAG_HASH_IPV6 + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_QOS_DEFAULT_TC = (SAI_SWITCH_ATTR_COUNTER_REFRESH_INTERVAL + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_QOS_DOT1P_TO_TC_MAP = (SAI_SWITCH_ATTR_QOS_DEFAULT_TC + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_QOS_DOT1P_TO_COLOR_MAP = (SAI_SWITCH_ATTR_QOS_DOT1P_TO_TC_MAP + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_QOS_DSCP_TO_TC_MAP = (SAI_SWITCH_ATTR_QOS_DOT1P_TO_COLOR_MAP + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_QOS_DSCP_TO_COLOR_MAP = (SAI_SWITCH_ATTR_QOS_DSCP_TO_TC_MAP + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_QOS_TC_TO_QUEUE_MAP = (SAI_SWITCH_ATTR_QOS_DSCP_TO_COLOR_MAP + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_QOS_TC_AND_COLOR_TO_DOT1P_MAP = (SAI_SWITCH_ATTR_QOS_TC_TO_QUEUE_MAP + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP = (SAI_SWITCH_ATTR_QOS_TC_AND_COLOR_TO_DOT1P_MAP + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_SWITCH_SHELL_ENABLE = (SAI_SWITCH_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_SWITCH_PROFILE_ID = (SAI_SWITCH_ATTR_SWITCH_SHELL_ENABLE + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_SWITCH_HARDWARE_INFO = (SAI_SWITCH_ATTR_SWITCH_PROFILE_ID + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_FIRMWARE_PATH_NAME = (SAI_SWITCH_ATTR_SWITCH_HARDWARE_INFO + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_INIT_SWITCH = (SAI_SWITCH_ATTR_FIRMWARE_PATH_NAME + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_SWITCH_STATE_CHANGE_NOTIFY = (SAI_SWITCH_ATTR_INIT_SWITCH + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_SWITCH_SHUTDOWN_REQUEST_NOTIFY = (SAI_SWITCH_ATTR_SWITCH_STATE_CHANGE_NOTIFY + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_SHUTDOWN_REQUEST_NOTIFY = SAI_SWITCH_ATTR_SWITCH_SHUTDOWN_REQUEST_NOTIFY# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_FDB_EVENT_NOTIFY = (SAI_SWITCH_ATTR_SHUTDOWN_REQUEST_NOTIFY + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_PORT_STATE_CHANGE_NOTIFY = (SAI_SWITCH_ATTR_FDB_EVENT_NOTIFY + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_PACKET_EVENT_NOTIFY = (SAI_SWITCH_ATTR_PORT_STATE_CHANGE_NOTIFY + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_FAST_API_ENABLE = (SAI_SWITCH_ATTR_PACKET_EVENT_NOTIFY + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_MIRROR_TC = (SAI_SWITCH_ATTR_FAST_API_ENABLE + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_ACL_STAGE_INGRESS = (SAI_SWITCH_ATTR_MIRROR_TC + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_ACL_STAGE_EGRESS = (SAI_SWITCH_ATTR_ACL_STAGE_INGRESS + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_SRV6_MAX_SID_DEPTH = (SAI_SWITCH_ATTR_ACL_STAGE_EGRESS + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_SRV6_TLV_TYPE = (SAI_SWITCH_ATTR_SRV6_MAX_SID_DEPTH + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_QOS_NUM_LOSSLESS_QUEUES = (SAI_SWITCH_ATTR_SRV6_TLV_TYPE + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_QUEUE_PFC_DEADLOCK_NOTIFY = (SAI_SWITCH_ATTR_QOS_NUM_LOSSLESS_QUEUES + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_PFC_DLR_PACKET_ACTION = (SAI_SWITCH_ATTR_QUEUE_PFC_DEADLOCK_NOTIFY + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_PFC_TC_DLD_INTERVAL_RANGE = (SAI_SWITCH_ATTR_PFC_DLR_PACKET_ACTION + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_PFC_TC_DLD_INTERVAL = (SAI_SWITCH_ATTR_PFC_TC_DLD_INTERVAL_RANGE + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_PFC_TC_DLR_INTERVAL_RANGE = (SAI_SWITCH_ATTR_PFC_TC_DLD_INTERVAL + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_PFC_TC_DLR_INTERVAL = (SAI_SWITCH_ATTR_PFC_TC_DLR_INTERVAL_RANGE + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_SUPPORTED_PROTECTED_OBJECT_TYPE = (SAI_SWITCH_ATTR_PFC_TC_DLR_INTERVAL + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_TPID_OUTER_VLAN = (SAI_SWITCH_ATTR_SUPPORTED_PROTECTED_OBJECT_TYPE + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_TPID_INNER_VLAN = (SAI_SWITCH_ATTR_TPID_OUTER_VLAN + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_CRC_CHECK_ENABLE = (SAI_SWITCH_ATTR_TPID_INNER_VLAN + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_CRC_RECALCULATION_ENABLE = (SAI_SWITCH_ATTR_CRC_CHECK_ENABLE + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_BFD_SESSION_STATE_CHANGE_NOTIFY = (SAI_SWITCH_ATTR_CRC_RECALCULATION_ENABLE + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_NUMBER_OF_BFD_SESSION = (SAI_SWITCH_ATTR_BFD_SESSION_STATE_CHANGE_NOTIFY + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_MAX_BFD_SESSION = (SAI_SWITCH_ATTR_NUMBER_OF_BFD_SESSION + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_SUPPORTED_IPV4_BFD_SESSION_OFFLOAD_TYPE = (SAI_SWITCH_ATTR_MAX_BFD_SESSION + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_SUPPORTED_IPV6_BFD_SESSION_OFFLOAD_TYPE = (SAI_SWITCH_ATTR_SUPPORTED_IPV4_BFD_SESSION_OFFLOAD_TYPE + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_MIN_BFD_RX = (SAI_SWITCH_ATTR_SUPPORTED_IPV6_BFD_SESSION_OFFLOAD_TYPE + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_MIN_BFD_TX = (SAI_SWITCH_ATTR_MIN_BFD_RX + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_ECN_ECT_THRESHOLD_ENABLE = (SAI_SWITCH_ATTR_MIN_BFD_TX + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_VXLAN_DEFAULT_ROUTER_MAC = (SAI_SWITCH_ATTR_ECN_ECT_THRESHOLD_ENABLE + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_VXLAN_DEFAULT_PORT = (SAI_SWITCH_ATTR_VXLAN_DEFAULT_ROUTER_MAC + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_MAX_MIRROR_SESSION = (SAI_SWITCH_ATTR_VXLAN_DEFAULT_PORT + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_MAX_SAMPLED_MIRROR_SESSION = (SAI_SWITCH_ATTR_MAX_MIRROR_SESSION + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_SUPPORTED_EXTENDED_STATS_MODE = (SAI_SWITCH_ATTR_MAX_SAMPLED_MIRROR_SESSION + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_UNINIT_DATA_PLANE_ON_REMOVAL = (SAI_SWITCH_ATTR_SUPPORTED_EXTENDED_STATS_MODE + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_TAM_OBJECT_ID = (SAI_SWITCH_ATTR_UNINIT_DATA_PLANE_ON_REMOVAL + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_TAM_EVENT_NOTIFY = (SAI_SWITCH_ATTR_TAM_OBJECT_ID + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_SUPPORTED_OBJECT_TYPE_LIST = (SAI_SWITCH_ATTR_TAM_EVENT_NOTIFY + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_PRE_SHUTDOWN = (SAI_SWITCH_ATTR_SUPPORTED_OBJECT_TYPE_LIST + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_NAT_ZONE_COUNTER_OBJECT_ID = (SAI_SWITCH_ATTR_PRE_SHUTDOWN + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_NAT_ENABLE = (SAI_SWITCH_ATTR_NAT_ZONE_COUNTER_OBJECT_ID + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_HARDWARE_ACCESS_BUS = (SAI_SWITCH_ATTR_NAT_ENABLE + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_PLATFROM_CONTEXT = (SAI_SWITCH_ATTR_HARDWARE_ACCESS_BUS + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_REGISTER_READ = (SAI_SWITCH_ATTR_PLATFROM_CONTEXT + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_REGISTER_WRITE = (SAI_SWITCH_ATTR_REGISTER_READ + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_FIRMWARE_DOWNLOAD_BROADCAST = (SAI_SWITCH_ATTR_REGISTER_WRITE + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_FIRMWARE_LOAD_METHOD = (SAI_SWITCH_ATTR_FIRMWARE_DOWNLOAD_BROADCAST + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_FIRMWARE_LOAD_TYPE = (SAI_SWITCH_ATTR_FIRMWARE_LOAD_METHOD + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_FIRMWARE_DOWNLOAD_EXECUTE = (SAI_SWITCH_ATTR_FIRMWARE_LOAD_TYPE + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_FIRMWARE_BROADCAST_STOP = (SAI_SWITCH_ATTR_FIRMWARE_DOWNLOAD_EXECUTE + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_FIRMWARE_VERIFY_AND_INIT_SWITCH = (SAI_SWITCH_ATTR_FIRMWARE_BROADCAST_STOP + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_FIRMWARE_STATUS = (SAI_SWITCH_ATTR_FIRMWARE_VERIFY_AND_INIT_SWITCH + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_FIRMWARE_MAJOR_VERSION = (SAI_SWITCH_ATTR_FIRMWARE_STATUS + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_FIRMWARE_MINOR_VERSION = (SAI_SWITCH_ATTR_FIRMWARE_MAJOR_VERSION + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_PORT_CONNECTOR_LIST = (SAI_SWITCH_ATTR_FIRMWARE_MINOR_VERSION + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_PROPOGATE_PORT_STATE_FROM_LINE_TO_SYSTEM_PORT_SUPPORT = (SAI_SWITCH_ATTR_PORT_CONNECTOR_LIST + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_TYPE = (SAI_SWITCH_ATTR_PROPOGATE_PORT_STATE_FROM_LINE_TO_SYSTEM_PORT_SUPPORT + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_MACSEC_OBJECT_LIST = (SAI_SWITCH_ATTR_TYPE + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_QOS_MPLS_EXP_TO_TC_MAP = (SAI_SWITCH_ATTR_MACSEC_OBJECT_LIST + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_QOS_MPLS_EXP_TO_COLOR_MAP = (SAI_SWITCH_ATTR_QOS_MPLS_EXP_TO_TC_MAP + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_QOS_TC_AND_COLOR_TO_MPLS_EXP_MAP = (SAI_SWITCH_ATTR_QOS_MPLS_EXP_TO_COLOR_MAP + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_SWITCH_ID = (SAI_SWITCH_ATTR_QOS_TC_AND_COLOR_TO_MPLS_EXP_MAP + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_MAX_SYSTEM_CORES = (SAI_SWITCH_ATTR_SWITCH_ID + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_SYSTEM_PORT_CONFIG_LIST = (SAI_SWITCH_ATTR_MAX_SYSTEM_CORES + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_NUMBER_OF_SYSTEM_PORTS = (SAI_SWITCH_ATTR_SYSTEM_PORT_CONFIG_LIST + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_SYSTEM_PORT_LIST = (SAI_SWITCH_ATTR_NUMBER_OF_SYSTEM_PORTS + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_NUMBER_OF_FABRIC_PORTS = (SAI_SWITCH_ATTR_SYSTEM_PORT_LIST + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_FABRIC_PORT_LIST = (SAI_SWITCH_ATTR_NUMBER_OF_FABRIC_PORTS + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_PACKET_DMA_MEMORY_POOL_SIZE = (SAI_SWITCH_ATTR_FABRIC_PORT_LIST + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_FAILOVER_CONFIG_MODE = (SAI_SWITCH_ATTR_PACKET_DMA_MEMORY_POOL_SIZE + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_SUPPORTED_FAILOVER_MODE = (SAI_SWITCH_ATTR_FAILOVER_CONFIG_MODE + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_TUNNEL_OBJECTS_LIST = (SAI_SWITCH_ATTR_SUPPORTED_FAILOVER_MODE + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_PACKET_AVAILABLE_DMA_MEMORY_POOL_SIZE = (SAI_SWITCH_ATTR_TUNNEL_OBJECTS_LIST + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_PRE_INGRESS_ACL = (SAI_SWITCH_ATTR_PACKET_AVAILABLE_DMA_MEMORY_POOL_SIZE + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_AVAILABLE_SNAPT_ENTRY = (SAI_SWITCH_ATTR_PRE_INGRESS_ACL + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_AVAILABLE_DNAPT_ENTRY = (SAI_SWITCH_ATTR_AVAILABLE_SNAPT_ENTRY + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_AVAILABLE_DOUBLE_NAPT_ENTRY = (SAI_SWITCH_ATTR_AVAILABLE_DNAPT_ENTRY + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_SLAVE_MDIO_ADDR_LIST = (SAI_SWITCH_ATTR_AVAILABLE_DOUBLE_NAPT_ENTRY + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_MY_MAC_TABLE_MINIMUM_PRIORITY = (SAI_SWITCH_ATTR_SLAVE_MDIO_ADDR_LIST + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_MY_MAC_TABLE_MAXIMUM_PRIORITY = (SAI_SWITCH_ATTR_MY_MAC_TABLE_MINIMUM_PRIORITY + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_MY_MAC_LIST = (SAI_SWITCH_ATTR_MY_MAC_TABLE_MAXIMUM_PRIORITY + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_INSTALLED_MY_MAC_ENTRIES = (SAI_SWITCH_ATTR_MY_MAC_LIST + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_AVAILABLE_MY_MAC_ENTRIES = (SAI_SWITCH_ATTR_INSTALLED_MY_MAC_ENTRIES + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_MAX_NUMBER_OF_FORWARDING_CLASSES = (SAI_SWITCH_ATTR_AVAILABLE_MY_MAC_ENTRIES + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_QOS_DSCP_TO_FORWARDING_CLASS_MAP = (SAI_SWITCH_ATTR_MAX_NUMBER_OF_FORWARDING_CLASSES + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_QOS_MPLS_EXP_TO_FORWARDING_CLASS_MAP = (SAI_SWITCH_ATTR_QOS_DSCP_TO_FORWARDING_CLASS_MAP + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_IPSEC_OBJECT_ID = (SAI_SWITCH_ATTR_QOS_MPLS_EXP_TO_FORWARDING_CLASS_MAP + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_IPSEC_SA_TAG_TPID = (SAI_SWITCH_ATTR_IPSEC_OBJECT_ID + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_IPSEC_SA_STATUS_CHANGE_NOTIFY = (SAI_SWITCH_ATTR_IPSEC_SA_TAG_TPID + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_NAT_EVENT_NOTIFY = (SAI_SWITCH_ATTR_IPSEC_SA_STATUS_CHANGE_NOTIFY + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_MAX_ECMP_MEMBER_COUNT = (SAI_SWITCH_ATTR_NAT_EVENT_NOTIFY + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_ECMP_MEMBER_COUNT = (SAI_SWITCH_ATTR_MAX_ECMP_MEMBER_COUNT + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_ARS_PROFILE = (SAI_SWITCH_ATTR_ECMP_MEMBER_COUNT + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_ACL_STAGE_POST_INGRESS = (SAI_SWITCH_ATTR_ARS_PROFILE + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_CREDIT_WD = (SAI_SWITCH_ATTR_ACL_STAGE_POST_INGRESS + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_CREDIT_WD_TIMER = (SAI_SWITCH_ATTR_CREDIT_WD + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_SWITCH_ISOLATE = (SAI_SWITCH_ATTR_CREDIT_WD_TIMER + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_HOSTIF_OPER_STATUS_UPDATE_MODE = (SAI_SWITCH_ATTR_SWITCH_ISOLATE + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_SWITCH_ASIC_SDK_HEALTH_EVENT_NOTIFY = (SAI_SWITCH_ATTR_HOSTIF_OPER_STATUS_UPDATE_MODE + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_REG_FATAL_SWITCH_ASIC_SDK_HEALTH_CATEGORY = (SAI_SWITCH_ATTR_SWITCH_ASIC_SDK_HEALTH_EVENT_NOTIFY + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_REG_WARNING_SWITCH_ASIC_SDK_HEALTH_CATEGORY = (SAI_SWITCH_ATTR_REG_FATAL_SWITCH_ASIC_SDK_HEALTH_CATEGORY + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_REG_NOTICE_SWITCH_ASIC_SDK_HEALTH_CATEGORY = (SAI_SWITCH_ATTR_REG_WARNING_SWITCH_ASIC_SDK_HEALTH_CATEGORY + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_ACL_CHAIN_LIST = (SAI_SWITCH_ATTR_REG_NOTICE_SWITCH_ASIC_SDK_HEALTH_CATEGORY + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_PORT_HOST_TX_READY_NOTIFY = (SAI_SWITCH_ATTR_ACL_CHAIN_LIST + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_TUNNEL_TERM_TABLE_ENTRY_MINIMUM_PRIORITY = (SAI_SWITCH_ATTR_PORT_HOST_TX_READY_NOTIFY + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_TUNNEL_TERM_TABLE_ENTRY_MAXIMUM_PRIORITY = (SAI_SWITCH_ATTR_TUNNEL_TERM_TABLE_ENTRY_MINIMUM_PRIORITY + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_TWAMP_SESSION_EVENT_NOTIFY = (SAI_SWITCH_ATTR_TUNNEL_TERM_TABLE_ENTRY_MAXIMUM_PRIORITY + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_AVAILABLE_TWAMP_SESSION = (SAI_SWITCH_ATTR_TWAMP_SESSION_EVENT_NOTIFY + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_MAX_TWAMP_SESSION = (SAI_SWITCH_ATTR_AVAILABLE_TWAMP_SESSION + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_AVAILABLE_IP_NEXT_HOP_GROUP_MEMBER_ENTRY = (SAI_SWITCH_ATTR_MAX_TWAMP_SESSION + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_AVAILABLE_SYSTEM_VOQS = (SAI_SWITCH_ATTR_AVAILABLE_IP_NEXT_HOP_GROUP_MEMBER_ENTRY + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_END = (SAI_SWITCH_ATTR_AVAILABLE_SYSTEM_VOQS + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_CUSTOM_RANGE_START = 0x10000000# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

SAI_SWITCH_ATTR_CUSTOM_RANGE_END = (SAI_SWITCH_ATTR_CUSTOM_RANGE_START + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

sai_switch_attr_t = enum__sai_switch_attr_t# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3014

enum__sai_switch_asic_sdk_health_severity_t = c_int# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3030

SAI_SWITCH_ASIC_SDK_HEALTH_SEVERITY_FATAL = 0# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3030

SAI_SWITCH_ASIC_SDK_HEALTH_SEVERITY_WARNING = (SAI_SWITCH_ASIC_SDK_HEALTH_SEVERITY_FATAL + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3030

SAI_SWITCH_ASIC_SDK_HEALTH_SEVERITY_NOTICE = (SAI_SWITCH_ASIC_SDK_HEALTH_SEVERITY_WARNING + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3030

sai_switch_asic_sdk_health_severity_t = enum__sai_switch_asic_sdk_health_severity_t# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3030

enum__sai_switch_asic_sdk_health_category_t = c_int# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3049

SAI_SWITCH_ASIC_SDK_HEALTH_CATEGORY_SW = 0# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3049

SAI_SWITCH_ASIC_SDK_HEALTH_CATEGORY_FW = (SAI_SWITCH_ASIC_SDK_HEALTH_CATEGORY_SW + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3049

SAI_SWITCH_ASIC_SDK_HEALTH_CATEGORY_CPU_HW = (SAI_SWITCH_ASIC_SDK_HEALTH_CATEGORY_FW + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3049

SAI_SWITCH_ASIC_SDK_HEALTH_CATEGORY_ASIC_HW = (SAI_SWITCH_ASIC_SDK_HEALTH_CATEGORY_CPU_HW + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3049

sai_switch_asic_sdk_health_category_t = enum__sai_switch_asic_sdk_health_category_t# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3049

enum__sai_switch_stat_t = c_int# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3139

SAI_SWITCH_STAT_IN_DROP_REASON_RANGE_BASE = 0x00001000# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3139

SAI_SWITCH_STAT_IN_CONFIGURED_DROP_REASONS_0_DROPPED_PKTS = SAI_SWITCH_STAT_IN_DROP_REASON_RANGE_BASE# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3139

SAI_SWITCH_STAT_IN_CONFIGURED_DROP_REASONS_1_DROPPED_PKTS = (SAI_SWITCH_STAT_IN_CONFIGURED_DROP_REASONS_0_DROPPED_PKTS + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3139

SAI_SWITCH_STAT_IN_CONFIGURED_DROP_REASONS_2_DROPPED_PKTS = (SAI_SWITCH_STAT_IN_CONFIGURED_DROP_REASONS_1_DROPPED_PKTS + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3139

SAI_SWITCH_STAT_IN_CONFIGURED_DROP_REASONS_3_DROPPED_PKTS = (SAI_SWITCH_STAT_IN_CONFIGURED_DROP_REASONS_2_DROPPED_PKTS + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3139

SAI_SWITCH_STAT_IN_CONFIGURED_DROP_REASONS_4_DROPPED_PKTS = (SAI_SWITCH_STAT_IN_CONFIGURED_DROP_REASONS_3_DROPPED_PKTS + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3139

SAI_SWITCH_STAT_IN_CONFIGURED_DROP_REASONS_5_DROPPED_PKTS = (SAI_SWITCH_STAT_IN_CONFIGURED_DROP_REASONS_4_DROPPED_PKTS + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3139

SAI_SWITCH_STAT_IN_CONFIGURED_DROP_REASONS_6_DROPPED_PKTS = (SAI_SWITCH_STAT_IN_CONFIGURED_DROP_REASONS_5_DROPPED_PKTS + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3139

SAI_SWITCH_STAT_IN_CONFIGURED_DROP_REASONS_7_DROPPED_PKTS = (SAI_SWITCH_STAT_IN_CONFIGURED_DROP_REASONS_6_DROPPED_PKTS + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3139

SAI_SWITCH_STAT_IN_DROP_REASON_RANGE_END = 0x00001fff# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3139

SAI_SWITCH_STAT_OUT_DROP_REASON_RANGE_BASE = 0x00002000# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3139

SAI_SWITCH_STAT_OUT_CONFIGURED_DROP_REASONS_0_DROPPED_PKTS = SAI_SWITCH_STAT_OUT_DROP_REASON_RANGE_BASE# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3139

SAI_SWITCH_STAT_OUT_CONFIGURED_DROP_REASONS_1_DROPPED_PKTS = (SAI_SWITCH_STAT_OUT_CONFIGURED_DROP_REASONS_0_DROPPED_PKTS + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3139

SAI_SWITCH_STAT_OUT_CONFIGURED_DROP_REASONS_2_DROPPED_PKTS = (SAI_SWITCH_STAT_OUT_CONFIGURED_DROP_REASONS_1_DROPPED_PKTS + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3139

SAI_SWITCH_STAT_OUT_CONFIGURED_DROP_REASONS_3_DROPPED_PKTS = (SAI_SWITCH_STAT_OUT_CONFIGURED_DROP_REASONS_2_DROPPED_PKTS + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3139

SAI_SWITCH_STAT_OUT_CONFIGURED_DROP_REASONS_4_DROPPED_PKTS = (SAI_SWITCH_STAT_OUT_CONFIGURED_DROP_REASONS_3_DROPPED_PKTS + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3139

SAI_SWITCH_STAT_OUT_CONFIGURED_DROP_REASONS_5_DROPPED_PKTS = (SAI_SWITCH_STAT_OUT_CONFIGURED_DROP_REASONS_4_DROPPED_PKTS + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3139

SAI_SWITCH_STAT_OUT_CONFIGURED_DROP_REASONS_6_DROPPED_PKTS = (SAI_SWITCH_STAT_OUT_CONFIGURED_DROP_REASONS_5_DROPPED_PKTS + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3139

SAI_SWITCH_STAT_OUT_CONFIGURED_DROP_REASONS_7_DROPPED_PKTS = (SAI_SWITCH_STAT_OUT_CONFIGURED_DROP_REASONS_6_DROPPED_PKTS + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3139

SAI_SWITCH_STAT_OUT_DROP_REASON_RANGE_END = 0x00002fff# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3139

SAI_SWITCH_STAT_FABRIC_DROP_REASON_RANGE_BASE = 0x00003000# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3139

SAI_SWITCH_STAT_ECC_DROP = SAI_SWITCH_STAT_FABRIC_DROP_REASON_RANGE_BASE# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3139

SAI_SWITCH_STAT_REACHABILITY_DROP = (SAI_SWITCH_STAT_ECC_DROP + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3139

SAI_SWITCH_STAT_HIGHEST_QUEUE_CONGESTION_LEVEL = (SAI_SWITCH_STAT_REACHABILITY_DROP + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3139

SAI_SWITCH_STAT_GLOBAL_DROP = (SAI_SWITCH_STAT_HIGHEST_QUEUE_CONGESTION_LEVEL + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3139

SAI_SWITCH_STAT_PACKET_INTEGRITY_DROP = (SAI_SWITCH_STAT_GLOBAL_DROP + 1)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3139

SAI_SWITCH_STAT_FABRIC_DROP_REASON_RANGE_END = 0x00003fff# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3139

sai_switch_stat_t = enum__sai_switch_stat_t# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3139

sai_switch_asic_sdk_health_event_notification_fn = CFUNCTYPE(UNCHECKED(None), sai_object_id_t, sai_switch_asic_sdk_health_severity_t, sai_timespec_t, sai_switch_asic_sdk_health_category_t, sai_switch_health_data_t, sai_u8_list_t)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3276

sai_switch_shutdown_request_notification_fn = CFUNCTYPE(UNCHECKED(None), sai_object_id_t)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3294

sai_switch_state_change_notification_fn = CFUNCTYPE(UNCHECKED(None), sai_object_id_t, sai_switch_oper_status_t)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3305

sai_switch_register_read_fn = CFUNCTYPE(UNCHECKED(sai_status_t), uint64_t, uint32_t, uint32_t, uint32_t, POINTER(uint32_t))# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3325

sai_switch_register_write_fn = CFUNCTYPE(UNCHECKED(sai_status_t), uint64_t, uint32_t, uint32_t, uint32_t, POINTER(uint32_t))# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3348

sai_switch_mdio_read_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, uint32_t, uint32_t, uint32_t, POINTER(uint32_t))# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3368

sai_switch_mdio_write_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, uint32_t, uint32_t, uint32_t, POINTER(uint32_t))# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3388

sai_switch_mdio_cl22_read_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, uint32_t, uint32_t, uint32_t, POINTER(uint32_t))# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3408

sai_switch_mdio_cl22_write_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, uint32_t, uint32_t, uint32_t, POINTER(uint32_t))# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3428

sai_create_switch_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3448

sai_remove_switch_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3462

sai_set_switch_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3473

sai_get_switch_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3486

sai_get_switch_stats_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, uint32_t, POINTER(sai_stat_id_t), POINTER(uint64_t))# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3501

sai_get_switch_stats_ext_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, uint32_t, POINTER(sai_stat_id_t), sai_stats_mode_t, POINTER(uint64_t))# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3518

sai_clear_switch_stats_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, uint32_t, POINTER(sai_stat_id_t))# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3534

sai_create_switch_tunnel_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3549

sai_remove_switch_tunnel_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t)# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3564

sai_set_switch_tunnel_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3575

sai_get_switch_tunnel_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3588

# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3614
class struct__sai_switch_api_t(Structure):
    pass

struct__sai_switch_api_t.__slots__ = [
    'create_switch',
    'remove_switch',
    'set_switch_attribute',
    'get_switch_attribute',
    'get_switch_stats',
    'get_switch_stats_ext',
    'clear_switch_stats',
    'switch_mdio_read',
    'switch_mdio_write',
    'create_switch_tunnel',
    'remove_switch_tunnel',
    'set_switch_tunnel_attribute',
    'get_switch_tunnel_attribute',
    'switch_mdio_cl22_read',
    'switch_mdio_cl22_write',
]
struct__sai_switch_api_t._fields_ = [
    ('create_switch', sai_create_switch_fn),
    ('remove_switch', sai_remove_switch_fn),
    ('set_switch_attribute', sai_set_switch_attribute_fn),
    ('get_switch_attribute', sai_get_switch_attribute_fn),
    ('get_switch_stats', sai_get_switch_stats_fn),
    ('get_switch_stats_ext', sai_get_switch_stats_ext_fn),
    ('clear_switch_stats', sai_clear_switch_stats_fn),
    ('switch_mdio_read', sai_switch_mdio_read_fn),
    ('switch_mdio_write', sai_switch_mdio_write_fn),
    ('create_switch_tunnel', sai_create_switch_tunnel_fn),
    ('remove_switch_tunnel', sai_remove_switch_tunnel_fn),
    ('set_switch_tunnel_attribute', sai_set_switch_tunnel_attribute_fn),
    ('get_switch_tunnel_attribute', sai_get_switch_tunnel_attribute_fn),
    ('switch_mdio_cl22_read', sai_switch_mdio_cl22_read_fn),
    ('switch_mdio_cl22_write', sai_switch_mdio_cl22_write_fn),
]

sai_switch_api_t = struct__sai_switch_api_t# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3614

enum__sai_system_port_type_t = c_int# /home/bluecmd/Downloads/SAI/inc/saisystemport.h: 47

SAI_SYSTEM_PORT_TYPE_LOCAL = 0# /home/bluecmd/Downloads/SAI/inc/saisystemport.h: 47

SAI_SYSTEM_PORT_TYPE_REMOTE = (SAI_SYSTEM_PORT_TYPE_LOCAL + 1)# /home/bluecmd/Downloads/SAI/inc/saisystemport.h: 47

sai_system_port_type_t = enum__sai_system_port_type_t# /home/bluecmd/Downloads/SAI/inc/saisystemport.h: 47

enum__sai_system_port_attr_t = c_int# /home/bluecmd/Downloads/SAI/inc/saisystemport.h: 142

SAI_SYSTEM_PORT_ATTR_START = 0# /home/bluecmd/Downloads/SAI/inc/saisystemport.h: 142

SAI_SYSTEM_PORT_ATTR_TYPE = SAI_SYSTEM_PORT_ATTR_START# /home/bluecmd/Downloads/SAI/inc/saisystemport.h: 142

SAI_SYSTEM_PORT_ATTR_QOS_NUMBER_OF_VOQS = (SAI_SYSTEM_PORT_ATTR_TYPE + 1)# /home/bluecmd/Downloads/SAI/inc/saisystemport.h: 142

SAI_SYSTEM_PORT_ATTR_QOS_VOQ_LIST = (SAI_SYSTEM_PORT_ATTR_QOS_NUMBER_OF_VOQS + 1)# /home/bluecmd/Downloads/SAI/inc/saisystemport.h: 142

SAI_SYSTEM_PORT_ATTR_PORT = (SAI_SYSTEM_PORT_ATTR_QOS_VOQ_LIST + 1)# /home/bluecmd/Downloads/SAI/inc/saisystemport.h: 142

SAI_SYSTEM_PORT_ATTR_ADMIN_STATE = (SAI_SYSTEM_PORT_ATTR_PORT + 1)# /home/bluecmd/Downloads/SAI/inc/saisystemport.h: 142

SAI_SYSTEM_PORT_ATTR_CONFIG_INFO = (SAI_SYSTEM_PORT_ATTR_ADMIN_STATE + 1)# /home/bluecmd/Downloads/SAI/inc/saisystemport.h: 142

SAI_SYSTEM_PORT_ATTR_QOS_TC_TO_QUEUE_MAP = (SAI_SYSTEM_PORT_ATTR_CONFIG_INFO + 1)# /home/bluecmd/Downloads/SAI/inc/saisystemport.h: 142

SAI_SYSTEM_PORT_ATTR_END = (SAI_SYSTEM_PORT_ATTR_QOS_TC_TO_QUEUE_MAP + 1)# /home/bluecmd/Downloads/SAI/inc/saisystemport.h: 142

SAI_SYSTEM_PORT_ATTR_CUSTOM_RANGE_START = 0x10000000# /home/bluecmd/Downloads/SAI/inc/saisystemport.h: 142

SAI_SYSTEM_PORT_ATTR_CUSTOM_RANGE_END = (SAI_SYSTEM_PORT_ATTR_CUSTOM_RANGE_START + 1)# /home/bluecmd/Downloads/SAI/inc/saisystemport.h: 142

sai_system_port_attr_t = enum__sai_system_port_attr_t# /home/bluecmd/Downloads/SAI/inc/saisystemport.h: 142

sai_create_system_port_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saisystemport.h: 154

sai_remove_system_port_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t)# /home/bluecmd/Downloads/SAI/inc/saisystemport.h: 167

sai_set_system_port_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saisystemport.h: 178

sai_get_system_port_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saisystemport.h: 191

# /home/bluecmd/Downloads/SAI/inc/saisystemport.h: 206
class struct__sai_system_port_api_t(Structure):
    pass

struct__sai_system_port_api_t.__slots__ = [
    'create_system_port',
    'remove_system_port',
    'set_system_port_attribute',
    'get_system_port_attribute',
]
struct__sai_system_port_api_t._fields_ = [
    ('create_system_port', sai_create_system_port_fn),
    ('remove_system_port', sai_remove_system_port_fn),
    ('set_system_port_attribute', sai_set_system_port_attribute_fn),
    ('get_system_port_attribute', sai_get_system_port_attribute_fn),
]

sai_system_port_api_t = struct__sai_system_port_api_t# /home/bluecmd/Downloads/SAI/inc/saisystemport.h: 206

enum__sai_tam_attr_t = c_int# /home/bluecmd/Downloads/SAI/inc/saitam.h: 100

SAI_TAM_ATTR_START = 0# /home/bluecmd/Downloads/SAI/inc/saitam.h: 100

SAI_TAM_ATTR_TELEMETRY_OBJECTS_LIST = SAI_TAM_ATTR_START# /home/bluecmd/Downloads/SAI/inc/saitam.h: 100

SAI_TAM_ATTR_EVENT_OBJECTS_LIST = (SAI_TAM_ATTR_TELEMETRY_OBJECTS_LIST + 1)# /home/bluecmd/Downloads/SAI/inc/saitam.h: 100

SAI_TAM_ATTR_INT_OBJECTS_LIST = (SAI_TAM_ATTR_EVENT_OBJECTS_LIST + 1)# /home/bluecmd/Downloads/SAI/inc/saitam.h: 100

SAI_TAM_ATTR_TAM_BIND_POINT_TYPE_LIST = (SAI_TAM_ATTR_INT_OBJECTS_LIST + 1)# /home/bluecmd/Downloads/SAI/inc/saitam.h: 100

SAI_TAM_ATTR_END = (SAI_TAM_ATTR_TAM_BIND_POINT_TYPE_LIST + 1)# /home/bluecmd/Downloads/SAI/inc/saitam.h: 100

SAI_TAM_ATTR_CUSTOM_RANGE_START = 0x10000000# /home/bluecmd/Downloads/SAI/inc/saitam.h: 100

SAI_TAM_ATTR_CUSTOM_RANGE_END = (SAI_TAM_ATTR_CUSTOM_RANGE_START + 1)# /home/bluecmd/Downloads/SAI/inc/saitam.h: 100

sai_tam_attr_t = enum__sai_tam_attr_t# /home/bluecmd/Downloads/SAI/inc/saitam.h: 100

sai_create_tam_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saitam.h: 116

sai_remove_tam_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t)# /home/bluecmd/Downloads/SAI/inc/saitam.h: 131

sai_set_tam_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saitam.h: 142

sai_get_tam_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saitam.h: 155

enum__sai_tam_tel_math_func_type_t = c_int# /home/bluecmd/Downloads/SAI/inc/saitam.h: 183

SAI_TAM_TEL_MATH_FUNC_TYPE_NONE = 0# /home/bluecmd/Downloads/SAI/inc/saitam.h: 183

SAI_TAM_TEL_MATH_FUNC_TYPE_GEO_MEAN = (SAI_TAM_TEL_MATH_FUNC_TYPE_NONE + 1)# /home/bluecmd/Downloads/SAI/inc/saitam.h: 183

SAI_TAM_TEL_MATH_FUNC_TYPE_ALGEBRAIC_MEAN = (SAI_TAM_TEL_MATH_FUNC_TYPE_GEO_MEAN + 1)# /home/bluecmd/Downloads/SAI/inc/saitam.h: 183

SAI_TAM_TEL_MATH_FUNC_TYPE_AVERAGE = (SAI_TAM_TEL_MATH_FUNC_TYPE_ALGEBRAIC_MEAN + 1)# /home/bluecmd/Downloads/SAI/inc/saitam.h: 183

SAI_TAM_TEL_MATH_FUNC_TYPE_MODE = (SAI_TAM_TEL_MATH_FUNC_TYPE_AVERAGE + 1)# /home/bluecmd/Downloads/SAI/inc/saitam.h: 183

SAI_TAM_TEL_MATH_FUNC_TYPE_RATE = (SAI_TAM_TEL_MATH_FUNC_TYPE_MODE + 1)# /home/bluecmd/Downloads/SAI/inc/saitam.h: 183

sai_tam_tel_math_func_type_t = enum__sai_tam_tel_math_func_type_t# /home/bluecmd/Downloads/SAI/inc/saitam.h: 183

enum__sai_tam_math_func_attr_t = c_int# /home/bluecmd/Downloads/SAI/inc/saitam.h: 215

SAI_TAM_MATH_FUNC_ATTR_START = 0# /home/bluecmd/Downloads/SAI/inc/saitam.h: 215

SAI_TAM_MATH_FUNC_ATTR_TAM_TEL_MATH_FUNC_TYPE = SAI_TAM_MATH_FUNC_ATTR_START# /home/bluecmd/Downloads/SAI/inc/saitam.h: 215

SAI_TAM_MATH_FUNC_ATTR_END = (SAI_TAM_MATH_FUNC_ATTR_TAM_TEL_MATH_FUNC_TYPE + 1)# /home/bluecmd/Downloads/SAI/inc/saitam.h: 215

SAI_TAM_MATH_FUNC_ATTR_CUSTOM_RANGE_START = 0x10000000# /home/bluecmd/Downloads/SAI/inc/saitam.h: 215

SAI_TAM_MATH_FUNC_ATTR_CUSTOM_RANGE_END = (SAI_TAM_MATH_FUNC_ATTR_CUSTOM_RANGE_START + 1)# /home/bluecmd/Downloads/SAI/inc/saitam.h: 215

sai_tam_math_func_attr_t = enum__sai_tam_math_func_attr_t# /home/bluecmd/Downloads/SAI/inc/saitam.h: 215

sai_create_tam_math_func_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saitam.h: 227

sai_remove_tam_math_func_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t)# /home/bluecmd/Downloads/SAI/inc/saitam.h: 240

sai_get_tam_math_func_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saitam.h: 252

sai_set_tam_math_func_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saitam.h: 265

enum__sai_tam_event_threshold_unit_t = c_int# /home/bluecmd/Downloads/SAI/inc/saitam.h: 308

SAI_TAM_EVENT_THRESHOLD_UNIT_NANOSEC = 0# /home/bluecmd/Downloads/SAI/inc/saitam.h: 308

SAI_TAM_EVENT_THRESHOLD_UNIT_USEC = (SAI_TAM_EVENT_THRESHOLD_UNIT_NANOSEC + 1)# /home/bluecmd/Downloads/SAI/inc/saitam.h: 308

SAI_TAM_EVENT_THRESHOLD_UNIT_MSEC = (SAI_TAM_EVENT_THRESHOLD_UNIT_USEC + 1)# /home/bluecmd/Downloads/SAI/inc/saitam.h: 308

SAI_TAM_EVENT_THRESHOLD_UNIT_PERCENT = (SAI_TAM_EVENT_THRESHOLD_UNIT_MSEC + 1)# /home/bluecmd/Downloads/SAI/inc/saitam.h: 308

SAI_TAM_EVENT_THRESHOLD_UNIT_BYTES = (SAI_TAM_EVENT_THRESHOLD_UNIT_PERCENT + 1)# /home/bluecmd/Downloads/SAI/inc/saitam.h: 308

SAI_TAM_EVENT_THRESHOLD_UNIT_PACKETS = (SAI_TAM_EVENT_THRESHOLD_UNIT_BYTES + 1)# /home/bluecmd/Downloads/SAI/inc/saitam.h: 308

SAI_TAM_EVENT_THRESHOLD_UNIT_CELLS = (SAI_TAM_EVENT_THRESHOLD_UNIT_PACKETS + 1)# /home/bluecmd/Downloads/SAI/inc/saitam.h: 308

sai_tam_event_threshold_unit_t = enum__sai_tam_event_threshold_unit_t# /home/bluecmd/Downloads/SAI/inc/saitam.h: 308

enum__sai_tam_event_threshold_attr_t = c_int# /home/bluecmd/Downloads/SAI/inc/saitam.h: 385

SAI_TAM_EVENT_THRESHOLD_ATTR_START = 0# /home/bluecmd/Downloads/SAI/inc/saitam.h: 385

SAI_TAM_EVENT_THRESHOLD_ATTR_HIGH_WATERMARK = SAI_TAM_EVENT_THRESHOLD_ATTR_START# /home/bluecmd/Downloads/SAI/inc/saitam.h: 385

SAI_TAM_EVENT_THRESHOLD_ATTR_LOW_WATERMARK = (SAI_TAM_EVENT_THRESHOLD_ATTR_HIGH_WATERMARK + 1)# /home/bluecmd/Downloads/SAI/inc/saitam.h: 385

SAI_TAM_EVENT_THRESHOLD_ATTR_LATENCY = (SAI_TAM_EVENT_THRESHOLD_ATTR_LOW_WATERMARK + 1)# /home/bluecmd/Downloads/SAI/inc/saitam.h: 385

SAI_TAM_EVENT_THRESHOLD_ATTR_RATE = (SAI_TAM_EVENT_THRESHOLD_ATTR_LATENCY + 1)# /home/bluecmd/Downloads/SAI/inc/saitam.h: 385

SAI_TAM_EVENT_THRESHOLD_ATTR_ABS_VALUE = (SAI_TAM_EVENT_THRESHOLD_ATTR_RATE + 1)# /home/bluecmd/Downloads/SAI/inc/saitam.h: 385

SAI_TAM_EVENT_THRESHOLD_ATTR_UNIT = (SAI_TAM_EVENT_THRESHOLD_ATTR_ABS_VALUE + 1)# /home/bluecmd/Downloads/SAI/inc/saitam.h: 385

SAI_TAM_EVENT_THRESHOLD_ATTR_END = (SAI_TAM_EVENT_THRESHOLD_ATTR_UNIT + 1)# /home/bluecmd/Downloads/SAI/inc/saitam.h: 385

SAI_TAM_EVENT_THRESHOLD_ATTR_CUSTOM_RANGE_START = 0x10000000# /home/bluecmd/Downloads/SAI/inc/saitam.h: 385

SAI_TAM_EVENT_THRESHOLD_ATTR_CUSTOM_RANGE_END = (SAI_TAM_EVENT_THRESHOLD_ATTR_CUSTOM_RANGE_START + 1)# /home/bluecmd/Downloads/SAI/inc/saitam.h: 385

sai_tam_event_threshold_attr_t = enum__sai_tam_event_threshold_attr_t# /home/bluecmd/Downloads/SAI/inc/saitam.h: 385

sai_create_tam_event_threshold_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saitam.h: 397

sai_remove_tam_event_threshold_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t)# /home/bluecmd/Downloads/SAI/inc/saitam.h: 410

sai_get_tam_event_threshold_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saitam.h: 422

sai_set_tam_event_threshold_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saitam.h: 435

enum__sai_tam_int_type_t = c_int# /home/bluecmd/Downloads/SAI/inc/saitam.h: 484

SAI_TAM_INT_TYPE_IOAM = 0# /home/bluecmd/Downloads/SAI/inc/saitam.h: 484

SAI_TAM_INT_TYPE_IFA1 = (SAI_TAM_INT_TYPE_IOAM + 1)# /home/bluecmd/Downloads/SAI/inc/saitam.h: 484

SAI_TAM_INT_TYPE_IFA2 = (SAI_TAM_INT_TYPE_IFA1 + 1)# /home/bluecmd/Downloads/SAI/inc/saitam.h: 484

SAI_TAM_INT_TYPE_P4_INT_1 = (SAI_TAM_INT_TYPE_IFA2 + 1)# /home/bluecmd/Downloads/SAI/inc/saitam.h: 484

SAI_TAM_INT_TYPE_P4_INT_2 = (SAI_TAM_INT_TYPE_P4_INT_1 + 1)# /home/bluecmd/Downloads/SAI/inc/saitam.h: 484

SAI_TAM_INT_TYPE_DIRECT_EXPORT = (SAI_TAM_INT_TYPE_P4_INT_2 + 1)# /home/bluecmd/Downloads/SAI/inc/saitam.h: 484

SAI_TAM_INT_TYPE_IFA1_TAILSTAMP = (SAI_TAM_INT_TYPE_DIRECT_EXPORT + 1)# /home/bluecmd/Downloads/SAI/inc/saitam.h: 484

SAI_TAM_INT_TYPE_PATH_TRACING = (SAI_TAM_INT_TYPE_IFA1_TAILSTAMP + 1)# /home/bluecmd/Downloads/SAI/inc/saitam.h: 484

sai_tam_int_type_t = enum__sai_tam_int_type_t# /home/bluecmd/Downloads/SAI/inc/saitam.h: 484

enum__sai_tam_int_presence_type_t = c_int# /home/bluecmd/Downloads/SAI/inc/saitam.h: 514

SAI_TAM_INT_PRESENCE_TYPE_UNDEFINED = 0# /home/bluecmd/Downloads/SAI/inc/saitam.h: 514

SAI_TAM_INT_PRESENCE_TYPE_PB = (SAI_TAM_INT_PRESENCE_TYPE_UNDEFINED + 1)# /home/bluecmd/Downloads/SAI/inc/saitam.h: 514

SAI_TAM_INT_PRESENCE_TYPE_L3_PROTOCOL = (SAI_TAM_INT_PRESENCE_TYPE_PB + 1)# /home/bluecmd/Downloads/SAI/inc/saitam.h: 514

SAI_TAM_INT_PRESENCE_TYPE_DSCP = (SAI_TAM_INT_PRESENCE_TYPE_L3_PROTOCOL + 1)# /home/bluecmd/Downloads/SAI/inc/saitam.h: 514

sai_tam_int_presence_type_t = enum__sai_tam_int_presence_type_t# /home/bluecmd/Downloads/SAI/inc/saitam.h: 514

enum__sai_tam_int_attr_t = c_int# /home/bluecmd/Downloads/SAI/inc/saitam.h: 810

SAI_TAM_INT_ATTR_START = 0# /home/bluecmd/Downloads/SAI/inc/saitam.h: 810

SAI_TAM_INT_ATTR_TYPE = SAI_TAM_INT_ATTR_START# /home/bluecmd/Downloads/SAI/inc/saitam.h: 810

SAI_TAM_INT_ATTR_DEVICE_ID = (SAI_TAM_INT_ATTR_TYPE + 1)# /home/bluecmd/Downloads/SAI/inc/saitam.h: 810

SAI_TAM_INT_ATTR_IOAM_TRACE_TYPE = (SAI_TAM_INT_ATTR_DEVICE_ID + 1)# /home/bluecmd/Downloads/SAI/inc/saitam.h: 810

SAI_TAM_INT_ATTR_INT_PRESENCE_TYPE = (SAI_TAM_INT_ATTR_IOAM_TRACE_TYPE + 1)# /home/bluecmd/Downloads/SAI/inc/saitam.h: 810

SAI_TAM_INT_ATTR_INT_PRESENCE_PB1 = (SAI_TAM_INT_ATTR_INT_PRESENCE_TYPE + 1)# /home/bluecmd/Downloads/SAI/inc/saitam.h: 810

SAI_TAM_INT_ATTR_INT_PRESENCE_PB2 = (SAI_TAM_INT_ATTR_INT_PRESENCE_PB1 + 1)# /home/bluecmd/Downloads/SAI/inc/saitam.h: 810

SAI_TAM_INT_ATTR_INT_PRESENCE_DSCP_VALUE = (SAI_TAM_INT_ATTR_INT_PRESENCE_PB2 + 1)# /home/bluecmd/Downloads/SAI/inc/saitam.h: 810

SAI_TAM_INT_ATTR_INLINE = (SAI_TAM_INT_ATTR_INT_PRESENCE_DSCP_VALUE + 1)# /home/bluecmd/Downloads/SAI/inc/saitam.h: 810

SAI_TAM_INT_ATTR_INT_PRESENCE_L3_PROTOCOL = (SAI_TAM_INT_ATTR_INLINE + 1)# /home/bluecmd/Downloads/SAI/inc/saitam.h: 810

SAI_TAM_INT_ATTR_TRACE_VECTOR = (SAI_TAM_INT_ATTR_INT_PRESENCE_L3_PROTOCOL + 1)# /home/bluecmd/Downloads/SAI/inc/saitam.h: 810

SAI_TAM_INT_ATTR_ACTION_VECTOR = (SAI_TAM_INT_ATTR_TRACE_VECTOR + 1)# /home/bluecmd/Downloads/SAI/inc/saitam.h: 810

SAI_TAM_INT_ATTR_P4_INT_INSTRUCTION_BITMAP = (SAI_TAM_INT_ATTR_ACTION_VECTOR + 1)# /home/bluecmd/Downloads/SAI/inc/saitam.h: 810

SAI_TAM_INT_ATTR_METADATA_FRAGMENT_ENABLE = (SAI_TAM_INT_ATTR_P4_INT_INSTRUCTION_BITMAP + 1)# /home/bluecmd/Downloads/SAI/inc/saitam.h: 810

SAI_TAM_INT_ATTR_METADATA_CHECKSUM_ENABLE = (SAI_TAM_INT_ATTR_METADATA_FRAGMENT_ENABLE + 1)# /home/bluecmd/Downloads/SAI/inc/saitam.h: 810

SAI_TAM_INT_ATTR_REPORT_ALL_PACKETS = (SAI_TAM_INT_ATTR_METADATA_CHECKSUM_ENABLE + 1)# /home/bluecmd/Downloads/SAI/inc/saitam.h: 810

SAI_TAM_INT_ATTR_FLOW_LIVENESS_PERIOD = (SAI_TAM_INT_ATTR_REPORT_ALL_PACKETS + 1)# /home/bluecmd/Downloads/SAI/inc/saitam.h: 810

SAI_TAM_INT_ATTR_LATENCY_SENSITIVITY = (SAI_TAM_INT_ATTR_FLOW_LIVENESS_PERIOD + 1)# /home/bluecmd/Downloads/SAI/inc/saitam.h: 810

SAI_TAM_INT_ATTR_ACL_GROUP = (SAI_TAM_INT_ATTR_LATENCY_SENSITIVITY + 1)# /home/bluecmd/Downloads/SAI/inc/saitam.h: 810

SAI_TAM_INT_ATTR_MAX_HOP_COUNT = (SAI_TAM_INT_ATTR_ACL_GROUP + 1)# /home/bluecmd/Downloads/SAI/inc/saitam.h: 810

SAI_TAM_INT_ATTR_MAX_LENGTH = (SAI_TAM_INT_ATTR_MAX_HOP_COUNT + 1)# /home/bluecmd/Downloads/SAI/inc/saitam.h: 810

SAI_TAM_INT_ATTR_NAME_SPACE_ID = (SAI_TAM_INT_ATTR_MAX_LENGTH + 1)# /home/bluecmd/Downloads/SAI/inc/saitam.h: 810

SAI_TAM_INT_ATTR_NAME_SPACE_ID_GLOBAL = (SAI_TAM_INT_ATTR_NAME_SPACE_ID + 1)# /home/bluecmd/Downloads/SAI/inc/saitam.h: 810

SAI_TAM_INT_ATTR_INGRESS_SAMPLEPACKET_ENABLE = (SAI_TAM_INT_ATTR_NAME_SPACE_ID_GLOBAL + 1)# /home/bluecmd/Downloads/SAI/inc/saitam.h: 810

SAI_TAM_INT_ATTR_COLLECTOR_LIST = (SAI_TAM_INT_ATTR_INGRESS_SAMPLEPACKET_ENABLE + 1)# /home/bluecmd/Downloads/SAI/inc/saitam.h: 810

SAI_TAM_INT_ATTR_MATH_FUNC = (SAI_TAM_INT_ATTR_COLLECTOR_LIST + 1)# /home/bluecmd/Downloads/SAI/inc/saitam.h: 810

SAI_TAM_INT_ATTR_REPORT_ID = (SAI_TAM_INT_ATTR_MATH_FUNC + 1)# /home/bluecmd/Downloads/SAI/inc/saitam.h: 810

SAI_TAM_INT_ATTR_END = (SAI_TAM_INT_ATTR_REPORT_ID + 1)# /home/bluecmd/Downloads/SAI/inc/saitam.h: 810

SAI_TAM_INT_ATTR_CUSTOM_RANGE_START = 0x10000000# /home/bluecmd/Downloads/SAI/inc/saitam.h: 810

SAI_TAM_INT_ATTR_CUSTOM_RANGE_END = (SAI_TAM_INT_ATTR_CUSTOM_RANGE_START + 1)# /home/bluecmd/Downloads/SAI/inc/saitam.h: 810

sai_tam_int_attr_t = enum__sai_tam_int_attr_t# /home/bluecmd/Downloads/SAI/inc/saitam.h: 810

sai_create_tam_int_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saitam.h: 822

sai_remove_tam_int_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t)# /home/bluecmd/Downloads/SAI/inc/saitam.h: 835

sai_get_tam_int_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saitam.h: 847

sai_set_tam_int_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saitam.h: 860

enum__sai_tam_telemetry_type_t = c_int# /home/bluecmd/Downloads/SAI/inc/saitam.h: 909

SAI_TAM_TELEMETRY_TYPE_NE = 0# /home/bluecmd/Downloads/SAI/inc/saitam.h: 909

SAI_TAM_TELEMETRY_TYPE_SWITCH = (SAI_TAM_TELEMETRY_TYPE_NE + 1)# /home/bluecmd/Downloads/SAI/inc/saitam.h: 909

SAI_TAM_TELEMETRY_TYPE_FABRIC = (SAI_TAM_TELEMETRY_TYPE_SWITCH + 1)# /home/bluecmd/Downloads/SAI/inc/saitam.h: 909

SAI_TAM_TELEMETRY_TYPE_FLOW = (SAI_TAM_TELEMETRY_TYPE_FABRIC + 1)# /home/bluecmd/Downloads/SAI/inc/saitam.h: 909

SAI_TAM_TELEMETRY_TYPE_INT = (SAI_TAM_TELEMETRY_TYPE_FLOW + 1)# /home/bluecmd/Downloads/SAI/inc/saitam.h: 909

SAI_TAM_TELEMETRY_TYPE_COUNTER_SUBSCRIPTION = (SAI_TAM_TELEMETRY_TYPE_INT + 1)# /home/bluecmd/Downloads/SAI/inc/saitam.h: 909

sai_tam_telemetry_type_t = enum__sai_tam_telemetry_type_t# /home/bluecmd/Downloads/SAI/inc/saitam.h: 909

enum__sai_tam_tel_type_attr_t = c_int# /home/bluecmd/Downloads/SAI/inc/saitam.h: 1087

SAI_TAM_TEL_TYPE_ATTR_START = 0# /home/bluecmd/Downloads/SAI/inc/saitam.h: 1087

SAI_TAM_TEL_TYPE_ATTR_TAM_TELEMETRY_TYPE = SAI_TAM_TEL_TYPE_ATTR_START# /home/bluecmd/Downloads/SAI/inc/saitam.h: 1087

SAI_TAM_TEL_TYPE_ATTR_INT_SWITCH_IDENTIFIER = (SAI_TAM_TEL_TYPE_ATTR_TAM_TELEMETRY_TYPE + 1)# /home/bluecmd/Downloads/SAI/inc/saitam.h: 1087

SAI_TAM_TEL_TYPE_ATTR_SWITCH_ENABLE_PORT_STATS = (SAI_TAM_TEL_TYPE_ATTR_INT_SWITCH_IDENTIFIER + 1)# /home/bluecmd/Downloads/SAI/inc/saitam.h: 1087

SAI_TAM_TEL_TYPE_ATTR_SWITCH_ENABLE_PORT_STATS_INGRESS = (SAI_TAM_TEL_TYPE_ATTR_SWITCH_ENABLE_PORT_STATS + 1)# /home/bluecmd/Downloads/SAI/inc/saitam.h: 1087

SAI_TAM_TEL_TYPE_ATTR_SWITCH_ENABLE_PORT_STATS_EGRESS = (SAI_TAM_TEL_TYPE_ATTR_SWITCH_ENABLE_PORT_STATS_INGRESS + 1)# /home/bluecmd/Downloads/SAI/inc/saitam.h: 1087

SAI_TAM_TEL_TYPE_ATTR_SWITCH_ENABLE_VIRTUAL_QUEUE_STATS = (SAI_TAM_TEL_TYPE_ATTR_SWITCH_ENABLE_PORT_STATS_EGRESS + 1)# /home/bluecmd/Downloads/SAI/inc/saitam.h: 1087

SAI_TAM_TEL_TYPE_ATTR_SWITCH_ENABLE_OUTPUT_QUEUE_STATS = (SAI_TAM_TEL_TYPE_ATTR_SWITCH_ENABLE_VIRTUAL_QUEUE_STATS + 1)# /home/bluecmd/Downloads/SAI/inc/saitam.h: 1087

SAI_TAM_TEL_TYPE_ATTR_SWITCH_ENABLE_MMU_STATS = (SAI_TAM_TEL_TYPE_ATTR_SWITCH_ENABLE_OUTPUT_QUEUE_STATS + 1)# /home/bluecmd/Downloads/SAI/inc/saitam.h: 1087

SAI_TAM_TEL_TYPE_ATTR_SWITCH_ENABLE_FABRIC_STATS = (SAI_TAM_TEL_TYPE_ATTR_SWITCH_ENABLE_MMU_STATS + 1)# /home/bluecmd/Downloads/SAI/inc/saitam.h: 1087

SAI_TAM_TEL_TYPE_ATTR_SWITCH_ENABLE_FILTER_STATS = (SAI_TAM_TEL_TYPE_ATTR_SWITCH_ENABLE_FABRIC_STATS + 1)# /home/bluecmd/Downloads/SAI/inc/saitam.h: 1087

SAI_TAM_TEL_TYPE_ATTR_SWITCH_ENABLE_RESOURCE_UTILIZATION_STATS = (SAI_TAM_TEL_TYPE_ATTR_SWITCH_ENABLE_FILTER_STATS + 1)# /home/bluecmd/Downloads/SAI/inc/saitam.h: 1087

SAI_TAM_TEL_TYPE_ATTR_FABRIC_Q = (SAI_TAM_TEL_TYPE_ATTR_SWITCH_ENABLE_RESOURCE_UTILIZATION_STATS + 1)# /home/bluecmd/Downloads/SAI/inc/saitam.h: 1087

SAI_TAM_TEL_TYPE_ATTR_NE_ENABLE = (SAI_TAM_TEL_TYPE_ATTR_FABRIC_Q + 1)# /home/bluecmd/Downloads/SAI/inc/saitam.h: 1087

SAI_TAM_TEL_TYPE_ATTR_DSCP_VALUE = (SAI_TAM_TEL_TYPE_ATTR_NE_ENABLE + 1)# /home/bluecmd/Downloads/SAI/inc/saitam.h: 1087

SAI_TAM_TEL_TYPE_ATTR_MATH_FUNC = (SAI_TAM_TEL_TYPE_ATTR_DSCP_VALUE + 1)# /home/bluecmd/Downloads/SAI/inc/saitam.h: 1087

SAI_TAM_TEL_TYPE_ATTR_REPORT_ID = (SAI_TAM_TEL_TYPE_ATTR_MATH_FUNC + 1)# /home/bluecmd/Downloads/SAI/inc/saitam.h: 1087

SAI_TAM_TEL_TYPE_ATTR_COUNTER_SUBSCRIPTION_LIST = (SAI_TAM_TEL_TYPE_ATTR_REPORT_ID + 1)# /home/bluecmd/Downloads/SAI/inc/saitam.h: 1087

SAI_TAM_TEL_TYPE_ATTR_END = (SAI_TAM_TEL_TYPE_ATTR_COUNTER_SUBSCRIPTION_LIST + 1)# /home/bluecmd/Downloads/SAI/inc/saitam.h: 1087

SAI_TAM_TEL_TYPE_ATTR_CUSTOM_RANGE_START = 0x10000000# /home/bluecmd/Downloads/SAI/inc/saitam.h: 1087

SAI_TAM_TEL_TYPE_ATTR_CUSTOM_RANGE_END = (SAI_TAM_TEL_TYPE_ATTR_CUSTOM_RANGE_START + 1)# /home/bluecmd/Downloads/SAI/inc/saitam.h: 1087

sai_tam_tel_type_attr_t = enum__sai_tam_tel_type_attr_t# /home/bluecmd/Downloads/SAI/inc/saitam.h: 1087

sai_create_tam_tel_type_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saitam.h: 1099

sai_remove_tam_tel_type_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t)# /home/bluecmd/Downloads/SAI/inc/saitam.h: 1112

sai_get_tam_tel_type_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saitam.h: 1124

sai_set_tam_tel_type_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saitam.h: 1137

enum__sai_tam_report_type_t = c_int# /home/bluecmd/Downloads/SAI/inc/saitam.h: 1185

SAI_TAM_REPORT_TYPE_SFLOW = 0# /home/bluecmd/Downloads/SAI/inc/saitam.h: 1185

SAI_TAM_REPORT_TYPE_IPFIX = (SAI_TAM_REPORT_TYPE_SFLOW + 1)# /home/bluecmd/Downloads/SAI/inc/saitam.h: 1185

SAI_TAM_REPORT_TYPE_PROTO = (SAI_TAM_REPORT_TYPE_IPFIX + 1)# /home/bluecmd/Downloads/SAI/inc/saitam.h: 1185

SAI_TAM_REPORT_TYPE_THRIFT = (SAI_TAM_REPORT_TYPE_PROTO + 1)# /home/bluecmd/Downloads/SAI/inc/saitam.h: 1185

SAI_TAM_REPORT_TYPE_JSON = (SAI_TAM_REPORT_TYPE_THRIFT + 1)# /home/bluecmd/Downloads/SAI/inc/saitam.h: 1185

SAI_TAM_REPORT_TYPE_P4_EXTN = (SAI_TAM_REPORT_TYPE_JSON + 1)# /home/bluecmd/Downloads/SAI/inc/saitam.h: 1185

SAI_TAM_REPORT_TYPE_HISTOGRAM = (SAI_TAM_REPORT_TYPE_P4_EXTN + 1)# /home/bluecmd/Downloads/SAI/inc/saitam.h: 1185

SAI_TAM_REPORT_TYPE_VENDOR_EXTN = (SAI_TAM_REPORT_TYPE_HISTOGRAM + 1)# /home/bluecmd/Downloads/SAI/inc/saitam.h: 1185

sai_tam_report_type_t = enum__sai_tam_report_type_t# /home/bluecmd/Downloads/SAI/inc/saitam.h: 1185

enum__sai_tam_report_mode_t = c_int# /home/bluecmd/Downloads/SAI/inc/saitam.h: 1198

SAI_TAM_REPORT_MODE_ALL = 0# /home/bluecmd/Downloads/SAI/inc/saitam.h: 1198

SAI_TAM_REPORT_MODE_BULK = (SAI_TAM_REPORT_MODE_ALL + 1)# /home/bluecmd/Downloads/SAI/inc/saitam.h: 1198

sai_tam_report_mode_t = enum__sai_tam_report_mode_t# /home/bluecmd/Downloads/SAI/inc/saitam.h: 1198

enum__sai_tam_report_interval_unit_t = c_int# /home/bluecmd/Downloads/SAI/inc/saitam.h: 1220

SAI_TAM_REPORT_INTERVAL_UNIT_NANOSEC = 0# /home/bluecmd/Downloads/SAI/inc/saitam.h: 1220

SAI_TAM_REPORT_INTERVAL_UNIT_USEC = (SAI_TAM_REPORT_INTERVAL_UNIT_NANOSEC + 1)# /home/bluecmd/Downloads/SAI/inc/saitam.h: 1220

SAI_TAM_REPORT_INTERVAL_UNIT_MSEC = (SAI_TAM_REPORT_INTERVAL_UNIT_USEC + 1)# /home/bluecmd/Downloads/SAI/inc/saitam.h: 1220

sai_tam_report_interval_unit_t = enum__sai_tam_report_interval_unit_t# /home/bluecmd/Downloads/SAI/inc/saitam.h: 1220

enum__sai_tam_report_attr_t = c_int# /home/bluecmd/Downloads/SAI/inc/saitam.h: 1336

SAI_TAM_REPORT_ATTR_START = 0# /home/bluecmd/Downloads/SAI/inc/saitam.h: 1336

SAI_TAM_REPORT_ATTR_TYPE = SAI_TAM_REPORT_ATTR_START# /home/bluecmd/Downloads/SAI/inc/saitam.h: 1336

SAI_TAM_REPORT_ATTR_HISTOGRAM_NUMBER_OF_BINS = (SAI_TAM_REPORT_ATTR_TYPE + 1)# /home/bluecmd/Downloads/SAI/inc/saitam.h: 1336

SAI_TAM_REPORT_ATTR_HISTOGRAM_BIN_BOUNDARY = (SAI_TAM_REPORT_ATTR_HISTOGRAM_NUMBER_OF_BINS + 1)# /home/bluecmd/Downloads/SAI/inc/saitam.h: 1336

SAI_TAM_REPORT_ATTR_QUOTA = (SAI_TAM_REPORT_ATTR_HISTOGRAM_BIN_BOUNDARY + 1)# /home/bluecmd/Downloads/SAI/inc/saitam.h: 1336

SAI_TAM_REPORT_ATTR_REPORT_MODE = (SAI_TAM_REPORT_ATTR_QUOTA + 1)# /home/bluecmd/Downloads/SAI/inc/saitam.h: 1336

SAI_TAM_REPORT_ATTR_REPORT_INTERVAL = (SAI_TAM_REPORT_ATTR_REPORT_MODE + 1)# /home/bluecmd/Downloads/SAI/inc/saitam.h: 1336

SAI_TAM_REPORT_ATTR_ENTERPRISE_NUMBER = (SAI_TAM_REPORT_ATTR_REPORT_INTERVAL + 1)# /home/bluecmd/Downloads/SAI/inc/saitam.h: 1336

SAI_TAM_REPORT_ATTR_TEMPLATE_REPORT_INTERVAL = (SAI_TAM_REPORT_ATTR_ENTERPRISE_NUMBER + 1)# /home/bluecmd/Downloads/SAI/inc/saitam.h: 1336

SAI_TAM_REPORT_ATTR_REPORT_INTERVAL_UNIT = (SAI_TAM_REPORT_ATTR_TEMPLATE_REPORT_INTERVAL + 1)# /home/bluecmd/Downloads/SAI/inc/saitam.h: 1336

SAI_TAM_REPORT_ATTR_END = (SAI_TAM_REPORT_ATTR_REPORT_INTERVAL_UNIT + 1)# /home/bluecmd/Downloads/SAI/inc/saitam.h: 1336

SAI_TAM_REPORT_ATTR_CUSTOM_RANGE_START = 0x10000000# /home/bluecmd/Downloads/SAI/inc/saitam.h: 1336

SAI_TAM_REPORT_ATTR_CUSTOM_RANGE_END = (SAI_TAM_REPORT_ATTR_CUSTOM_RANGE_START + 1)# /home/bluecmd/Downloads/SAI/inc/saitam.h: 1336

sai_tam_report_attr_t = enum__sai_tam_report_attr_t# /home/bluecmd/Downloads/SAI/inc/saitam.h: 1336

sai_create_tam_report_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saitam.h: 1348

sai_remove_tam_report_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t)# /home/bluecmd/Downloads/SAI/inc/saitam.h: 1361

sai_get_tam_report_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saitam.h: 1373

sai_set_tam_report_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saitam.h: 1386

enum__sai_tam_reporting_unit_t = c_int# /home/bluecmd/Downloads/SAI/inc/saitam.h: 1415

SAI_TAM_REPORTING_UNIT_SEC = 0# /home/bluecmd/Downloads/SAI/inc/saitam.h: 1415

SAI_TAM_REPORTING_UNIT_MINUTE = (SAI_TAM_REPORTING_UNIT_SEC + 1)# /home/bluecmd/Downloads/SAI/inc/saitam.h: 1415

SAI_TAM_REPORTING_UNIT_HOUR = (SAI_TAM_REPORTING_UNIT_MINUTE + 1)# /home/bluecmd/Downloads/SAI/inc/saitam.h: 1415

SAI_TAM_REPORTING_UNIT_DAY = (SAI_TAM_REPORTING_UNIT_HOUR + 1)# /home/bluecmd/Downloads/SAI/inc/saitam.h: 1415

sai_tam_reporting_unit_t = enum__sai_tam_reporting_unit_t# /home/bluecmd/Downloads/SAI/inc/saitam.h: 1415

enum__sai_tam_telemetry_attr_t = c_int# /home/bluecmd/Downloads/SAI/inc/saitam.h: 1477

SAI_TAM_TELEMETRY_ATTR_START = 0# /home/bluecmd/Downloads/SAI/inc/saitam.h: 1477

SAI_TAM_TELEMETRY_ATTR_TAM_TYPE_LIST = SAI_TAM_TELEMETRY_ATTR_START# /home/bluecmd/Downloads/SAI/inc/saitam.h: 1477

SAI_TAM_TELEMETRY_ATTR_COLLECTOR_LIST = (SAI_TAM_TELEMETRY_ATTR_TAM_TYPE_LIST + 1)# /home/bluecmd/Downloads/SAI/inc/saitam.h: 1477

SAI_TAM_TELEMETRY_ATTR_TAM_REPORTING_UNIT = (SAI_TAM_TELEMETRY_ATTR_COLLECTOR_LIST + 1)# /home/bluecmd/Downloads/SAI/inc/saitam.h: 1477

SAI_TAM_TELEMETRY_ATTR_REPORTING_INTERVAL = (SAI_TAM_TELEMETRY_ATTR_TAM_REPORTING_UNIT + 1)# /home/bluecmd/Downloads/SAI/inc/saitam.h: 1477

SAI_TAM_TELEMETRY_ATTR_END = (SAI_TAM_TELEMETRY_ATTR_REPORTING_INTERVAL + 1)# /home/bluecmd/Downloads/SAI/inc/saitam.h: 1477

SAI_TAM_TELEMETRY_ATTR_CUSTOM_RANGE_START = 0x10000000# /home/bluecmd/Downloads/SAI/inc/saitam.h: 1477

SAI_TAM_TELEMETRY_ATTR_CUSTOM_RANGE_END = (SAI_TAM_TELEMETRY_ATTR_CUSTOM_RANGE_START + 1)# /home/bluecmd/Downloads/SAI/inc/saitam.h: 1477

sai_tam_telemetry_attr_t = enum__sai_tam_telemetry_attr_t# /home/bluecmd/Downloads/SAI/inc/saitam.h: 1477

sai_create_tam_telemetry_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saitam.h: 1489

sai_remove_tam_telemetry_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t)# /home/bluecmd/Downloads/SAI/inc/saitam.h: 1502

sai_get_tam_telemetry_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saitam.h: 1514

sai_set_tam_telemetry_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saitam.h: 1527

enum__sai_tam_transport_type_t = c_int# /home/bluecmd/Downloads/SAI/inc/saitam.h: 1561

SAI_TAM_TRANSPORT_TYPE_NONE = 0# /home/bluecmd/Downloads/SAI/inc/saitam.h: 1561

SAI_TAM_TRANSPORT_TYPE_TCP = (SAI_TAM_TRANSPORT_TYPE_NONE + 1)# /home/bluecmd/Downloads/SAI/inc/saitam.h: 1561

SAI_TAM_TRANSPORT_TYPE_UDP = (SAI_TAM_TRANSPORT_TYPE_TCP + 1)# /home/bluecmd/Downloads/SAI/inc/saitam.h: 1561

SAI_TAM_TRANSPORT_TYPE_GRPC = (SAI_TAM_TRANSPORT_TYPE_UDP + 1)# /home/bluecmd/Downloads/SAI/inc/saitam.h: 1561

SAI_TAM_TRANSPORT_TYPE_MIRROR = (SAI_TAM_TRANSPORT_TYPE_GRPC + 1)# /home/bluecmd/Downloads/SAI/inc/saitam.h: 1561

sai_tam_transport_type_t = enum__sai_tam_transport_type_t# /home/bluecmd/Downloads/SAI/inc/saitam.h: 1561

enum__sai_tam_transport_auth_type_t = c_int# /home/bluecmd/Downloads/SAI/inc/saitam.h: 1583

SAI_TAM_TRANSPORT_AUTH_TYPE_NONE = 0# /home/bluecmd/Downloads/SAI/inc/saitam.h: 1583

SAI_TAM_TRANSPORT_AUTH_TYPE_SSL = (SAI_TAM_TRANSPORT_AUTH_TYPE_NONE + 1)# /home/bluecmd/Downloads/SAI/inc/saitam.h: 1583

SAI_TAM_TRANSPORT_AUTH_TYPE_TLS = (SAI_TAM_TRANSPORT_AUTH_TYPE_SSL + 1)# /home/bluecmd/Downloads/SAI/inc/saitam.h: 1583

sai_tam_transport_auth_type_t = enum__sai_tam_transport_auth_type_t# /home/bluecmd/Downloads/SAI/inc/saitam.h: 1583

enum__sai_tam_transport_attr_t = c_int# /home/bluecmd/Downloads/SAI/inc/saitam.h: 1653

SAI_TAM_TRANSPORT_ATTR_START = 0# /home/bluecmd/Downloads/SAI/inc/saitam.h: 1653

SAI_TAM_TRANSPORT_ATTR_TRANSPORT_TYPE = SAI_TAM_TRANSPORT_ATTR_START# /home/bluecmd/Downloads/SAI/inc/saitam.h: 1653

SAI_TAM_TRANSPORT_ATTR_SRC_PORT = (SAI_TAM_TRANSPORT_ATTR_TRANSPORT_TYPE + 1)# /home/bluecmd/Downloads/SAI/inc/saitam.h: 1653

SAI_TAM_TRANSPORT_ATTR_DST_PORT = (SAI_TAM_TRANSPORT_ATTR_SRC_PORT + 1)# /home/bluecmd/Downloads/SAI/inc/saitam.h: 1653

SAI_TAM_TRANSPORT_ATTR_TRANSPORT_AUTH_TYPE = (SAI_TAM_TRANSPORT_ATTR_DST_PORT + 1)# /home/bluecmd/Downloads/SAI/inc/saitam.h: 1653

SAI_TAM_TRANSPORT_ATTR_MTU = (SAI_TAM_TRANSPORT_ATTR_TRANSPORT_AUTH_TYPE + 1)# /home/bluecmd/Downloads/SAI/inc/saitam.h: 1653

SAI_TAM_TRANSPORT_ATTR_END = (SAI_TAM_TRANSPORT_ATTR_MTU + 1)# /home/bluecmd/Downloads/SAI/inc/saitam.h: 1653

SAI_TAM_TRANSPORT_ATTR_CUSTOM_RANGE_START = 0x10000000# /home/bluecmd/Downloads/SAI/inc/saitam.h: 1653

SAI_TAM_TRANSPORT_ATTR_CUSTOM_RANGE_END = (SAI_TAM_TRANSPORT_ATTR_CUSTOM_RANGE_START + 1)# /home/bluecmd/Downloads/SAI/inc/saitam.h: 1653

sai_tam_transport_attr_t = enum__sai_tam_transport_attr_t# /home/bluecmd/Downloads/SAI/inc/saitam.h: 1653

sai_create_tam_transport_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saitam.h: 1665

sai_remove_tam_transport_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t)# /home/bluecmd/Downloads/SAI/inc/saitam.h: 1678

sai_get_tam_transport_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saitam.h: 1690

sai_set_tam_transport_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saitam.h: 1703

enum__sai_tam_collector_attr_t = c_int# /home/bluecmd/Downloads/SAI/inc/saitam.h: 1797

SAI_TAM_COLLECTOR_ATTR_START = 0# /home/bluecmd/Downloads/SAI/inc/saitam.h: 1797

SAI_TAM_COLLECTOR_ATTR_SRC_IP = SAI_TAM_COLLECTOR_ATTR_START# /home/bluecmd/Downloads/SAI/inc/saitam.h: 1797

SAI_TAM_COLLECTOR_ATTR_DST_IP = (SAI_TAM_COLLECTOR_ATTR_SRC_IP + 1)# /home/bluecmd/Downloads/SAI/inc/saitam.h: 1797

SAI_TAM_COLLECTOR_ATTR_LOCALHOST = (SAI_TAM_COLLECTOR_ATTR_DST_IP + 1)# /home/bluecmd/Downloads/SAI/inc/saitam.h: 1797

SAI_TAM_COLLECTOR_ATTR_VIRTUAL_ROUTER_ID = (SAI_TAM_COLLECTOR_ATTR_LOCALHOST + 1)# /home/bluecmd/Downloads/SAI/inc/saitam.h: 1797

SAI_TAM_COLLECTOR_ATTR_TRUNCATE_SIZE = (SAI_TAM_COLLECTOR_ATTR_VIRTUAL_ROUTER_ID + 1)# /home/bluecmd/Downloads/SAI/inc/saitam.h: 1797

SAI_TAM_COLLECTOR_ATTR_TRANSPORT = (SAI_TAM_COLLECTOR_ATTR_TRUNCATE_SIZE + 1)# /home/bluecmd/Downloads/SAI/inc/saitam.h: 1797

SAI_TAM_COLLECTOR_ATTR_DSCP_VALUE = (SAI_TAM_COLLECTOR_ATTR_TRANSPORT + 1)# /home/bluecmd/Downloads/SAI/inc/saitam.h: 1797

SAI_TAM_COLLECTOR_ATTR_END = (SAI_TAM_COLLECTOR_ATTR_DSCP_VALUE + 1)# /home/bluecmd/Downloads/SAI/inc/saitam.h: 1797

SAI_TAM_COLLECTOR_ATTR_CUSTOM_RANGE_START = 0x10000000# /home/bluecmd/Downloads/SAI/inc/saitam.h: 1797

SAI_TAM_COLLECTOR_ATTR_CUSTOM_RANGE_END = (SAI_TAM_COLLECTOR_ATTR_CUSTOM_RANGE_START + 1)# /home/bluecmd/Downloads/SAI/inc/saitam.h: 1797

sai_tam_collector_attr_t = enum__sai_tam_collector_attr_t# /home/bluecmd/Downloads/SAI/inc/saitam.h: 1797

sai_create_tam_collector_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saitam.h: 1809

sai_remove_tam_collector_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t)# /home/bluecmd/Downloads/SAI/inc/saitam.h: 1822

sai_get_tam_collector_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saitam.h: 1834

sai_set_tam_collector_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saitam.h: 1847

enum__sai_tam_event_type_t = c_int# /home/bluecmd/Downloads/SAI/inc/saitam.h: 1915

SAI_TAM_EVENT_TYPE_FLOW_STATE = 0# /home/bluecmd/Downloads/SAI/inc/saitam.h: 1915

SAI_TAM_EVENT_TYPE_FLOW_WATCHLIST = (SAI_TAM_EVENT_TYPE_FLOW_STATE + 1)# /home/bluecmd/Downloads/SAI/inc/saitam.h: 1915

SAI_TAM_EVENT_TYPE_FLOW_TCPFLAG = (SAI_TAM_EVENT_TYPE_FLOW_WATCHLIST + 1)# /home/bluecmd/Downloads/SAI/inc/saitam.h: 1915

SAI_TAM_EVENT_TYPE_QUEUE_THRESHOLD = (SAI_TAM_EVENT_TYPE_FLOW_TCPFLAG + 1)# /home/bluecmd/Downloads/SAI/inc/saitam.h: 1915

SAI_TAM_EVENT_TYPE_QUEUE_TAIL_DROP = (SAI_TAM_EVENT_TYPE_QUEUE_THRESHOLD + 1)# /home/bluecmd/Downloads/SAI/inc/saitam.h: 1915

SAI_TAM_EVENT_TYPE_PACKET_DROP = (SAI_TAM_EVENT_TYPE_QUEUE_TAIL_DROP + 1)# /home/bluecmd/Downloads/SAI/inc/saitam.h: 1915

SAI_TAM_EVENT_TYPE_RESOURCE_UTILIZATION = (SAI_TAM_EVENT_TYPE_PACKET_DROP + 1)# /home/bluecmd/Downloads/SAI/inc/saitam.h: 1915

SAI_TAM_EVENT_TYPE_IPG_SHARED = (SAI_TAM_EVENT_TYPE_RESOURCE_UTILIZATION + 1)# /home/bluecmd/Downloads/SAI/inc/saitam.h: 1915

SAI_TAM_EVENT_TYPE_IPG_XOFF_ROOM = (SAI_TAM_EVENT_TYPE_IPG_SHARED + 1)# /home/bluecmd/Downloads/SAI/inc/saitam.h: 1915

SAI_TAM_EVENT_TYPE_BSP = (SAI_TAM_EVENT_TYPE_IPG_XOFF_ROOM + 1)# /home/bluecmd/Downloads/SAI/inc/saitam.h: 1915

sai_tam_event_type_t = enum__sai_tam_event_type_t# /home/bluecmd/Downloads/SAI/inc/saitam.h: 1915

enum__sai_tam_event_action_attr_t = c_int# /home/bluecmd/Downloads/SAI/inc/saitam.h: 1956

SAI_TAM_EVENT_ACTION_ATTR_START = 0# /home/bluecmd/Downloads/SAI/inc/saitam.h: 1956

SAI_TAM_EVENT_ACTION_ATTR_REPORT_TYPE = SAI_TAM_EVENT_ACTION_ATTR_START# /home/bluecmd/Downloads/SAI/inc/saitam.h: 1956

SAI_TAM_EVENT_ACTION_ATTR_QOS_ACTION_TYPE = (SAI_TAM_EVENT_ACTION_ATTR_REPORT_TYPE + 1)# /home/bluecmd/Downloads/SAI/inc/saitam.h: 1956

SAI_TAM_EVENT_ACTION_ATTR_END = (SAI_TAM_EVENT_ACTION_ATTR_QOS_ACTION_TYPE + 1)# /home/bluecmd/Downloads/SAI/inc/saitam.h: 1956

SAI_TAM_EVENT_ACTION_ATTR_CUSTOM_RANGE_START = 0x10000000# /home/bluecmd/Downloads/SAI/inc/saitam.h: 1956

SAI_TAM_EVENT_ACTION_ATTR_CUSTOM_RANGE_END = (SAI_TAM_EVENT_ACTION_ATTR_CUSTOM_RANGE_START + 1)# /home/bluecmd/Downloads/SAI/inc/saitam.h: 1956

sai_tam_event_action_attr_t = enum__sai_tam_event_action_attr_t# /home/bluecmd/Downloads/SAI/inc/saitam.h: 1956

sai_create_tam_event_action_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saitam.h: 1968

sai_remove_tam_event_action_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t)# /home/bluecmd/Downloads/SAI/inc/saitam.h: 1981

sai_get_tam_event_action_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saitam.h: 1993

sai_set_tam_event_action_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saitam.h: 2006

enum__sai_tam_event_attr_t = c_int# /home/bluecmd/Downloads/SAI/inc/saitam.h: 2077

SAI_TAM_EVENT_ATTR_START = 0# /home/bluecmd/Downloads/SAI/inc/saitam.h: 2077

SAI_TAM_EVENT_ATTR_TYPE = SAI_TAM_EVENT_ATTR_START# /home/bluecmd/Downloads/SAI/inc/saitam.h: 2077

SAI_TAM_EVENT_ATTR_ACTION_LIST = (SAI_TAM_EVENT_ATTR_TYPE + 1)# /home/bluecmd/Downloads/SAI/inc/saitam.h: 2077

SAI_TAM_EVENT_ATTR_COLLECTOR_LIST = (SAI_TAM_EVENT_ATTR_ACTION_LIST + 1)# /home/bluecmd/Downloads/SAI/inc/saitam.h: 2077

SAI_TAM_EVENT_ATTR_THRESHOLD = (SAI_TAM_EVENT_ATTR_COLLECTOR_LIST + 1)# /home/bluecmd/Downloads/SAI/inc/saitam.h: 2077

SAI_TAM_EVENT_ATTR_DSCP_VALUE = (SAI_TAM_EVENT_ATTR_THRESHOLD + 1)# /home/bluecmd/Downloads/SAI/inc/saitam.h: 2077

SAI_TAM_EVENT_ATTR_END = (SAI_TAM_EVENT_ATTR_DSCP_VALUE + 1)# /home/bluecmd/Downloads/SAI/inc/saitam.h: 2077

SAI_TAM_EVENT_ATTR_CUSTOM_RANGE_START = 0x10000000# /home/bluecmd/Downloads/SAI/inc/saitam.h: 2077

SAI_TAM_EVENT_ATTR_CUSTOM_RANGE_END = (SAI_TAM_EVENT_ATTR_CUSTOM_RANGE_START + 1)# /home/bluecmd/Downloads/SAI/inc/saitam.h: 2077

sai_tam_event_attr_t = enum__sai_tam_event_attr_t# /home/bluecmd/Downloads/SAI/inc/saitam.h: 2077

sai_create_tam_event_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saitam.h: 2089

sai_remove_tam_event_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t)# /home/bluecmd/Downloads/SAI/inc/saitam.h: 2102

sai_get_tam_event_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saitam.h: 2114

sai_set_tam_event_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saitam.h: 2127

enum__sai_tam_counter_subscription_attr_t = c_int# /home/bluecmd/Downloads/SAI/inc/saitam.h: 2189

SAI_TAM_COUNTER_SUBSCRIPTION_ATTR_START = 0# /home/bluecmd/Downloads/SAI/inc/saitam.h: 2189

SAI_TAM_COUNTER_SUBSCRIPTION_ATTR_TEL_TYPE = SAI_TAM_COUNTER_SUBSCRIPTION_ATTR_START# /home/bluecmd/Downloads/SAI/inc/saitam.h: 2189

SAI_TAM_COUNTER_SUBSCRIPTION_ATTR_OBJECT_ID = (SAI_TAM_COUNTER_SUBSCRIPTION_ATTR_TEL_TYPE + 1)# /home/bluecmd/Downloads/SAI/inc/saitam.h: 2189

SAI_TAM_COUNTER_SUBSCRIPTION_ATTR_STAT_ID = (SAI_TAM_COUNTER_SUBSCRIPTION_ATTR_OBJECT_ID + 1)# /home/bluecmd/Downloads/SAI/inc/saitam.h: 2189

SAI_TAM_COUNTER_SUBSCRIPTION_ATTR_LABEL = (SAI_TAM_COUNTER_SUBSCRIPTION_ATTR_STAT_ID + 1)# /home/bluecmd/Downloads/SAI/inc/saitam.h: 2189

SAI_TAM_COUNTER_SUBSCRIPTION_ATTR_END = (SAI_TAM_COUNTER_SUBSCRIPTION_ATTR_LABEL + 1)# /home/bluecmd/Downloads/SAI/inc/saitam.h: 2189

SAI_TAM_COUNTER_SUBSCRIPTION_ATTR_CUSTOM_RANGE_START = 0x10000000# /home/bluecmd/Downloads/SAI/inc/saitam.h: 2189

SAI_TAM_COUNTER_SUBSCRIPTION_ATTR_CUSTOM_RANGE_END = (SAI_TAM_COUNTER_SUBSCRIPTION_ATTR_CUSTOM_RANGE_START + 1)# /home/bluecmd/Downloads/SAI/inc/saitam.h: 2189

sai_tam_counter_subscription_attr_t = enum__sai_tam_counter_subscription_attr_t# /home/bluecmd/Downloads/SAI/inc/saitam.h: 2189

sai_create_tam_counter_subscription_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saitam.h: 2201

sai_remove_tam_counter_subscription_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t)# /home/bluecmd/Downloads/SAI/inc/saitam.h: 2214

sai_set_tam_counter_subscription_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saitam.h: 2225

sai_get_tam_counter_subscription_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saitam.h: 2238

sai_tam_event_notification_fn = CFUNCTYPE(UNCHECKED(None), sai_object_id_t, sai_size_t, POINTER(None), uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saitam.h: 2257

# /home/bluecmd/Downloads/SAI/inc/saitam.h: 2275
for _lib in _libs.values():
    if not _lib.has("sai_tam_telemetry_get_data", "cdecl"):
        continue
    sai_tam_telemetry_get_data = _lib.get("sai_tam_telemetry_get_data", "cdecl")
    sai_tam_telemetry_get_data.argtypes = [sai_object_id_t, sai_object_list_t, c_bool, POINTER(sai_size_t), POINTER(None)]
    sai_tam_telemetry_get_data.restype = sai_status_t
    break

# /home/bluecmd/Downloads/SAI/inc/saitam.h: 2349
class struct__sai_tam_api_t(Structure):
    pass

struct__sai_tam_api_t.__slots__ = [
    'create_tam',
    'remove_tam',
    'set_tam_attribute',
    'get_tam_attribute',
    'create_tam_math_func',
    'remove_tam_math_func',
    'set_tam_math_func_attribute',
    'get_tam_math_func_attribute',
    'create_tam_report',
    'remove_tam_report',
    'set_tam_report_attribute',
    'get_tam_report_attribute',
    'create_tam_event_threshold',
    'remove_tam_event_threshold',
    'set_tam_event_threshold_attribute',
    'get_tam_event_threshold_attribute',
    'create_tam_int',
    'remove_tam_int',
    'set_tam_int_attribute',
    'get_tam_int_attribute',
    'create_tam_tel_type',
    'remove_tam_tel_type',
    'set_tam_tel_type_attribute',
    'get_tam_tel_type_attribute',
    'create_tam_transport',
    'remove_tam_transport',
    'set_tam_transport_attribute',
    'get_tam_transport_attribute',
    'create_tam_telemetry',
    'remove_tam_telemetry',
    'set_tam_telemetry_attribute',
    'get_tam_telemetry_attribute',
    'create_tam_collector',
    'remove_tam_collector',
    'set_tam_collector_attribute',
    'get_tam_collector_attribute',
    'create_tam_event_action',
    'remove_tam_event_action',
    'set_tam_event_action_attribute',
    'get_tam_event_action_attribute',
    'create_tam_event',
    'remove_tam_event',
    'set_tam_event_attribute',
    'get_tam_event_attribute',
    'create_tam_counter_subscription',
    'remove_tam_counter_subscription',
    'set_tam_counter_subscription_attribute',
    'get_tam_counter_subscription_attribute',
]
struct__sai_tam_api_t._fields_ = [
    ('create_tam', sai_create_tam_fn),
    ('remove_tam', sai_remove_tam_fn),
    ('set_tam_attribute', sai_set_tam_attribute_fn),
    ('get_tam_attribute', sai_get_tam_attribute_fn),
    ('create_tam_math_func', sai_create_tam_math_func_fn),
    ('remove_tam_math_func', sai_remove_tam_math_func_fn),
    ('set_tam_math_func_attribute', sai_set_tam_math_func_attribute_fn),
    ('get_tam_math_func_attribute', sai_get_tam_math_func_attribute_fn),
    ('create_tam_report', sai_create_tam_report_fn),
    ('remove_tam_report', sai_remove_tam_report_fn),
    ('set_tam_report_attribute', sai_set_tam_report_attribute_fn),
    ('get_tam_report_attribute', sai_get_tam_report_attribute_fn),
    ('create_tam_event_threshold', sai_create_tam_event_threshold_fn),
    ('remove_tam_event_threshold', sai_remove_tam_event_threshold_fn),
    ('set_tam_event_threshold_attribute', sai_set_tam_event_threshold_attribute_fn),
    ('get_tam_event_threshold_attribute', sai_get_tam_event_threshold_attribute_fn),
    ('create_tam_int', sai_create_tam_int_fn),
    ('remove_tam_int', sai_remove_tam_int_fn),
    ('set_tam_int_attribute', sai_set_tam_int_attribute_fn),
    ('get_tam_int_attribute', sai_get_tam_int_attribute_fn),
    ('create_tam_tel_type', sai_create_tam_tel_type_fn),
    ('remove_tam_tel_type', sai_remove_tam_tel_type_fn),
    ('set_tam_tel_type_attribute', sai_set_tam_tel_type_attribute_fn),
    ('get_tam_tel_type_attribute', sai_get_tam_tel_type_attribute_fn),
    ('create_tam_transport', sai_create_tam_transport_fn),
    ('remove_tam_transport', sai_remove_tam_transport_fn),
    ('set_tam_transport_attribute', sai_set_tam_transport_attribute_fn),
    ('get_tam_transport_attribute', sai_get_tam_transport_attribute_fn),
    ('create_tam_telemetry', sai_create_tam_telemetry_fn),
    ('remove_tam_telemetry', sai_remove_tam_telemetry_fn),
    ('set_tam_telemetry_attribute', sai_set_tam_telemetry_attribute_fn),
    ('get_tam_telemetry_attribute', sai_get_tam_telemetry_attribute_fn),
    ('create_tam_collector', sai_create_tam_collector_fn),
    ('remove_tam_collector', sai_remove_tam_collector_fn),
    ('set_tam_collector_attribute', sai_set_tam_collector_attribute_fn),
    ('get_tam_collector_attribute', sai_get_tam_collector_attribute_fn),
    ('create_tam_event_action', sai_create_tam_event_action_fn),
    ('remove_tam_event_action', sai_remove_tam_event_action_fn),
    ('set_tam_event_action_attribute', sai_set_tam_event_action_attribute_fn),
    ('get_tam_event_action_attribute', sai_get_tam_event_action_attribute_fn),
    ('create_tam_event', sai_create_tam_event_fn),
    ('remove_tam_event', sai_remove_tam_event_fn),
    ('set_tam_event_attribute', sai_set_tam_event_attribute_fn),
    ('get_tam_event_attribute', sai_get_tam_event_attribute_fn),
    ('create_tam_counter_subscription', sai_create_tam_counter_subscription_fn),
    ('remove_tam_counter_subscription', sai_remove_tam_counter_subscription_fn),
    ('set_tam_counter_subscription_attribute', sai_set_tam_counter_subscription_attribute_fn),
    ('get_tam_counter_subscription_attribute', sai_get_tam_counter_subscription_attribute_fn),
]

sai_tam_api_t = struct__sai_tam_api_t# /home/bluecmd/Downloads/SAI/inc/saitam.h: 2349

enum__sai_tunnel_map_type_t = c_int# /home/bluecmd/Downloads/SAI/inc/saitunnel.h: 86

SAI_TUNNEL_MAP_TYPE_OECN_TO_UECN = 0x00000000# /home/bluecmd/Downloads/SAI/inc/saitunnel.h: 86

SAI_TUNNEL_MAP_TYPE_UECN_OECN_TO_OECN = 0x00000001# /home/bluecmd/Downloads/SAI/inc/saitunnel.h: 86

SAI_TUNNEL_MAP_TYPE_VNI_TO_VLAN_ID = 0x00000002# /home/bluecmd/Downloads/SAI/inc/saitunnel.h: 86

SAI_TUNNEL_MAP_TYPE_VLAN_ID_TO_VNI = 0x00000003# /home/bluecmd/Downloads/SAI/inc/saitunnel.h: 86

SAI_TUNNEL_MAP_TYPE_VNI_TO_BRIDGE_IF = 0x00000004# /home/bluecmd/Downloads/SAI/inc/saitunnel.h: 86

SAI_TUNNEL_MAP_TYPE_BRIDGE_IF_TO_VNI = 0x00000005# /home/bluecmd/Downloads/SAI/inc/saitunnel.h: 86

SAI_TUNNEL_MAP_TYPE_VNI_TO_VIRTUAL_ROUTER_ID = 0x00000006# /home/bluecmd/Downloads/SAI/inc/saitunnel.h: 86

SAI_TUNNEL_MAP_TYPE_VIRTUAL_ROUTER_ID_TO_VNI = 0x00000007# /home/bluecmd/Downloads/SAI/inc/saitunnel.h: 86

SAI_TUNNEL_MAP_TYPE_VSID_TO_VLAN_ID = 0x00000008# /home/bluecmd/Downloads/SAI/inc/saitunnel.h: 86

SAI_TUNNEL_MAP_TYPE_VLAN_ID_TO_VSID = 0x00000009# /home/bluecmd/Downloads/SAI/inc/saitunnel.h: 86

SAI_TUNNEL_MAP_TYPE_VSID_TO_BRIDGE_IF = 0x0000000a# /home/bluecmd/Downloads/SAI/inc/saitunnel.h: 86

SAI_TUNNEL_MAP_TYPE_BRIDGE_IF_TO_VSID = 0x0000000b# /home/bluecmd/Downloads/SAI/inc/saitunnel.h: 86

SAI_TUNNEL_MAP_TYPE_VIRTUAL_ROUTER_ID_TO_VPN_SID = 0x0000000c# /home/bluecmd/Downloads/SAI/inc/saitunnel.h: 86

SAI_TUNNEL_MAP_TYPE_PREFIX_AGG_ID_TO_SRV6_VPN_SID = 0x0000000d# /home/bluecmd/Downloads/SAI/inc/saitunnel.h: 86

SAI_TUNNEL_MAP_TYPE_CUSTOM_RANGE_BASE = 0x10000000# /home/bluecmd/Downloads/SAI/inc/saitunnel.h: 86

sai_tunnel_map_type_t = enum__sai_tunnel_map_type_t# /home/bluecmd/Downloads/SAI/inc/saitunnel.h: 86

enum__sai_tunnel_map_entry_attr_t = c_int# /home/bluecmd/Downloads/SAI/inc/saitunnel.h: 273

SAI_TUNNEL_MAP_ENTRY_ATTR_START = 0x00000000# /home/bluecmd/Downloads/SAI/inc/saitunnel.h: 273

SAI_TUNNEL_MAP_ENTRY_ATTR_TUNNEL_MAP_TYPE = SAI_TUNNEL_MAP_ENTRY_ATTR_START# /home/bluecmd/Downloads/SAI/inc/saitunnel.h: 273

SAI_TUNNEL_MAP_ENTRY_ATTR_TUNNEL_MAP = 0x00000001# /home/bluecmd/Downloads/SAI/inc/saitunnel.h: 273

SAI_TUNNEL_MAP_ENTRY_ATTR_OECN_KEY = 0x00000002# /home/bluecmd/Downloads/SAI/inc/saitunnel.h: 273

SAI_TUNNEL_MAP_ENTRY_ATTR_OECN_VALUE = 0x00000003# /home/bluecmd/Downloads/SAI/inc/saitunnel.h: 273

SAI_TUNNEL_MAP_ENTRY_ATTR_UECN_KEY = 0x00000004# /home/bluecmd/Downloads/SAI/inc/saitunnel.h: 273

SAI_TUNNEL_MAP_ENTRY_ATTR_UECN_VALUE = 0x00000005# /home/bluecmd/Downloads/SAI/inc/saitunnel.h: 273

SAI_TUNNEL_MAP_ENTRY_ATTR_VLAN_ID_KEY = 0x00000006# /home/bluecmd/Downloads/SAI/inc/saitunnel.h: 273

SAI_TUNNEL_MAP_ENTRY_ATTR_VLAN_ID_VALUE = 0x00000007# /home/bluecmd/Downloads/SAI/inc/saitunnel.h: 273

SAI_TUNNEL_MAP_ENTRY_ATTR_VNI_ID_KEY = 0x00000008# /home/bluecmd/Downloads/SAI/inc/saitunnel.h: 273

SAI_TUNNEL_MAP_ENTRY_ATTR_VNI_ID_VALUE = 0x00000009# /home/bluecmd/Downloads/SAI/inc/saitunnel.h: 273

SAI_TUNNEL_MAP_ENTRY_ATTR_BRIDGE_ID_KEY = 0x0000000a# /home/bluecmd/Downloads/SAI/inc/saitunnel.h: 273

SAI_TUNNEL_MAP_ENTRY_ATTR_BRIDGE_ID_VALUE = 0x0000000b# /home/bluecmd/Downloads/SAI/inc/saitunnel.h: 273

SAI_TUNNEL_MAP_ENTRY_ATTR_VIRTUAL_ROUTER_ID_KEY = 0x0000000c# /home/bluecmd/Downloads/SAI/inc/saitunnel.h: 273

SAI_TUNNEL_MAP_ENTRY_ATTR_VIRTUAL_ROUTER_ID_VALUE = 0x0000000d# /home/bluecmd/Downloads/SAI/inc/saitunnel.h: 273

SAI_TUNNEL_MAP_ENTRY_ATTR_VSID_ID_KEY = 0x0000000e# /home/bluecmd/Downloads/SAI/inc/saitunnel.h: 273

SAI_TUNNEL_MAP_ENTRY_ATTR_VSID_ID_VALUE = 0x0000000f# /home/bluecmd/Downloads/SAI/inc/saitunnel.h: 273

SAI_TUNNEL_MAP_ENTRY_ATTR_PREFIX_AGG_ID_KEY = 0x00000010# /home/bluecmd/Downloads/SAI/inc/saitunnel.h: 273

SAI_TUNNEL_MAP_ENTRY_ATTR_SRV6_VPN_SID_VALUE = 0x00000011# /home/bluecmd/Downloads/SAI/inc/saitunnel.h: 273

SAI_TUNNEL_MAP_ENTRY_ATTR_END = (SAI_TUNNEL_MAP_ENTRY_ATTR_SRV6_VPN_SID_VALUE + 1)# /home/bluecmd/Downloads/SAI/inc/saitunnel.h: 273

SAI_TUNNEL_MAP_ENTRY_ATTR_CUSTOM_RANGE_START = 0x10000000# /home/bluecmd/Downloads/SAI/inc/saitunnel.h: 273

SAI_TUNNEL_MAP_ENTRY_ATTR_CUSTOM_RANGE_END = (SAI_TUNNEL_MAP_ENTRY_ATTR_CUSTOM_RANGE_START + 1)# /home/bluecmd/Downloads/SAI/inc/saitunnel.h: 273

sai_tunnel_map_entry_attr_t = enum__sai_tunnel_map_entry_attr_t# /home/bluecmd/Downloads/SAI/inc/saitunnel.h: 273

enum__sai_tunnel_map_attr_t = c_int# /home/bluecmd/Downloads/SAI/inc/saitunnel.h: 313

SAI_TUNNEL_MAP_ATTR_START = 0x00000000# /home/bluecmd/Downloads/SAI/inc/saitunnel.h: 313

SAI_TUNNEL_MAP_ATTR_TYPE = SAI_TUNNEL_MAP_ATTR_START# /home/bluecmd/Downloads/SAI/inc/saitunnel.h: 313

SAI_TUNNEL_MAP_ATTR_ENTRY_LIST = (SAI_TUNNEL_MAP_ATTR_TYPE + 1)# /home/bluecmd/Downloads/SAI/inc/saitunnel.h: 313

SAI_TUNNEL_MAP_ATTR_END = (SAI_TUNNEL_MAP_ATTR_ENTRY_LIST + 1)# /home/bluecmd/Downloads/SAI/inc/saitunnel.h: 313

SAI_TUNNEL_MAP_ATTR_CUSTOM_RANGE_START = 0x10000000# /home/bluecmd/Downloads/SAI/inc/saitunnel.h: 313

SAI_TUNNEL_MAP_ATTR_CUSTOM_RANGE_END = (SAI_TUNNEL_MAP_ATTR_CUSTOM_RANGE_START + 1)# /home/bluecmd/Downloads/SAI/inc/saitunnel.h: 313

sai_tunnel_map_attr_t = enum__sai_tunnel_map_attr_t# /home/bluecmd/Downloads/SAI/inc/saitunnel.h: 313

sai_create_tunnel_map_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saitunnel.h: 325

sai_remove_tunnel_map_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t)# /home/bluecmd/Downloads/SAI/inc/saitunnel.h: 338

sai_set_tunnel_map_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saitunnel.h: 349

sai_get_tunnel_map_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saitunnel.h: 362

enum__sai_tunnel_ttl_mode_t = c_int# /home/bluecmd/Downloads/SAI/inc/saitunnel.h: 395

SAI_TUNNEL_TTL_MODE_UNIFORM_MODEL = 0# /home/bluecmd/Downloads/SAI/inc/saitunnel.h: 395

SAI_TUNNEL_TTL_MODE_PIPE_MODEL = (SAI_TUNNEL_TTL_MODE_UNIFORM_MODEL + 1)# /home/bluecmd/Downloads/SAI/inc/saitunnel.h: 395

sai_tunnel_ttl_mode_t = enum__sai_tunnel_ttl_mode_t# /home/bluecmd/Downloads/SAI/inc/saitunnel.h: 395

enum__sai_tunnel_dscp_mode_t = c_int# /home/bluecmd/Downloads/SAI/inc/saitunnel.h: 425

SAI_TUNNEL_DSCP_MODE_UNIFORM_MODEL = 0# /home/bluecmd/Downloads/SAI/inc/saitunnel.h: 425

SAI_TUNNEL_DSCP_MODE_PIPE_MODEL = (SAI_TUNNEL_DSCP_MODE_UNIFORM_MODEL + 1)# /home/bluecmd/Downloads/SAI/inc/saitunnel.h: 425

sai_tunnel_dscp_mode_t = enum__sai_tunnel_dscp_mode_t# /home/bluecmd/Downloads/SAI/inc/saitunnel.h: 425

enum__sai_tunnel_peer_mode_t = c_int# /home/bluecmd/Downloads/SAI/inc/saitunnel.h: 442

SAI_TUNNEL_PEER_MODE_P2P = 0# /home/bluecmd/Downloads/SAI/inc/saitunnel.h: 442

SAI_TUNNEL_PEER_MODE_P2MP = (SAI_TUNNEL_PEER_MODE_P2P + 1)# /home/bluecmd/Downloads/SAI/inc/saitunnel.h: 442

sai_tunnel_peer_mode_t = enum__sai_tunnel_peer_mode_t# /home/bluecmd/Downloads/SAI/inc/saitunnel.h: 442

enum__sai_tunnel_attr_t = c_int# /home/bluecmd/Downloads/SAI/inc/saitunnel.h: 788

SAI_TUNNEL_ATTR_START = 0# /home/bluecmd/Downloads/SAI/inc/saitunnel.h: 788

SAI_TUNNEL_ATTR_TYPE = SAI_TUNNEL_ATTR_START# /home/bluecmd/Downloads/SAI/inc/saitunnel.h: 788

SAI_TUNNEL_ATTR_UNDERLAY_INTERFACE = (SAI_TUNNEL_ATTR_TYPE + 1)# /home/bluecmd/Downloads/SAI/inc/saitunnel.h: 788

SAI_TUNNEL_ATTR_OVERLAY_INTERFACE = (SAI_TUNNEL_ATTR_UNDERLAY_INTERFACE + 1)# /home/bluecmd/Downloads/SAI/inc/saitunnel.h: 788

SAI_TUNNEL_ATTR_PEER_MODE = (SAI_TUNNEL_ATTR_OVERLAY_INTERFACE + 1)# /home/bluecmd/Downloads/SAI/inc/saitunnel.h: 788

SAI_TUNNEL_ATTR_ENCAP_SRC_IP = (SAI_TUNNEL_ATTR_PEER_MODE + 1)# /home/bluecmd/Downloads/SAI/inc/saitunnel.h: 788

SAI_TUNNEL_ATTR_ENCAP_DST_IP = (SAI_TUNNEL_ATTR_ENCAP_SRC_IP + 1)# /home/bluecmd/Downloads/SAI/inc/saitunnel.h: 788

SAI_TUNNEL_ATTR_ENCAP_TTL_MODE = (SAI_TUNNEL_ATTR_ENCAP_DST_IP + 1)# /home/bluecmd/Downloads/SAI/inc/saitunnel.h: 788

SAI_TUNNEL_ATTR_ENCAP_TTL_VAL = (SAI_TUNNEL_ATTR_ENCAP_TTL_MODE + 1)# /home/bluecmd/Downloads/SAI/inc/saitunnel.h: 788

SAI_TUNNEL_ATTR_ENCAP_DSCP_MODE = (SAI_TUNNEL_ATTR_ENCAP_TTL_VAL + 1)# /home/bluecmd/Downloads/SAI/inc/saitunnel.h: 788

SAI_TUNNEL_ATTR_ENCAP_DSCP_VAL = (SAI_TUNNEL_ATTR_ENCAP_DSCP_MODE + 1)# /home/bluecmd/Downloads/SAI/inc/saitunnel.h: 788

SAI_TUNNEL_ATTR_ENCAP_GRE_KEY_VALID = (SAI_TUNNEL_ATTR_ENCAP_DSCP_VAL + 1)# /home/bluecmd/Downloads/SAI/inc/saitunnel.h: 788

SAI_TUNNEL_ATTR_ENCAP_GRE_KEY = (SAI_TUNNEL_ATTR_ENCAP_GRE_KEY_VALID + 1)# /home/bluecmd/Downloads/SAI/inc/saitunnel.h: 788

SAI_TUNNEL_ATTR_ENCAP_ECN_MODE = (SAI_TUNNEL_ATTR_ENCAP_GRE_KEY + 1)# /home/bluecmd/Downloads/SAI/inc/saitunnel.h: 788

SAI_TUNNEL_ATTR_ENCAP_MAPPERS = (SAI_TUNNEL_ATTR_ENCAP_ECN_MODE + 1)# /home/bluecmd/Downloads/SAI/inc/saitunnel.h: 788

SAI_TUNNEL_ATTR_DECAP_ECN_MODE = (SAI_TUNNEL_ATTR_ENCAP_MAPPERS + 1)# /home/bluecmd/Downloads/SAI/inc/saitunnel.h: 788

SAI_TUNNEL_ATTR_DECAP_MAPPERS = (SAI_TUNNEL_ATTR_DECAP_ECN_MODE + 1)# /home/bluecmd/Downloads/SAI/inc/saitunnel.h: 788

SAI_TUNNEL_ATTR_DECAP_TTL_MODE = (SAI_TUNNEL_ATTR_DECAP_MAPPERS + 1)# /home/bluecmd/Downloads/SAI/inc/saitunnel.h: 788

SAI_TUNNEL_ATTR_DECAP_DSCP_MODE = (SAI_TUNNEL_ATTR_DECAP_TTL_MODE + 1)# /home/bluecmd/Downloads/SAI/inc/saitunnel.h: 788

SAI_TUNNEL_ATTR_TERM_TABLE_ENTRY_LIST = (SAI_TUNNEL_ATTR_DECAP_DSCP_MODE + 1)# /home/bluecmd/Downloads/SAI/inc/saitunnel.h: 788

SAI_TUNNEL_ATTR_LOOPBACK_PACKET_ACTION = (SAI_TUNNEL_ATTR_TERM_TABLE_ENTRY_LIST + 1)# /home/bluecmd/Downloads/SAI/inc/saitunnel.h: 788

SAI_TUNNEL_ATTR_VXLAN_UDP_SPORT_MODE = (SAI_TUNNEL_ATTR_LOOPBACK_PACKET_ACTION + 1)# /home/bluecmd/Downloads/SAI/inc/saitunnel.h: 788

SAI_TUNNEL_ATTR_VXLAN_UDP_SPORT = (SAI_TUNNEL_ATTR_VXLAN_UDP_SPORT_MODE + 1)# /home/bluecmd/Downloads/SAI/inc/saitunnel.h: 788

SAI_TUNNEL_ATTR_VXLAN_UDP_SPORT_MASK = (SAI_TUNNEL_ATTR_VXLAN_UDP_SPORT + 1)# /home/bluecmd/Downloads/SAI/inc/saitunnel.h: 788

SAI_TUNNEL_ATTR_SA_INDEX = (SAI_TUNNEL_ATTR_VXLAN_UDP_SPORT_MASK + 1)# /home/bluecmd/Downloads/SAI/inc/saitunnel.h: 788

SAI_TUNNEL_ATTR_IPSEC_SA_PORT_LIST = (SAI_TUNNEL_ATTR_SA_INDEX + 1)# /home/bluecmd/Downloads/SAI/inc/saitunnel.h: 788

SAI_TUNNEL_ATTR_ENCAP_QOS_TC_AND_COLOR_TO_DSCP_MAP = (SAI_TUNNEL_ATTR_IPSEC_SA_PORT_LIST + 1)# /home/bluecmd/Downloads/SAI/inc/saitunnel.h: 788

SAI_TUNNEL_ATTR_ENCAP_QOS_TC_TO_QUEUE_MAP = (SAI_TUNNEL_ATTR_ENCAP_QOS_TC_AND_COLOR_TO_DSCP_MAP + 1)# /home/bluecmd/Downloads/SAI/inc/saitunnel.h: 788

SAI_TUNNEL_ATTR_DECAP_QOS_DSCP_TO_TC_MAP = (SAI_TUNNEL_ATTR_ENCAP_QOS_TC_TO_QUEUE_MAP + 1)# /home/bluecmd/Downloads/SAI/inc/saitunnel.h: 788

SAI_TUNNEL_ATTR_DECAP_QOS_TC_TO_PRIORITY_GROUP_MAP = (SAI_TUNNEL_ATTR_DECAP_QOS_DSCP_TO_TC_MAP + 1)# /home/bluecmd/Downloads/SAI/inc/saitunnel.h: 788

SAI_TUNNEL_ATTR_VXLAN_UDP_SPORT_SECURITY = (SAI_TUNNEL_ATTR_DECAP_QOS_TC_TO_PRIORITY_GROUP_MAP + 1)# /home/bluecmd/Downloads/SAI/inc/saitunnel.h: 788

SAI_TUNNEL_ATTR_END = (SAI_TUNNEL_ATTR_VXLAN_UDP_SPORT_SECURITY + 1)# /home/bluecmd/Downloads/SAI/inc/saitunnel.h: 788

SAI_TUNNEL_ATTR_CUSTOM_RANGE_START = 0x10000000# /home/bluecmd/Downloads/SAI/inc/saitunnel.h: 788

SAI_TUNNEL_ATTR_CUSTOM_RANGE_END = (SAI_TUNNEL_ATTR_CUSTOM_RANGE_START + 1)# /home/bluecmd/Downloads/SAI/inc/saitunnel.h: 788

sai_tunnel_attr_t = enum__sai_tunnel_attr_t# /home/bluecmd/Downloads/SAI/inc/saitunnel.h: 788

enum__sai_tunnel_stat_t = c_int# /home/bluecmd/Downloads/SAI/inc/saitunnel.h: 807

SAI_TUNNEL_STAT_IN_OCTETS = 0# /home/bluecmd/Downloads/SAI/inc/saitunnel.h: 807

SAI_TUNNEL_STAT_IN_PACKETS = (SAI_TUNNEL_STAT_IN_OCTETS + 1)# /home/bluecmd/Downloads/SAI/inc/saitunnel.h: 807

SAI_TUNNEL_STAT_OUT_OCTETS = (SAI_TUNNEL_STAT_IN_PACKETS + 1)# /home/bluecmd/Downloads/SAI/inc/saitunnel.h: 807

SAI_TUNNEL_STAT_OUT_PACKETS = (SAI_TUNNEL_STAT_OUT_OCTETS + 1)# /home/bluecmd/Downloads/SAI/inc/saitunnel.h: 807

sai_tunnel_stat_t = enum__sai_tunnel_stat_t# /home/bluecmd/Downloads/SAI/inc/saitunnel.h: 807

sai_create_tunnel_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saitunnel.h: 819

sai_remove_tunnel_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t)# /home/bluecmd/Downloads/SAI/inc/saitunnel.h: 832

sai_set_tunnel_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saitunnel.h: 843

sai_get_tunnel_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saitunnel.h: 856

sai_get_tunnel_stats_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, uint32_t, POINTER(sai_stat_id_t), POINTER(uint64_t))# /home/bluecmd/Downloads/SAI/inc/saitunnel.h: 871

sai_get_tunnel_stats_ext_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, uint32_t, POINTER(sai_stat_id_t), sai_stats_mode_t, POINTER(uint64_t))# /home/bluecmd/Downloads/SAI/inc/saitunnel.h: 888

sai_clear_tunnel_stats_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, uint32_t, POINTER(sai_stat_id_t))# /home/bluecmd/Downloads/SAI/inc/saitunnel.h: 904

enum__sai_tunnel_term_table_entry_type_t = c_int# /home/bluecmd/Downloads/SAI/inc/saitunnel.h: 926

SAI_TUNNEL_TERM_TABLE_ENTRY_TYPE_P2P = 0# /home/bluecmd/Downloads/SAI/inc/saitunnel.h: 926

SAI_TUNNEL_TERM_TABLE_ENTRY_TYPE_P2MP = (SAI_TUNNEL_TERM_TABLE_ENTRY_TYPE_P2P + 1)# /home/bluecmd/Downloads/SAI/inc/saitunnel.h: 926

SAI_TUNNEL_TERM_TABLE_ENTRY_TYPE_MP2P = (SAI_TUNNEL_TERM_TABLE_ENTRY_TYPE_P2MP + 1)# /home/bluecmd/Downloads/SAI/inc/saitunnel.h: 926

SAI_TUNNEL_TERM_TABLE_ENTRY_TYPE_MP2MP = (SAI_TUNNEL_TERM_TABLE_ENTRY_TYPE_MP2P + 1)# /home/bluecmd/Downloads/SAI/inc/saitunnel.h: 926

sai_tunnel_term_table_entry_type_t = enum__sai_tunnel_term_table_entry_type_t# /home/bluecmd/Downloads/SAI/inc/saitunnel.h: 926

enum__sai_tunnel_term_table_entry_attr_t = c_int# /home/bluecmd/Downloads/SAI/inc/saitunnel.h: 1060

SAI_TUNNEL_TERM_TABLE_ENTRY_ATTR_START = 0# /home/bluecmd/Downloads/SAI/inc/saitunnel.h: 1060

SAI_TUNNEL_TERM_TABLE_ENTRY_ATTR_VR_ID = SAI_TUNNEL_TERM_TABLE_ENTRY_ATTR_START# /home/bluecmd/Downloads/SAI/inc/saitunnel.h: 1060

SAI_TUNNEL_TERM_TABLE_ENTRY_ATTR_TYPE = (SAI_TUNNEL_TERM_TABLE_ENTRY_ATTR_VR_ID + 1)# /home/bluecmd/Downloads/SAI/inc/saitunnel.h: 1060

SAI_TUNNEL_TERM_TABLE_ENTRY_ATTR_DST_IP = (SAI_TUNNEL_TERM_TABLE_ENTRY_ATTR_TYPE + 1)# /home/bluecmd/Downloads/SAI/inc/saitunnel.h: 1060

SAI_TUNNEL_TERM_TABLE_ENTRY_ATTR_DST_IP_MASK = (SAI_TUNNEL_TERM_TABLE_ENTRY_ATTR_DST_IP + 1)# /home/bluecmd/Downloads/SAI/inc/saitunnel.h: 1060

SAI_TUNNEL_TERM_TABLE_ENTRY_ATTR_SRC_IP = (SAI_TUNNEL_TERM_TABLE_ENTRY_ATTR_DST_IP_MASK + 1)# /home/bluecmd/Downloads/SAI/inc/saitunnel.h: 1060

SAI_TUNNEL_TERM_TABLE_ENTRY_ATTR_SRC_IP_MASK = (SAI_TUNNEL_TERM_TABLE_ENTRY_ATTR_SRC_IP + 1)# /home/bluecmd/Downloads/SAI/inc/saitunnel.h: 1060

SAI_TUNNEL_TERM_TABLE_ENTRY_ATTR_TUNNEL_TYPE = (SAI_TUNNEL_TERM_TABLE_ENTRY_ATTR_SRC_IP_MASK + 1)# /home/bluecmd/Downloads/SAI/inc/saitunnel.h: 1060

SAI_TUNNEL_TERM_TABLE_ENTRY_ATTR_ACTION_TUNNEL_ID = (SAI_TUNNEL_TERM_TABLE_ENTRY_ATTR_TUNNEL_TYPE + 1)# /home/bluecmd/Downloads/SAI/inc/saitunnel.h: 1060

SAI_TUNNEL_TERM_TABLE_ENTRY_ATTR_IP_ADDR_FAMILY = (SAI_TUNNEL_TERM_TABLE_ENTRY_ATTR_ACTION_TUNNEL_ID + 1)# /home/bluecmd/Downloads/SAI/inc/saitunnel.h: 1060

SAI_TUNNEL_TERM_TABLE_ENTRY_ATTR_IPSEC_VERIFIED = (SAI_TUNNEL_TERM_TABLE_ENTRY_ATTR_IP_ADDR_FAMILY + 1)# /home/bluecmd/Downloads/SAI/inc/saitunnel.h: 1060

SAI_TUNNEL_TERM_TABLE_ENTRY_ATTR_PRIORITY = (SAI_TUNNEL_TERM_TABLE_ENTRY_ATTR_IPSEC_VERIFIED + 1)# /home/bluecmd/Downloads/SAI/inc/saitunnel.h: 1060

SAI_TUNNEL_TERM_TABLE_ENTRY_ATTR_END = (SAI_TUNNEL_TERM_TABLE_ENTRY_ATTR_PRIORITY + 1)# /home/bluecmd/Downloads/SAI/inc/saitunnel.h: 1060

SAI_TUNNEL_TERM_TABLE_ENTRY_ATTR_CUSTOM_RANGE_START = 0x10000000# /home/bluecmd/Downloads/SAI/inc/saitunnel.h: 1060

SAI_TUNNEL_TERM_TABLE_ENTRY_ATTR_CUSTOM_RANGE_END = (SAI_TUNNEL_TERM_TABLE_ENTRY_ATTR_CUSTOM_RANGE_START + 1)# /home/bluecmd/Downloads/SAI/inc/saitunnel.h: 1060

sai_tunnel_term_table_entry_attr_t = enum__sai_tunnel_term_table_entry_attr_t# /home/bluecmd/Downloads/SAI/inc/saitunnel.h: 1060

sai_create_tunnel_term_table_entry_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saitunnel.h: 1072

sai_remove_tunnel_term_table_entry_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t)# /home/bluecmd/Downloads/SAI/inc/saitunnel.h: 1085

sai_set_tunnel_term_table_entry_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saitunnel.h: 1096

sai_get_tunnel_term_table_entry_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saitunnel.h: 1109

sai_create_tunnel_map_entry_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saitunnel.h: 1124

sai_remove_tunnel_map_entry_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t)# /home/bluecmd/Downloads/SAI/inc/saitunnel.h: 1137

sai_set_tunnel_map_entry_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saitunnel.h: 1148

sai_get_tunnel_map_entry_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saitunnel.h: 1161

# /home/bluecmd/Downloads/SAI/inc/saitunnel.h: 1195
class struct__sai_tunnel_api_t(Structure):
    pass

struct__sai_tunnel_api_t.__slots__ = [
    'create_tunnel_map',
    'remove_tunnel_map',
    'set_tunnel_map_attribute',
    'get_tunnel_map_attribute',
    'create_tunnel',
    'remove_tunnel',
    'set_tunnel_attribute',
    'get_tunnel_attribute',
    'get_tunnel_stats',
    'get_tunnel_stats_ext',
    'clear_tunnel_stats',
    'create_tunnel_term_table_entry',
    'remove_tunnel_term_table_entry',
    'set_tunnel_term_table_entry_attribute',
    'get_tunnel_term_table_entry_attribute',
    'create_tunnel_map_entry',
    'remove_tunnel_map_entry',
    'set_tunnel_map_entry_attribute',
    'get_tunnel_map_entry_attribute',
    'create_tunnels',
    'remove_tunnels',
    'set_tunnels_attribute',
    'get_tunnels_attribute',
]
struct__sai_tunnel_api_t._fields_ = [
    ('create_tunnel_map', sai_create_tunnel_map_fn),
    ('remove_tunnel_map', sai_remove_tunnel_map_fn),
    ('set_tunnel_map_attribute', sai_set_tunnel_map_attribute_fn),
    ('get_tunnel_map_attribute', sai_get_tunnel_map_attribute_fn),
    ('create_tunnel', sai_create_tunnel_fn),
    ('remove_tunnel', sai_remove_tunnel_fn),
    ('set_tunnel_attribute', sai_set_tunnel_attribute_fn),
    ('get_tunnel_attribute', sai_get_tunnel_attribute_fn),
    ('get_tunnel_stats', sai_get_tunnel_stats_fn),
    ('get_tunnel_stats_ext', sai_get_tunnel_stats_ext_fn),
    ('clear_tunnel_stats', sai_clear_tunnel_stats_fn),
    ('create_tunnel_term_table_entry', sai_create_tunnel_term_table_entry_fn),
    ('remove_tunnel_term_table_entry', sai_remove_tunnel_term_table_entry_fn),
    ('set_tunnel_term_table_entry_attribute', sai_set_tunnel_term_table_entry_attribute_fn),
    ('get_tunnel_term_table_entry_attribute', sai_get_tunnel_term_table_entry_attribute_fn),
    ('create_tunnel_map_entry', sai_create_tunnel_map_entry_fn),
    ('remove_tunnel_map_entry', sai_remove_tunnel_map_entry_fn),
    ('set_tunnel_map_entry_attribute', sai_set_tunnel_map_entry_attribute_fn),
    ('get_tunnel_map_entry_attribute', sai_get_tunnel_map_entry_attribute_fn),
    ('create_tunnels', sai_bulk_object_create_fn),
    ('remove_tunnels', sai_bulk_object_remove_fn),
    ('set_tunnels_attribute', sai_bulk_object_set_attribute_fn),
    ('get_tunnels_attribute', sai_bulk_object_get_attribute_fn),
]

sai_tunnel_api_t = struct__sai_tunnel_api_t# /home/bluecmd/Downloads/SAI/inc/saitunnel.h: 1195

enum__sai_udf_base_t = c_int# /home/bluecmd/Downloads/SAI/inc/saiudf.h: 50

SAI_UDF_BASE_L2 = 0# /home/bluecmd/Downloads/SAI/inc/saiudf.h: 50

SAI_UDF_BASE_L3 = (SAI_UDF_BASE_L2 + 1)# /home/bluecmd/Downloads/SAI/inc/saiudf.h: 50

SAI_UDF_BASE_L4 = (SAI_UDF_BASE_L3 + 1)# /home/bluecmd/Downloads/SAI/inc/saiudf.h: 50

sai_udf_base_t = enum__sai_udf_base_t# /home/bluecmd/Downloads/SAI/inc/saiudf.h: 50

enum__sai_udf_attr_t = c_int# /home/bluecmd/Downloads/SAI/inc/saiudf.h: 124

SAI_UDF_ATTR_START = 0# /home/bluecmd/Downloads/SAI/inc/saiudf.h: 124

SAI_UDF_ATTR_MATCH_ID = SAI_UDF_ATTR_START# /home/bluecmd/Downloads/SAI/inc/saiudf.h: 124

SAI_UDF_ATTR_GROUP_ID = (SAI_UDF_ATTR_MATCH_ID + 1)# /home/bluecmd/Downloads/SAI/inc/saiudf.h: 124

SAI_UDF_ATTR_BASE = (SAI_UDF_ATTR_GROUP_ID + 1)# /home/bluecmd/Downloads/SAI/inc/saiudf.h: 124

SAI_UDF_ATTR_OFFSET = (SAI_UDF_ATTR_BASE + 1)# /home/bluecmd/Downloads/SAI/inc/saiudf.h: 124

SAI_UDF_ATTR_HASH_MASK = (SAI_UDF_ATTR_OFFSET + 1)# /home/bluecmd/Downloads/SAI/inc/saiudf.h: 124

SAI_UDF_ATTR_END = (SAI_UDF_ATTR_HASH_MASK + 1)# /home/bluecmd/Downloads/SAI/inc/saiudf.h: 124

SAI_UDF_ATTR_CUSTOM_RANGE_START = 0x10000000# /home/bluecmd/Downloads/SAI/inc/saiudf.h: 124

SAI_UDF_ATTR_CUSTOM_RANGE_END = (SAI_UDF_ATTR_CUSTOM_RANGE_START + 1)# /home/bluecmd/Downloads/SAI/inc/saiudf.h: 124

sai_udf_attr_t = enum__sai_udf_attr_t# /home/bluecmd/Downloads/SAI/inc/saiudf.h: 124

enum__sai_udf_match_attr_t = c_int# /home/bluecmd/Downloads/SAI/inc/saiudf.h: 203

SAI_UDF_MATCH_ATTR_START = 0# /home/bluecmd/Downloads/SAI/inc/saiudf.h: 203

SAI_UDF_MATCH_ATTR_L2_TYPE = SAI_UDF_MATCH_ATTR_START# /home/bluecmd/Downloads/SAI/inc/saiudf.h: 203

SAI_UDF_MATCH_ATTR_L3_TYPE = (SAI_UDF_MATCH_ATTR_L2_TYPE + 1)# /home/bluecmd/Downloads/SAI/inc/saiudf.h: 203

SAI_UDF_MATCH_ATTR_GRE_TYPE = (SAI_UDF_MATCH_ATTR_L3_TYPE + 1)# /home/bluecmd/Downloads/SAI/inc/saiudf.h: 203

SAI_UDF_MATCH_ATTR_PRIORITY = (SAI_UDF_MATCH_ATTR_GRE_TYPE + 1)# /home/bluecmd/Downloads/SAI/inc/saiudf.h: 203

SAI_UDF_MATCH_ATTR_L4_DST_PORT_TYPE = (SAI_UDF_MATCH_ATTR_PRIORITY + 1)# /home/bluecmd/Downloads/SAI/inc/saiudf.h: 203

SAI_UDF_MATCH_ATTR_END = (SAI_UDF_MATCH_ATTR_L4_DST_PORT_TYPE + 1)# /home/bluecmd/Downloads/SAI/inc/saiudf.h: 203

SAI_UDF_MATCH_ATTR_CUSTOM_RANGE_START = 0x10000000# /home/bluecmd/Downloads/SAI/inc/saiudf.h: 203

SAI_UDF_MATCH_ATTR_CUSTOM_RANGE_END = (SAI_UDF_MATCH_ATTR_CUSTOM_RANGE_START + 1)# /home/bluecmd/Downloads/SAI/inc/saiudf.h: 203

sai_udf_match_attr_t = enum__sai_udf_match_attr_t# /home/bluecmd/Downloads/SAI/inc/saiudf.h: 203

enum__sai_udf_group_type_t = c_int# /home/bluecmd/Downloads/SAI/inc/saiudf.h: 222

SAI_UDF_GROUP_TYPE_START = 0# /home/bluecmd/Downloads/SAI/inc/saiudf.h: 222

SAI_UDF_GROUP_TYPE_GENERIC = SAI_UDF_GROUP_TYPE_START# /home/bluecmd/Downloads/SAI/inc/saiudf.h: 222

SAI_UDF_GROUP_TYPE_HASH = (SAI_UDF_GROUP_TYPE_GENERIC + 1)# /home/bluecmd/Downloads/SAI/inc/saiudf.h: 222

SAI_UDF_GROUP_TYPE_END = (SAI_UDF_GROUP_TYPE_HASH + 1)# /home/bluecmd/Downloads/SAI/inc/saiudf.h: 222

sai_udf_group_type_t = enum__sai_udf_group_type_t# /home/bluecmd/Downloads/SAI/inc/saiudf.h: 222

enum__sai_udf_group_attr_t = c_int# /home/bluecmd/Downloads/SAI/inc/saiudf.h: 272

SAI_UDF_GROUP_ATTR_START = 0# /home/bluecmd/Downloads/SAI/inc/saiudf.h: 272

SAI_UDF_GROUP_ATTR_UDF_LIST = SAI_UDF_GROUP_ATTR_START# /home/bluecmd/Downloads/SAI/inc/saiudf.h: 272

SAI_UDF_GROUP_ATTR_TYPE = (SAI_UDF_GROUP_ATTR_UDF_LIST + 1)# /home/bluecmd/Downloads/SAI/inc/saiudf.h: 272

SAI_UDF_GROUP_ATTR_LENGTH = (SAI_UDF_GROUP_ATTR_TYPE + 1)# /home/bluecmd/Downloads/SAI/inc/saiudf.h: 272

SAI_UDF_GROUP_ATTR_END = (SAI_UDF_GROUP_ATTR_LENGTH + 1)# /home/bluecmd/Downloads/SAI/inc/saiudf.h: 272

SAI_UDF_GROUP_ATTR_CUSTOM_RANGE_START = 0x10000000# /home/bluecmd/Downloads/SAI/inc/saiudf.h: 272

SAI_UDF_GROUP_ATTR_CUSTOM_RANGE_END = (SAI_UDF_GROUP_ATTR_CUSTOM_RANGE_START + 1)# /home/bluecmd/Downloads/SAI/inc/saiudf.h: 272

sai_udf_group_attr_t = enum__sai_udf_group_attr_t# /home/bluecmd/Downloads/SAI/inc/saiudf.h: 272

sai_create_udf_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saiudf.h: 284

sai_remove_udf_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t)# /home/bluecmd/Downloads/SAI/inc/saiudf.h: 297

sai_set_udf_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saiudf.h: 308

sai_get_udf_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saiudf.h: 321

sai_create_udf_match_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saiudf.h: 336

sai_remove_udf_match_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t)# /home/bluecmd/Downloads/SAI/inc/saiudf.h: 349

sai_set_udf_match_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saiudf.h: 360

sai_get_udf_match_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saiudf.h: 373

sai_create_udf_group_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saiudf.h: 388

sai_remove_udf_group_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t)# /home/bluecmd/Downloads/SAI/inc/saiudf.h: 401

sai_set_udf_group_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saiudf.h: 412

sai_get_udf_group_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saiudf.h: 425

# /home/bluecmd/Downloads/SAI/inc/saiudf.h: 448
class struct__sai_udf_api_t(Structure):
    pass

struct__sai_udf_api_t.__slots__ = [
    'create_udf',
    'remove_udf',
    'set_udf_attribute',
    'get_udf_attribute',
    'create_udf_match',
    'remove_udf_match',
    'set_udf_match_attribute',
    'get_udf_match_attribute',
    'create_udf_group',
    'remove_udf_group',
    'set_udf_group_attribute',
    'get_udf_group_attribute',
]
struct__sai_udf_api_t._fields_ = [
    ('create_udf', sai_create_udf_fn),
    ('remove_udf', sai_remove_udf_fn),
    ('set_udf_attribute', sai_set_udf_attribute_fn),
    ('get_udf_attribute', sai_get_udf_attribute_fn),
    ('create_udf_match', sai_create_udf_match_fn),
    ('remove_udf_match', sai_remove_udf_match_fn),
    ('set_udf_match_attribute', sai_set_udf_match_attribute_fn),
    ('get_udf_match_attribute', sai_get_udf_match_attribute_fn),
    ('create_udf_group', sai_create_udf_group_fn),
    ('remove_udf_group', sai_remove_udf_group_fn),
    ('set_udf_group_attribute', sai_set_udf_group_attribute_fn),
    ('get_udf_group_attribute', sai_get_udf_group_attribute_fn),
]

sai_udf_api_t = struct__sai_udf_api_t# /home/bluecmd/Downloads/SAI/inc/saiudf.h: 448

enum__sai_virtual_router_attr_t = c_int# /home/bluecmd/Downloads/SAI/inc/saivirtualrouter.h: 129

SAI_VIRTUAL_ROUTER_ATTR_START = 0# /home/bluecmd/Downloads/SAI/inc/saivirtualrouter.h: 129

SAI_VIRTUAL_ROUTER_ATTR_ADMIN_V4_STATE = SAI_VIRTUAL_ROUTER_ATTR_START# /home/bluecmd/Downloads/SAI/inc/saivirtualrouter.h: 129

SAI_VIRTUAL_ROUTER_ATTR_ADMIN_V6_STATE = (SAI_VIRTUAL_ROUTER_ATTR_ADMIN_V4_STATE + 1)# /home/bluecmd/Downloads/SAI/inc/saivirtualrouter.h: 129

SAI_VIRTUAL_ROUTER_ATTR_SRC_MAC_ADDRESS = (SAI_VIRTUAL_ROUTER_ATTR_ADMIN_V6_STATE + 1)# /home/bluecmd/Downloads/SAI/inc/saivirtualrouter.h: 129

SAI_VIRTUAL_ROUTER_ATTR_VIOLATION_TTL1_PACKET_ACTION = (SAI_VIRTUAL_ROUTER_ATTR_SRC_MAC_ADDRESS + 1)# /home/bluecmd/Downloads/SAI/inc/saivirtualrouter.h: 129

SAI_VIRTUAL_ROUTER_ATTR_VIOLATION_IP_OPTIONS_PACKET_ACTION = (SAI_VIRTUAL_ROUTER_ATTR_VIOLATION_TTL1_PACKET_ACTION + 1)# /home/bluecmd/Downloads/SAI/inc/saivirtualrouter.h: 129

SAI_VIRTUAL_ROUTER_ATTR_UNKNOWN_L3_MULTICAST_PACKET_ACTION = (SAI_VIRTUAL_ROUTER_ATTR_VIOLATION_IP_OPTIONS_PACKET_ACTION + 1)# /home/bluecmd/Downloads/SAI/inc/saivirtualrouter.h: 129

SAI_VIRTUAL_ROUTER_ATTR_LABEL = (SAI_VIRTUAL_ROUTER_ATTR_UNKNOWN_L3_MULTICAST_PACKET_ACTION + 1)# /home/bluecmd/Downloads/SAI/inc/saivirtualrouter.h: 129

SAI_VIRTUAL_ROUTER_ATTR_END = (SAI_VIRTUAL_ROUTER_ATTR_LABEL + 1)# /home/bluecmd/Downloads/SAI/inc/saivirtualrouter.h: 129

SAI_VIRTUAL_ROUTER_ATTR_CUSTOM_RANGE_START = 0x10000000# /home/bluecmd/Downloads/SAI/inc/saivirtualrouter.h: 129

SAI_VIRTUAL_ROUTER_ATTR_CUSTOM_RANGE_END = (SAI_VIRTUAL_ROUTER_ATTR_CUSTOM_RANGE_START + 1)# /home/bluecmd/Downloads/SAI/inc/saivirtualrouter.h: 129

sai_virtual_router_attr_t = enum__sai_virtual_router_attr_t# /home/bluecmd/Downloads/SAI/inc/saivirtualrouter.h: 129

sai_create_virtual_router_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saivirtualrouter.h: 143

sai_remove_virtual_router_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t)# /home/bluecmd/Downloads/SAI/inc/saivirtualrouter.h: 156

sai_set_virtual_router_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saivirtualrouter.h: 167

sai_get_virtual_router_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saivirtualrouter.h: 180

# /home/bluecmd/Downloads/SAI/inc/saivirtualrouter.h: 195
class struct__sai_virtual_router_api_t(Structure):
    pass

struct__sai_virtual_router_api_t.__slots__ = [
    'create_virtual_router',
    'remove_virtual_router',
    'set_virtual_router_attribute',
    'get_virtual_router_attribute',
]
struct__sai_virtual_router_api_t._fields_ = [
    ('create_virtual_router', sai_create_virtual_router_fn),
    ('remove_virtual_router', sai_remove_virtual_router_fn),
    ('set_virtual_router_attribute', sai_set_virtual_router_attribute_fn),
    ('get_virtual_router_attribute', sai_get_virtual_router_attribute_fn),
]

sai_virtual_router_api_t = struct__sai_virtual_router_api_t# /home/bluecmd/Downloads/SAI/inc/saivirtualrouter.h: 195

enum__sai_vlan_tagging_mode_t = c_int# /home/bluecmd/Downloads/SAI/inc/saivlan.h: 52

SAI_VLAN_TAGGING_MODE_UNTAGGED = 0# /home/bluecmd/Downloads/SAI/inc/saivlan.h: 52

SAI_VLAN_TAGGING_MODE_TAGGED = (SAI_VLAN_TAGGING_MODE_UNTAGGED + 1)# /home/bluecmd/Downloads/SAI/inc/saivlan.h: 52

SAI_VLAN_TAGGING_MODE_PRIORITY_TAGGED = (SAI_VLAN_TAGGING_MODE_TAGGED + 1)# /home/bluecmd/Downloads/SAI/inc/saivlan.h: 52

sai_vlan_tagging_mode_t = enum__sai_vlan_tagging_mode_t# /home/bluecmd/Downloads/SAI/inc/saivlan.h: 52

enum__sai_vlan_mcast_lookup_key_type_t = c_int# /home/bluecmd/Downloads/SAI/inc/saivlan.h: 67

SAI_VLAN_MCAST_LOOKUP_KEY_TYPE_MAC_DA = 0# /home/bluecmd/Downloads/SAI/inc/saivlan.h: 67

SAI_VLAN_MCAST_LOOKUP_KEY_TYPE_XG = (SAI_VLAN_MCAST_LOOKUP_KEY_TYPE_MAC_DA + 1)# /home/bluecmd/Downloads/SAI/inc/saivlan.h: 67

SAI_VLAN_MCAST_LOOKUP_KEY_TYPE_SG = (SAI_VLAN_MCAST_LOOKUP_KEY_TYPE_XG + 1)# /home/bluecmd/Downloads/SAI/inc/saivlan.h: 67

SAI_VLAN_MCAST_LOOKUP_KEY_TYPE_XG_AND_SG = (SAI_VLAN_MCAST_LOOKUP_KEY_TYPE_SG + 1)# /home/bluecmd/Downloads/SAI/inc/saivlan.h: 67

sai_vlan_mcast_lookup_key_type_t = enum__sai_vlan_mcast_lookup_key_type_t# /home/bluecmd/Downloads/SAI/inc/saivlan.h: 67

enum__sai_vlan_flood_control_type_t = c_int# /home/bluecmd/Downloads/SAI/inc/saivlan.h: 98

SAI_VLAN_FLOOD_CONTROL_TYPE_ALL = 0# /home/bluecmd/Downloads/SAI/inc/saivlan.h: 98

SAI_VLAN_FLOOD_CONTROL_TYPE_NONE = (SAI_VLAN_FLOOD_CONTROL_TYPE_ALL + 1)# /home/bluecmd/Downloads/SAI/inc/saivlan.h: 98

SAI_VLAN_FLOOD_CONTROL_TYPE_L2MC_GROUP = (SAI_VLAN_FLOOD_CONTROL_TYPE_NONE + 1)# /home/bluecmd/Downloads/SAI/inc/saivlan.h: 98

SAI_VLAN_FLOOD_CONTROL_TYPE_COMBINED = (SAI_VLAN_FLOOD_CONTROL_TYPE_L2MC_GROUP + 1)# /home/bluecmd/Downloads/SAI/inc/saivlan.h: 98

sai_vlan_flood_control_type_t = enum__sai_vlan_flood_control_type_t# /home/bluecmd/Downloads/SAI/inc/saivlan.h: 98

enum__sai_vlan_attr_t = c_int# /home/bluecmd/Downloads/SAI/inc/saivlan.h: 414

SAI_VLAN_ATTR_START = 0# /home/bluecmd/Downloads/SAI/inc/saivlan.h: 414

SAI_VLAN_ATTR_VLAN_ID = SAI_VLAN_ATTR_START# /home/bluecmd/Downloads/SAI/inc/saivlan.h: 414

SAI_VLAN_ATTR_MEMBER_LIST = (SAI_VLAN_ATTR_VLAN_ID + 1)# /home/bluecmd/Downloads/SAI/inc/saivlan.h: 414

SAI_VLAN_ATTR_MAX_LEARNED_ADDRESSES = (SAI_VLAN_ATTR_MEMBER_LIST + 1)# /home/bluecmd/Downloads/SAI/inc/saivlan.h: 414

SAI_VLAN_ATTR_STP_INSTANCE = (SAI_VLAN_ATTR_MAX_LEARNED_ADDRESSES + 1)# /home/bluecmd/Downloads/SAI/inc/saivlan.h: 414

SAI_VLAN_ATTR_LEARN_DISABLE = (SAI_VLAN_ATTR_STP_INSTANCE + 1)# /home/bluecmd/Downloads/SAI/inc/saivlan.h: 414

SAI_VLAN_ATTR_IPV4_MCAST_LOOKUP_KEY_TYPE = (SAI_VLAN_ATTR_LEARN_DISABLE + 1)# /home/bluecmd/Downloads/SAI/inc/saivlan.h: 414

SAI_VLAN_ATTR_IPV6_MCAST_LOOKUP_KEY_TYPE = (SAI_VLAN_ATTR_IPV4_MCAST_LOOKUP_KEY_TYPE + 1)# /home/bluecmd/Downloads/SAI/inc/saivlan.h: 414

SAI_VLAN_ATTR_UNKNOWN_NON_IP_MCAST_OUTPUT_GROUP_ID = (SAI_VLAN_ATTR_IPV6_MCAST_LOOKUP_KEY_TYPE + 1)# /home/bluecmd/Downloads/SAI/inc/saivlan.h: 414

SAI_VLAN_ATTR_UNKNOWN_IPV4_MCAST_OUTPUT_GROUP_ID = (SAI_VLAN_ATTR_UNKNOWN_NON_IP_MCAST_OUTPUT_GROUP_ID + 1)# /home/bluecmd/Downloads/SAI/inc/saivlan.h: 414

SAI_VLAN_ATTR_UNKNOWN_IPV6_MCAST_OUTPUT_GROUP_ID = (SAI_VLAN_ATTR_UNKNOWN_IPV4_MCAST_OUTPUT_GROUP_ID + 1)# /home/bluecmd/Downloads/SAI/inc/saivlan.h: 414

SAI_VLAN_ATTR_UNKNOWN_LINKLOCAL_MCAST_OUTPUT_GROUP_ID = (SAI_VLAN_ATTR_UNKNOWN_IPV6_MCAST_OUTPUT_GROUP_ID + 1)# /home/bluecmd/Downloads/SAI/inc/saivlan.h: 414

SAI_VLAN_ATTR_INGRESS_ACL = (SAI_VLAN_ATTR_UNKNOWN_LINKLOCAL_MCAST_OUTPUT_GROUP_ID + 1)# /home/bluecmd/Downloads/SAI/inc/saivlan.h: 414

SAI_VLAN_ATTR_EGRESS_ACL = (SAI_VLAN_ATTR_INGRESS_ACL + 1)# /home/bluecmd/Downloads/SAI/inc/saivlan.h: 414

SAI_VLAN_ATTR_META_DATA = (SAI_VLAN_ATTR_EGRESS_ACL + 1)# /home/bluecmd/Downloads/SAI/inc/saivlan.h: 414

SAI_VLAN_ATTR_UNKNOWN_UNICAST_FLOOD_CONTROL_TYPE = (SAI_VLAN_ATTR_META_DATA + 1)# /home/bluecmd/Downloads/SAI/inc/saivlan.h: 414

SAI_VLAN_ATTR_UNKNOWN_UNICAST_FLOOD_GROUP = (SAI_VLAN_ATTR_UNKNOWN_UNICAST_FLOOD_CONTROL_TYPE + 1)# /home/bluecmd/Downloads/SAI/inc/saivlan.h: 414

SAI_VLAN_ATTR_UNKNOWN_MULTICAST_FLOOD_CONTROL_TYPE = (SAI_VLAN_ATTR_UNKNOWN_UNICAST_FLOOD_GROUP + 1)# /home/bluecmd/Downloads/SAI/inc/saivlan.h: 414

SAI_VLAN_ATTR_UNKNOWN_MULTICAST_FLOOD_GROUP = (SAI_VLAN_ATTR_UNKNOWN_MULTICAST_FLOOD_CONTROL_TYPE + 1)# /home/bluecmd/Downloads/SAI/inc/saivlan.h: 414

SAI_VLAN_ATTR_BROADCAST_FLOOD_CONTROL_TYPE = (SAI_VLAN_ATTR_UNKNOWN_MULTICAST_FLOOD_GROUP + 1)# /home/bluecmd/Downloads/SAI/inc/saivlan.h: 414

SAI_VLAN_ATTR_BROADCAST_FLOOD_GROUP = (SAI_VLAN_ATTR_BROADCAST_FLOOD_CONTROL_TYPE + 1)# /home/bluecmd/Downloads/SAI/inc/saivlan.h: 414

SAI_VLAN_ATTR_CUSTOM_IGMP_SNOOPING_ENABLE = (SAI_VLAN_ATTR_BROADCAST_FLOOD_GROUP + 1)# /home/bluecmd/Downloads/SAI/inc/saivlan.h: 414

SAI_VLAN_ATTR_TAM_OBJECT = (SAI_VLAN_ATTR_CUSTOM_IGMP_SNOOPING_ENABLE + 1)# /home/bluecmd/Downloads/SAI/inc/saivlan.h: 414

SAI_VLAN_ATTR_END = (SAI_VLAN_ATTR_TAM_OBJECT + 1)# /home/bluecmd/Downloads/SAI/inc/saivlan.h: 414

SAI_VLAN_ATTR_CUSTOM_RANGE_START = 0x10000000# /home/bluecmd/Downloads/SAI/inc/saivlan.h: 414

SAI_VLAN_ATTR_CUSTOM_RANGE_END = (SAI_VLAN_ATTR_CUSTOM_RANGE_START + 1)# /home/bluecmd/Downloads/SAI/inc/saivlan.h: 414

sai_vlan_attr_t = enum__sai_vlan_attr_t# /home/bluecmd/Downloads/SAI/inc/saivlan.h: 414

enum__sai_vlan_member_attr_t = c_int# /home/bluecmd/Downloads/SAI/inc/saivlan.h: 466

SAI_VLAN_MEMBER_ATTR_START = 0# /home/bluecmd/Downloads/SAI/inc/saivlan.h: 466

SAI_VLAN_MEMBER_ATTR_VLAN_ID = SAI_VLAN_MEMBER_ATTR_START# /home/bluecmd/Downloads/SAI/inc/saivlan.h: 466

SAI_VLAN_MEMBER_ATTR_BRIDGE_PORT_ID = (SAI_VLAN_MEMBER_ATTR_VLAN_ID + 1)# /home/bluecmd/Downloads/SAI/inc/saivlan.h: 466

SAI_VLAN_MEMBER_ATTR_VLAN_TAGGING_MODE = (SAI_VLAN_MEMBER_ATTR_BRIDGE_PORT_ID + 1)# /home/bluecmd/Downloads/SAI/inc/saivlan.h: 466

SAI_VLAN_MEMBER_ATTR_END = (SAI_VLAN_MEMBER_ATTR_VLAN_TAGGING_MODE + 1)# /home/bluecmd/Downloads/SAI/inc/saivlan.h: 466

SAI_VLAN_MEMBER_ATTR_CUSTOM_RANGE_START = 0x10000000# /home/bluecmd/Downloads/SAI/inc/saivlan.h: 466

SAI_VLAN_MEMBER_ATTR_CUSTOM_RANGE_END = (SAI_VLAN_MEMBER_ATTR_CUSTOM_RANGE_START + 1)# /home/bluecmd/Downloads/SAI/inc/saivlan.h: 466

sai_vlan_member_attr_t = enum__sai_vlan_member_attr_t# /home/bluecmd/Downloads/SAI/inc/saivlan.h: 466

enum__sai_vlan_stat_t = c_int# /home/bluecmd/Downloads/SAI/inc/saivlan.h: 488

SAI_VLAN_STAT_IN_OCTETS = 0# /home/bluecmd/Downloads/SAI/inc/saivlan.h: 488

SAI_VLAN_STAT_IN_PACKETS = (SAI_VLAN_STAT_IN_OCTETS + 1)# /home/bluecmd/Downloads/SAI/inc/saivlan.h: 488

SAI_VLAN_STAT_IN_UCAST_PKTS = (SAI_VLAN_STAT_IN_PACKETS + 1)# /home/bluecmd/Downloads/SAI/inc/saivlan.h: 488

SAI_VLAN_STAT_IN_NON_UCAST_PKTS = (SAI_VLAN_STAT_IN_UCAST_PKTS + 1)# /home/bluecmd/Downloads/SAI/inc/saivlan.h: 488

SAI_VLAN_STAT_IN_DISCARDS = (SAI_VLAN_STAT_IN_NON_UCAST_PKTS + 1)# /home/bluecmd/Downloads/SAI/inc/saivlan.h: 488

SAI_VLAN_STAT_IN_ERRORS = (SAI_VLAN_STAT_IN_DISCARDS + 1)# /home/bluecmd/Downloads/SAI/inc/saivlan.h: 488

SAI_VLAN_STAT_IN_UNKNOWN_PROTOS = (SAI_VLAN_STAT_IN_ERRORS + 1)# /home/bluecmd/Downloads/SAI/inc/saivlan.h: 488

SAI_VLAN_STAT_OUT_OCTETS = (SAI_VLAN_STAT_IN_UNKNOWN_PROTOS + 1)# /home/bluecmd/Downloads/SAI/inc/saivlan.h: 488

SAI_VLAN_STAT_OUT_PACKETS = (SAI_VLAN_STAT_OUT_OCTETS + 1)# /home/bluecmd/Downloads/SAI/inc/saivlan.h: 488

SAI_VLAN_STAT_OUT_UCAST_PKTS = (SAI_VLAN_STAT_OUT_PACKETS + 1)# /home/bluecmd/Downloads/SAI/inc/saivlan.h: 488

SAI_VLAN_STAT_OUT_NON_UCAST_PKTS = (SAI_VLAN_STAT_OUT_UCAST_PKTS + 1)# /home/bluecmd/Downloads/SAI/inc/saivlan.h: 488

SAI_VLAN_STAT_OUT_DISCARDS = (SAI_VLAN_STAT_OUT_NON_UCAST_PKTS + 1)# /home/bluecmd/Downloads/SAI/inc/saivlan.h: 488

SAI_VLAN_STAT_OUT_ERRORS = (SAI_VLAN_STAT_OUT_DISCARDS + 1)# /home/bluecmd/Downloads/SAI/inc/saivlan.h: 488

SAI_VLAN_STAT_OUT_QLEN = (SAI_VLAN_STAT_OUT_ERRORS + 1)# /home/bluecmd/Downloads/SAI/inc/saivlan.h: 488

sai_vlan_stat_t = enum__sai_vlan_stat_t# /home/bluecmd/Downloads/SAI/inc/saivlan.h: 488

sai_create_vlan_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saivlan.h: 500

sai_remove_vlan_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t)# /home/bluecmd/Downloads/SAI/inc/saivlan.h: 513

sai_set_vlan_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saivlan.h: 524

sai_get_vlan_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saivlan.h: 537

sai_create_vlan_member_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saivlan.h: 552

sai_remove_vlan_member_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t)# /home/bluecmd/Downloads/SAI/inc/saivlan.h: 565

sai_set_vlan_member_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saivlan.h: 576

sai_get_vlan_member_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saivlan.h: 589

sai_get_vlan_stats_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, uint32_t, POINTER(sai_stat_id_t), POINTER(uint64_t))# /home/bluecmd/Downloads/SAI/inc/saivlan.h: 604

sai_get_vlan_stats_ext_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, uint32_t, POINTER(sai_stat_id_t), sai_stats_mode_t, POINTER(uint64_t))# /home/bluecmd/Downloads/SAI/inc/saivlan.h: 621

sai_clear_vlan_stats_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, uint32_t, POINTER(sai_stat_id_t))# /home/bluecmd/Downloads/SAI/inc/saivlan.h: 637

# /home/bluecmd/Downloads/SAI/inc/saivlan.h: 661
class struct__sai_vlan_api_t(Structure):
    pass

struct__sai_vlan_api_t.__slots__ = [
    'create_vlan',
    'remove_vlan',
    'set_vlan_attribute',
    'get_vlan_attribute',
    'create_vlan_member',
    'remove_vlan_member',
    'set_vlan_member_attribute',
    'get_vlan_member_attribute',
    'create_vlan_members',
    'remove_vlan_members',
    'get_vlan_stats',
    'get_vlan_stats_ext',
    'clear_vlan_stats',
]
struct__sai_vlan_api_t._fields_ = [
    ('create_vlan', sai_create_vlan_fn),
    ('remove_vlan', sai_remove_vlan_fn),
    ('set_vlan_attribute', sai_set_vlan_attribute_fn),
    ('get_vlan_attribute', sai_get_vlan_attribute_fn),
    ('create_vlan_member', sai_create_vlan_member_fn),
    ('remove_vlan_member', sai_remove_vlan_member_fn),
    ('set_vlan_member_attribute', sai_set_vlan_member_attribute_fn),
    ('get_vlan_member_attribute', sai_get_vlan_member_attribute_fn),
    ('create_vlan_members', sai_bulk_object_create_fn),
    ('remove_vlan_members', sai_bulk_object_remove_fn),
    ('get_vlan_stats', sai_get_vlan_stats_fn),
    ('get_vlan_stats_ext', sai_get_vlan_stats_ext_fn),
    ('clear_vlan_stats', sai_clear_vlan_stats_fn),
]

sai_vlan_api_t = struct__sai_vlan_api_t# /home/bluecmd/Downloads/SAI/inc/saivlan.h: 661

enum__sai_ecn_mark_mode_t = c_int# /home/bluecmd/Downloads/SAI/inc/saiwred.h: 65

SAI_ECN_MARK_MODE_NONE = 0# /home/bluecmd/Downloads/SAI/inc/saiwred.h: 65

SAI_ECN_MARK_MODE_GREEN = (SAI_ECN_MARK_MODE_NONE + 1)# /home/bluecmd/Downloads/SAI/inc/saiwred.h: 65

SAI_ECN_MARK_MODE_YELLOW = (SAI_ECN_MARK_MODE_GREEN + 1)# /home/bluecmd/Downloads/SAI/inc/saiwred.h: 65

SAI_ECN_MARK_MODE_RED = (SAI_ECN_MARK_MODE_YELLOW + 1)# /home/bluecmd/Downloads/SAI/inc/saiwred.h: 65

SAI_ECN_MARK_MODE_GREEN_YELLOW = (SAI_ECN_MARK_MODE_RED + 1)# /home/bluecmd/Downloads/SAI/inc/saiwred.h: 65

SAI_ECN_MARK_MODE_GREEN_RED = (SAI_ECN_MARK_MODE_GREEN_YELLOW + 1)# /home/bluecmd/Downloads/SAI/inc/saiwred.h: 65

SAI_ECN_MARK_MODE_YELLOW_RED = (SAI_ECN_MARK_MODE_GREEN_RED + 1)# /home/bluecmd/Downloads/SAI/inc/saiwred.h: 65

SAI_ECN_MARK_MODE_ALL = (SAI_ECN_MARK_MODE_YELLOW_RED + 1)# /home/bluecmd/Downloads/SAI/inc/saiwred.h: 65

sai_ecn_mark_mode_t = enum__sai_ecn_mark_mode_t# /home/bluecmd/Downloads/SAI/inc/saiwred.h: 65

enum__sai_wred_attr_t = c_int# /home/bluecmd/Downloads/SAI/inc/saiwred.h: 626

SAI_WRED_ATTR_START = 0x00000000# /home/bluecmd/Downloads/SAI/inc/saiwred.h: 626

SAI_WRED_ATTR_GREEN_ENABLE = SAI_WRED_ATTR_START# /home/bluecmd/Downloads/SAI/inc/saiwred.h: 626

SAI_WRED_ATTR_GREEN_MIN_THRESHOLD = 0x00000001# /home/bluecmd/Downloads/SAI/inc/saiwred.h: 626

SAI_WRED_ATTR_GREEN_MAX_THRESHOLD = 0x00000002# /home/bluecmd/Downloads/SAI/inc/saiwred.h: 626

SAI_WRED_ATTR_GREEN_DROP_PROBABILITY = 0x00000003# /home/bluecmd/Downloads/SAI/inc/saiwred.h: 626

SAI_WRED_ATTR_YELLOW_ENABLE = 0x00000004# /home/bluecmd/Downloads/SAI/inc/saiwred.h: 626

SAI_WRED_ATTR_YELLOW_MIN_THRESHOLD = 0x00000005# /home/bluecmd/Downloads/SAI/inc/saiwred.h: 626

SAI_WRED_ATTR_YELLOW_MAX_THRESHOLD = 0x00000006# /home/bluecmd/Downloads/SAI/inc/saiwred.h: 626

SAI_WRED_ATTR_YELLOW_DROP_PROBABILITY = 0x00000007# /home/bluecmd/Downloads/SAI/inc/saiwred.h: 626

SAI_WRED_ATTR_RED_ENABLE = 0x00000008# /home/bluecmd/Downloads/SAI/inc/saiwred.h: 626

SAI_WRED_ATTR_RED_MIN_THRESHOLD = 0x00000009# /home/bluecmd/Downloads/SAI/inc/saiwred.h: 626

SAI_WRED_ATTR_RED_MAX_THRESHOLD = 0x0000000a# /home/bluecmd/Downloads/SAI/inc/saiwred.h: 626

SAI_WRED_ATTR_RED_DROP_PROBABILITY = 0x0000000b# /home/bluecmd/Downloads/SAI/inc/saiwred.h: 626

SAI_WRED_ATTR_WEIGHT = 0x0000000c# /home/bluecmd/Downloads/SAI/inc/saiwred.h: 626

SAI_WRED_ATTR_ECN_MARK_MODE = 0x0000000d# /home/bluecmd/Downloads/SAI/inc/saiwred.h: 626

SAI_WRED_ATTR_ECN_GREEN_MIN_THRESHOLD = 0x0000000e# /home/bluecmd/Downloads/SAI/inc/saiwred.h: 626

SAI_WRED_ATTR_ECN_GREEN_MAX_THRESHOLD = 0x0000000f# /home/bluecmd/Downloads/SAI/inc/saiwred.h: 626

SAI_WRED_ATTR_ECN_GREEN_MARK_PROBABILITY = 0x00000010# /home/bluecmd/Downloads/SAI/inc/saiwred.h: 626

SAI_WRED_ATTR_ECN_YELLOW_MIN_THRESHOLD = 0x00000011# /home/bluecmd/Downloads/SAI/inc/saiwred.h: 626

SAI_WRED_ATTR_ECN_YELLOW_MAX_THRESHOLD = 0x00000012# /home/bluecmd/Downloads/SAI/inc/saiwred.h: 626

SAI_WRED_ATTR_ECN_YELLOW_MARK_PROBABILITY = 0x00000013# /home/bluecmd/Downloads/SAI/inc/saiwred.h: 626

SAI_WRED_ATTR_ECN_RED_MIN_THRESHOLD = 0x00000014# /home/bluecmd/Downloads/SAI/inc/saiwred.h: 626

SAI_WRED_ATTR_ECN_RED_MAX_THRESHOLD = 0x00000015# /home/bluecmd/Downloads/SAI/inc/saiwred.h: 626

SAI_WRED_ATTR_ECN_RED_MARK_PROBABILITY = 0x00000016# /home/bluecmd/Downloads/SAI/inc/saiwred.h: 626

SAI_WRED_ATTR_ECN_COLOR_UNAWARE_MIN_THRESHOLD = 0x00000017# /home/bluecmd/Downloads/SAI/inc/saiwred.h: 626

SAI_WRED_ATTR_ECN_COLOR_UNAWARE_MAX_THRESHOLD = 0x00000018# /home/bluecmd/Downloads/SAI/inc/saiwred.h: 626

SAI_WRED_ATTR_ECN_COLOR_UNAWARE_MARK_PROBABILITY = 0x00000019# /home/bluecmd/Downloads/SAI/inc/saiwred.h: 626

SAI_WRED_ATTR_GREEN_MIN_THRESHOLD_64 = 0x0000001a# /home/bluecmd/Downloads/SAI/inc/saiwred.h: 626

SAI_WRED_ATTR_GREEN_MAX_THRESHOLD_64 = 0x0000001b# /home/bluecmd/Downloads/SAI/inc/saiwred.h: 626

SAI_WRED_ATTR_YELLOW_MIN_THRESHOLD_64 = 0x0000001c# /home/bluecmd/Downloads/SAI/inc/saiwred.h: 626

SAI_WRED_ATTR_YELLOW_MAX_THRESHOLD_64 = 0x0000001d# /home/bluecmd/Downloads/SAI/inc/saiwred.h: 626

SAI_WRED_ATTR_RED_MIN_THRESHOLD_64 = 0x0000001e# /home/bluecmd/Downloads/SAI/inc/saiwred.h: 626

SAI_WRED_ATTR_RED_MAX_THRESHOLD_64 = 0x0000001f# /home/bluecmd/Downloads/SAI/inc/saiwred.h: 626

SAI_WRED_ATTR_ECN_GREEN_MIN_THRESHOLD_64 = 0x00000020# /home/bluecmd/Downloads/SAI/inc/saiwred.h: 626

SAI_WRED_ATTR_ECN_GREEN_MAX_THRESHOLD_64 = 0x00000021# /home/bluecmd/Downloads/SAI/inc/saiwred.h: 626

SAI_WRED_ATTR_ECN_YELLOW_MIN_THRESHOLD_64 = 0x00000022# /home/bluecmd/Downloads/SAI/inc/saiwred.h: 626

SAI_WRED_ATTR_ECN_YELLOW_MAX_THRESHOLD_64 = 0x00000023# /home/bluecmd/Downloads/SAI/inc/saiwred.h: 626

SAI_WRED_ATTR_ECN_RED_MIN_THRESHOLD_64 = 0x00000024# /home/bluecmd/Downloads/SAI/inc/saiwred.h: 626

SAI_WRED_ATTR_ECN_RED_MAX_THRESHOLD_64 = 0x00000025# /home/bluecmd/Downloads/SAI/inc/saiwred.h: 626

SAI_WRED_ATTR_ECN_COLOR_UNAWARE_MIN_THRESHOLD_64 = 0x00000026# /home/bluecmd/Downloads/SAI/inc/saiwred.h: 626

SAI_WRED_ATTR_ECN_COLOR_UNAWARE_MAX_THRESHOLD_64 = 0x00000027# /home/bluecmd/Downloads/SAI/inc/saiwred.h: 626

SAI_WRED_ATTR_END = (SAI_WRED_ATTR_ECN_COLOR_UNAWARE_MAX_THRESHOLD_64 + 1)# /home/bluecmd/Downloads/SAI/inc/saiwred.h: 626

SAI_WRED_ATTR_CUSTOM_RANGE_START = 0x10000000# /home/bluecmd/Downloads/SAI/inc/saiwred.h: 626

SAI_WRED_ATTR_CUSTOM_RANGE_END = (SAI_WRED_ATTR_CUSTOM_RANGE_START + 1)# /home/bluecmd/Downloads/SAI/inc/saiwred.h: 626

sai_wred_attr_t = enum__sai_wred_attr_t# /home/bluecmd/Downloads/SAI/inc/saiwred.h: 626

sai_create_wred_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saiwred.h: 638

sai_remove_wred_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t)# /home/bluecmd/Downloads/SAI/inc/saiwred.h: 651

sai_set_wred_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saiwred.h: 662

sai_get_wred_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saiwred.h: 675

# /home/bluecmd/Downloads/SAI/inc/saiwred.h: 690
class struct__sai_wred_api_t(Structure):
    pass

struct__sai_wred_api_t.__slots__ = [
    'create_wred',
    'remove_wred',
    'set_wred_attribute',
    'get_wred_attribute',
]
struct__sai_wred_api_t._fields_ = [
    ('create_wred', sai_create_wred_fn),
    ('remove_wred', sai_remove_wred_fn),
    ('set_wred_attribute', sai_set_wred_attribute_fn),
    ('get_wred_attribute', sai_get_wred_attribute_fn),
]

sai_wred_api_t = struct__sai_wred_api_t# /home/bluecmd/Downloads/SAI/inc/saiwred.h: 690

enum__sai_isolation_group_type_t = c_int# /home/bluecmd/Downloads/SAI/inc/saiisolationgroup.h: 47

SAI_ISOLATION_GROUP_TYPE_PORT = 0# /home/bluecmd/Downloads/SAI/inc/saiisolationgroup.h: 47

SAI_ISOLATION_GROUP_TYPE_BRIDGE_PORT = (SAI_ISOLATION_GROUP_TYPE_PORT + 1)# /home/bluecmd/Downloads/SAI/inc/saiisolationgroup.h: 47

sai_isolation_group_type_t = enum__sai_isolation_group_type_t# /home/bluecmd/Downloads/SAI/inc/saiisolationgroup.h: 47

enum__sai_isolation_group_attr_t = c_int# /home/bluecmd/Downloads/SAI/inc/saiisolationgroup.h: 87

SAI_ISOLATION_GROUP_ATTR_START = 0# /home/bluecmd/Downloads/SAI/inc/saiisolationgroup.h: 87

SAI_ISOLATION_GROUP_ATTR_TYPE = SAI_ISOLATION_GROUP_ATTR_START# /home/bluecmd/Downloads/SAI/inc/saiisolationgroup.h: 87

SAI_ISOLATION_GROUP_ATTR_ISOLATION_MEMBER_LIST = (SAI_ISOLATION_GROUP_ATTR_TYPE + 1)# /home/bluecmd/Downloads/SAI/inc/saiisolationgroup.h: 87

SAI_ISOLATION_GROUP_ATTR_END = (SAI_ISOLATION_GROUP_ATTR_ISOLATION_MEMBER_LIST + 1)# /home/bluecmd/Downloads/SAI/inc/saiisolationgroup.h: 87

SAI_ISOLATION_GROUP_ATTR_CUSTOM_RANGE_START = 0x10000000# /home/bluecmd/Downloads/SAI/inc/saiisolationgroup.h: 87

SAI_ISOLATION_GROUP_ATTR_CUSTOM_RANGE_END = (SAI_ISOLATION_GROUP_ATTR_CUSTOM_RANGE_START + 1)# /home/bluecmd/Downloads/SAI/inc/saiisolationgroup.h: 87

sai_isolation_group_attr_t = enum__sai_isolation_group_attr_t# /home/bluecmd/Downloads/SAI/inc/saiisolationgroup.h: 87

enum__sai_isolation_group_member_attr_t = c_int# /home/bluecmd/Downloads/SAI/inc/saiisolationgroup.h: 130

SAI_ISOLATION_GROUP_MEMBER_ATTR_START = 0# /home/bluecmd/Downloads/SAI/inc/saiisolationgroup.h: 130

SAI_ISOLATION_GROUP_MEMBER_ATTR_ISOLATION_GROUP_ID = SAI_ISOLATION_GROUP_MEMBER_ATTR_START# /home/bluecmd/Downloads/SAI/inc/saiisolationgroup.h: 130

SAI_ISOLATION_GROUP_MEMBER_ATTR_ISOLATION_OBJECT = (SAI_ISOLATION_GROUP_MEMBER_ATTR_ISOLATION_GROUP_ID + 1)# /home/bluecmd/Downloads/SAI/inc/saiisolationgroup.h: 130

SAI_ISOLATION_GROUP_MEMBER_ATTR_END = (SAI_ISOLATION_GROUP_MEMBER_ATTR_ISOLATION_OBJECT + 1)# /home/bluecmd/Downloads/SAI/inc/saiisolationgroup.h: 130

SAI_ISOLATION_GROUP_MEMBER_ATTR_CUSTOM_RANGE_START = 0x10000000# /home/bluecmd/Downloads/SAI/inc/saiisolationgroup.h: 130

SAI_ISOLATION_GROUP_MEMBER_ATTR_CUSTOM_RANGE_END = (SAI_ISOLATION_GROUP_MEMBER_ATTR_CUSTOM_RANGE_START + 1)# /home/bluecmd/Downloads/SAI/inc/saiisolationgroup.h: 130

sai_isolation_group_member_attr_t = enum__sai_isolation_group_member_attr_t# /home/bluecmd/Downloads/SAI/inc/saiisolationgroup.h: 130

sai_create_isolation_group_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saiisolationgroup.h: 142

sai_remove_isolation_group_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t)# /home/bluecmd/Downloads/SAI/inc/saiisolationgroup.h: 155

sai_set_isolation_group_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saiisolationgroup.h: 166

sai_get_isolation_group_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saiisolationgroup.h: 179

sai_create_isolation_group_member_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saiisolationgroup.h: 194

sai_remove_isolation_group_member_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t)# /home/bluecmd/Downloads/SAI/inc/saiisolationgroup.h: 207

sai_set_isolation_group_member_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saiisolationgroup.h: 218

sai_get_isolation_group_member_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saiisolationgroup.h: 231

# /home/bluecmd/Downloads/SAI/inc/saiisolationgroup.h: 250
class struct__sai_isolation_group_api_t(Structure):
    pass

struct__sai_isolation_group_api_t.__slots__ = [
    'create_isolation_group',
    'remove_isolation_group',
    'set_isolation_group_attribute',
    'get_isolation_group_attribute',
    'create_isolation_group_member',
    'remove_isolation_group_member',
    'set_isolation_group_member_attribute',
    'get_isolation_group_member_attribute',
]
struct__sai_isolation_group_api_t._fields_ = [
    ('create_isolation_group', sai_create_isolation_group_fn),
    ('remove_isolation_group', sai_remove_isolation_group_fn),
    ('set_isolation_group_attribute', sai_set_isolation_group_attribute_fn),
    ('get_isolation_group_attribute', sai_get_isolation_group_attribute_fn),
    ('create_isolation_group_member', sai_create_isolation_group_member_fn),
    ('remove_isolation_group_member', sai_remove_isolation_group_member_fn),
    ('set_isolation_group_member_attribute', sai_set_isolation_group_member_attribute_fn),
    ('get_isolation_group_member_attribute', sai_get_isolation_group_member_attribute_fn),
]

sai_isolation_group_api_t = struct__sai_isolation_group_api_t# /home/bluecmd/Downloads/SAI/inc/saiisolationgroup.h: 250

enum__sai_my_mac_attr_t = c_int# /home/bluecmd/Downloads/SAI/inc/saimymac.h: 106

SAI_MY_MAC_ATTR_START = 0# /home/bluecmd/Downloads/SAI/inc/saimymac.h: 106

SAI_MY_MAC_ATTR_PRIORITY = SAI_MY_MAC_ATTR_START# /home/bluecmd/Downloads/SAI/inc/saimymac.h: 106

SAI_MY_MAC_ATTR_PORT_ID = (SAI_MY_MAC_ATTR_PRIORITY + 1)# /home/bluecmd/Downloads/SAI/inc/saimymac.h: 106

SAI_MY_MAC_ATTR_VLAN_ID = (SAI_MY_MAC_ATTR_PORT_ID + 1)# /home/bluecmd/Downloads/SAI/inc/saimymac.h: 106

SAI_MY_MAC_ATTR_MAC_ADDRESS = (SAI_MY_MAC_ATTR_VLAN_ID + 1)# /home/bluecmd/Downloads/SAI/inc/saimymac.h: 106

SAI_MY_MAC_ATTR_MAC_ADDRESS_MASK = (SAI_MY_MAC_ATTR_MAC_ADDRESS + 1)# /home/bluecmd/Downloads/SAI/inc/saimymac.h: 106

SAI_MY_MAC_ATTR_END = (SAI_MY_MAC_ATTR_MAC_ADDRESS_MASK + 1)# /home/bluecmd/Downloads/SAI/inc/saimymac.h: 106

SAI_MY_MAC_ATTR_CUSTOM_RANGE_START = 0x10000000# /home/bluecmd/Downloads/SAI/inc/saimymac.h: 106

SAI_MY_MAC_ATTR_CUSTOM_RANGE_END = (SAI_MY_MAC_ATTR_CUSTOM_RANGE_START + 1)# /home/bluecmd/Downloads/SAI/inc/saimymac.h: 106

sai_my_mac_attr_t = enum__sai_my_mac_attr_t# /home/bluecmd/Downloads/SAI/inc/saimymac.h: 106

sai_create_my_mac_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saimymac.h: 118

sai_remove_my_mac_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t)# /home/bluecmd/Downloads/SAI/inc/saimymac.h: 131

sai_set_my_mac_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saimymac.h: 142

sai_get_my_mac_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saimymac.h: 155

# /home/bluecmd/Downloads/SAI/inc/saimymac.h: 170
class struct__sai_my_mac_api_t(Structure):
    pass

struct__sai_my_mac_api_t.__slots__ = [
    'create_my_mac',
    'remove_my_mac',
    'set_my_mac_attribute',
    'get_my_mac_attribute',
]
struct__sai_my_mac_api_t._fields_ = [
    ('create_my_mac', sai_create_my_mac_fn),
    ('remove_my_mac', sai_remove_my_mac_fn),
    ('set_my_mac_attribute', sai_set_my_mac_attribute_fn),
    ('get_my_mac_attribute', sai_get_my_mac_attribute_fn),
]

sai_my_mac_api_t = struct__sai_my_mac_api_t# /home/bluecmd/Downloads/SAI/inc/saimymac.h: 170

enum__sai_twamp_session_auth_mode_t = c_int# /home/bluecmd/Downloads/SAI/inc/saitwamp.h: 51

SAI_TWAMP_SESSION_AUTH_MODE_UNAUTHENTICATED = 0# /home/bluecmd/Downloads/SAI/inc/saitwamp.h: 51

SAI_TWAMP_SESSION_AUTH_MODE_AUTHENTICATED = (SAI_TWAMP_SESSION_AUTH_MODE_UNAUTHENTICATED + 1)# /home/bluecmd/Downloads/SAI/inc/saitwamp.h: 51

SAI_TWAMP_SESSION_AUTH_MODE_ENCRYPTED = (SAI_TWAMP_SESSION_AUTH_MODE_AUTHENTICATED + 1)# /home/bluecmd/Downloads/SAI/inc/saitwamp.h: 51

sai_twamp_session_auth_mode_t = enum__sai_twamp_session_auth_mode_t# /home/bluecmd/Downloads/SAI/inc/saitwamp.h: 51

enum__sai_twamp_session_role_t = c_int# /home/bluecmd/Downloads/SAI/inc/saitwamp.h: 64

SAI_TWAMP_SESSION_ROLE_SENDER = 0# /home/bluecmd/Downloads/SAI/inc/saitwamp.h: 64

SAI_TWAMP_SESSION_ROLE_REFLECTOR = (SAI_TWAMP_SESSION_ROLE_SENDER + 1)# /home/bluecmd/Downloads/SAI/inc/saitwamp.h: 64

sai_twamp_session_role_t = enum__sai_twamp_session_role_t# /home/bluecmd/Downloads/SAI/inc/saitwamp.h: 64

enum__sai_twamp_mode_t = c_int# /home/bluecmd/Downloads/SAI/inc/saitwamp.h: 81

SAI_TWAMP_MODE_FULL = 0# /home/bluecmd/Downloads/SAI/inc/saitwamp.h: 81

SAI_TWAMP_MODE_LIGHT = (SAI_TWAMP_MODE_FULL + 1)# /home/bluecmd/Downloads/SAI/inc/saitwamp.h: 81

sai_twamp_mode_t = enum__sai_twamp_mode_t# /home/bluecmd/Downloads/SAI/inc/saitwamp.h: 81

enum__sai_twamp_pkt_tx_mode_t = c_int# /home/bluecmd/Downloads/SAI/inc/saitwamp.h: 97

SAI_TWAMP_PKT_TX_MODE_CONTINUOUS = 0# /home/bluecmd/Downloads/SAI/inc/saitwamp.h: 97

SAI_TWAMP_PKT_TX_MODE_PACKET_COUNT = (SAI_TWAMP_PKT_TX_MODE_CONTINUOUS + 1)# /home/bluecmd/Downloads/SAI/inc/saitwamp.h: 97

SAI_TWAMP_PKT_TX_MODE_PERIOD = (SAI_TWAMP_PKT_TX_MODE_PACKET_COUNT + 1)# /home/bluecmd/Downloads/SAI/inc/saitwamp.h: 97

sai_twamp_pkt_tx_mode_t = enum__sai_twamp_pkt_tx_mode_t# /home/bluecmd/Downloads/SAI/inc/saitwamp.h: 97

enum__sai_twamp_timestamp_format_t = c_int# /home/bluecmd/Downloads/SAI/inc/saitwamp.h: 114

SAI_TWAMP_TIMESTAMP_FORMAT_NTP = 0# /home/bluecmd/Downloads/SAI/inc/saitwamp.h: 114

SAI_TWAMP_TIMESTAMP_FORMAT_PTP = (SAI_TWAMP_TIMESTAMP_FORMAT_NTP + 1)# /home/bluecmd/Downloads/SAI/inc/saitwamp.h: 114

sai_twamp_timestamp_format_t = enum__sai_twamp_timestamp_format_t# /home/bluecmd/Downloads/SAI/inc/saitwamp.h: 114

enum__sai_twamp_encapsulation_type_t = c_int# /home/bluecmd/Downloads/SAI/inc/saitwamp.h: 141

SAI_TWAMP_ENCAPSULATION_TYPE_IP = 0# /home/bluecmd/Downloads/SAI/inc/saitwamp.h: 141

SAI_TWAMP_ENCAPSULATION_TYPE_MPLS_L2VPN = (SAI_TWAMP_ENCAPSULATION_TYPE_IP + 1)# /home/bluecmd/Downloads/SAI/inc/saitwamp.h: 141

SAI_TWAMP_ENCAPSULATION_TYPE_MPLS_L3VPN = (SAI_TWAMP_ENCAPSULATION_TYPE_MPLS_L2VPN + 1)# /home/bluecmd/Downloads/SAI/inc/saitwamp.h: 141

SAI_TWAMP_ENCAPSULATION_TYPE_VXLAN = (SAI_TWAMP_ENCAPSULATION_TYPE_MPLS_L3VPN + 1)# /home/bluecmd/Downloads/SAI/inc/saitwamp.h: 141

sai_twamp_encapsulation_type_t = enum__sai_twamp_encapsulation_type_t# /home/bluecmd/Downloads/SAI/inc/saitwamp.h: 141

enum__sai_twamp_session_attr_t = c_int# /home/bluecmd/Downloads/SAI/inc/saitwamp.h: 568

SAI_TWAMP_SESSION_ATTR_START = 0# /home/bluecmd/Downloads/SAI/inc/saitwamp.h: 568

SAI_TWAMP_SESSION_ATTR_TWAMP_MODE = SAI_TWAMP_SESSION_ATTR_START# /home/bluecmd/Downloads/SAI/inc/saitwamp.h: 568

SAI_TWAMP_SESSION_ATTR_SESSION_ROLE = (SAI_TWAMP_SESSION_ATTR_TWAMP_MODE + 1)# /home/bluecmd/Downloads/SAI/inc/saitwamp.h: 568

SAI_TWAMP_SESSION_ATTR_AUTH_MODE = (SAI_TWAMP_SESSION_ATTR_SESSION_ROLE + 1)# /home/bluecmd/Downloads/SAI/inc/saitwamp.h: 568

SAI_TWAMP_SESSION_ATTR_HW_LOOKUP_VALID = (SAI_TWAMP_SESSION_ATTR_AUTH_MODE + 1)# /home/bluecmd/Downloads/SAI/inc/saitwamp.h: 568

SAI_TWAMP_SESSION_ATTR_VIRTUAL_ROUTER = (SAI_TWAMP_SESSION_ATTR_HW_LOOKUP_VALID + 1)# /home/bluecmd/Downloads/SAI/inc/saitwamp.h: 568

SAI_TWAMP_SESSION_ATTR_SRC_MAC = (SAI_TWAMP_SESSION_ATTR_VIRTUAL_ROUTER + 1)# /home/bluecmd/Downloads/SAI/inc/saitwamp.h: 568

SAI_TWAMP_SESSION_ATTR_DST_MAC = (SAI_TWAMP_SESSION_ATTR_SRC_MAC + 1)# /home/bluecmd/Downloads/SAI/inc/saitwamp.h: 568

SAI_TWAMP_SESSION_ATTR_VLAN_ID = (SAI_TWAMP_SESSION_ATTR_DST_MAC + 1)# /home/bluecmd/Downloads/SAI/inc/saitwamp.h: 568

SAI_TWAMP_SESSION_ATTR_VLAN_PRI = (SAI_TWAMP_SESSION_ATTR_VLAN_ID + 1)# /home/bluecmd/Downloads/SAI/inc/saitwamp.h: 568

SAI_TWAMP_SESSION_ATTR_VLAN_CFI = (SAI_TWAMP_SESSION_ATTR_VLAN_PRI + 1)# /home/bluecmd/Downloads/SAI/inc/saitwamp.h: 568

SAI_TWAMP_SESSION_ATTR_VLAN_HEADER_VALID = (SAI_TWAMP_SESSION_ATTR_VLAN_CFI + 1)# /home/bluecmd/Downloads/SAI/inc/saitwamp.h: 568

SAI_TWAMP_SESSION_ATTR_SRC_IP = (SAI_TWAMP_SESSION_ATTR_VLAN_HEADER_VALID + 1)# /home/bluecmd/Downloads/SAI/inc/saitwamp.h: 568

SAI_TWAMP_SESSION_ATTR_DST_IP = (SAI_TWAMP_SESSION_ATTR_SRC_IP + 1)# /home/bluecmd/Downloads/SAI/inc/saitwamp.h: 568

SAI_TWAMP_SESSION_ATTR_UDP_SRC_PORT = (SAI_TWAMP_SESSION_ATTR_DST_IP + 1)# /home/bluecmd/Downloads/SAI/inc/saitwamp.h: 568

SAI_TWAMP_SESSION_ATTR_UDP_DST_PORT = (SAI_TWAMP_SESSION_ATTR_UDP_SRC_PORT + 1)# /home/bluecmd/Downloads/SAI/inc/saitwamp.h: 568

SAI_TWAMP_SESSION_ATTR_DSCP = (SAI_TWAMP_SESSION_ATTR_UDP_DST_PORT + 1)# /home/bluecmd/Downloads/SAI/inc/saitwamp.h: 568

SAI_TWAMP_SESSION_ATTR_TTL = (SAI_TWAMP_SESSION_ATTR_DSCP + 1)# /home/bluecmd/Downloads/SAI/inc/saitwamp.h: 568

SAI_TWAMP_SESSION_ATTR_TUNNEL_SRC_MAC = (SAI_TWAMP_SESSION_ATTR_TTL + 1)# /home/bluecmd/Downloads/SAI/inc/saitwamp.h: 568

SAI_TWAMP_SESSION_ATTR_TUNNEL_DST_MAC = (SAI_TWAMP_SESSION_ATTR_TUNNEL_SRC_MAC + 1)# /home/bluecmd/Downloads/SAI/inc/saitwamp.h: 568

SAI_TWAMP_SESSION_ATTR_TUNNEL_OUTER_VLAN_ID = (SAI_TWAMP_SESSION_ATTR_TUNNEL_DST_MAC + 1)# /home/bluecmd/Downloads/SAI/inc/saitwamp.h: 568

SAI_TWAMP_SESSION_ATTR_TUNNEL_OUTER_VLAN_PRI = (SAI_TWAMP_SESSION_ATTR_TUNNEL_OUTER_VLAN_ID + 1)# /home/bluecmd/Downloads/SAI/inc/saitwamp.h: 568

SAI_TWAMP_SESSION_ATTR_TUNNEL_OUTER_VLAN_CFI = (SAI_TWAMP_SESSION_ATTR_TUNNEL_OUTER_VLAN_PRI + 1)# /home/bluecmd/Downloads/SAI/inc/saitwamp.h: 568

SAI_TWAMP_SESSION_ATTR_TUNNEL_OUTER_VLAN_HEADER_VALID = (SAI_TWAMP_SESSION_ATTR_TUNNEL_OUTER_VLAN_CFI + 1)# /home/bluecmd/Downloads/SAI/inc/saitwamp.h: 568

SAI_TWAMP_SESSION_ATTR_TUNNEL_LABELSTACK = (SAI_TWAMP_SESSION_ATTR_TUNNEL_OUTER_VLAN_HEADER_VALID + 1)# /home/bluecmd/Downloads/SAI/inc/saitwamp.h: 568

SAI_TWAMP_SESSION_ATTR_TUNNEL_SRC_IP = (SAI_TWAMP_SESSION_ATTR_TUNNEL_LABELSTACK + 1)# /home/bluecmd/Downloads/SAI/inc/saitwamp.h: 568

SAI_TWAMP_SESSION_ATTR_TUNNEL_DST_IP = (SAI_TWAMP_SESSION_ATTR_TUNNEL_SRC_IP + 1)# /home/bluecmd/Downloads/SAI/inc/saitwamp.h: 568

SAI_TWAMP_SESSION_ATTR_TUNNEL_VNI = (SAI_TWAMP_SESSION_ATTR_TUNNEL_DST_IP + 1)# /home/bluecmd/Downloads/SAI/inc/saitwamp.h: 568

SAI_TWAMP_SESSION_ATTR_TUNNEL_UDP_SRC_PORT = (SAI_TWAMP_SESSION_ATTR_TUNNEL_VNI + 1)# /home/bluecmd/Downloads/SAI/inc/saitwamp.h: 568

SAI_TWAMP_SESSION_ATTR_TUNNEL_UDP_DST_PORT = (SAI_TWAMP_SESSION_ATTR_TUNNEL_UDP_SRC_PORT + 1)# /home/bluecmd/Downloads/SAI/inc/saitwamp.h: 568

SAI_TWAMP_SESSION_ATTR_TWAMP_ENCAPSULATION_TYPE = (SAI_TWAMP_SESSION_ATTR_TUNNEL_UDP_DST_PORT + 1)# /home/bluecmd/Downloads/SAI/inc/saitwamp.h: 568

SAI_TWAMP_SESSION_ATTR_TWAMP_TIMESTAMP_FORMAT = (SAI_TWAMP_SESSION_ATTR_TWAMP_ENCAPSULATION_TYPE + 1)# /home/bluecmd/Downloads/SAI/inc/saitwamp.h: 568

SAI_TWAMP_SESSION_ATTR_SESSION_ENABLE_TRANSMIT = (SAI_TWAMP_SESSION_ATTR_TWAMP_TIMESTAMP_FORMAT + 1)# /home/bluecmd/Downloads/SAI/inc/saitwamp.h: 568

SAI_TWAMP_SESSION_ATTR_PACKET_LENGTH = (SAI_TWAMP_SESSION_ATTR_SESSION_ENABLE_TRANSMIT + 1)# /home/bluecmd/Downloads/SAI/inc/saitwamp.h: 568

SAI_TWAMP_SESSION_ATTR_PORT = (SAI_TWAMP_SESSION_ATTR_PACKET_LENGTH + 1)# /home/bluecmd/Downloads/SAI/inc/saitwamp.h: 568

SAI_TWAMP_SESSION_ATTR_TRANSMIT_PORT = (SAI_TWAMP_SESSION_ATTR_PORT + 1)# /home/bluecmd/Downloads/SAI/inc/saitwamp.h: 568

SAI_TWAMP_SESSION_ATTR_RECEIVE_PORT = (SAI_TWAMP_SESSION_ATTR_TRANSMIT_PORT + 1)# /home/bluecmd/Downloads/SAI/inc/saitwamp.h: 568

SAI_TWAMP_SESSION_ATTR_TWAMP_PKT_TX_MODE = (SAI_TWAMP_SESSION_ATTR_RECEIVE_PORT + 1)# /home/bluecmd/Downloads/SAI/inc/saitwamp.h: 568

SAI_TWAMP_SESSION_ATTR_TX_PKT_CNT = (SAI_TWAMP_SESSION_ATTR_TWAMP_PKT_TX_MODE + 1)# /home/bluecmd/Downloads/SAI/inc/saitwamp.h: 568

SAI_TWAMP_SESSION_ATTR_TX_PKT_PERIOD = (SAI_TWAMP_SESSION_ATTR_TX_PKT_CNT + 1)# /home/bluecmd/Downloads/SAI/inc/saitwamp.h: 568

SAI_TWAMP_SESSION_ATTR_TX_INTERVAL = (SAI_TWAMP_SESSION_ATTR_TX_PKT_PERIOD + 1)# /home/bluecmd/Downloads/SAI/inc/saitwamp.h: 568

SAI_TWAMP_SESSION_ATTR_TIMEOUT = (SAI_TWAMP_SESSION_ATTR_TX_INTERVAL + 1)# /home/bluecmd/Downloads/SAI/inc/saitwamp.h: 568

SAI_TWAMP_SESSION_ATTR_STATISTICS_INTERVAL = (SAI_TWAMP_SESSION_ATTR_TIMEOUT + 1)# /home/bluecmd/Downloads/SAI/inc/saitwamp.h: 568

SAI_TWAMP_SESSION_ATTR_END = (SAI_TWAMP_SESSION_ATTR_STATISTICS_INTERVAL + 1)# /home/bluecmd/Downloads/SAI/inc/saitwamp.h: 568

SAI_TWAMP_SESSION_ATTR_CUSTOM_RANGE_START = 0x10000000# /home/bluecmd/Downloads/SAI/inc/saitwamp.h: 568

SAI_TWAMP_SESSION_ATTR_CUSTOM_RANGE_END = (SAI_TWAMP_SESSION_ATTR_CUSTOM_RANGE_START + 1)# /home/bluecmd/Downloads/SAI/inc/saitwamp.h: 568

sai_twamp_session_attr_t = enum__sai_twamp_session_attr_t# /home/bluecmd/Downloads/SAI/inc/saitwamp.h: 568

enum__sai_twamp_session_stat_t = c_int# /home/bluecmd/Downloads/SAI/inc/saitwamp.h: 617

SAI_TWAMP_SESSION_STAT_RX_PACKETS = 0# /home/bluecmd/Downloads/SAI/inc/saitwamp.h: 617

SAI_TWAMP_SESSION_STAT_RX_BYTE = (SAI_TWAMP_SESSION_STAT_RX_PACKETS + 1)# /home/bluecmd/Downloads/SAI/inc/saitwamp.h: 617

SAI_TWAMP_SESSION_STAT_TX_PACKETS = (SAI_TWAMP_SESSION_STAT_RX_BYTE + 1)# /home/bluecmd/Downloads/SAI/inc/saitwamp.h: 617

SAI_TWAMP_SESSION_STAT_TX_BYTE = (SAI_TWAMP_SESSION_STAT_TX_PACKETS + 1)# /home/bluecmd/Downloads/SAI/inc/saitwamp.h: 617

SAI_TWAMP_SESSION_STAT_DROP_PACKETS = (SAI_TWAMP_SESSION_STAT_TX_BYTE + 1)# /home/bluecmd/Downloads/SAI/inc/saitwamp.h: 617

SAI_TWAMP_SESSION_STAT_MAX_LATENCY = (SAI_TWAMP_SESSION_STAT_DROP_PACKETS + 1)# /home/bluecmd/Downloads/SAI/inc/saitwamp.h: 617

SAI_TWAMP_SESSION_STAT_MIN_LATENCY = (SAI_TWAMP_SESSION_STAT_MAX_LATENCY + 1)# /home/bluecmd/Downloads/SAI/inc/saitwamp.h: 617

SAI_TWAMP_SESSION_STAT_AVG_LATENCY = (SAI_TWAMP_SESSION_STAT_MIN_LATENCY + 1)# /home/bluecmd/Downloads/SAI/inc/saitwamp.h: 617

SAI_TWAMP_SESSION_STAT_MAX_JITTER = (SAI_TWAMP_SESSION_STAT_AVG_LATENCY + 1)# /home/bluecmd/Downloads/SAI/inc/saitwamp.h: 617

SAI_TWAMP_SESSION_STAT_MIN_JITTER = (SAI_TWAMP_SESSION_STAT_MAX_JITTER + 1)# /home/bluecmd/Downloads/SAI/inc/saitwamp.h: 617

SAI_TWAMP_SESSION_STAT_AVG_JITTER = (SAI_TWAMP_SESSION_STAT_MIN_JITTER + 1)# /home/bluecmd/Downloads/SAI/inc/saitwamp.h: 617

SAI_TWAMP_SESSION_STAT_FIRST_TS = (SAI_TWAMP_SESSION_STAT_AVG_JITTER + 1)# /home/bluecmd/Downloads/SAI/inc/saitwamp.h: 617

SAI_TWAMP_SESSION_STAT_LAST_TS = (SAI_TWAMP_SESSION_STAT_FIRST_TS + 1)# /home/bluecmd/Downloads/SAI/inc/saitwamp.h: 617

SAI_TWAMP_SESSION_STAT_DURATION_TS = (SAI_TWAMP_SESSION_STAT_LAST_TS + 1)# /home/bluecmd/Downloads/SAI/inc/saitwamp.h: 617

sai_twamp_session_stat_t = enum__sai_twamp_session_stat_t# /home/bluecmd/Downloads/SAI/inc/saitwamp.h: 617

enum__sai_twamp_session_state_t = c_int# /home/bluecmd/Downloads/SAI/inc/saitwamp.h: 630

SAI_TWAMP_SESSION_STATE_INACTIVE = 0# /home/bluecmd/Downloads/SAI/inc/saitwamp.h: 630

SAI_TWAMP_SESSION_STATE_ACTIVE = (SAI_TWAMP_SESSION_STATE_INACTIVE + 1)# /home/bluecmd/Downloads/SAI/inc/saitwamp.h: 630

sai_twamp_session_state_t = enum__sai_twamp_session_state_t# /home/bluecmd/Downloads/SAI/inc/saitwamp.h: 630

# /home/bluecmd/Downloads/SAI/inc/saitwamp.h: 652
class struct__sai_twamp_session_stats_data_t(Structure):
    pass

struct__sai_twamp_session_stats_data_t.__slots__ = [
    'index',
    'number_of_counters',
    'counters_ids',
    'counters',
]
struct__sai_twamp_session_stats_data_t._fields_ = [
    ('index', uint32_t),
    ('number_of_counters', uint32_t),
    ('counters_ids', POINTER(sai_twamp_session_stat_t)),
    ('counters', POINTER(uint64_t)),
]

sai_twamp_session_stats_data_t = struct__sai_twamp_session_stats_data_t# /home/bluecmd/Downloads/SAI/inc/saitwamp.h: 652

# /home/bluecmd/Downloads/SAI/inc/saitwamp.h: 672
class struct__sai_twamp_session_event_notification_data_t(Structure):
    pass

struct__sai_twamp_session_event_notification_data_t.__slots__ = [
    'twamp_session_id',
    'session_state',
    'session_stats',
]
struct__sai_twamp_session_event_notification_data_t._fields_ = [
    ('twamp_session_id', sai_object_id_t),
    ('session_state', sai_twamp_session_state_t),
    ('session_stats', sai_twamp_session_stats_data_t),
]

sai_twamp_session_event_notification_data_t = struct__sai_twamp_session_event_notification_data_t# /home/bluecmd/Downloads/SAI/inc/saitwamp.h: 672

sai_create_twamp_session_fn = CFUNCTYPE(UNCHECKED(sai_status_t), POINTER(sai_object_id_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saitwamp.h: 685

sai_remove_twamp_session_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t)# /home/bluecmd/Downloads/SAI/inc/saitwamp.h: 699

sai_set_twamp_session_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saitwamp.h: 711

sai_get_twamp_session_attribute_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, uint32_t, POINTER(sai_attribute_t))# /home/bluecmd/Downloads/SAI/inc/saitwamp.h: 725

sai_get_twamp_session_stats_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, uint32_t, POINTER(sai_stat_id_t), POINTER(uint64_t))# /home/bluecmd/Downloads/SAI/inc/saitwamp.h: 740

sai_get_twamp_session_stats_ext_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, uint32_t, POINTER(sai_stat_id_t), sai_stats_mode_t, POINTER(uint64_t))# /home/bluecmd/Downloads/SAI/inc/saitwamp.h: 757

sai_clear_twamp_session_stats_fn = CFUNCTYPE(UNCHECKED(sai_status_t), sai_object_id_t, uint32_t, POINTER(sai_stat_id_t))# /home/bluecmd/Downloads/SAI/inc/saitwamp.h: 773

sai_twamp_session_event_notification_fn = CFUNCTYPE(UNCHECKED(None), uint32_t, POINTER(sai_twamp_session_event_notification_data_t))# /home/bluecmd/Downloads/SAI/inc/saitwamp.h: 786

# /home/bluecmd/Downloads/SAI/inc/saitwamp.h: 803
class struct__sai_twamp_api_t(Structure):
    pass

struct__sai_twamp_api_t.__slots__ = [
    'create_twamp_session',
    'remove_twamp_session',
    'set_twamp_session_attribute',
    'get_twamp_session_attribute',
    'get_twamp_session_stats',
    'get_twamp_session_stats_ext',
    'clear_twamp_session_stats',
]
struct__sai_twamp_api_t._fields_ = [
    ('create_twamp_session', sai_create_twamp_session_fn),
    ('remove_twamp_session', sai_remove_twamp_session_fn),
    ('set_twamp_session_attribute', sai_set_twamp_session_attribute_fn),
    ('get_twamp_session_attribute', sai_get_twamp_session_attribute_fn),
    ('get_twamp_session_stats', sai_get_twamp_session_stats_fn),
    ('get_twamp_session_stats_ext', sai_get_twamp_session_stats_ext_fn),
    ('clear_twamp_session_stats', sai_clear_twamp_session_stats_fn),
]

sai_twamp_api_t = struct__sai_twamp_api_t# /home/bluecmd/Downloads/SAI/inc/saitwamp.h: 803

# /home/bluecmd/Downloads/SAI/inc/saiversion.h: 45
for _lib in _libs.values():
    if not _lib.has("sai_query_api_version", "cdecl"):
        continue
    sai_query_api_version = _lib.get("sai_query_api_version", "cdecl")
    sai_query_api_version.argtypes = [POINTER(sai_api_version_t)]
    sai_query_api_version.restype = sai_status_t
    break

enum__sai_api_t = c_int# /home/bluecmd/Downloads/SAI/inc/sai.h: 156

SAI_API_UNSPECIFIED = 0# /home/bluecmd/Downloads/SAI/inc/sai.h: 156

SAI_API_SWITCH = 1# /home/bluecmd/Downloads/SAI/inc/sai.h: 156

SAI_API_PORT = 2# /home/bluecmd/Downloads/SAI/inc/sai.h: 156

SAI_API_FDB = 3# /home/bluecmd/Downloads/SAI/inc/sai.h: 156

SAI_API_VLAN = 4# /home/bluecmd/Downloads/SAI/inc/sai.h: 156

SAI_API_VIRTUAL_ROUTER = 5# /home/bluecmd/Downloads/SAI/inc/sai.h: 156

SAI_API_ROUTE = 6# /home/bluecmd/Downloads/SAI/inc/sai.h: 156

SAI_API_NEXT_HOP = 7# /home/bluecmd/Downloads/SAI/inc/sai.h: 156

SAI_API_NEXT_HOP_GROUP = 8# /home/bluecmd/Downloads/SAI/inc/sai.h: 156

SAI_API_ROUTER_INTERFACE = 9# /home/bluecmd/Downloads/SAI/inc/sai.h: 156

SAI_API_NEIGHBOR = 10# /home/bluecmd/Downloads/SAI/inc/sai.h: 156

SAI_API_ACL = 11# /home/bluecmd/Downloads/SAI/inc/sai.h: 156

SAI_API_HOSTIF = 12# /home/bluecmd/Downloads/SAI/inc/sai.h: 156

SAI_API_MIRROR = 13# /home/bluecmd/Downloads/SAI/inc/sai.h: 156

SAI_API_SAMPLEPACKET = 14# /home/bluecmd/Downloads/SAI/inc/sai.h: 156

SAI_API_STP = 15# /home/bluecmd/Downloads/SAI/inc/sai.h: 156

SAI_API_LAG = 16# /home/bluecmd/Downloads/SAI/inc/sai.h: 156

SAI_API_POLICER = 17# /home/bluecmd/Downloads/SAI/inc/sai.h: 156

SAI_API_WRED = 18# /home/bluecmd/Downloads/SAI/inc/sai.h: 156

SAI_API_QOS_MAP = 19# /home/bluecmd/Downloads/SAI/inc/sai.h: 156

SAI_API_QUEUE = 20# /home/bluecmd/Downloads/SAI/inc/sai.h: 156

SAI_API_SCHEDULER = 21# /home/bluecmd/Downloads/SAI/inc/sai.h: 156

SAI_API_SCHEDULER_GROUP = 22# /home/bluecmd/Downloads/SAI/inc/sai.h: 156

SAI_API_BUFFER = 23# /home/bluecmd/Downloads/SAI/inc/sai.h: 156

SAI_API_HASH = 24# /home/bluecmd/Downloads/SAI/inc/sai.h: 156

SAI_API_UDF = 25# /home/bluecmd/Downloads/SAI/inc/sai.h: 156

SAI_API_TUNNEL = 26# /home/bluecmd/Downloads/SAI/inc/sai.h: 156

SAI_API_L2MC = 27# /home/bluecmd/Downloads/SAI/inc/sai.h: 156

SAI_API_IPMC = 28# /home/bluecmd/Downloads/SAI/inc/sai.h: 156

SAI_API_RPF_GROUP = 29# /home/bluecmd/Downloads/SAI/inc/sai.h: 156

SAI_API_L2MC_GROUP = 30# /home/bluecmd/Downloads/SAI/inc/sai.h: 156

SAI_API_IPMC_GROUP = 31# /home/bluecmd/Downloads/SAI/inc/sai.h: 156

SAI_API_MCAST_FDB = 32# /home/bluecmd/Downloads/SAI/inc/sai.h: 156

SAI_API_BRIDGE = 33# /home/bluecmd/Downloads/SAI/inc/sai.h: 156

SAI_API_TAM = 34# /home/bluecmd/Downloads/SAI/inc/sai.h: 156

SAI_API_SRV6 = 35# /home/bluecmd/Downloads/SAI/inc/sai.h: 156

SAI_API_MPLS = 36# /home/bluecmd/Downloads/SAI/inc/sai.h: 156

SAI_API_DTEL = 37# /home/bluecmd/Downloads/SAI/inc/sai.h: 156

SAI_API_BFD = 38# /home/bluecmd/Downloads/SAI/inc/sai.h: 156

SAI_API_ISOLATION_GROUP = 39# /home/bluecmd/Downloads/SAI/inc/sai.h: 156

SAI_API_NAT = 40# /home/bluecmd/Downloads/SAI/inc/sai.h: 156

SAI_API_COUNTER = 41# /home/bluecmd/Downloads/SAI/inc/sai.h: 156

SAI_API_DEBUG_COUNTER = 42# /home/bluecmd/Downloads/SAI/inc/sai.h: 156

SAI_API_MACSEC = 43# /home/bluecmd/Downloads/SAI/inc/sai.h: 156

SAI_API_SYSTEM_PORT = 44# /home/bluecmd/Downloads/SAI/inc/sai.h: 156

SAI_API_MY_MAC = 45# /home/bluecmd/Downloads/SAI/inc/sai.h: 156

SAI_API_IPSEC = 46# /home/bluecmd/Downloads/SAI/inc/sai.h: 156

SAI_API_GENERIC_PROGRAMMABLE = 47# /home/bluecmd/Downloads/SAI/inc/sai.h: 156

SAI_API_ARS = 48# /home/bluecmd/Downloads/SAI/inc/sai.h: 156

SAI_API_ARS_PROFILE = 49# /home/bluecmd/Downloads/SAI/inc/sai.h: 156

SAI_API_TWAMP = 50# /home/bluecmd/Downloads/SAI/inc/sai.h: 156

SAI_API_MAX = (SAI_API_TWAMP + 1)# /home/bluecmd/Downloads/SAI/inc/sai.h: 156

SAI_API_CUSTOM_RANGE_START = 256# /home/bluecmd/Downloads/SAI/inc/sai.h: 156

SAI_API_CUSTOM_RANGE_END = (SAI_API_CUSTOM_RANGE_START + 1)# /home/bluecmd/Downloads/SAI/inc/sai.h: 156

sai_api_t = enum__sai_api_t# /home/bluecmd/Downloads/SAI/inc/sai.h: 156

enum__sai_log_level_t = c_int# /home/bluecmd/Downloads/SAI/inc/sai.h: 181

SAI_LOG_LEVEL_DEBUG = 0# /home/bluecmd/Downloads/SAI/inc/sai.h: 181

SAI_LOG_LEVEL_INFO = 1# /home/bluecmd/Downloads/SAI/inc/sai.h: 181

SAI_LOG_LEVEL_NOTICE = 2# /home/bluecmd/Downloads/SAI/inc/sai.h: 181

SAI_LOG_LEVEL_WARN = 3# /home/bluecmd/Downloads/SAI/inc/sai.h: 181

SAI_LOG_LEVEL_ERROR = 4# /home/bluecmd/Downloads/SAI/inc/sai.h: 181

SAI_LOG_LEVEL_CRITICAL = 5# /home/bluecmd/Downloads/SAI/inc/sai.h: 181

sai_log_level_t = enum__sai_log_level_t# /home/bluecmd/Downloads/SAI/inc/sai.h: 181

sai_profile_get_value_fn = CFUNCTYPE(UNCHECKED(c_char_p), sai_switch_profile_id_t, String)# /home/bluecmd/Downloads/SAI/inc/sai.h: 183

sai_profile_get_next_value_fn = CFUNCTYPE(UNCHECKED(c_int), sai_switch_profile_id_t, POINTER(POINTER(c_char)), POINTER(POINTER(c_char)))# /home/bluecmd/Downloads/SAI/inc/sai.h: 187

# /home/bluecmd/Downloads/SAI/inc/sai.h: 211
class struct__sai_service_method_table_t(Structure):
    pass

struct__sai_service_method_table_t.__slots__ = [
    'profile_get_value',
    'profile_get_next_value',
]
struct__sai_service_method_table_t._fields_ = [
    ('profile_get_value', sai_profile_get_value_fn),
    ('profile_get_next_value', sai_profile_get_next_value_fn),
]

sai_service_method_table_t = struct__sai_service_method_table_t# /home/bluecmd/Downloads/SAI/inc/sai.h: 211

# /home/bluecmd/Downloads/SAI/inc/sai.h: 223
for _lib in _libs.values():
    if not _lib.has("sai_api_initialize", "cdecl"):
        continue
    sai_api_initialize = _lib.get("sai_api_initialize", "cdecl")
    sai_api_initialize.argtypes = [uint64_t, POINTER(sai_service_method_table_t)]
    sai_api_initialize.restype = sai_status_t
    break

# /home/bluecmd/Downloads/SAI/inc/sai.h: 237
for _lib in _libs.values():
    if not _lib.has("sai_api_query", "cdecl"):
        continue
    sai_api_query = _lib.get("sai_api_query", "cdecl")
    sai_api_query.argtypes = [sai_api_t, POINTER(POINTER(None))]
    sai_api_query.restype = sai_status_t
    break

# /home/bluecmd/Downloads/SAI/inc/sai.h: 247
for _lib in _libs.values():
    if not _lib.has("sai_api_uninitialize", "cdecl"):
        continue
    sai_api_uninitialize = _lib.get("sai_api_uninitialize", "cdecl")
    sai_api_uninitialize.argtypes = []
    sai_api_uninitialize.restype = sai_status_t
    break

# /home/bluecmd/Downloads/SAI/inc/sai.h: 259
for _lib in _libs.values():
    if not _lib.has("sai_log_set", "cdecl"):
        continue
    sai_log_set = _lib.get("sai_log_set", "cdecl")
    sai_log_set.argtypes = [sai_api_t, sai_log_level_t]
    sai_log_set.restype = sai_status_t
    break

# /home/bluecmd/Downloads/SAI/inc/sai.h: 271
for _lib in _libs.values():
    if not _lib.has("sai_object_type_query", "cdecl"):
        continue
    sai_object_type_query = _lib.get("sai_object_type_query", "cdecl")
    sai_object_type_query.argtypes = [sai_object_id_t]
    sai_object_type_query.restype = sai_object_type_t
    break

# /home/bluecmd/Downloads/SAI/inc/sai.h: 284
for _lib in _libs.values():
    if not _lib.has("sai_switch_id_query", "cdecl"):
        continue
    sai_switch_id_query = _lib.get("sai_switch_id_query", "cdecl")
    sai_switch_id_query.argtypes = [sai_object_id_t]
    sai_switch_id_query.restype = sai_object_id_t
    break

# /home/bluecmd/Downloads/SAI/inc/sai.h: 294
for _lib in _libs.values():
    if not _lib.has("sai_dbg_generate_dump", "cdecl"):
        continue
    sai_dbg_generate_dump = _lib.get("sai_dbg_generate_dump", "cdecl")
    sai_dbg_generate_dump.argtypes = [String]
    sai_dbg_generate_dump.restype = sai_status_t
    break

# /home/bluecmd/Downloads/SAI/inc/sai.h: 309
for _lib in _libs.values():
    if not _lib.has("sai_object_type_get_availability", "cdecl"):
        continue
    sai_object_type_get_availability = _lib.get("sai_object_type_get_availability", "cdecl")
    sai_object_type_get_availability.argtypes = [sai_object_id_t, sai_object_type_t, uint32_t, POINTER(sai_attribute_t), POINTER(uint64_t)]
    sai_object_type_get_availability.restype = sai_status_t
    break

# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 145
try:
    SAI_NULL_OBJECT_ID = 0
except:
    pass

# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 554
try:
    SAI_ACL_USER_DEFINED_FIELD_ATTR_ID_RANGE = 0xFF
except:
    pass

# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 46
try:
    SAI_HOSTIF_NAME_SIZE = 16
except:
    pass

# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 51
try:
    SAI_HOSTIF_GENETLINK_MCGRP_NAME_SIZE = 16
except:
    pass

# /home/bluecmd/Downloads/SAI/inc/saistatus.h: 43
def SAI_STATUS_CODE(_S_):
    return (-_S_)

# /home/bluecmd/Downloads/SAI/inc/saistatus.h: 50
try:
    SAI_STATUS_SUCCESS = 0x00000000
except:
    pass

# /home/bluecmd/Downloads/SAI/inc/saistatus.h: 55
try:
    SAI_STATUS_FAILURE = (SAI_STATUS_CODE (0x00000001))
except:
    pass

# /home/bluecmd/Downloads/SAI/inc/saistatus.h: 60
try:
    SAI_STATUS_NOT_SUPPORTED = (SAI_STATUS_CODE (0x00000002))
except:
    pass

# /home/bluecmd/Downloads/SAI/inc/saistatus.h: 65
try:
    SAI_STATUS_NO_MEMORY = (SAI_STATUS_CODE (0x00000003))
except:
    pass

# /home/bluecmd/Downloads/SAI/inc/saistatus.h: 70
try:
    SAI_STATUS_INSUFFICIENT_RESOURCES = (SAI_STATUS_CODE (0x00000004))
except:
    pass

# /home/bluecmd/Downloads/SAI/inc/saistatus.h: 75
try:
    SAI_STATUS_INVALID_PARAMETER = (SAI_STATUS_CODE (0x00000005))
except:
    pass

# /home/bluecmd/Downloads/SAI/inc/saistatus.h: 81
try:
    SAI_STATUS_ITEM_ALREADY_EXISTS = (SAI_STATUS_CODE (0x00000006))
except:
    pass

# /home/bluecmd/Downloads/SAI/inc/saistatus.h: 87
try:
    SAI_STATUS_ITEM_NOT_FOUND = (SAI_STATUS_CODE (0x00000007))
except:
    pass

# /home/bluecmd/Downloads/SAI/inc/saistatus.h: 92
try:
    SAI_STATUS_BUFFER_OVERFLOW = (SAI_STATUS_CODE (0x00000008))
except:
    pass

# /home/bluecmd/Downloads/SAI/inc/saistatus.h: 97
try:
    SAI_STATUS_INVALID_PORT_NUMBER = (SAI_STATUS_CODE (0x00000009))
except:
    pass

# /home/bluecmd/Downloads/SAI/inc/saistatus.h: 102
try:
    SAI_STATUS_INVALID_PORT_MEMBER = (SAI_STATUS_CODE (0x0000000A))
except:
    pass

# /home/bluecmd/Downloads/SAI/inc/saistatus.h: 107
try:
    SAI_STATUS_INVALID_VLAN_ID = (SAI_STATUS_CODE (0x0000000B))
except:
    pass

# /home/bluecmd/Downloads/SAI/inc/saistatus.h: 112
try:
    SAI_STATUS_UNINITIALIZED = (SAI_STATUS_CODE (0x0000000C))
except:
    pass

# /home/bluecmd/Downloads/SAI/inc/saistatus.h: 117
try:
    SAI_STATUS_TABLE_FULL = (SAI_STATUS_CODE (0x0000000D))
except:
    pass

# /home/bluecmd/Downloads/SAI/inc/saistatus.h: 122
try:
    SAI_STATUS_MANDATORY_ATTRIBUTE_MISSING = (SAI_STATUS_CODE (0x0000000E))
except:
    pass

# /home/bluecmd/Downloads/SAI/inc/saistatus.h: 127
try:
    SAI_STATUS_NOT_IMPLEMENTED = (SAI_STATUS_CODE (0x0000000F))
except:
    pass

# /home/bluecmd/Downloads/SAI/inc/saistatus.h: 132
try:
    SAI_STATUS_ADDR_NOT_FOUND = (SAI_STATUS_CODE (0x00000010))
except:
    pass

# /home/bluecmd/Downloads/SAI/inc/saistatus.h: 137
try:
    SAI_STATUS_OBJECT_IN_USE = (SAI_STATUS_CODE (0x00000011))
except:
    pass

# /home/bluecmd/Downloads/SAI/inc/saistatus.h: 145
try:
    SAI_STATUS_INVALID_OBJECT_TYPE = (SAI_STATUS_CODE (0x00000012))
except:
    pass

# /home/bluecmd/Downloads/SAI/inc/saistatus.h: 154
try:
    SAI_STATUS_INVALID_OBJECT_ID = (SAI_STATUS_CODE (0x00000013))
except:
    pass

# /home/bluecmd/Downloads/SAI/inc/saistatus.h: 159
try:
    SAI_STATUS_INVALID_NV_STORAGE = (SAI_STATUS_CODE (0x00000014))
except:
    pass

# /home/bluecmd/Downloads/SAI/inc/saistatus.h: 164
try:
    SAI_STATUS_NV_STORAGE_FULL = (SAI_STATUS_CODE (0x00000015))
except:
    pass

# /home/bluecmd/Downloads/SAI/inc/saistatus.h: 169
try:
    SAI_STATUS_SW_UPGRADE_VERSION_MISMATCH = (SAI_STATUS_CODE (0x00000016))
except:
    pass

# /home/bluecmd/Downloads/SAI/inc/saistatus.h: 174
try:
    SAI_STATUS_NOT_EXECUTED = (SAI_STATUS_CODE (0x00000017))
except:
    pass

# /home/bluecmd/Downloads/SAI/inc/saistatus.h: 179
try:
    SAI_STATUS_STAGE_MISMATCH = (SAI_STATUS_CODE (0x00000018))
except:
    pass

# /home/bluecmd/Downloads/SAI/inc/saistatus.h: 196
try:
    SAI_STATUS_INVALID_ATTRIBUTE_0 = (SAI_STATUS_CODE (0x00010000))
except:
    pass

# /home/bluecmd/Downloads/SAI/inc/saistatus.h: 201
try:
    SAI_STATUS_INVALID_ATTRIBUTE_MAX = (SAI_STATUS_CODE (0x0001FFFF))
except:
    pass

# /home/bluecmd/Downloads/SAI/inc/saistatus.h: 208
try:
    SAI_STATUS_INVALID_ATTR_VALUE_0 = (SAI_STATUS_CODE (0x00020000))
except:
    pass

# /home/bluecmd/Downloads/SAI/inc/saistatus.h: 213
try:
    SAI_STATUS_INVALID_ATTR_VALUE_MAX = (SAI_STATUS_CODE (0x0002FFFF))
except:
    pass

# /home/bluecmd/Downloads/SAI/inc/saistatus.h: 223
try:
    SAI_STATUS_ATTR_NOT_IMPLEMENTED_0 = (SAI_STATUS_CODE (0x00030000))
except:
    pass

# /home/bluecmd/Downloads/SAI/inc/saistatus.h: 228
try:
    SAI_STATUS_ATTR_NOT_IMPLEMENTED_MAX = (SAI_STATUS_CODE (0x0003FFFF))
except:
    pass

# /home/bluecmd/Downloads/SAI/inc/saistatus.h: 238
try:
    SAI_STATUS_UNKNOWN_ATTRIBUTE_0 = (SAI_STATUS_CODE (0x00040000))
except:
    pass

# /home/bluecmd/Downloads/SAI/inc/saistatus.h: 243
try:
    SAI_STATUS_UNKNOWN_ATTRIBUTE_MAX = (SAI_STATUS_CODE (0x0004FFFF))
except:
    pass

# /home/bluecmd/Downloads/SAI/inc/saistatus.h: 253
try:
    SAI_STATUS_ATTR_NOT_SUPPORTED_0 = (SAI_STATUS_CODE (0x00050000))
except:
    pass

# /home/bluecmd/Downloads/SAI/inc/saistatus.h: 258
try:
    SAI_STATUS_ATTR_NOT_SUPPORTED_MAX = (SAI_STATUS_CODE (0x0005FFFF))
except:
    pass

# /home/bluecmd/Downloads/SAI/inc/saistatus.h: 267
def SAI_STATUS_IS_INVALID_ATTRIBUTE(x):
    return ((x & (~0xFFFF)) == SAI_STATUS_INVALID_ATTRIBUTE_0)

# /home/bluecmd/Downloads/SAI/inc/saistatus.h: 272
def SAI_STATUS_IS_INVALID_ATTR_VALUE(x):
    return ((x & (~0xFFFF)) == SAI_STATUS_INVALID_ATTR_VALUE_0)

# /home/bluecmd/Downloads/SAI/inc/saistatus.h: 277
def SAI_STATUS_IS_ATTR_NOT_IMPLEMENTED(x):
    return ((x & (~0xFFFF)) == SAI_STATUS_ATTR_NOT_IMPLEMENTED_0)

# /home/bluecmd/Downloads/SAI/inc/saistatus.h: 282
def SAI_STATUS_IS_UNKNOWN_ATTRIBUTE(x):
    return ((x & (~0xFFFF)) == SAI_STATUS_INVALID_ATTRIBUTE_0)

# /home/bluecmd/Downloads/SAI/inc/saistatus.h: 287
def SAI_STATUS_IS_ATTR_NOT_SUPPORTED(x):
    return ((x & (~0xFFFF)) == SAI_STATUS_ATTR_NOT_SUPPORTED_0)

# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 39
try:
    SAI_MAX_HARDWARE_ID_LEN = 255
except:
    pass

# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3145
try:
    SAI_SWITCH_ATTR_MAX_KEY_STRING_LEN = 64
except:
    pass

# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3154
try:
    SAI_SWITCH_ATTR_MAX_KEY_COUNT = 16
except:
    pass

# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3163
try:
    SAI_KEY_FDB_TABLE_SIZE = 'SAI_FDB_TABLE_SIZE'
except:
    pass

# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3168
try:
    SAI_KEY_L3_ROUTE_TABLE_SIZE = 'SAI_L3_ROUTE_TABLE_SIZE'
except:
    pass

# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3173
try:
    SAI_KEY_L3_NEIGHBOR_TABLE_SIZE = 'SAI_L3_NEIGHBOR_TABLE_SIZE'
except:
    pass

# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3178
try:
    SAI_KEY_NUM_LAG_MEMBERS = 'SAI_NUM_LAG_MEMBERS'
except:
    pass

# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3183
try:
    SAI_KEY_NUM_LAGS = 'SAI_NUM_LAGS'
except:
    pass

# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3188
try:
    SAI_KEY_NUM_ECMP_MEMBERS = 'SAI_NUM_ECMP_MEMBERS'
except:
    pass

# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3193
try:
    SAI_KEY_NUM_ECMP_GROUPS = 'SAI_NUM_ECMP_GROUPS'
except:
    pass

# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3198
try:
    SAI_KEY_NUM_UNICAST_QUEUES = 'SAI_NUM_UNICAST_QUEUES'
except:
    pass

# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3203
try:
    SAI_KEY_NUM_MULTICAST_QUEUES = 'SAI_NUM_MULTICAST_QUEUES'
except:
    pass

# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3208
try:
    SAI_KEY_NUM_QUEUES = 'SAI_NUM_QUEUES'
except:
    pass

# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3213
try:
    SAI_KEY_NUM_CPU_QUEUES = 'SAI_NUM_CPU_QUEUES'
except:
    pass

# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3218
try:
    SAI_KEY_INIT_CONFIG_FILE = 'SAI_INIT_CONFIG_FILE'
except:
    pass

# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3228
try:
    SAI_KEY_BOOT_TYPE = 'SAI_BOOT_TYPE'
except:
    pass

# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3234
try:
    SAI_KEY_WARM_BOOT_READ_FILE = 'SAI_WARM_BOOT_READ_FILE'
except:
    pass

# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3240
try:
    SAI_KEY_WARM_BOOT_WRITE_FILE = 'SAI_WARM_BOOT_WRITE_FILE'
except:
    pass

# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3248
try:
    SAI_KEY_HW_PORT_PROFILE_ID_CONFIG_FILE = 'SAI_HW_PORT_PROFILE_ID_CONFIG_FILE'
except:
    pass

# /home/bluecmd/Downloads/SAI/inc/saivlan.h: 39
try:
    SAI_VLAN_COUNTER_SET_DEFAULT = 0
except:
    pass

# /home/bluecmd/Downloads/SAI/inc/saiversion.h: 30
try:
    SAI_MAJOR = 1
except:
    pass

# /home/bluecmd/Downloads/SAI/inc/saiversion.h: 31
try:
    SAI_MINOR = 13
except:
    pass

# /home/bluecmd/Downloads/SAI/inc/saiversion.h: 32
try:
    SAI_REVISION = 0
except:
    pass

# /home/bluecmd/Downloads/SAI/inc/saiversion.h: 34
def SAI_VERSION(major, minor, revision):
    return (((10000 * major) + (100 * minor)) + revision)

# /home/bluecmd/Downloads/SAI/inc/saiversion.h: 36
try:
    SAI_API_VERSION = (SAI_VERSION (SAI_MAJOR, SAI_MINOR, SAI_REVISION))
except:
    pass

_sai_timespec_t = struct__sai_timespec_t# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 139

_sai_object_list_t = struct__sai_object_list_t# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 167

_sai_u8_list_t = struct__sai_u8_list_t# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 313

_sai_s8_list_t = struct__sai_s8_list_t# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 324

_sai_u16_list_t = struct__sai_u16_list_t# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 330

_sai_s16_list_t = struct__sai_s16_list_t# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 336

_sai_u32_list_t = struct__sai_u32_list_t# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 342

_sai_s32_list_t = struct__sai_s32_list_t# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 348

_sai_u32_range_t = struct__sai_u32_range_t# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 354

_sai_s32_range_t = struct__sai_s32_range_t# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 360

_sai_u16_range_t = struct__sai_u16_range_t# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 366

_sai_u16_range_list_t = struct__sai_u16_range_list_t# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 372

_sai_vlan_list_t = struct__sai_vlan_list_t# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 385

_sai_ip_addr_t = union__sai_ip_addr_t# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 405

_sai_ip_address_t = struct__sai_ip_address_t# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 413

_sai_ip_address_list_t = struct__sai_ip_address_list_t# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 419

_sai_ip_prefix_t = struct__sai_ip_prefix_t# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 430

_sai_ip_prefix_list_t = struct__sai_ip_prefix_list_t# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 436

_sai_prbs_rx_state_t = struct__sai_prbs_rx_state_t# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 462

_sai_latch_status_t = struct__sai_latch_status_t# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 471

_sai_port_lane_latch_status_t = struct__sai_port_lane_latch_status_t# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 477

_sai_port_lane_latch_status_list_t = struct__sai_port_lane_latch_status_list_t# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 483

_sai_acl_field_data_mask_t = union__sai_acl_field_data_mask_t# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 524

_sai_acl_field_data_data_t = union__sai_acl_field_data_data_t# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 578

_sai_acl_field_data_t = struct__sai_acl_field_data_t# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 613

_sai_acl_action_parameter_t = union__sai_acl_action_parameter_t# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 662

_sai_acl_action_data_t = struct__sai_acl_action_data_t# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 686

_sai_qos_map_params_t = struct__sai_qos_map_params_t# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 755

_sai_qos_map_t = struct__sai_qos_map_t# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 765

_sai_qos_map_list_t = struct__sai_qos_map_list_t# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 775

_sai_map_t = struct__sai_map_t# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 785

_sai_map_list_t = struct__sai_map_list_t# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 795

_sai_acl_chain_t = struct__sai_acl_chain_t# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 839

_sai_acl_chain_list_t = struct__sai_acl_chain_list_t# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 849

_sai_acl_capability_t = struct__sai_acl_capability_t# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 890

_sai_acl_resource_t = struct__sai_acl_resource_t# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 997

_sai_acl_resource_list_t = struct__sai_acl_resource_list_t# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 1013

_sai_hmac_t = struct__sai_hmac_t# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 1041

_sai_tlv_entry_t = union__sai_tlv_entry_t# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 1059

_sai_tlv_t = struct__sai_tlv_t# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 1070

_sai_tlv_list_t = struct__sai_tlv_list_t# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 1082

_sai_segment_list_t = struct__sai_segment_list_t# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 1094

_sai_json_t = struct__sai_json_t# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 1123

_sai_port_lane_eye_values_t = struct__sai_port_lane_eye_values_t# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 1136

_sai_port_eye_values_list_t = struct__sai_port_eye_values_list_t# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 1158

_sai_port_frequency_offset_ppm_values_t = struct__sai_port_frequency_offset_ppm_values_t# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 1167

_sai_port_frequency_offset_ppm_list_t = struct__sai_port_frequency_offset_ppm_list_t# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 1176

_sai_port_snr_values_t = struct__sai_port_snr_values_t# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 1188

_sai_port_snr_list_t = struct__sai_port_snr_list_t# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 1197

_sai_system_port_config_t = struct__sai_system_port_config_t# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 1262

_sai_system_port_config_list_t = struct__sai_system_port_config_list_t# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 1274

_sai_fabric_port_reachability_t = struct__sai_fabric_port_reachability_t# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 1286

_sai_port_err_status_list_t = struct__sai_port_err_status_list_t# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 1331

_sai_attribute_value_t = union__sai_attribute_value_t# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 1531

_sai_attribute_t = struct__sai_attribute_t# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 1543

_sai_stat_capability_t = struct__sai_stat_capability_t# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 1700

_sai_stat_capability_list_t = struct__sai_stat_capability_list_t# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 1707

_sai_switch_health_data_t = struct__sai_switch_health_data_t# /home/bluecmd/Downloads/SAI/inc/saitypes.h: 1733

_sai_acl_api_t = struct__sai_acl_api_t# /home/bluecmd/Downloads/SAI/inc/saiacl.h: 3738

_sai_ars_api_t = struct__sai_ars_api_t# /home/bluecmd/Downloads/SAI/inc/saiars.h: 237

_sai_ars_profile_api_t = struct__sai_ars_profile_api_t# /home/bluecmd/Downloads/SAI/inc/saiarsprofile.h: 404

_sai_bfd_session_state_notification_t = struct__sai_bfd_session_state_notification_t# /home/bluecmd/Downloads/SAI/inc/saibfd.h: 132

_sai_bfd_api_t = struct__sai_bfd_api_t# /home/bluecmd/Downloads/SAI/inc/saibfd.h: 664

_sai_bridge_api_t = struct__sai_bridge_api_t# /home/bluecmd/Downloads/SAI/inc/saibridge.h: 717

_sai_buffer_api_t = struct__sai_buffer_api_t# /home/bluecmd/Downloads/SAI/inc/saibuffer.h: 758

_sai_counter_api_t = struct__sai_counter_api_t# /home/bluecmd/Downloads/SAI/inc/saicounter.h: 223

_sai_debug_counter_api_t = struct__sai_debug_counter_api_t# /home/bluecmd/Downloads/SAI/inc/saidebugcounter.h: 519

_sai_dtel_api_t = struct__sai_dtel_api_t# /home/bluecmd/Downloads/SAI/inc/saidtel.h: 870

_sai_fdb_entry_t = struct__sai_fdb_entry_t# /home/bluecmd/Downloads/SAI/inc/saifdb.h: 71

_sai_fdb_event_notification_data_t = struct__sai_fdb_event_notification_data_t# /home/bluecmd/Downloads/SAI/inc/saifdb.h: 346

_sai_fdb_api_t = struct__sai_fdb_api_t# /home/bluecmd/Downloads/SAI/inc/saifdb.h: 531

_sai_generic_programmable_api_t = struct__sai_generic_programmable_api_t# /home/bluecmd/Downloads/SAI/inc/saigenericprogrammable.h: 150

_sai_hash_api_t = struct__sai_hash_api_t# /home/bluecmd/Downloads/SAI/inc/saihash.h: 410

_sai_hostif_api_t = struct__sai_hostif_api_t# /home/bluecmd/Downloads/SAI/inc/saihostif.h: 1453

_sai_ipmc_group_api_t = struct__sai_ipmc_group_api_t# /home/bluecmd/Downloads/SAI/inc/saiipmcgroup.h: 232

_sai_ipmc_entry_t = struct__sai_ipmc_entry_t# /home/bluecmd/Downloads/SAI/inc/saiipmc.h: 76

_sai_ipmc_api_t = struct__sai_ipmc_api_t# /home/bluecmd/Downloads/SAI/inc/saiipmc.h: 208

_sai_ipsec_sa_status_notification_t = struct__sai_ipsec_sa_status_notification_t# /home/bluecmd/Downloads/SAI/inc/saiipsec.h: 95

_sai_ipsec_api_t = struct__sai_ipsec_api_t# /home/bluecmd/Downloads/SAI/inc/saiipsec.h: 1015

_sai_l2mc_group_api_t = struct__sai_l2mc_group_api_t# /home/bluecmd/Downloads/SAI/inc/sail2mcgroup.h: 242

_sai_l2mc_entry_t = struct__sai_l2mc_entry_t# /home/bluecmd/Downloads/SAI/inc/sail2mc.h: 76

_sai_l2mc_api_t = struct__sai_l2mc_api_t# /home/bluecmd/Downloads/SAI/inc/sail2mc.h: 184

_sai_lag_api_t = struct__sai_lag_api_t# /home/bluecmd/Downloads/SAI/inc/sailag.h: 397

_sai_macsec_api_t = struct__sai_macsec_api_t# /home/bluecmd/Downloads/SAI/inc/saimacsec.h: 1431

_sai_mcast_fdb_entry_t = struct__sai_mcast_fdb_entry_t# /home/bluecmd/Downloads/SAI/inc/saimcastfdb.h: 58

_sai_mcast_fdb_api_t = struct__sai_mcast_fdb_api_t# /home/bluecmd/Downloads/SAI/inc/saimcastfdb.h: 174

_sai_mirror_api_t = struct__sai_mirror_api_t# /home/bluecmd/Downloads/SAI/inc/saimirror.h: 444

_sai_inseg_entry_t = struct__sai_inseg_entry_t# /home/bluecmd/Downloads/SAI/inc/saimpls.h: 245

_sai_mpls_api_t = struct__sai_mpls_api_t# /home/bluecmd/Downloads/SAI/inc/saimpls.h: 404

_sai_neighbor_entry_t = struct__sai_neighbor_entry_t# /home/bluecmd/Downloads/SAI/inc/saineighbor.h: 206

_sai_neighbor_api_t = struct__sai_neighbor_api_t# /home/bluecmd/Downloads/SAI/inc/saineighbor.h: 380

_sai_next_hop_group_api_t = struct__sai_next_hop_group_api_t# /home/bluecmd/Downloads/SAI/inc/sainexthopgroup.h: 610

_sai_next_hop_api_t = struct__sai_next_hop_api_t# /home/bluecmd/Downloads/SAI/inc/sainexthop.h: 337

_sai_route_entry_t = struct__sai_route_entry_t# /home/bluecmd/Downloads/SAI/inc/sairoute.h: 182

_sai_route_api_t = struct__sai_route_api_t# /home/bluecmd/Downloads/SAI/inc/sairoute.h: 345

_sai_nat_entry_key_t = struct__sai_nat_entry_key_t# /home/bluecmd/Downloads/SAI/inc/sainat.h: 269

_sai_nat_entry_mask_t = struct__sai_nat_entry_mask_t# /home/bluecmd/Downloads/SAI/inc/sainat.h: 301

_sai_nat_entry_data_t = struct__sai_nat_entry_data_t# /home/bluecmd/Downloads/SAI/inc/sainat.h: 315

_sai_nat_entry_t = struct__sai_nat_entry_t# /home/bluecmd/Downloads/SAI/inc/sainat.h: 346

_sai_nat_event_notification_data_t = struct__sai_nat_event_notification_data_t# /home/bluecmd/Downloads/SAI/inc/sainat.h: 374

_sai_nat_api_t = struct__sai_nat_api_t# /home/bluecmd/Downloads/SAI/inc/sainat.h: 701

_sai_my_sid_entry_t = struct__sai_my_sid_entry_t# /home/bluecmd/Downloads/SAI/inc/saisrv6.h: 467

_sai_srv6_api_t = struct__sai_srv6_api_t# /home/bluecmd/Downloads/SAI/inc/saisrv6.h: 637

_sai_object_key_entry_t = union__sai_object_key_entry_t# /home/bluecmd/Downloads/SAI/inc/saiobject.h: 119

_sai_object_key_t = struct__sai_object_key_t# /home/bluecmd/Downloads/SAI/inc/saiobject.h: 133

_sai_attr_capability_t = struct__sai_attr_capability_t# /home/bluecmd/Downloads/SAI/inc/saiobject.h: 155

_sai_policer_api_t = struct__sai_policer_api_t# /home/bluecmd/Downloads/SAI/inc/saipolicer.h: 372

_sai_port_oper_status_notification_t = struct__sai_port_oper_status_notification_t# /home/bluecmd/Downloads/SAI/inc/saiport.h: 92

_sai_port_api_t = struct__sai_port_api_t# /home/bluecmd/Downloads/SAI/inc/saiport.h: 4093

_sai_qos_map_api_t = struct__sai_qos_map_api_t# /home/bluecmd/Downloads/SAI/inc/saiqosmap.h: 197

_sai_queue_deadlock_notification_data_t = struct__sai_queue_deadlock_notification_data_t# /home/bluecmd/Downloads/SAI/inc/saiqueue.h: 440

_sai_queue_api_t = struct__sai_queue_api_t# /home/bluecmd/Downloads/SAI/inc/saiqueue.h: 569

_sai_router_interface_api_t = struct__sai_router_interface_api_t# /home/bluecmd/Downloads/SAI/inc/sairouterinterface.h: 459

_sai_rpf_group_api_t = struct__sai_rpf_group_api_t# /home/bluecmd/Downloads/SAI/inc/sairpfgroup.h: 232

_sai_samplepacket_api_t = struct__sai_samplepacket_api_t# /home/bluecmd/Downloads/SAI/inc/saisamplepacket.h: 196

_sai_scheduler_group_api_t = struct__sai_scheduler_group_api_t# /home/bluecmd/Downloads/SAI/inc/saischedulergroup.h: 185

_sai_scheduler_api_t = struct__sai_scheduler_api_t# /home/bluecmd/Downloads/SAI/inc/saischeduler.h: 207

_sai_stp_api_t = struct__sai_stp_api_t# /home/bluecmd/Downloads/SAI/inc/saistp.h: 279

_sai_switch_api_t = struct__sai_switch_api_t# /home/bluecmd/Downloads/SAI/inc/saiswitch.h: 3614

_sai_system_port_api_t = struct__sai_system_port_api_t# /home/bluecmd/Downloads/SAI/inc/saisystemport.h: 206

_sai_tam_api_t = struct__sai_tam_api_t# /home/bluecmd/Downloads/SAI/inc/saitam.h: 2349

_sai_tunnel_api_t = struct__sai_tunnel_api_t# /home/bluecmd/Downloads/SAI/inc/saitunnel.h: 1195

_sai_udf_api_t = struct__sai_udf_api_t# /home/bluecmd/Downloads/SAI/inc/saiudf.h: 448

_sai_virtual_router_api_t = struct__sai_virtual_router_api_t# /home/bluecmd/Downloads/SAI/inc/saivirtualrouter.h: 195

_sai_vlan_api_t = struct__sai_vlan_api_t# /home/bluecmd/Downloads/SAI/inc/saivlan.h: 661

_sai_wred_api_t = struct__sai_wred_api_t# /home/bluecmd/Downloads/SAI/inc/saiwred.h: 690

_sai_isolation_group_api_t = struct__sai_isolation_group_api_t# /home/bluecmd/Downloads/SAI/inc/saiisolationgroup.h: 250

_sai_my_mac_api_t = struct__sai_my_mac_api_t# /home/bluecmd/Downloads/SAI/inc/saimymac.h: 170

_sai_twamp_session_stats_data_t = struct__sai_twamp_session_stats_data_t# /home/bluecmd/Downloads/SAI/inc/saitwamp.h: 652

_sai_twamp_session_event_notification_data_t = struct__sai_twamp_session_event_notification_data_t# /home/bluecmd/Downloads/SAI/inc/saitwamp.h: 672

_sai_twamp_api_t = struct__sai_twamp_api_t# /home/bluecmd/Downloads/SAI/inc/saitwamp.h: 803

_sai_service_method_table_t = struct__sai_service_method_table_t# /home/bluecmd/Downloads/SAI/inc/sai.h: 211

# No inserted files

# No prefix-stripping

