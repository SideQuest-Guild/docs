# Run it locally

## Prerequisites

You need [Rust](https://www.rust-lang.org/), installed with `rustup`, plus what GPUI (the UI
toolkit) needs to build on your system:

::::{tab-set}
:sync-group: os

:::{tab-item} {iconify}`mdi:microsoft-windows` Windows
:sync: windows

Nothing beyond what `rustup` asks for: the Visual Studio C++ build tools that Rust's MSVC
toolchain uses. CI builds on a stock `windows-latest` runner with no extra steps.
:::

:::{tab-item} {iconify}`mdi:apple` macOS
:sync: macos

The full Xcode app, not just the Command Line Tools: GPUI compiles Metal shaders (graphics code
that runs on the GPU) at build time. If Xcode is installed but not selected, run
`sudo xcode-select -s /Applications/Xcode.app`.
:::

:::{tab-item} {iconify}`mdi:linux` Linux
:sync: linux

A few system libraries. The `Install Linux build dependencies` step in
`.github/workflows/ci.yml` has the exact package list for Ubuntu.
:::
::::

## Steps

```sh
make install   # rustup components (rustfmt, clippy) + cargo-deny
make run       # run the companion against your real WoW install
```

## Run it without a real WoW install

```sh
make demo
```

This runs the companion against fixture data, with no real WoW install, sync token, or network
needed. Use it to work on the UI without a game install or guild credentials.

## Try a macOS bundle locally

```sh
make bundle-macos
```

Builds a release binary and assembles a local, ad-hoc-signed `SideQuest Companion.app`, using the
same script the release workflow uses (`packaging/macos/bundle.sh`), so you can test the real
bundle without waiting on CI.
