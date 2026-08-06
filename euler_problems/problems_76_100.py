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
    "Problem solutions 76-100."