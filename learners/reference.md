---
title: 'FIXME'
---

## Glossary

## Running SCons

To run SCons:

```bash
$ scons
```

SCons will look for a configuration file called `SConstruct` and will build the
default target(s).
.

To use a configuration file with a different name, use the `--sconstruct` option e.g.

```bash
$ scons --sconstruct=build-files/analyze
```

To build a specific target, provide it as an argument e.g.

```bash
$ scons isles.dat
```

If the target is up-to-date, SCons will print a message like:

```output
scons: Reading SConscript files ...
scons: done reading SConscript files.
scons: Building targets ...
scons: `isles.dat' is up to date.
scons: done building targets.
```

To see the actions SCons will run when building a target, without
running the actions, use the `--dry-run` flag e.g.

```bash
$ scons --dry-run isles.dat
```

Alternatively, use the abbreviation `-n`.

```bash
$ scons -n isles.dat
```

## Trouble Shooting

TBD

## Configuration files

SCons uses Python as the configuration file language. Tasks can be defined in Python class/function
call syntax.

Tasks:

```python
Command(
    target=["target"],
    source=["source1", "source2"]
    action=["action1", "action2"]
)
```

- Each task has one or more targets, the files to be created, or built.
- Each task has one or more sources, the depedencies that are needed to
  build the target.
- Targets and sources can be passed as list via keyword arguments.
- Each rule has one or more actions, commands to run to build the
  target using the sources.
- Actions are provided as a list of strings via keyword arguments.

Dependencies:

- If any source does not exist then SCons will look for a task to
  build it.
- The order of rebuilding dependencies is declarative. You should not
  assume that they will be built in the order in which they are listed.
- Dependencies must form a directed acyclic graph. A target cannot
  depend on a dependency which, in turn depends upon, or has a
  dependency which depends upon, that target.

Comments:

```python
# SCons uses Python for its configuration language. This is a Python comment.
```

List continuation:

```python
archive = [
    "isles.dat",
    "isles.png",
    "abyss.dat",
    "abyss.png",
    "sierra.dat",
    "sierra.png",
]
```

- If a list of targets, sources, or actions is too long, an SConstruct file can become more
  difficult to read.
- Python allows you to split up a list over multiple lines, to make them easier to read.
- Python will combine the multiple lines into a single list

Alias targets:

SCons can define [aliases](https://scons.org/doc/production/HTML/scons-man.html#f-Alias) as
short-hand for collections of build targets.

```python
targets = Command(
    target=["target1", "target2"],
    source=["source"],
    action=["action"]
)
Alias("target", targets)
```

- Alias targets are a short-hand for building target lists.

Special variables:

SCons has several [special
variables](https://scons.org/doc/production/HTML/scons-man.html#special_variables) available for
task construction. A few common use cases are mentioned here.

- `$SOURCE` and `$SOURCES[0]` denote 'the first source of the current task'.
- `$SOURCES` denotes 'the sources of the current task'.
- `$TARGET` and `$TARGETS[0]` denote 'the first target of the current task'.
- `$TARGETS` denotes 'the dependencies of the current task'.
- `$TARGET.filebase` denotes 'the stem of the first target of the current task'.

Pattern rules:

```make
%.dat : books/%.txt $(COUNT_SRC)
	$(COUNT_EXE) $< $@
```

- The Make wildcard, `%`, specifies a pattern.
- If Make finds a dependency matching the pattern, then the pattern is
  substituted into the target.
- The Make wildcard can only be used in targets and dependencies.
- e.g. if Make found a file called `books/abyss.txt`, it would set the
  target to be `abyss.dat`.

Defining and using variables:

```make
COUNT_SRC=wordcount.py
COUNT_EXE=python $(COUNT_SRC)
```

- A variable is assigned a value. For example, `COUNT_SRC`
  is assigned the value `wordcount.py`.
- `$(...)` is a reference to a variable. It requests that
  Make substitutes the name of a variable for its value.

Suppress printing of actions:

```make
.PHONY : variables
variables:
	@echo TXT_FILES: $(TXT_FILES)
```

- Prefix an action by `@` to instruct Make not to print that action.

Include the contents of a Makefile in another Makefile:

```make
include config.mk
```

wildcard function:

```make
TXT_FILES=$(wildcard books/*.txt)
```

- Looks for all files matching a pattern e.g. `books/*.txt`, and
  return these in a list.
- e.g. `TXT_FILES` is set to `books/abyss.txt books/isles.txt books/last.txt books/sierra.txt`.

patsubst ('path substitution') function:

```make
DAT_FILES=$(patsubst books/%.txt, %.dat, $(TXT_FILES))
```

- Every string that matches `books/%.txt` in `$(TXT_FILES)` is
  replaced by `%.dat` and the strings are returned in a list.
- e.g. if `TXT_FILES` is `books/abyss.txt books/isles.txt books/last.txt books/sierra.txt` this sets `DAT_FILES` to `abyss.dat isles.dat last.dat sierra.dat`.

Default targets:

- In Make version 3.79 the default target is the first target in the
  Makefile.
- In Make 3.81, the default target can be explicitly set using the
  special variable `.DEFAULT_GOAL` e.g.

```make
.DEFAULT_GOAL := all
```

## Manuals

[GNU Make Manual][gnu-make-manual]. Reference sections include:

- [Summary of Options][options-summary] for the `make` command.
- [Quick Reference][quick-reference] of Make directives, text manipulation functions, and special variables.
- [Automatic Variables][automatic-variables].
- [Special Built-in Target Names][special-targets]

## Glossary

[action]{#action}
:   The steps a [build manager](#build-manager) must take to create or
update a file or other object.

[assignment]{#assignment}
:   A request that [Make](#make) stores something in a
[variable](#variable).

[automatic variable]{#automatic-variable}
:   A variable whose value is automatically redefined for each
[rule](#rule). [Make](#make)'s automatic variables include `$@`,
which holds the rule's [target](#target), `$^`, which holds its
[dependencies](#dependency), and, `$<`, which holds the first of
its dependencies, and `$*`, which holds the [stem](#stem) with which
the pattern was matched. Automatic variables are typically used in
[pattern rules](#pattern-rule).

[build file]{#build-file}
:   A description of [dependencies](#dependency) and [rules](#rule)
for a [build manager](#build-manager).

[build manager]{#build-manager}
:   A program, such as [Make](#make), whose main purpose is to build or
update software, documentation, web sites, data files, images, and
other things.

[default rule]{#default-rule}
:   The [rule](#rule) that is executed if no [target](#target) is
specified when a [build manager](#build-manager) is run.

[default target]{#default-target}
:   The [target](#target) of the [default rule](#default-rule).

[dependency]{#dependency}
:   A file that a [target](#target) depends on. If any of a target's
[dependencies](#dependency) are newer than the target itself, the
target needs to be updated. A target's dependencies are also
called its prerequisites. If a target's dependencies do not exist,
then they need to be built first.

[false dependency]{#false-dependency}
:   This can refer to a [dependency](#dependency) that is artificial.
e.g. a false dependency is introduced if a data analysis script
is added as a dependency to the data files that the script
analyses.

[function]{#function}
:   A built-in [Make](#make) utility that performs some operation, for
example gets a list of files matching a pattern.

[incremental build]{#incremental-build}
:   The feature of a [build manager](#build-manager) by
which it only rebuilds files that, either directory
or indirectly, depend on a file that was changed.

[macro]{#macro}
:   Used as a synonym for [variable](#variable) in certain versions of
[Make](#make).

[Make]{#make}
:   A popular [build manager](#build-manager), from GNU, created in 1977.

[Makefile]{#makefile}
:   A [build file](#build-file) used by [Make](#make), which, by
default, are named `Makefile`.

[pattern rule]{#pattern-rule}
:   A [rule](#rule) that specifies a general way to build or update an
entire class of files that can be managed the same way. For
example, a pattern rule can specify how to compile any C file
rather than a single, specific C file, or, to analyze any data
file rather than a single, specific data file. Pattern rules
typically make use of [automatic variables](#automatic-variable)
and [wildcards](#wildcard).

[phony target]{#phony-target}
:   A [target](#target) that does not correspond to a file or other
object. Phony targets are usually symbolic names for sequences of
[actions](#action).

[prerequisite]{#prerequisite}
:   A synonym for [dependency](#dependency).

[reference]{#reference}
:   A request that [Make](#make) substitutes the name of a
[variable](#variable) for its value.

[rule]{#rule}
:   A specification of a [target](#target)'s
[dependencies](#dependency) and what [actions](#action) need to be
executed to build or update the target.

[stem]{#stem}
:   The part of the target that was matched by the pattern rule. If
the target is `file.dat` and the target pattern was `%.dat`, then
the stem `$*` is `file`.

[target]{#target}
:   A thing to be created or updated, for example a file. Targets can
have [dependencies](#dependency) that must exist, and be
up-to-date, before the target itself can be built or updated.

[variable]{#variable}
:   A symbolic name for something in a [Makefile](#makefile).

[wildcard]{#wildcard}
:   A pattern that can be specified in [dependencies](#dependency) and
[targets](#target). If [Make](#make) finds a dependency matching
the pattern, then the pattern is substituted into the
target. wildcards are often used in [pattern
rules](#pattern-rule). The Make wildcard is `%`.

[gnu-make-manual]: https://www.gnu.org/software/make/manual/
[options-summary]: https://www.gnu.org/software/make/manual/html_node/Options-Summary.html
[quick-reference]: https://www.gnu.org/software/make/manual/html_node/Quick-Reference.html
[automatic-variables]: https://www.gnu.org/software/make/manual/html_node/Automatic-Variables.html
[special-targets]: https://www.gnu.org/software/make/manual/html_node/Special-Targets.html



