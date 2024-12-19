%global _cross_first_party 1
%undefine _auto_set_build_flags

Name: %{_cross_os}libpopt
Version: 1.19
Release: 1%{?dist}
Summary: C library for parsing command line parameters
License: MIT AND LicenseRef-Fedora-Public-Domain
URL: https://github.com/rpm-software-management/popt
Source0: http://ftp.rpm.org/popt/releases/popt-1.x/popt-%{version}.tar.gz

BuildRequires: %{_cross_os}glibc-devel

%description
%{summary}.

%package devel
Summary: Development files for %{name}
Requires: %{name}

%description devel
This package provides header files and libraries necessary for developing
programs which use the popt C library.

%prep
%autosetup -n popt-%{version} -p1

%build
%set_cross_build_flags

%cross_configure \
    --disable-static \
    --disable-nls \
    --disable-rpath

%make_build

%install
%make_install


%files
%license COPYING
%{_cross_libdir}/libpopt.so.*
%exclude %{_cross_mandir}
%exclude %{_cross_datadir}/locale

%files devel
%{_cross_includedir}/popt.h
%{_cross_libdir}/libpopt.so
%{_cross_libdir}/pkgconfig/popt.pc

%changelog
