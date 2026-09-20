from itertools import combinations
from fractions import Fraction
def rank(matrix):
    matrix = [
        [Fraction(x) for x in row]
        for row in matrix
    ]

    if not matrix:
        return 0

    rows = len(matrix)
    cols = len(matrix[0])

    r = 0

    for col in range(cols):
        pivot = None

        for row in range(r, rows):
            if matrix[row][col] != 0:
                pivot = row
                break

        if pivot is None:
            continue

        matrix[r], matrix[pivot] = matrix[pivot], matrix[r]

        for row in range(r + 1, rows):
            if matrix[row][col] == 0:
                continue

            factor = matrix[row][col] / matrix[r][col]

            for j in range(col, cols):
                matrix[row][j] -= factor * matrix[r][j]

        r += 1

        if r == rows:
            break

    return r


def nullspace(matrix):
    matrix = [
        [Fraction(x) for x in row]
        for row in matrix
    ]

    if not matrix:
        return []

    rows = len(matrix)
    cols = len(matrix[0])

    r = 0
    pivots = []

    for col in range(cols):
        pivot = None

        for row in range(r, rows):
            if matrix[row][col] != 0:
                pivot = row
                break

        if pivot is None:
            continue

        matrix[r], matrix[pivot] = matrix[pivot], matrix[r]

        divisor = matrix[r][col]

        for j in range(col, cols):
            matrix[r][j] /= divisor

        for row in range(rows):
            if row == r:
                continue

            if matrix[row][col] == 0:
                continue

            factor = matrix[row][col]

            for j in range(col, cols):
                matrix[row][j] -= factor * matrix[r][j]

        pivots.append(col)
        r += 1

    free_columns = [
        col
        for col in range(cols)
        if col not in pivots
    ]

    basis = []

    for free in free_columns:
        vector = [Fraction(0)] * cols
        vector[free] = Fraction(1)

        for row, pivot in enumerate(pivots):
            vector[pivot] = -matrix[row][free]

        basis.append(vector)

    return basis


def active_constraints(point, constraints):
    active = []

    for i, (coefficients, relation, b) in enumerate(constraints):

        lhs = sum(
            Fraction(a) * x
            for a, x in zip(coefficients, point)
        )

        b = Fraction(b)

        if relation == "=":
            if lhs == b:
                active.append(i)

        elif relation == "<=":
            if lhs == b:
                active.append(i)

        elif relation == ">=":
            if lhs == b:
                active.append(i)

    return active


def feasible(point, constraints):
    for coefficients, relation, b in constraints:

        lhs = sum(
            Fraction(a) * x
            for a, x in zip(coefficients, point)
        )

        b = Fraction(b)

        if relation == "<=" and lhs > b:
            return False

        if relation == ">=" and lhs < b:
            return False

        if relation == "=" and lhs != b:
            return False

    return True


def neighbors(point, constraints):
    point = tuple(Fraction(x) for x in point)
    n = len(point)

    result = set()

    for selected in combinations(range(len(constraints)), n - 1):

        A = [
            constraints[i][0]
            for i in selected
        ]

        if rank(A) != n - 1:
            continue

        for i in selected:
            coefficients, relation, b = constraints[i]

            ax = sum(
                Fraction(a) * x
                for a, x in zip(coefficients, point)
            )

            if ax != Fraction(b):
                break
        else:
            direction = nullspace(A)[0]

            for sign in (1, -1):

                d = tuple(sign * x for x in direction)

                t = None

                for coefficients, relation, b in constraints:

                    ax = sum(
                        Fraction(a) * x
                        for a, x in zip(coefficients, point)
                    )

                    ad = sum(
                        Fraction(a) * dx
                        for a, dx in zip(coefficients, d)
                    )

                    if relation == "<=" and ad > 0:
                        value = (Fraction(b) - ax) / ad

                    elif relation == ">=" and ad < 0:
                        value = (Fraction(b) - ax) / ad

                    else:
                        continue

                    if value > 0 and (t is None or value < t):
                        t = value

                if t is None:
                    continue

                neighbor = tuple(
                    x + t * dx
                    for x, dx in zip(point, d)
                )

                if feasible(neighbor, constraints):
                    result.add(neighbor)

    return list(result)


def objective_value(objective, point):
    return sum(
        Fraction(a) * x
        for a, x in zip(objective, point)
    )


def solve_lp(objective, constraints, start):
    point = tuple(
        Fraction(x)
        for x in start
    )

    if not feasible(point, constraints):
        raise ValueError(
            "Starting point is not feasible"
        )

    visited = set()

    while True:

        if point in visited:
            raise RuntimeError(
                "Cycle detected"
            )

        visited.add(point)

        current_value = objective_value(
            objective,
            point
        )

        print(
            "Point:",
            point,
            "Value:",
            current_value
        )

        adjacent = neighbors(
            point,
            constraints
        )

        if not adjacent:
            return point, current_value

        best_point = point
        best_value = current_value

        for candidate in adjacent:

            candidate_value = objective_value(
                objective,
                candidate
            )

            if candidate_value > best_value:
                best_point = candidate
                best_value = candidate_value

        if best_point == point:
            return point, current_value

        point = best_point


constraints = [
    ([2,1,1,0,2,0,1], "<=", 40),
    ([1,2,0,1,1,2,0], "<=", 35),
    ([1,0,2,1,0,1,2], "<=", 30),
    ([0,1,1,2,1,0,1], "<=", 32),
    ([2,0,1,0,1,1,0], "<=", 28),
    ([0,2,0,1,2,0,1], "<=", 30),
]
constraints += [
    ([1 if i == j else 0 for i in range(7)], ">=", 0) for j in range(7)
]
objective = [7,4,9,6,8,5,10]
point, optimum = solve_lp(objective, constraints, start=(0,) * 7)
print("\nOptimal point:", point)
print("Optimal value:", optimum)
