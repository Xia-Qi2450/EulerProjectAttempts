"""
CLI/output helper methods for EulerSolver: headers, spinners, progress bar,
typewriter-style text, and other console presentation utilities.

HelpersMixin is combined into EulerSolver in solver.py, so every method
here can freely use `self.` attributes defined in EulerSolver.__init__
(e.g. self.terminal_width, self._spinner_frames).
"""

import sys
import time
from typing import Any
import itertools

from colorama import Fore, Style
from halo import Halo


class Helpers:
    """Console/output helpers shared by every Euler problem method."""

    # Set in EulerSolver.__init__. Declared here (with no value assigned)
    # purely so Pylance/Pyright knows these exist on self - this is just a
    # type annotation, it doesn't run or set anything at import time.
    terminal_width: int
    _spinner_frames: itertools.cycle

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

    def save_output(self, problem: int, suffix: str, text: str) -> str:
        filename = f"{problem:04d}_{suffix}.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(text)

        return filename

    def _typewriter(self, text: str, delay: float = 0.03, newline: bool = True) -> None:
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

    def _load(self, text:str, finish_text:str ,duration:float, fail:bool = False, fake_duration=None) -> None:
        spinner_interval = 0.25
        duration_str = fake_duration or "??.?"
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
                spinner.succeed(f"{finish_text} {Style.DIM}({duration_str}s){Style.NORMAL}")
            case True:
                spinner.fail(f"{finish_text} {Style.DIM}({duration_str}s){Style.NORMAL}")

    def _wait(self, custom_text:str="[Press Enter to continue]") -> None:
        print(f"{Fore.LIGHTBLACK_EX}{custom_text}{Fore.RESET}", end="", flush=True)
        input()

    def _progress_bar(self, current, total, title="Progress", bar_length=30) -> None:
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
 
