%global _cross_first_party 1
%undefine _auto_set_build_flags

Name: %{_cross_os}libaio
Version: 0.3.111
Release: 1%{?dist}
Summary: Linux-native asynchronous I/O access library
License: LGPL-2.0-or-later
URL: http://releases.pagure.org/libaio
Source0: %{url}/libaio-%{version}.tar.gz

Patch1: libaio-install-to-destdir-slash-usr.patch
Patch2: libaio-remove-nostartfiles-nostdlib-from-build-flags.patch

BuildRequires: %{_cross_os}glibc-devel

%description
The Linux-native asynchronous I/O facility ("async I/O", or "aio") has a
richer API and capability set than the simple POSIX async I/O facility.
This library, libaio, provides the Linux-native API for async I/O.
The POSIX async I/O facility requires this library in order to provide
kernel-accelerated async I/O capabilities, as do applications which
require the Linux-native async I/O API.

%package devel
Summary: Development files for Linux-native asynchronous I/O access
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
This package provides header files to include and libraries to link with
for the Linux-native asynchronous I/O facility ("async I/O", or "aio").

%prep
%autosetup -n libaio-%{version} -p1

%build
%set_cross_build_flags

# This package uses ASMs to implement symbol versioning and is thus
# incompatible with LTO
%define _lto_cflags %{nil}

make %{?_smp_mflags}

%install
cd src
install -D -m 0644 libaio.h %{buildroot}%{_cross_includedir}/libaio.h
install -D -m 0755 libaio.so.1.0.1 %{buildroot}%{_cross_libdir}/libaio.so.1.0.1
ln -s libaio.so.1.0.1 %{buildroot}%{_cross_libdir}/libaio.so.1
ln -s libaio.so.1 %{buildroot}%{_cross_libdir}/libaio.so

%files
%license COPYING
%{_cross_libdir}/libaio.so.*

%files devel
%{_cross_includedir}/*
%{_cross_libdir}/libaio.so

%changelog
