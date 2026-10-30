# Test and check

```sh
make ci
```

| Check | Command | What it covers |
|---|---|---|
| Formatting | `make fmt-check` | `cargo fmt --all --check` |
| Lint | `make lint` | `cargo clippy --all-targets -- -D warnings`: clippy, Rust's linter, with warnings treated as failures |
| Tests | `make test` | `cargo test` |
| Dependencies | `make deny` | `cargo-deny`: checks licenses, security advisories, and where dependencies come from. Unmaintained-package advisories warn instead of failing. |

`make fmt` applies the formatting fixes for you.
