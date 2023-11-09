# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.3.1] - 2023-09-11

### MAJOR RELEASE VERSION

### Added

- !commandMc command to send console commands to the Minecraft server
- !switch <on|off> to start and stop the Minecraft server

### Changed

- Majorly reworked the way some imports interact
- Added some new dependancies
- Updated requirements.txt

## [1.3.0] - 2023-09-11

### Major Update

- !mcswitch command now functions (somewhat, usually).  lots and lots to do now, can't list it all right here! Check [GitHub](https://github.com/notoriouslogank/mcswitch/issues).

## [1.2.1] - 2023-08-11

### Fixed

- Cog loading messages now appear in correct order

### Added

- Missing docstring(s) in !help command

## [1.2.0] - 2023-08-11

### Breaking Changes

- Restructured entire module: created mcswitch/utils/, mcswitch/server.utils, mcswitch/docs folders to contain source code
- Changed most instances of importing helpers.py: imports are much more streamlined

### Added

- !define command to get the Meriam-Webster definition of a word
- !help command description: !define

### Fixed

- Minor formatting errors in CHANGELOG.md
- !changelog command

## [1.1.6] - 2023-08-11

### Changed

-Reformatted the embed created by !help

## [1.1.5] - 2023-08-11

### Fixed

- Formatting errors in README.md
- Removed unused import in help.py

### Added

- Link to GitHub Issue Tracker in !help embed

### Changed

- Rewrote all docstrings for brevity and clarity.
- Removed two (ostensibly) unused imports in helpers.py
- Rewrote all !help command descriptions

### Removed

- Unused mc.sh file

## [1.1.4] - 2023-08-11

### Deprecated

- getLog() helper function; obsoleted by !changelog()

### Added

- on ready messages for each Cog
- embed for !changelog command

### Changed

- !changelog command now sends embed

### Fixed

- !changelog command works properly now
- Minor formatting errors in CHANGELOG.md

## [1.1.3] - 2023-07-11

### Added

- Custom MyHelpCommand to replace defaulHelpCommand
- Custom help message for every user engagable bot command
- Avatar to help message; will be deploying this further in future updates

### Removed

- Default !help function

## [1.1.2] - 2023-07-11

### Changed

- Default !help() command no longer uses automatic arguments and instead defaults to docstring args

### Added

- Descriptions for arguments in !help() function

## [1.1.1] - 2023-07-11

### Changed

- BotStatus cog renamed to Status

### Added

-Docstrings for all commands (cogs/)

### Fixed

- All cogs should work as intended now
- Imports should work correctly throughout
- Reformatted entire codebase (Black formatter)
- Sorted imports correctly (isort)

### Removed

- Unused imports throughout module

## [1.0.3-dev] - 2023-07-11

### Added

- cogs/ directory for transition to cog-based commands
- cogs/moderation.py: moderation commands
- cogs/status.py: bot status and info commands
- cogs/tools.py: useful commands, tools, etc. the bot can access

## [1.0.2] - 2023-07-11

## Removed

- All logging support; will be migrating to proprietary log format because logging sucks in this module

### Changed

- !lmgtfy() now returns a separate message with only the query string
- log file name changed to 'mcswitch.log'

### Fixed

- Minor formatting errors in CHANGELOG.md

## [1.0.1] - 2023-07-11

### Added

- !playing() command to post game information
- sample-env
- lmgtfy() *may* now send the requesting user a DM with their query string

## [0.9.9] - 2023-06-11

### Fixed

- Minor formatting problems with CHANGELOG.md

### Changed

- Certain commands now auto-remove the original command to obfuscate the sender

## [0.9.8] - 2023-06-11

### Fixed

- Minor formatting issues

### Removed

- Unused functions

## [0.9.7] - 2023-06-11

### Changed

- Sorted imports with isort

## [0.9.6] - 2023-06-11

### Fixed

- Clear command now functions as expected

### Changed

- Moved Channel ID to .env as CHANNEL

### Removed

- Unused imports

## [0.9.5] - 2023-06-11

### Added

- Delete command to have the bot silently delete messages.
- onmessage check for 'curse' words

## [0.9.4] - 2023-06-11

### Changed

- Names of several minor functions (helpers.timestamp() is now imported simply as timestamp(), for example.)
- Sequencing of some functions, mostly as a matter of formatting

### Fixed

- Minor formatting errors

### Added

- Docstrings to all bot commands
- helpers.py module to contain non-bot commands and events

### Removed

- Unused imports

## [0.9.1] - 2023-04-11

### Added

- say() command
- getLog()
- console messages about current status

### Fixed

- changelog() *should* work now

### Deprecated

- getChangelog()

## [0.9.0]

### Added

- getChangelog()
- !changelog command

## [0.8.5] - 2023-04-11

### Deprecated

- Command online() replaced with status()

### Changed

- Formatted main.py using Black formatter

### Bugfixes

- Removed all log messages containing variables (may not be callable?)

## [0.8.4] - 2023-04-11

### Changed

- Temporarily disable automatic versioning due to possible bug(s)

### Bugfixes

- Removed most log messages to attempt to alleviate error(s)

## [0.8.3] - 2023-04-11

### Added

- .vscode settings directory to .gitignore

## [0.8.2] - 2023-04-11

### Added

- Logging support for many (all?) commands

## [0.8.1] - 2023-04-11

### Fixed

- Semantic version now increments automatically (from this file)

### Added

- getVer() function to source the semantic version info from CHANGELOG.md

## [0.8.0] - 2023-04-11

### Added

- requirements.txt
- Content to README.md

### Changed

- Edited CHANGELOG.md for formatting

## [0.7.7] - 2023-04-11

### Added

- CHANGELOG.md

### Changed

- Updated .gitignore