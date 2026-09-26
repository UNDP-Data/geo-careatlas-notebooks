## Care Atlas Notebooks Repository

This repository holds the content of [CareAtlas](https://github.com/UNDP-Data/geo-careatlas):
the apps, their marimo notebooks and who has access to them.

Most changes should go through CareAtlas rather than being pushed here directly.
CareAtlas keeps its own clone of this repository, commits on behalf of the people
using it, and decides what is published based on the files described below.

## Layout

Each top-level folder is an app. The folder name is the app's address in
CareAtlas, so `poverty_map/` is served at `/apps/poverty_map`.

```
poverty_map/
  app.toml          title, description, visibility and members
  main.py           a marimo notebook
  regional.py       another notebook in the same app
_archive/           apps and notebooks that owners have archived
README.md
```

Folder names use lowercase letters, digits, `-` and `_`. Folders starting with
`_` are never shown as apps, and files starting with `_` are never shown as
notebooks, so they can hold helper modules.

## app.toml

```toml
title = "Poverty map"
description = "Poverty headcount ratios at subnational level."
visibility = "restricted"   # or "public"

[members]
owners = ["octocat"]
editors = ["@UNDP-Data/gender-team"]
viewers = []
```

- `visibility`: `public` apps can be viewed by anyone, even without signing in.
  `restricted` apps can only be viewed by their members. If it's missing, the app
  is restricted.
- Members are GitHub usernames or teams written as `@org/team` (`@org` for a whole
  organisation). Names are not case-sensitive. A person gets the highest role they
  match.
- Every app needs at least one owner.

| Role | Can do |
|---|---|
| Viewer | Run the app's notebooks |
| Editor | Edit their own copy of the notebooks, commit, and submit changes for review |
| Owner | Everything editors can, plus publish directly, approve or reject submissions, change settings and members, add or archive notebooks, and archive the app |

Owners normally change `app.toml` through the app's Settings page. Changes made
by editors to `app.toml` are never published.

## Branches

- `main` is the published version. It is what viewers see in CareAtlas.
- `edit/<app>/<user>` is one person's copy of one app. CareAtlas pushes it when
  that person commits. Its contents are not visible in CareAtlas until they are
  published.

When an owner publishes or approves changes, CareAtlas squashes them into a
single commit on `main` with a message the owner confirms. The person who made
the changes is the commit author, and approvals add an `Approved-by:` line. The
intermediate commits on the editor's branch don't appear on `main`, and the
branch is reset once everything on it is published.

CareAtlas itself commits some changes on `main`: creating apps, settings changes,
adding and archiving notebooks, and the archive clean-up described below.

## Notebooks

Notebooks are [marimo](https://marimo.io) notebooks. Jupyter notebooks can be
uploaded in CareAtlas and are converted to marimo on upload.

Notebooks run in CareAtlas's Python environment, so they can only import
packages installed there. At the time of writing that includes marimo, pandas,
numpy, altair, lonboard, shapely and pyarrow. If a notebook needs another
package, it has to be added to CareAtlas's dependencies first.

The first markdown heading in a notebook (for example `mo.md("# Poverty map")`)
is used as its title in CareAtlas, and the module docstring as its description.

Caches that marimo and Python write next to notebooks (`__marimo__/`,
`__pycache__/`) are never committed.

## Archived apps and notebooks

When an owner archives something, it is moved into `_archive/` with the time it
was archived in its name:

| Archived item | Location |
|---|---|
| App | `_archive/<app>-<YYYYMMDD-HHMMSS>/` |
| Notebook | `_archive/<app>/<notebook>-<YYYYMMDD-HHMMSS>.py` |

After 30 days CareAtlas removes archived items from `main` in a single commit.
They remain in the history. To restore something, see "Restoring archived apps
and notebooks" in the
[CareAtlas README](https://github.com/UNDP-Data/geo-careatlas#restoring-archived-apps-and-notebooks).

## Changing things directly

People with write access can push here directly, for example to restore an
archived app or to fix an `app.toml` when nobody can open its Settings page.
CareAtlas picks up changes to `main` within five minutes.

A few things to keep in mind:

- Push to `main` only. Don't push to or delete someone's `edit/...` branch; it
  holds their work in progress.
- Keep every app with at least one owner, and keep `app.toml` valid TOML.
  CareAtlas skips apps whose `app.toml` it can't read.
- Don't rewrite the history of `main`. CareAtlas and everyone's branches are based
  on it.

## What not to commit

This repository is private, but restricted apps are only restricted inside
CareAtlas. Anyone with access to the repository can read every app. Don't commit
personal data, credentials or anything that shouldn't be readable by everyone
with repository access. Keep large data files out as well; load data from
GeoHub or another data source instead.

