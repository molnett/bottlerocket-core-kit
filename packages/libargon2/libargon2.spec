%global debug_package %{nil}

Name: %{_cross_os}libargon2
Version: 20190702
Release: 1%{?dist}
Summary: The password-hashing library
License: CC0-1.0 OR Apache-2.0
URL: https://github.com/P-H-C/phc-winner-argon2
Source0: %{url}/archive/%{version}.tar.gz

BuildRequires: %{_cross_os}glibc-devel
Requires: %{_cross_os}glibc

%global soname 1

%description
Argon2 is a password-hashing function that summarizes the state of the art
in the design of memory-hard functions and can be used to hash passwords
for credential storage, key derivation, or other applications.

It has three variants:
* Argon2d: Faster and uses data-depending memory access
* Argon2i: Uses data-independent memory access
* Argon2id: Hybrid of Argon2i and Argon2d

%package devel
Summary: Development files for Argon2 password hashing library
Requires: %{name}

%description devel
Development files for the Argon2 password hashing library.

%prep
%autosetup -n phc-winner-argon2-%{version}

# Verify soname version
if ! grep -q 'ABI_VERSION = %{soname}' Makefile; then
    echo "Error: soname version mismatch"
    grep ABI_VERSION Makefile
    exit 1
fi

# Fix pkgconfig file
sed -e 's:lib/@HOST_MULTIARCH@:%{_lib}:;s/@UPSTREAM_VER@/%{version}/' -i libargon2.pc.in

%build
%set_cross_build_flags

# Modify Makefile to use proper flags and paths
sed -e '/^CFLAGS/s:^CFLAGS:LDFLAGS=%{_cross_ldflags}\nCFLAGS:' \
    -e 's:-O3 -Wall:%{_cross_cflags}:' \
    -e '/^LIBRARY_REL/s:lib:%{_lib}:' \
    -e 's:-march=\$(OPTTARGET) :${CFLAGS} :' \
    -e 's:CFLAGS += -march=\$(OPTTARGET)::' \
    -i Makefile

make -j1 PREFIX=%{_cross_prefix} \
    CC=%{_cross_target}-gcc \
    OPTTARGET=none \
    LIBRARY_REL=lib

%install
make install DESTDIR=%{buildroot} \
    PREFIX=%{_cross_prefix} \
    LIBRARY_REL=lib

rm %{buildroot}%{_cross_bindir}/argon2
rm %{buildroot}%{_cross_libdir}/libargon2.a
# Fix permissions
chmod -x %{buildroot}%{_cross_includedir}/argon2.h
find %{buildroot}%{_cross_libdir} -name "libargon2.so" -type f -exec chmod +x {} \;

%files
%license LICENSE
%{_cross_attribution_file}
%{_cross_libdir}/libargon2.so
%{_cross_libdir}/libargon2.so.%{soname}

%files devel
%doc README.md CHANGELOG.md
%{_cross_includedir}/argon2.h
%{_cross_pkgconfigdir}/libargon2.pc

%changelog 
