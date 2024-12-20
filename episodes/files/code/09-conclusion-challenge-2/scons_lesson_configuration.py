import pathlib

import SCons.Script
from SCons.Script import DEFAULT_TARGETS
from SCons.Node.Alias import default_ans

COUNT_SOURCE = "countwords.py"
LANGUAGE = "python"
ZIPF_SOURCE = "testzipf.py"
TEXT_FILES = SCons.Script.Glob("books/*.txt")
DATA_FILES = [
    pathlib.Path(str(text_file)).with_suffix(".dat").name
    for text_file in TEXT_FILES
]
PLOT_SOURCE = "plotcounts.py"
PLOT_FILES = [
    pathlib.Path(data_file).with_suffix(".png").name
    for data_file in DATA_FILES
]
CODE_FILES = SCons.Script.Glob("*.py")


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


def plot_counts(env, plot_files, language=LANGUAGE, plot_source=PLOT_SOURCE):
    """Pseudo-builder to produce `.png` targets from the `plotcounts.py` script

    Assumes that the source data files are found in `{plot_file}.dat`

    :param env: SCons construction environment. Do not provide when using this
        function with the `env.AddMethod` and `env.CountWords` access style.
    :param plot_files: List of string names of the plot files to create.
    """
    target_nodes = []
    for plot_file in plot_files:
        plot_path = pathlib.Path(plot_file)
        data_file = plot_path.with_suffix(".dat")
        target_nodes.extend(
            env.Command(
                target=[plot_file],
                source=[data_file, plot_source],
                action=["${language} ${plot_source} ${SOURCES[0]} ${TARGET}"],
                language=language,
                plot_source=plot_source,
            )
        )
    return target_nodes


def return_help_content(nodes, message="", help_content=dict()):
    """Return a dictionary of {node: message} string pairs

    Helpful in constructing help content for :meth:`project_help`. Will not
    overwrite existing keys.

    :param nodes: SCons node objects, e.g. targets and aliases
    :param message: Help message to assign to every node in nodes

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
    def add_content(nodes, help_content=help_content, message=""):
        """Append a help message for all nodes using provided help content if
        available.

        :param nodes: SCons node objects, e.g. targets and aliases

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
