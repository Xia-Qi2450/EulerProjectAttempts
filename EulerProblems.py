#!/usr/bin/env python3
import sys
import os
import time
import math
import random
import itertools
from collections import Counter
from typing import Any
import argparse
import shutil

# ===============
# Custom Errors
# ===============

class EulerProblemError(Exception):
    """Base exception for Project Euler errors."""

class EulerProblemNotImplemented(EulerProblemError):
    """When a Euler Problem is not implemented and it's being called."""
    def __init__(self, problem_no:int) -> None:
        message = f"Euler Problem number {problem_no} Has not been implemented yet."
        super().__init__(message)

class EulerProblemExecutionError(EulerProblemError):
    """When something weird happens during code execution."""
    def __init__(self, problem_no: int, error: Exception):
        self.problem_no = problem_no
        self.error = error

        super().__init__(
            f"Euler Problem {problem_no} failed during execution.\n"
            f"Caused by {type(error).__name__}: {error}"
        )

class RequiredModulesNotFound(Exception):
    """When required modules are not able to be imported due to it not being found."""
    def __init__(self, module) -> None:
        message = (
            f"The required module '{module}' for this script cannot be imported. "
            "Please install it via pip."
        )
        super().__init__(message)

class ImportModulesFail(Exception):
    """When importing modules fail to be imported."""
    def __init__(self, error) -> None:
        message = (
            f"An unexpected error occurred while trying to import the modules: {error}"
        )
        super().__init__(message)

# ===========================
# Try to import requirements
# ===========================

try:
    import colorama
    from colorama import Fore, Style
    from halo import Halo
except ModuleNotFoundError as e:
    raise RequiredModulesNotFound(e.name) from e
except Exception as e:
    raise ImportModulesFail(e) from e

class EulerSolver:
    """A collection of Project Euler solutions."""

    def __init__(self, easter_eggs=True, forced_easter_eggs = False):
        colorama.init(autoreset=True)
        self.VERSION = "0.5"
        self.GOAL = "100"
        self.EASTER_EGGS = easter_eggs
        self.FORCED_EASTER_EGGS = forced_easter_eggs
        self._spinner_frames = itertools.cycle("|/-\\")
        self.terminal_width = shutil.get_terminal_size(fallback=(100, 24)).columns
        self.current_file = os.path.realpath(__file__)
        self.problem8_number = "7316717653133062491922511967442657474235534919493496983520312774506326239578318016984801869478851843858615607891129494954595017379583319528532088055111254069874715852386305071569329096329522744304355766896648950445244523161731856403098711121722383113622298934233803081353362766142828064444866452387493035890729629049156044077239071381051585930796086670172427121883998797908792274921901699720888093776657273330010533678812202354218097512545405947522435258490771167055601360483958644670632441572215539753697817977846174064955149290862569321978468622482839722413756570560574902614079729686524145351004748216637048440319989000889524345065854122758866688116427171479924442928230863465674813919123162824586178664583591245665294765456828489128831426076900422421902267105562632111110937054421750694165896040807198403850962455444362981230987879927244284909188845801561660979191338754992005240636899125607176060588611646710940507754100225698315520005593572972571636269561882670428252483600823257530420752963450"
        self.problem11_grid = "08 02 22 97 38 15 00 40 00 75 04 05 07 78 52 12 50 77 91 08\n49 49 99 40 17 81 18 57 60 87 17 40 98 43 69 48 04 56 62 00\n81 49 31 73 55 79 14 29 93 71 40 67 53 88 30 03 49 13 36 65\n52 70 95 23 04 60 11 42 69 24 68 56 01 32 56 71 37 02 36 91\n22 31 16 71 51 67 63 89 41 92 36 54 22 40 40 28 66 33 13 80\n24 47 32 60 99 03 45 02 44 75 33 53 78 36 84 20 35 17 12 50\n32 98 81 28 64 23 67 10 26 38 40 67 59 54 70 66 18 38 64 70\n67 26 20 68 02 62 12 20 95 63 94 39 63 08 40 91 66 49 94 21\n24 55 58 05 66 73 99 26 97 17 78 78 96 83 14 88 34 89 63 72\n21 36 23 09 75 00 76 44 20 45 35 14 00 61 33 97 34 31 33 95\n78 17 53 28 22 75 31 67 15 94 03 80 04 62 16 14 09 53 56 92\n16 39 05 42 96 35 31 47 55 58 88 24 00 17 54 24 36 29 85 57\n86 56 00 48 35 71 89 07 05 44 44 37 44 60 21 58 51 54 17 58\n19 80 81 68 05 94 47 69 28 73 92 13 86 52 17 77 04 89 55 40\n04 52 08 83 97 35 99 16 07 97 57 32 16 26 26 79 33 27 98 66\n88 36 68 87 57 62 20 72 03 46 33 67 46 55 12 32 63 93 53 69\n04 42 16 73 38 25 39 11 24 94 72 18 08 46 29 32 40 62 76 36\n20 69 36 41 72 30 23 88 34 62 99 69 82 67 59 85 74 04 36 16\n20 73 35 29 78 31 90 01 74 31 49 71 48 86 81 16 23 57 05 54\n01 70 54 71 83 51 54 69 16 92 33 48 61 43 52 01 89 19 67 48"
        self.problem13_numbers = """37107287533902102798797998220837590246510135740250
                                    46376937677490009712648124896970078050417018260538
                                    74324986199524741059474233309513058123726617309629
                                    91942213363574161572522430563301811072406154908250
                                    23067588207539346171171980310421047513778063246676
                                    89261670696623633820136378418383684178734361726757
                                    28112879812849979408065481931592621691275889832738
                                    44274228917432520321923589422876796487670272189318
                                    47451445736001306439091167216856844588711603153276
                                    70386486105843025439939619828917593665686757934951
                                    62176457141856560629502157223196586755079324193331
                                    64906352462741904929101432445813822663347944758178
                                    92575867718337217661963751590579239728245598838407
                                    58203565325359399008402633568948830189458628227828
                                    80181199384826282014278194139940567587151170094390
                                    35398664372827112653829987240784473053190104293586
                                    86515506006295864861532075273371959191420517255829
                                    71693888707715466499115593487603532921714970056938
                                    54370070576826684624621495650076471787294438377604
                                    53282654108756828443191190634694037855217779295145
                                    36123272525000296071075082563815656710885258350721
                                    45876576172410976447339110607218265236877223636045
                                    17423706905851860660448207621209813287860733969412
                                    81142660418086830619328460811191061556940512689692
                                    51934325451728388641918047049293215058642563049483
                                    62467221648435076201727918039944693004732956340691
                                    15732444386908125794514089057706229429197107928209
                                    55037687525678773091862540744969844508330393682126
                                    18336384825330154686196124348767681297534375946515
                                    80386287592878490201521685554828717201219257766954
                                    78182833757993103614740356856449095527097864797581
                                    16726320100436897842553539920931837441497806860984
                                    48403098129077791799088218795327364475675590848030
                                    87086987551392711854517078544161852424320693150332
                                    59959406895756536782107074926966537676326235447210
                                    69793950679652694742597709739166693763042633987085
                                    41052684708299085211399427365734116182760315001271
                                    65378607361501080857009149939512557028198746004375
                                    35829035317434717326932123578154982629742552737307
                                    94953759765105305946966067683156574377167401875275
                                    88902802571733229619176668713819931811048770190271
                                    25267680276078003013678680992525463401061632866526
                                    36270218540497705585629946580636237993140746255962
                                    24074486908231174977792365466257246923322810917141
                                    91430288197103288597806669760892938638285025333403
                                    34413065578016127815921815005561868836468420090470
                                    23053081172816430487623791969842487255036638784583
                                    11487696932154902810424020138335124462181441773470
                                    63783299490636259666498587618221225225512486764533
                                    67720186971698544312419572409913959008952310058822
                                    95548255300263520781532296796249481641953868218774
                                    76085327132285723110424803456124867697064507995236
                                    37774242535411291684276865538926205024910326572967
                                    23701913275725675285653248258265463092207058596522
                                    29798860272258331913126375147341994889534765745501
                                    18495701454879288984856827726077713721403798879715
                                    38298203783031473527721580348144513491373226651381
                                    34829543829199918180278916522431027392251122869539
                                    40957953066405232632538044100059654939159879593635
                                    29746152185502371307642255121183693803580388584903
                                    41698116222072977186158236678424689157993532961922
                                    62467957194401269043877107275048102390895523597457
                                    23189706772547915061505504953922979530901129967519
                                    86188088225875314529584099251203829009407770775672
                                    11306739708304724483816533873502340845647058077308
                                    82959174767140363198008187129011875491310547126581
                                    97623331044818386269515456334926366572897563400500
                                    42846280183517070527831839425882145521227251250327
                                    55121603546981200581762165212827652751691296897789
                                    32238195734329339946437501907836945765883352399886
                                    75506164965184775180738168837861091527357929701337
                                    62177842752192623401942399639168044983993173312731
                                    32924185707147349566916674687634660915035914677504
                                    99518671430235219628894890102423325116913619626622
                                    73267460800591547471830798392868535206946944540724
                                    76841822524674417161514036427982273348055556214818
                                    97142617910342598647204516893989422179826088076852
                                    87783646182799346313767754307809363333018982642090
                                    10848802521674670883215120185883543223812876952786
                                    71329612474782464538636993009049310363619763878039
                                    62184073572399794223406235393808339651327408011116
                                    66627891981488087797941876876144230030984490851411
                                    60661826293682836764744779239180335110989069790714
                                    85786944089552990653640447425576083659976645795096
                                    66024396409905389607120198219976047599490197230297
                                    64913982680032973156037120041377903785566085089252
                                    16730939319872750275468906903707539413042652315011
                                    94809377245048795150954100921645863754710598436791
                                    78639167021187492431995700641917969777599028300699
                                    15368713711936614952811305876380278410754449733078
                                    40789923115535562561142322423255033685442488917353
                                    44889911501440648020369068063960672322193204149535
                                    41503128880339536053299340368006977710650566631954
                                    81234880673210146739058568557934581403627822703280
                                    82616570773948327592232845941706525094512325230608
                                    22918802058777319719839450180888072429661980811197
                                    77158542502016545090413245809786882778948721859617
                                    72107838435069186155435662884062257473692284509516
                                    20849603980134001723930671666823555245252804609722
                                    53503534226472524250874054075591789781264330331690"""
        self.problem18triangle = [
            [75],
            [95, 64],
            [17, 47, 82],
            [18, 35, 87, 10],
            [20,  4, 82, 47, 65],
            [19,  1, 23, 75,  3, 34],
            [88,  2, 77, 73,  7, 63, 67],
            [99, 65,  4, 28,  6, 16, 70, 92],
            [41, 41, 26, 56, 83, 40, 80, 70, 33],
            [41, 48, 72, 33, 47, 32, 37, 16, 94, 29],
            [53, 71, 44, 65, 25, 43, 91, 52, 97, 51, 14],
            [70, 11, 33, 28, 77, 73, 17, 78, 39, 68, 17, 57],
            [91, 71, 52, 38, 17, 14, 91, 43, 58, 50, 27, 29, 48],
            [63, 66,  4, 68, 89, 53, 67, 30, 73, 16, 69, 87, 40, 31],
            [4, 62, 98, 27, 23,  9, 70, 98, 73, 93, 38, 53, 60,  4, 23]
        ]

    # ==========================================================
    # Helper Methods
    # ==========================================================

    def header(self, problem_number, description: str) -> None:
        """Print a formatted problem header."""
        print(f"\nEuler's problem {problem_number}: {Fore.BLUE}{description}")

    def run_task(self, text: str, function, *args) -> Any:
        """Run a function with a Halo spinner and timer."""
        spinner = Halo(text=text, spinner="bouncingBar")
        start = time.time()
        spinner.start()
        time.sleep(0.5)
        result = function(*args)

        spinner.succeed(f"DONE! {Style.DIM}({time.time() - 0.5 - start:.4f}s){Style.NORMAL}")
        return result
    
    def list_problems(self, print_out=True) -> list:
        """List every implemented Project Euler problem."""
        if print_out:
            print(f"{Fore.CYAN}Implemented Problems{Fore.RESET}\n")

        methods = sorted(
            (
                name for name in dir(self)
                if name.startswith("problem") and name[7:].isdigit()
            ),
            key=lambda name: int(name[7:])
        )
        if print_out :
            for name in methods:
                method = getattr(self, name)
                description = (method.__doc__ or "No description").strip()
                print(f"{Fore.GREEN}{int(name[7:]):>3}{Fore.RESET} - {description}")
        return methods

    def _typewriter(self, text: str, delay: float = 0.03, newline: bool = True):
        """Print text progressively like a dialogue box."""

        pauses = {
            ".": 0.35,
            "!": 0.35,
            "?": 0.35,
            ",": 0.15,
            ":": 0.20,
        }

        for char in text:
            print(char, end="", flush=True)

            time.sleep(pauses.get(char, delay))

        if newline:
            print()

    def _load(self, text:str, finish_text:str ,duration:float, fail:bool = False):
        spinner_interval = 0.25
        spinner = Halo(text, spinner="bouncingBar")
        spinner.start()
        frames = [f"{text}.", f"{text}..", f"{text}..."]
        i = 0
        while True:
            spinner.text = frames[i % len(frames)]
            i += 1
            time.sleep(spinner_interval)
            if i*spinner_interval >= duration:
                break
        match fail:
            case False:
                spinner.succeed(f"{finish_text} {Style.DIM}(?.??s){Style.NORMAL}")
            case True:
                spinner.fail(f"{finish_text} {Style.DIM}(?.??s){Style.NORMAL}")

    def _wait(self, custom_text:str="[Press Enter to continue]"):
        input(f"{Fore.LIGHTBLACK_EX}{custom_text}{Fore.RESET}")

    def _progress_bar(self, current, total, title="Progress", bar_length=30):
        """
        Render a single-line progress bar to stdout.
    
        Format:
            {spinning_bar} {title}: [#######          ] {current}/{total} {percentage}%
    
        Call this repeatedly with an increasing `current` value. It automatically
        prints a trailing newline once current reaches total.
        """
        total = max(total, 1)  # avoid div by zero
        percent = (current / total) * 100
        filled = int(bar_length * current // total)
        bar = "#" * filled + " " * (bar_length - filled)
        spin = next(self._spinner_frames) if current < total else "#"
    
        sys.stdout.write(f"\r{spin} {title}: [{bar}] {current}/{total} {percent:.0f}%")
        sys.stdout.flush()
    
        if current >= total:
            sys.stdout.write("\n")
 

    # ==========================================================
    # Utility Functions
    # ==========================================================

    def find_all_squares_until(self, limit:int):
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
    
    def is_prime(self, n) -> bool:
        """Checks if a number is prime."""
        if n < 2:
            return False
        for i in range(2, int(math.isqrt(n)) + 1):
            if n % i == 0:
                return False
        return True

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
                if self.is_palindrome_str(product):
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
    
    def grid_adjacent_digit_multiplier(self, grid):
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
    
    def count_divisors(self, n):
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
    
    def count_lattice_paths(self, grid_size):
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
    
    def number_to_words(self, n):
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
    
    def solve_maximum_path(self, triangle):
        "Returns the path with the max value"
        # Iterate from the second-to-last row up to the top row (row index 0)
        for row in reversed(range(len(triangle) - 1)):
            for col in range(len(triangle[row])):
                max_child = max(triangle[row + 1][col], triangle[row + 1][col + 1])
                triangle[row][col] += max_child
                
        return triangle[0][0]
    
    def is_leap_year(self, year):
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
    
    def sum_proper_divisors(self, n):

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

    def has_pandigital_product(self, n):
        # Find all factors of the product n
        for i in range(1, math.isqrt(n) + 1):
            if n % i == 0:
                identity_str = f"{i}{n // i}{n}"
                if len(identity_str) == 9 and "".join(sorted(identity_str)) == "123456789":
                    return True
        return False

    def word_value(self, word) -> int:
        """Calculate the sum of letter positions (A=1, B=2, etc.)."""
        return sum(ord(char) - ord('A') + 1 for char in word)

    def is_triangle(self, n) -> bool:
        """Check if n is a triangle number using 8n + 1 perfect square test."""
        root = math.isqrt(8 * n + 1)
        return root * root == 8 * n + 1 and root % 2 == 1

    def is_substring_divisible(self, num) -> bool:
        primes = [2, 3, 5, 7, 11, 13, 17]
        for i, p in enumerate(primes):
            # Extract 3-digit substring starting at index i + 1
            sub = num[i + 1] * 100 + num[i + 2] * 10 + num[i + 3]
            if sub % p != 0:
                return False
        return True

    def is_pentagonal(self, n) -> bool:
        # Check if n is a pentagonal number using the inverse formula
        # P_k = k(3k - 1)/2 => 3k^2 - k - 2P = 0
        # k = (1 + sqrt(1 + 24 * n)) / 6
        temp = (1 + (1 + 24 * n) ** 0.5) / 6
        return temp.is_integer()

    # ==========================================================
    # Easter Eggs
    # ==========================================================

    def _try_easter_egg(self, problem: int) -> bool:
        if not self.FORCED_EASTER_EGGS:
            if not self.EASTER_EGGS or random.randrange(100) != problem % 100:
                return False

        easter_eggs = {
            5: self.nakano5,
            39: self.miku39,
            41: self.teto41,
        }

        egg = easter_eggs.get(problem)
        if egg:
            egg()
            return True

        return False

    def nakano5(self):
        """
        Display the hidden Project Euler Problem 5 easter egg.
        
        This easter egg has a 1% chance of appearing when Problem 5
        is executed unless disabled with --no-easter-eggs.
        
        Who know why quintuplets could be so amazing?
        """
        # TODO: Make a Quintessential Quintuplets easter egg here!

    def miku39(self):
        """
        Display the hidden Project Euler Problem 39 easter egg.

        This easter egg has a 1% chance of appearing when Problem 39
        is executed unless disabled with --no-easter-eggs.

        Crypton, please don't sue me.
        """
        print(Fore.CYAN + "=" * self.terminal_width)
        print(f"{Fore.YELLOW}/// WARNING ///{Fore.RESET}")
        print()
        self._typewriter("An unexpected route has been discovered.")
        time.sleep(0.2)
        self._load("Loading hidden problem", "DONE!", 1.2)
        self._wait()

        self.header(
            "39?",
            "Find the world's greatest virtual singer."
        )
        result = self.run_task(
            "Finding the world's greatest virtual singer...",
            lambda: "Hatsune Miku"
        )
        self._typewriter(
            f"The world's greatest virtual singer is: ",
            newline=False
        )
        print(f"{Fore.GREEN}{result}{Fore.RESET}")
        self._wait()
        total = random.randint(50,200)
        i = 0
        while i < total:
            self._progress_bar(i, total, title="GET miku.py")
            i += random.randint(0,5)
            time.sleep(0.1)
        i = None
        self._load("Verifying", "Something went wrong...", 5, True)
        time.sleep(1)
        self._typewriter("She is in your computer...")
        self._wait("[???]")
        self._typewriter("SHE IS HERE...", 0.1)
        self._wait("[What?]")
        print(f"Traceback (most recent call last):")
        print(f"  File \"{self.current_file}\", line {Fore.RED}1526{Fore.RESET}, in {Fore.RED}problem39{Fore.RESET}")
        print(f"    {Fore.MAGENTA}self.miku39{Fore.RED}(){Fore.RESET}")
        print(f"    {Fore.MAGENTA}~~~~~~~~~~~{Fore.RED}^^{Fore.RESET}")
        print(f"  File \"{self.current_file}\", line {Fore.RED}729{Fore.RESET}, in {Fore.RED}miku39{Fore.RESET}")
        print(f"    {Fore.MAGENTA}miku.start_runtime{Fore.RED}(){Fore.RESET}")
        print(f"    {Fore.MAGENTA}~~~~~~~~~~~~~~~~~~{Fore.RED}^^{Fore.RESET}")
        print(f"  File \"<miku_runtime>\", line {Fore.RED}???{Fore.RESET}, in {Fore.RED}try_install{Fore.RESET}")
        print(f"    {Fore.MAGENTA}Ȗũï{Fore.RED}Ž{Fore.MAGENTA}ǧÉƱɺħ￿ØɃ{Fore.RED}ţʢɠ{Fore.MAGENTA}ǙƶǙ￿¥{Fore.RED}ĭğ{Fore.MAGENTA}ɶȘƆÜǧ{Fore.RED}öʌɯʚȅ￿{Fore.MAGENTA}ŅŤɺģ¶{Fore.RESET}")
        print(f"    {Fore.MAGENTA}~~~{Fore.RED}^{Fore.MAGENTA}~~~~~~~~{Fore.RED}^^^{Fore.MAGENTA}~~~~~{Fore.RED}^^{Fore.MAGENTA}~~~~~{Fore.RED}^^^^^^{Fore.MAGENTA}~~~~~{Fore.RESET}")
        print(f"{Fore.MAGENTA}{Style.BRIGHT}MikuIsHidingInYourWiFi{Fore.RESET}{Style.NORMAL}: {Fore.RED}Thank you(39) for using EulerProblems.py, ありがとうございます。{Fore.RESET}")
        input()
        with open("miku.txt", "w") as f:
            f.write("[Intro] \nOoh-ee-ooh \nOoh-ee-ooh \nOoh-ee-ooh \nOoh-ee-ooh \n\n[Verse 1] \nMiku, Miku, you can call me Miku \nBlue hair, blue tie, hiding in your Wi-Fi \nOpen secrets, anyone can find me \nHear your music running through my mind \n\n[Chorus] \nI'm thinkin' Miku, Miku (Ooh-ee-ooh) \nI'm thinkin' Miku, Miku (Ooh-ee-ooh) \nI'm thinkin' Miku, Miku (Ooh-ee-ooh) \nI'm thinkin' Miku, Miku (Ooh-ee-ooh) \n\n[Pre-Chorus] \nI'm on top of the world because of you \nAll I wanted to do is follow you \nI'll keep singing along to all of you \nI'll keep singing along \n\n[Chorus] \nI'm thinkin' Miku, Miku (Ooh-ee-ooh) \nI'm thinkin' Miku, Miku (Ooh-ee-ooh) \nI'm thinkin' Miku, Miku (Ooh-ee-ooh) \nI'm thinkin' Miku, Miku (Ooh-ee-ooh) \n\n[Verse 2] \nMiku, Miku, what's it like to be you? \n20/20, looking in the rear view \nPlay me, break me, make me feel like Superman \nYou can do anything you want \n\n[Pre-Chorus] \nI'm on top of the world because of you \nAll I wanted to do is follow you \nI'll keep singing along to all of you \nI'll keep singing along \nI'm on top of the world because of you \nI do nothing that they could never do \nI'll keep playing along with all of you \nI'll keep playing along \n\n[Chorus] \nI'm thinkin' Miku, Miku (Ooh-ee-ooh) \nI'm thinkin' Miku, Miku (Ooh-ee-ooh) \nI'm thinkin' Miku, Miku (Ooh-ee-ooh) \nI'm thinkin' Miku, Miku (Ooh-ee-ooh) \n\n[Bridge] \nWhere were we walking together? \nI will see you in the end \nI'll take you where you've never been \nAnd bring you back again \nListen to me with your eyes \nI'm watching you from in the sky \nIf you forget, I'll fade away \nI'm asking you to let me stay \nSo bathe me in your magic light \nAnd keep it on in darkest night \nI need you here to keep me strong \nTo live my life and sing along \nI'm waiting with you wide awake \nLike your expensive poison snake \nYou found me here inside a dream \nWalk through the fire straight to me \n\n[Outro] \n​tsap eht morf dnuos tsal ,erutuf eht morf dnuos tsriF")
        self._load("Recovering", "Recovered! A txt file has been created.", 2)
        self._wait("[Continue to next problem]")
        print(Fore.CYAN + "=" * self.terminal_width)
    
    def teto41(self):
        """
        Display the hidden Project Euler Problem 41 easter egg.
        
        This easter egg has a 1% chance of appearing when Problem 41
        is executed unless disabled with --no-easter-eggs.
        
        Teto word of the day! Mathematics!
        """
        # TODO: Make a Kasane Teto easter egg here!

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
    
    def problem26(self):
        "Find the value of d < 1000 for which 1/d contains the longest recurring cycle in its decimal fraction part."
        self.header(
            26,
            "Find the value of d < 1000 for which 1/d contains the longest recurring cycle in its decimal fraction part."
        )
        def get_cycle_length(d):
            # Track the step/index at which each remainder was seen
            seen_remainders = {}
            remainder = 1
            step = 0
            while remainder != 0:
                if remainder in seen_remainders:
                    return step - seen_remainders[remainder]
                
                seen_remainders[remainder] = step
                remainder = (remainder * 10) % d
                step += 1
            return 0  # Divides evenly 
        
        def task():
            max_len = 0
            best_d = 0
            for d in range(2, 1000):
                length = get_cycle_length(d)
                if length > max_len:
                    max_len = length
                    best_d = d
            return best_d, max_len
        
        d_value, cycle_len = self.run_task(
            "Finding the largest recurring decimal...",
            task       
        )
        print(f"The value of d < 1000 with the longest cycle is: {Fore.GREEN}{d_value}{Fore.RESET}")
        print(f"Length of the cycle is: {Fore.GREEN}{cycle_len}{Fore.RESET}")
    
    def problem27(self):
        "Find the product of the coefficients a and b in the quadratic expression n^2 + an + b that yields the maximum number of consecutive primes, starting with n = 0"
        self.header(
            27,
            "Find the product of the coefficients a and b in the quadratic expression n^2 + an + b that yields the maximum number of consecutive primes, starting with n = 0"
        )
        def task():
            max_primes = 0
            best_a = 0
            best_b = 0
            for b in range(2, 1000):
                if not self.is_prime(b):
                    continue
                for a in range(-999, 1000):
                    n = 0
                    while True:
                        candidate = n**2 + a * n + b
                        if candidate <= 0 or not self.is_prime(candidate):
                            break
                        n += 1
                    if n > max_primes:
                        max_primes = n
                        best_a = a
                        best_b = b
            return best_a * best_b, best_a, best_b
        
        product, a, b = self.run_task(
            "Finding the coefficents and the product of the former...",
            task
        )
        print(f"The coefficients are: a = {Fore.GREEN}{a}{Fore.RESET}, b = {Fore.GREEN}{b}{Fore.RESET}")
        print(f"Product of coefficients (a * b) is: {Fore.GREEN}{product}{Fore.RESET}")

    def problem28(self):
        "Find the sum of the numbers on the diagonals in a 1001 by 1001 spiral"
        self.header(
            28,
            "Find the sum of the numbers on the diagonals in a 1001 by 1001 spiral"
        )
        def task(grid_size):
            total_sum = 1
            current_number = 1
            
            # Outer layers advance by 2 step sizes each time (2, 4, 6, ..., grid_size - 1)
            for step in range(2, grid_size, 2):
                for _ in range(4):
                    current_number += step
                    total_sum += current_number
                    
            return total_sum
        
        result = self.run_task(
            "Finding the sum...",
            task,
            1001
        )
        print(f"The sum of numbers on the diagonals is: {Fore.GREEN}{result}{Fore.RESET}")

    def problem29(self):
        "Find the number of distinct terms in the sequence generated by a^b for 2 <= a <= 100 and 2 <= b <= 100"
        self.header(
            29,
            "Find the number of distinct terms in the sequence generated by a^b for 2 <= a <= 100 and 2 <= b <= 100"
        )
        def task():
            # Use a set comprehension to automatically filter out duplicate values
            distinct_powers = {a**b for a in range(2, 101) for b in range(2, 101)}
            return len(distinct_powers)
        
        result = self.run_task(
            "Finding the number of distinct terms",
            task
        )
        print(f"The number of distict terms is: {Fore.GREEN}{result}{Fore.RESET}")
    
    def problem30(self):
        "Find the sum of all the numbers that can be written as the sum of fifth powers of their digits."
        self.header(
            30,
            "Find the sum of all the numbers that can be written as the sum of fifth powers of their digits."
        )
        def task():
            total_sum = 0
            upper_bound = 6 * (9 ** 5)
            for number in range(2, upper_bound + 1):
                digit_sum = sum(int(digit) ** 5 for digit in str(number))
                if digit_sum == number:
                    total_sum += number    
            return total_sum
        
        result = self.run_task(
            "Finding the sum...",
            task
        )
        print(f"The sum of all the numbers that can be written as the sum of fifth powers of there digits is: {Fore.GREEN}{result}{Fore.RESET}")

    def problem31(self):
        "Find the number of different ways can £2 be made using any number of coins?"
        self.header(
            31,
            "Find the number of different ways can £2 be made using any number of coins?"
        )
        def task():
            target = 200
            coins = [1, 2, 5, 10, 20, 50, 100, 200]
            
            # dp[i] will store the number of ways to form a target sum 'i'
            dp = [1] + [0] * target
            
            for coin in coins:
                for i in range(coin, target + 1):
                    dp[i] += dp[i - coin]
                    
            return dp[target]
        
        result = self.run_task(
            "Finding all the ways to make £2...",
            task
        )
        print(f"The total number of ways to make £2 is: {Fore.GREEN}{result}{Fore.RESET}")

    def problem32(self):
        "Find the sum of all products whose multiplicand/multiplier/product identity can be written as a 1 through 9 pandigital."
        self.header(
            32,
            "Find the sum of all products whose multiplicand/multiplier/product identity can be written as a 1 through 9 pandigital."
        )
        def task():
             # Store unique products to avoid counting duplicates
            unique_products = set()
            for product in range(1000, 10000):
                if self.has_pandigital_product(product):
                    unique_products.add(product)
            return sum(unique_products)

        result = self.run_task(
            "Finding the sum of the pandigital...",
            task
        )
        print(f"The sum of all products whose identities can be written as a 1 - 9 pandigital is: {Fore.GREEN}{result}{Fore.RESET}")

    def problem33(self):
        "Find the value of the denominator. If the product of these four fractions is given in its lowest common terms."
        self.header(
            33,
            "Find the value of the denominator. If the product of these four fractions is given in its lowest common terms."
        )
        def task():
            product_numerator = 1
            product_denominator = 1
            for d in range(10, 100):
                for n in range(10, d):
                    n1, n0 = n // 10, n % 10
                    d1, d0 = d // 10, d % 10
                    if n0 == 0 and d0 == 0:
                        continue
                    if n0 == d1 and (n * d0 == d * n1):
                        product_numerator *= n
                        product_denominator *= d
            final_denominator = product_denominator // math.gcd(product_numerator, product_denominator)
            return final_denominator
        result = self.run_task(
            "Finding the denominator...",
            task
        )
        print(f"The value of the denominator when the product of these four factions is given in its lowest common terms is: {Fore.GREEN}{result}{Fore.RESET}")

    def problem34(self):
        "Find the sum of all numbers which are equal to the sum of the factorial of their digits."
        self.header(
            34,
            "Find the sum of all numbers which are equal to the sum of the factorial of their digits."
        )
        def task():
            factorials = [math.factorial(i) for i in range(10)]
            def sum_of_digit_factorials(n):
                total = 0
                while n > 0:
                    total += factorials[n % 10]
                    n //= 10
                return total
            upper_limit = 7 * factorials[9]
            match_sum = 0
            for num in range(3, upper_limit + 1):
                if num == sum_of_digit_factorials(num):
                    match_sum += num
            return match_sum
        result = self.run_task(
            "Finding the sum...",
            task
        )
        print(f"The sum of all number that are equal to the sum of the factorial of their digits is: {Fore.GREEN}{result}{Fore.RESET}")

    def problem35(self):
        "Find the number of circular primes are there below one million."
        self.header(
            35,
            "Find the number of circular primes are there below one million."
        )
        def task():
            limit = 1_000_000
            is_prime_lookup = self.sieve_of_eratosthenes_list(limit)
            circular_prime_count = 0
            invalid_digits = {'0', '2', '4', '5', '6', '8'}
            for num in range(2, limit):
                if not is_prime_lookup[num]:
                    continue
                num_str = str(num)
                if len(num_str) > 1 and any(digit in invalid_digits for digit in num_str):
                    continue
                is_circular = True
                for i in range(len(num_str)):
                    rotation = int(num_str[i:] + num_str[:i])
                    if not is_prime_lookup[rotation]:
                        is_circular = False
                        break
                if is_circular:
                    circular_prime_count += 1    
            return circular_prime_count

        result = self.run_task(
            "Finding all circular primes under 1000000...",
            task
        )
        print(f"The number of circulat primes under one million is: {Fore.GREEN}{result}{Fore.RESET}")

    def problem36(self):
        "Find the sum of all numbers, less than one million, which are palindromic in base 10 and base 2."
        self.header(
            36,
            "Find the sum of all numbers, less than one million, which are palindromic in base 10 and base 2."
        )
        def task():
            total_sum = 0
            # Even numbers in binary always end in 0, so they cannot be base-2 palindromes (no leading zeros).
            # Thus, we only check odd numbers.
            for n in range(1, 1000000, 2):
                if self.is_palindrome(str(n)) and self.is_palindrome(bin(n)[2:]):
                    total_sum += n
            return total_sum
        result = self.run_task(
            "Finding the sum of all palindromic numbers...",
            task
        )
        print(f"The sum of all numbers, less than one million, which are palindromic in base 10 and base 2 is: {Fore.GREEN}{result}{Fore.RESET}")

    def problem37(self):
        "Find the sum of the only eleven primes that are both truncatable from left to right and right to left."
        self.header(
            37,
            "Find the sum of the only eleven primes that are both truncatable from left to right and right to left."
        )
        def task():
            limit = 1000000
            is_prime = self.sieve_of_eratosthenes_list(limit)

            def is_truncatable(n: int) -> bool:
                # Single-digit primes are excluded by problem definition
                if n < 10:
                    return False
                str_n = str(n)
                for i in range(1, len(str_n)):
                    if not is_prime[int(str_n[:i])] or not is_prime[int(str_n[i:])]:
                        return False
                return True
            truncatable_primes = []
            current_number = 11
            while len(truncatable_primes) < 11:
                if is_prime[current_number] and is_truncatable(current_number):
                    truncatable_primes.append(current_number)
                current_number += 2  # Skip even numbers to save time

            return sum(truncatable_primes)
        result = self.run_task(
            "Finding all truncateable primes...",
            task
        )
        print(f"The sum of the only eleven primes that are truncatable from left to right and right to left is: {Fore.GREEN}{result}{Fore.RESET}")

    def problem38(self):
        "Find the largest 1 to 9 pandigital 9-digit number that can be formed as the concatenated product of an integer with (1, 2,...,n) where n > 1."
        self.header(
            38,
            "Find the largest 1 to 9 pandigital 9-digit number that can be formed as the concatenated product of an integer with (1, 2,...,n) where n > 1."
        )
        def task():
            for num in range(9876, 9122, -1):
                concatenated = str(num) + str(2 * num)
                if len(set(concatenated)) == 9 and '0' not in concatenated:
                    return concatenated
        result = self.run_task(
            "Finding the number...",
            task
        )
        print(f"The largest 1 to 9 pandigital 9-digit number is: {Fore.GREEN}{result}{Fore.RESET}")

    def problem39(self):
        "Find the perimeter that maximizes the number of integer right-angled triangle solutions for p ≤ 1000"
        self.header(
            39,
            "Find the perimeter that maximizes the number of integer right-angled triangle solutions for p ≤ 1000"
        )
        if self._try_easter_egg(39):
            return
        def task(max_p=1000):
            perimeters = []
            for a in range(1, max_p // 3):
                for b in range(a, max_p // 2):
                    c_squared = a**2 + b**2
                    c = int(c_squared**0.5)
                    if c**2 == c_squared:
                        p = a + b + c
                        if p <= max_p:
                            perimeters.append(p)
            frequency_map = Counter(perimeters)
            most_common_p, max_solutions = frequency_map.most_common(1)[0]
            return most_common_p, max_solutions
        result, _max = self.run_task(
            "FInding the perimeter...",
            task
        )
        print(f"The perimeter that maximizes the number of integer right-angled triangle solutions is: {Fore.GREEN}{result}{Fore.RESET}")
        print(f"The max solutions it gives is: {Fore.GREEN}{_max}{Fore.RESET}")

    def problem40(self):
        "Find the product of specific positional digits in Champernowne's constant."
        self.header(
            40,
            "Find the product of specific positional digits in Champernowne's constant."
        )
        def task():
            champernowne_str = ""
            i = 1
            while len(champernowne_str) < 1000000:
                champernowne_str += str(i)
                i += 1
            product = 1
            for power in range(7):
                target_index = 10**power
                digit = int(champernowne_str[target_index - 1])
                product *= digit
            return product

        result = self.run_task(
            "Combing through Champernowne's Constant...",
            task
        )
        print(f"The product in Champernowne's constant is: {Fore.GREEN}{result}{Fore.RESET}")

    def problem41(self):
        "Find the largest n-digit pandigital prime that exists"
        self.header(
            41,
            "Find the largest n-digit pandigital prime that exists"
        )
        if self._try_easter_egg(41):
            return
        def task():
            # Start with 7 digits since 9 and 8 digit pandigitals are always divisible by 3
            digits = "7654321"
            for p in itertools.permutations(digits):
                num = int("".join(p))
                if self.is_prime(num):
                    return num
        result = self.run_task(
            "Finding the pandigital prime...",
            task
        )
        print(f"The largest pandigital prime that exists is: {Fore.GREEN}{result}{Fore.RESET}")

    def problem42(self):
        "Find the number of triangle words in a text file."
        self.header(
            42,
            "Find the number of triangle words in a text file."
        )
        def task():
            with open("0042_words.txt", "r") as f:
                content = f.read()
            # Clean up and split the CSV-style quoted words
            words = content.strip('"').split('","')
            triangle_count = sum(1 for w in words if self.is_triangle(self.word_value(w)))
            return triangle_count
        result = self.run_task(
            "Finding the number of triangle words...",
            task
        )
        print(f"The number of triangle words in the text file is: {Fore.GREEN}{result}{Fore.RESET}")

    def problem43(self):
        "Find the sum of all 0-to-9 pandigital numbers that have a specific sub-string divisibility property tested against the primes 2, 3, 5, 7, 11, 13, and 17"
        self.header(
            43,
            "Find the sum of all 0-to-9 pandigital numbers that have a specific sub-string divisibility property tested against the primes 2, 3, 5, 7, 11, 13, and 17"
        )
        def task():
            total_sum = 0
            # Generate all permutations of digits 0 through 9
            for p in itertools.permutations(range(10)):
                if p[0] == 0:
                    continue  # Not a valid 10-digit number if it starts with 0
                if self.is_substring_divisible(p):
                    number_val = int("".join(map(str, p)))
                    total_sum += number_val
            return total_sum
        result = self.run_task(
            "Finding the sum...",
            task
        )
        print(f"The sum of all 0-to-9 pandigital numbers that have a specific sub-string divisibility property tested against primes is: {Fore.GREEN}{result}{Fore.RESET}")

    def problem44(self):
        "Find the pair of pentagonal numbers with a pentagonal sum and difference that minimizes their difference."
        self.header(
            44,
            "Find the pair of pentagonal numbers with a pentagonal sum and difference that minimizes their difference."
        )
        def task():
            pentagons = []
            k = 1
            while True:
                pk = k * (3 * k - 1) // 2
                pentagons.append(pk)
                for j in range(k - 1, -1, -1):
                    pj = pentagons[j]
                    if self.is_pentagonal(pk - pj) and self.is_pentagonal(pk + pj):
                        return pk, pj, pk - pj
                k += 1
        num1, num2, result = self.run_task(
            "Finding the pair of pentagonal numbers...",
            task
        )
        print(f"The pair of pentagonal numbers with a pentagonal sum and difference that minimizes their difference are: {Fore.GREEN}{num1}{Fore.RESET} and {Fore.GREEN}{num2}{Fore.RESET}")
        print(f"The difference of the numbers is: {Fore.GREEN}{result}{Fore.RESET}")

    def problem45(self):
        "Find the next triangle number that is also pentagonal and hexagonal."
        self.header(
            45,
            "Find the next triangle number that is also pentagonal and hexagonal."
        )
        def task():
            n = 143
            while True:
                n += 1
                h = n * (2 * n - 1)
                # Check if h is pentagonal: (sqrt(24h + 1) + 1) / 6 must be an integer
                p_discriminant = (24 * h + 1) ** 0.5
                if p_discriminant.is_integer() and (p_discriminant + 1) % 6 == 0:
                    return h
        result = self.run_task(
            "Finding the triangle number that is also pentagonal and hexagonal...",
            task          
        )
        print(f"The next triangle number that is booth pentagonal and hexagonal is: {Fore.GREEN}{result}{Fore.RESET}")

    def problem46(self):
        "Find the smallest odd composite that cannot be written as the sum of a prime and twice a square."
        self.header(
            46,
            "Find the smallest odd composite that cannot be written as the sum of a prime and twice a square."
        )
        def task():
            primes = [2]
            n = 3
            while True:
                if self.is_prime(n):
                    primes.append(n)
                else:
                    falsified = True
                    for p in primes:
                        if p >= n:
                            break
                        remainder = (n - p) // 2
                        root = math.isqrt(remainder)
                        if root * root == remainder:
                            falsified = False
                            break
                    if falsified:
                        return n
                n += 2 
        result = self.run_task(
            "Combing through odd numbers...",
            task
        )
        print(f"The smallest odd composite that satisfies the conditions is: {Fore.GREEN}{result}{Fore.RESET}")

    def problem47(self):
        "Find the first four consecutive integers to have four distinct prime factors each."
        self.header(
            47,
            "Find the first four consecutive integers to have four distinct prime factors each."
        )
        def task(limit=200_000):
            counts = [0] * limit
            for i in range(2, limit):
                if counts[i] == 0:  # i is prime
                    for j in range(i, limit, i):
                        counts[j] += 1

            # Look for 4 consecutive numbers with 4 distinct prime factors
            for i in range(2, limit - 3):
                if (
                    counts[i] == 4
                    and counts[i + 1] == 4
                    and counts[i + 2] == 4
                    and counts[i + 3] == 4
                ):
                    return i, i+1, i+2, i+3
        num1, num2, num3, num4 = self.run_task(
            "Finding the first 4...",
            task
        )
        print(f"The first four consecutive integers to have four distinct prime factors each are: {Fore.GREEN}{num1}, {num2}, {num3}, {num4}{Fore.RESET}")
        print(f"With the first being: {Fore.GREEN}{num1}{Fore.RESET}")
        
    def problem48(self):
        "Find the last ten digits of the sum of self-powers from 1 to 1000."
        self.header(
            48,
            "Calculate the last ten digits of the sum of self-powers from 1 to 1000."
        )
        def task():
            # Define the modulus for the last 10 digits
            MOD = 10**10
            total_sum = sum(pow(i, i, MOD) for i in range(1, 1001))
            result = total_sum % MOD
            return result
        result = self.run_task(
            "Calculating a huge number...",
            task
        )
        print(f"The last ten digits of the sum of self-powers is: {Fore.GREEN}{result}{Fore.RESET}")

    def problem49(self):
        "Find the second 4-digit prime permutation sequence and its 12-digit concatenation."
        self.header(
            49,
            "Find the second 4-digit prime permutation sequence and its 12-digit concatenation."
        )
        def task():
            for first in range(1111, 3340):
                second = first + 3330
                third = first + 6660
                
                # Skip the sequence given in the problem statement
                if first == 1487:
                    continue
                    
                # Check if all three numbers are prime
                if self.is_prime(first) and self.is_prime(second) and self.is_prime(third):
                    # Check if all three numbers are permutations of each other
                    if sorted(str(first)) == sorted(str(second)) == sorted(str(third)):
                        return f"{first}{second}{third}"
        result = self.run_task(
            "Finding the 4-digit prime permutation sequence...",
            task
        )
        print(f"The 12-digit concatenation of second 4-digit prime permutation sequence is: {Fore.GREEN}{result}{Fore.RESET} ")

    def problem50(self):
        "Finds the prime below the limit that is the sum of the most consecutive primes."
        self.header(
            50,
            "Finds the prime below the limit that is the sum of the most consecutive primes."
        )
        def task(limit:int):
            is_prime = self.sieve_of_eratosthenes_list(limit)
            primes = [i for i, p in enumerate(is_prime) if p]
            prefix_sums = [0]
            for p in primes:
                prefix_sums.append(prefix_sums[-1] + p)
                
            max_length = 0
            best_prime = 0
            n_primes = len(primes)
            for i in range(n_primes):
                for j in range(i + max_length + 1, n_primes):
                    window_sum = prefix_sums[j] - prefix_sums[i]
                    if window_sum >= limit:
                        break
                    if is_prime[window_sum]:
                        max_length = j - i
                        best_prime = window_sum
            return best_prime
        result = self.run_task(
            "Combing through the Sieve of Eratosthenes...",
            task,
            1_000_000
        )
        print(f"The prime below the limit that is the sum of the most consecutive primes is: {Fore.GREEN}{result}{Fore.RESET}")

    # ==========================================================
    # Runner
    # ==========================================================

    def run(self, problems=None):
        start_time = 0
        if problems is None:
            start_time = time.perf_counter()
            problems = sorted(
                int(name[7:])
                for name in dir(self)
                if name.startswith("problem") and name[7:].isdigit()
            )
        for number in problems:
            method = getattr(self, f"problem{number}", None)

            if callable(method):
                try:
                    method()
                except ZeroDivisionError as e:
                    raise EulerProblemExecutionError(
                        number,
                        ZeroDivisionError("Attempted calculation contains division by 0. Calculation fails.")
                    ) from e
                except Exception as e:
                    print(f"{Fore.RED}Problem {number} ran into an error during execution.{Fore.RESET}")
                    raise EulerProblemExecutionError(number, e) from e
            else:
                print(f"{Fore.RED}Problem {number} has not been implemented.{Fore.RESET}")
                raise EulerProblemNotImplemented(number)
        if start_time != 0: 
            runtime = time.perf_counter() - start_time
            print(Fore.CYAN + "="*self.terminal_width)
            print(Fore.CYAN + f"Total Runtime: {runtime:.4f}s")

# ================
# Argparse Configs
# ================

solver = EulerSolver()

parser = argparse.ArgumentParser(
    prog=f"EulerProblems.py",
    description=f"Euler Project Attempts {Fore.CYAN}v{solver.VERSION}{Fore.RESET} - A Script with the first {solver.GOAL} Project Euler questions solved using Python.",
    epilog=f"Currently having {len(solver.list_problems(False))-1}/{solver.GOAL} problems sloved!",
    suggest_on_error=True
)
parser.add_argument(
    "problems",
    nargs="*",
    type=int,
    metavar="N",
    help="Problem numbers to run"
)
parser.add_argument(
    "-a",
    "--all",
    action="store_true",
    help="Run every implemented problem."
)
parser.add_argument(
    "-l",
    "--list",
    action="store_true",
    help="List all implemented problems."
)
parser.add_argument(
    "-n",
    "--no-easter-eggs",
    action="store_true",
    help="Disables easter eggs from happening for clean output."
)
parser.add_argument(
    "--force-easter-eggs",
    action="store_true",
    help=argparse.SUPPRESS,
)
parser.add_argument(
    "-v",
    "--version",
    action="version",
    version=(
        f"%(prog)s {Fore.CYAN}v{solver.VERSION}{Fore.RESET}"
        f" - Progress: {len(solver.list_problems(False))-1}/{solver.GOAL} solved"
    ),
)

if __name__ == "__main__":
    args = parser.parse_args()
    if args.no_easter_eggs and args.force_easter_eggs:
        parser.error(
            "--force-easter-eggs cannot be used together with --no-easter-eggs."
        )
    solver.EASTER_EGGS = not args.no_easter_eggs
    solver.FORCED_EASTER_EGGS = args.force_easter_eggs
    if args.list:
        solver.list_problems()
    elif args.all:
        solver.run()
    elif args.problems:
        solver.run(args.problems)
    else:
        # No arguments defaults to help
        parser.print_help()
        