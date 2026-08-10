"""
Project Euler solutions: problem76 through problem100.

Problems76To100 is combined into EulerSolver in solver.py. It
genuinely inherits from UtilsMixin and EasterEggs since these problems
call self.header, self.run_task, self.simulate_monopoly, self.sieve_of_eratosthenes_list 
and so on.
"""

import math
import itertools
import collections
import heapq

from colorama import Fore

from .utils import UtilsMixin
from .easter_eggs import EasterEggs


class Problems76To100(UtilsMixin, EasterEggs):
    """Problem solutions 76-100."""

    problem81_matrix: list[list[int]]
    monopoly_squares: list[str]

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

    def problem81(self):
        "Find the minimal path sum from the top left to the bottom right by only moving right and down in 0081_matrix.txt"
        self.header(
            81,
            "Find the minimal path sum from the top left to the bottom right by only moving right and down in 0081_matrix.txt"
        )
        def solve_matrix_path(matrix):
            rows = len(matrix)
            cols = len(matrix[0])
            for j in range(1, cols):
                matrix[0][j] += matrix[0][j - 1]
            for i in range(1, rows):
                matrix[i][0] += matrix[i - 1][0]
            for i in range(1, rows):
                for j in range(1, cols):
                    matrix[i][j] += min(matrix[i - 1][j], matrix[i][j - 1])
            return matrix[-1][-1]

        result = self.run_task(
            "Looking through the 80 by 80 matrix...",
            solve_matrix_path,
            self.problem81_matrix
        )
        print(f"The minimal path sum the top left to the bottom right is: {Fore.GREEN}{result}{Fore.RESET}")

    def problem82(self):
        "Find the minimal path sum from the left column to the right column in 0081_matrix.txt"
        self.header(
            82,
            "Find the minimal path sum from the left column to the right column in 0081_matrix.txt"
        )
        def solve(matrix):
            n = len(matrix)
            dp = [row[-1] for row in matrix]

            for col in range(n - 2, -1, -1):
                next_dp = [matrix[row][col] + dp[row] for row in range(n)]
                for row in range(1, n):
                    next_dp[row] = min(next_dp[row], next_dp[row - 1] + matrix[row][col])
                for row in range(n - 2, -1, -1):
                    next_dp[row] = min(next_dp[row], next_dp[row + 1] + matrix[row][col])
                dp = next_dp

            return min(dp)
        result = self.run_task(
            "Looking through the 80 by 80 matrix... again...",
            solve,
            self.problem81_matrix
        )
        print(f"The minimal path sum from the left column to the right column is: {Fore.GREEN}{result}{Fore.RESET}")

    def problem83(self):
        "Find the minimal path sum from the top left to the bottom right by moving left, right, up, and down in 0081_matrix.txt"
        self.header(
            83,
            "Find the minimal path sum from the top left to the bottom right by moving left, right, up, and down in 0081_matrix.txt"
        )
        def solve(mat):
            n = len(mat)
            m = len(mat[0])
            
            # Priority queue stores tuples of (cumulative_sum, row, col)
            pq = [(mat[0][0], 0, 0)]
            dist = [[float('inf')] * m for _ in range(n)]
            dist[0][0] = mat[0][0]
            directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
            
            while pq:
                current_sum, r, c = heapq.heappop(pq)
                if r == n - 1 and c == m - 1:
                    return current_sum
                if current_sum > dist[r][c]:
                    continue
                for dr, dc in directions:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < n and 0 <= nc < m:
                        new_sum = current_sum + mat[nr][nc]
                        if new_sum < dist[nr][nc]:
                            dist[nr][nc] = new_sum
                            heapq.heappush(pq, (new_sum, nr, nc))
        result = self.run_task(
            "Looking through the 80 by 80 matrix... again... and again...",
            solve,
            self.problem81_matrix
        )
        print(f"The minimal path sum from the top left to the bottom right by moving left, right, up, and down is: {Fore.GREEN}{result}{Fore.RESET}")

    def problem84(self):
        "Simulate a Monopoly board game using a Monte Carlo approach to find the three most frequently visited squares."
        self.header(
            84,
            "Simulate a Monopoly board game using a Monte Carlo approach to find the three most frequently visited squares."
        )
        modal_string, sorted_squares = self.run_task(
            "Simulating a monopoly game...",
            self.simulate_monopoly,
            self.monopoly_squares
        )
        print(f"The three most visited squares are: {Fore.GREEN}{sorted_squares}{Fore.RESET}")
        print(f"With their modal string being: {Fore.GREEN}{modal_string}{Fore.RESET}")

    def problem85(self):
        "Find an m x n grid where the number of sub-rectangles is closest to 2,000,000"
        self.header(
            85,
            "Find an m x n grid where the number of sub-rectangles is closest to 2,000,000"
        )
        def solve():
            target = 2000000
            closest_diff = target
            best_area = 0
            # Max m or n won't exceed roughly sqrt(2 * target) + 1 ≈ 2000
            for m in range(1, 2000):
                for n in range(m, 2000):  # start from m to avoid duplicate pairs
                    num_rects = (m * (m + 1) * n * (n + 1)) // 4
                    diff = abs(num_rects - target)
                    if diff < closest_diff:
                        closest_diff = diff
                        best_area = m * n
                    # If the count exceeds the target significantly, break inner loop
                    if num_rects > target + target:
                        break
            return best_area
        result = self.run_task(
            "Counting rectangles...",
            solve
        )
        print(f"The dimensions of a grid were the number of sub-rectangles is closest ti 2 million is: {Fore.GREEN}{result}{Fore.RESET}")

    def problem86(self):
        "Find the least value of M such that the number of solutions first exceeds one million."
        self.header(
            86,
            "Find the least value of M such that the number of solutions first exceeds one million."
        )
        def solve():
            count = 0
            M = 0
            target_limit = 1000000
            while count <= target_limit:
                M += 1
                for S in range(2, 2 * M + 1):
                    path_squared = M * M + S * S
                    root = math.isqrt(path_squared)
                    if root * root == path_squared:
                        if S <= M:
                            count += S // 2
                        else:
                            count += (S // 2) - (S - M) + 1
                            
            return M
        result = self.run_task(
            "Counting solutions...",
            solve
        )
        print(f"The least value of M such that the number of solutions first exceeds one million is: {Fore.GREEN}{result}{Fore.RESET}")

    def problem87(self):
        "Find out how many numbers below the limit can be expressed as the sum of a prime square, prime cube, and prime fourth power."
        self.header(
            87,
            "Find out how many numbers below the limit can be expressed as the sum of a prime square, prime cube, and prime fourth power."
        )
        def solve(limit=50_000_000):
            # The largest prime needed is just under the square root of the limit
            max_prime_limit = int(math.isqrt(limit)) + 1
            is_prime_list = self.sieve_of_eratosthenes_list(max_prime_limit)
            primes = [p for p, is_prime in enumerate(is_prime_list) if is_prime]
            valid_numbers = set()
            
            for a in primes:
                p4 = a**4
                if p4 >= limit:
                    break
                for b in primes:
                    p3 = b**3
                    if p4 + p3 >= limit:
                        break
                    for c in primes:
                        p2 = c**2
                        total = p4 + p3 + p2
                        if total >= limit:
                            break
                        valid_numbers.add(total)
                        
            return len(valid_numbers)
        result = self.run_task(
            "Sieve of Eratosthenes coming in clutch...",
            solve
        )
        print(f"The number of numbers below the limit is: {Fore.GREEN}{result}{Fore.RESET}")

    def problem88(self):
        "Find the sum of all the minimal product-sum numbers for 2 ≤ k ≤ 12000"
        self.header(
            88,
            "Find the sum of all the minimal product-sum numbers for 2 ≤ k ≤ 12000"
        )
        def solve(max_k=12000):
            limit = 2 * max_k
            min_product_sum = [float('inf')] * (max_k + 1)
            def search(product, sum_val, count, start):
                k = count + (product - sum_val)
                if k <= max_k:
                    if product < min_product_sum[k]:
                        min_product_sum[k] = product
                
                i = start
                while True:
                    next_prod = product * i
                    if next_prod > limit:
                        break
                    search(next_prod, sum_val + i, count + 1, i)
                    i += 1

            search(1, 0, 0, 2)
            
            unique_numbers = set(min_product_sum[2:])
            return sum(unique_numbers)
        result = self.run_task(
            "Why is there so many sums to solve...",
            solve
        )
        print(f"The sum of all the minimal product-sum numbers is: {Fore.GREEN}{result}{Fore.RESET}")

    def problem89(self):
        "Find the number of characters saved by writing each of these in their minimal form in Roman numerals."
        self.header(
            89,
            "Find the number of characters saved by writing each of these in their minimal form in Roman numerals."
        )
        def solve():
            chars_saved = 0
    
            with open("0089_roman.txt", "r") as file:
                for line in file:
                    original = line.strip()
                    integer_value = self.roman_to_int(original)
                    minimal_roman = self.int_to_roman(integer_value)
                    chars_saved += len(original) - len(minimal_roman)
            return chars_saved
        result = self.run_task(
            "Roman numerals vs Arabic numerals...",
            solve
        )
        print(f"The number of characters saved is: {Fore.GREEN}{result}{Fore.RESET}")

    def problem90(self):
        "Find the number of distinct arrangements of the two cubes allow for all of the square numbers to be displayed"
        self.header(
            90,
            "Find the number of distinct arrangements of the two cubes allow for all of the square numbers to be displayed"
        )
        def can_form_squares(die1, die2):
            # Target 2-digit squares under 100
            squares = [
                ('0', '1'), ('0', '4'), ('0', '9'), 
                ('1', '6'), ('2', '5'), ('3', '6'), 
                ('4', '9'), ('6', '4'), ('8', '1')
            ]
            d1 = set(str(x) for x in die1)
            if '6' in d1 or '9' in d1:
                d1.add('6')
                d1.add('9')
            d2 = set(str(x) for x in die2)
            if '6' in d2 or '9' in d2:
                d2.add('6')
                d2.add('9')
            # Check if every single square number can be formed by the two dice
            for digit1, digit2 in squares:
                if not (
                    (digit1 in d1 and digit2 in d2) or 
                    (digit1 in d2 and digit2 in d1)
                ):
                    return False
            return True

        def task():
            # Generate all unique combinations of 6 digits from 0-9
            all_dice = list(itertools.combinations(range(10), 6))
            valid_pairs = 0
            
            # Iterate over all unique unordered pairs of dice
            for i in range(len(all_dice)):
                for j in range(i, len(all_dice)):
                    if can_form_squares(all_dice[i], all_dice[j]):
                        valid_pairs += 1
                        
            return valid_pairs

        result = self.run_task(
            "Rolling the two cubes a.k.a. dice...",
            task
        )
        print(f"The number of distict arrangements if the dice is: {Fore.GREEN}{result}{Fore.RESET}")


    