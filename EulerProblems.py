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

        spinner.succeed(f"DONE! ({time.time() - start:.5f}s)")
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
        upper_bound = 10**digits - 1  
        lower_bound = 10 ** (digits - 1)  

        max_palindrome = 0
        best_factors = (0, 0)

        for i in range(upper_bound, lower_bound - 1, -1):
            if i * i < max_palindrome:
                break
            for j in range(i, lower_bound - 1, -1):
                product = i * j
                if product <= max_palindrome:
                    break
                if self.is_palindrome(product):
                    max_palindrome = product
                    best_factors = (i, j)

        return max_palindrome, best_factors
    
    def sum_square_difference(self, n=100):
        """
        Returns the difference between the square of the the sum and the sum of the square
        """
        square_of_sum = sum(range(1, n + 1)) ** 2
        sum_of_squares = sum(i**2 for i in range(1, n + 1))
        
        return square_of_sum - sum_of_squares
    
    def sieve_of_eratosthenes(self, limit:int, target_index:int):
        """
        Returns the prime numbers at your targeted index with a limit using the Sieve of Eratosthenes
        """
        sieve = [True] * limit
        sieve[0] = sieve[1] = False
        primes = []
        
        for num in range(2, limit):
            if sieve[num]:
                primes.append(num)
                if len(primes) == target_index:
                    return num
                for multiple in range(num * num, limit, num):
                    sieve[multiple] = False

         # CRITICAL FIX: Handle what happens if the loop ends and target isn't reached
        raise ValueError(f"{Fore.RED}The limit {limit} is too small to find prime index {target_index}. Increase your limit.{Fore.RESET}")

    def adjacent_digit_multiplier(self, num_str:str, window_size:int):
        """
        Returns the max product of adjacent numbers with a window size
        """
        max_product = 0
        for i in range(len(num_str) - window_size + 1):
            window = num_str[i : i + window_size]
            digits = [int(d) for d in window]
            # Use math.prod to calculate product of the window
            current_product = math.prod(digits)
            
            if current_product > max_product:
                max_product = current_product
        return max_product
    
    def find_pythagorean_triplets(self, limit):
        """
        Find all Pythagorean triplets where all numbers are less than or equal to the limit
        """
        triplets = []
        for a in range(1, limit + 1):
            for b in range(a + 1, limit + 1):
                c_squared = a**2 + b**2
                c = int(c_squared ** 0.5)
                
                if c * c == c_squared and c <= limit:
                    triplets.append((a, b, c))
        
        return triplets
    
    def sum_primes_under_limit(self, limit: int):
        """
        Returns the sum of all prime numbers below a given limit using the Sieve of Eratosthenes
        """
        sieve = [True] * limit
        sieve[0] = sieve[1] = False
        primes = []
        
        for num in range(2, limit):
            if sieve[num]:
                primes.append(num)
                # Optimization: No need to flag multiples if num * num is beyond our array limit
                if num * num < limit:
                    for multiple in range(num * num, limit, num):
                        sieve[multiple] = False
        return sum(primes)
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
            "7316717653133062491922511967442657474235534919493496983520312774506326239578318016984801869478851843858615607891129494954595017379583319528532088055111254069874715852386305071569329096329522744304355766896648950445244523161731856403098711121722383113622298934233803081353362766142828064444866452387493035890729629049156044077239071381051585930796086670172427121883998797908792274921901699720888093776657273330010533678812202354218097512545405947522435258490771167055601360483958644670632441572215539753697817977846174064955149290862569321978468622482839722413756570560574902614079729686524145351004748216637048440319989000889524345065854122758866688116427171479924442928230863465674813919123162824586178664583591245665294765456828489128831426076900422421902267105562632111110937054421750694165896040807198403850962455444362981230987879927244284909188845801561660979191338754992005240636899125607176060588611646710940507754100225698315520005593572972571636269561882670428252483600823257530420752963450",
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

    # ==========================================================
    # Runner
    # ==========================================================

    def run(self):
        self.problem0()
        self.problem1()
        self.problem2()
        self.problem3()
        self.problem4()
        self.problem5()
        self.problem6()
        self.problem7()
        self.problem8()
        self.problem9()
        self.problem10()


if __name__ == "__main__":
    solver = EulerSolver()
    solver.run()