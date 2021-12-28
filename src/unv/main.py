from code import InteractiveConsole
from argparse import ArgumentParser
from .compile import compile

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
    def push(self, line):
        self.buffer.append(line)
        source = "\n".join(self.buffer)
        more = self.runsource(compile(source), self.filename)
        if not more:
            self.resetbuffer()
        return more


def main():
    parser = ArgumentParser(description=INTRO)
    parser.add_argument("file", help="An Unv source file to run")
    args = parser.parse_args()

    if args.file:
        exec(open(args.file, "r").read(), {})
    else:
        console = UnvConsole({"true": True, "false": False})
        console.interact("Interactive Unv Console.")


if __name__ == "__main__":
    main()
