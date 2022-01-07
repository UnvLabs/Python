from code import InteractiveConsole
from argparse import ArgumentParser
from tokenize import TokenError
from .compile import compile
import encodings

try:
    import readline
except ImportError:
    pass

INTRO = """
|     |  
|     | |/ \ \  /
 \___/  |   | \/   Compiler
"""


class UnvConsole(InteractiveConsole):
    def runsource(self, source, filename="<input>", symbol="single"):
        try:
            pycode = compile(source)
        except TokenError:
            return True

        if pycode is None:
            return True

        try:
            code = self.compile(pycode, filename, symbol)
        except (OverflowError, SyntaxError, ValueError):
            self.showsyntaxerror(filename)
            return False

        if code is None:
            return True

        # Case 3
        self.runcode(code)
        return False


def main():
    parser = ArgumentParser(description=INTRO)
    parser.add_argument("file", help="An Unv source file to run", nargs='?')
    args = parser.parse_args()

    if args.file:
        exec(open(args.file, "r").read(), {})
    else:
        console = UnvConsole({"true": True, "false": False})
        console.interact("Interactive Unv Console.")


if __name__ == "__main__":
    main()
