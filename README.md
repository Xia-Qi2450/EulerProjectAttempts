# Project Euler Solutions in Python

[![GitHub release](https://img.shields.io/github/v/release/Xia-Qi2450/EulerProjectAttempts)](https://github.com/Xia-Qi2450/EulerProjectAttempts/releases)
[![License](https://img.shields.io/github/license/Xia-Qi2450/EulerProjectAttempts)](LICENSE.txt)
[![Python](https://img.shields.io/badge/python-3.14-blue.svg?logo=python)](https://www.python.org/downloads/release/python-3147/)
[![Release](https://github.com/Xia-Qi2450/EulerProjectAttempts/actions/workflows/release.yaml/badge.svg)](https://github.com/Xia-Qi2450/EulerProjectAttempts/actions/workflows/release.yaml)
[![Python Backwards Compatibility](https://github.com/Xia-Qi2450/EulerProjectAttempts/actions/workflows/compatibility.yaml/badge.svg)](https://github.com/Xia-Qi2450/EulerProjectAttempts/actions/workflows/compatibility.yaml)

A collection of my solutions to the first **100 Project Euler** problems, written in Python.
Now I am deciding to do another 100! I need something to keep me from playing games.

The goal of this project isn't just to get the correct answers—it's also an opportunity to practice writing clean, reusable, and reasonably efficient code while learning new algorithms and mathematical techniques.

**Current Progress:** **100/200** ✅

```text
█████████████████████████░░░░░░░░░░░░░░░░░░░░░░░░░  50%
```

> **Note**
>
> This project may occasionally surprise you. If you prefer perfectly reproducible output, use `--no-easter-eggs`.

---

## Features

- Solutions organized inside a single `EulerSolver` class
- Reusable helper functions for common mathematical operations
- Automatic discovery of implemented problems
- Command-line interface powered by `argparse`
- Run individual Project Euler problems
- List all implemented problems
- Animated loading spinners using [**Halo**](https://github.com/manrajgrover/halo)
- Colored terminal output using [**Colorama**](https://github.com/tartley/colorama)
- Execution time displayed for computationally intensive problems
- Clean and readable code with docstrings
- Modular package structure (`euler_problems/`) split by responsibility for easier maintenance

---

## Currently Solved

| Problem | Description | Status |
| ---------: | ------------- | :------: |
| 0 | Sum of odd perfect squares up to 756000 | ✅ |
| 1 | Multiples of 3 or 5 | ✅ |
| 2 | Even Fibonacci Numbers | ✅ |
| 3 | Largest Prime Factor | ✅ |
| 4 | Largest Palindrome Product | ✅ |
| *5* | ✦ Smallest Multiple | ✅ |
| 6 | Sum Square Difference | ✅ |

...

Check [PROBLEMS](PROBLEMS.md) for the full completed list

✦ Some solved problems contain optional surprises.
> Note: Problem 0 is the starting challenge for account creation
---

## Project Structure

```text
EulerProblems.py         (Thin entry point - run this, same CLI as always)
ci_smoke.py              (The CI test script to make sure everyting works)
requirements.txt         (The requirements)
euler_problems/          (Package containing all solver logic)
    __init__.py             (Dependency check + package exports)
    exceptions.py           (Custom exception hierarchy)
    data.py                 (Large static data blobs - problems 8, 11, 13, 18, etc.)
    helpers.py              (CLI/output helpers - spinners, progress bar, etc.)
    utils.py                (Reusable math helper functions)
    easter_eggs.py          (Hidden easter egg behavior)
    problems_00_25.py       (Solutions: problem0 - problem25)
    problems_26_50.py       (Solutions: problem26 - problem50)
    problems_51_75.py       (Solutions: problem51 - problem75)
    problems_76_100.py      (Solutions: problem76 - problem100)
    solver.py               (EulerSolver class, combining everything above)
    cli.py                  (argparse setup + main entry point)
0022_names.txt           (The names for Problem 22)
0042_words.txt           (The words for Problem 42)
0054_poker.txt           (The poker hands for Problem 54)
0059_cipher.txt          (The encrypted message for Problem 59)
0067_triangle.txt        (The triangle for Problem 67)
0079_keylog.txt          (The keyslogs for Problem 79)
0081_matrix.txt          (The matrix for Problems 81-83)
0089_roman.txt           (The Roman numerals for Problem 89)
0096_sudoku.txt          (The Sudoku games for Problem 96)
0098_words.txt           (The words for Problem 98)
0099_base_exp.txt        (The exponents for Problem 99)
README.md                (This file)
LICENSE.txt              (The MIT License)
```

This project used to live entirely inside one ~3,100-line file. It's now split
across the `euler_problems/` package, with each piece combined into a single
`EulerSolver` class via mixins:

- Utility/helper methods → `helpers.py`, `utils.py`
- Hidden easter eggs → `easter_eggs.py`
- Individual Project Euler solutions → `problems_00_25.py`, `problems_26_50.py`, `problems_51_75.py`, `problems_76_100.py`
- Runner / CLI → `solver.py`, `cli.py`

Nothing changes about how you run it - `python EulerProblems.py ...` still works
exactly like before; it's now just a thin entry point into the package.

---

## Requirements

Python 3.10+ is supported, with Python 3.14+ recommended for the best experience.

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Running

Prints out a help message:

```bash
python EulerProblems.py
```

Run every implemented Project Euler solution:

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
 XX - Latest implemented problem
```

### Debug options

List all debug options currently implemented, select the option by inputing the corresponding number.

```bash
python EulerProblems.py debug
```

---

## Helper Functions

Many Project Euler problems reuse common algorithms. Instead of rewriting code, helper methods are shared across multiple solutions.

Current helper functionality includes:

- Prime number generation
- Sieve of Eratosthenes
- Prime factorization
- Fibonacci generation
- Palindrome checking
- Divisor counting
- Dynamic programming
- Mathematical utilities
- And more as new problems require them.

---

## Goal

Finish all **100** Project Euler problems while continually improving:

- Python knowledge
- Algorithm design
- Mathematical problem solving
- Runtime efficiency
- Code readability

> This is currently complete. This repository is still being maintained and adding new problems. Check [PROBLEMS](PROBLEMS.md) for a list of all problems that has been completed

---

## Future Ideas

- [x] Command-line interface
- [x] Run individual problems
- [x] List implemented problems
- [x] Debug options
- [ ] Benchmark mode
- [ ] Automatic answer verification against Project Euler answers
- [ ] Export benchmark results to CSV
- [ ] Unit tests
- [ ] More optimized algorithms for later problems
- [x] Progress statistics
- [x] Separate helper functions into their own module
- [x] Split codebase into multiple modules

---

## Why this project?

Project Euler offers problems that combine mathematics with programming. Rather than simply obtaining the correct answer, this project focuses on writing solutions that are:

- Readable
- Reusable
- Efficient
- Well documented
- Easy to benchmark and improve over time

Every solved problem is another opportunity to learn something new.

---

## ✦ Easter Eggs

This project contains a handful of hidden easter eggs for those who are lucky enough to find them.

By default, easter eggs have a small chance of appearing during the execution of certain Project Euler problems.

If you would like deterministic output for benchmarking, screenshots, or automated testing, you can disable them:

```bash
python EulerProblems.py --no-easter-eggs
```

> *Hint:* At least one easter egg is hidden in **Problem 39**...

---

## License

This project is released under the MIT License.
