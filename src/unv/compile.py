import re
from tokenize import tokenize, NEWLINE
from io import BytesIO

COMMENTS = r"###[\s\S]*?###|#.*"
STRINGS = r""""(?:\\["\\]|[^"\\])*"|'(?:\\['\\]|[^'\\])*'"""


def compile(input):
    without_comments = re.sub(COMMENTS, "", input)
    strings_converted = re.sub(
        STRINGS,
        lambda match: match.group().replace("\n", "\\n"),
        without_comments,
    )
    tokens = tokenize(BytesIO(strings_converted.encode("utf-8")).readline)

    code = ""
    sqb = 0
    parens = 0
    braces = 0
    add_colon = False
    for token in tokens:
        if token.start != token.end:
            if token.type == 1 and token.string == "function":
                code += "def"
                add_colon = True
            else:
                if (
                    token.type == 1
                    and token.string
                    in "if|else|switch|try|catch|class|do|while|for".split("|")
                ):
                    add_colon = True
                if token.type == 54:
                    if token.string == "(":
                        parens += 1
                    elif token.string == ")":
                        parens -= 1
                    elif token.string == "[":
                        sqb += 1
                    elif token.string == "]":
                        sqb -= 1
                    elif token.string == "{":
                        braces += 1
                    elif token.string == "}":
                        braces -= 1
                if (
                    add_colon
                    and token.type == NEWLINE
                    and not sqb
                    and not parens
                    and not braces
                ):
                    code += ":"
                    add_colon = False
                code += token.string
    return code
