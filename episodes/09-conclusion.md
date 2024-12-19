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

[This Makefile](files/code/09-conclusion-challenge-1/SConstruct)
contains a simple solution to this challenge.

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
the Makefile itself so it's easy to update our archive file as the project changes.

Edit the Makefile to create an archive file of your project.  Add new rules, update existing
rules and add new variables to:

- Create a new directory called `zipf_analysis` in the project directory.

- Copy all our code, data, plots, the Zipf summary table, the Makefile and config.mk
  to this directory.
  The `cp -r` command can be used to copy files and directories
  into the new `zipf_analysis` directory:

  ```bash
  $ cp -r [files and directories to copy] zipf_analysis/
  ```

- Hint: create a new variable for the `books` directory so that it can be
  copied to the new `zipf_analysis` directory

- Create an archive, `zipf_analysis.tar.gz`, of this directory. The
  bash command `tar` can be used, as follows:

  ```bash
  $ tar -czf zipf_analysis.tar.gz zipf_analysis
  ```

- Update the target `all` so that it creates `zipf_analysis.tar.gz`.

- Remove `zipf_analysis.tar.gz` when `make clean` is called.

- Print the values of any additional variables you have defined when
  `make variables` is called.

:::::::::::::::  solution

## Solution

[This Makefile](files/code/09-conclusion-challenge-2/Makefile)
and [this `config.mk`](files/code/09-conclusion-challenge-2/config.mk)
contain a solution to this challenge.



:::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::::::::::::::::

:::::::::::::::::::::::::::::::::::::::  challenge

## Archiving the Makefile

Why does the Makefile rule for the archive directory add the Makefile to our archive of code,
data, plots and Zipf summary table?

:::::::::::::::  solution

## Solution

Our code files (`countwords.py`, `plotcounts.py`, `testzipf.py`) implement
the individual parts of our workflow. They allow us to create `.dat`
files from `.txt` files, and `results.txt` and `.png` files from `.dat` files.
Our Makefile, however, documents dependencies between
our code, raw data, derived data, and plots, as well as implementing
our workflow as a whole. `config.mk` contains configuration information
for our Makefile, so it must be archived too.



:::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::::::::::::::::

:::::::::::::::::::::::::::::::::::::::  challenge

## `touch` the Archive Directory

Why does the Makefile rule for the archive directory `touch` the archive directory after moving our code, data, plots and summary table into it?

:::::::::::::::  solution

## Solution

A directory's timestamp is not automatically updated when files are copied into it.
If the code, data, plots, and summary table are updated and copied into the
archive directory, the archive directory's timestamp must be updated with `touch`
so that the rule that makes `zipf_analysis.tar.gz` knows to run again;
without this `touch`, `zipf_analysis.tar.gz` will only be created the first time
the rule is run and will not be updated on subsequent runs even if the contents
of the archive directory have changed.



:::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::::::::::::::::

:::::::::::::::::::::::::::::::::::::::: keypoints

- Makefiles save time by automating repetitive work, and save thinking by documenting how to reproduce results.

::::::::::::::::::::::::::::::::::::::::::::::::::


