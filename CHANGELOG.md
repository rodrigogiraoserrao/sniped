
<a name='changelog-1.1.0'></a>
# 1.1.0 — 2022-03-19

## Added

- Command `config` to manage configurations:
  - option `--show` prints default configuration to stdout;
  - option `--pretty` to determine whether printing to stdout is pretty or plain;
  - option `--write` to write the configuration to a file;

- Dependency on `rich` for pretty output.

## Changed

- Default snappify config now has empty file name.

<a name='changelog-1.0.0'></a>
# 1.0.0 — 2022-03-19

## Removed

- Command `snappify`.
- Command `carbon`.

## Added

- Added the command `create` to create snippets, instead of having one command per service.

- Command `create` to create images out of code snippets.

## Changed

- Pin `scriv` to a more recent revision so that Markdown fragments are handled better.

- Default behaviour is to output to stdout.

# 0.2.1 — 2022-03-19

### Changed

- Unified code that makes API calls.

- Add default values to:
  - OUT argument (saves to `"out.png"` by default);
  - LANGUAGE argument for carbon (is `"auto"` by default);

# 0.2.0 — 2022-03-18

### Added

- Support for the [Snappify](https://snappify.io) API (note that Snappify's API is still under heavy development and might introduce breaking changes; use at your own risk).

# 0.1.0 – 2022-03-18

### Added

- Added initial dependencies:
  - `black` for code formatting;
  - set up `black` as a pre-commit hook;
  - `scriv` for changelogs;

### Added

- Added support for snippets created through [carbon](https://carbon.now.sh);

### Added

- `sniped` can now be installed as a script.

### Added

- Code can be piped from standard input.

### Changed

- Carbon configuration is now read from a Python dictionary.
