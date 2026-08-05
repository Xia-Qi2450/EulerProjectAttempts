"""
Custom exception hierarchy for the Project Euler solver.

Note: RequiredModulesNotFound and ImportModulesFail deliberately avoid
importing colorama/halo themselves - they exist to report that those
packages are missing, so they can't depend on them being present.
"""

class EulerProblemError(Exception):
    """Base exception for Project Euler errors."""

class EulerProblemNotImplemented(NotImplementedError, EulerProblemError):
    """When a Euler Problem is not implemented and it's being called."""
    def __init__(self, problem_no:int) -> None:
        message = f"Euler Problem number {problem_no} Has not been implemented yet."
        super().__init__(message)

class EulerProblemExecutionError(RuntimeError, EulerProblemError):
    """When something weird happens during code execution."""
    def __init__(self, problem_no: int, error: Exception):
        from colorama import Fore, Style  # safe here: only raised after startup import check passes

        self.problem_no = problem_no
        self.error = error

        super().__init__(
            f"Euler Problem {problem_no} failed during execution.\n"
            f"Caused by {Style.BRIGHT}{Fore.MAGENTA}{type(error).__name__}{Fore.RESET}{Style.NORMAL}: {Fore.MAGENTA}{error}{Fore.MAGENTA}"
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
