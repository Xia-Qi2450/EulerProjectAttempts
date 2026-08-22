"""
Reusable math/number-theory helper functions used across many Euler
problem solutions (primes, palindromes, sieves, sequences, etc.).

UtilsMixin is combined into EulerSolver in solver.py.
"""

import math
import collections
import random

from colorama import Fore


class UtilsMixin:
    """Standalone math helpers shared by problem solutions."""

    # Set in EulerSolver.__init__; declared here for the type checker only.
    CARD_VALUES: dict
    ROMAN_MAP: dict[str, int]

    def find_all_squares_until(self, limit:int) -> list[int]:
        """Return every perfect square up to the given limit."""
        squares = []

        n = 0
        while n * n <= limit:
            squares.append(n * n)
            n += 1

        return squares

    def fibonacci_generator(self):
        """Yields (index, value) pairs for the Fibonacci sequence."""
        a, b = 1, 1
        index = 1
        
        while True:
            yield index, a
            a, b = b, a + b

    def fibonacci_sequence_limit(self, limit:int):
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

    def is_palindrome(self, s) -> bool:
        return s == s[::-1]
    
    def is_palindrome_str(self, number: int) -> bool:
        """Checks if a number reads the same backward as forward."""
        return str(number) == str(number)[::-1]
    
    def is_prime(self, n:int) -> bool:
        """Checks if a number is prime."""
        if n < 2:
            return False
        for i in range(2, int(math.isqrt(n)) + 1):
            if n % i == 0:
                return False
        return True

    def is_square(self, n:int) -> bool:
        s = int(math.isqrt(n))
        return s * s == n

    def get_largest_palindrome_product(self, digits: int) -> tuple[int, tuple[int, int]]:
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
                if self.is_palindrome_str(product):
                    max_palindrome = product
                    best_factors = (i, j)

        return max_palindrome, best_factors
    
    def sum_square_difference(self, n:int=100):
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

    def sieve_of_eratosthenes_list(self, limit:int):
        """Generates a boolean list where index represents primality."""
        is_prime = [True] * limit
        is_prime[0] = is_prime[1] = False
        for i in range(2, int(limit**0.5) + 1):
            if is_prime[i]:
                for j in range(i * i, limit, i):
                    is_prime[j] = False
        return is_prime

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
    
    def find_pythagorean_triplets(self, limit:int) -> list[tuple[int, int, int]]:
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
    
    def grid_adjacent_digit_multiplier(self, grid:list[list[int]]):
        """
        Returns the max product of the 4 adjacent numbers in every direction in a grid
        """
        max_product = 0
        rows, cols = len(grid), len(grid[0])

        # Iterate through every cell and check four directions
        for r in range(rows):
            for c in range(cols):
                # Horizontal (Right)
                if c + 3 < cols:
                    max_product = max(max_product, grid[r][c] * grid[r][c+1] * grid[r][c+2] * grid[r][c+3])
                # Vertical (Down)
                if r + 3 < rows:
                    max_product = max(max_product, grid[r][c] * grid[r+1][c] * grid[r+2][c] * grid[r+3][c])
                # Diagonal Down-Right
                if r + 3 < rows and c + 3 < cols:
                    max_product = max(max_product, grid[r][c] * grid[r+1][c+1] * grid[r+2][c+2] * grid[r+3][c+3])
                # Diagonal Down-Left
                if r + 3 < rows and c - 3 >= 0:
                    max_product = max(max_product, grid[r][c] * grid[r+1][c-1] * grid[r+2][c-2] * grid[r+3][c-3])
        return max_product
    
    def count_divisors(self, n:int):
        """Finds the number of divisors for a given integer."""
        divisors = 0
        end = math.isqrt(n)
        for i in range(1, end + 1):
            if n % i == 0:
                divisors += 2 
        if end * end == n:
            divisors -= 1  
        return divisors
    
    def find_longest_collatz(self, limit=1000000):
        cache = [0] * limit
        cache[1] = 1  # Base case: 1 has a chain length of 1
        max_len = 0
        best_start = 0
        
        for i in range(1, limit):
            n = i
            path = []
            # Traverse until we hit a number whose chain length is already known
            while n >= limit or cache[n] == 0:
                path.append(n)
                if n % 2 == 0:
                    n //= 2
                else:
                    n = 3 * n + 1
            # Populate the cache for all unmapped sequence steps in reverse order
            current_len = cache[n]
            for element in reversed(path):
                current_len += 1
                if element < limit:
                    cache[element] = current_len
            # Keep track of the longest chain found
            if cache[i] > max_len:
                max_len = cache[i]
                best_start = i
        return best_start, max_len
    
    def count_lattice_paths(self, grid_size:int):
        """
        Creates a grid and populates each node with the sum of the paths from its right and bottom neighbors.
        """
        dp = [[0] * (grid_size + 1) for _ in range(grid_size + 1)]
        
        for i in range(grid_size + 1):
            dp[i][grid_size] = 1
            dp[grid_size][i] = 1
        for r in range(grid_size - 1, -1, -1):
            for c in range(grid_size - 1, -1, -1):
                dp[r][c] = dp[r + 1][c] + dp[r][c + 1]
        return dp[0][0]
    
    def number_to_words(self, n:int):
        "Returns the pronounced version of words up to 1000. The English language sucks."
        # Dictionaries to map the irregular patterns of the English language
        ones = ["", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", 
                "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", 
                "seventeen", "eighteen", "nineteen"]
        tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]
        if n == 1000:
            return "one thousand"
        words = []
        if n >= 100:
            words.append(ones[n // 100] + " hundred")
            n %= 100
            # If there are trailing numbers, British convention requires "and"
            if n > 0:
                words.append("and")
        if n >= 20:
            words.append(tens[n // 10])
            if n % 10 > 0:
                words.append(ones[n % 10])
        elif n > 0:
            words.append(ones[n])
            
        return " ".join(words)
    
    def solve_maximum_path(self, triangle:list[list[int]]):
        "Returns the path with the max value"
        # Iterate from the second-to-last row up to the top row (row index 0)
        for row in reversed(range(len(triangle) - 1)):
            for col in range(len(triangle[row])):
                max_child = max(triangle[row + 1][col], triangle[row + 1][col + 1])
                triangle[row][col] += max_child
                
        return triangle[0][0]
    
    def is_leap_year(self, year:int) -> bool:
        # A leap year occurs on any year evenly divisible by 4, 
        # but not on a century unless it is divisible by 400.
        if year % 400 == 0:
            return True
        if year % 100 == 0:
            return False
        return year % 4 == 0
    
    def count_sundays_algorithmic(self):
        # Days in each month (January to December)
        months = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        
        # 1 Jan 1900 was a Monday (let Monday = 1, Sunday = 0)
        # 1900 was not a leap year (365 days). 365 % 7 = 1 day shift.
        # Therefore, 1 Jan 1901 was a Tuesday (weekday = 2).
        current_weekday = 2 
        sundays = 0
        
        for year in range(1901, 2001):
            for month_idx in range(12):
                # If the current day is Sunday (0), increment count
                if current_weekday == 0:
                    sundays += 1
                    
                # Determine days in the current month
                days_in_month = months[month_idx]
                if month_idx == 1 and self.is_leap_year(year): # February
                    days_in_month = 29
                    
                # Shift the weekday tracker for the 1st of the next month
                current_weekday = (current_weekday + days_in_month) % 7
                
        return sundays
    
    def sum_proper_divisors(self, n:int):
        """Calculates the sum of all proper divisors of n."""
        if n <= 1:
            return 0
        
        # 1 is always a proper divisor
        total_sum = 1 
        
        # Find factors up to the square root of n
        for i in range(2, int(n**0.5) + 1):
            if n % i == 0:
                total_sum += i
                # If factors are distinct, add the matching pair
                if i != n // i:
                    total_sum += n // i
                    
        return total_sum

    def has_pandigital_product(self, n:int) -> bool:
        # Find all factors of the product n
        for i in range(1, math.isqrt(n) + 1):
            if n % i == 0:
                identity_str = f"{i}{n // i}{n}"
                if len(identity_str) == 9 and "".join(sorted(identity_str)) == "123456789":
                    return True
        return False

    def word_value(self, word:str) -> int:
        """Calculate the sum of letter positions (A=1, B=2, etc.)."""
        return sum(ord(char) - ord('A') + 1 for char in word)

    def is_triangle(self, n:int) -> bool:
        """Check if n is a triangle number using 8n + 1 perfect square test."""
        root = math.isqrt(8 * n + 1)
        return root * root == 8 * n + 1 and root % 2 == 1

    def is_substring_divisible(self, num:tuple) -> bool:
        primes = [2, 3, 5, 7, 11, 13, 17]
        for i, p in enumerate(primes):
            # Extract 3-digit substring starting at index i + 1
            sub = num[i + 1] * 100 + num[i + 2] * 10 + num[i + 3]
            if sub % p != 0:
                return False
        return True

    def is_pentagonal(self, n:int) -> bool:
        """Check if n is a pentagonal number using the inverse formula"""
        # P_k = k(3k - 1)/2 => 3k^2 - k - 2P = 0
        # k = (1 + sqrt(1 + 24 * n)) / 6
        temp = (1 + (1 + 24 * n) ** 0.5) / 6
        return temp.is_integer()

    def evaluate_hand(self, hand:list) -> tuple[int, list[int]]:
        """
        Evaluates a 5-card hand and returns a score tuple: (hand_rank, [tie_breakers])
        Higher hand_rank wins. If equal, Python automatically compares the elements 
        inside the tie_breakers list from left to right.
        """
        ranks = sorted([self.CARD_VALUES[card[0]] for card in hand], reverse=True)
        suits = [card[1] for card in hand]
        is_flush = len(set(suits)) == 1
        is_straight = len(set(ranks)) == 5 and (ranks[0] - ranks[4] == 4)
        frequencies = sorted([(ranks.count(r), r) for r in set(ranks)], reverse=True)
        counts_pattern = [f[0] for f in frequencies]
        tie_breakers = [f[1] for f in frequencies]
        
        # Hand Rank Categories:
        # 8: Straight Flush (and Royal Flush if top card is Ace)
        # 7: Four of a Kind
        # 6: Full House
        # 5: Flush
        # 4: Straight
        # 3: Three of a Kind
        # 2: Two Pair
        # 1: One Pair
        # 0: High Card
        
        if is_straight and is_flush:
            return (8, tie_breakers)
        if counts_pattern == [4, 1]:
            return (7, tie_breakers)
        if counts_pattern == [3, 2]:
            return (6, tie_breakers)
        if is_flush:
            return (5, tie_breakers)
        if is_straight:
            return (4, tie_breakers)
        if counts_pattern == [3, 1, 1]:
            return (3, tie_breakers)
        if counts_pattern == [2, 2, 1]:
            return (2, tie_breakers)
        if counts_pattern == [2, 1, 1, 1]:
            return (1, tie_breakers)
        return (0, tie_breakers)

    def is_lychrel(self, n:int) -> bool:
        """Checks if a number is a Lychrel number"""
        for _ in range(50):
            n += int(str(n)[::-1])
            if str(n) == str(n)[::-1]:
                return False 
        return True 

    def generate_polygonal_numbers(self):
        """Generates polygonal numbers from triangles to octagons"""
        # Formulas mapped from 3 (Triangle) to 8 (Octagonal)
        formulas = {
            3: lambda n: n * (n + 1) // 2,
            4: lambda n: n * n,
            5: lambda n: n * (3 * n - 1) // 2,
            6: lambda n: n * (2 * n - 1),
            7: lambda n: n * (5 * n - 3) // 2,
            8: lambda n: n * (3 * n - 2)
        }
        poly_map = collections.defaultdict(list)
        for sides, formula in formulas.items():
            n = 1
            while True:
                val = formula(n)
                if val >= 10000:
                    break
                if val >= 1000:
                    if val % 100 >= 10:
                        poly_map[sides].append(val)
                n += 1
        return poly_map

    def get_period_length(self, n:int):
        """
        Computes the period length of the continued fraction for sqrt(n).
        Returns 0 if n is a perfect square.
        """
        a0 = math.isqrt(n)
        if a0 * a0 == n:
            return 0  # Perfect squares have no periodic fractional part
        m = 0
        d = 1
        a = a0
        period = 0
        
        while a != 2 * a0:
            m = d * a - m
            d = (n - m * m) // d
            a = (a0 + m) // d
            period += 1
        return period

    def solve_pell(self, d:int):
        """Returns the fundamental x for x^2 - d*y^2 = 1 using continued fractions"""
        m = 0
        d_denom = 1
        a0 = int(math.isqrt(d))
        a = a0
        
        num1, num = 1, a0
        den1, den = 0, 1
        
        while num * num - d * den * den != 1:
            m = d_denom * a - m
            d_denom = (d - m * m) // d_denom
            a = (a0 + m) // d_denom
            
            num1, num = num, a * num + num1
            den1, den = den, a * den + den1
            
        return num

    def simulate_monopoly(self, squares, rolls=1000000, sides=4):
        def handle_chance(card, pos):
            # 0: Advance to GO
            if card == 0:
                return 0
            # 1: Go to JAIL
            elif card == 1:
                return 10
            # 2: Advance to C1
            elif card == 2:
                return 11
            # 3: Advance to E3
            elif card == 3:
                return 24
            # 4: Advance to H2
            elif card == 4:
                return 39
            # 5: Advance to R1
            elif card == 5:
                return 5

            # 6 & 7: Go to next Railroad (R1=5, R2=15, R3=25, R4=35)
            elif card in (6, 7):
                if pos == 7:
                    return 15  # CH1 -> R2
                if pos == 22:
                    return 25  # CH2 -> R3
                if pos == 36:
                    return 5  # CH3 -> R1 (wraps around)

            # 8: Go to next Utility (U1=12, U2=28)
            elif card == 8:
                if pos in (7, 36):
                    return 12  # CH1 or CH3 -> U1
                if pos == 22:
                    return 28  # CH2 -> U2

            # 9: Go back 3 squares
            elif card == 9:
                new_pos = (pos - 3) % 40
                # Special edge case: If CH3 (36) sends you back 3, you land on CC3 (33).
                # You must immediately pull a Community Chest card.
                if new_pos == 33:
                # This is handled inside the main loop.
                    pass
                return new_pos
            # 10-15: Do nothing (player stays on the Chance square)
            return pos

        pos = 0
        doubles_count = 0
        counts = {sq: 0 for sq in squares}

        cc_deck = list(range(16))
        ch_deck = list(range(16))
        random.shuffle(cc_deck)
        random.shuffle(ch_deck)

        for _ in range(rolls):
            d1 = random.randint(1, sides)
            d2 = random.randint(1, sides)

            if d1 == d2:
                doubles_count += 1
            else:
                doubles_count = 0

            if doubles_count == 3:
                pos = 10  # JAIL
                doubles_count = 0
            else:
                pos = (pos + d1 + d2) % 40

            # Process square rules
            current_sq = squares[pos]
            if "CH" in current_sq:
                card = ch_deck.pop(0)
                ch_deck.append(card)
                pos = handle_chance(card, pos)
                # CRITICAL: If Chance sends you back 3 from CH3, you are now on CC3!
                # You must immediately resolve a Community Chest card.
                if pos == 33: 
                    card = cc_deck.pop(0)
                    cc_deck.append(card)
                    if card == 0: pos = 0
                    elif card == 1: pos = 10

            elif "CC" in current_sq:
                card = cc_deck.pop(0)
                cc_deck.append(card)
                if card == 0: pos = 0
                elif card == 1: pos = 10

            if squares[pos] == "G2J":
                pos = 10
                
            # Check again in case Chance moved the player to Go to Jail or Community Chest
            current_sq = squares[pos]
            if current_sq == "G2J":
                pos = 10
            elif "CC" in current_sq:
                card = cc_deck.pop(0)
                cc_deck.append(card)
                if card == 0:
                    pos = 0
                elif card == 1:
                    pos = 10

            counts[squares[pos]] += 1

        sorted_sqs = sorted(counts.keys(), key=lambda x: counts[x], reverse=True)
        res = [str(squares.index(sq)) for sq in sorted_sqs[:3]]
        return "".join([num.zfill(2) for num in res]), sorted_sqs[:3]

    def roman_to_int(self, s: str) -> int:
        """Converts a Roman numeral string to an integer."""
        total = 0
        i = 0
        while i < len(s):
            # Check two character subtractive pairs first
            if i + 1 < len(s) and s[i:i+2] in self.ROMAN_MAP:
                total += self.ROMAN_MAP[s[i:i+2]]
                i += 2
            else:
                total += self.ROMAN_MAP[s[i]]
                i += 1
        return total

    def int_to_roman(self, num: int) -> str:
        """Converts an integer to its minimal Roman numeral string."""
        result = []
        for token, val in self.ROMAN_MAP.items():
            count = num // val
            result.append(token * count)
            num %= val
        return "".join(result)

    def load_sudoku_puzzles(self, filename:str) -> list[list[list[int]]]:
        """
        Generates a list of all the sudoku puzzles in a given text file
        """
        puzzles = []
        current_grid = []
        with open(filename, "r") as file:
            for line in file:
                line = line.strip()
                if line.startswith("Grid"):
                    if current_grid:
                        puzzles.append(current_grid)
                        current_grid = []
                elif line:  # Avoid empty lines
                    current_grid.append([int(char) for char in line])
        if current_grid:
            puzzles.append(current_grid)
            
        return puzzles

    def solve_sudoku(self, grid:list):
        """
        Solves the sudoku puzzles from the list given from self.load_sudoku_puzzles()
        """
        def is_valid(grid, r:int, c:int, num:int):
            # Check row
            if num in grid[r]:
                return False
                
            # Check column
            if num in [grid[i][c] for i in range(9)]:
                return False
                
            # Check 3x3 box
            box_r, box_c = (r // 3) * 3, (c // 3) * 3
            for i in range(box_r, box_r + 3):
                for j in range(box_c, box_c + 3):
                    if grid[i][j] == num:
                        return False
                        
            return True

        for r in range(9):
            for c in range(9):
                if grid[r][c] == 0:
                    for num in range(1, 10):
                        if is_valid(grid, r, c, num):
                            grid[r][c] = num
                            
                            if self.solve_sudoku(grid):
                                return True
                                
                            grid[r][c] = 0  # Backtrack
                    return False
        return True

    def count_divisors_n_squared(self, n:int) -> int:
        """Calculates the number of divisors of n^2 using prime factorization."""
        divisors = 1
        d = 2
        while d * d <= n:
            if n % d == 0:
                count = 0
                while n % d == 0:
                    count += 1
                    n //= d
                # If p^count divides n, then p^(2*count) divides n^2
                divisors *= (2 * count + 1)
            d += 1
        if n > 1:
            # Remaining prime factor has an exponent of 1
            divisors *= (2 * 1 + 1)
        return divisors
