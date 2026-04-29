import re


def generate_parse_tree(code):
    tree = []
    tree.append("Program")

    lines = code.split("\n")

    for line in lines:
        line = line.strip()

        if line == "":
            continue

        if line.startswith("#include"):
            tree.append("├── Header")
            tree.append(f"│   └── {line}")

        elif line.startswith("int main"):
            tree.append("├── Main Function")
            tree.append("│   └── int main()")

        elif line.startswith("int "):
            tree.append("├── Declaration")
            tree.append(f"│   └── {line}")

        elif line.startswith("scanf"):
            tree.append("├── Input Statement")
            tree.append(f"│   └── {line}")

        elif line.startswith("printf"):
            tree.append("├── Output Statement")
            tree.append(f"│   └── {line}")

        elif line.startswith("if"):
            tree.append("├── If Statement")
            tree.append(f"│   └── Condition: {line}")

        elif line.startswith("for"):
            tree.append("├── For Loop")
            tree.append(f"│   └── {line}")

        elif line.startswith("while"):
            tree.append("├── While Loop")
            tree.append(f"│   └── {line}")

        elif "=" in line and line.endswith(";"):
            tree.append("├── Assignment")
            tree.append(f"│   └── {line}")

        elif line.startswith("return"):
            tree.append("├── Return Statement")
            tree.append(f"│   └── {line}")

    return tree