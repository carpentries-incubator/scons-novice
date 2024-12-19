---
title: SConscript files
teaching: 30
exercises: 10
---

::::::::::::::::::::::::::::::::::::::: objectives

- Recognize the key parts of the SConstruct file, tasks, targets, sources, and
  actions.
- Write a simple SConstruct file.
- Run SCons from the shell.
- Explain when and why to mark targets as `.PHONY`.
- Explain constraints on dependencies.

::::::::::::::::::::::::::::::::::::::::::::::::::

:::::::::::::::::::::::::::::::::::::::: questions

- How do I write a simple SConstruct file?

::::::::::::::::::::::::::::::::::::::::::::::::::

Create a file, called `SConstruct`, with the following content:

```python
import os


env = Environment(os.environ.copy())

# Count words.
env.Command(
    target=["isles.dat"],
    source=["books/isles.txt"],
    action=["python countwords.py books/isles.txt isles.dat"],
)
```

This is a [build file](../learners/reference.md#build-file), which for SCons is called an
[SConscript](../learners/reference.md#makefile) file - a file executed by SCons. `SConstruct` is the
conventional name for the root configuration file. Secondary configuration files are named
`SConscript` by convention, but can take any filename. Together all SCons configuration files take
the generic name `SConscript` files. From now on, SCons configuration files will be referred to
collectively as `SConscript` files, but it is important to remember that projects usually start with
the `SConstruct` file naming convention.

The syntax should be familiar to [Python](https://www.python.org/) users because SCons uses Python
as the configuration language. Note how the action resembles a line from our shell script.

Let us go through each section in turn:

- First we import the `os` module and create an SCons with a copy of the active shell environment
  [construction
  environment](https://scons.org/doc/production/HTML/scons-user.html#sect-construction-environments).
  Most build managers inherit the active shell environment by default. SCons requires a little more
  effort, but this separation of construction environment from the external environment is valuable in
  complex computational science and engineering workflows which may require several, mutually
  exclusive environments for each task in a single workflow or project. For the purposes of this
  lesson, we will use a single construction environment inherited from the shell's active Conda
  environment.
- `#` denotes a *comment*. Any text from `#` to the end of the line is
  ignored by SCons but could be very helpful for anyone reading your SConstruct file.
- `env.Command` is the generic task definition class used by SCons. Note that the task is defined
  inside a construction environment we created earlier. If there were more than one construction
  environment available, additional tasks could use unique, task specific, construction
  environments.
- `isles.dat` is a [target](../learners/reference.md#target), a file to be
  created, or built.
- `books/isles.txt` is a [source](../learners/reference.md#source), also called a
  [dependency](../learners/reference.md#dependency), a file that is needed to build or update the
  target. Targets can have one or more dependencies.
- `python countwords.py books/isles.txt isles.dat` is an
  [action](../learners/reference.md#action), a command to run to build or
  update the target using the sources. Targets can have one or more
  actions. These actions form a recipe to build the target
  from its sources and are executed similarly to a shell script.
- Targets, sources, and actions are passed as keyword arguments and may be a string or a list of
  strings.
- Together, the target, sources, and actions form a [task](../learners/reference.md#task).

Our task above describes how to build the target `isles.dat` using the
action `python countwords.py` and the source `books/isles.txt`.

Information that was implicit in our shell script - that we are
generating a file called `isles.dat` and that creating this file
requires `books/isles.txt` - is now made explicit by SCons' syntax.

Let's first ensure we start from scratch and delete the `.dat` and `.png`
files we created earlier:

```bash
$ rm *.dat *.png
```

By default, SCons looks for a root SConscript file, called `SConstruct`, and we can
run SCons as follows:

```bash
$ scons
```

By default, SCons prints several status messages and the actions it executes:

```output
scons: Reading SConscript files ...
scons: done reading SConscript files.
scons: Building targets ...
python countwords.py books/isles.txt isles.dat
scons: done building targets.
```

The status messages can be silenced with the `-Q` option.

Let's see if we got what we expected.

```bash
$ head -5 isles.dat
```

The first 5 lines of `isles.dat` should look exactly like before.

:::::::::::::::::::::::::::::::::::::::::  callout

## The SConstruct File Does Not Have to be Called `SConstruct`

We don't have to call our root SCons configuration file `SConstruct`. However, if we call it
something else we need to tell SCons where to find it. This we can do using `-f` flag. For example,
if our SConstruct file is named `MyOtherSConstruct`:

```bash
$ scons -f MyOtherSConstruct
```

SCons does not require a specific file extension. The suffix `.scons` can be used to identify
SConscript files that are not called `SConstruct` or `SConscript` e.g. `install.scons`,
`common.scons` etc.


::::::::::::::::::::::::::::::::::::::::::::::::::

When we re-run our SConstruct file, SCons now informs us that:

```output
scons: Reading SConscript files ...
scons: done reading SConscript files.
scons: Building targets ...
scons: `isles.dat' is up to date.
scons: done building targets.
```

This is because our target, `isles.dat`, has now been created, and
SCons will not create it again. To see how this works, let's pretend to
update one of the text files. Rather than opening the file in an
editor, we can use the shell `touch` command to update its timestamp
(which would happen if we did edit the file):

```bash
$ touch books/isles.txt
```

If we compare the timestamps of `books/isles.txt` and `isles.dat`,

```bash
$ ls -l books/isles.txt isles.dat
```

then we see that `isles.dat`, the target, is now older
than `books/isles.txt`, its dependency:

```output
-rw-r--r--    1 mjj      Administ   323972 Jun 12 10:35 books/isles.txt
-rw-r--r--    1 mjj      Administ   182273 Jun 12 09:58 isles.dat
```

If we run SCons again,

```bash
$ scons
```

it does not recreate `isles.dat`.

```output
scons: Reading SConscript files ...
scons: done reading SConscript files.
scons: Building targets ...
scons: `isles.dat' is up to date.
scons: done building targets.
```

Many build managers, such as [GNU Make](../episodes/01-intro.md#gnu-make) use timestamps to track
the state of source and target files. If we were using GNU Make, Make would have re-created the
`isles.dat` file.

By default SCons computes content signatures from the file content to track the state of source and
target files. If the content of a file has not changed, it is considered up-to-date and SCons will
not create it again. Computing the content signature takes more time than checking a timestamp, so
SCons provides an option to use the more traditional timestamp state. However, in computational science and
engineering workflows, which often contain tasks requiring hours or days to compute, the added time
required to check file content is often a valuable trade-off because it avoids launching
long-running tasks more robustly than a simple timestamp check.

To observe SCons re-creating the target `isles.dat`, we must actually modify the `books/isles.txt`
file. Any change to the file contents, even adding a newline, will change the content signature
computed as an `md5sum`. If we run the `md5sum` ourselves, we can see the signature change before
and after the file edit.

```bash
$ md5sum books/isles.dat
```

```output
6cc2c020856be849418f9d744ac1f5ee  books/isles.txt
```

```bash
$ echo "" >> books/isles.txt
```

We can see that appending a blank newline changes the computed content signature.

```bash
$ md5sum books/isles.dat
```

```output
22b5adfc3b267e2e658ba75de4aeb74b  books/isles.txt
```
If we run SCons again, it will re-create `isles.dat` because the content of the source file
`books/isles.txt` has changed.

```bash
$ scons
```

```output
scons: Reading SConscript files ...
scons: done reading SConscript files.
scons: Building targets ...
python countwords.py books/isles.txt isles.dat
scons: done building targets.
```

When it is asked to build a target, SCons checks the 'content signature' of both the target and its
sources and the 'action signature' of the associated action list. If any source or action content
has changed since the target was built, then the actions are re-run to update the target. Using this
approach, SCons knows to only rebuild the files that, either directly or indirectly, depend on the
file that changed. This is called an [incremental
build](../learners/reference.md#incremental-build).

:::::::::::::::::::::::::::::::::::::::::  callout

## SConscript Files as Documentation

By explicitly recording the inputs to and outputs from steps in our
analysis and the dependencies between files, SConscript files act as a type
of documentation, reducing the number of things we have to remember.


::::::::::::::::::::::::::::::::::::::::::::::::::

Let's add another task to the end of `SConstruct`:

```python
env.Command(
    target=["abyss.dat"],
    source=["books/absyss.txt"],
	  action=["python countwords.py books/abyss.txt abyss.dat"],
)
```

If we run SCons,

```bash
$ scons
```

then we get:

```output
scons: Reading SConscript files ...
scons: done reading SConscript files.
scons: Building targets ...
scons: `isles.dat' is up to date.
python countwords.py books/abyss.txt abyss.dat
scons: done building targets.
```

The first target is reported as up to date and SCons builds the second target. The default behavior
of SCons is to build all default targets, and unless otherwise specified, all targets are added to
the default targets list.

If we do not want to build all targets, we can also build a specific target by name. First, confirm
that running SCons again reports both targets up to date.

```bash
$ scons
```

```output
scons: Reading SConscript files ...
scons: done reading SConscript files.
scons: Building targets ...
scons: `isles.dat' is up to date.
scons: `abyss.dat' is up to date.
scons: done building targets.
```

Then confirm that when specifying a target, SCons only reports on the requested target.

```bash
$ scons abyss.dat
```

```output
scons: Reading SConscript files ...
scons: done reading SConscript files.
scons: Building targets ...
scons: `abyss.dat' is up to date.
scons: done building targets.
```

:::::::::::::::::::::::::::::::::::::::::  callout

## "Up to Date" Versus "Nothing to be Done"

If we ask SCons to build a file that already exists and is up to
date, then SCons informs us that:

```output
scons: `isles.dat' is up to date.
```

If we ask Make to build a file that exists but for which there is
no rule in our Makefile, then we get message like:

```bash
$ scons countwords.py
```

```output
scons: Nothing to be done for `countwords.py'.
```

`up to date` means that the `SConstruct` file has a task with one or more actions
whose target is the name of a file (or directory) and the file is up to date.

`Nothing to be done` means that
the file exists but either :

- the `SConstruct` file has no task for it, or
- the `SConstruct` file has a task for it, but that task has no actions


::::::::::::::::::::::::::::::::::::::::::::::::::

We may want to remove all our data files so we can explicitly recreate
them all. We can introduce a new target, and associated rule, to do
this. We will call it `clean`, as this is a common name for rules that
delete auto-generated files, like our `.dat` files:

```make
clean :
	rm -f *.dat
```

This is an example of a rule that has no dependencies. `clean` has no
dependencies on any `.dat` file as it makes no sense to create these
just to remove them. We just want to remove the data files whether or
not they exist. If we run Make and specify this target,

```bash
$ make clean
```

then we get:

```output
rm -f *.dat
```

There is no actual thing built called `clean`. Rather, it is a
short-hand that we can use to execute a useful sequence of
actions. Such targets, though very useful, can lead to problems. For
example, let us recreate our data files, create a directory called
`clean`, then run Make:

```bash
$ make isles.dat abyss.dat
$ mkdir clean
$ make clean
```

We get:

```output
make: `clean' is up to date.
```

Make finds a file (or directory) called `clean` and, as its `clean`
rule has no dependencies, assumes that `clean` has been built and is
up-to-date and so does not execute the rule's actions. As we are using
`clean` as a short-hand, we need to tell Make to always execute this
rule if we run `make clean`, by telling Make that this is a
[phony target](../learners/reference.md#phony-target), that it does not build
anything. This we do by marking the target as `.PHONY`:

```make
.PHONY : clean
clean :
	rm -f *.dat
```

If we run Make,

```bash
$ make clean
```

then we get:

```output
rm -f *.dat
```

We can add a similar command to create all the data files. We can put
this at the top of our Makefile so that it is the [default
target](../learners/reference.md#default-target), which is executed by default
if no target is given to the `make` command:

```make
.PHONY : dats
dats : isles.dat abyss.dat
```

This is an example of a rule that has dependencies that are targets of
other rules. When Make runs, it will check to see if the dependencies
exist and, if not, will see if rules are available that will create
these. If such rules exist it will invoke these first, otherwise
Make will raise an error.

:::::::::::::::::::::::::::::::::::::::::  callout

## Dependencies

The order of rebuilding dependencies is arbitrary. You should not
assume that they will be built in the order in which they are
listed.

Dependencies must form a directed acyclic graph. A target cannot
depend on a dependency which itself, or one of its dependencies,
depends on that target.


::::::::::::::::::::::::::::::::::::::::::::::::::

This rule (`dats`) is also an example of a rule that has no actions. It is used
purely to trigger the build of its dependencies, if needed.

If we run,

```bash
$ make dats
```

then Make creates the data files:

```output
python countwords.py books/isles.txt isles.dat
python countwords.py books/abyss.txt abyss.dat
```

If we run `make dats` again, then Make will see that the dependencies (`isles.dat`
and `abyss.dat`) are already up to date.
Given the target `dats` has no actions, there is `nothing to be done`:

```bash
$ make dats
```

```output
make: Nothing to be done for `dats'.
```

Our Makefile now looks like this:

```make
# Count words.
.PHONY : dats
dats : isles.dat abyss.dat

isles.dat : books/isles.txt
	python countwords.py books/isles.txt isles.dat

abyss.dat : books/abyss.txt
	python countwords.py books/abyss.txt abyss.dat

.PHONY : clean
clean :
	rm -f *.dat
```

The following figure shows a graph of the dependencies embodied within
our Makefile, involved in building the `dats` target:

![](fig/02-makefile.png "Dependencies represented within the Makefile"){alt='Dependencies represented within the Makefile'}

:::::::::::::::::::::::::::::::::::::::  challenge

## Write Two New Rules

1. Write a new rule for `last.dat`, created from `books/last.txt`.
2. Update the `dats` rule with this target.
3. Write a new rule for `results.txt`, which creates the summary
  table. The rule needs to:
  - Depend upon each of the three `.dat` files.
  - Invoke the action `python testzipf.py abyss.dat isles.dat last.dat > results.txt`.
4. Put this rule at the top of the Makefile so that it is the default target.
5. Update `clean` so that it removes `results.txt`.

The starting Makefile is [here](files/code/02-makefile/Makefile).

:::::::::::::::  solution

## Solution

See [this file](files/code/02-makefile-challenge/Makefile) for a solution.



:::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::::::::::::::::

The following figure shows the dependencies embodied within our
Makefile, involved in building the `results.txt` target:

![](fig/02-makefile-challenge.png "results.txt dependencies represented within the Makefile"){alt='results.txt dependencies represented within the Makefile'}

:::::::::::::::::::::::::::::::::::::::: keypoints

- Use `#` for comments in Makefiles.
- Write rules as `target: dependencies`.
- Specify update actions in a tab-indented block under the rule.
- Use `.PHONY` to mark targets that don't correspond to files.

::::::::::::::::::::::::::::::::::::::::::::::::::


