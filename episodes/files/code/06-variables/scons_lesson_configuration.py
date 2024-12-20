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
