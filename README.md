# Project Euler Solutions in Python

A collection of my solutions to the first **100 Project Euler** problems, written in Python.

The goal of this project isn't just to get the correct answers—it's also an opportunity to practice writing clean, reusable, and reasonably efficient code while learning new algorithms and mathematical techniques.

**Current Progress:** **20 / 100** ✅

```
██████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  20%
```

---

## Features

- Solutions organized inside a single `EulerSolver` class
- Reusable helper functions for common mathematical operations
- Automatic discovery of implemented problems
- Command-line interface powered by `argparse`
- Run individual Project Euler problems
- List all implemented problems
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
| 16 | Power Digit Sum | ✅ |
| 17 | Number Letter Counts | ✅ |
| 18 | Maximum Path Sum I | ✅ |
| 19 | Counting Sundays | ✅ |
| 20 | Factorial Digit Sum | ✅ |

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

Run every implemented Project Euler solution:

```bash
python EulerProblems.py
```

or explicitly:

```bash
python EulerProblems.py --all
```

### Run specific problems

Execute one or more individual problems by specifying their numbers.

```bash
python EulerProblems.py 1
```

```bash
python EulerProblems.py 1 5 10 15
```

### List implemented problems

View every currently implemented Project Euler problem.

```bash
python EulerProblems.py --list
```

or

```bash
python EulerProblems.py -l
```

Example output:

```text
Implemented Problems

  0 - Find the sum of all odd perfect squares up to 756000
  1 - Find the sum of all multiples of 3 or 5 below 1000
  2 - Find the sum of all even Fibonacci numbers below 4 million
  ...
 15 - Find the number of lattice paths through a 20×20 grid
```

---

## Helper Functions

Reusable algorithms currently include:

- Perfect square generation
- Fibonacci sequence generator
- Largest prime factor
- Palindrome checker
- Largest palindrome product
- Sum square difference
- Sieve of Eratosthenes
- Adjacent digit product
- Pythagorean triplet generation
- Prime summation
- Grid product search
- Divisor counting
- Collatz sequence solver
- Lattice path counting
- Integer-to-English word conversion
- Maximum triangle path solver
- Leap year calculation
- Sunday counting algorithm

---

## Goal

Finish all **100** Project Euler problems while continually improving:

- Python knowledge
- Algorithm design
- Mathematical problem solving
- Runtime efficiency
- Code readability

---

## Future Ideas

- [x] Command-line interface
- [x] Run individual problems
- [x] List implemented problems
- [ ] Benchmark mode
- [ ] Automatic answer verification against Project Euler answers
- [ ] Export benchmark results to CSV
- [ ] Unit tests
- [ ] More optimized algorithms for later problems
- [ ] Progress statistics
- [ ] Separate helper functions into their own module

---

## License

This project is released under the MIT License.