%global _cross_first_party 1
%undefine _auto_set_build_flags

Name: %{_cross_os}dmsetup
Version: 2.03.29
Release: 1%{?dist}
Summary: Device mapper utility
License: GPL-2.0-only
URL: https://sourceware.org/lvm2
Source0: https://sourceware.org/pub/lvm2/releases/LVM2.%{version}.tgz

BuildRequires: %{_cross_os}glibc-devel
BuildRequires: %{_cross_os}libselinux-devel
BuildRequires: %{_cross_os}systemd-devel
BuildRequires: %{_cross_os}libaio-devel
Requires: %{_cross_os}libdevmapper = %{version}-%{release}
Requires: %{_cross_os}systemd
Requires: %{_cross_os}libselinux
Requires: %{_cross_os}libaio

%description
This package contains the supporting userspace utility, dmsetup,
for the kernel device-mapper.

%package -n %{_cross_os}libdevmapper
Summary: Device mapper shared library
Requires: %{_cross_os}systemd
Requires: %{_cross_os}libselinux
Requires: %{_cross_os}libaio

%description -n %{_cross_os}libdevmapper
This package contains the device-mapper shared library, libdevmapper.

%prep
%autosetup -n LVM2.%{version} -p1

%build
%global _default_pid_dir /run
%global _default_dm_run_dir /run
%global _default_run_dir /run/lvm
%global _default_locking_dir /run/lock/lvm
%global _udevdir %{_prefix}/lib/udev/rules.d

%cross_configure \
  --with-default-dm-run-dir=%{_default_dm_run_dir} \
  --with-default-run-dir=%{_default_run_dir} \
  --with-default-pid-dir=%{_default_pid_dir} \
  --with-default-locking-dir=%{_default_locking_dir} \
  --with-usrlibdir=%{_cross_libdir} \
  --with-user= \
  --with-group= \
  --with-device-uid=0 \
  --with-device-gid=6 \
  --with-device-mode=0660 \
  --enable-pkgconfig \
  --enable-udev_sync \
  --disable-dmeventd \
  --disable-readline \
  --enable-selinux \
  --disable-cache_check_needs_check \
  --disable-lvmpolld \
  --disable-lvmlockd \
  --disable-dbus-service \
  --disable-notify-dbus \
  --disable-dmfilemapd \
  --disable-blkid_wiping \
  --disable-fsadm \
  --disable-lvmetad \
  --disable-use-lvmetad \
  --disable-lvmpolld \
  --disable-lvmlockd-dlm \
  --disable-lvmlockd-sanlock \
  --disable-thin-provisioning-tools \
  --disable-cache-tools \
  --disable-vdo \
  --disable-writecache \
  --disable-integrity \
  --disable-lvm \
  --disable-lvm1 \
  --disable-lvm2 \
  --disable-lvmconfig \
  --disable-lvmpolld \
  --disable-lvmlockd \
  --disable-lvmnotify \
  --disable-lvmsystemid \
  --disable-lvmimportvdo \
  --disable-lvmcache \
  --disable-lvmraid \
  --disable-lvmreport \
  --disable-lvmthin \
  --disable-lvmvdo \
  --disable-manpages

%make_build device-mapper

%install
make install_device-mapper DESTDIR=%{buildroot} INSTALL="/usr/bin/install -p"

# Remove unpackaged files
rm -f %{buildroot}%{_cross_sbindir}/blkdeactivate
rm -f %{buildroot}%{_cross_sbindir}/dmstats
rm -rf %{buildroot}%{_cross_datadir}/man

# Only install dmsetup related files
install -d %{buildroot}%{_cross_sbindir}
install -p -m 0755 libdm/dm-tools/dmsetup %{buildroot}%{_cross_sbindir}/dmsetup
install -d %{buildroot}%{_cross_libdir}

# Device mapper library
install -p -m 0755 libdm/ioctl/libdevmapper.so.1.02 %{buildroot}%{_cross_libdir}/
ln -s libdevmapper.so.1.02 %{buildroot}%{_cross_libdir}/libdevmapper.so.1
ln -sf libdevmapper.so.1 %{buildroot}%{_cross_libdir}/libdevmapper.so

install -d %{buildroot}%{_cross_includedir}
install -p -m 0644 libdm/libdevmapper.h %{buildroot}%{_cross_includedir}/
install -d %{buildroot}%{_cross_prefix}/lib/udev/rules.d
install -p -m 0644 udev/10-dm.rules %{buildroot}%{_cross_prefix}/lib/udev/rules.d/
install -p -m 0644 udev/13-dm-disk.rules %{buildroot}%{_cross_prefix}/lib/udev/rules.d/
install -p -m 0644 udev/95-dm-notify.rules %{buildroot}%{_cross_prefix}/lib/udev/rules.d/

%files
%license COPYING COPYING.LIB
%{_cross_sbindir}/dmsetup
%{_cross_prefix}/lib/udev/rules.d/10-dm.rules
%{_cross_prefix}/lib/udev/rules.d/13-dm-disk.rules
%{_cross_prefix}/lib/udev/rules.d/95-dm-notify.rules

%files -n %{_cross_os}libdevmapper
%license COPYING COPYING.LIB
%{_cross_libdir}/libdevmapper.so.*

%package -n %{_cross_os}libdevmapper-devel
Summary: Development libraries and headers for device-mapper
Requires: %{_cross_os}libdevmapper = %{version}-%{release}

%description -n %{_cross_os}libdevmapper-devel
This package contains files needed to develop applications that use
the device-mapper libraries.

%files -n %{_cross_os}libdevmapper-devel
%{_cross_libdir}/libdevmapper.so
%{_cross_includedir}/libdevmapper.h
%{_cross_pkgconfigdir}/devmapper.pc


%changelog
