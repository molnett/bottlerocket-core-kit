Name: %{_cross_os}aws-lc-fips
Version: 3.0.0
Release: 1%{?dist}
Summary: AWS-LC cryptographic library (FIPS)
License: Apache-2.0 OR ISC OR BSD-3-Clause OR MIT OR CC0-1.0 OR OpenSSL OR SSLeay-standalone
URL: https://github.com/aws/aws-lc

Source0: https://github.com/aws/aws-lc/archive/AWS-LC-FIPS-%{version}/aws-lc-AWS-LC-FIPS-%{version}.tar.gz

BuildRequires: %{_cross_os}glibc-devel

Requires: %{_cross_os}glibc

%description
AWS-LC is a general-purpose cryptographic library maintained by the
AWS Cryptography team for AWS and their customers. It іs based on code
from the Google BoringSSL project and the OpenSSL project. This version
includes FIPS support.

%package devel
Summary: Development files for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
AWS-LC development files from package %{name}.

%prep
%setup -n aws-lc-AWS-LC-FIPS-%{version}

%build
%set_cross_build_flags

mkdir -p aws-lc-build
cd aws-lc-build

%cross_cmake ../ \
    -GNinja \
    -DCMAKE_BUILD_TYPE=RelWithDebInfo \
    -DBUILD_SHARED_LIBS=ON \
    -DBUILD_TESTING=OFF \
    -DCMAKE_INSTALL_PREFIX=%{_cross_prefix} \
    -DCMAKE_INSTALL_LIBDIR=%{_cross_libdir} \
    -DCMAKE_SKIP_INSTALL_RPATH=ON

cmake --build .

%install
cd aws-lc-build
DESTDIR="%{buildroot}" cmake --install .

# Create versioned shared library symlinks
ln -s libcrypto.so %{buildroot}%{_cross_libdir}/libcrypto.so.1.1
ln -s libcrypto.so.1.1 %{buildroot}%{_cross_libdir}/libcrypto.so.1
ln -s libssl.so %{buildroot}%{_cross_libdir}/libssl.so.1.1
ln -s libssl.so.1.1 %{buildroot}%{_cross_libdir}/libssl.so.1

# Set proper permissions for libraries
chmod 755 %{buildroot}%{_cross_libdir}/*.so*

# Remove CMake files as they're not needed in the target system
rm -rf %{buildroot}%{_cross_libdir}/crypto/cmake
rm -rf %{buildroot}%{_cross_libdir}/ssl/cmake

%files
%{_cross_attribution_file}
%{_cross_libdir}/libcrypto.so.*
%{_cross_libdir}/libssl.so.*
%{_cross_bindir}/bssl
%{_cross_bindir}/openssl

%files devel
%{_cross_includedir}/openssl
%{_cross_libdir}/pkgconfig/*.pc
%{_cross_libdir}/libcrypto.so
%{_cross_libdir}/libssl.so

%changelog
