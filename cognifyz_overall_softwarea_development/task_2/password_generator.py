"""
╔══════════════════════════════════════════════════════════╗
║           ✦  NUMBER PATTERN GENERATOR  ✦                 ║
║        Interactive Console Pattern Studio                ║
╚══════════════════════════════════════════════════════════╝
"""

import time
import os
import sys

# ─── ANSI Color Codes ────────────────────────────────────────
class Color:
    RESET      = "\033[0m"
    BOLD       = "\033[1m"
    DIM        = "\033[2m"

    CYAN       = "\033[96m"
    MAGENTA    = "\033[95m"
    YELLOW     = "\033[93m"
    GREEN      = "\033[92m"
    RED        = "\033[91m"
    BLUE       = "\033[94m"
    WHITE      = "\033[97m"
    ORANGE     = "\033[38;5;208m"
    PURPLE     = "\033[38;5;135m"
    PINK       = "\033[38;5;213m"

    BG_BLACK   = "\033[40m"
    BG_DARK    = "\033[48;5;234m"


# ─── Utility Functions ───────────────────────────────────────
def clear():
    os.system("cls" if os.name == "nt" else "clear")

def c(text, color):
    return f"{color}{text}{Color.RESET}"

def typewrite(text, delay=0.012):
    for ch in text:
        sys.stdout.write(ch)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def divider(char="─", width=60, color=Color.CYAN):
    print(c(char * width, color))

def pause(msg="Press Enter to continue..."):
    input(c(f"\n  {msg}", Color.DIM))


# ─── Banner ──────────────────────────────────────────────────
def show_banner():
    clear()
    banner = f"""
{Color.CYAN}{Color.BOLD}
  ╔══════════════════════════════════════════════════════════╗
  ║                                                          ║
  ║   {Color.YELLOW}  ███╗   ██╗██╗   ██╗███╗   ███╗██████╗ ████████╗  {Color.CYAN}║
  ║   {Color.YELLOW}  ████╗  ██║██║   ██║████╗ ████║██╔══██╗╚══██╔══╝  {Color.CYAN}║
  ║   {Color.YELLOW}  ██╔██╗ ██║██║   ██║██╔████╔██║██████╔╝   ██║     {Color.CYAN}║
  ║   {Color.YELLOW}  ██║╚██╗██║██║   ██║██║╚██╔╝██║██╔══██╗   ██║     {Color.CYAN}║
  ║   {Color.YELLOW}  ██║ ╚████║╚██████╔╝██║ ╚═╝ ██║██████╔╝   ██║     {Color.CYAN}║
  ║   {Color.YELLOW}  ╚═╝  ╚═══╝ ╚═════╝ ╚═╝     ╚═╝╚═════╝    ╚═╝     {Color.CYAN}║
  ║                                                          ║
  ║   {Color.MAGENTA}        ✦  P A T T E R N   S T U D I O  ✦          {Color.CYAN}║
  ║                                                          ║
  ╚══════════════════════════════════════════════════════════╝
{Color.RESET}"""
    print(banner)
    typewrite(c("  Initializing Pattern Engine...", Color.DIM), delay=0.018)
    time.sleep(0.4)
    typewrite(c("  Ready. Let the patterns begin ✦\n", Color.GREEN), delay=0.018)


# ─── Menu ────────────────────────────────────────────────────
def show_menu():
    print(c("\n  ┌─────────────────────────────────────────┐", Color.CYAN))
    print(c("  │       SELECT A PATTERN TYPE              │", Color.CYAN))
    print(c("  ├─────────────────────────────────────────┤", Color.CYAN))
    options = [
        ("1", "Pyramid Pattern",         "▲", Color.YELLOW),
        ("2", "Inverted Pyramid",        "▼", Color.ORANGE),
        ("3", "Number Triangle",         "◆", Color.MAGENTA),
        ("4", "Diamond Pattern ✦ Bonus", "◈", Color.PINK),
        ("5", "Pascal's Triangle",       "⬡", Color.GREEN),
        ("6", "Hollow Rectangle",        "□", Color.BLUE),
        ("0", "Exit",                    "✕", Color.RED),
    ]
    for key, label, icon, col in options:
        num_col = Color.WHITE if key != "0" else Color.RED
        print(f"  {c('│', Color.CYAN)}  {c(f'[{key}]', num_col)}  {c(icon, col)}  {c(label, Color.WHITE):<36}{c('│', Color.CYAN)}")
    print(c("  └─────────────────────────────────────────┘", Color.CYAN))


# ─── Input Validation ────────────────────────────────────────
def get_rows(min_rows=1, max_rows=20):
    while True:
        try:
            val = input(c(f"\n  Enter number of rows ({min_rows}–{max_rows}): ", Color.CYAN))
            rows = int(val)
            if rows < min_rows:
                print(c(f"  ⚠  Must be at least {min_rows}. Try again.", Color.RED))
            elif rows > max_rows:
                print(c(f"  ⚠  Max is {max_rows} for clean display. Try again.", Color.RED))
            else:
                return rows
        except ValueError:
            print(c("  ✕  Invalid input — please enter a whole number.", Color.RED))


# ─── Pattern Header ──────────────────────────────────────────
def pattern_header(name, rows, icon="✦"):
    print()
    divider("═", 60, Color.MAGENTA)
    print(c(f"  {icon}  Your Generated Pattern", Color.YELLOW + Color.BOLD))
    print(c(f"  Selected Pattern : {name}", Color.WHITE))
    print(c(f"  Rows             : {rows}", Color.WHITE))
    divider("═", 60, Color.MAGENTA)
    print()


def pattern_footer(elapsed):
    print()
    divider("─", 60, Color.DIM)
    print(c(f"  ⏱  Generated in {elapsed:.4f} seconds", Color.GREEN))
    divider("─", 60, Color.DIM)


# ─── Patterns ────────────────────────────────────────────────

# 1. Pyramid Pattern
def pyramid(rows):
    pattern_header("Pyramid Pattern", rows, "▲")
    start = time.perf_counter()
    for i in range(1, rows + 1):
        spaces = " " * (rows - i)
        nums = ""
        for j in range(1, 2 * i):
            col = Color.CYAN if j % 2 == 1 else Color.YELLOW
            nums += c(str(j if j <= i else 2 * i - j), col)
        print(f"  {spaces}{nums}")
    pattern_footer(time.perf_counter() - start)


# 2. Inverted Pyramid
def inverted_pyramid(rows):
    pattern_header("Inverted Pyramid", rows, "▼")
    start = time.perf_counter()
    for i in range(rows, 0, -1):
        spaces = " " * (rows - i)
        nums = ""
        for j in range(1, 2 * i):
            col = Color.ORANGE if j % 2 == 1 else Color.MAGENTA
            nums += c(str(j if j <= i else 2 * i - j), col)
        print(f"  {spaces}{nums}")
    pattern_footer(time.perf_counter() - start)


# 3. Number Triangle
def number_triangle(rows):
    pattern_header("Number Triangle", rows, "◆")
    start = time.perf_counter()
    num = 1
    colors = [Color.CYAN, Color.YELLOW, Color.MAGENTA, Color.GREEN, Color.ORANGE]
    for i in range(1, rows + 1):
        row_str = ""
        for j in range(1, i + 1):
            col = colors[(num - 1) % len(colors)]
            row_str += c(f"{num:3}", col)
            num += 1
        print(f"  {row_str}")
    pattern_footer(time.perf_counter() - start)


# 4. Diamond Pattern (Bonus)
def diamond(rows):
    pattern_header("Diamond Pattern ✦", rows, "◈")
    start = time.perf_counter()
    # Upper half
    for i in range(1, rows + 1):
        spaces = " " * (rows - i)
        nums = ""
        for j in range(1, 2 * i):
            col = Color.PINK if j % 2 == 1 else Color.PURPLE
            nums += c(str(j if j <= i else 2 * i - j), col)
        print(f"  {spaces}{nums}")
    # Lower half
    for i in range(rows - 1, 0, -1):
        spaces = " " * (rows - i)
        nums = ""
        for j in range(1, 2 * i):
            col = Color.PURPLE if j % 2 == 1 else Color.PINK
            nums += c(str(j if j <= i else 2 * i - j), col)
        print(f"  {spaces}{nums}")
    pattern_footer(time.perf_counter() - start)


# 5. Pascal's Triangle
def pascals_triangle(rows):
    pattern_header("Pascal's Triangle", rows, "⬡")
    start = time.perf_counter()
    row = [1]
    all_rows = []
    for _ in range(rows):
        all_rows.append(row)
        row = [1] + [row[j] + row[j + 1] for j in range(len(row) - 1)] + [1]

    # Determine width from last row
    width = sum(len(f"{n:^6}") for n in all_rows[-1])
    colors = [Color.CYAN, Color.GREEN, Color.YELLOW, Color.MAGENTA, Color.ORANGE, Color.PINK]

    for i, r in enumerate(all_rows):
        row_str = ""
        for j, n in enumerate(r):
            col = colors[(i + j) % len(colors)]
            row_str += c(f"{n:^6}", col)
        print(f"  {row_str.center(width + 2)}")
    pattern_footer(time.perf_counter() - start)


# 6. Hollow Rectangle
def hollow_rectangle(rows):
    pattern_header("Hollow Rectangle", rows, "□")
    cols = rows * 2 + 1
    start = time.perf_counter()
    for i in range(1, rows + 1):
        row_str = ""
        for j in range(1, cols + 1):
            is_border = (i == 1 or i == rows or j == 1 or j == cols)
            if is_border:
                col = Color.BLUE if (i + j) % 2 == 0 else Color.CYAN
                row_str += c(str((i + j) % 9 + 1), col)
            else:
                row_str += c("·", Color.DIM)
        print(f"  {row_str}")
    pattern_footer(time.perf_counter() - start)


# ─── Main Loop ───────────────────────────────────────────────
def main():
    show_banner()

    pattern_map = {
        "1": ("Pyramid Pattern",         pyramid),
        "2": ("Inverted Pyramid",        inverted_pyramid),
        "3": ("Number Triangle",         number_triangle),
        "4": ("Diamond Pattern",         diamond),
        "5": ("Pascal's Triangle",       pascals_triangle),
        "6": ("Hollow Rectangle",        hollow_rectangle),
    }

    while True:
        show_menu()
        choice = input(c("\n  Your choice: ", Color.YELLOW)).strip()

        if choice == "0":
            print(c("\n  ✦ Thank you for using Pattern Studio. Goodbye!\n", Color.MAGENTA))
            break

        if choice not in pattern_map:
            print(c("  ✕  Invalid choice. Please select from the menu.", Color.RED))
            time.sleep(1)
            continue

        name, fn = pattern_map[choice]
        print(c(f"\n  ✦ Pattern Selected: {name}", Color.GREEN))

        max_r = 12 if choice == "5" else 20
        rows = get_rows(max_rows=max_r)

        print(c("\n  Generating pattern...", Color.DIM))
        time.sleep(0.2)

        fn(rows)

        again = input(c("\n  Generate another pattern? (y/n): ", Color.CYAN)).strip().lower()
        if again != "y":
            print(c("\n  ✦ Thank you for using Pattern Studio. Goodbye!\n", Color.MAGENTA))
            break
        clear()
        show_banner()


if __name__ == "__main__":
    main()