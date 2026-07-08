import time
import math

import colorama
from colorama import Fore
from halo import Halo


class EulerSolver:
    """A collection of Project Euler solutions."""

    def __init__(self):
        colorama.init(autoreset=True)

    # ==========================================================
    # Helper Methods
    # ==========================================================

    def header(self, problem_number: int, description: str):
        """Print a formatted problem header."""
        print(f"\nEuler's problem {problem_number}: {Fore.BLUE}{description}")

    def run_task(self, text: str, function, *args):
        """Run a function with a Halo spinner and timer."""
        spinner = Halo(text=text, spinner="dots")
        start = time.time()
        spinner.start()

        result = function(*args)

        spinner.succeed(f"DONE! ({time.time() - start:.3f}s)")
        return result

    # ==========================================================
    # Utility Functions
    # ==========================================================

    def find_all_squares_until(self, limit):
        """Return every perfect square up to the given limit."""
        squares = []

        n = 0
        while n * n <= limit:
            squares.append(n * n)
            n += 1

        return squares

    def fibonacci_sequence(self, limit):
        """Yield Fibonacci numbers below the given limit."""
        a, b = 0, 1

        while a < limit:
            yield a
            a, b = b, a + b

    def largest_prime_factor(self, n):
        """Return the largest prime factor of n."""
        factor = 2

        while factor * factor <= n:
            if n % factor == 0:
                n //= factor
            else:
                factor += 1

        return n

    # ==========================================================
    # Project Euler Problems
    # ==========================================================

    def problem0(self):
        """Find the sum of all odd perfect squares up to 756000"""
        self.header(
            0,
            "Find the sum of all odd perfect squares up to 756000"
        )

        squares = self.run_task(
            "Finding perfect squares...",
            self.find_all_squares_until,
            756000
        )

        # Every number here is already a perfect square.
        odd_squares = [square for square in squares if square % 2 == 1]

        print(f"Total odd perfect squares found: {Fore.GREEN}{len(odd_squares)}")
        print(f"Sum of odd perfect squares: {Fore.GREEN}{sum(odd_squares)}")

    def problem1(self):
        """Find the sum of all multiples of 3 or 5 below 1000"""
        self.header(
            1,
            "Find the sum of all multiples of 3 or 5 below 1000"
        )

        total = sum(
            number
            for number in range(1000)
            if number % 3 == 0 or number % 5 == 0
        )

        print(f"Sum of multiples of 3 or 5 below 1000: {Fore.GREEN}{total}")

    def problem2(self):
        """Find the sum of all even Fibonacci numbers below 4 million"""
        self.header(
            2,
            "Find the sum of all even Fibonacci numbers below 4 million"
        )

        even_fibonacci = self.run_task(
            "Generating Fibonacci numbers...",
            lambda limit: [
                n for n in self.fibonacci_sequence(limit)
                if n % 2 == 0
            ],
            4000000
        )

        print(
            f"Sum of even Fibonacci numbers below 4 million: "
            f"{Fore.GREEN}{sum(even_fibonacci)}"
        )

    def problem3(self):
        """Find the largest prime factor of 600851475143"""
        self.header(
            3,
            "Find the largest prime factor of 600851475143"
        )

        largest_factor = self.run_task(
            "Finding largest prime factor...",
            self.largest_prime_factor,
            600851475143
        )

        print(
            f"Largest prime factor of 600851475143: "
            f"{Fore.GREEN}{largest_factor}"
        )

    # ==========================================================
    # Runner
    # ==========================================================

    def run(self):
        self.problem0()
        self.problem1()
        self.problem2()
        self.problem3()


if __name__ == "__main__":
    solver = EulerSolver()
    solver.run()