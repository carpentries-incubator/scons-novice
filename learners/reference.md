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

SCons uses [Python][python] as the [configuration language][configuration-language]. Tasks can be
defined in Python class/function call syntax.

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

Cleaning targets:

SCons can clean specific targets with the `--clean` option

```bash
$ scons target --clean
```

and clean all targets with the `.` special target

```bash
$ scons . --clean
```

Alias targets:

SCons can define [aliases][aliases] as short-hand for collections of build targets.

```python
target_nodes = Command(
    target=["target1", "target2"],
    source=["source"],
    action=["action"]
)
Alias("target_alias", target_nodes)
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

Builders:

SCons users can write custom
[builders][builders] for commonly
re-used actions.

```python
my_builder = Builder(
    action=["action"]
)
env = Environment(BUILDERS={"MyBuilder": my_builder})
env.MyBuilder(
    target=["target"],
    source=["source"]
)
```

Psuedo-builders:

SCons users can write custom [pseudo-builders][pseudo-builders] to handle common file types or
Builder argument parsing.

```python
import pathlib


def count_books(env, name, count_executable="python", count_source="count_words.py"):
    target = [f"{name}.dat"]
    source = [
        pathlib.Path("books") / f"{name}.txt",
        count_source,
    ]
    target_nodes = env.Command(
        target=target,
        source=source,
        action=["${count_executable} ${count_source} ${TARGET} ${SOURCES}"],
        count_executable=count_executable,
        count_source=count_source,
    )
    return target_nodes


env = Environment()
env.AddMethod("CountBooks", count_books)
env.CountBooks("isles")
env.CountBooks("abyss")
```

Defining and using variables:

SCons uses [Python][python] as the [configuration language][configuration-language]. Variables may
be defined in Python syntax.

```python
count_source="wordcount.py"
count_executable=f"python {count_source}"
```

- A variable is assigned a value. For example, `count_source`
  is assigned the string `"wordcount.py"`.
- [f-string][f-string] syntax
  allows string construction from variables. The value of `count_source` will be used in the string
  construction of `count_exectuable`.

Suppress printing of actions:

SCons provides several mechanisms to control output. The `-Q` flag suppresses printing of all
progress messages. Task actions may suppress printing commands with a preceding `@` symbol.

```python
target_nodes = Command(
    target=["target"],
    source=["source"],
    action=["@action"],
)
Alias("target", target_nodes)
```

- Prefix an action by `@` to instruct SCons not to print that action.

Multiple configuration files:

SCons provides the option to call more than one configuration file with the [SConscript][SConscript]
function. These are conventionally named `SConscript`, but could take any file name.

```python
SConscript("SConscript")
SConscript("configuration")
```

wildcard function:

SCons provides a [Glob][Glob] method to construct lists of files.

```python
text_files=Glob("books/*.txt")
```

- Looks for all files matching a pattern e.g. `books/*.txt`, and
  return these in a list.
- e.g. `text_files` is set to `["books/abyss.txt", "books/isles.txt", "books/last.txt",
  "books/sierra.txt"]`.

List comprehensions:

Python has a [list comprehension][list-comprehension] feature for constructing lists. In combination
with the [pathlib][pathlib] OS agnostic path manipulation can be performed on lists of files.

```python
import pathlib
text_files = ["books/abyss.txt", "books/isles.txt", "books/last.txt", "books/sierra.txt"]
text_paths = [pathlib.Path(book) for book in text_files]
data_paths = [book.with_suffix("*.dat") for book in text_paths if book.parent == "books" and book.suffix == ".txt"]
data_files = [str(book) for book in book_paths]
```

- Every string that matches `books/*.txt` in `text_paths` is replaced by `*.dat` and the strings are
  returned in a list.
- e.g. if `text_files` is `["books/abyss.txt", "books/isles.txt", "books/last.txt",
  "books/sierra.txt"]` this sets `data_files` to `["books/abyss.dat", "books/isles.dat",
  "books/last.dat", "books/sierra.dat"]`.
- SCons >= 4.6 can operate on pathlib objects natively, so the final conversion back to strings is
  not strictly necessary.

Default targets:

SCons has a [Default][Default] function for changing the default target list.

- Unless otherwise specified, all targets are part of the default targets list.
- If the `Default` method is called, only those targets explicitly included are part of the default
  targets list

```python
Default(target_nodes)
```

## Manuals

[SCons Documentation][scons-documentation] includes

- [SCons User Guide][scons-user]
- [SCons Manpage][scons-man]

## Glossary

[action]{#action}
:   The steps a [build manager](#build-manager) must take to create or
update a file or other object.

[assignment]{#assignment}
:   A request that [Python](#glossary-python) stores something in a [variable](#variable).

[build file]{#build-file}
:   A synonym for [configuration file](#configuration-file)

[configuration file]{#configuration-file}
:   A description of [tasks](#task) for a [build manager](#build-manager).  Also called a [build
file](#build-file).

[build manager]{#build-manager}
:   A program, such as [SCons](#scons), whose main purpose is to build or
update software, documentation, web sites, data files, images, and
other things.

[default target]{#default-target}
:   The [target](#target) that is built if no [target](#target) is specified when a [build
manager](#build-manager) is run.

[dependency]{#dependency}
:   A synonym for [source](#source).

[function]{#function}
:   A [Python](#glossary-python), [SCons](#scons), or user-defined function that performs some operation, for
example gets a list of files matching a pattern.

[Glob]{#glossary-glob}
:   A pattern matching search function provided by [SCons](#scons): [Glob][glob].

[incremental build]{#incremental-build}
:   The feature of a [build manager](#build-manager) by
which it only rebuilds files that, either directory
or indirectly, depend on a file that was changed.

[Make]{#make}
:   A popular [build manager](#build-manager), from GNU, created in 1977.

[Makefile]{#makefile}
:   A [build file](#build-file) used by [Make](#make), which, by
default, are named `Makefile`.

[prerequisite]{#prerequisite}
:   A synonym for [source](#source).

[Python]{#glossary-python}
:   A commonly used programming language in computational science and engineering.

[SCons]{#scons}
:   A [Python](#glossary-python)-based, open-source [build manager](#build-manager) based on the `ScCons` build tool
designed for a Software Carpentry Build competition in August 2000: [SCons][scons].

[SConstruct]{#sconstruct}
:   The primary [configuration file](#configuration-file) for the [SCons](#scons) [build
manager](#build-manager).

[SConscript]{#sconscript}
:   The conventional name for secondary [configuration file](#configuration-file)s for the
[SCons](#scons) [build manager](#build-manager).

[source]{#source}
:   A file that a [target](#target) depends on. If any of a target's [sources](#source) are newer
than the target itself, the target needs to be updated. A target's sources are also called its
[prerequisites](#prerequisite) or [dependencies](#dependency). If a target's sources do not exist,
then they need to be built first.

[special variable]{#special-variable}
:   A reserved [variable](#variable) that [SCons](#scons) will substitute with its value in action
strings.

[stem]{#stem}
:   The part of the target that was matched by the pattern rule. If
the target is `file.dat` and the target pattern was `%.dat`, then
the stem `$*` is `file`.

[target]{#target}
:   A thing to be created or updated, for example a file. Targets can have [sources](#source) that
must exist, and be up-to-date, before the target itself can be built or updated.

[task]{#task}
:   A specification of a [target](#target)'s [sources](#source) and what [actions](#action) need to
be executed to build or update the target.

[variable]{#variable}
:   A symbolic name for something in an [SCons](#scons) configuration file.

[wildcard]{#wildcard}
:   A pattern that can be specified in the [Glob](#glossary-glob) function search for files.

[gnu-make-manual]: https://www.gnu.org/software/make/manual/
[options-summary]: https://www.gnu.org/software/make/manual/html_node/Options-Summary.html
[quick-reference]: https://www.gnu.org/software/make/manual/html_node/Quick-Reference.html
[automatic-variables]: https://www.gnu.org/software/make/manual/html_node/Automatic-Variables.html
[special-targets]: https://www.gnu.org/software/make/manual/html_node/Special-Targets.html

[python]: https://www.python.org/
[scons-documentation]: https://scons.org/documentation.html
[scons-user]: https://scons.org/doc/production/HTML/scons-user.html
[scons-man]: https://scons.org/doc/production/HTML/scons-man.html
[configuration-language]: https://scons.org/doc/production/HTML/scons-user.html#sect-sconstruct-python
[builders]: https://scons.org/doc/production/HTML/scons-user.html#chap-builders-writing
[aliases]: https://scons.org/doc/production/HTML/scons-man.html#f-Alias
[pseudo-builders]: https://scons.org/doc/production/HTML/scons-user.html#chap-add-method
[f-string]: https://docs.python.org/3/tutorial/inputoutput.html#formatted-string-literals
[SConscript]: https://scons.org/doc/production/HTML/scons-user.html#sect-sconscript-files
[Glob]: https://scons.org/doc/production/HTML/scons-man.html#f-Glob
[list-comprehension]: https://docs.python.org/3/tutorial/datastructures.html#list-comprehensions
[pathlib]: https://docs.python.org/3/library/pathlib.html
[Default]: https://scons.org/doc/production/HTML/scons-user.html#sect-default-targets-function
