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

    def largest_prime_factor(self, n) -> int:
        """Return the largest prime factor of n."""
        factor = 2

        while factor * factor <= n:
            if n % factor == 0:
                n //= factor
            else:
                factor += 1

        return n
    
    def is_palindrome(self, number: int) -> bool:
        """Checks if a number reads the same backward as forward."""
        return str(number) == str(number)[::-1]

    def get_largest_palindrome_product(self, digits: int) -> tuple:
        """
        Finds the largest palindrome made from the product of two N-digit numbers.
        Returns a tuple containing: (largest_palindrome, factor_1, factor_2)
        """
        # Calculate limits dynamically based on digit count
        upper_bound = 10**digits - 1  # e.g., 999 for 3 digits
        lower_bound = 10 ** (digits - 1)  # e.g., 100 for 3 digits

        max_palindrome = 0
        best_factors = (0, 0)

        # Iterate downwards to find the largest product first
        for i in range(upper_bound, lower_bound - 1, -1):

            # Optimization 1: i * i is the maximum possible product for the current i.
            # If it is smaller than our current maximum, no larger palindrome can be found.
            if i * i < max_palindrome:
                break

            for j in range(i, lower_bound - 1, -1):
                product = i * j

                # Optimization 2: Since j decreases, products will only get smaller.
                if product <= max_palindrome:
                    break

                if self.is_palindrome(product):
                    max_palindrome = product
                    best_factors = (i, j)

        return max_palindrome, best_factors
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

    def problem4(self):
        "find the largest palindromic number made from the product of two 3-digit numbers"
        self.header(
            4,
            "find the largest palindromic number made from the product of two 3-digit numbers"
        )
        result_3, factors_3 = self.run_task(
            "Finding 3-digit palindrome...",
            self.get_largest_palindrome_product,
            3
        )
        print(f"3-Digit Result: {Fore.GREEN}{result_3} {Fore.RESET} (Factors: {Fore.GREEN}{factors_3})")

    # ==========================================================
    # Runner
    # ==========================================================

    def run(self):
        self.problem0()
        self.problem1()
        self.problem2()
        self.problem3()
        self.problem4()


if __name__ == "__main__":
    solver = EulerSolver()
    solver.run()