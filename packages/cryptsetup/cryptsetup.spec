%global debug_package %{nil}

Name: %{_cross_os}cryptsetup
Version: 2.7.5
Release: 1%{?dist}
Summary: Libraries for disk encryption support
License: GPL-2.0-or-later WITH cryptsetup-OpenSSL-exception AND LGPL-2.1-or-later WITH cryptsetup-OpenSSL-exception
URL: https://gitlab.com/cryptsetup/cryptsetup
Source0: https://www.kernel.org/pub/linux/utils/cryptsetup/v2.7/cryptsetup-%{version}.tar.xz

BuildRequires: %{_cross_os}glibc-devel
BuildRequires: %{_cross_os}libdevmapper-devel
BuildRequires: %{_cross_os}libjson-c-devel
BuildRequires: %{_cross_os}libblkid-devel
BuildRequires: %{_cross_os}libuuid-devel
BuildRequires: %{_cross_os}libpopt-devel
BuildRequires: %{_cross_os}kernel-6.1-devel
BuildRequires: %{_cross_os}libblkid-devel
BuildRequires: %{_cross_os}systemd-devel
BuildRequires: %{_cross_os}aws-lc-fips-devel
BuildRequires: %{_cross_os}libargon2-devel

Requires: %{_cross_os}libdevmapper
Requires: %{_cross_os}libjson-c
Requires: %{_cross_os}libblkid
Requires: %{_cross_os}libuuid
Requires: %{_cross_os}libpopt
Requires: %{_cross_os}systemd
Requires: %{_cross_os}aws-lc-fips
Requires: %{_cross_os}libargon2

%description
%{summary}.

%package devel
Summary: Development files for cryptsetup
Requires: %{name}
Requires: %{_cross_os}libargon2-devel

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%autosetup -n cryptsetup-%{version} -p1

%build
%cross_configure \
    --disable-asciidoc \
    --disable-ssh-token \
    --enable-libargon2 \
    --disable-pwquality \
    --disable-static \
    --disable-cryptsetup \
    --disable-veritysetup \
    --disable-integritysetup \
    --disable-nls \
    --with-crypto_backend=openssl \

%force_disable_rpath

%make_build

%install
%make_install

# Remove unwanted files
rm -rf %{buildroot}%{_cross_libdir}/tmpfiles.d/cryptsetup.conf

%files
%license COPYING COPYING.LGPL
%{_cross_libdir}/libcryptsetup.so.*
%{_cross_libdir}/libcryptsetup.so
%{_cross_attribution_file}
%exclude %{_cross_mandir}

%files devel
%{_cross_libdir}/pkgconfig/libcryptsetup.pc
%{_cross_includedir}/libcryptsetup.h

%changelog 
