# Musical Victoria

## Development

### Dependencies

This project was written with **Python 3.12** using the following dependencies:

- [`python3.12`](https://github.com/python/cpython/tree/3.12)
  - [`fastapi`](https://github.com/fastapi/fastapi)
  - [`pydantic`](https://github.com/pydantic/pydantic)
  - [`sqlalchemy`](https://github.com/sqlalchemy/sqlalchemy)

### Set-Up

> If you use a BSD or Windows system, you can ignore this section. You can
> install the dependencies and set up your environment in whatever way works
> best for you, such as with [`pip`](https://github.com/pypa/pip) or your system
> package manager.

It is recommended that you use [`direnv`][direnv] and [`nix`][nix] for
development ease and consistency if you are using a Linux or MacOS system.

The project has a `devShell` configured with the project dependencies versioned
and pinned.

If you install [`direnv`][direnv] and [`nix`][nix] on your system, all you have
to do is:

1. Ensure that `experimental-features = flakes nix-command` is in your
   `nix.conf` if not already enabled on your system. You can manually add it or,
   if using a Linux system, run [`./enable-flakes`](./enable-flakes) to add this
   automatically after reviewing the script.
2. Clone the repository.
3. `cd` into the directory.
4. After inspecting [`flake.nix`](./flake.nix) and [`.envrc`](./.envrc) to be
   sure that it is safe, run `direnv allow`.

That's it! It's as simple as that.

A project `venv` will be automatically created by [`nix`][nix]. This will
contain both the `python` binary and the dependencies. These are versioned,
matching the lock file, and are isolated from your system installations.

You don't have to do any manual maintenance nor updating. The project Python
version and dependencies will be automatically updated to match the lock file on
their own. This is reproducible development, where all contributors use the same
environment and inputs. No more _"... but it works on my system."_ issues.

The isolated project environment will be _"loaded"_ automatically whenever you
`cd` into the directory. Upon leaving the directory, the environment will be
_"unloaded"_, returning back to your normal system environment.

If you use a graphical editor, open your editor from within this directory to
have it use the environment, or if you prefer, you can manually point it to the
environment `.venv` on your own to have it use the project resources rather than
your system's.

### Resources

#### Direnv

- Home Page 🏠: <https://direnv.net/>
- GitHub Page 🌳: <https://github.com/direnv/direnv/tree/master>
- Installation 💻: <https://direnv.net/docs/installation.html>

#### Nix

- Home Page 🏠: <https://nixos.org/>
- GitHub Page 🌳: <https://github.com/NixOS/nix>
- Installation 💻: <https://nixos.org/download/#download-nix>

<!---->

[direnv]: https://github.com/direnv/direnv/tree/master
[nix]: https://github.com/NixOS/nix
