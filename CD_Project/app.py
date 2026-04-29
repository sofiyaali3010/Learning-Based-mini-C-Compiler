from flask import Flask, render_template, request
from compiler.analyzer import analyze
import re

app = Flask(__name__)


def extract_inputs(code):
    variables = []

    for line in code.split("\n"):
        line = line.strip()

        if line.startswith("scanf"):
            found = re.findall(r"&(\w+)", line)

            for var in found:
                if var not in variables:
                    variables.append(var)

    return variables


@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    code = ""
    input_vars = []
    user_inputs = {}

    if request.method == "POST":
        code = request.form.get("code", "")
        input_vars = extract_inputs(code)

        for var in input_vars:
            user_inputs[var] = request.form.get(var, "")

        result = analyze(code, user_inputs)

    return render_template(
        "index.html",
        result=result,
        code=code,
        input_vars=input_vars
    )


if __name__ == "__main__":
    print("Server running...")
    app.run(debug=True)