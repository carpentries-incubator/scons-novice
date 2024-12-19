---
title: Builders and Pseudo-builders
teaching: 10
exercises: 0
---

::::::::::::::::::::::::::::::::::::::: objectives

- Write SCons builders.

::::::::::::::::::::::::::::::::::::::::::::::::::

:::::::::::::::::::::::::::::::::::::::: questions

- How can I define common task operations for similar files?

::::::::::::::::::::::::::::::::::::::::::::::::::

Our SConstruct file still has repeated content. The task for each `.dat`
file are identical apart from the text and data file names. We can
replace these tasks with a single [builder](../learners/reference.md#builder) which can be used to
build any `.dat` file from a `.txt` file in `books/`:

```python
count_words_builder = env.Builder(
    action=["python ${SOURCES[-1]} ${SOURCES[0]} ${TARGET}"],
)
```

After creating the custom builder, we need to add it to the construction environment to make it
available for task definitions.

```python
env.Append(BUILDERS={"CountWords": count_words_builder})
```

Now we can convert our `.dat` tasks from the `Command` to `CountWords` builder.

```python
env.CountWords(
    target=["isles.dat"],
    source=["books/isles.txt", "countwords.py"],
)

env.CountWords(
    target=["abyss.dat"],
    source=["books/abyss.txt", "countwords.py"],
)

env.CountWords(
    target=["last.dat"],
    source=["books/last.txt", "countwords.py"],
)
```

Custom builders like `CountWords` allow us to apply the same action to many tasks.

If we re-run SCons,

```bash
$ scons dats --clean
$ scons dats
```

then we get:

```output
scons: Reading SConscript files ...
scons: done reading SConscript files.
scons: Building targets ...
python countwords.py books/isles.txt isles.dat
python countwords.py books/abyss.txt abyss.dat
python countwords.py books/last.txt last.dat
scons: done building targets.
```

We can further simplify the task definition by moving the text file handling with a Pseudo-builder.
Pseudo-builders behave like builders, but allow flexibility in task construction handling with
user-defined arguments. We will use the `pathlib` module to help us construct OS-agnostic paths and
perform path manipulation. At the top of your `SConstruct` file, update the imports as below.

```python
import os
import pathlib
```

Now define a new `count_words` pseudo-builder function to replace the `count_word_builders` and add
it to the construction environment.

```python
def count_words(env, data_file):
    """Pseudo-builder to run the `countwords.py` script and produce `.dat` target

    Assumes that the source text file is found in `books/{data_file}.txt`

    :param env: SCons construction environment. Do not provide when using this
        function with the `env.AddMethod` and `env.CountWords` access style.
    :param data_file: String name of the data file to create.
    """
    data_path = pathlib.Path(data_file)
    text_file = pathlib.Path("books") / data_path.with_suffix[".txt"]
    target_nodes = env.Command(
        target=[data_file],
        source=[text_file, "countwords.py"],
        action=["python ${SOURCES[-1]} ${SOURCES[0]} ${TARGET}"],
    )
    return target_nodes


env.AddMethod("CountWords", count_words)
```

This pseudo-builder has further reduced the interface necessary to define the `.dat` tasks, which
now can be re-written as

```python
env.CountWords("isles.dat")
env.CountWords("abyss.dat")
env.CountWords("last.dat")
```

For students familiar with GNU Make, pseudo-builders are similar to Make 'pattern rules', but
pseudo-builders are both more verbose and more flexible. Pseudo-builders require a full Python
function definition syntax, but they can do more than simple file extension pattern matching and
anything the user requires.

A psuedo-builder alone will not allow us to match arbitrary files using the `.dat` file extension.
If we desire the full Make 'pattern rule' behavior, we can accept a target name and match it to our
pseudo-builder with the SCons
[`COMMAND_LINE_TARGETS`](https://scons.org/doc/production/HTML/scons-user.html#sect-var-COMMAND-LINE-TARGETS)
variable.

Add the following to the bottom of your SConstruct file

```python
for target in COMMAND_LINE_TARGETS:
    if pathlib.Path(target).suffix == ".dat":
        env.CountWords(target)
```

Now we can define tasks for new files not found in our pre-defined tasks as

```bash
$ scons sierra.dat
```

```output
scons: Reading SConscript files ...
scons: done reading SConscript files.
scons: Building targets ...
python countwords.py books/sierra.txt sierra.dat
scons: done building targets.
```

:::::::::::::::::::::::::::::::::::::::::  callout

## Where We Are

[This SConstruct file](files/code/05-builders-patterns/SConstruct)
contains all of our work so far.


::::::::::::::::::::::::::::::::::::::::::::::::::

:::::::::::::::::::::::::::::::::::::::: keypoints

- Use the `Builder` function and `Append` the construction environment `BUILDERS` dictionary to
  define common actions.
- Use the `AddMethod` function and Python functions to define pseudo-builders with custom tailored
  task handling.
- Use the special SCons variable `COMMAND_LINE_TARGETS` to perform dynamic handling that
  depends on command line target requests.

::::::::::::::::::::::::::::::::::::::::::::::::::

