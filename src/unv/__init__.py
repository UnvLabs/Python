def compile(input):
  input = input.replace(
    /("(?:\\["\\]|[^"\\])*"|'(?:\\['\\]|[^'\\])*')|###[^]*?###|#.*/gm,
    (_, string) => (string ? string.replace(/\n/g, "\\n") : "")
  )
  lines = input.split("\n")
  comment = false
  indents = []
  output = ""
  for line in lines:
    statement = line.match(
      /^(\s*)(if|else|switch|try|catch|(?:async\s+)?function\*?|class|do|while|for)\s+(.+)/
    )
    if statement:
      let [, spaces, name, args] = statement
      indents.unshift(spaces.length)
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
