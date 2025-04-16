---
title: Self-Documenting SConstruct files
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
can be useful, both for ourselves and for others, to provide a `--help`
option in our SConstruct file. This can provide a summary of the names of
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
  --variables  Print the text files returned by Glob and exit (default: False)

Default Targets:
  results.txt

Aliases:
  dats
```

Where SCons is composing the help message for our custom command-line options for us already. So,
how would we implement this? We could call `Help` like:

```python
help_message = "\n\nDefault Targets:\n  results.txt\n\nAliases:\n  dats"
env.Help(help_message, append=True, keep_local=True)
```

But every time we add or remove a task, or change the default target list, we would have to update
the help message string manually. It would be better if we
could construct the list of default targets and aliases from the configured tasks. We can use the
SCons `default_ans` and `DEFAULT_TARGETS` variables. First update the imports at the top of the
`scons_lesson_configuration.py` file

```python
import pathlib

import SCons.Script
from SCons.Script import DEFAULT_TARGETS
from SCons.Node.Alias import default_ans
```

Then add new help message construction functions at the bottom of the
`scons_lesson_configuration.py` file.

```python
def return_help_content(nodes, message="", help_content=dict()):
    """Return a dictionary of {node: message} string pairs

    Helpful in constructing help content for :meth:`project_help`. Will not
    overwrite existing keys.

    :param nodes: SCons node objects, e.g. targets and aliases
    :param str message: Help message to assign to every node in nodes
    :param dict help_content: Optional dictionary with target help messages
        ``{target: help}``

    :returns: Dictionary of {node: message} string pairs
    :rtype: dict
    """
    new_help_content = {str(node): message for node in nodes}
    new_help_content.update(help_content)
    return new_help_content


def project_help(help_content=dict()):
    """Append the SCons help message with default targets and aliases

    Must come *after* all default targets and aliases are defined.

    :param dict help_content: Optional dictionary with target help messages
        ``{target: help}``
    """
    def add_content(nodes, message="", help_content=help_content):
        """Append a help message for all nodes using provided help content if
        available.

        :param nodes: SCons node objects, e.g. targets and aliases
        :param str message: Help message to assign to every node in nodes
        :param dict help_content: Optional dictionary with target help messages
            ``{target: help}``

        :returns: appended help message
        :rtype: str
        """
        keys = [str(node) for node in nodes]
        for key in keys:
            if key in help_content.keys():
                message += f"    {key}: {help_content[key]}\n"
            else:
                message += f"    {key}\n"
        return message

    defaults_message = add_content(
        DEFAULT_TARGETS, message="\nDefault Targets:\n"
    )
    alias_message = add_content(default_ans, message="\nTarget Aliases:\n")
    SCons.Script.Help(
        defaults_message + alias_message, append=True, keep_local=True
    )
```

Finally, update the bottom of the `SConstruct` file with the new function calls. It is important
that the `project_help` call comes *after* all default targets are assigned and all aliases are
created.

```python
dats = env.Alias("dats", DATA_FILES)
help_content = return_help_content(
    dats,
    "Count words in text files.",
)

results = env.Command(
    target=["results.txt"],
    source=[ZIPF_SOURCE] + DATA_FILES,
    action=["${language} ${zipf_source} ${SOURCES[1:]} > ${TARGET}"],
    language=LANGUAGE,
    zipf_source=ZIPF_SOURCE,
)
help_content = return_help_content(
    results,
    "Generate Zipf summary table.",
    help_content,
)

env.Default(["results.txt"])

project_help(help_content)
```

If we now run

```bash
$ scons --help
```

we get some SCons status messages, our help message, and the hint for the full SCons help message:

```output
scons: Reading SConscript files ...
scons: done reading SConscript files.
Local Options:
  --variables  Print the files returned by Glob and exit (default: 'False')

Default Targets:
    results.txt: Generate Zipf summary table.

Target Aliases:
    dats: Count words in text files.

Use scons -H for help about SCons built-in command-line options.
```

If we add, change or remove a default target or alias, we will automatically see updated lists in
our help messages.

:::::::::::::::::::::::::::::::::::::::::  callout

## Where We Are

[This SConstruct file](files/code/08-self-doc/SConstruct)
and this [Python module](files/code/08-self-doc/scons_lesson_configuration.py)
contain all of our work so far.


::::::::::::::::::::::::::::::::::::::::::::::::::

:::::::::::::::::::::::::::::::::::::::: keypoints

- Document SConstruct options, targets, and aliases with the SCons `default_ans` and
  `DEFAULT_TARGETS` variables and the `Help` function.

::::::::::::::::::::::::::::::::::::::::::::::::::

