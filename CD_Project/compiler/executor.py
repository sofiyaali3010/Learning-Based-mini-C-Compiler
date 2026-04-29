import re


# -------------------------
# SAFE VARIABLE SUBSTITUTE
# -------------------------

def substitute_variables(expr, variables):

    for var in variables:

        safe_var = re.escape(var)

        expr = re.sub(
            r"\b" + safe_var + r"\b",
            str(variables[var]),
            expr
        )

    return expr


# -------------------------
# EXPRESSION EVALUATION
# -------------------------

def evaluate_expression(expr, variables):

    expr = substitute_variables(expr, variables)

    try:
        return eval(expr)
    except:
        return 0


# -------------------------
# EXECUTOR
# -------------------------

def execute(code, user_inputs=None):

    if user_inputs is None:
        user_inputs = {}

    variables = {}
    output = []
    trace = []

    lines = code.split("\n")

    i = 0

    while i < len(lines):

        line = lines[i].strip()

        # -------------------------
        # IGNORE
        # -------------------------

        if (
            line.startswith("#include")
            or line.startswith("int main")
            or line == "{"
            or line == "}"
            or line == ""
        ):
            i += 1
            continue

        # -------------------------
        # VARIABLE DECLARATION
        # -------------------------

        if line.startswith("int"):

            decl = line.replace("int", "").replace(";", "")
            parts = decl.split(",")

            for part in parts:

                part = part.strip()

                if "=" in part:

                    var, expr = part.split("=")

                    value = evaluate_expression(expr.strip(), variables)

                    variables[var.strip()] = value
                    trace.append(f"{var.strip()} = {value}")

                else:

                    var = part.strip()

                    variables[var] = 0
                    trace.append(f"{var} initialized to 0")

            i += 1
            continue

        # -------------------------
        # SCANF
        # -------------------------

        if line.startswith("scanf"):

            vars_found = re.findall(r"&(\w+)", line)

            for var in vars_found:

                raw = user_inputs.get(var)

                if raw is None or raw == "":
                    value = 0
                else:
                    try:
                        value = int(raw)
                    except:
                        value = 0

                variables[var] = value
                trace.append(f"scanf → {var} = {value}")

            i += 1
            continue

        # -------------------------
        # FOR LOOP
        # -------------------------

        if line.startswith("for"):

            match = re.search(r"for\s*\((.*);(.*);(.*)\)", line)

            init = match.group(1).strip()
            condition = match.group(2).strip()
            increment = match.group(3).strip()

            # INIT
            var, expr = init.split("=")
            value = evaluate_expression(expr.strip(), variables)

            variables[var.strip()] = value
            trace.append(f"{var.strip()} = {value}")

            i += 1

            # COLLECT BODY
            body = []

            while i < len(lines):
                inner = lines[i].strip()
                if inner == "}":
                    break
                body.append(inner)
                i += 1

            # EXECUTE LOOP
            while True:

                cond_eval = substitute_variables(condition, variables)

                if not eval(cond_eval):
                    trace.append(f"Condition ({condition}) → FALSE")
                    break

                trace.append(f"Condition ({condition}) → TRUE")

                j = 0

                while j < len(body):

                    stmt = body[j]

                    # -------------------------
                    # IF INSIDE LOOP
                    # -------------------------

                    if stmt.startswith("if"):

                        cond = re.search(r"\((.*)\)", stmt).group(1)

                        cond_eval = substitute_variables(cond, variables)

                        result = eval(cond_eval)

                        trace.append(
                            f"Condition ({cond}) → {'TRUE' if result else 'FALSE'}"
                        )

                        j += 1

                        if result:

                            while j < len(body):

                                inner = body[j]

                                if inner == "}":
                                    break

                                if "=" in inner:

                                    var, expr = inner.replace(";", "").split("=")

                                    value = evaluate_expression(expr.strip(), variables)

                                    variables[var.strip()] = value

                                    trace.append(
                                        f"{var.strip()} = {expr.strip()} → {value}"
                                    )

                                j += 1

                        else:

                            while j < len(body):
                                if body[j] == "}":
                                    break
                                j += 1

                    # -------------------------
                    # PRINTF
                    # -------------------------

                    elif stmt.startswith("printf"):

                        vars_found = re.findall(r",\s*(\w+)", stmt)

                        for var in vars_found:

                            value = variables.get(var, 0)

                            output.append(str(value))

                            trace.append(f"printf → {value}")

                    # -------------------------
                    # ASSIGNMENT
                    # -------------------------

                    elif "=" in stmt:

                        var, expr = stmt.replace(";", "").split("=")

                        value = evaluate_expression(expr.strip(), variables)

                        variables[var.strip()] = value

                        trace.append(
                            f"{var.strip()} = {expr.strip()} → {value}"
                        )

                    j += 1

                # INCREMENT
                var, expr = increment.split("=")

                value = evaluate_expression(expr.strip(), variables)

                variables[var.strip()] = value

                trace.append(f"{var.strip()} = {value}")

            i += 1
            continue

        # -------------------------
        # IF (OUTSIDE LOOP)
        # -------------------------

        if line.startswith("if"):

            condition = re.search(r"\((.*)\)", line).group(1)

            cond_eval = substitute_variables(condition, variables)

            result = eval(cond_eval)

            trace.append(
                f"Condition ({condition}) → {'TRUE' if result else 'FALSE'}"
            )

            i += 1

            if result:

                while i < len(lines):

                    inner = lines[i].strip()

                    if inner == "}":
                        break

                    if "=" in inner:

                        var, expr = inner.replace(";", "").split("=")

                        value = evaluate_expression(expr.strip(), variables)

                        variables[var.strip()] = value

                        trace.append(
                            f"{var.strip()} = {expr.strip()} → {value}"
                        )

                    i += 1

            else:

                while i < len(lines):
                    if lines[i].strip() == "}":
                        break
                    i += 1

            i += 1
            continue

        # -------------------------
        # ASSIGNMENT
        # -------------------------

        if "=" in line and line.endswith(";"):

            var, expr = line.replace(";", "").split("=")

            value = evaluate_expression(expr.strip(), variables)

            variables[var.strip()] = value

            trace.append(
                f"{var.strip()} = {expr.strip()} → {value}"
            )

            i += 1
            continue

        # -------------------------
        # PRINTF
        # -------------------------

        if line.startswith("printf"):

            vars_found = re.findall(r",\s*(\w+)", line)

            for var in vars_found:

                value = variables.get(var, 0)

                output.append(str(value))

                trace.append(f"printf → {value}")

            i += 1
            continue

        i += 1

    # -------------------------
    # SYMBOL TABLE
    # -------------------------

    symbol_table = []

    for var in variables:

        symbol_table.append({
            "name": var,
            "type": "int",
            "value": variables[var]
        })

    return output, symbol_table, trace