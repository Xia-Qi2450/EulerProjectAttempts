"""
EulerSolver: the combined Project Euler solver class.

This class is deliberately thin - almost all of its behavior comes from
the mixins below. Each mixin lives in its own file so no single file in
this package needs to hold the entire solver:

    HelpersMixin        -> helpers.py       (CLI/output helpers)
    UtilsMixin           -> utils.py         (math helper functions)
    EasterEggsMixin       -> easter_eggs.py   (hidden easter eggs; inherits HelpersMixin)
    Problems00To25Mixin   -> problems_00_25.py (inherits UtilsMixin, EasterEggsMixin)
    Problems26To50Mixin   -> problems_26_50.py (inherits UtilsMixin, EasterEggsMixin)
    Problems51To75Mixin   -> problems_51_75.py (inherits UtilsMixin, HelpersMixin)

Each mixin genuinely inherits the other mixins whose methods it calls
(rather than just assuming they'll be mixed in later), so only the three
problem mixins need to be listed here - the rest come along transitively.
This is also what lets a type checker like Pylance/Pyright correctly
resolve calls like self.header(...) inside a problem method: it's now
real inheritance, not an assumption baked in only at combination time.
"""

import os
import time
import itertools
import shutil

from colorama import Fore, Style

from . import data
from .exceptions import EulerProblemNotImplemented, EulerProblemExecutionError
from .problems_00_25 import Problems00To25
from .problems_26_50 import Problems26To50
from .problems_51_75 import Problems51To75


class EulerSolver(
    Problems00To25,
    Problems26To50,
    Problems51To75,
):
    """
    Solve and manage Project Euler problems.

    The solver provides implementations of the first 100 Project Euler
    problems together with utilities for execution, benchmarking,
    progress tracking, and command-line interaction.

    Attributes
    ----------
    VERSION : str
        Current version of the solver.
    GOAL : int
        Target number of Project Euler problems.
    EASTER_EGGS : bool
        Whether random easter eggs are enabled.
    FORCED_EASTER_EGGS : bool
        Force easter eggs to appear regardless of probability.
    problem_times : dict[int, float]
        Runtime statistics collected for executed problems.
    """

    def __init__(self, easter_eggs=True, forced_easter_eggs=False) -> None:
        import colorama
        colorama.init(autoreset=True)
        self.VERSION = "0.6"
        self.GOAL = "100"
        self.EASTER_EGGS: bool = easter_eggs
        self.FORCED_EASTER_EGGS: bool = forced_easter_eggs
        self.terminal_width: int = shutil.get_terminal_size(fallback=(100, 24)).columns
        self.problem_times: dict[int, float] = {}
        self.current_file: str = os.path.realpath(__file__)
        self.problem8_number = data.PROBLEM8_NUMBER
        self.problem11_grid = data.PROBLEM11_GRID
        self.problem13_numbers = data.PROBLEM13_NUMBERS
        self.problem18triangle = data.PROBLEM18_TRIANGLE
        self.CARD_VALUES = dict(data.CARD_VALUES)

    def __str__(self):
        return (
            f"EulerSolver v{self.VERSION} "
            f"({len(self.list_problems(False)) - 1}/{self.GOAL} solved)"
        )

    # ==========================================================
    # Runner
    # ==========================================================

    def run(self, problems=None):
        start_time = None
        if problems is None:
            start_time = time.perf_counter()
            problems = sorted(
                int(name[7:])
                for name in dir(self)
                if name.startswith("problem") and name[7:].isdigit()
            )
        for number in problems:
            method = getattr(self, f"problem{number}", None)

            if callable(method):
                try:
                    problem_start = time.perf_counter()
                    method()
                    elapsed = time.perf_counter() - problem_start
                    self.problem_times[number] = elapsed
                except KeyboardInterrupt:
                    print(f"{Style.DIM}{Fore.YELLOW}\nProgram interrupted by user{Fore.RESET}{Style.NORMAL}")
                    return
                except ZeroDivisionError as e:
                    raise EulerProblemExecutionError(
                        number,
                        ZeroDivisionError(
                            "Attempted calculation contains division by 0. Calculation fails."
                            "Yes, this is a nod towards the TI-84 Plus CE error when dividing by zero."
                            )
                    ) from e
                except Exception as e:
                    print(f"{Fore.RED}Problem {number} ran into an error during execution.{Fore.RESET}")
                    raise EulerProblemExecutionError(number, e) from e
            else:
                print(f"{Fore.RED}Problem {number} has not been implemented.{Fore.RESET}")
                raise EulerProblemNotImplemented(number)
        if start_time is not None: 
            runtime = time.perf_counter() - start_time
            average = runtime / len(problems)

            print(Fore.CYAN + "=" * self.terminal_width)
            print(Fore.CYAN + f"Total Runtime   : {runtime:.4f}s")
            print(Fore.CYAN + f"Average/problem : {average:.4f}s")

            print(Fore.CYAN + "-" * self.terminal_width)
            print(f"{Style.BRIGHT}Top 3 Slowest Problems{Style.NORMAL}")

            slowest = sorted(
                self.problem_times.items(),
                key=lambda item: item[1],
                reverse=True
            )[:3]

            print(f"{'Problem':<8}{'Runtime':>12}")
            for problem, elapsed in slowest:
                print(f"{problem:<8}{elapsed:>11.4f}s")
