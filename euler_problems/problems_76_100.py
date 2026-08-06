"""
Project Euler solutions: problem76 through problem100.

Problems76To100 is combined into EulerSolver in solver.py. It
genuinely inherits from UtilsMixin and EasterEggs since these problems
call self.header, self.run_task, 
"""

import math
import itertools
import collections

from colorama import Fore

from .utils import UtilsMixin
from .easter_eggs import EasterEggs


class Problems76To100(UtilsMixin, EasterEggs):
    """Problem solutions 76-100."""

    def problem76(self):
        "Find the number of ways can one hundred be written as a sum of at least two positive integers."
        self.header(
            76,
            "Find the number of ways can one hundred be written as a sum of at least two positive integers."
        )
        def task(target=100):
            # Initialize a list to store the number of combinations for each value
            # ways[i] will store the number of partitions for the number i
            ways = [1] + [0] * target
            
            for i in range(1, target):
                for j in range(i, target + 1):
                    ways[j] += ways[j - i]
                    
            return ways[target]
        result = self.run_task(
            "Trying combinations...",
            task
        )
        print(f"The number of ways is: {Fore.GREEN}{result}{Fore.RESET}")

    def problem77(self):
        "Find the first value that can be written as a sum of primes in over 5,000 different ways"
        self.header(
            77,
            "Find the first value that can be written as a sum of primes in over 5,000 different ways"
        )
        def task(LIMIT=100):
            # Get the primes from  sieve
            is_prime_list = self.sieve_of_eratosthenes_list(LIMIT)
            primes = [i for i, is_p in enumerate(is_prime_list) if is_p]
            ways = [0] * LIMIT
            ways[0] = 1  # Base case: 1 way to form the sum 0
            
            # Run the unbounded coin-change DP algorithm
            for p in primes:
                for i in range(p, LIMIT):
                    ways[i] += ways[i - p]
                    
            # Find the first integer that exceeds 5,000 ways
            for i in range(2, LIMIT):
                if ways[i] > 5000:
                    return i, ways[i]
        result, combinations = self.run_task(
            "Sieving through numbers...",
            task
        )
        print(f"The first value that can be written as a sum of primes in over 5,000 different ways is: {Fore.GREEN}{result}{Fore.RESET}")
        print(f"With the number different ways being: {Fore.GREEN}{combinations}{Fore.RESET}")

    def problem78(self):
        "Find the minimum value of n for which the coin partition function p(n) is divisible by one million"
        self.header(
            78,
            "Find the minimum value of n for which the coin partition function p(n) is divisible by one million"
        )
        def task():
            p = [1]
            modulus = 10**6
            n = 1
            while True:
                p_n = 0
                k = 1
                while True:
                    # Generate pentagonal numbers for k and -k
                    g1 = k * (3 * k - 1) // 2
                    g2 = k * (3 * k + 1) // 2
                    sign = 1 if k % 2 != 0 else -1
                    if g1 <= n:
                        p_n += sign * p[n - g1]
                    if g2 <= n:
                        p_n += sign * p[n - g2]
                        
                    # If both generated gaps exceed our current target, terminate loop
                    if g1 > n and g2 > n:
                        break
                    k += 1
                # Apply modulo to keep numbers small and fast
                p_n %= modulus
                # Target match check
                if p_n == 0:
                    return n
                    
                p.append(p_n)
                n += 1
        result = self.run_task(
            "Generating pentagonal numbers...",
            task
        )
        print(f"The minimum value of n for which the coin partition function p(n) is divisible by one million is: {Fore.GREEN}{result}{Fore.RESET}")

    def problem79(self):
        "Find the shortest secret passcode by topologically sorting digit precedence from keylog entries."
        self.header(
            79,
            "Find the shortest secret passcode by topologically sorting digit precedence from keylog entries."
        )
        def task():
            with open("0079_keylog.txt", "r") as f:
                attempts = [line.strip() for line in f if line.strip()]
            after_map = {digit: set() for attempt in attempts for digit in attempt}
            for attempt in attempts:
                d1, d2, d3 = attempt[0], attempt[1], attempt[2]
                after_map[d1].add(d2)
                after_map[d1].add(d3)
                after_map[d2].add(d3)
            # Sort unique digits by the number of subsequent digits (descending order)
            sorted_digits = sorted(after_map.keys(), key=lambda d: len(after_map[d]), reverse=True)

            passcode = "".join(sorted_digits)
            return passcode
        result = self.run_task(
            "Finding the secret password...",
            task
        )
        print(f"The secret password is: {Fore.GREEN}{result}{Fore.RESET}")

    def problem80(self):
        "Find the sum of the first 100 decimal digits for all irrational square roots of the first 100 natural numbers."
        self.header(
            80,
            "Find the sum of the first 100 decimal digits for all irrational square roots of the first 100 natural numbers."
        )
        def task():
            total_digit_sum = 0
            multiplier = 10**200 
            for i in range(1, 101):
                root = math.isqrt(i)
                # Skip perfect squares 
                if root * root == i:
                    continue
                scaled_root = math.isqrt(i * multiplier)
                digits_str = str(scaled_root)[:100]
                # Sum the numerical value of each digit
                total_digit_sum += sum(int(digit) for digit in digits_str)
            return total_digit_sum
        result = self.run_task(
            "Looking through non-perfect squares...",
            task
        )
        print(f"The sum of the first 100 decimal digits of the first 100 natural number's irrational square roots is: {Fore.GREEN}{result}{Fore.RESET}")