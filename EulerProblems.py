#!/usr/bin/env python3
"""
Project Euler Attempts
======================

Thin entry point. All real logic now lives in the euler_problems/ package
(see euler_problems/__init__.py for a map of what lives where).

This file exists so `python EulerProblems.py ...` keeps working exactly
like it did before the refactor - same CLI, same flags, same behavior.

Author: Xia Qi
License: MIT
"""

from euler_problems.cli import main

if __name__ == "__main__":
    main()
