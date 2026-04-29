import re


def remove_strings(line):
    return re.sub(r'"[^"]*"', "", line)


def check_semantics(code):
    errors = []
    declared_vars = set()

    keywords = {
        "int", "if", "for", "while", "return", "main",
        "printf", "scanf"
    }

    lines = code.split("\n")

    for i, raw_line in enumerate(lines, start=1):
        line = raw_line.strip()

        if (
            line == ""
            or line.startswith("#include")
            or line.startswith("int main")
            or line == "{"
            or line == "}"
        ):
            continue

        if line.startswith("int"):
            declaration = line.replace("int", "", 1).replace(";", "")
            parts = declaration.split(",")

            for part in parts:
                part = part.strip()

                if "=" in part:
                    var = part.split("=")[0].strip()
                else:
                    var = part.strip()

                if var:
                    declared_vars.add(var)

            continue

        if line.startswith("scanf"):
            vars_used = re.findall(r"&(\w+)", line)

            for var in vars_used:
                if var not in declared_vars:
                    errors.append({
                        "line": i,
                        "problem": f"Variable '{var}' used but not declared",
                        "fix": f"Declare it first like: int {var};"
                    })

            continue

        clean_line = remove_strings(line)

        tokens = re.findall(r"\b[a-zA-Z_]\w*\b", clean_line)

        for token in tokens:
            if token in keywords:
                continue

            if token in declared_vars:
                continue

            errors.append({
                "line": i,
                "problem": f"Variable '{token}' used but not declared",
                "fix": f"Declare it first like: int {token};"
            })

    return errors