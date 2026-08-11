"""
Command-line interface for the Project Euler solver.

Kept separate from solver.py so the argparse wiring doesn't clutter the
solver logic, and so tests can import build_parser()/main() without
triggering argument parsing as a side effect of import.
"""

import argparse
import sys

from colorama import Fore

from .solver import EulerSolver


def build_parser(solver: EulerSolver) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="EulerProblems.py",
        description=(
            f"Euler Project Attempts {Fore.CYAN}v{solver.VERSION}{Fore.RESET} - "
            f"A Script with the first {solver.GOAL} Project Euler questions solved using Python."
        ),
        epilog=f"Currently having {len(solver.list_problems(False)) - 1}/{solver.GOAL} problems solved!",
    )
    if sys.version_info >= (3, 14):
        parser.suggest_on_error = True
    parser.add_argument(
        "problems",
        nargs="*",
        type=str,
        metavar="N",
        help="Problem numbers to run",
    )
    parser.add_argument(
        "-a",
        "--all",
        action="store_true",
        help="Run every implemented problem.",
    )
    parser.add_argument(
        "-l",
        "--list",
        action="store_true",
        help="List all implemented problems.",
    )
    parser.add_argument(
        "-n",
        "--no-easter-eggs",
        action="store_true",
        help="Disables easter eggs from happening for clean output.",
    )
    parser.add_argument(
        "--force-easter-eggs",
        action="store_true",
        help=argparse.SUPPRESS,
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=(
            f"%(prog)s {Fore.CYAN}v{solver.VERSION}{Fore.RESET}"
            f" - Progress: {len(solver.list_problems(False)) - 1}/{solver.GOAL} solved"
        ),
    )
    return parser


def main() -> None:
    solver = EulerSolver()
    parser = build_parser(solver)
    args = parser.parse_args()

    if args.no_easter_eggs and args.force_easter_eggs:
        parser.error(
            "--force-easter-eggs cannot be used together with --no-easter-eggs."
        )

    solver.EASTER_EGGS = not args.no_easter_eggs
    solver.FORCED_EASTER_EGGS = args.force_easter_eggs

    if args.list:
        solver.list_problems()
    elif args.all:
        solver.run()
    elif args.problems:
        solver.run(args.problems)
    else:
        # No arguments defaults to help
        parser.print_help()


if __name__ == "__main__":
    main()
