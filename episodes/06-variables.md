---
title: Variables
teaching: 15
exercises: 5
---

::::::::::::::::::::::::::::::::::::::: objectives

- Use variables in SConscript files.
- Explain the benefits of decoupling configuration from computation.

::::::::::::::::::::::::::::::::::::::::::::::::::

:::::::::::::::::::::::::::::::::::::::: questions

- How can I eliminate redundancy in my SConscript files?

::::::::::::::::::::::::::::::::::::::::::::::::::

Despite our efforts, our SConstruct still has repeated content, i.e.  the program we use to run our
scripts, `python`. Additionally, if we renamed our scripts we'd have to hunt through our SConstruct
file in multiple places.

We can introduce Python [variables](../learners/reference.md#variable) after the import statements
in `SConstruct` to hold our script name:

```python
COUNT_SOURCE = "countwords.py"
```

This is a variable [assignment](../learners/reference.md#assignment) -
`COUNT_SOURCE` is assigned the value `"countwords.py"` and behaves like (actually is) normal Python
variable assignment. The all capitals naming convention indicates that the variable is intended for
use as a setting or constant value.

We can do the same thing with the interpreter language used to run the script:

```python
LANGUAGE = "python"
```

Similar to the SCons special substitution variables, we can define any number of per-task or
per-builder substitution variables with keyword arguments. The same `${...}` substitution syntax
tells SCons to replace a task action string variable with its value when SCons is run.

Defining the variable `LANGUAGE` in this way avoids repeating `python` in our
SConstruct file, and allows us to easily
change how our script is run (e.g. we might want to use a different
version of Python and need to change `python` to `python2` -- or we might want
to rewrite the script using another language (e.g. switch from Python to R)).

In the `count_words` pseudo-builder function we will define optional arguments `language` and
`count_source`, which are defined to default as `LANGUAGE` and `COUNT_SOURCE` respectively and passed
through as `Command` task keyword arguments. This tells SCons to replace the variable `language`
with its value `python`, and to replace the variable `count_source` with its value `countwords.py`.

We will define and use the intermediate function keyword argument variables instead of using the
upper case variables directly to avoid mixing up the function's scope with the `SConstruct` scope.
This is a detail of good practice in Python development, and since SConscript files are Python code,
you should follow the usual Python practices and style guides wherever possible.

:::::::::::::::::::::::::::::::::::::::  challenge

## Use Variables

Update `SConstruct` so that the `.dat` rule
references the variable `count_source` and `language`.
Then do the same for the `testzipf.py` script
and the `results.txt` rule,
using `ZIPF_SOURCE` as the variable name.

:::::::::::::::  solution

## Solution

[This SConstruct file](files/code/06-variables-challenge/SConstruct)
contains a solution to this challenge.


:::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::::::::::::::::

We place variables intended for use as configuration constants at the top of an SConstruct file so
they are easy to find and modify. Alternatively, we can pull them out into a new file that just
holds variable definitions (i.e. delete them from the original SConstruct file). Because SCons uses
Python as the configuration language, we can also move our custom builders and psuedo-builders. Let
us create `scons_lesson_configuration.py` from the content below.

```python
import pathlib

COUNT_SOURCE = "countwords.py"
LANGUAGE = "python"
ZIPF_SOURCE = "testzipf.py"


def count_words(env, data_file, language=LANGUAGE, count_source=COUNT_SOURCE):
    """Pseudo-builder to produce `.dat` targets from the `countwords.py` script

    Assumes that the source text file is found in `books/{data_file}.txt`

    :param env: SCons construction environment. Do not provide when using this
        function with the `env.AddMethod` and `env.CountWords` access style.
    :param data_file: String name of the data file to create.
    """
    data_path = pathlib.Path(data_file)
    text_file = pathlib.Path("books") / data_path.with_suffix(".txt")
    target_nodes = env.Command(
        target=[data_file],
        source=[text_file, count_source],
        action=["${language} ${count_source} ${SOURCES[0]} ${TARGET}"],
        language=language,
        count_source=count_source,
    )
    return target_nodes
```

An added benefit to moving our custom functions into a file with the `.py` extension is that we can
use automated documentation tools, such as [Sphinx](https://www.sphinx-doc.org/en/master/), to build
project documentation.

We can then import `scons_lesson_configuration.py` into the SConstruct file with a standard Python
import:

```python
from scons_lesson_configuration import *
```

Note that the above import statement merges the module namespace into the SConstruct file namespace.
We must be careful to avoid re-using variable and function names, which would overwrite the names
provided by our module.

We can re-run SCons to see that everything still works:

```bash
$ scons . --clean
$ scons dats
$ scons results.txt
```

:::::::::::::::::::::::::::::::::::::::::  callout

## Where We Are

[This SConstruct file](files/code/06-variables/SConstruct)
and this [Python module](files/code/06-variables/scons_lesson_configuration.py)
contain all of our work so far.


::::::::::::::::::::::::::::::::::::::::::::::::::

:::::::::::::::::::::::::::::::::::::::: keypoints

- Define variables by assigning values to names with Python syntax
- Reference variables using SCons substitution syntax `${...}`.

::::::::::::::::::::::::::::::::::::::::::::::::::

