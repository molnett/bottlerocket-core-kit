# device-mapper

This package provides the device-mapper userspace utility `dmsetup` and related libraries from the LVM2 project.

`Cargo.toml` contains metadata for Bottlerocket's build tool, including the source URL and checksum for the LVM2 source code.

`device-mapper.spec` is the spec for the package build. It builds only the basic device-mapper components needed for dmsetup functionality.

The package includes:
Main package:
- dmsetup binary
- dmeventd daemon
- libdevmapper shared library
- libdevmapper-event shared library
- udev rules for device-mapper

Development package (-devel):
- Development headers for device-mapper
- Development headers for device-mapper-event
- Development symlinks for libraries