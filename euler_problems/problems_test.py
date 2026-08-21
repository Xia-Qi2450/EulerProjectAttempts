"""
Project Euler solutions: testing and debugging utilities.

Provides methods for testing utility functions, Project Euler 
solutions, and other shared components of the project.
"""

import random
import string
import time
import shutil
import traceback


from colorama import Fore

from euler_problems.exceptions import EulerProblemError

from . import data
from .utils import UtilsMixin
from .easter_eggs import EasterEggs

class ProblemsTest(UtilsMixin, EasterEggs):
    """Testing and debugging methods for Project Euler problems."""

    def __init__(self) -> None:
        """Initalise testing variables..."""
        self.SPINNERS:bool = True
        self.terminal_width: int = shutil.get_terminal_size(fallback=(70, 24)).columns
        self.LIST_OF_RANDOM_WORDS = ["python", "jumble", "easy", "difficult", "answer",  "xylophone"]
        self.word = random.choice(self.LIST_OF_RANDOM_WORDS) + random.choice(self.LIST_OF_RANDOM_WORDS) + random.choice(self.LIST_OF_RANDOM_WORDS) + random.choice(self.LIST_OF_RANDOM_WORDS) + random.choice(self.LIST_OF_RANDOM_WORDS) + random.choice(self.LIST_OF_RANDOM_WORDS) + random.choice(self.LIST_OF_RANDOM_WORDS) + random.choice(self.LIST_OF_RANDOM_WORDS) + random.choice(self.LIST_OF_RANDOM_WORDS) + random.choice(self.LIST_OF_RANDOM_WORDS)
        self.random_list = random.sample(range(1, 71), 70)
        self.fibonacci_list = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987, 1597, 2584, 4181, 6765, 10946, 17711, 28657, 46368, 75025, 121393, 196418, 317811, 514229, 832040, 1346269, 2178309, 3524578, 5702887, 9227465, 14930352, 24157817, 39088169, 63245986, 102334155, 165580141, 267914296, 433494437, 701408733, 1134903170, 1836311903, 2971215073, 4807526976, 7778742049]
        self.ROMAN_MAP = data.ROMAN_MAP

    def _random_task(self, duration:float, returnMsg:str):
        """Just a glorified time.sleep() with a return message"""
        time.sleep(duration)
        return returnMsg

    def test_basic_functions(self, word:str):
        """This function tests for all basic functions to make sure that they are working."""
        try: 
            print(f"{Fore.CYAN}Testing for problem header:{Fore.RESET}")
            self.header(random.randint(1,700), word)
            time.sleep(0.5)
            self.header("String", "Problem")
            time.sleep(0.5)
            self.header(random.randint(1,700), string.ascii_letters)
            time.sleep(0.5)
            print(f"{Fore.CYAN}Testing for problem solving spinner:{Fore.RESET}")
            result = self.run_task("Running task", self._random_task, random.uniform(1, 2.5), True)
            if not result: 
                raise Exception("self.run_task did not output anything!")
            self.SPINNERS = False
            time.sleep(0.5)
            print(f"{Fore.CYAN}Testing for problem solving clean:{Fore.RESET}")
            result = self.run_task("Running task", self._random_task, random.uniform(1, 2.5), True)
            if not result: 
                raise Exception("self.run_task did not output anything!")
            print(f"{Fore.GREEN}All basic functions tests passed!{Fore.RESET}")
            print(f"{Fore.GREEN}Clearing and reseting variables...{Fore.RESET}")
            self.SPINNERS = True
            result = None
                
        except Exception as e:
            raise EulerProblemError(
                f"Basic function test failed: {type(e).__name__}: {e}"
            ) from e

        return True

    def test_run_task_exceptions(self):
        """This function ensure exceptions from tasks are propagated correctly."""

        def failing_task():
            raise ValueError("Intentional test failure")

        try:
            print(f"{Fore.CYAN}Testing for exception propagation:{Fore.RESET}")
            self.run_task("Testing exception handling", failing_task)
        except ValueError as e:
            if str(e) != "Intentional test failure":
                raise EulerProblemError("Exception message was modified unexpectedly!") from e
            else:
                print("\n")
                print(traceback.format_exc())
                print(f"{Fore.GREEN}Exception propagation tests passed!{Fore.RESET}")

        return True
        
    def test_utils(self):
        """Tests for essential math utility functions"""
        try:
            print(f"{Fore.CYAN}Testing for essential utility functions:{Fore.RESET}")
            print(f"{Fore.CYAN} Testing for prime detection:{Fore.RESET}")
            prime = self.run_task(" Test for is_prime(actually not prime)", self.is_prime, 10)
            if prime:
                raise ValueError("Number isn't prime, tested prime.")
            prime = self.run_task(" Test for is_prime(actually prime)", self.is_prime, 7)
            if not prime:
                raise ValueError("Number is prime, tested non-prime.")
            print(f"{Fore.GREEN}    Prime tests passed!{Fore.RESET} (1/7)")
            time.sleep(0.5)
            print()
            print(f"{Fore.CYAN} Testing for palindrome detection:{Fore.RESET}")
            palindrome = self.run_task("Test for is_palindrome(actually not palindrome)", self.is_palindrome_str, 1234567890)
            if palindrome:
                raise ValueError("Number isn't palindrome, tested palindrome.")
            palindrome = self.run_task("Test for is_palindrome(actually palindrome)", self.is_palindrome_str, 1234554321)
            if not palindrome:
                raise ValueError("Number is palindrome, tested non-palindrome.")
            palindrome = self.run_task("Test for string is_palindrome(actually not palindrome)", self.is_palindrome, "Never odd or even")
            if palindrome:
                raise ValueError("String isn't palindrome, tested palindrome.")
            palindrome = self.run_task("Test for string is_palindrome(actually palindrome)", self.is_palindrome, "neveroddoreven")
            if not palindrome:
                raise ValueError("String is palindrome, tested non-palindrome.")
            print(f"{Fore.GREEN}    Palindrome tests passed!{Fore.RESET} (2/7)")
            time.sleep(0.5)
            print()
            print(f"{Fore.CYAN} Testing for square detection:{Fore.RESET}")
            square = self.run_task("    Test for is_square(actually not square)", self.is_square, 20)
            if square:
                raise ValueError("Number isn't square, tested square.")
            square = self.run_task("    Test for is_square(actually square)", self.is_square, 25)
            if not square:
                raise ValueError("Number is square, tested non-square.")
            print(f"{Fore.GREEN}    Square tests passed!{Fore.RESET} (3/7)")
            time.sleep(0.5)
            print()
            print(f"{Fore.CYAN} Testing for fibonacci generation:{Fore.RESET}")
            fibonacci = self.run_task(" Test for fibonacci generator", self.fibonacci_sequence_limit, 7778742050)
            expected = self.fibonacci_list
            actual = list(fibonacci)
            if actual != expected:
                raise ValueError(
                    f"Fibonacci generator produced incorrect numbers.\n"
                    f"Expected: {expected}\n"
                    f"Got: {actual}"
                )
            print(f"{Fore.GREEN}    Fibonacci generation passed!{Fore.RESET} (4/7)")
            time.sleep(0.5)
            print()
            print(f"{Fore.CYAN} Testing for the Sieve of Eratosthenes/Prime generation:{Fore.RESET}")
            def test_sieve_of_eratosthenes():
                Sieve: list[bool] = self.sieve_of_eratosthenes_list(10000)
                for i, is_prime in enumerate(Sieve):
                    if is_prime != self.is_prime(i):
                        raise ValueError(
                            f"Sieve of Eratosthenes produced incorrect results.\n"
                            f"On number: {i}\n"
                            f"Expected: {self.is_prime(i)}\n"
                            f"Got: {is_prime}"
                        )
            self.run_task("Test for Sieve of Eratosthenes", test_sieve_of_eratosthenes)
            print(f"{Fore.GREEN}    Sieve of Eratosthenes test passed!{Fore.RESET} (5/7)")
            time.sleep(0.5)
            print()
            print(f"{Fore.CYAN} Testing for the Square generation:{Fore.RESET}")
            def test_square_gen():
                squares:list[int] = self.find_all_squares_until(10000)
                for i, is_square in enumerate(squares):
                    if not self.is_square(is_square):
                        raise ValueError(
                            f"Square generation produced incorrect results.\n"
                            f"Expected: {True}\n"
                            f"Got: {self.is_square(is_square)}"
                        )
            self.run_task("Test for Square generation", test_square_gen)        
            print(f"{Fore.GREEN}    Square generation test passed!{Fore.RESET} (6/7)")
            time.sleep(0.5)
            print()
            print(f"{Fore.CYAN} Testing for Roman numeral translation:{Fore.RESET}")
            def Roman_to_num_to_Roman():
                original = 1024
                roman = self.int_to_roman(original)
                final = self.roman_to_int(roman)
                if original != final:
                    raise ValueError(
                        f"Translating from Arabic to Roman numerals and back failed.\n"
                        f"Expected: {original}\n"
                        f"Got: {final}"
                    )
            self.run_task("Test for Roman numeral translation", Roman_to_num_to_Roman)        
            print(f"{Fore.GREEN}    Roman numeral translation test passed!{Fore.RESET} (7/7)")
            time.sleep(0.5)
            print()
            print(f"{Fore.GREEN}All essential utility functions tests passed!{Fore.RESET}")
            print(f"{Fore.GREEN}Clearing and reseting variables...{Fore.RESET}")
            prime = None
            palindrome = None
            square = None
            fibonacci = None
            expected = None
            actual = None
        except Exception as e:
            raise EulerProblemError(
                f"Utility functions test failed: {type(e).__name__}: {e}"
            ) from e

        return True


        
