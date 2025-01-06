[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.3265286.svg)](https://doi.org/10.5281/zenodo.3265286)
[![Create a Slack Account with us](https://img.shields.io/badge/Create_Slack_Account-The_Carpentries-071159.svg)](https://slack-invite.carpentries.org/)
[![Slack Status](https://img.shields.io/badge/Slack_Channel-swc--make-E01563.svg)](https://carpentries.slack.com/messages/C9X2YCPT5)

# scons-novice

Adapted from
[https://github.com/swcarpentry/make-novice](https://github.com/swcarpentry/make-novice) source
repository at commit
[ba7c2dd](https://github.com/swcarpentry/make-novice/tree/ba7c2ddeecc2deb6fbd540107f3d4446c85675fe)

    Mike Jackson (ed.): "Software Carpentry: Automation and Make."
    Version 2016.06, June 2016,
    https://github.com/swcarpentry/make-novice, 10.5281/zenodo.57473.

The following instructions are adapted from https://carpentries.github.io/workbench/

Maintainer(s):

- Kyle Brindley

## Site Environment

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

## Site and Lessons Environment

The combined environment for building the site and running the lessons can be built from the version
controlled `environment.yml` file. This is the environment used by the CI server for testing.

```
$ conda env create --name scons-lesson-dev --file environment.yml
$ TMPDIR=/scratch/$USER/workbench R -e 'install.packages(c("sandpaper", "varnish", "pegboard", "tinkr"), repos = list(carpentries="https://carpentries.r-universe.dev/", CRAN="https://cloud.r-project.org"))'
```
