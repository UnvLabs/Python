import re

def replacer(match):
    if match.group(1):
        return re.sub(r"\n", "\\n", group())
    else:
        return ""

REPLACERE = r"""("(?:\\["\\]|[^"\\])*"|'(?:\\['\\]|[^'\\])*')|###[\s\S]*?###|#.*"""

STAT = r"^(\s*)(if|else|switch|try|catch|(?:async\s+)?function\*?|class|do|while|for)\s+(.+)"
def compile(input):
    input = re.sub(REPLACERE, replacer, input)
    lines = input.splitlines()
    comment = false
    indents = []
    output = ""
    for line in lines:
        statement = re.search(STAT, line)
        if statement:
            indents.push(spaces.length)
            output += `${spaces}${name} ${
        /function|try|class/.test(name) ? args : `(${args})`
      } {\n`
    else:
      spaces = line.match(/^\s*/)[0].length;
      for indent in indents.copy():
        if indent < spaces: break
        output += `${" ".repeat(indent)}}\n`
        indents.shift()
      }
      output +=
        line.replace(/^([\w\s,=]+)=(.*)/, (_, start, end) => {
          let vars = start.split("=");
          return `${
            vars.length > 1 ? `var ${vars.slice(1).join(",")}\n` : ""
          }var ${vars
            .map((a) => (~a.indexOf(",") ? `[${a}]` : a))
            .join("=")}=$assign(${end})`;
        }) + "\n"
    }
  }
  return output;
}
