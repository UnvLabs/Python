import re
from tokenize import (
    tokenize,
    ENCODING,
    ENDMARKER,
    INDENT,
    DEDENT,
    NEWLINE,
    NL,
    NAME,
    OP,
    Untokenizer,
)
from io import BytesIO

COMMENTS = r"###[\s\S]*?###|#.*"
STRINGS = r""""(?:\\["\\]|[^"\\])*"|'(?:\\['\\]|[^'\\])*'"""
IMPORT = r"""import([\s\S]+?)from\s*("(?:\\["\\]|[^"\\])*"|'(?:\\['\\]|[^'\\])*')"""


class UnvUntokenizer(Untokenizer):
    def untokenize(self, iterable):
        it = iter(iterable)
        indents = []
        startline = False
        sqb = 0
        parens = 0
        braces = 0
        add_colon = False
        for t in it:
            if len(t) == 2:
                self.compat(t, it)
                break
            tok_type, token, start, end, line = t
            if tok_type == NAME:
                if token == "function":
                    token = "def"
                    add_colon = True
                if token in "if|else|switch|try|catch|class|do|while|for".split("|"):
                    add_colon = True
            elif tok_type == OP:
                if token == "(":
                    parens += 1
                elif token == ")":
                    parens -= 1
                elif token == "[":
                    sqb += 1
                elif token == "]":
                    sqb -= 1
                elif token == "{":
                    braces += 1
                elif token == "}":
                    braces -= 1
            elif (
                add_colon
                and tok_type == NEWLINE
                and not sqb
                and not parens
                and not braces
            ):
                token = ":" + token
                add_colon = False

            if tok_type == ENCODING:
                self.encoding = token
                continue
            if tok_type == ENDMARKER:
                break
            if tok_type == INDENT:
                indents.append(token)
                continue
            elif tok_type == DEDENT:
                indents.pop()
                self.prev_row, self.prev_col = end
                continue
            elif tok_type in (NEWLINE, NL):
                startline = True
            elif startline and indents:
                indent = indents[-1]
                if start[1] >= len(indent):
                    self.tokens.append(indent)
                    self.prev_col = len(indent)
                startline = False
            self.add_whitespace(start)
            self.tokens.append(token)
            self.prev_row, self.prev_col = end
            if tok_type in (NEWLINE, NL):
                self.prev_row += 1
                self.prev_col = 0
        return "".join(self.tokens)


def compile(input):
    without_comments = re.sub(COMMENTS, "", input)
    strings_converted = re.sub(
        STRINGS,
        lambda match: match.group().replace("\n", "\\n"),
        without_comments,
    )
    imports_resolved = re.sub(
        IMPORT,
        lambda match: "from "
        + match.group(2)[1:-1].replace("../", "..").replace("./", ".").replace("/", ".")
        + " import "
        + match.group(1),
        strings_converted,
    )
    tokens = tokenize(BytesIO(imports_resolved.encode("utf-8")).readline)

    ut = UnvUntokenizer()
    out = ut.untokenize(list(tokens))
    return out
