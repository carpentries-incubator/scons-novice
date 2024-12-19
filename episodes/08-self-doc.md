---
title: Self-Documenting SConscript files
teaching: 10
exercises: 0
---

::::::::::::::::::::::::::::::::::::::: objectives

- Write self-documenting SConstruct files with built-in help.

::::::::::::::::::::::::::::::::::::::::::::::::::

:::::::::::::::::::::::::::::::::::::::: questions

- How should I document an SConscript file?

::::::::::::::::::::::::::::::::::::::::::::::::::

Many bash commands, and programs that people have written that can be
run from within bash, support a `--help` flag to display more
information on how to use the commands or programs. In this spirit, it
can be useful, both for ourselves and for others, to provide a `help`
target in our SConstruct file. This can provide a summary of the names of
the key targets and what they do, so we don't need to look at the
SConstruct file itself unless we want to.

SCons provides the common `--help` flag and a `Help` function for building user customizable help
messages. The less common `-H` flag will print the SCons help message. For our SConstruct file,
running with `--help` option might print:

```bash
$ scons --help
```

```output
Local Options:
  --variables                 Print the text files returned by Glob (default $(default))

Default Targets:
  results.txt

Aliases:
  dats
```

Where SCons is composing the help message for our custom command-line options for us already. So,
how would we implement this? We could call `Help` like:

```python
help_message = (
    "\n\n"
    "Default Targets:\n"
    "  results.txt\n"
    "\n"
    "Aliases:\n"
    "  dats"
)
env.Help(help_message, append=True, keep_local=True)
```

But every time we add or remove a task, or change the default target list, we would have to update
the help message string manually. It would be better if we
could construct the list of default targets and aliases from the configured tasks. We can use the
SCons `default_ans` and `DEFAULT_TARGETS` variables. First update the imports at the top of the
`SConstruct` file

```python
from SCons.Node.Alias import default_ans
from SCons.Script import DEFAULT_TARGETS
```

Then add the help message construction at the bottom of the `SConstruct` file. It is important that
the `Help` call comes *after* all default targets are assigned and all aliases are created.

```python
help_message = "\nDefault Targets:\n"
for target in DEFAULT_TARGETS:
    help_message += f"    {str(target)}\n"
help_message += "\nTarget Aliases:\n"
for alias in default_ans:
    help_message += f"    {alias}\n"
env.Help(help_message, append=True, keep_local=True)
```

If we now run

```bash
$ scons --help
```

we get:

```output
scons: Reading SConscript files ...
scons: done reading SConscript files.
Local Options:
  --variables  Print the text files returned by Glob (default $(default))

Default Targets:
    results.txt

Target Aliases:
    dats

Use scons -H for help about SCons built-in command-line options.
```

If we add, change or remove a target or rule, we now only need to
remember to add, update or remove a comment next to the rule. So long
as we respect our convention of using `##` for such comments, then our
`help` rule will take care of detecting these comments and printing
them for us.

:::::::::::::::::::::::::::::::::::::::::  callout

## Where We Are

[This Makefile](files/code/08-self-doc/Makefile)
and [its accompanying `config.mk`](files/code/08-self-doc/config.mk)
contain all of our work so far.


::::::::::::::::::::::::::::::::::::::::::::::::::

[sed-docs]: https://www.gnu.org/software/sed/


:::::::::::::::::::::::::::::::::::::::: keypoints

- Document Makefiles by adding specially-formatted comments and a target to extract and format them.

::::::::::::::::::::::::::::::::::::::::::::::::::


