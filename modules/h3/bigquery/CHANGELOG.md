# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.4] - 2021-09-22

### Changed
- Review HEXRING, KRING functions.
- Change KRING_INDEXED to KRING_DISTANCES.

## [1.0.3] - 2021-08-24

### Fixed
- Support GEOMETRYCOLLECTION from ST_ASH3_POLYFILL.

## [1.0.2] - 2021-08-04

### Added
- Add KRING_INDEXED function.

## [1.0.1] - 2021-04-09

### Changed
- Use hexadecimal as default type instead of int for h3 indexes.

### Fixed
- Fix ST_BOUNDARY generating error when not able to parse geometry.

## [1.0.0] - 2021-03-31

### Added
- Create h3 module.
- Add ST_ASH3 function.
- Add LONGLAT_ASH3 function.
- Add ST_ASH3_POLYFILL function.
- Add ST_BOUNDARY function.
- Add ISVALID function.
- Add COMPACT function.
- Add UNCOMPACT function.
- Add TOPARENT function.
- Add TOCHILDREN function.
- Add ISPENTAGON function.
- Add DISTANCE function.
- Add KRING function.
- Add HEXRING function.
- Add VERSION function.