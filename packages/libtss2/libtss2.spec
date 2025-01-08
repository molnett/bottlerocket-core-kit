Name: %{_cross_os}libtss2
Version: 4.1.3
Release: 1%{?dist}
Summary: TPM2.0 Software Stack core libraries
License: BSD-2-Clause
URL: https://github.com/tpm2-software/tpm2-tss
Source0: %{url}/releases/download/%{version}/tpm2-tss-%{version}.tar.gz

BuildRequires: %{_cross_os}glibc-devel
BuildRequires: %{_cross_os}aws-lc-fips-devel

Requires: %{_cross_os}glibc
Requires: %{_cross_os}aws-lc-fips

%description
Core libraries from the TPM2.0 Software Stack, specifically tss2-esys,
tss2-rc, and tss2-mu which are needed for TPM2 support in systemd.

%package devel
Summary: Development files for TPM2.0 Software Stack core libraries
Requires: %{name}
Requires: %{_cross_os}aws-lc-fips-devel

%description devel
Development files for the core TPM2.0 Software Stack libraries.

%prep
%autosetup -n tpm2-tss-%{version}

%build
CONFIGURE_OPTS=(
 --enable-esys
 --enable-tcti-device
 --disable-nodl
 --with-crypto=ossl
 --disable-static
 --disable-silent-rules
 --disable-doxygen-doc
 --disable-fapi
 --disable-policy
 --disable-tcti-mssim
 --disable-tcti-swtpm
 --disable-tcti-cmd
 --disable-tcti-spi-ltt2go
 --disable-tcti-spi-ftdi
 --disable-defaultflags
 --disable-weakcrypto
 --disable-log-file
 --disable-integration
 --disable-unit
 --disable-tcti-pcap
 --disable-tcti-spidev
 --disable-man-pages
 --with-maxloglevel=error
 --with-sysusersdir=%{_cross_sysusersdir}
 --with-tmpfilesdir=%{_cross_tmpfilesdir}
 --with-udevrulesdir=%{_cross_udevrulesdir}
 --with-runstatedir=%{_rundir}
)

%set_cross_build_flags

%cross_configure "${CONFIGURE_OPTS[@]}"

# Fix Rpath issues
#sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
#sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

%make_build

%install
%make_install


%files
%license LICENSE
%{_cross_attribution_file}
%{_cross_libdir}/libtss2-esys.so.*
%{_cross_libdir}/libtss2-rc.so.*
%{_cross_libdir}/libtss2-mu.so.*
%{_cross_libdir}/libtss2-sys.so.*
%{_cross_libdir}/libtss2-tctildr.so.*
%{_cross_libdir}/libtss2-tcti-device.so.*
%{_cross_libdir}/libtss2-tcti-i2c-helper.so.*
%{_cross_libdir}/libtss2-tcti-spi-helper.so.*
%{_cross_udevrulesdir}/tpm-udev.rules
%exclude %{_cross_mandir}

%files devel
%{_cross_libdir}/libtss2-esys.so
%{_cross_libdir}/libtss2-rc.so
%{_cross_libdir}/libtss2-mu.so
%{_cross_libdir}/libtss2-sys.so
%{_cross_libdir}/libtss2-tctildr.so
%{_cross_libdir}/libtss2-tcti-device.so
%{_cross_libdir}/libtss2-tcti-i2c-helper.so
%{_cross_libdir}/libtss2-tcti-spi-helper.so
%{_cross_includedir}/tss2
%{_cross_pkgconfigdir}/tss2-esys.pc
%{_cross_pkgconfigdir}/tss2-rc.pc
%{_cross_pkgconfigdir}/tss2-mu.pc
%{_cross_pkgconfigdir}/tss2-sys.pc
%{_cross_pkgconfigdir}/tss2-tctildr.pc
%{_cross_pkgconfigdir}/tss2-tcti-device.pc
%{_cross_pkgconfigdir}/tss2-tcti-i2c-helper.pc
%{_cross_pkgconfigdir}/tss2-tcti-spi-helper.pc

%changelog 
