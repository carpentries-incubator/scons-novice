---
title: Variables
teaching: 15
exercises: 5
---

::::::::::::::::::::::::::::::::::::::: objectives

- Use variables in a Makefile.
- Explain the benefits of decoupling configuration from computation.

::::::::::::::::::::::::::::::::::::::::::::::::::

:::::::::::::::::::::::::::::::::::::::: questions

- How can I eliminate redundancy in my Makefiles?

::::::::::::::::::::::::::::::::::::::::::::::::::

Despite our efforts, our Makefile still has repeated content, i.e.  the program we use to run our
scripts, `python`. Additionally, if we renamed our scripts we'd have to hunt through our SConstruct
file in multiple places.

We can introduce a Python [variables](../learners/reference.md#variable) after the import statements
in `SConstruct` to hold our script name:

```python
COUNT_SOURCE = "countwords.py"
```

This is a variable [assignment](../learners/reference.md#assignment) -
`COUNT_SOURCE` is assigned the value `"countwords.py"` and behaves like (actually is) normal Python
variable assignment.

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

[This Makefile](files/code/06-variables-challenge/Makefile)
contains a solution to this challenge.



:::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::::::::::::::::

We place variables intended for use as configuration constants at the top of an SConstruct file so
they are easy to find and modify. Alternatively, we can pull them out into a new
file that just holds variable definitions (i.e. delete them from
the original SConstruct file). Let us create `config.scons` file:

```python
# Count words script.
LANGUAGE=python
COUNT_SRC=countwords.py

# Test Zipf's rule
ZIPF_SRC=testzipf.py
```

We can then import `config.mk` into `Makefile` using:

```make
include config.mk
```

We can re-run Make to see that everything still works:

```bash
$ make clean
$ make dats
$ make results.txt
```

We have separated the configuration of our Makefile from its rules --
the parts that do all the work. If we want to change our script name
or how it is executed we just need to edit our configuration file, not
our source code in `Makefile`. Decoupling code from configuration in
this way is good programming practice, as it promotes more modular,
flexible and reusable code.

:::::::::::::::::::::::::::::::::::::::::  callout

## Where We Are

[This Makefile](files/code/06-variables/Makefile)
and [its accompanying `config.mk`](files/code/06-variables/config.mk)
contain all of our work so far.


::::::::::::::::::::::::::::::::::::::::::::::::::

:::::::::::::::::::::::::::::::::::::::: keypoints

- Define variables by assigning values to names.
- Reference variables using `$(...)`.

::::::::::::::::::::::::::::::::::::::::::::::::::


