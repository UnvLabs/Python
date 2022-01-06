import re
from tokenize import tokenize, NEWLINE
from io import BytesIO

COMMENTS = r"###[\s\S]*?###|#.*"
STRINGS = r""""(?:\\["\\]|[^"\\])*"|'(?:\\['\\]|[^'\\])*'"""
STATEMENT = re.compile(
    r"^\s*()\s+.+", re.MULTILINE
)
FUNCTION = re.compile(r"^(\s*(?:async\s+)?)function(\*?\s+.+)", re.MULTILINE)

def compile(input):
    without_comments = re.sub(COMMENTS, "", input)
    strings_converted = re.sub(
        STRINGS,
        lambda match: match.group().replace("\n", "\\n"),
        without_comments,
    )
    tokens = tokenize(BytesIO(strings_converted.encode('utf-8')).readline)

    code = ""
    sqb = 0
    parens = 0
    braces = 0
    add_colon = false
    for token in tokens:
        if token.start != token.end:
            if token.type == 1 and token.string == "function":
                code += "def"
                add_colon = true
            else:
                if token.type == 1 and token.string in "if|else|switch|try|catch|class|do|while|for".split("|"):
                    add_colon = true
                if token.type == 54:
                    if token.string == "(": parens +=1
                    else if token.string == ")": parens -= 1
                    else if token.string == "[": sqb += 1
                    else if token.string == "]": sqb -= 1
                    else if token.string == "{": braces += 1
                    else if token.string == "}": braces -= 1
                if add_colon and token.type == NEWLINE and not sqb and not parens and not braces:
                    code += ":"
                    add_colon = false
                        
                code += token.string
