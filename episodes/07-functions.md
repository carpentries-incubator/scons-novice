---
title: Functions
teaching: 20
exercises: 5
---

::::::::::::::::::::::::::::::::::::::: objectives

- Write SConstruct that use functions to match and transform sets of files.

::::::::::::::::::::::::::::::::::::::::::::::::::

:::::::::::::::::::::::::::::::::::::::: questions

- How *else* can I eliminate redundancy in my SConscript files?

::::::::::::::::::::::::::::::::::::::::::::::::::

At this point, we have the following SConstruct file:

```python
import os
import pathlib

from scons_lesson_configuration import *

env = Environment(ENV=os.environ.copy())
env.AddMethod(count_words, "CountWords")

env.CountWords("isles.dat")
env.CountWords("abyss.dat")
env.CountWords("last.dat")

env.Alias("dats", ["isles.dat", "abyss.dat", "last.dat"])

env.Command(
    target=["results.txt"],
    source=[ZIPF_SOURCE, "isles.dat", "abyss.dat", "last.dat"],
    action=["${language} ${zipf_source} ${SOURCES[1:]} > ${TARGET}"],
    language=LANGUAGE,
    zipf_source=ZIPF_SOURCE,
)

env.Default(["results.txt"])

for target in COMMAND_LINE_TARGETS:
    if pathlib.Path(target).suffix == ".dat":
        env.CountWords(target)
```

Python and SCons have many [functions](../learners/reference.md#function) which can be used
to write more complex tasks. One example is `Glob`. `Glob` gets a
list of files matching some pattern, which we can then save in a
variable. So, for example, we can get a list of all our text files
(files ending in `.txt`) and save these in a variable by updating
the beginning of our `scons_lesson_configuration.py` file:

```python
import pathlib

import SCons.Script

COUNT_SOURCE = "countwords.py"
LANGUAGE = "python"
ZIPF_SOURCE = "testzipf.py"
TEXT_FILES = SCons.Script.Glob("books/*.txt")
```

Because our new Python module is no longer part of the SConstruct file, it does not have direct
access to the special SCons namespace. We need to import SCons like a Python package to use the
`Glob` function.

We can add a [custom command-line
option](https://scons.org/doc/production/HTML/scons-user.html#sect-AddOption) `--variables` to
our SConstruct file to print the `TEXT_FILES` value and exit configuration prior to building using Python
[f-string](https://docs.python.org/3/tutorial/inputoutput.html#formatted-string-literals) syntax:

```python
AddOption(
    "--variables",
    action="store_true",
    help="Print the text files returned by Glob and exit (default: %default)",
)
if GetOption("text_files"):
    text_file_strings = [str(node) for node in TEXT_FILES]
    print(f"TEXT_FILES: {text_file_strings}")
    Exit(0)
```

:::::::::::::::::::::::::::::::::::::::::  callout

## print and Exit

We can use the Python built-in `print` function to print to STDOUT, which is our terminal by
default. If we needed to execute a shell command, we could also use the
[`Execute`](https://scons.org/doc/production/HTML/scons-user.html#id1419) function to run a command
immediately during configuration instead of defining a task.

The SCons `Exit` function exits the configuration immediately. Here we use zero as the conventional
'success' code of most shells because the intended behavior of the `--text-file` option is
documented as an early exit from configuration.

::::::::::::::::::::::::::::::::::::::::::::::::::

If we run SCons:

```bash
$ scons --variables
```

We get:

```output
scons: Reading SConscript files ...
TEXT_FILES: ['books/abyss.txt', 'books/isles.txt', 'books/last.txt', 'books/sierra.txt']
```

Note how `sierra.txt` is now included too. There are some progress messages missing from the output
due to the early `Exit`. The configuration phase is exited immediately and there is no build phase.

We can construct a list of data files with a list comprehension that performs path manipulation of
the text files list to the `scons_lesson_configuration.py` module. We will use the `pathlib` module
again for OS-agnostic path separators.

```python
DATA_FILES = [
    pathlib.Path(str(text_file)).with_suffix(".dat").name
    for text_file in TEXT_FILES
]
```

We can extend the `--variables` option in SConstruct file to show the value of `DATA_FILES` too.
Recovering the SCons node objects into a string, then a `pathlib.Path`, and finally trimming the
parent directory returns a list of strings, so we can print the list directly.

```python
if GetOption("variables"):
    text_file_strings = [str(node) for node in TEXT_FILES]
    print(f"TEXT_FILES: {text_file_strings}")
    print(f"DATA_FILES: {DATA_FILES}")
    Exit(0)
```

If we run SCons,

```bash
$ scons --variables
```

then we get:

```output
scons: Reading SConscript files ...
TEXT_FILES: ['books/abyss.txt', 'books/isles.txt', 'books/last.txt', 'books/sierra.txt']
DATA_FILES: ['abyss.dat', 'isles.dat', 'last.dat', 'sierra.dat']
```

Finally, we can update our `count_words` function in `scons_lesson_configuration.py` to accept a
list of data files and reduce our `CountWords` function calls to a single instance in `SConstruct`.
We will have to collect the target nodes returned by `Command` and compile the full list of target
nodes to return from our psuedo-builder.

```python
def count_words(env, data_files, language=LANGUAGE, count_source=COUNT_SOURCE):
    """Pseudo-builder to produce `.dat` targets from the `countwords.py` script

    Assumes that the source text file is found in `books/{data_file}.txt`

    :param env: SCons construction environment. Do not provide when using this
        function with the `env.AddMethod` and `env.CountWords` access style.
    :param data_files: List of string names of the data files to create.
    """
    data_path = pathlib.Path(data_file)
    target_nodes = []
    for data_file in data_files:
        text_file = pathlib.Path("books") / data_path.with_suffix(".txt")
        target_nodes.extend(
            env.Command(
                target=[data_file],
                source=[text_file, count_source],
                action=["${language} ${count_source} ${SOURCES[0]} ${TARGET}"],
                language=language,
                count_source=count_source,
            )
        )
    return target_nodes
```

```python
env = Environment(ENV=os.environ.copy())
env.AddMethod(count_words, "CountWords")

env.CountWords(DATA_FILES)

env.Alias("dats", DATA_FILES)
```

Now, `sierra.txt` is processed, too. If you update the `Alias` function call, we can process all
`.txt` files with the same `dats` alias. The `COMMAND_LIST_TARGETS` loop is no longer required and
may be removed.

```bash
$ scons dats --clean
$ scons dats
```

We get:

```output
scons: Reading SConscript files ...
scons: done reading SConscript files.
scons: Building targets ...
python countwords.py books/abyss.txt abyss.dat
python countwords.py books/isles.txt isles.dat
python countwords.py books/last.txt last.dat
python countwords.py books/sierra.txt sierra.dat
scons: done building targets.
```

We can also rewrite `results.txt`:

```make
env.Command(
    target=["results.txt"],
    source=[ZIPF_SOURCE] + DATA_FILES,
    action=["${language} ${zipf_source} ${SOURCES[1:]} > ${TARGET}"],
    language=LANGUAGE,
    zipf_source=ZIPF_SOURCE,
)
```

If we re-run SCons:

```bash
$ scons . --clean
$ scons results.txt
```

We get:

```output
scons: Reading SConscript files ...
scons: done reading SConscript files.
scons: Building targets ...
python countwords.py books/abyss.txt abyss.dat
python countwords.py books/isles.txt isles.dat
python countwords.py books/last.txt last.dat
python countwords.py books/sierra.txt sierra.dat
python testzipf.py abyss.dat isles.dat last.dat sierra.dat > results.txt
scons: done building targets.
```

Let's check the `results.txt` file:

```bash
$ cat results.txt
```

```output
Book	First	Second	Ratio
abyss	4044	2807	1.44
isles	3822	2460	1.55
last	12244	5566	2.20
sierra	4242	2469	1.72
```

So the range of the ratios of occurrences of the two most frequent
words in our books is indeed around 2, as predicted by Zipf's Law,
i.e., the most frequently-occurring word occurs approximately twice as
often as the second most frequent word.

Here is our final SConstruct file:

```python
import os
import pathlib

from scons_lesson_configuration import *

AddOption(
    "--variables",
    action="store_true",
    default=False,
    help="Print the files returned by Glob and exit (default: '%default')",
)
if GetOption("variables"):
    text_file_strings = [str(node) for node in TEXT_FILES]
    print(f"TEXT_FILES: {text_file_strings}")
    print(f"DATA_FILES: {DATA_FILES}")
    Exit(0)

env = Environment(ENV=os.environ.copy())
env.AddMethod(count_words, "CountWords")

env.CountWords(DATA_FILES)

env.Alias("dats", DATA_FILES)

env.Command(
    target=["results.txt"],
    source=[ZIPF_SOURCE] + DATA_FILES,
    action=["${language} ${zipf_source} ${SOURCES[1:]} > ${TARGET}"],
    language=LANGUAGE,
    zipf_source=ZIPF_SOURCE,
)

env.Default(["results.txt"])
```

and the supporting `scons_lesson_configuration.py` module:

```python
import pathlib

import SCons.Script

COUNT_SOURCE = "countwords.py"
LANGUAGE = "python"
ZIPF_SOURCE = "testzipf.py"
TEXT_FILES = SCons.Script.Glob("books/*.txt")
DATA_FILES = [
    pathlib.Path(str(text_file)).with_suffix(".dat").name
    for text_file in TEXT_FILES
]


def count_words(env, data_files, language=LANGUAGE, count_source=COUNT_SOURCE):
    """Pseudo-builder to produce `.dat` targets from the `countwords.py` script

    Assumes that the source text files are found in `books/{data_file}.txt`

    :param env: SCons construction environment. Do not provide when using this
        function with the `env.AddMethod` and `env.CountWords` access style.
    :param data_files: List of string names of the data files to create.
    """
    target_nodes = []
    for data_file in data_files:
        data_path = pathlib.Path(data_file)
        text_file = pathlib.Path("books") / data_path.with_suffix(".txt")
        target_nodes.extend(
            env.Command(
                target=[data_file],
                source=[text_file, count_source],
                action=["${language} ${count_source} ${SOURCES[0]} ${TARGET}"],
                language=language,
                count_source=count_source,
            )
        )
    return target_nodes
```

The following figure shows the dependencies embodied within our SConstruct file,
involved in building the `results.txt` target,
now we have introduced our function:

![](fig/07-functions.png "results.txt dependencies after introducing a function"){alt='results.txt dependencies after introducing a function'}

:::::::::::::::::::::::::::::::::::::::::  callout

## Where We Are

[This SConstruct file](files/code/07-functions/SConstruct)
contains all of our work so far.


::::::::::::::::::::::::::::::::::::::::::::::::::

:::::::::::::::::::::::::::::::::::::::  challenge

## Adding more books

We can now do a better job at testing Zipf's rule by adding more books.
The books we have used come from the [Project Gutenberg](https://www.gutenberg.org/) website.
Project Gutenberg offers thousands of free ebooks to download.

**Exercise instructions:**

- go to [Project Gutenberg](https://www.gutenberg.org/) and use the search box to find another book,
  for example ['The Picture of Dorian Gray'](https://www.gutenberg.org/ebooks/174) from Oscar Wilde.
- download the 'Plain Text UTF-8' version and save it to the `books` folder;
  choose a short name for the file (**that doesn't include spaces**) e.g. "dorian\_gray.txt"
  because the filename is going to be used in the `results.txt` file
- optionally, open the file in a text editor and remove extraneous text at the beginning and end
  (look for the phrase `END OF THE PROJECT GUTENBERG EBOOK [title]`)
- run `scons` and check that the correct commands are run, given the dependency tree
- check the results.txt file to see how this book compares to the others


::::::::::::::::::::::::::::::::::::::::::::::::::

:::::::::::::::::::::::::::::::::::::::: keypoints

- SCons uses the Python programming language with acces to all of Python's many built-in functions.
- SCons provides many functions that work natively with the internal node objects required to manage
  the SCons directed graph.
- Use the SCons `Glob` function to get lists of SCons nodes from file names matching a pattern.
- Use Python built-in and standard library modules to manage file names and paths.

::::::::::::::::::::::::::::::::::::::::::::::::::

