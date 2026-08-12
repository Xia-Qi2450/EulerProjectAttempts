"""
euler_problems
==============

A command-line Project Euler solver.

This package is the split-up version of the original single-file
EulerProblems.py. The EulerSolver class is now assembled from several
"mixin" files instead of living in one huge file:

    exceptions.py             - custom exception hierarchy
    data.py                   - large static data blobs (problem 8/11/13/18 inputs)
    helpers.py                - CLI/output helpers (spinners, progress bar, etc.)
    utils.py                  - reusable math helper functions
    easter_eggs.py            - hidden easter egg behavior
    problems_00_25.py         - problem0 .. problem25
    problems_26_50.py         - problem26 .. problem50
    problems_51_75.py         - problem51 .. problem75
    problems_76_100.py        - problem76 .. problem100
    solver.py                 - EulerSolver, combining all of the above via
                                 multiple inheritance ("mixins"), plus __init__/run()
    cli.py                    - argparse setup and the console entry point

Because this dependency check has to run before colorama/halo are known to
exist, it lives here in __init__.py: importing any submodule of this
package always runs __init__.py first, so the friendly error below fires
before Python has a chance to raise a raw ModuleNotFoundError.
"""

from .exceptions import (
    EulerProblemError,
    EulerProblemNotImplemented,
    EulerProblemExecutionError,
    RequiredModulesNotFound,
    ImportModulesFail,
)

try:
    import colorama
    from colorama import Fore, Style
    from halo import Halo
except ModuleNotFoundError as e:
    raise RequiredModulesNotFound(e.name) from e
except Exception as e:
    raise ImportModulesFail(e) from e

from .solver import EulerSolver

__all__ = [
    "EulerSolver",
    "EulerProblemError",
    "EulerProblemNotImplemented",
    "EulerProblemExecutionError",
    "RequiredModulesNotFound",
    "ImportModulesFail",
]
