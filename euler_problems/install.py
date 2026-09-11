"""
Downloads the external data files that some Project Euler problems need
(names.txt, sudoku puzzles, matrices, etc.) directly from projecteuler.net,
styled after `dnf install`'s transaction output.

Run via:
    ./EulerProblems.py install                  # download everything that's missing
    ./EulerProblems.py install 22 96             # download just what problems 22 and 96 need
    ./EulerProblems.py install -y                # skip the confirmation prompt
    ./EulerProblems.py install --reinstall 81    # re-download even if already present

InstallerMixin is combined into EulerSolver in solver.py the same way every
other mixin is, so it reuses self._progress_bar/self.terminal_width/
self.SPINNERS from Helpers instead of reinventing them.
"""

import os
import requests
import urllib.error
import urllib.request

from colorama import Fore, Style

from .helpers import Helpers

PROJECT_EULER_BASE_URL = "https://projecteuler.net/resources/documents/"
USER_AGENT = "EulerProjectAttempts-Installer/1.0"

# Single source of truth: which problem(s) need which file. Several problems
# can share one file - 81/82/83 all read the same matrix, for instance.
DATA_FILES: dict[int, str] = {
    22: "0022_names.txt",
    42: "0042_words.txt",
    54: "0054_poker.txt",
    59: "0059_cipher.txt",
    67: "0067_triangle.txt",
    79: "0079_keylog.txt",
    81: "0081_matrix.txt",
    82: "0081_matrix.txt",
    83: "0081_matrix.txt",
    89: "0089_roman.txt",
    96: "0096_sudoku.txt",
    98: "0098_words.txt",
    99: "0099_base_exp.txt",
    102: "0102_triangles.txt",
    105: "0105_sets.txt",
    107: "0107_network.txt",
}


def _unique_files() -> list[str]:
    """Every distinct filename in DATA_FILES, ascending by problem, deduplicated."""
    seen: list[str] = []
    for _, filename in sorted(DATA_FILES.items()):
        if filename not in seen:
            seen.append(filename)
    return seen


def _problems_for(filename: str) -> list[int]:
    return sorted(n for n, f in DATA_FILES.items() if f == filename)


def _format_size(num_bytes: int | None) -> str:
    if num_bytes is None:
        return "Unknown"
    size = float(num_bytes)
    for unit in ("B", "KiB", "MiB"):
        if size < 1024 or unit == "MiB":
            return f"{size:.0f} {unit}" if unit == "B" else f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} GiB"


class InstallerMixin(Helpers):
    """Downloads Project Euler's external data files, dnf-style."""

    def _resolve_install_targets(self, args: list[str]) -> tuple[list[str], bool, bool]:
        """
        Turns whatever followed "install" on the command line - e.g.
        ["22", "96"], ["-y"], ["--reinstall", "81"], or [] for "everything" -
        into (filenames, force, assume_yes).
        """
        force = False
        assume_yes = False
        numbers: list[str] = []

        for token in args:
            if token in ("-f", "--reinstall", "--force"):
                force = True
            elif token in ("-y", "--assumeyes", "--yes"):
                assume_yes = True
            else:
                numbers.append(token)

        if numbers:
            filenames: list[str] = []
            for token in numbers:
                if not token.isdigit() or int(token) not in DATA_FILES:
                    print(f"{Fore.YELLOW}No data file is associated with problem '{token}' - skipping.{Fore.RESET}")
                    continue
                filename = DATA_FILES[int(token)]
                if filename not in filenames:
                    filenames.append(filename)
        else:
            filenames = _unique_files()

        return filenames, force, assume_yes

    def _head_content_length(self, url: str) -> int | None:
        request =requests.get(url, headers={"User-Agent": USER_AGENT})
        try:
            with request as response:
                length = len(response.content)
                return int(length) if length is not None else None
        except (requests.HTTPError, ValueError, TimeoutError):
            return None

    def _download_file(self, url: str, dest: str, index: int, total: int, totals:dict[str, int | None]={}) -> int:
        """Streams url to dest, driving self._progress_bar. Returns bytes written."""
        request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        length: int | None = 0
        if totals: length = totals[url.removeprefix(PROJECT_EULER_BASE_URL)]
        else: length = self._head_content_length(url)
        chunk_size = 4096
        written = 0
        title = f"({index}/{total}) {os.path.basename(dest)}"
        tmp_path = dest + ".part"

        with urllib.request.urlopen(request, timeout=15) as response:
            total_size = int(length) if length is not None else None

            with open(tmp_path, "wb") as out:
                while True:
                    chunk = response.read(chunk_size)
                    if not chunk:
                        break
                    out.write(chunk)
                    written += len(chunk)
                    self._progress_bar(written, total_size or written, title=title)

        os.replace(tmp_path, dest)
        return written

    def install(self, args: list[str] | None = None) -> None:
        """Download the external data files certain problems need, dnf-style."""
        args = args or []
        filenames, force, assume_yes = self._resolve_install_targets(args)

        if not filenames:
            print(f"{Fore.RED}Nothing to install.{Fore.RESET}")
            return

        print(f"{Fore.CYAN}Project Euler Data File Installer{Fore.RESET}")
        print("Last metadata expiration check: 0:00:00 ago.")

        to_install = [f for f in filenames if force or not os.path.isfile(f)]
        already_present = [f for f in filenames if f not in to_install]

        for filename in already_present:
            print(f"Package {filename} is already installed, skipping.")

        if not to_install:
            print(f"\n{Fore.GREEN}Nothing to do. All requested files are already present.{Fore.RESET}")
            return

        print(f"{Fore.GREEN}Dependencies resolved.{Fore.RESET}")
        print("=" * self.terminal_width)
        print(f" {'Problem':<20}{'File':<30}{'Size':>10}   Source")
        print("=" * self.terminal_width)
        print("Installing:")

        sizes: dict[str, int | None] = {}
        for filename in to_install:
            url = PROJECT_EULER_BASE_URL + filename
            size = self._head_content_length(url)
            sizes[filename] = size
            problems = ", ".join(str(p) for p in _problems_for(filename))
            print(f" {problems:<20}{filename:<30}{_format_size(size):>10}   projecteuler.net")

        print()
        print(f"{Style.BRIGHT}Transaction Summary{Style.NORMAL}")
        print("=" * self.terminal_width)
        print(f"Install  {len(to_install)} File{'s' if len(to_install) != 1 else ''}")
        known_sizes = [s for s in sizes.values() if s is not None]
        if known_sizes:
            print(f"\nTotal download size: {_format_size(sum(known_sizes))}")

        if not assume_yes:
            answer = input(f"\n{Fore.CYAN}Is this ok [y/N]: {Fore.RESET}")
            if answer.strip().lower() not in ("y", "yes"):
                print(f"{Fore.YELLOW}Operation aborted.{Fore.RESET}")
                return

        print(f"\n{Style.BRIGHT}Downloading Packages:{Style.NORMAL}")
        succeeded: list[str] = []
        failed: list[str] = []
        try:
            for i, filename in enumerate(to_install, start=1):
                url = PROJECT_EULER_BASE_URL + filename
                try:
                    self._download_file(url, filename, i, len(to_install), sizes)
                    succeeded.append(filename)
                except (urllib.error.URLError, TimeoutError, OSError) as e:
                    print(f"{Fore.RED}Failed to download {filename}: {e}{Fore.RESET}")
                    failed.append(filename)
        except KeyboardInterrupt:
            print(f"\n{Style.DIM}{Fore.YELLOW}Installation interrupted by user{Fore.RESET}{Style.NORMAL}")
            return

        if not succeeded:
            print(f"\n{Fore.RED}No files were downloaded.{Fore.RESET}")
            return

        print()
        print(f"{Style.DIM}Running transaction check{Style.NORMAL}")
        print(f"{Style.DIM}Running transaction test{Style.NORMAL}")
        print(f"{Style.DIM}Transaction test succeeded.{Style.NORMAL}")
        print(f"{Style.DIM}Running transaction{Style.NORMAL}")
        for i, filename in enumerate(succeeded, start=1):
            problems = ", ".join(str(p) for p in _problems_for(filename))
            plural = "s" if len(_problems_for(filename)) != 1 else ""
            label = f"  Installing : {filename} (problem{plural} {problems})"
            print(f"{label:<70}{i}/{len(succeeded)}")

        print(f"\n{Fore.GREEN}Installed:{Fore.RESET}")
        for filename in succeeded:
            print(f"  {filename}")

        if failed:
            print(f"\n{Fore.RED}Failed:{Fore.RESET}")
            for filename in failed:
                print(f"  {filename}")

        print(f"\n{Fore.GREEN}{Style.BRIGHT}Complete!{Style.NORMAL}{Fore.RESET}")
