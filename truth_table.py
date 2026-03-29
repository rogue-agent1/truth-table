#!/usr/bin/env python3
"""Boolean truth table generator and expression evaluator."""
import sys, re

OPS = {"and": lambda a, b: a and b, "or": lambda a, b: a or b,
       "xor": lambda a, b: a ^ b, "nand": lambda a, b: not (a and b),
       "nor": lambda a, b: not (a or b), "implies": lambda a, b: (not a) or b,
       "iff": lambda a, b: a == b}

def evaluate(expr, env):
    expr = expr.strip()
    if expr.startswith("not "):
        return not evaluate(expr[4:], env)
    if expr.startswith("(") and expr.endswith(")"):
        depth = 0
        for i, c in enumerate(expr):
            if c == "(": depth += 1
            elif c == ")": depth -= 1
            if depth == 0 and i == len(expr) - 1:
                return evaluate(expr[1:-1], env)
            elif depth == 0: break
    for op_name, op_fn in OPS.items():
        parts = expr.split(f" {op_name} ", 1)
        if len(parts) == 2:
            return op_fn(evaluate(parts[0], env), evaluate(parts[1], env))
    if expr in ("true", "1", "T"): return True
    if expr in ("false", "0", "F"): return False
    return env.get(expr, False)

def extract_vars(expr):
    tokens = re.findall(r'[a-zA-Z_]\w*', expr)
    ops = set(OPS.keys()) | {"not", "true", "false", "T", "F"}
    return sorted(set(t for t in tokens if t not in ops))

def truth_table(expr):
    variables = extract_vars(expr)
    rows = []
    for i in range(2 ** len(variables)):
        env = {}
        for j, v in enumerate(variables):
            env[v] = bool((i >> (len(variables) - 1 - j)) & 1)
        result = evaluate(expr, env)
        rows.append(({**env}, result))
    return variables, rows

def main():
    if len(sys.argv) < 2: print("Usage: truth_table.py <demo|test|expr>"); return
    if sys.argv[1] == "test":
        assert evaluate("true and false", {}) == False
        assert evaluate("true or false", {}) == True
        assert evaluate("not true", {}) == False
        assert evaluate("A and B", {"A": True, "B": True}) == True
        assert evaluate("A implies B", {"A": True, "B": False}) == False
        assert evaluate("A implies B", {"A": False, "B": False}) == True
        assert evaluate("A xor B", {"A": True, "B": False}) == True
        vars, rows = truth_table("A and B")
        assert len(vars) == 2 and len(rows) == 4
        assert rows[-1][1] == True  # T and T
        assert rows[0][1] == False  # F and F
        vars2, rows2 = truth_table("A or B")
        assert sum(1 for _, r in rows2 if r) == 3
        print("All tests passed!")
    else:
        expr = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else "A and B"
        variables, rows = truth_table(expr)
        header = " | ".join(variables + [expr])
        print(header); print("-" * len(header))
        for env, result in rows:
            vals = " | ".join("T" if env[v] else "F" for v in variables)
            print(f"{vals} | {'T' if result else 'F'}")

if __name__ == "__main__": main()
