"""
╔══════════════════════════════════════════════════════════╗
║           🧠  BRAIN BLAST QUIZ GAME  🧠                  ║
║         Test your knowledge across 3 levels!             ║
╚══════════════════════════════════════════════════════════╝
"""

import time
import random
import threading
import sys
import os

# ─────────────────────────────────────────────
#  ANSI COLOR CODES (makes the terminal pretty!)
# ─────────────────────────────────────────────
GREEN  = "\033[92m"
RED    = "\033[91m"
YELLOW = "\033[93m"
CYAN   = "\033[96m"
BOLD   = "\033[1m"
RESET  = "\033[0m"
MAGENTA = "\033[95m"
BLUE   = "\033[94m"

# ─────────────────────────────────────────────
#  QUESTION BANK
# ─────────────────────────────────────────────

QUESTIONS = {
    "easy": [
        {"q": "What is the capital of France?",
         "options": ["A) Berlin", "B) Madrid", "C) Paris", "D) Rome"],
         "answer": "C", "points": 10},
        {"q": "How many sides does a triangle have?",
         "options": ["A) 2", "B) 3", "C) 4", "D) 5"],
         "answer": "B", "points": 10},
        {"q": "What color do you get when you mix red and white?",
         "options": ["A) Purple", "B) Orange", "C) Pink", "D) Brown"],
         "answer": "C", "points": 10},
        {"q": "Which planet is known as the Red Planet?",
         "options": ["A) Venus", "B) Jupiter", "C) Saturn", "D) Mars"],
         "answer": "D", "points": 10},
        {"q": "What is 12 × 12?",
         "options": ["A) 124", "B) 144", "C) 132", "D) 148"],
         "answer": "B", "points": 10},
        {"q": "Who wrote 'Romeo and Juliet'?",
         "options": ["A) Charles Dickens", "B) Mark Twain", "C) William Shakespeare", "D) Jane Austen"],
         "answer": "C", "points": 10},
        {"q": "What is the largest ocean on Earth?",
         "options": ["A) Atlantic", "B) Indian", "C) Arctic", "D) Pacific"],
         "answer": "D", "points": 10},
    ],
    "medium": [
        {"q": "What is the chemical symbol for Gold?",
         "options": ["A) Go", "B) Gd", "C) Au", "D) Ag"],
         "answer": "C", "points": 20},
        {"q": "In which year did World War II end?",
         "options": ["A) 1943", "B) 1945", "C) 1947", "D) 1950"],
         "answer": "B", "points": 20},
        {"q": "What is the speed of light (approx.) in km/s?",
         "options": ["A) 100,000", "B) 200,000", "C) 300,000", "D) 400,000"],
         "answer": "C", "points": 20},
        {"q": "Which programming language is known as the 'mother of all languages'?",
         "options": ["A) Python", "B) Java", "C) C", "D) FORTRAN"],
         "answer": "C", "points": 20},
        {"q": "What is the powerhouse of the cell?",
         "options": ["A) Nucleus", "B) Ribosome", "C) Golgi body", "D) Mitochondria"],
         "answer": "D", "points": 20},
        {"q": "How many bones are in the adult human body?",
         "options": ["A) 186", "B) 206", "C) 226", "D) 246"],
         "answer": "B", "points": 20},
        {"q": "Which element has the atomic number 1?",
         "options": ["A) Helium", "B) Oxygen", "C) Hydrogen", "D) Carbon"],
         "answer": "C", "points": 20},
    ],
    "hard": [
        {"q": "What is the only even prime number?",
         "options": ["A) 0", "B) 1", "C) 2", "D) 4"],
         "answer": "C", "points": 30},
        {"q": "Who developed the theory of general relativity?",
         "options": ["A) Isaac Newton", "B) Niels Bohr", "C) Albert Einstein", "D) Max Planck"],
         "answer": "C", "points": 30},
        {"q": "What is the value of π (pi) to 4 decimal places?",
         "options": ["A) 3.1415", "B) 3.1416", "C) 3.1419", "D) 3.1421"],
         "answer": "B", "points": 30},
        {"q": "Which country has the most natural lakes?",
         "options": ["A) Russia", "B) USA", "C) Brazil", "D) Canada"],
         "answer": "D", "points": 30},
        {"q": "What does 'HTTP' stand for?",
         "options": ["A) HyperText Transfer Protocol",
                     "B) High Tech Transfer Protocol",
                     "C) HyperText Transmission Process",
                     "D) Hybrid Text Transfer Protocol"],
         "answer": "A", "points": 30},
        {"q": "What is the smallest prime number greater than 100?",
         "options": ["A) 101", "B) 103", "C) 107", "D) 109"],
         "answer": "B", "points": 30},
        {"q": "Which gas makes up about 78% of Earth's atmosphere?",
         "options": ["A) Oxygen", "B) Carbon Dioxide", "C) Argon", "D) Nitrogen"],
         "answer": "D", "points": 30},
    ]
}

# Time limits per level (in seconds)
TIME_LIMITS = {"easy": 15, "medium": 12, "hard": 10}

# Number of questions per level
QUESTIONS_PER_LEVEL = 5

# ─────────────────────────────────────────────
#  UTILITY FUNCTIONS
# ─────────────────────────────────────────────

def clear():
    """Clear the terminal screen."""
    os.system("cls" if os.name == "nt" else "clear")

def slow_print(text, delay=0.03):
    """Print text character by character for a typewriter effect."""
    for ch in text:
        sys.stdout.write(ch)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def divider(char="─", length=58, color=CYAN):
    """Print a styled divider line."""
    print(color + char * length + RESET)

def banner():
    """Print the game banner."""
    clear()
    print(CYAN + BOLD)
    print("╔══════════════════════════════════════════════════════════╗")
    print("║          🧠  B R A I N   B L A S T   Q U I Z  🧠         ║")
    print("║         Think fast. Answer smart. Beat the clock!        ║")
    print("╚══════════════════════════════════════════════════════════╝")
    print(RESET)

# ─────────────────────────────────────────────
#  TIMED INPUT — gets answer within time limit
# ─────────────────────────────────────────────

_user_answer = None
_answer_event = threading.Event()

def _get_input(prompt):
    """Thread-safe input capture."""
    global _user_answer
    try:
        _user_answer = input(prompt).strip().upper()
    except EOFError:
        _user_answer = ""
    _answer_event.set()

def timed_input(prompt, timeout):
    """
    Display a prompt and wait for input up to `timeout` seconds.
    Returns (answer, time_taken) or (None, timeout) if time runs out.
    """
    global _user_answer
    _user_answer = None
    _answer_event.clear()

    # Start input thread
    t = threading.Thread(target=_get_input, args=(prompt,), daemon=True)
    t.start()

    start = time.time()
    # Show countdown while waiting
    while not _answer_event.is_set():
        elapsed = time.time() - start
        remaining = timeout - elapsed
        if remaining <= 0:
            print(f"\r{RED}⏰  Time's up!{RESET}                          ")
            return None, timeout
        # Refresh countdown display on same line
        bar_len = 20
        filled = int((remaining / timeout) * bar_len)
        bar_color = GREEN if remaining > timeout * 0.5 else YELLOW if remaining > timeout * 0.25 else RED
        bar = bar_color + "█" * filled + "░" * (bar_len - filled) + RESET
        sys.stdout.write(
            f"\r  ⏱  [{bar}{bar_color}] {remaining:4.1f}s remaining   "
        )
        sys.stdout.flush()
        time.sleep(0.1)

    elapsed = time.time() - start
    print()  # newline after countdown bar
    return _user_answer, round(elapsed, 2)

# ─────────────────────────────────────────────
#  DISPLAY A QUESTION
# ─────────────────────────────────────────────

def display_question(q_num, total, question_data, level_name, score, time_limit):
    """
    Render the question UI and collect the timed answer.
    Returns (is_correct: bool, points_earned: int, time_taken: float)
    """
    divider()
    print(f"  {BOLD}{CYAN}Level: {level_name.upper()}{RESET}   "
          f"{YELLOW}Q {q_num}/{total}{RESET}   "
          f"{GREEN}Score: {score}{RESET}   "
          f"{MAGENTA}⏱ Limit: {time_limit}s{RESET}")
    divider()
    print()
    slow_print(f"  {BOLD}❓  {question_data['q']}{RESET}", delay=0.02)
    print()
    for opt in question_data["options"]:
        print(f"     {YELLOW}{opt}{RESET}")
    print()

    prompt = f"  {BOLD}Your answer (A/B/C/D): {RESET}"
    answer, elapsed = timed_input(prompt, time_limit)

    # Evaluate
    correct_ans = question_data["answer"]
    points = question_data["points"]

    if answer is None:
        # Timed out
        print(f"\n  {RED}✗  No answer! Correct answer was: {BOLD}{correct_ans}{RESET}")
        return False, 0, time_limit

    if answer not in ("A", "B", "C", "D"):
        print(f"\n  {RED}✗  Invalid choice! Correct answer was: {BOLD}{correct_ans}{RESET}")
        return False, 0, elapsed

    if answer == correct_ans:
        # Bonus points for answering quickly (under half the time limit)
        bonus = 5 if elapsed < time_limit / 2 else 0
        total_pts = points + bonus
        bonus_msg = f"  {GREEN}⚡ Speed bonus: +{bonus} pts!{RESET}" if bonus else ""
        print(f"\n  {GREEN}✓  Correct! +{points} pts{RESET} {f'(answered in {elapsed}s)'}")
        if bonus_msg:
            print(bonus_msg)
        return True, total_pts, elapsed
    else:
        print(f"\n  {RED}✗  Wrong! Correct answer was: {BOLD}{correct_ans}{RESET}  "
              f"(You answered: {answer}, took {elapsed}s)")
        return False, 0, elapsed

# ─────────────────────────────────────────────
#  PLAY A SINGLE LEVEL
# ─────────────────────────────────────────────

def play_level(level_key, level_num, player_name, running_score):
    """
    Run one full level. Returns (level_score, passed: bool).
    """
    level_names = {"easy": "🟢 Easy", "medium": "🟡 Medium", "hard": "🔴 Hard"}
    level_name   = level_names[level_key]
    time_limit   = TIME_LIMITS[level_key]
    pool         = random.sample(QUESTIONS[level_key], QUESTIONS_PER_LEVEL)

    clear()
    banner()
    print(f"\n  {BOLD}{CYAN}━━━  LEVEL {level_num}: {level_name.upper()}  ━━━{RESET}")
    print(f"  {YELLOW}⏱  Time per question: {time_limit} seconds{RESET}")
    print(f"  {YELLOW}⭐  Points per correct answer: {pool[0]['points']} (+5 speed bonus if fast!){RESET}")
    print(f"  {YELLOW}📋  Questions: {QUESTIONS_PER_LEVEL}{RESET}")
    print()
    input(f"  {GREEN}Press ENTER when you're ready, {player_name}...{RESET}")

    level_score  = 0
    correct_count = 0

    for idx, q_data in enumerate(pool, 1):
        clear()
        banner()
        is_correct, pts, _ = display_question(
            idx, QUESTIONS_PER_LEVEL, q_data, level_name,
            running_score + level_score, time_limit
        )
        if is_correct:
            level_score   += pts
            correct_count += 1

        time.sleep(1.5)

    # Level summary
    clear()
    banner()
    divider("═")
    print(f"\n  {BOLD}📊  LEVEL {level_num} COMPLETE — {level_name.upper()}{RESET}")
    divider("═")
    print(f"  ✅  Correct answers : {GREEN}{correct_count} / {QUESTIONS_PER_LEVEL}{RESET}")
    print(f"  🏆  Level score     : {CYAN}{level_score} pts{RESET}")
    print(f"  📈  Running total   : {YELLOW}{running_score + level_score} pts{RESET}")
    divider()

    # Need at least 3/5 to pass and advance
    passed = correct_count >= 3
    if passed:
        print(f"\n  {GREEN}{BOLD}🎉  Level passed! Great job!{RESET}")
    else:
        print(f"\n  {RED}{BOLD}💔  Level failed (needed 3+ correct). Game over.{RESET}")
    print()

    return level_score, passed

# ─────────────────────────────────────────────
#  PERFORMANCE BADGE
# ─────────────────────────────────────────────

def performance_badge(score, max_score):
    """Return a title and message based on final score percentage."""
    pct = (score / max_score) * 100 if max_score > 0 else 0
    if pct >= 85:
        return f"{CYAN}🏆  QUIZ MASTER — PRO PLAYER!{RESET}", \
               "Absolutely brilliant! You aced the Brain Blast Quiz!"
    elif pct >= 60:
        return f"{GREEN}⭐  INTERMEDIATE THINKER{RESET}", \
               "Solid performance! Keep sharpening that brain!"
    else:
        return f"{YELLOW}🌱  BEGINNER EXPLORER{RESET}", \
               "Great start! Practice makes perfect — try again!"

# ─────────────────────────────────────────────
#  GAME INSTRUCTIONS
# ─────────────────────────────────────────────

def show_instructions():
    """Display the how-to-play screen."""
    clear()
    banner()
    divider("═")
    slow_print(f"  {BOLD}{CYAN}  📖  HOW TO PLAY{RESET}", delay=0.025)
    divider("═")
    rules = [
        "  🎯  Answer multiple-choice questions (A / B / C / D)",
        "  ⏱   Each level has a per-question time limit",
        "  ✅  Score points for correct answers",
        "  ⚡  Answer in under HALF the time for a speed bonus!",
        "  📈  You need 3+ correct out of 5 to advance",
        "  🔥  Three levels: Easy → Medium → Hard",
        "  🏆  Final badge based on your total score",
    ]
    for rule in rules:
        slow_print(f"{YELLOW}{rule}{RESET}", delay=0.015)
    divider()
    print()
    input(f"  {GREEN}Press ENTER to continue...{RESET}")

# ─────────────────────────────────────────────
#  HIGH SCORE FILE (simple persistence)
# ─────────────────────────────────────────────

SCORE_FILE = "brain_blast_scores.txt"

def save_score(name, score):
    """Append score to a simple text leaderboard file."""
    with open(SCORE_FILE, "a") as f:
        timestamp = time.strftime("%Y-%m-%d %H:%M")
        f.write(f"{timestamp} | {name:<20} | {score:>5} pts\n")

def show_leaderboard():
    """Display the top scores saved locally."""
    if not os.path.exists(SCORE_FILE):
        print(f"  {YELLOW}No scores saved yet!{RESET}")
        return
    print(f"\n  {BOLD}{CYAN}🏅  TOP SCORES{RESET}")
    divider()
    with open(SCORE_FILE) as f:
        lines = f.readlines()
    # Sort by score descending
    try:
        sorted_lines = sorted(
            lines,
            key=lambda l: int(l.split("|")[2].strip().split()[0]),
            reverse=True
        )
        for i, line in enumerate(sorted_lines[:10], 1):
            print(f"  {YELLOW}#{i:<2}{RESET}  {line.strip()}")
    except Exception:
        for line in lines[-10:]:
            print(f"  {line.strip()}")
    divider()

# ─────────────────────────────────────────────
#  MAIN GAME LOOP
# ─────────────────────────────────────────────

def main():
    max_possible_score = QUESTIONS_PER_LEVEL * (30 + 5) * 3  # Hard pts + speed bonus × 3 levels
    levels = [("easy", 1), ("medium", 2), ("hard", 3)]

    while True:
        # ── Welcome screen ──────────────────────────
        banner()
        print(f"  {YELLOW}Welcome to Brain Blast — the ultimate timed quiz!{RESET}\n")

        # Menu
        print(f"  {BOLD}MAIN MENU{RESET}")
        print(f"  {CYAN}1{RESET} → Play Game")
        print(f"  {CYAN}2{RESET} → How to Play")
        print(f"  {CYAN}3{RESET} → Leaderboard")
        print(f"  {CYAN}4{RESET} → Quit")
        print()
        choice = input(f"  {BOLD}Enter choice (1-4): {RESET}").strip()

        if choice == "2":
            show_instructions()
            continue
        elif choice == "3":
            clear()
            banner()
            show_leaderboard()
            print()
            input(f"  {GREEN}Press ENTER to return to menu...{RESET}")
            continue
        elif choice == "4":
            clear()
            banner()
            slow_print(f"\n  {CYAN}Thanks for playing Brain Blast! Goodbye! 👋{RESET}")
            print()
            break
        elif choice != "1":
            print(f"\n  {RED}Please enter 1, 2, 3, or 4.{RESET}")
            time.sleep(1)
            continue

        # ── Get player name ──────────────────────────
        print()
        player_name = input(f"  {BOLD}Enter your name, challenger: {RESET}").strip()
        if not player_name:
            player_name = "Champion"

        # ── Brief welcome ────────────────────────────
        clear()
        banner()
        slow_print(f"\n  {GREEN}{BOLD}🎮  Welcome, {player_name}! Let the quiz begin!{RESET}")
        print(f"  {YELLOW}You'll face 3 levels — Easy, Medium, and Hard.{RESET}")
        print(f"  {YELLOW}Answer correctly AND quickly for maximum points!{RESET}\n")
        time.sleep(2)

        # ── Play through levels ──────────────────────
        total_score = 0
        game_complete = True

        for level_key, level_num in levels:
            level_score, passed = play_level(
                level_key, level_num, player_name, total_score
            )
            total_score += level_score

            if not passed:
                game_complete = False
                time.sleep(2)
                break  # Eliminated — stop here

            if level_num < 3:  # More levels ahead
                input(f"\n  {GREEN}Press ENTER to continue to Level {level_num + 1}...{RESET}")

        # ── Final results ────────────────────────────
        clear()
        banner()
        divider("═")
        print(f"\n  {BOLD}{CYAN}🎊  GAME OVER — FINAL RESULTS  🎊{RESET}")
        divider("═")
        print(f"\n  {BOLD}Player : {YELLOW}{player_name}{RESET}")
        print(f"  {BOLD}Score  : {GREEN}{total_score} pts{RESET}  "
              f"(out of {max_possible_score} possible)")

        badge_title, badge_msg = performance_badge(total_score, max_possible_score)
        print(f"\n  {badge_title}")
        print(f"  {YELLOW}{badge_msg}{RESET}")

        if game_complete:
            print(f"\n  {CYAN}🏅  You completed ALL THREE levels! Incredible!{RESET}")

        divider()

        # Save and show leaderboard
        save_score(player_name, total_score)
        show_leaderboard()

        # ── Play again? ──────────────────────────────
        print()
        again = input(f"  {BOLD}Play again? (Y/N): {RESET}").strip().upper()
        if again != "Y":
            clear()
            banner()
            slow_print(f"\n  {CYAN}Thanks for playing, {player_name}! "
                       f"Your final score was {total_score} pts. See you next time! 🧠{RESET}")
            print()
            break

# ─────────────────────────────────────────────
#  ENTRY POINT
# ─────────────────────────────────────────────

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n  {YELLOW}Game interrupted. Thanks for playing! 👋{RESET}\n")