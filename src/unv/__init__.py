import re

COMMENTS = r"###[\s\S]*?###|#.*"
STRINGS = r""""(?:\\["\\]|[^"\\])*"|'(?:\\['\\]|[^'\\])*'"""
STATEMENT = re.compile(
    r"^\s*(if|else|switch|try|catch|class|do|while|for)\s+.+", re.MULTILINE
)
FUNCTION = re.compile(r"^(\s*(?:async\s+)?)function(\*?\s+.+)", re.MULTILINE)


def compile(input):
    without_comments = re.sub(COMMENTS, "", input)
    strings_converted = re.sub(
        STRINGS,
        lambda match: match.group().replace("\n", "\\n"),
        without_comments,
    )
    added_colons = re.sub(
        STATEMENT, lambda match: match.group() + ":", strings_converted
    )
    functions_converted = re.sub(
        FUNCTION,
        lambda match: match.group(1) + "def" + match.group(2) + ":",
        added_colons,
    )
    return functions_converted
