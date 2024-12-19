# libaio

Current version: 0.3.111

This package provides the Linux-native asynchronous I/O access library. The Linux-native asynchronous I/O facility ("async I/O", or "aio") has a richer API and capability set than the simple POSIX async I/O facility.

## Updating

To update to a new version:
1. Update the version number in `Cargo.toml` and `libaio.spec`
2. Update the SHA512 hash in `Cargo.toml`
3. Update the changelog in `libaio.spec`

## Building

This package is built with cargo using the standard Bottlerocket build process.

## License

This package is licensed under LGPL-2.0-or-later.
See the [libaio project page](http://releases.pagure.org/libaio) for more details. 