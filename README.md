# scons-novice

Adapted from
[https://swcarpentry.github.io/make-novice/](https://swcarpentry.github.io/make-novice/) source
repository at commit [ba7c2dd](https://github.com/swcarpentry/make-novice)

The following instructions are adopted from https://carpentries.github.io/workbench/

## Environment

Install Conda and create an environment from the conda-forge channel. You may need to re-direct
``TMPDIR`` if ``/tmp`` is mounted without execute permissions.

```
$ conda create --channel conda-forge --name workbench 'git>=2.28' 'r-base>=3.6' 'pandoc>=2.11' pkg-config libxslt r-httr2 r-pkgdown r-httpuv r-servr
$ TMPDIR=/scratch/$USER/workbench R -e 'install.packages(c("sandpaper", "varnish", "pegboard", "tinkr"), repos = list(carpentries="https://carpentries.r-universe.dev/", CRAN="https://cloud.r-project.org"))'
```

## Build

Interactive build-while-editing. Note that your terminal will not return, so you need to edit from
a separate terminal/window: [serve](https://carpentries.github.io/sandpaper/reference/serve.html)

```
$ R -e 'sandpaper::serve(quiet = FALSE, port = "3435")'
```

Build once without interactive, locally web-hosted URL: [build lesson](https://carpentries.github.io/sandpaper/reference/build_lesson.html)

```
$ R -e 'sandpaper::build_lesson(preview = FALSE)'
```

-----

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.3265286.svg)](https://doi.org/10.5281/zenodo.3265286)
[![Create a Slack Account with us](https://img.shields.io/badge/Create_Slack_Account-The_Carpentries-071159.svg)](https://slack-invite.carpentries.org/)
[![Slack Status](https://img.shields.io/badge/Slack_Channel-swc--make-E01563.svg)](https://carpentries.slack.com/messages/C9X2YCPT5)

# make-novice

An introduction to Make using reproducible papers as a motivating example.
Please see [https://swcarpentry.github.io/make-novice/](https://swcarpentry.github.io/make-novice/) for a rendered version
of this material, [the lesson template documentation][lesson-example]
for instructions on formatting, building, and submitting material,
or run `make` in this directory for a list of helpful commands.

Maintainer(s):

- [Gerard Capes][capes-gerard]

[lesson-example]: https://swcarpentry.github.com/lesson-example/
[capes-gerard]: https://carpentries.org/instructors/#gcapes
