import re

def tokenize(code):
    tokens = re.findall(r"[A-Za-z_]\w*|\d+(\.\d+)?|==|<=|>=|!=|[+\-*/=;{}()<>]", code)
    return tokens