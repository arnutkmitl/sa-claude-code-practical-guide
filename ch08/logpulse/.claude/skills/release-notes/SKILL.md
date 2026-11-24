---
name: release-notes
description: Draft a CHANGELOG.md entry for logpulse from the git
  history since the last tag. Use when the user asks for release
  notes, a changelog entry, or what changed since the last release.
argument-hint: "[version]"
allowed-tools: Bash(git describe *) Bash(git log *) Read Edit
---

# Release notes for logpulse

## Current state

- Last release tag: !`git describe --tags --abbrev=0`
- Commits on this branch (newest first):

!`git log --oneline --no-merges -30`

## Task

Write a new entry at the top of `CHANGELOG.md` for version
$ARGUMENTS (use "Unreleased" if no version was given) with today's
date. Include only the commits made after the last release tag.

## Format

Follow the existing entries in `CHANGELOG.md`:

- Group changes under `### Added`, `### Changed`, `### Fixed`.
  Leave out a group that has no changes.
- One line per user-visible change, written for someone who runs
  logpulse, not for its developers. Name options with backticks.
- Leave out changes users can't see: tests, refactors, and project
  files for Claude Code (`CLAUDE.md`, `.claude/`).
- Don't invent changes. If a commit message is unclear, read the
  commit with `git log -1 --stat <hash>` before you describe it.

## When you finish

Show the new entry and list the commits you left out, with a reason
for each. Don't commit.
