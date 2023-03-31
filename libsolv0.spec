%define major 0
%define libname %mklibname solv %{major}
%define extlibname %mklibname solvext %{major}
%define devname %mklibname solv -d

Summary:	Old version of the libsolv dependency resolution library
Name:		libsolv0
Version:	0.6.39
Release:	2
License:	MIT
Group:		System/Libraries
# See also: https://github.com/openSUSE/libsolv
URL:		http://en.opensuse.org/openSUSE:Libzypp_satsolver
Source0:	https://github.com/openSUSE/libsolv/archive/refs/tags/%{version}.tar.gz

# OpenMandriva patch for transitioning from RPM5
Patch1001:	1001-ext-Ignore-DistEpoch-entirely.patch
# ARMv8 support https://github.com/openSUSE/libsolv/pull/260
Patch1002:	https://github.com/openSUSE/libsolv/pull/260/commits/3c2b27fbf1c2e7b2d91c2b43a54dbcdf1771dcb0.patch
# znver1 support
Patch1003:	libsolv-0.6.34-znver1.patch

BuildRequires:	cmake
BuildRequires:	ninja
BuildRequires:	pkgconfig(icu-i18n)
BuildRequires:	pkgconfig(rpm)
BuildRequires:	pkgconfig(zlib)
BuildRequires:	pkgconfig(bzip2)
BuildRequires:	pkgconfig(liblzma)
BuildRequires:	pkgconfig(libzstd)
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	pkgconfig(zck)
BuildConflicts:	pkgconfig(rpm) >= 5
Requires:	gzip
Requires:	bzip2
Requires:	xz
Requires:	coreutils
Requires:	findutils

%description
Solving dependencies is the core functionality for any software management
application on Linux.

Dependencies are used to divide and share functionalities across multiple
software elements.

Linux (and Unix) follows two basic concepts to implement Divide & Conquer -
breaking a large problem into smaller, more manageable ones.

* Make each program do one thing well. See Basics of the Unix Philosophy
  for details.
* Use shared libraries to share implementations and save disk and memory
  space 

Every software package expresses the functionalities it provides to others
and those it requires from others through dependencies.

The task of the dependency resolver is to check and fulfill all these
relations when managing software.

Basic laws of resolving

The dependency solver tries to solve dependencies without user intervention
based on two basic rules

* Fulfill the install/remove requests given at start
* Keep the (dependencies of the) installed system consistent 

Since the solver treats every package alike, these rules have some major and
sometimes unexpected implications. A broken dependency might result in
removal of lots of packages - the resulting system is still consistent
but highly unusable. 

%if "%{libname}" != "%{name}"
%package -n %{libname}
Summary:	Package dependency solver and repository storage system
Group:		System/Libraries
Requires:	libsolv >= %{EVRD}

%description -n %{libname}
Package dependency solver and repository storage system.
%endif

%package -n %{extlibname}
Summary:	Package dependency solver and repository storage system
Group:		System/Libraries
Requires:	%{libname} = %{EVRD}

%description -n %{extlibname}
Package dependency solver and repository storage system.

%prep
%autosetup -p1 -n libsolv-%{version}

# The parameters below are intended to ensure
# that the DNF stack works correctly on OpenMandriva
# The FEDORA switch sets some definitions up that aren't
# otherwise available.
%cmake -GNinja \
	-DFEDORA=1 \
	-DWITH_LIBXML2:BOOL=ON \
	-DENABLE_COMPLEX_DEPS:BOOL=ON \
	-DENABLE_RPMDB_BYRPMHEADER:BOOL=ON \
	-DENABLE_RPMDB_LIBRPM:BOOL=ON \
	-DENABLE_RPMPKG_LIBRPM:BOOL=ON \
	-DENABLE_LZMA_COMPRESSION:BOOL=ON \
	-DENABLE_ZSTD_COMPRESSION:BOOL=ON \
	-DENABLE_ZCHUNK_COMPRESSION:BOOL=ON \
	-DENABLE_BZIP2_COMPRESSION:BOOL=ON \
	-DENABLE_COMPS:BOOL=ON \
	-DENABLE_APPDATA:BOOL=ON \
	-DENABLE_HELIXREPO:BOOL=ON \
	-DENABLE_RPMDB:BOOL=ON \
	-DENABLE_COMPLEX_DEPS:BOOL=ON \
	-DENABLE_SUSEREPO:BOOL=ON

%build
%ninja_build -C build

%install
%ninja_install -C build

# Not for compat packages...
rm -rf %{buildroot}%{_bindir} \
	%{buildroot}%{_mandir} \
	%{buildroot}%{_includedir} \
	%{buildroot}%{_libdir}/pkgconfig \
	%{buildroot}%{_libdir}/*.so \
	%{buildroot}%{_datadir}/cmake

%if "%{libname}" != "%{name}"
%files -n %{libname}
%else
%files
%endif
%{_libdir}/libsolv.so.%{major}

%files -n %{extlibname}
%{_libdir}/libsolvext.so.%{major}
