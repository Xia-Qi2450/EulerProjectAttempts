"""
Hidden easter egg behavior for EulerSolver.

Each egg has a small (1%) chance of triggering when its associated
problem number is run, unless disabled with --no-easter-eggs (or forced
with the hidden --force-easter-eggs flag). Purely cosmetic/for fun -
none of this affects the actual Project Euler answers.

EasterEggsMixin is combined into EulerSolver in solver.py. It genuinely
inherits from HelpersMixin (rather than just assuming it) since it calls
self.header/self.run_task/self._typewriter/etc. - that real inheritance
is what lets Pylance/Pyright resolve those calls instead of flagging
them as unknown attributes.
"""

import random
import time
from datetime import datetime

from colorama import Fore, Style

from .helpers import Helpers


class EasterEggs(Helpers):
    """Hidden easter egg behavior, gated by EulerSolver._try_easter_egg."""

    # Set in EulerSolver.__init__; declared here for the type checker only.
    EASTER_EGGS: bool
    FORCED_EASTER_EGGS: bool
    current_file: str

    def _try_easter_egg(self, problem: int) -> bool:
        if not self.FORCED_EASTER_EGGS:
            if not self.EASTER_EGGS or random.randrange(100) != problem % 100:
                return False

        easter_eggs = {
            5: self.nakano5,
            37: self.march37,
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
        
        Who knew quintuplets could be so amazing?
        """
        from colorama import Back
        quints = ["Ichika", "Nino", "Miku", "Yotsuba", "Itsuki"]
        colors = [Fore.YELLOW, Fore.MAGENTA, Fore.BLUE, Fore.GREEN, Fore.RED]
        # TODO: Make a Quintessential Quintuplets easter egg here!
        print(Fore.CYAN + "=" * self.terminal_width)
        print(f"{Fore.YELLOW}/// WARNING ///{Fore.RESET}")
        print()
        self._typewriter("An unexpected route has been discovered.")
        time.sleep(0.2)
        self._load("Loading hidden problem", "DONE!", 1.2)
        self._wait()

        print(f"\nEuler's problem 5?: ")
        time.sleep(1)
        self._typewriter("No.")
        time.sleep(0.2)
        self._typewriter("Euler's Problem 5(x5): ", 0.05)
        print(f"{Fore.YELLOW}Select your answer{Fore.RESET}:")
        print()
        print(f"1. {Fore.BLACK}{Back.YELLOW}Ichika{Back.RESET}{Fore.RESET} \n2. {Fore.WHITE}{Back.MAGENTA}Nino{Back.RESET}{Fore.RESET} \n3. {Fore.WHITE}{Back.BLUE}Miku{Back.RESET}{Fore.RESET} \n4. {Fore.BLACK}{Back.GREEN}Yotsuba{Back.RESET}{Fore.RESET} \n5. {Fore.BLACK}{Back.RED}Itsuki{Back.RESET}{Fore.RESET}")
        ans = input(f"{Fore.CYAN}>>> {Fore.RESET}")
        try:
            ans = int(ans)
        except ValueError:
            print(f"{Fore.RED}Answer entered does not correspond to any quintuplets. Defaulting to Miku...{Fore.RESET}")
            ans = 3
        if not 1 <= ans <= 5:
            print(f"{Fore.RED}Answer entered does not correspond to any quintuplets. Defaulting to Miku...{Fore.RESET}")
            ans = 3
            print(f"You have entered {ans}. {colors[int(ans)-1]}{quints[int(ans)-1]}{Fore.RESET}")
        time.sleep(1)
        self._typewriter("...")
        self._typewriter("Interesting choice.")
        self._load("Evaluating your selection", "Finished!", random.uniform(0.5, 3))
        match ans:
            case 1:
                self._typewriter("You have chosen Ichika...")
                self._wait()
                self._typewriter("Big sister energy detected.")
                self._typewriter("A respectable choice.")
            case 2:
                self._typewriter("You have chosen Nino...")
                self._wait()
                self._typewriter("You like tsunderes, don't you?")
                self._typewriter("I won't judge.")
            case 3:
                self._typewriter("You have chosen Miku...")
                self._wait()
                self._typewriter("Excellent taste.")
                self._typewriter("I completely agree.")
            case 4:
                self._typewriter("You have chosen Yotsuba...")
                self._wait()
                self._typewriter("Positive energy levels are off the charts.")
                self._typewriter("Smile detected.")
            case 5:
                self._typewriter("You have chosen Itsuki...")
                self._wait()
                self._typewriter("Snack inventory increased by 500%.")
                self._typewriter("Food budget exceeded.")
        self._wait()
        self._load("Sending answer to for logging", "Something went wrong!", random.uniform(1, 5), True)
        self._typewriter("...")
        self._typewriter("Unfortunately...")
        self._wait()

        self._typewriter("This problem has multiple equally valid solutions.")
        time.sleep(3)
        print(f"Traceback (most recent call last):")
        print(f"  File \"{self.current_file}\", line {Fore.RED}1253{Fore.RESET}, in {Fore.RED}problem5{Fore.RESET}")
        print(f"    {Fore.MAGENTA}self._try_easter_egg{Fore.RED}(5){Fore.RESET}")
        print(f"    {Fore.MAGENTA}~~~~~~~~~~~~~~~~~~~~{Fore.RED}^^^{Fore.RESET}")
        print(f"  File \"{self.current_file}\", line {Fore.RED}802{Fore.RESET}, in {Fore.RED}_try_easter_egg{Fore.RESET}")
        print(f"    {Fore.MAGENTA}egg{Fore.RED}(){Fore.RESET}")
        print(f"    {Fore.MAGENTA}~~~{Fore.RED}^^{Fore.RESET}")
        print(f"  File \"{self.current_file}\", line {Fore.RED}884{Fore.RESET}, in {Fore.RED}nakano5{Fore.RESET}")
        print(f"    {Fore.MAGENTA}raise BestGirlConflictError{Fore.RED}(\"Expected one answer, received five.\"){Fore.RESET}")
        print(f"    {Fore.MAGENTA}~~~~~~~~~~~~~~~~~~~~~~~~~~~{Fore.RED}^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^{Fore.RESET}")
        print(f"{Fore.MAGENTA}{Style.BRIGHT}BestGirlConflictError{Fore.RESET}{Style.NORMAL}: {Fore.RED}Expected one answer, received five. {Fore.RESET}")
        input()

        choice = "N/A"
        verdict = "NIL"
        notes = "NIL"
        with open("nakano.txt", "w", encoding="utf-8") as f:
            match ans:
                case 1:
                    choice = "Ichika"
                    verdict = "Responsible"
                    notes = "Big sister energy detected."
                case 2:
                    choice = "Nino"
                    verdict = "Determined"
                    notes = "High tsundere tolerance confirmed."
                case 3:
                    choice = "Miku"
                    verdict = "Cultured"
                    notes = "History buff detected."
                case 4:
                    choice = "Yotsuba"
                    verdict = "Optimistic"
                    notes = "Energy levels exceed safe operating limits."
                case 5:
                    choice = "Itsuki"
                    verdict = "Hungry"
                    notes = "Food expenditure expected to increase."

            f.write(
                f"""Nakano Compatibility Report
=============================

Generated: {datetime.now():%Y-%m-%d %H:%M:%S}

Selected Candidate : {choice}
Evaluation Result  : {verdict}

Notes
-----
{notes}

Conclusion
----------
The Project Euler solver is unable to mathematically prove
which Nakano sister is objectively the best.

Reason:
All five solutions satisfy the constraints.

Status: INCONCLUSIVE

Thank you for participating."""
            )

        self._load("Recovering", "Recovered! A txt file has been created.", 2)
        self._wait("[Continue to next problem]")
        print(Fore.CYAN + "=" * self.terminal_width)

    def march37(self):
        """
        Display the hidden Project Euler Problem 37 easter egg.
                
        This easter egg has a 1% chance of appearing when Problem 37
        is executed unless disabled with --no-easter-eggs.
                
        March 7th is An enthusiastic girl who was saved from eternal ice by the Astral Express Crew, and......
        """
        # TODO: Make a March 7th from Honkai: Star Rail easter egg here!
        def dialog(charname:str,  message:str, speed:float, charcolor=Fore.WHITE, auto=False):
            print(f"{charcolor}{charname}{Fore.RESET}: ", end="", flush=True)
            time.sleep(0.3)
            self._typewriter(message, 0.03/speed, True)
            time.sleep(0.3)
            if not auto:
                self._wait()
        print(Fore.CYAN + "=" * self.terminal_width)
        self.header("37?", "Connect with March on the Astral Express")
        time.sleep(2)

        self._load("Connecting to Astral Express", "Connected!", random.uniform(3,8), False, f"{random.randint(200,500)}m")
        self._typewriter("....................")
        total = 100
        i = 0
        while i < total:
            self._progress_bar(i, total, title="Testing connection")
            i += random.randint(0,2)
            time.sleep(0.1)
        i = None
        self._load("Waiting for reciever", "Connection timed out, retrying...", 15, True, "Nil")
        time.sleep(0.5)
        self._load("Waiting for reciever", "Reciever March 7th connected!", random.uniform(5,15), False, f"{round(random.uniform(5,15), 2)}")
        time.sleep(0.5)

        dialog("March 7th", "Hello, is this working?", 0.7, Fore.CYAN)
        dialog("You", "Yep.", 1.2, Fore.GREEN)
        dialog("March 7th", "Wait..", 0.7, Fore.CYAN, True)
        dialog("March 7th", "Why can't I see you?", 0.7, Fore.CYAN)
        dialog("You", "This is a terminal.", 1.2, Fore.GREEN)
        dialog("March 7th", "...", 0.7, Fore.CYAN, True)
        dialog("March 7th", "What's a terminal?", 0.7, Fore.CYAN)
        dialog("You", "March, I don't want to explain that again.", 1.2, Fore.GREEN)
        dialog("March 7th", "Hmph, you meanie!", 0.7, Fore.CYAN)
        time.sleep(1)
        dialog("March 7th", "Project Euler Problem 37?", 0.7, Fore.CYAN, True)
        dialog("March 7th", "Is that a train route?", 0.7, Fore.CYAN, True)
        dialog("You", "No.", 1.2, Fore.GREEN)
        dialog("March 7th", "Is it food?", 0.7, Fore.CYAN, True)
        dialog("You", "No.", 1.2, Fore.GREEN)
        dialog("March 7th", "Is it one of Himeko's coffee recipes?", 0.7, Fore.CYAN, True)
        dialog("You", "Definitely not.", 1.2, Fore.GREEN)
        dialog("March 7th", "Then what IS it??", 0.5, Fore.CYAN)
        dialog("You", "I'm finding truncatable primes.", 1.2, Fore.GREEN)
        dialog("March 7th", "...", 0.7, Fore.CYAN, True)
        dialog("March 7th", "That sounds incredibly fake.", 0.7, Fore.CYAN)
        dialog("You", "It's real.", 1.2, Fore.GREEN)
        dialog("March 7th", "Math people scare me.", 0.7, Fore.CYAN)
        time.sleep(1)
        dialog("March 7th", "Oh and before I go...", 0.7, Fore.CYAN, True)
        dialog("March 7th", "Smile!", 0.7, Fore.CYAN)
        dialog("You", "March, you know this is all text right?", 1.2, Fore.GREEN, True)
        print("📸 *click*")

        with open("march.txt", "w", encoding="utf-8") as convo:
            convo.write("""
Astral Express Conversation Log

Subject:
A programmer solving Project Euler.

Mood:
Concentrating very hard.

Result:
Photo acquired successfully.

Rating:
★★★★★

Conversation:
March 7th: Hello, is this working?

You: Yep.

March 7th: Wait..
March 7th: Why can't I see you?

You: This is a terminal.

March 7th: ...
March 7th: What's a terminal?

You: March, I don't want to explain that again.

March 7th: Hmph, you meanie!

March 7th: Project Euler Problem 37?
March 7th: Is that a train route?
You: No.

March 7th: Is it food?
You: No.

March 7th: Is it one of Himeko's coffee recipes?
You: Definitely not.

March 7th: Then what IS it??

You: I'm finding truncatable primes.

March 7th: ...
March 7th: That sounds incredibly fake.

You: It's real.

March 7th: Math people scare me.

March 7th: Oh and before I go...
March 7th: Smile!

You: March, you know this is all text right?
                           
            """)
        self._load("Saving conversation", "Saved at march.txt!", random.uniform(1,2))

        dialog("You", "Oh, at least she know how to save text.", 1.2, Fore.GREEN)
        time.sleep(2)
        self._load("Waiting for reciever to respond", "ERROR: Reciever currently unreachable, terminating session...", 5, True, f"NA m")
        time.sleep(1)
        print(f"{Fore.RED}Session Terminated{Fore.RESET}")
        time.sleep(1)
        self._wait("[Continue to next problem]")
        print(Fore.CYAN + "=" * self.terminal_width)

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
        print(f"  File \"{self.current_file}\", line {Fore.RED}1952{Fore.RESET}, in {Fore.RED}problem39{Fore.RESET}")
        print(f"    {Fore.MAGENTA}self._try_easter_egg{Fore.RED}(39){Fore.RESET}")
        print(f"    {Fore.MAGENTA}~~~~~~~~~~~~~~~~~~~~{Fore.RED}^^^^{Fore.RESET}")
        print(f"  File \"{self.current_file}\", line {Fore.RED}802{Fore.RESET}, in {Fore.RED}_try_easter_egg{Fore.RESET}")
        print(f"    {Fore.MAGENTA}egg{Fore.RED}(){Fore.RESET}")
        print(f"    {Fore.MAGENTA}~~~{Fore.RED}^^{Fore.RESET}")
        print(f"  File \"{self.current_file}\", line {Fore.RED}1132{Fore.RESET}, in {Fore.RED}miku39{Fore.RESET}")
        print(f"    {Fore.MAGENTA}miku.start_runtime{Fore.RED}(){Fore.RESET}")
        print(f"    {Fore.MAGENTA}~~~~~~~~~~~~~~~~~~{Fore.RED}^^{Fore.RESET}")
        print(f"  File \"<miku_runtime>\", line {Fore.RED}???{Fore.RESET}, in {Fore.RED}try_install{Fore.RESET}")
        print(f"    {Fore.MAGENTA}Ȗũï{Fore.RED}Ž{Fore.MAGENTA}ǧÉƱɺħ￿ØɃ{Fore.RED}ţʢɠ{Fore.MAGENTA}ǙƶǙ￿¥{Fore.RED}ĭğ{Fore.MAGENTA}ɶȘƆÜǧ{Fore.RED}öʌɯʚȅ￿{Fore.MAGENTA}ŅŤɺģ¶{Fore.RESET}")
        print(f"    {Fore.MAGENTA}~~~{Fore.RED}^{Fore.MAGENTA}~~~~~~~~{Fore.RED}^^^{Fore.MAGENTA}~~~~~{Fore.RED}^^{Fore.MAGENTA}~~~~~{Fore.RED}^^^^^^{Fore.MAGENTA}~~~~~{Fore.RESET}")
        print(f"{Fore.MAGENTA}{Style.BRIGHT}MikuIsHidingInYourWiFi{Fore.RESET}{Style.NORMAL}: {Fore.RED}Thank you(39) for using EulerProblems.py, ありがとうございます。{Fore.RESET}")
        input()
        with open("miku.txt", "w", encoding="utf-8") as f:
            f.write("[Intro] \nOoh-ee-ooh \nOoh-ee-ooh \nOoh-ee-ooh \nOoh-ee-ooh \n\n[Verse 1] \nMiku, Miku, you can call me Miku \nBlue hair, blue tie, hiding in your Wi-Fi \nOpen secrets, anyone can find me \nHear your music running through my mind \n\n[Chorus] \nI'm thinkin' Miku, Miku (Ooh-ee-ooh) \nI'm thinkin' Miku, Miku (Ooh-ee-ooh) \nI'm thinkin' Miku, Miku (Ooh-ee-ooh) \nI'm thinkin' Miku, Miku (Ooh-ee-ooh) \n\n[Pre-Chorus] \nI'm on top of the world because of you \nAll I wanted to do is follow you \nI'll keep singing along to all of you \nI'll keep singing along \n\n[Chorus] \nI'm thinkin' Miku, Miku (Ooh-ee-ooh) \nI'm thinkin' Miku, Miku (Ooh-ee-ooh) \nI'm thinkin' Miku, Miku (Ooh-ee-ooh) \nI'm thinkin' Miku, Miku (Ooh-ee-ooh) \n\n[Verse 2] \nMiku, Miku, what's it like to be you? \n20/20, looking in the rear view \nPlay me, break me, make me feel like Superman \nYou can do anything you want \n\n[Pre-Chorus] \nI'm on top of the world because of you \nAll I wanted to do is follow you \nI'll keep singing along to all of you \nI'll keep singing along \nI'm on top of the world because of you \nI do nothing that they could never do \nI'll keep playing along with all of you \nI'll keep playing along \n\n[Chorus] \nI'm thinkin' Miku, Miku (Ooh-ee-ooh) \nI'm thinkin' Miku, Miku (Ooh-ee-ooh) \nI'm thinkin' Miku, Miku (Ooh-ee-ooh) \nI'm thinkin' Miku, Miku (Ooh-ee-ooh) \n\n[Bridge] \nWhere were we walking together? \nI will see you in the end \nI'll take you where you've never been \nAnd bring you back again \nListen to me with your eyes \nI'm watching you from in the sky \nIf you forget, I'll fade away \nI'm asking you to let me stay \nSo bathe me in your magic light \nAnd keep it on in darkest night \nI need you here to keep me strong \nTo live my life and sing along \nI'm waiting with you wide awake \nLike your expensive poison snake \nYou found me here inside a dream \nWalk through the fire straight to me \n\n[Outro] \n​tsap eht morf dnuos tsal ,erutuf eht morf dnuos tsriF")
        self._load("Recovering", "Recovered! A txt file has been created.", 2)
        self._wait("[Continue to next problem]")
        print(Fore.CYAN + "=" * self.terminal_width)
    
    def teto41(self):
        """
        (WIP)
        Display the hidden Project Euler Problem 41 easter egg.
        
        This easter egg has a 1% chance of appearing when Problem 41
        is executed unless disabled with --no-easter-eggs.
        
        Teto word of the day! Mathematics!
        """
        # TODO: Make a Kasane Teto easter egg here!

        print(Fore.CYAN + "=" * self.terminal_width)
        print(f"{Fore.YELLOW}/// WARNING ///{Fore.RESET}")
        print()
        self._typewriter("An unexpected route has been discovered.")
        time.sleep(0.2)
        self._load(
            "Loading hidden problem",
            "ERROR: Necessary libraries are not installed",
            5,
            True
        )
        self._wait()

        self._load(
            "Preparing to download necessary libraries",
            "Done!",
            3,
            False,
            3
        )

        time.sleep(1)
        total = random.randint(int(5e8), int(2e9))
        i = 0
        while i < total:
            self._progress_bar(i, total, title="Downloading bagettes...")
            i += random.randint(int(5e6), int(15e6))
            time.sleep(0.1)
        print(
            f"\rDownloaded bagettes, fetched {(total / 1e6):.2f} MB, "
            f"Checksum OK!                                             "
        )

        total = random.randint(int(1e11), int(9e13))
        i = 0
        while i < total:
            self._progress_bar(i, total, title="Downloading Teto...")
            i += random.randint(int(9e6), int(25e6))
            time.sleep(0.1)
            if i > int(5e9):
                time.sleep(5)
                break
        print()
        print(
            f"{Fore.RED}{Style.BRIGHT}FATAL ERROR{Style.NORMAL}: "
            f"Download cannot write to output file because "
            f"No space left on device"
        )

        time.sleep(2)
        self._typewriter("Attempting to diagnose storage issue...")
        time.sleep(1)
        self._load(
            "Checking available storage",
            "Complete!",
            2,
            False
        )
        time.sleep(1)
        print(f"{Fore.RED}Available storage: {Fore.YELLOW}0 bytes{Fore.RESET}")
        print(f"{Fore.RED}Required storage:  {Fore.YELLOW}{total / 1e12:.2f} TB{Fore.RESET}")
        time.sleep(2)
        self._typewriter("...")
        time.sleep(1)
        self._typewriter("Maybe downloading Teto was a bad idea.")
        self._wait()

        with open("teto.txt", "w", encoding="utf-8") as f:
            f.write(f"""
TETO INSTALLATION REPORT
========================

Status: FATAL ERROR

Package: kasane_teto
Version: 41.0

Downloading...
    bagettes.................... OK
    songs....................... OK
    teto........................ OK

Extracting...
    teto.zip.................... OK

Writing files...
    teto.py..................... OK
    teto_voicebank.............. OK
    teto_baguette............... OK
    teto̴̴̪̰̗̬̪̰̗̬̎̈́̅̎̈́̅̕̕͜͜

FATAL ERROR:
    No space left on device

Attempted allocation: {total} bytes
Available space:      0 bytes

Teto installation aborted.

Teto word of the day: Mathematics!

""")
        self._load(
            "Recovering",
            "Recovered! A txt file has been created.",
            2
        )
        self._wait("[Continue to next problem]")
        print(Fore.CYAN + "=" * self.terminal_width)

        
