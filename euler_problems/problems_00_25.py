"""
Project Euler solutions: problem0 through problem25.

Problems00To25 is combined into EulerSolver in solver.py. It
genuinely inherits from UtilsMixin and EasterEggsMixin (which itself
inherits HelpersMixin) since these problems call self.header,
self.run_task, self.is_prime, self._try_easter_egg, and so on.
"""

import math
import itertools

from colorama import Fore

from .utils import UtilsMixin
from .easter_eggs import EasterEggs


class Problems00To25(UtilsMixin, EasterEggs):
    """Problem solutions 0-25."""

    # Set in EulerSolver.__init__; declared here for the type checker only.
    problem8_number: str
    problem11_grid: str
    problem13_numbers: str
    problem18triangle: list

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
        total = self.run_task("Finding the sum of the multiple...", lambda: sum(
            number
            for number in range(1000)
            if number % 3 == 0 or number % 5 == 0
        )
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
                n for n in self.fibonacci_sequence_limit(limit)
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
        "Find the largest palindromic number made from the product of two 3-digit numbers"
        self.header(
            4,
            "Find the largest palindromic number made from the product of two 3-digit numbers"
        )
        result_3, factors_3 = self.run_task(
            "Finding 3-digit palindrome...",
            self.get_largest_palindrome_product,
            3
        )
        print(f"The 3-digit palindrome is: {Fore.GREEN}{result_3}{Fore.RESET} (Factors: {Fore.GREEN}{factors_3}{Fore.RESET})")
    
    def problem5(self):
        "Find the smallest positive number that is evenly divisible by all numbers from 1 to 20."
        self.header(
            5,
            "Find the smallest positive number that is evenly divisible by all numbers from 1 to 20."
        )
        if self._try_easter_egg(5):
            return
        result = self.run_task(
            "Finding the least common multiple...",
            math.lcm,
            *range(1,21)
        )
        print(f"The smallest positive number is: {Fore.GREEN}{result}{Fore.RESET}")
    
    def problem6(self):
        "Find the difference between the square of the sum and the sum of the squares of the first 100 natural numbers"
        self.header(
            6,
            "Find the difference between the square of the sum and the sum of the squares of the first 100 natural numbers"
        )
        result = self.run_task(
            "Finding the difference...",
            self.sum_square_difference,
            100
        )
        print(f"The difference between the square of the sum and the sum of the squares is: {Fore.GREEN}{result}{Fore.RESET}")

    def problem7(self):
        "Find the 10,001st prime number"
        self.header(
            7,
            "Find the 10,001st prime number"
        )
        result = self.run_task(
            "Finding prime numbers using the Sieve of Eratosthenes...",
            self.sieve_of_eratosthenes,
            150000, 10001
        )
        print(f"The 10,001st prime number is: {Fore.GREEN}{result}{Fore.RESET}")

    def problem8(self):
        "Find the product of 13 adjacent digits in the 1000-digit number"
        self.header(
            8,
            "Find the product of 13 adjacent digits in the 1000-digit number"
        )
        result = self.run_task(
            "Finding max product...",
            self.adjacent_digit_multiplier,
            self.problem8_number,
            13
        )
        print(f"The max product of 13 adjacent digits in the 1000-digit number is: {Fore.GREEN}{result}{Fore.RESET}")

    def problem9(self):
        "Find the unique Pythagorean triplet where a + b + c = 1000 and the product a * b * c."
        self.header(
            9,
            "Find the unique Pythagorean triplet where a + b + c = 1000 and the product a * b * c."
        )
        all_triplets = self.run_task(
            "Finding all triplets until 500...",
            self.find_pythagorean_triplets,
            1000
        )
        for a, b, c in all_triplets:
            if a + b + c == 1000:
                product = a * b * c
                print(f"Found unique triplet: {Fore.GREEN}a={a}, b={b}, c={c}{Fore.RESET}")
                print(f"Product (a*b*c) = {Fore.GREEN}{product}{Fore.RESET}")

    def problem10(self):
        "Find the sum of all prime numbers below two million"
        self.header(
            10,
            "Find the sum of all prime numbers below two million"
        )
        result = self.run_task(
            "Finding the sum of all prime numbers...",
            self.sum_primes_under_limit,
            2000000
        )
        print(f"The sum of all prime numbers below two million is {Fore.GREEN}{result}{Fore.RESET}")

    def problem11(self):
        "Find the greatest product of four adjacent numbers in any direction within a given 20 * 20 grid of numbers"
        self.header(
            11,
            "Find the greatest product of four adjacent numbers in any direction within a given 20 * 20 grid of numbers"
        )
        grid_str = self.problem11_grid
        grid = [[int(num) for num in line.split()] for line in grid_str.strip().split("\n")]
        result = self.run_task(
            "Finding the max product...",
            self.grid_adjacent_digit_multiplier,
            grid
        )
        print(f"The greatest product is: {Fore.GREEN}{result}{Fore.RESET}")

    def problem12(self):
        "Find the value of the first triangle number to have over five hundred divisors"
        self.header(
            12,
            "Find the value of the first triangle number to have over five hundred divisors"
        )
        def find_first_triangle_number(limit):
            """Finds the first triangle number with more divisors than the limit."""
            triangle = 0
            for i in itertools.count(1):
                triangle += i  # i-th triangle number is 1 + 2 + ... + i
                if self.count_divisors(triangle) > limit:
                    return triangle
                
        result = self.run_task("Finding the triangle number...", find_first_triangle_number, 500)
        print(f"The first triangle number with over 500 divisors is: {Fore.GREEN}{result}{Fore.RESET}")

    def problem13(self):
        "Find the first ten digits of the sum of 100 50-digit numbers"
        self.header(
            13,
            "Find the first ten digits of the sum of 100 50-digit numbers"
        )
        numbers_string = self.problem13_numbers
        def task():
            lines = numbers_string.strip().splitlines()
            total_sum = sum(int(line) for line in lines)
            first_ten_digits = str(total_sum)[:10]
            return first_ten_digits
        
        result = self.run_task(
            "Finding the sum...",
            task
        )
        print(f"The first 10 digits are: {Fore.GREEN}{result}{Fore.RESET}")

    def problem14(self):
        "Find the starting number under one million that produces the longest Collatz chain"
        self.header(
            14,
            "Find the starting number under one million that produces the longest Collatz chain"
        )
        start_num, length = self.run_task(
            "Finding the starting number and length...",
            self.find_longest_collatz,
            1000000
        )
        print(f"The starting number is: {Fore.GREEN}{start_num}{Fore.RESET}")
        print(f"The chain length is: {Fore.GREEN}{length}{Fore.RESET}")

    def problem15(self):
        "Find the number of paths from the top-left to the bottom-right corner of a grid using only right and down moves"
        self.header(
            15,
            "Find the number of paths from the top-left to the bottom-right corner of a grid using only right and down moves"
        )
        result = self.run_task(
            "Finding all lattice paths...",
            self.count_lattice_paths,
            20
        )
        print(f"The total number of paths that exitsts is: {Fore.GREEN}{result}{Fore.RESET}")

    def problem16(self):
        "Find the sum of the digits of the number 2^1000"
        self.header(
            16,
            "Find the sum of the digits of the number 2^1000"
        )
        def task():
            # One-liner solution using a generator expression
            return sum(int(digit) for digit in str(2**1000))
        
        result = self.run_task(
            "Finding the sum...",
            task
        )
        print(f"The sum of the digits is: {Fore.GREEN}{result}{Fore.RESET}")

    def problem17(self):
        "Find the total number of letters used to write out the numbers in words from 1 to 1000"
        self.header(
            17,
            "Find the total number of letters used to write out the numbers in words from 1 to 1000"
        )
        def task():
            total_letters = 0
            for i in range(1, 1001):
                word_representation = self.number_to_words(i)
                clean_word = word_representation.replace(" ", "").replace("-", "")
                total_letters += len(clean_word)
            return total_letters
        
        result = self.run_task(
            "Counting all letters...",
            task
        )
        print(f"Total letter count is: {Fore.GREEN}{result}{Fore.RESET}")

    def problem18(self):
        "Find the maximum total from top to bottom of the given triangle"
        self.header(
            18,
            "Find the maximum total from top to bottom of the given triangle"
        )
        result = self.run_task(
            "Finding the maximum...",
            self.solve_maximum_path,
            self.problem18triangle
        )
        print(f"The maximum path sum is: {Fore.GREEN}{result}{Fore.RESET}")

    def problem19(self):
        "Find the number of Sundays that fell on the first of the month during the twentieth century (1 Jan 1901 to 31 Dec 2000). I am not using datetime to cheese it."
        self.header(
            19,
            "Find the number of Sundays that fell on the first of the month during the twentieth century (1 Jan 1901 to 31 Dec 2000)"
        )
        result = self.run_task(
            "Finding the number of Sundays...",
            self.count_sundays_algorithmic,
        )
        print(f"The Total number of Sundays is: {Fore.GREEN}{result}{Fore.RESET}")

    def problem20(self):
        "Find the sum of the digits in the number 100 factorial(!)"
        self.header(
            20,
            "Find the sum of the digits in the number 100 factorial(!)"
        )
        def task():
            return sum(map(int, str(math.factorial(100))))
        
        result = self.run_task(
            "Finding the sum...",
            task
        )
        print(f"The sum of the digits of 100! is: {Fore.GREEN}{result}{Fore.RESET} ")
    
    def problem21(self):
        "Find the sum of all the amicable numbers under 10000"
        self.header(
            21, 
            "Find the sum of all the amicable numbers under 10000"
        )
        def task(limit):
            amicable_sum = 0
            for a in range(1, limit):
                b = self.sum_proper_divisors(a)
                
                # Condition 1: a and b must be distinct (a != b)
                # Condition 2: avoid double counting by checking a < b
                if a < b and b < limit:
                    if self.sum_proper_divisors(b) == a:
                        amicable_sum += a + b
            return amicable_sum
        
        result = self.run_task(
            "Finding the sum...",
            task,
            10000
        )
        print(f"The sum of the amicable numbers is: {Fore.GREEN}{result}{Fore.RESET}")
    
    def problem22(self):
        "Find the total of all the name scores in the file"
        self.header(
            22,
            "Find the total of all the name scores in the file"
        )
        def task(file):
            # Read the text file containing the comma-separated names
            with open(file, 'r') as f:
                content = f.read()
            names = [name.strip('"') for name in content.split(',')]
            names.sort() 
            total_score = 0
            for rank, name in enumerate(names, start=1):
                alphabetical_value = sum(ord(char) - 64 for char in name)
                total_score += rank * alphabetical_value
            return total_score
        
        result = self.run_task(
            "Totaling up all name scores...",
            task,
            "0022_names.txt"
        )
        print(f"The total score of all the names is: {Fore.GREEN}{result}{Fore.RESET}")

    def problem23(self):
        "Find the sum of all the positive integers which cannot be written as the sum of two abundant numbers."
        self.header(
            23,
            "Find the sum of all the positive integers which cannot be written as the sum of two abundant numbers."
        )
        def task():
            # The mathematical ceiling given in the problem statement
            LIMIT = 28124  
            divisorsum = [0] * LIMIT
            for i in range(1, LIMIT):
                for j in range(i * 2, LIMIT, i):
                    divisorsum[j] += i
            abundant_nums = [i for (i, x) in enumerate(divisorsum) if x > i]
            expressible_as_abundant_sum = [False] * LIMIT
            for i in abundant_nums:
                for j in abundant_nums:
                    if i + j < LIMIT:
                        expressible_as_abundant_sum[i + j] = True
                    else:
                        # Since abundant_nums is sorted, if i + j exceeds the limit, 
                        # any subsequent j will also exceed it. We can safely break.
                        break
            total_sum = sum(i for (i, x) in enumerate(expressible_as_abundant_sum) if not x)
            return total_sum
        
        result = self.run_task(
            "Finding the sum...",
            task
        )
        print(f"The sum of all positive integers which cannot be written as the sum of two abundant numbers is: {Fore.GREEN}{result}{Fore.RESET}")
    
    def problem24(self):
        "Find the millionth lexicographic permutation of the digits 0, 1, 2, 3, 4, 5, 6, 7, 8 and 9"
        self.header(
            24,
            "Find the millionth lexicographic permutation of the digits 0, 1, 2, 3, 4, 5, 6, 7, 8 and 9"
        )
        def task():
            # 0-indexed position of the millionth permutation
            target_index = 999999 
            digits = list(range(10))
            result = []
            for i in range(9, -1, -1):
                digit_idx, target_index = divmod(target_index, math.factorial(i))
                result.append(digits.pop(digit_idx))
            return "".join(map(str, result))
        
        result = self.run_task(
            "Finding the millionth permutation...",
            task
        )
        print(f"The millionth lexicographic permutation is: {Fore.GREEN}{result}{Fore.RESET}")

    def problem25(self):
        "Find the index of the first term in the Fibonacci sequence to contain 1000 digits?"
        self.header(
            25,
            "Find the index of the first term in the Fibonacci sequence to contain 1000 digits?"
        )
        def task():
            index = 1
            for i, value in self.fibonacci_generator():
                # Check if the number has 1,000 digits
                if len(str(value)) >= 1000:
                    return index
                index += 1
        result = self.run_task(
            'Finding the 1000-digit Fibonacci number...',
            task
        )
        print(f"The index of the 1000-digit Fibonacci number is: {Fore.GREEN}{result}{Fore.RESET}")
    
