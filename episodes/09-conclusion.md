---
title: Conclusion
teaching: 5
exercises: 30
---

::::::::::::::::::::::::::::::::::::::: objectives

- Understand advantages of automated build tools such as SCons.

::::::::::::::::::::::::::::::::::::::::::::::::::

:::::::::::::::::::::::::::::::::::::::: questions

- What are the advantages and disadvantages of using tools like SCons?

::::::::::::::::::::::::::::::::::::::::::::::::::

Automated build tools such as SCons can help us in a number of
ways. They help us to automate repetitive commands, hence saving us
time and reducing the likelihood of errors compared with running
these commands manually.

They can also save time by ensuring that automatically-generated
artifacts (such as data files or plots) are only recreated when the
files that were used to create these have changed in some way.

Through their notion of targets, sources, and actions, they serve
as a form of documentation, recording dependencies between code,
scripts, tools, configurations, raw data, derived data, plots, and
papers.

:::::::::::::::::::::::::::::::::::::::  challenge

## Creating PNGs

Add new rules, update existing rules, and add new variables to:

- Create `.png` files from `.dat` files using `plotcounts.py`.
- Update the default target to include the `.png` files.
- Remove all auto-generated files (`.dat`, `.png`,
  `results.txt`).

:::::::::::::::  solution

## Solution

[This SConstruct file](files/code/09-conclusion-challenge-1/SConstruct)
and this [Python module](files/code/09-conclusion-challenge-1/scons_lesson_configuration.py)
contain a simple solution to this challenge.

A more elegant solution would be to re-write the `count_words` pseudo-builder as a generic, two-file
Python script pseudo-builder that accepts a target file, source file, and Python script to assemble into an
action. There's a hint for such a conversion found in the implemented action string.

To remove all targets, use the SCons special `.` target and the `--clean` flag.

```bash
scons . --clean
```

:::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::::::::::::::::

The following figure shows the dependencies involved in building the `.` or 'all'
target, once we've added support for images:

![](fig/09-conclusion-challenge-1.png "results.txt dependencies once images have been added"){alt='results.txt dependencies once images have been added'}

:::::::::::::::::::::::::::::::::::::::  challenge

## Creating an Archive

Often it is useful to create an archive file of your project that includes all data, code
and results. An archive file can package many files into a single file that can easily be
downloaded and shared with collaborators. We can add steps to create the archive file inside
the SConstruct itself so it's easy to update our archive file as the project changes.

Edit the SConstruct to create an archive file of your project. Add new rules, update existing
rules and add new variables to:

- Create a `zipf_analysis.tar.gz` archive including our code, data, plots, the Zipf summary table,
  the SConstruct file with the SCons
  [`Tar` builder](https://scons.org/doc/production/HTML/scons-man.html#b-Tar).

- Update the default targets list so that it creates `zipf_analysis.tar.gz`.

- Print the values of any additional variables you have defined when
  `scons --variables` is called.

:::::::::::::::  solution

## Solution

[This SConstruct file](files/code/09-conclusion-challenge-2/SConstruct)
and this [Python module](files/code/09-conclusion-challenge-2/scons_lesson_configuration.py)
contain a simple solution to this challenge.


:::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::::::::::::::::

:::::::::::::::::::::::::::::::::::::::  challenge

## Archiving the SConstruct file

Why does the SCons task for the archive directory add the SConstruct to our archive of code,
data, plots and Zipf summary table?

:::::::::::::::  solution

## Solution

Our code files (`countwords.py`, `plotcounts.py`, `testzipf.py`) implement
the individual parts of our workflow. They allow us to create `.dat`
files from `.txt` files, and `results.txt` and `.png` files from `.dat` files.
Our SConstruct file, however, documents dependencies between
our code, raw data, derived data, and plots, as well as implementing
our workflow as a whole.


:::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::::::::::::::::

:::::::::::::::::::::::::::::::::::::::: keypoints

- SCons and SConscript files save time by automating repetitive work, and save thinking by
  documenting how to reproduce results.

::::::::::::::::::::::::::::::::::::::::::::::::::

