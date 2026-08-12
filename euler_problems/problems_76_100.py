"""
Project Euler solutions: problem76 through problem100.

Problems76To100 is combined into EulerSolver in solver.py. It
genuinely inherits from UtilsMixin and EasterEggs since these problems
call self.header, self.run_task, self.simulate_monopoly, self.sieve_of_eratosthenes_list 
and so on.
"""

import math
import itertools
import fractions
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

    def problem91(self):
        "Find the number of right triangles that can be formed in a 50x50 grid with one vertex at the origin."
        self.header(
            91,
            "Find the number of right triangles that can be formed in a 50x50 grid with one vertex at the origin."
        )
        def task(limit=50):
            count = 0
            # Loop over all possible positions for point P (x1, y1)
            for x1 in range(limit + 1):
                for y1 in range(limit + 1):
                    if x1 == 0 and y1 == 0:
                        continue
                        
                    # Loop over all possible positions for point Q (x2, y2)
                    for x2 in range(limit + 1):
                        for y2 in range(limit + 1):
                            if x2 == 0 and y2 == 0:
                                continue
                            
                            # Prevent duplicate combinations and overlapping lines
                            # This ensures angle(P) > angle(Q)
                            if y2 * x1 < y1 * x2:
                                # Calculate squared side lengths
                                op_sq = x1**2 + y1**2
                                oq_sq = x2**2 + y2**2
                                pq_sq = (x2 - x1)**2 + (y2 - y1)**2
                                
                                # Check if it satisfies the Pythagorean theorem
                                if (op_sq + oq_sq == pq_sq) or (op_sq + pq_sq == oq_sq) or (oq_sq + pq_sq == op_sq):
                                    count += 1
            return count
        result = self.run_task(
            "Counting right triangles...",
            task
        )
        print(f"The number of right triangles that can be formed is: {Fore.GREEN}{result}{Fore.RESET}")

    def problem92(self):
        "Find out how many starting numbers below 10,000,000 have a square digit sum chain that ends in 89."
        self.header(
            92,
            "Find out how many starting numbers below 10,000,000 have a square digit sum chain that ends in 89."
        )
        def task():
            # Precompute terminal endpoints for numbers up to 567 
            terminal = {1: 1, 89: 89}
            def get_terminal(n):
                if n in terminal:
                    return terminal[n]
                path = []
                while n not in terminal:
                    path.append(n)
                    n = sum(int(d)**2 for d in str(n))
                t = terminal[n]
                for p in path:
                    terminal[p] = t
                return t
            count_89 = 0
            
            # Generate all unique combinations of 7 digits (0-9) with replacement
            for combo in itertools.combinations_with_replacement(range(10), 7):
                if combo == (0, 0, 0, 0, 0, 0, 0):
                    continue  # Skip zero as the problem asks for starting numbers
                sq_sum = sum(d**2 for d in combo)
                if get_terminal(sq_sum) == 89:
                    counts = collections.Counter(combo)
                    perms = math.factorial(7)
                    for c in counts.values():
                        perms //= math.factorial(c)
                    count_89 += perms
            return count_89
        result = self.run_task(
            "Counting numbers ending in 89...",
            task
        )
        print(f"The number of starting numbers below 10,000,000 that have a square digit sum chain that ends in 89 is: {Fore.GREEN}{result}{Fore.RESET} ")

    def problem93(self):
        "Find the set of four distinct digits that can produce the longest consecutive sequence of positive integers using standard arithmetic operators."
        self.header(
            93,
            "Find the set of four distinct digits that can produce the longest consecutive sequence of positive integers using standard arithmetic operators."
        )
        def task():
            def get_expressions(a, b, c, d):
                # Generate all unique numeric values obtainable from 4 numbers
                def compute(nums):
                    if len(nums) == 1:
                        return {nums[0]}
                    results = set()
                    for i in range(1, len(nums)):
                        left_vals = compute(nums[:i])
                        right_vals = compute(nums[i:])
                        for l in left_vals:
                            for r in right_vals:
                                results.add(l + r)
                                results.add(l - r)
                                results.add(l * r)
                                if r != 0:
                                    results.add(l / r)
                    return results
                all_values = set()
                for p in set(itertools.permutations((a, b, c, d))):
                    # Convert to Fraction to handle division cleanly
                    frac_nums = [fractions.Fraction(x) for x in p]
                    all_values.update(compute(frac_nums))
                    
                # Extract positive integers
                int_values = set()
                for val in all_values:
                    if val.denominator == 1 and val.numerator > 0:
                        int_values.add(val.numerator)
                        
                return int_values
            def longest_streak(nums):
                n = 1
                while n in nums:
                    n += 1
                return n - 1
            max_streak = 0
            best_digits = ""
            combined = ""
            for a in range(1, 10):
                for b in range(a + 1, 10):
                    for c in range(b + 1, 10):
                        for d in range(c + 1, 10):
                            vals = get_expressions(a, b, c, d)
                            streak = longest_streak(vals)
                            if streak > max_streak:
                                max_streak = streak
                                best_digits = f"{a}, {b}, {c}, {d}"
                                combined = f"{a}{b}{c}{d}"
                                
            return best_digits, combined

        result, combined = self.run_task(
            "Doing some arithmetic...",
            task
        )
        print(f"The set of four distinct digits that can produce the longest consecutive sequence of positive integers is: {Fore.GREEN}{result}{Fore.RESET}")
        print(f"Which combined together is: {Fore.GREEN}{combined}{Fore.RESET}")

    def problem94(self):
        "Find the sum of perimeters for almost equilateral triangles with integer sides and area up to a perimeter limit."
        self.header(
            94,
            "Find the sum of perimeters for almost equilateral triangles with integer sides and area up to a perimeter limit."
        )
        def task(limit=1_000_000_000):
            # Initial solution for x^2 - 3y^2 = 4
            x, y = 4, 2
            total_perimeter_sum = 0
            while True:
                # Generate the next Pell solution using transformation rules
                next_x = 2 * x + 3 * y
                next_y = x + 2 * y
                x, y = next_x, next_y
                if (x - 1) % 3 == 0:
                    a = (x - 1) // 3
                    perimeter = 3 * a + 1
                    if perimeter > limit:
                        break
                    if a > 1: # Triangle must have positive area and physical meaning
                        total_perimeter_sum += perimeter
                if (x + 1) % 3 == 0:
                    a = (x + 1) // 3
                    perimeter = 3 * a - 1
                    if perimeter > limit:
                        break
                    if a > 1:
                        total_perimeter_sum += perimeter
            return total_perimeter_sum
        result = self.run_task(
            "Pell's matrix transformation...",
            task
        )
        print(f"The sum of perimeters for almost equilateral triangles is: {Fore.GREEN}{result}{Fore.RESET}")

    def problem95(self):
        "Find the smallest member of the longest amicable chain with no element exceeding one million."
        self.header(
            95,
            "Find the smallest member of the longest amicable chain with no element exceeding one million."
        )
        def task(limit=1_000_000):
            # Generate primes using sieve method
            is_prime = self.sieve_of_eratosthenes_list(limit + 1)
            primes = [i for i, prime in enumerate(is_prime) if prime]

            # Compute divisor sums linearly using prime factorization
            div_sum = [1] * (limit + 1)
            for p in primes:
                p_pow = p
                while p_pow <= limit:
                    term = (p_pow * p - 1) // (p - 1)
                    for j in range(p_pow, limit + 1, p_pow):
                        if (j // p_pow) % p != 0:
                            div_sum[j] *= term
                    p_pow *= p
            for i in range(2, limit + 1):
                div_sum[i] -= i

            # Find longest amicable chain (same loop logic as before)
            max_len = 0
            best_min_element = 0
            visited = [0] * (limit + 1)
            for i in range(2, limit + 1):
                if visited[i] != 0:
                    continue
                curr = i
                chain = []
                chain_set = set() 
                while curr <= limit and visited[curr] == 0:
                    visited[curr] = 2  
                    chain.append(curr)
                    chain_set.add(curr)
                    curr = div_sum[curr]              
                if curr <= limit and curr in chain_set:
                    loop_start_idx = chain.index(curr)
                    loop_elements = chain[loop_start_idx:]
                    loop_len = len(loop_elements)
                    
                    if loop_len > max_len:
                        max_len = loop_len
                        best_min_element = min(loop_elements)        
                for element in chain:
                    visited[element] = 1
            return best_min_element

        result = self.run_task(
            "Counting amicable chains...",
            task
        )
        print(f"The smallest member of the longest amicable chain is: {Fore.GREEN}{result}{Fore.RESET}")

    def problem96(self):
        "Solves 50 Sudoku puzzles and returns the sum of their top-left 3-digit numbers."
        self.header(
            96,
            "Solves 50 Sudoku puzzles and returns the sum of their top-left 3-digit numbers."
        )
        def task():
            puzzles = self.load_sudoku_puzzles("0096_sudoku.txt")
            total_sum = 0
            for i, grid in enumerate(puzzles):
                if self.solve_sudoku(grid):
                    # Extract the 3-digit number from the top-left corner
                    corner_value = grid[0][0] * 100 + grid[0][1] * 10 + grid[0][2]
                    total_sum += corner_value
            return total_sum
        result = self.run_task(
            "Solving sudokus...",
            task
        )
        print(f"The sum of there top-left 3-digit numbers is: {Fore.GREEN}{result}{Fore.RESET}")

    def problem97(self):
        "Find the last ten digits of 28433 x 2^(7830457) + 1"
        self.header(
            97,
            "Find the last ten digits of 28433 x 2^(7830457) + 1"
        )
        def solve():
            MOD = 10**10
            ans = (28433 * pow(2, 7830457, MOD) + 1) % MOD
            return ans
        result = self.run_task(
            "Huge Number Alert...",
            solve
        )
        print(f"The last ten digits of 28433 x 2^(7830457) + 1 is: {Fore.GREEN}{result}{Fore.RESET}")

    def problem98(self):
        "Find the maximum square number formed by an anagramic word pair."
        self.header(
            98,
            "Find the maximum square number formed by an anagramic word pair."
        )
        def task(words_list):
            # Group words by length and find anagram groups
            words_by_len = collections.defaultdict(list)
            for word in words_list:
                words_by_len[len(word)].append(word)
                
            anagram_pairs = []
            for length, words in words_by_len.items():
                if length < 2: 
                    continue
                # Group by sorted characters to find anagrams
                signature_map = collections.defaultdict(list)
                for word in words:
                    sig = "".join(sorted(word))
                    signature_map[sig].append(word)
                
                # Keep pairs/groups of anagrams
                for sig, matches in signature_map.items():
                    if len(matches) > 1:
                        anagram_pairs.append((length, matches))

            # Precompute perfect squares grouped by character length
            max_len = max([length for length, _ in anagram_pairs]) if anagram_pairs else 0
            squares_by_len = collections.defaultdict(list)
            limit = 10**max_len
            i = 1
            while True:
                sq = i * i
                if sq >= limit:
                    break
                sq_str = str(sq)
                squares_by_len[len(sq_str)].append(sq_str)
                i += 1

            max_square = 0

            # Match patterns between words and square strings
            for length, word_list in anagram_pairs:
                squares = squares_by_len[length]
                
                # Test every unique pair of words in the anagram group
                for i in range(len(word_list)):
                    for j in range(i + 1, len(word_list)):
                        word1 = word_list[i]
                        word2 = word_list[j]
                        
                        for sq_str in squares:
                            letter_to_digit = {}
                            digit_to_letter = {}
                            possible = True
                            
                            for char, digit in zip(word1, sq_str):
                                if char in letter_to_digit:
                                    if letter_to_digit[char] != digit:
                                        possible = False
                                        break
                                else:
                                    if digit in digit_to_letter:
                                        possible = False
                                        break
                                    letter_to_digit[char] = digit
                                    digit_to_letter[digit] = char
                            
                            if not possible:
                                continue
                            
                            # Convert word2 using the same mapping
                            word2_mapped = "".join(letter_to_digit[char] for char in word2)
                            if word2_mapped[0] == '0':
                                continue
                            if word2_mapped in squares:
                                val1 = int(sq_str)
                                val2 = int(word2_mapped)
                                max_square = max(max_square, val1, val2)
                                
            return max_square
        with open("0098_words.txt", "r") as f:
            raw_words = f.read()
            parsed_words = [w.strip('"') for w in raw_words.split(',')]

        result = self.run_task(
            "Looking through words",
            task,
            parsed_words
        )
        print(f"The maximum square number formed by an anagramic word pair is: {Fore.GREEN}{result}{Fore.RESET}")

    def problem99(self):
        "Find out which line number in a given text file has the largest numerical value when evaluated as base^(exponent)"
        self.header(
            99,
            "Find out which line number in a given text file has the largest numerical value when evaluated as base^(exponent)"
        )
        def task():
            max_value = 0.0
            best_line_number = 0
            with open("0099_base_exp.txt", "r") as file:
                for line_idx, line in enumerate(file, start=1):
                    if not line.strip():
                        continue
                    base_str, exp_str = line.split(",")
                    base = int(base_str)
                    exponent = int(exp_str)
                    
                    # Compute score using log properties
                    current_value = exponent * math.log(base)
                    
                    # Keep track of the maximum value seen so far
                    if current_value > max_value:
                        max_value = current_value
                        best_line_number = line_idx
            return best_line_number, max_value
        result, max_val = self.run_task(
            "Exponents are fun...",
            task
        )
        print(f"The number that has the largest numerical valye is: {Fore.GREEN}{result}{Fore.RESET}")
        print(f"With their score being: {Fore.GREEN}{max_val}{Fore.RESET}")

    def problem100(self):
        "Find the number of blue discs in a box of over 10^12 total discs where the probability of picking two blue discs is exactly 50%."
        self.header(
            100,
            "Find the number of blue discs in a box of over 10^12 total discs where the probability of picking two blue discs is exactly 50%."
        )
        def task():
            # Base case provided in the problem description (15 blue, 21 total)
            b = 15
            n = 21
            limit = 10**12
            
            # Generate larger pairs using Pell's equation recurrence relations
            while n <= limit:
                next_b = 3 * b + 2 * n - 2
                next_n = 4 * b + 3 * n - 3
                
                b, n = next_b, next_n
                
            return b
        result = self.run_task(
            "Calculating probabilities...",
            task
        )
        print(f"The number of blue disks is: {Fore.GREEN}{result}{Fore.RESET}")
        
    