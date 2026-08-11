import time

from euler_problems.solver import EulerSolver


# Problems known to be too slow for CI.
IGNORED_PROBLEMS = {
    58,
    60,
    70
}


def main():
    # Disable all easter eggs for CI smoke test.
    solver = EulerSolver()
    solver.EASTER_EGGS = False
    solver.FORCED_EASTER_EGGS = False
    solver.SPINNERS = False

    problems = sorted(
        int(name[7:])
        for name in dir(solver)
        if name.startswith("problem") and name[7:].isdigit()
    )

    problems = [
        problem
        for problem in problems
        if problem not in IGNORED_PROBLEMS
    ]

    print(f"Running smoke test for {len(problems)} problems...")
    print(f"Ignoring slow problems: {sorted(IGNORED_PROBLEMS)}")
    print("=" * 80)
    start_time = time.perf_counter()
    failures = []

    for number in problems:
        method = getattr(solver, f"problem{number}")

        start = time.perf_counter()

        try:
            method()
        except Exception as error:
            elapsed = time.perf_counter() - start

            print(
                f"❌ Problem {number} FAILED "
                f"after {elapsed:.4f}s"
            )
            print(f"   {type(error).__name__}: {error}")

            failures.append((number, error))

        else:
            elapsed = time.perf_counter() - start
            print(f"✔ Problem {number} passed ({elapsed:.4f}s)")

    print("=" * 80)
    end_time = time.perf_counter()
    print(f"Total time: {end_time - start_time:.4f}s")

    if failures:
        print(f"Smoke test failed: {len(failures)} problem(s) failed.")

        for number, error in failures:
            print(
                f"  - Problem {number}: "
                f"{type(error).__name__}: {error}"
            )

        raise SystemExit(1)

    print("Smoke test passed! All tested problems executed successfully.")


if __name__ == "__main__":
    main()