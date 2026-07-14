# Project Euler Solutions in Python

A collection of my solutions to the first **100 Project Euler** problems, written in Python.

The goal of this project isn't just to get the correct answers—it's also an opportunity to practice writing clean, reusable, and reasonably efficient code while learning new algorithms and mathematical techniques.

**Current Progress:** **15 / 100** ✅

---

## Features

- Solutions organized inside a single `EulerSolver` class
- Reusable helper functions for common mathematical operations
- Animated loading spinners using **Halo**
- Colored terminal output using **Colorama**
- Execution time displayed for computationally intensive problems
- Clean and readable code with docstrings

---

## Currently Solved

| Problem | Description | Status |
|---------:|-------------|:------:|
| 0 | Sum of odd perfect squares up to 756000 *(starting challenge for account creation)* | ✅ |
| 1 | Multiples of 3 or 5 | ✅ |
| 2 | Even Fibonacci Numbers | ✅ |
| 3 | Largest Prime Factor | ✅ |
| 4 | Largest Palindrome Product | ✅ |
| 5 | Smallest Multiple | ✅ |
| 6 | Sum Square Difference | ✅ |
| 7 | 10,001st Prime | ✅ |
| 8 | Largest Product in a Series | ✅ |
| 9 | Special Pythagorean Triplet | ✅ |
| 10 | Summation of Primes | ✅ |
| 11 | Largest Product in a Grid | ✅ |
| 12 | Highly Divisible Triangular Number | ✅ |
| 13 | Large Sum | ✅ |
| 14 | Longest Collatz Sequence | ✅ |
| 15 | Lattice Paths | ✅ |

---

## Project Structure

```
EulerProblems.py
```

Everything currently lives inside one file:

- Utility/helper methods
- Individual Project Euler solutions
- Runner

As the project grows, it may eventually be split into multiple modules.

---

## Requirements

Python **3.11+** is recommended.

Install dependencies:

```bash
pip install colorama halo
```

---

## Running

Simply execute:

```bash
python EulerProblems.py
```

Each solved problem will execute sequentially.

Example output:

```
Euler's problem 1: Find the sum of all multiples of 3 or 5 below 1000

✔ DONE! (0.00002s)

Sum of multiples of 3 or 5 below 1000:
233168
```

---

## Helper Functions

Some reusable utilities currently included:

- Perfect square generation
- Fibonacci sequence generator
- Largest prime factor
- Palindrome checker
- Largest palindrome product
- Sum square difference
- Sieve of Eratosthenes

These are shared across multiple Project Euler problems whenever possible.

---

## Goal

Finish all **100** Project Euler problems while continually improving:

- Python knowledge
- Algorithm design
- Mathematical problem solving
- Runtime efficiency
- Code readability

Current Progress:

```
███░░░░░░░░░░░░░░░░░ 15%
```

---

## Future Ideas

- [ ] Command-line argument to run a single problem
- [ ] Benchmark mode
- [ ] Automatic answer verification
- [ ] Unit tests
- [ ] More optimized algorithms
- [ ] Progress statistics
- [ ] Save benchmark history
- [ ] Separate helper functions into their own module

---

## License

This project is released under the MIT License.