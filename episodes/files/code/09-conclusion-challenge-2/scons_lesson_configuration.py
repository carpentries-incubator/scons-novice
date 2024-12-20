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
PNG_SOURCE = "plotcounts.py"
PLOT_FILES = [
    pathlib.Path(data_file).with_suffix(".png").name
    for data_file in DATA_FILES
]
CODE_FILES = Glob("*.py")


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
