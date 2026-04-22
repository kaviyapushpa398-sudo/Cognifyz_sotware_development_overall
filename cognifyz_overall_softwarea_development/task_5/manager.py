# ============================================================
#         📋  PERSISTENT TASK MANAGER  📋
#         File-Based Storage | Full CRUD | Auto-Save
# ============================================================

import os
import csv
import shutil
from datetime import datetime

# ── Constants ────────────────────────────────────────────────
TASKS_FILE   = "tasks.txt"
BACKUP_FILE  = "tasks_backup.txt"
DELIMITER    = "|"
FIELDS       = ["id", "title", "description", "status", "created_at"]

# ── Colour / Style Helpers ────────────────────────────────────
class C:
    RESET   = "\033[0m"
    BOLD    = "\033[1m"
    RED     = "\033[91m"
    GREEN   = "\033[92m"
    YELLOW  = "\033[93m"
    CYAN    = "\033[96m"
    MAGENTA = "\033[95m"
    BLUE    = "\033[94m"
    DIM     = "\033[2m"

def cprint(text, colour=C.RESET):
    print(f"{colour}{text}{C.RESET}")

def cinput(prompt, colour=C.CYAN):
    return input(f"{colour}{prompt}{C.RESET}").strip()

# ── Banner ────────────────────────────────────────────────────
def print_banner():
    cprint("\n" + "═" * 58, C.CYAN)
    cprint("       📋   PERSISTENT TASK MANAGER   📋", C.BOLD)
    cprint("    File-Backed Storage  •  Full CRUD  •  Auto-Save", C.DIM)
    cprint("═" * 58, C.CYAN)

# ── File Operations ───────────────────────────────────────────
def ensure_file():
    """Create the tasks file with a header row if it doesn't exist."""
    if not os.path.exists(TASKS_FILE):
        try:
            with open(TASKS_FILE, "w", encoding="utf-8") as f:
                f.write(DELIMITER.join(FIELDS) + "\n")
            cprint(f"  📁  Created new task file: '{TASKS_FILE}'", C.DIM)
        except IOError as e:
            cprint(f"  ❌  Could not create task file: {e}", C.RED)


def load_tasks():
    """Read all tasks from the file and return as a list of dicts."""
    ensure_file()
    tasks = []
    try:
        with open(TASKS_FILE, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f, delimiter=DELIMITER)
            for row in reader:
                tasks.append(dict(row))
        return tasks
    except FileNotFoundError:
        cprint("  ⚠️   Task file missing — starting fresh.", C.YELLOW)
        return []
    except Exception as e:
        cprint(f"  ❌  Error reading task file: {e}", C.RED)
        return []


def save_tasks(tasks):
    """Backup existing data, then write all tasks to the file."""
    try:
        # ── Backup before overwriting ──────────────────────────
        if os.path.exists(TASKS_FILE):
            shutil.copy2(TASKS_FILE, BACKUP_FILE)

        with open(TASKS_FILE, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDS, delimiter=DELIMITER)
            writer.writeheader()
            writer.writerows(tasks)
        return True
    except IOError as e:
        cprint(f"  ❌  Could not save tasks: {e}", C.RED)
        return False


def next_id(tasks):
    """Generate the next unique integer task ID."""
    if not tasks:
        return 1
    return max(int(t["id"]) for t in tasks) + 1


# ── Display Helpers ───────────────────────────────────────────
STATUS_ICONS = {"Pending": "🕐", "Completed": "✅"}
STATUS_COLORS = {"Pending": C.YELLOW, "Completed": C.GREEN}

def print_task_row(task, index=None):
    """Print a single task in a styled card format."""
    status      = task.get("status", "Pending")
    icon        = STATUS_ICONS.get(status, "🕐")
    col         = STATUS_COLORS.get(status, C.YELLOW)
    prefix      = f"  [{index}] " if index else "       "
    id_str      = f"{C.DIM}ID:{task['id']}{C.RESET}"
    title_str   = f"{C.BOLD}{task['title']}{C.RESET}"
    desc_str    = f"{C.DIM}{task['description'] or '—'}{C.RESET}"
    status_str  = f"{col}{icon} {status}{C.RESET}"
    date_str    = f"{C.DIM}{task.get('created_at', '')}{C.RESET}"

    print(f"{prefix}{title_str}  {id_str}")
    print(f"         📝 {desc_str}")
    print(f"         {status_str}   🗓️  {date_str}")
    print(f"  {'─' * 50}")


def view_tasks(tasks, sort_by_status=True):
    """Display all tasks, optionally sorted by status."""
    if not tasks:
        cprint("\n  📭  No tasks found. Add your first task!", C.YELLOW)
        return

    display = sorted(tasks, key=lambda t: t["status"]) if sort_by_status else tasks

    pending   = sum(1 for t in tasks if t["status"] == "Pending")
    completed = len(tasks) - pending

    cprint(f"\n  {'═' * 52}", C.CYAN)
    cprint(f"   📋  ALL TASKS   "
           f"Total: {C.BOLD}{len(tasks)}{C.RESET}  "
           f"{C.GREEN}✅ {completed}{C.RESET}  "
           f"{C.YELLOW}🕐 {pending}{C.RESET}", C.CYAN)
    cprint(f"  {'═' * 52}", C.CYAN)

    for i, task in enumerate(display, 1):
        print_task_row(task, index=i)


# ── CRUD Operations ───────────────────────────────────────────
def add_task(tasks):
    """Prompt user and add a new task."""
    cprint("\n  ╔══════════════════════════════════╗", C.GREEN)
    cprint("  ║        ➕  ADD NEW TASK           ║", C.GREEN)
    cprint("  ╚══════════════════════════════════╝", C.GREEN)

    title = cinput("  Title       : ")
    if not title:
        cprint("  ⚠️   Title cannot be empty!", C.YELLOW)
        return

    description = cinput("  Description : ")

    new_task = {
        "id"          : str(next_id(tasks)),
        "title"       : title,
        "description" : description,
        "status"      : "Pending",
        "created_at"  : datetime.now().strftime("%Y-%m-%d %H:%M"),
    }

    tasks.append(new_task)

    if save_tasks(tasks):
        cprint(f"\n  ✅  Task '{title}' added & saved! (ID: {new_task['id']})", C.GREEN)
    else:
        cprint("  ⚠️   Task added in memory but could not save to file.", C.YELLOW)


def update_task(tasks):
    """Allow the user to edit a task's title, description, or status."""
    if not tasks:
        cprint("\n  📭  No tasks to update.", C.YELLOW)
        return

    cprint("\n  ╔══════════════════════════════════╗", C.BLUE)
    cprint("  ║        ✏️   UPDATE TASK           ║", C.BLUE)
    cprint("  ╚══════════════════════════════════╝", C.BLUE)

    view_tasks(tasks, sort_by_status=False)

    try:
        task_id = cinput("  Enter Task ID to update: ", C.BLUE)
        task    = next((t for t in tasks if t["id"] == task_id), None)
    except Exception:
        task = None

    if not task:
        cprint(f"  ❌  No task found with ID '{task_id}'.", C.RED)
        return

    cprint(f"\n  Editing: {C.BOLD}{task['title']}{C.RESET}", C.BLUE)
    cprint("  (Press Enter to keep the current value)\n", C.DIM)

    new_title = cinput(f"  New Title       [{task['title']}] : ", C.BLUE)
    new_desc  = cinput(f"  New Description [{task['description'] or '—'}] : ", C.BLUE)

    cprint("  Status options: 1 = Pending   2 = Completed", C.DIM)
    status_choice = cinput("  New Status      (1/2, or Enter to keep) : ", C.BLUE)

    if new_title:
        task["title"] = new_title
    if new_desc:
        task["description"] = new_desc
    if status_choice == "1":
        task["status"] = "Pending"
    elif status_choice == "2":
        task["status"] = "Completed"

    if save_tasks(tasks):
        cprint(f"\n  ✅  Task ID {task_id} updated & saved!", C.GREEN)
    else:
        cprint("  ⚠️   Updated in memory but could not save to file.", C.YELLOW)


def delete_task(tasks):
    """Remove a task after user confirmation."""
    if not tasks:
        cprint("\n  📭  No tasks to delete.", C.YELLOW)
        return

    cprint("\n  ╔══════════════════════════════════╗", C.RED)
    cprint("  ║        🗑️   DELETE TASK           ║", C.RED)
    cprint("  ╚══════════════════════════════════╝", C.RED)

    view_tasks(tasks, sort_by_status=False)

    task_id = cinput("  Enter Task ID to delete: ", C.RED)
    task    = next((t for t in tasks if t["id"] == task_id), None)

    if not task:
        cprint(f"  ❌  No task found with ID '{task_id}'.", C.RED)
        return

    cprint(f"\n  ⚠️   You are about to delete: {C.BOLD}{task['title']}{C.RESET}", C.YELLOW)
    confirm = cinput("  Are you sure? (yes / no): ", C.YELLOW).lower()

    if confirm not in ("yes", "y"):
        cprint("  ↩️   Deletion cancelled.", C.DIM)
        return

    tasks.remove(task)

    if save_tasks(tasks):
        cprint(f"\n  🗑️   Task '{task['title']}' deleted & file updated!", C.GREEN)
    else:
        cprint("  ⚠️   Deleted in memory but could not save to file.", C.YELLOW)


# ── Menu ──────────────────────────────────────────────────────
def print_menu():
    cprint("\n  ┌────────────────────────────────────┐", C.CYAN)
    cprint("  │           MAIN  MENU               │", C.CYAN)
    cprint("  ├────────────────────────────────────┤", C.CYAN)
    cprint("  │  1️⃣   Add Task                      │", C.CYAN)
    cprint("  │  2️⃣   View All Tasks                │", C.CYAN)
    cprint("  │  3️⃣   Update Task                   │", C.CYAN)
    cprint("  │  4️⃣   Delete Task                   │", C.CYAN)
    cprint("  │  5️⃣   Exit                          │", C.CYAN)
    cprint("  └────────────────────────────────────┘", C.CYAN)


def get_menu_choice():
    while True:
        choice = cinput("  👉  Enter choice (1–5): ")
        if choice in ("1", "2", "3", "4", "5"):
            return choice
        cprint(f"  ⚠️   '{choice}' is not valid. Please enter 1, 2, 3, 4, or 5.", C.YELLOW)


# ── Main ──────────────────────────────────────────────────────
def main():
    print_banner()

    # Load tasks on startup
    tasks = load_tasks()
    count = len(tasks)

    if count > 0:
        cprint(f"\n  📂  Loaded {C.BOLD}{count}{C.RESET} task(s) from '{TASKS_FILE}'.", C.GREEN)
        pending   = sum(1 for t in tasks if t["status"] == "Pending")
        completed = count - pending
        cprint(f"      ✅ {completed} Completed   🕐 {pending} Pending", C.DIM)
    else:
        cprint(f"\n  📂  No existing tasks found. Starting fresh.", C.DIM)

    while True:
        print_menu()
        choice = get_menu_choice()

        if   choice == "1":
            add_task(tasks)
        elif choice == "2":
            view_tasks(tasks)
        elif choice == "3":
            update_task(tasks)
        elif choice == "4":
            delete_task(tasks)
        elif choice == "5":
            cprint("\n" + "═" * 58, C.CYAN)
            cprint("  👋  Thanks for using Task Manager. See you soon!", C.BOLD)
            cprint(f"  💾  All data is safely stored in '{TASKS_FILE}'.", C.DIM)
            cprint("═" * 58 + "\n", C.CYAN)
            break


# ── Entry Point ───────────────────────────────────────────────
if __name__ == "__main__":
    main()