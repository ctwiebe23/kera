# CHANGELOG

## 1.3.0 on 2025-09-08

### Added

- Key fallback when in collection slots; keys from the parent scope will now
  be available in child scopes (but will be overridden by the child when names
  conflict)

## 1.2.1 on 2025-09-08

### Changed

- Annotated all types in function signatures

## 1.2.0 on 2025-09-04

### Changed

- Made the default join string smarter (it now indents each entry to the same
  level automatically)

## 1.1.0 on 2025-08-28

### Added

- Proper command line interface using the argparser library

## 1.0.1 on 2025-08-23

### Fixed

- PyYAML included as a dependency in `./pyproject.toml`

## 1.0.0 on 2025-08-23

### Added

- Initial project release
