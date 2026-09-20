from itertools import combinations
from fractions import Fraction

def solve_system(equations):
    n = len(equations)
    if any(len(row) != n + 1 for row in equations):
        return None
    a = [[Fraction(x) for x in row] for row in equations]
    for col in range(n):
        pivot = None
        for row in range(col, n):
            if a[row][col] != 0:
                pivot = row
                break
        if pivot is None:
            return None
        if pivot != col:
            a[col], a[pivot] = a[pivot], a[col]
        for row in range(col + 1, n):
            if a[row][col] == 0:
                continue
            factor = a[row][col] / a[col][col]
            for j in range(col, n + 1):
                a[row][j] -= factor * a[col][j]
    x = [Fraction(0)] * n
    for row in range(n - 1, -1, -1):
        if a[row][row] == 0:
            return None
        s = sum(a[row][j] * x[j] for j in range(row + 1, n))
        x[row] = (a[row][n] - s) / a[row][row]
    return tuple(x)

def feasible(point, constraints):
    for coefficients, relation, b in constraints:
        lhs = sum(a * x for a, x in zip(coefficients, point))
        if relation == "<=" and lhs > b:
            return False
        if relation == ">=" and lhs < b:
            return False
        if relation == "=" and lhs != b:
            return False
    return True

def objective_value(objective, point):
    return sum(a * x for a, x in zip(objective, point))

def solve_lp(objective, constraints, bounds=None, maximize=True):
    n = len(objective)
    objective = [Fraction(x) for x in objective]
    normalized_constraints = []
    for coefficients, relation, b in constraints:
        coefficients = tuple(Fraction(x) for x in coefficients)
        normalized_constraints.append((coefficients, relation, Fraction(b)))
    boundary = list(normalized_constraints)
    if bounds is not None:
        for i, bound in enumerate(bounds):
            lower, upper = bound
            if lower is not None:
                coefficients = [Fraction(0)] * n
                coefficients[i] = Fraction(1)
                boundary.append((tuple(coefficients), ">=", Fraction(lower)))
            if upper is not None:
                coefficients = [Fraction(0)] * n
                coefficients[i] = Fraction(1)
                boundary.append((tuple(coefficients), "<=", Fraction(upper)))
    else:
        for i in range(n):
            coefficients = [Fraction(0)] * n
            coefficients[i] = Fraction(1)
            boundary.append((tuple(coefficients), ">=", Fraction(0)))
    best_point = None
    best_value = None
    for selected in combinations(boundary, n):
        equations = []
        valid = True
        for coefficients, relation, b in selected:
            if relation in ("=", "<=", ">="):
                equations.append(list(coefficients) + [b])
        point = solve_system(equations)
        if point is None:
            continue
        if not feasible(point, normalized_constraints):
            continue
        if bounds is not None:
            valid = True
            for x, (lower, upper) in zip(point, bounds):
                if lower is not None and x < lower:
                    valid = False
                    break
                if upper is not None and x > upper:
                    valid = False
                    break
            if not valid:
                continue
        current_value = objective_value(objective, point)
        if not maximize:
            current_value = -current_value
        if best_value is None or current_value > best_value:
            best_value = current_value
            best_point = point
    if best_point is None:
        return None, None
    actual_value = objective_value(objective, best_point)
    return best_point, actual_value

objective = [5, 3, 4, 6]
constraints = [
    ([2, 1, 1, 2], "<=", 20),
    ([1, 3, 2, 1], "<=", 18),
    ([1, 2, 3, 1], "<=", 16),
    ([2, 1, 1, 3], "<=", 24)
]
bounds = [
    (Fraction(0), None),
    (Fraction(0), None),
    (Fraction(0), None),
    (Fraction(0), None)
]

point, optimum = solve_lp(objective, constraints, bounds=bounds, maximize=True)
print("Optimal point:", point)
print("Optimal value:", optimum)
