# Run it locally

## Prerequisites

- [Rust](https://www.rust-lang.org/), installed with `rustup`
- GPUI's build dependencies

On Linux, GPUI needs a few system libraries first; see the `Install Linux build dependencies`
step in `.github/workflows/ci.yml` for the exact package list. On macOS, you need the full Xcode
app installed, not just the Command Line Tools, because GPUI compiles Metal shaders (graphics
code that runs on the GPU) at build time.

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
