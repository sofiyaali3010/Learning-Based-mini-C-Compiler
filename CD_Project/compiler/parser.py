import re


def check_syntax(code):
    errors = []
    brace_stack = []
    expecting_open_brace = False

    lines = code.split("\n")

    for i, raw_line in enumerate(lines, start=1):
        line = raw_line.strip()

        if line == "":
            continue

        if expecting_open_brace:
            if line == "{":
                brace_stack.append("{")
                expecting_open_brace = False
                continue
            else:
                errors.append({
                    "line": i,
                    "problem": "Missing opening brace after main function",
                    "fix": "Add { after int main()"
                })
                expecting_open_brace = False

        if line.startswith("#include"):
            if not re.fullmatch(r"#include\s*<stdio\.h>", line):
                errors.append({
                    "line": i,
                    "problem": "Invalid header syntax",
                    "fix": "Use: #include<stdio.h>"
                })
            continue

        if line.startswith("int main"):
            if re.fullmatch(r"int\s+main\s*\(\s*\)\s*\{", line):
                brace_stack.append("{")
            elif re.fullmatch(r"int\s+main\s*\(\s*\)", line):
                expecting_open_brace = True
            else:
                errors.append({
                    "line": i,
                    "problem": "Invalid main function syntax",
                    "fix": "Use: int main(){"
                })
            continue

        if line == "{":
            brace_stack.append("{")
            continue

        if line == "}":
            if not brace_stack:
                errors.append({
                    "line": i,
                    "problem": "Extra closing brace",
                    "fix": "Remove this } or add a matching { before it"
                })
            else:
                brace_stack.pop()
            continue

        if line.startswith("int"):
            if not line.endswith(";"):
                errors.append({
                    "line": i,
                    "problem": "Missing semicolon",
                    "fix": "Add ; at the end of the declaration"
                })
                continue

            if not re.fullmatch(
                r"int\s+\w+(\s*=\s*[\w\d\(\)\+\-\*/%\s]+)?(\s*,\s*\w+(\s*=\s*[\w\d\(\)\+\-\*/%\s]+)?)*\s*;",
                line
            ):
                errors.append({
                    "line": i,
                    "problem": "Invalid variable declaration",
                    "fix": "Use format like: int a; or int a = 5;"
                })
            continue

        if line.startswith("scanf"):
            if not line.endswith(";"):
                errors.append({
                    "line": i,
                    "problem": "Missing semicolon after scanf",
                    "fix": "Add ; after scanf statement"
                })
                continue

            match = re.fullmatch(
                r'scanf\s*\(\s*"(.*?)"\s*,\s*(&\w+(\s*,\s*&\w+)*)\s*\)\s*;',
                line
            )

            if not match:
                errors.append({
                    "line": i,
                    "problem": "Invalid scanf syntax",
                    "fix": 'Use: scanf("%d", &a);'
                })
                continue

            format_string = match.group(1)
            format_count = len(re.findall(r"%d", format_string))
            variable_count = len(re.findall(r"&(\w+)", line))

            if format_count == 0:
                errors.append({
                    "line": i,
                    "problem": "Missing %d in scanf",
                    "fix": 'Use: scanf("%d", &a);'
                })
            elif format_count != variable_count:
                errors.append({
                    "line": i,
                    "problem": "scanf format count does not match variables",
                    "fix": f"Use exactly {variable_count} %d format specifier(s)"
                })

            continue

        if line.startswith("printf"):
            if not line.endswith(";"):
                errors.append({
                    "line": i,
                    "problem": "Missing semicolon after printf",
                    "fix": "Add ; after printf statement"
                })
                continue

            match = re.fullmatch(
                r'printf\s*\(\s*"(.*?)"\s*(,\s*\w+(\s*,\s*\w+)*)?\s*\)\s*;',
                line
            )

            if not match:
                errors.append({
                    "line": i,
                    "problem": "Invalid printf syntax",
                    "fix": 'Use: printf("%d", a);'
                })
                continue

            format_string = match.group(1)
            format_count = len(re.findall(r"%d", format_string))
            variable_count = len(re.findall(r",\s*(\w+)", line))

            if format_count != variable_count:
                errors.append({
                    "line": i,
                    "problem": "printf format count does not match variables",
                    "fix": f"Use exactly {variable_count} %d format specifier(s)"
                })

            continue

        if line.startswith("if"):
            if not re.fullmatch(r"if\s*\(.*\)\s*\{", line):
                errors.append({
                    "line": i,
                    "problem": "Invalid if statement",
                    "fix": "Use: if(condition){"
                })
            else:
                brace_stack.append("{")
            continue

        if line.startswith("for"):
            if not re.fullmatch(r"for\s*\(.*;.*;.*\)\s*\{", line):
                errors.append({
                    "line": i,
                    "problem": "Invalid for loop",
                    "fix": "Use: for(i=0;i<n;i=i+1){"
                })
            else:
                brace_stack.append("{")
            continue

        if line.startswith("while"):
            if not re.fullmatch(r"while\s*\(.*\)\s*\{", line):
                errors.append({
                    "line": i,
                    "problem": "Invalid while loop",
                    "fix": "Use: while(condition){"
                })
            else:
                brace_stack.append("{")
            continue

        if line.startswith("return"):
            if not re.fullmatch(r"return\s+\d+\s*;", line):
                errors.append({
                    "line": i,
                    "problem": "Invalid return statement",
                    "fix": "Use: return 0;"
                })
            continue

        if "=" in line:
            if not line.endswith(";"):
                errors.append({
                    "line": i,
                    "problem": "Missing semicolon",
                    "fix": "Add ; at the end of the assignment"
                })
                continue

            if not re.fullmatch(r"\w+\s*=\s*[\w\d\(\)\+\-\*/%\s]+;", line):
                errors.append({
                    "line": i,
                    "problem": "Invalid assignment",
                    "fix": "Use format like: sum = a + b;"
                })
            continue

        errors.append({
            "line": i,
            "problem": "Invalid statement",
            "fix": "Check spelling, brackets, and semicolon"
        })

    if expecting_open_brace:
        errors.append({
            "line": len(lines),
            "problem": "Missing opening brace after main function",
            "fix": "Add { after int main()"
        })

    if brace_stack:
        errors.append({
            "line": len(lines),
            "problem": "Missing closing brace",
            "fix": "Add } at the end of the block"
        })

    return errors