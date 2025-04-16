---
title: Special Substitution Variables
teaching: 10
exercises: 5
---

::::::::::::::::::::::::::::::::::::::: objectives

- Use SCons special substitution variables to remove duplication in SConscript files.
- Explain why shell wildcards in dependencies can cause problems.

::::::::::::::::::::::::::::::::::::::::::::::::::

:::::::::::::::::::::::::::::::::::::::: questions

- How can I abbreviate the tasks in my SConscript files?

::::::::::::::::::::::::::::::::::::::::::::::::::

After the exercise at the end of the previous episode, our SConstruct file looked like
this:

```python
import os

env = Environment(ENV=os.environ.copy())

env.Command(
    target=["isles.dat"],
    source=["books/isles.txt"],
    action=["python countwords.py books/isles.txt isles.dat"],
)

env.Command(
    target=["abyss.dat"],
    source=["books/abyss.txt"],
	action=["python countwords.py books/abyss.txt abyss.dat"],
)

env.Command(
    target=["last.dat"],
    source=["books/last.txt"],
	action=["python countwords.py books/last.txt last.dat"],
)

env.Alias("dats", ["isles.dat", "abyss.dat", "last.dat"])

env.Command(
    target=["results.txt"],
    source=["isles.dat", "abyss.dat", "last.dat"],
    action=["python testzipf.py abyss.dat isles.dat last.dat > results.txt"],
)

env.Default(["results.txt"])
```

Our SConstruct file has a lot of duplication. For example, the names of text
files and data files are repeated in many places throughout the
file. SConscript files are a form of code and, in any code, repeated code
can lead to problems e.g. we rename a data file in one part of the
SConscript file but forget to rename it elsewhere.

:::::::::::::::::::::::::::::::::::::::::  callout

## D.R.Y. (Don't Repeat Yourself)

In many programming languages, the bulk of the language features are
there to allow the programmer to describe long-winded computational
routines as short, expressive, beautiful code.  Features in Python
or R or Java, such as user-defined variables and functions are useful in
part because they mean we don't have to write out (or think about)
all of the details over and over again.  This good habit of writing
things out only once is known as the "Don't Repeat Yourself"
principle or D.R.Y.


::::::::::::::::::::::::::::::::::::::::::::::::::

Let us set about removing some of the repetition from our SConstruct file.

In our `results.txt` task we duplicate the data file names and the
name of the results file name:

```python
env.Command(
    target=["results.txt"],
    source=["isles.dat", "abyss.dat", "last.dat"],
    action=["python testzipf.py abyss.dat isles.dat last.dat > results.txt"],
)
```

Looking at the results file name first, we can replace it in the action
with `${TARGET}`:

```python
env.Command(
    target=["results.txt"],
    source=["isles.dat", "abyss.dat", "last.dat"],
    action=["python testzipf.py abyss.dat isles.dat last.dat > ${TARGET}"],
)
```

`${TARGET}` is an SCons
[special variable](../learners/reference.md#special-variable)
which means 'the target of the current task'. When SCons is run it will
replace this variable with the target name.

We can replace the sources in the action with `${SOURCES}`:

```make
env.Command(
    target=["results.txt"],
    source=["isles.dat", "abyss.dat", "last.dat"],
    action=["python testzipf.py ${SOURCES} > ${TARGET}"],
)
```

`${SOURCES}` is another special substitution variable which means 'all the dependencies
of the current task'. Again, when SCons is run it will replace this
variable with the sources.

Let's clean our workflow and re-run our task:

```bash
$ scons . --clean
$ scons results.txt
```

We get:

```output
scons: Reading SConscript files ...
scons: done reading SConscript files.
scons: Building targets ...
python countwords.py books/isles.txt isles.dat
python countwords.py books/abyss.txt abyss.dat
python countwords.py books/last.txt last.dat
python testzipf.py isles.dat abyss.dat last.dat > results.txt
scons: done building targets.
```

:::::::::::::::::::::::::::::::::::::::  challenge

## Update Dependencies

What will happen if you now execute:

```bash
$ touch *.dat
$ scons results.txt
```

1. nothing
2. all files recreated
3. only `.dat` files recreated
4. only `results.txt` recreated

:::::::::::::::  solution

## Solution

``1.` Nothing.

The content of the `*.dat` has not changed, so `results.txt` is up to date.

If you run:

```bash
$ echo "" | tee -a books/*.txt
$ scons results.txt
```

you will find that the `.dat` files as well as `results.txt` are recreated.

If you run:

```bash
$ echo "manually-edited-ouput-is-bad 1 0.1" | tee -a *.dat
$ scons results.txt
```

you will find that the `results.txt` file is recreated because the content signature of the `.dat`
files has changed. However, the `.dat` files are not recreated. Despite our edit, the source and
action signatures of the `.dat` tasks have not changed. It is important that you never edit targets
manually to avoid out-of-sync and reproducibility errors arising in the middle of your workflow.
You can rely on SCons to know when to rebuild targets if you have well defined tasks with complete
target and sources lists

If you run this command or manually edited the `.dat` files, be sure to clean and rebuild them to
remove the manually edited lines.

```bash
scons dats --clean
scons results.txt
```


:::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::::::::::::::::

As we saw, `${SOURCES}` means 'all the dependencies of the current task'. This
works well for `results.txt` as its action treats all the dependencies
the same - as the input for the `testzipf.py` script.

However, for some tasks, we may want to treat the first dependency
differently. For example, our tasks for `.dat` use their first (and
only) dependency specifically as the input file to `countwords.py`. If
we add additional dependencies (as we will soon do) then we don't want
these being passed as input files to `countwords.py` as it expects only
one input file to be named when it is invoked.

SCons allows Pythonic, zero-based indexing of special substitution variables
``${SOURCES}`` and ``${TARGETS}`` for this use case. For example, `${SOURCES[0]}` means 'the first
dependency of the current task'.

:::::::::::::::::::::::::::::::::::::::  challenge

## Rewrite `.dat` Tasks to Use Special Substitution Variables

Rewrite each `.dat` task to use the special substitution variables `${TARGET}` ('the
target of the current task') and `${SOURCES[0]}` ('the first dependency of the
current task').
[This file](files/code/03-variables/SConstruct) contains
the SConstruct immediately before the challenge.

:::::::::::::::  solution

## Solution

See [this file](files/code/03-variables-challenge/SConstruct)
for a solution to this challenge.


:::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::::::::::::::::

:::::::::::::::::::::::::::::::::::::::: keypoints

- Use `${TARGET}` to refer to the target of the current task.
- Use `${SOURCES}` to refer to the dependencies of the current task.
- Use `${SOURCES[0]}` to refer to the first dependency of the current task.

::::::::::::::::::::::::::::::::::::::::::::::::::

