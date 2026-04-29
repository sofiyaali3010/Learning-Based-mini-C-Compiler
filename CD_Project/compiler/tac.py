import re


def generate_tac(code):
    tac = []
    temp_count = 1
    label_count = 1

    def new_temp():
        nonlocal temp_count
        temp = f"t{temp_count}"
        temp_count += 1
        return temp

    def new_label():
        nonlocal label_count
        label = f"L{label_count}"
        label_count += 1
        return label

    lines = code.split("\n")

    for line in lines:
        line = line.strip()

        if line == "":
            continue

        if (
            line.startswith("#include")
            or line.startswith("int main")
            or line == "{"
            or line == "}"
            or line.startswith("return")
        ):
            continue

        if line.startswith("int "):
            declaration = line.replace("int", "", 1).replace(";", "")
            parts = declaration.split(",")

            for part in parts:
                part = part.strip()

                if "=" in part:
                    var, expr = part.split("=")
                    tac.append(f"{var.strip()} = {expr.strip()}")

            continue

        if line.startswith("scanf"):
            vars_found = re.findall(r"&(\w+)", line)

            for var in vars_found:
                tac.append(f"read {var}")

            continue

        if line.startswith("printf"):
            vars_found = re.findall(r",\s*(\w+)", line)

            for var in vars_found:
                tac.append(f"print {var}")

            continue

        if line.startswith("if"):
            condition = re.search(r"\((.*)\)", line).group(1)
            label = new_label()

            tac.append(f"if {condition} goto {label}")
            tac.append(f"{label}:")

            continue

        if line.startswith("for"):
            match = re.search(r"for\s*\((.*);(.*);(.*)\)", line)

            if match:
                init = match.group(1).strip()
                condition = match.group(2).strip()
                update = match.group(3).strip()

                start_label = new_label()
                end_label = new_label()

                tac.append(init)
                tac.append(f"{start_label}:")
                tac.append(f"if not {condition} goto {end_label}")
                tac.append(f"// loop body")
                tac.append(update)
                tac.append(f"goto {start_label}")
                tac.append(f"{end_label}:")

            continue

        if "=" in line and line.endswith(";"):
            left, expr = line.replace(";", "").split("=", 1)
            left = left.strip()
            expr = expr.strip()

            bracket_match = re.search(r"\((.*?)\)", expr)

            if bracket_match:
                inner = bracket_match.group(1)
                temp1 = new_temp()

                tac.append(f"{temp1} = {inner}")

                expr = expr.replace(f"({inner})", temp1)

                if any(op in expr for op in ["+", "-", "*", "/", "%"]):
                    temp2 = new_temp()
                    tac.append(f"{temp2} = {expr}")
                    tac.append(f"{left} = {temp2}")
                else:
                    tac.append(f"{left} = {expr}")

            else:
                operators = ["+", "-", "*", "/", "%"]

                found_operator = None

                for op in operators:
                    if op in expr:
                        found_operator = op
                        break

                if found_operator:
                    temp = new_temp()
                    tac.append(f"{temp} = {expr}")
                    tac.append(f"{left} = {temp}")
                else:
                    tac.append(f"{left} = {expr}")

    return tac