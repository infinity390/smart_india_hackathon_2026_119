# Smart India Hackathon 2026 Problem Statement 119
Indigenous GPU-Accelerated Optimization Solver

## Running the program
Run the files, algorithm_A.py and algorithm_B.py directly

## Algorithm A (SLOWER)
Exact vertex enumeration using Fraction arithmetic & Gaussian elimination.
<br>
Solution of 1st problem
```
Optimal point: (Fraction(24, 5), Fraction(0, 1), Fraction(12, 5), Fraction(4, 1))
Optimal value: 288/5
```

## Algorithm B (FASTER)
Vertex-neighbor walking using exact Fraction arithmetic, nullspace directions, and ray-tracing.
<br>
Solution of 2nd problem
```
Point: (Fraction(0, 1), Fraction(0, 1), Fraction(0, 1), Fraction(0, 1), Fraction(0, 1), Fraction(0, 1), Fraction(0, 1)) Value: 0
Point: (Fraction(0, 1), Fraction(0, 1), Fraction(0, 1), Fraction(0, 1), Fraction(0, 1), Fraction(0, 1), Fraction(15, 1)) Value: 150
Point: (Fraction(0, 1), Fraction(0, 1), Fraction(0, 1), Fraction(0, 1), Fraction(15, 2), Fraction(0, 1), Fraction(15, 1)) Value: 210
Point: (Fraction(0, 1), Fraction(0, 1), Fraction(10, 1), Fraction(0, 1), Fraction(25, 2), Fraction(0, 1), Fraction(5, 1)) Value: 240
Point: (Fraction(0, 1), Fraction(0, 1), Fraction(10, 1), Fraction(0, 1), Fraction(68, 5), Fraction(22, 5), Fraction(14, 5)) Value: 1244/5

Optimal point: (Fraction(0, 1), Fraction(0, 1), Fraction(10, 1), Fraction(0, 1), Fraction(68, 5), Fraction(22, 5), Fraction(14, 5))
Optimal value: 1244/5
```
