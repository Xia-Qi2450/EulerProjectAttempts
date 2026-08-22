"""
Project Euler solutions: problem101 through problem125.

Problems101To125 is combined into EulerSolver in solver.py. It
genuinely inherits from UtilsMixin and EasterEggs since these problems
call self.header, self.run_task,  
and so on.
"""

import math
import itertools
import collections
import fractions

from colorama import Fore

from .utils import UtilsMixin
from .easter_eggs import EasterEggs

class Problems101To125(UtilsMixin, EasterEggs):
    """Problem solutions 101-125."""

    def problem101(self):
        "Find the sum of First Incorrect Terms (FITs) for optimum polynomials approximating a 10th-degree polynomial sequence."
        self.header(
            101,
            "Find the sum of First Incorrect Terms (FITs) for optimum polynomials approximating a 10th-degree polynomial sequence."
        )
        def u(n):
            """Generates the true n-th term of the 10th-degree polynomial sequence."""
            return sum((-1)**i * (n**i) for i in range(11))        
        def get_lagrange_val(points, x):
            """
            Evaluates the Lagrange interpolating polynomial 
            passing through 'points' at a given 'x'.
            """
            total = fractions.Fraction(0)
            k = len(points)
            for i in range(k):
                xi, yi = points[i]
                num, den = 1, 1
                for j in range(k):
                    if i != j:
                        xj, _ = points[j]
                        num *= (x - xj)
                        den *= (xi - xj)
                total += yi * fractions.Fraction(num, den)
            return total        
        def solve():
            # Precompute the first 11 terms of the true sequence
            true_terms = [u(n) for n in range(1, 12)]
            sum_of_fits = 0
            
            for k in range(1, 11):
                # Gather the first k known data points (n, u_n)
                points = [(n, true_terms[n - 1]) for n in range(1, k + 1)]
                fit_value = get_lagrange_val(points, k + 1)
                sum_of_fits += fit_value
            return int(sum_of_fits)
        result = self.run_task(
            "Evaluating Lagrange interpolating polynomials...",
            solve
        )
        print(f"The sum of First Incorrect Terms (FITs) is: {Fore.GREEN}{result}{Fore.RESET}")

    def problem102(self):
        "Find how many of the 1,000 given triangles in 0102_triangles.txt contain the origin (0, 0)"
        self.header(
            102,
            "Find how many of the 1,000 given triangles in 0102_triangles.txt contain the origin (0, 0)"
        )
        def is_origin_inside(x1, y1, x2, y2, x3, y3):
            # Using the area / barycentric sign method for point (0, 0)
            # The total area/sign determinant components relative to the origin
            def sign(p1x, p1y, p2x, p2y):
                return p1x * p2y - p2x * p1y
            b1 = sign(x1, y1, x2, y2) < 0
            b2 = sign(x2, y2, x3, y3) < 0
            b3 = sign(x3, y3, x1, y1) < 0
            # If all signs are the same (all true or all false depending on vertex order),
            # then the origin (0,0) is strictly inside the triangle.
            return (b1 == b2) and (b2 == b3)
        def solve():
            count = 0
            with open("0102_triangles.txt", "r") as f:
                for line in f:
                    if not line.strip():
                        continue
                    coords = list(map(int, line.strip().split(",")))
                    x1, y1, x2, y2, x3, y3 = coords
                    if is_origin_inside(x1, y1, x2, y2, x3, y3):
                        count += 1
            return count
        result = self.run_task(
            "Ploting triangles...",
            solve
        )
        print(f"The number of triangles that contain the origin is: {Fore.GREEN}{result}{Fore.RESET}")


    def problem103(self):
        "Find the optimum special sum set for n = 7 and return its elements concatenated as a string."
        self.header(
            103,
            "Find the optimum special sum set for n = 7 and return its elements concatenated as a string."
        )
        def is_special_sum_set(s):
            """
            Checks if a sorted tuple/list satisfies the special sum set properties.
            """
            n = len(s)
            # Rule 2 check: If B has more elements than C, S(B) > S(C).
            for k in range(1, (n + 1) // 2):
                if sum(s[:k+1]) <= sum(s[-k:]):
                    return False
                    
            # Rule 1 check: Unique subset sums.
            # Since Rule 2 is met, we track sums to ensure no duplicates exist.
            seen_sums = set()
            # Generate all non-empty subsets
            for r in range(1, n + 1):
                for subset in itertools.combinations(s, r):
                    sub_sum = sum(subset)
                    if sub_sum in seen_sums:
                        return False
                    seen_sums.add(sub_sum)
                    
            return True
        def solve():
            near_optimum = [20, 31, 38, 39, 40, 42, 45]
            
            best_sum = float('inf')
            best_set = None
            search_ranges = [range(x - 3, x + 4) for x in near_optimum]
            
            # Generate candidate sets from the search space
            for candidate in itertools.product(*search_ranges):
                if all(candidate[i] < candidate[i+1] for i in range(len(candidate)-1)):
                    current_sum = sum(candidate)
                    if current_sum < best_sum:
                        if is_special_sum_set(candidate):
                            best_sum = current_sum
                            best_set = candidate
            # Format the elements into a single string concatenation 
            return "".join(map(str, best_set)), best_set
        result, result_set = self.run_task(
            "Looking through sets...",
            solve
        )
        print(f"The optimum special sum set for n = 7 is: {Fore.GREEN}{result_set}{Fore.RESET}")
        print(f"With the concatenated string being: {Fore.GREEN}{result}{Fore.RESET}")

    def problem104(self):
        "Find the first Fibonacci number index for which both the first nine digits and the last nine digits are 1-9 pandigital."
        def is_pandigital_9(s):
            return "".join(sorted(str(s))) == "123456789"
        def solve():
            mod = 10**9
            a, b = 1, 1
            # F_1 = 1, F_2 = 1, so start index at 3
            k = 3
            
            # Precompute actual full values for a and b up to current index if needed,
            # or just keep exact bigints alongside mod ints.
            # Let's track exact F_{k-1} and F_k using bigints (fa, fb) 
            # and their suffixes (a, b) simultaneously.
            fa, fb = 1, 1
            while True:
                # Next Fibonacci value (exact bigint)
                fc = fa + fb
                fa, fb = fb, fc
                # Next Fibonacci value modulo 10^9 (tail suffix)
                c = (a + b) % mod
                a, b = b, c
                if is_pandigital_9(c):
                    # Check if the leading 9 digits of the exact number fc are pandigital
                    s = str(fc)
                    if is_pandigital_9(s[:9]):
                        return k
                k += 1
        result = self.run_task(
            "Looking through the Fibonacci squence...",
            solve
        )
        print(f"The first Fibonacci number index or which both the first nine digits and the last nine digits are 1-9 pandigital is: {Fore.GREEN}{result}{Fore.RESET}")


    def problem105(self):
        "Find the sum of the element totals of sets matching the special subset sum criteria from a provided file"
        self.header(
            105,
            "Find the sum of the element totals of sets matching the special subset sum criteria from a provided file"
        )
        def is_special_sum_set(s):
            s = sorted(s)
            # Rule 2: Optimal subset sum checks
            n = len(s)
            for i in range(1, n // 2 + 1):
                if sum(s[:i+1]) <= sum(s[-i:]): return False
            
            # Rule 1: Generate all subset sums to ensure uniqueness
            sums = {0}
            for x in s:
                new_sums = set()
                for current_sum in sums:
                    new_val = current_sum + x
                    if new_val in sums: return False
                    new_sums.add(new_val)
                sums.update(new_sums)
            return True
        def solve():
            # Load sets from 0105_sets.txt or pass them as a list of lists
            with open("0105_sets.txt", "r") as f:
                sets_data = [
                    [int(x) for x in line.strip().split(",")]
                    for line in f
                ]
            total_score = sum(
                sum(s)
                for s in sets_data
                if is_special_sum_set(s)
            )
            return total_score
        result = self.run_task(
            "Looking for special sums...",
            solve
        )
        print(f"The sum of the sets matching the special sum is: {Fore.GREEN}{result}{Fore.RESET}")


    def problem106(self):
        "Find how many equal-sized, disjoint subset pairs must be tested to verify a special sum set for n=12."
        self.header(
            106,
            "Find how many equal-sized, disjoint subset pairs must be tested to verify a special sum set for n=12."
        )
        def check_pairs(subset1, subset2):
            # Returns True if we actually need to test equality because 
            # relative element order doesn't dictate which sum is larger.
            gt = 0
            lt = 0
            for a, b in zip(subset1, subset2):
                if a > b:
                    gt += 1
                elif a < b:
                    lt += 1
            return gt > 0 and lt > 0
        def solve(n):
            total_tests = 0
            # Subsets must be of the same size r >= 2
            for r in range(2, n // 2 + 1):
                # Generate all choices of 2*r elements out of n, represented by indices 0..n-1
                for indices in itertools.combinations(range(n), 2 * r):
                    # Split the 2*r indices into two subsets of size r
                    # Fix the first element in subset1 to avoid duplicate symmetric pairs
                    for rest in itertools.combinations(indices[1:], r - 1):
                        sub1 = (indices[0],) + rest
                        sub2 = tuple(x for x in indices if x not in sub1)
                        # Ensure they are disjoint and ordered to prevent overcounting
                        if sub1[0] < sub2[0]:
                            # Check if they need explicit sum comparison
                            if check_pairs(sub1, sub2):
                                total_tests += 1
                                
            return total_tests
        result = self.run_task(
            "Comparing subset pairs...",
            solve,
            12
        )
        print(f"The number of equal-sized, disjoint subset pairs is: {Fore.GREEN}{result}{Fore.RESET}")

    def problem107(self):
        "Find the maximum weight reduction by finding the Minimum Spanning Tree of the network."
        self.header(
            107,
            "Find the maximum weight reduction by finding the Minimum Spanning Tree of the network."
        )
        def solve():
            edges = []
            total_weight = 0
            with open("0107_network.txt", "r") as f:
                matrix_lines = [
                    line.strip().split(",")
                    for line in f
                ]
            n = len(matrix_lines)
            
            # Parse adjacency matrix and collect unique edges
            for i in range(n):
                row = matrix_lines[i]
                for j in range(i + 1, n):
                    val = row[j]
                    if val != '-':
                        weight = int(val)
                        edges.append((weight, i, j))
                        total_weight += weight
                        
            # Sort edges by weight for Kruskal's algorithm
            edges.sort()
            
            # Disjoint Set Union (DSU) structure
            parent = list(range(n))
            def find(i):
                path = []
                while parent[i] != i:
                    path.append(i)
                    i = parent[i]
                for node in path:
                    parent[node] = i
                return i

            mst_weight = 0
            num_edges = 0
            
            for weight, u, v in edges:
                root_u = find(u)
                root_v = find(v)
                if root_u != root_v:
                    parent[root_u] = root_v
                    mst_weight += weight
                    num_edges += 1
                    if num_edges == n - 1:
                        break
                        
            return total_weight - mst_weight
        result = self.run_task(
            "Spanning the network...",
            solve
        )
        print(f"The maximum weight reduction in the network is: {Fore.GREEN}{result}{Fore.RESET}")

    def problem108(self):
        "Find the least value of n for which the equation 1/x + 1/y = 1/n has over 1000 distinct solutions."
        self.header(
            108,
            "Find the least value of n for which the equation 1/x + 1/y = 1/n has over 1000 distinct solutions."
        )
        def solve():
            # We step by 180 because highly composite numbers meeting this condition 
            # must be multiples of small highly divisible numbers (like 2 * 3 * 5 * 6 = 180)
            n = 180 
            while True:
                # Total unique solutions formula: (d(n^2) + 1) // 2
                if (self.count_divisors_n_squared(n) + 1) // 2 > 1000:
                    return n
                n += 180
        result = self.run_task(
            "Counting divisors...",
            solve
        )
        print(f"The least value of n is: {Fore.GREEN}{result}{Fore.RESET}")

    def problem109(self):
        "Find the total number of distinct dart checkouts with a score strictly less than 100."
        self.header(
            109,
            "Find the total number of distinct dart checkouts with a score strictly less than 100."
        )
        def solve(max_score=100):
            # Define all regions for individual dart throws
            singles = [i for i in range(1, 21)] + [25]
            doubles = [i * 2 for i in range(1, 21)] + [50]
            triples = [i * 3 for i in range(1, 21)]
            
            # Combined pool for the first two darts (including a 0 point miss)
            first_two_pool = singles + doubles + triples + [0]
            
            # The final checkout dart MUST be a double
            checkout_pool = doubles
            checkout_count = 0
            num_elements = len(first_two_pool)
            
            # Iterate through all valid combination pairs for the first 2 darts
            for i in range(num_elements):
                for j in range(i, num_elements):
                    score1 = first_two_pool[i]
                    score2 = first_two_pool[j]
                    
                    # Iterate through all possible finishing doubles
                    for score3 in checkout_pool:
                        total_score = score1 + score2 + score3
                        
                        # Check if total checkout score is strictly less than 100
                        if total_score < max_score:
                            checkout_count += 1
                            
            return checkout_count
        result = self.run_task(
            "Simulating dart throws...",
            solve
        )
        print(f"The total number of distict dart checkouts is: {Fore.GREEN}{result}{Fore.RESET}")

    def problem110(self):
        "Find the least value of n for which the number of distinct solutions to 1/x + 1/y = 1/n exceeds four million."
        self.header(
            110,
            "Find the least value of n for which the number of distinct solutions to 1/x + 1/y = 1/n exceeds four million."
        )
        def solve():
            # First 15 primes are enough since product of (2*a_i + 1) needs to exceed 8,000,000
            PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
            TARGET = 8_000_000  # 2 * 4,000,000

            min_n = float('inf')

            def search(index, current_n, current_divisors, max_exp):
                nonlocal min_n
                if current_divisors > TARGET:
                    if current_n < min_n:
                        min_n = current_n
                    return

                if index >= len(PRIMES):
                    return

                p = PRIMES[index]
                # Try decreasing exponents
                for exp in range(max_exp, -1, -1):
                    # Prevent overflow or unnecessary work if current_n already exceeds min_n
                    next_n = current_n * (p ** exp)
                    if next_n >= min_n:
                        continue
                    next_divisors = current_divisors * (2 * exp + 1)
                    search(index + 1, next_n, next_divisors, exp)

            search(0, 1, 1, 30)
            return min_n
        result = self.run_task(
            "Looking for the n...",
            solve
        )
        print(f"The least value of n is: {Fore.GREEN}{result}{Fore.RESET}")