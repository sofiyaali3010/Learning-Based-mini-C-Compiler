from compiler.parser import check_syntax
from compiler.semantic import check_semantics
from compiler.executor import execute
from compiler.parse_tree import generate_parse_tree
from compiler.tac import generate_tac


def analyze(code, user_inputs=None):
    if user_inputs is None:
        user_inputs = {}

    if code.strip() == "":
        return {
            "errors": [{
                "line": 0,
                "problem": "No code provided",
                "fix": "Write some C code first"
            }],
            "output": [],
            "score": 0,
            "symbol_table": [],
            "trace": [],
            "parse_tree": [],
            "tac": []
        }

    syntax_errors = check_syntax(code)
    semantic_errors = check_semantics(code)

    all_errors = syntax_errors + semantic_errors

    if not all_errors:
        output, symbol_table, trace = execute(code, user_inputs)
        parse_tree = generate_parse_tree(code)
        tac = generate_tac(code)
    else:
        output = []
        symbol_table = []
        trace = []
        parse_tree = []
        tac = []

    score = max(0, 100 - len(all_errors) * 5)

    return {
        "errors": all_errors,
        "output": output,
        "score": score,
        "symbol_table": symbol_table,
        "trace": trace,
        "parse_tree": parse_tree,
        "tac": tac
    }