from code import InteractiveConsole

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

def main(count, name):
    """Unv programming language"""
    console = UnvConsole({})
    try:
        import readline
    except ImportError:
        pass
    console.interact("Interactive Unv Console.")

def main():
    parser = argparse.ArgumentParser(description=INTRO, formatter_class=RawTextHelpFormatter)
    parser.add_argument('files', nargs='+', help='One or more source files that you would like converted.')
    parser.add_argument('-o', '--out-lang', help='Specify the desired output language. Defaults to JavaScript.',
                        dest='out_lang', type=str, choices=("py", "js"), default="")
    parser.add_argument('-e', '--out-ext', help='Specify the desired output files extension (such as py or js). '
                        'Default is baesd on lang', dest='out_ext', type=str,)
    parser.add_argument('-i' '--in-ext', help='Specify the extension of the files to parse. Defualt is .jiphy',
                        default="jiphy", dest="in_ext")
    parser.add_argument('-rc', '--recursive', dest='recursive', action='store_true',
                        help='Recursively look for files to convert')
    parser.add_argument('-od', '--out-dir', dest='out_dir', default="",
                        help="Specify in which directory files should be outputed")
    parser.add_argument('-d', '--diff', dest='diff', default=False, action='store_true',
                        help="Produce a diff that would result in running jiphy, "
                             "without actually performing any changes")
    parser.add_argument('-c', '--conform', dest='conform', default=False, action='store_true',
                        help="Conform all code within passed in files to the format implied by its extension")
    parser.add_argument('-v', '--version', dest='version', action='version',
                        version="Jiphy v.{0}".format(__version__))
    
    arguments = dict((key, value) for (key, value) in itemsview(vars(parser.parse_args())))



if __name__ == "__main__":
    main()
