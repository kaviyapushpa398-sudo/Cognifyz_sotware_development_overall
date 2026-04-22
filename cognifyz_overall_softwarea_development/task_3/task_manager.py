"""
╔══════════════════════════════════════════════════════════════╗
║              ✦  TASK MANAGER PRO  ✦                         ║
║          Console CRUD Application · Python OOP              ║
╚══════════════════════════════════════════════════════════════╝
"""

import os
import time
import sys
from datetime import datetime


# ─── ANSI Colors ─────────────────────────────────────────────
class C:
    RESET   = "\033[0m"
    BOLD    = "\033[1m"
    DIM     = "\033[2m"
    CYAN    = "\033[96m"
    MAGENTA = "\033[95m"
    YELLOW  = "\033[93m"
    GREEN   = "\033[92m"
    RED     = "\033[91m"
    BLUE    = "\033[94m"
    WHITE   = "\033[97m"
    ORANGE  = "\033[38;5;208m"
    GRAY    = "\033[38;5;245m"

def clr(text, *codes):
    return "".join(codes) + str(text) + C.RESET

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def typewrite(text, delay=0.015):
    for ch in text:
        sys.stdout.write(ch)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def divider(char="─", width=62, color=C.CYAN):
    print(clr(char * width, color))

def press_enter():
    input(clr("\n  [ Press Enter to continue ]", C.DIM))


# ─── Task Class ───────────────────────────────────────────────
class Task:
    _id_counter = 1

    def __init__(self, title: str, description: str = ""):
        self.id          = Task._id_counter
        Task._id_counter += 1
        self.title       = title.strip()
        self.description = description.strip()
        self.status      = "Pending"
        self.created_at  = datetime.now().strftime("%d %b %Y  %H:%M")
        self.updated_at  = None

    def complete(self):
        self.status     = "Completed"
        self.updated_at = datetime.now().strftime("%d %b %Y  %H:%M")

    def update(self, title=None, description=None):
        if title:
            self.title = title.strip()
        if description is not None:
            self.description = description.strip()
        self.updated_at = datetime.now().strftime("%d %b %Y  %H:%M")

    def status_badge(self):
        if self.status == "Completed":
            return clr(" ✔ DONE ", C.GREEN, C.BOLD)
        return clr(" ◌ PENDING ", C.YELLOW)

    def __repr__(self):
        return f"Task(id={self.id}, title='{self.title}', status='{self.status}')"


# ─── Task Manager ─────────────────────────────────────────────
class TaskManager:
    def __init__(self):
        self.tasks: list[Task] = []
        self._seed_demo_tasks()

    def _seed_demo_tasks(self):
        """Add a couple of demo tasks on first launch."""
        t1 = Task("Set up Python environment", "Install Python 3.11+, pip, and virtualenv.")
        t2 = Task("Read OOP documentation", "Study classes, inheritance, and encapsulation.")
        t2.complete()
        t3 = Task("Build Task Manager app", "Console CRUD app with color output and search.")
        self.tasks.extend([t1, t2, t3])

    # ── Helpers ──────────────────────────────────────────────
    def _find(self, task_id: int) -> Task | None:
        return next((t for t in self.tasks if t.id == task_id), None)

    def _stats(self):
        total     = len(self.tasks)
        done      = sum(1 for t in self.tasks if t.status == "Completed")
        pending   = total - done
        return total, done, pending

    # ── CREATE ───────────────────────────────────────────────
    def add_task(self):
        _section_header("ADD NEW TASK", "▲", C.CYAN)
        print(clr("  Leave a field empty to cancel.\n", C.DIM))

        title = input(clr("  Title       : ", C.CYAN)).strip()
        if not title:
            print(clr("\n  ✕ Cancelled — title cannot be empty.", C.RED))
            press_enter(); return

        desc  = input(clr("  Description : ", C.CYAN)).strip()
        task  = Task(title, desc)
        self.tasks.append(task)
        print(clr(f"\n  ✔ Task #{task.id} created successfully!", C.GREEN, C.BOLD))
        press_enter()

    # ── READ ─────────────────────────────────────────────────
    def view_tasks(self, tasks=None, title="ALL TASKS"):
        _section_header(title, "◆", C.MAGENTA)
        source = tasks if tasks is not None else self.tasks

        total, done, pending = self._stats()
        print(clr(f"  Total: {total}  ", C.WHITE) +
              clr(f"✔ Done: {done}  ", C.GREEN) +
              clr(f"◌ Pending: {pending}", C.YELLOW))
        divider("·", 62, C.GRAY)

        if not source:
            print(clr("\n  No tasks found.\n", C.DIM))
            press_enter(); return

        for t in source:
            id_str    = clr(f"  #{t.id:<4}", C.ORANGE, C.BOLD)
            badge     = t.status_badge()
            title_str = clr(t.title, C.WHITE, C.BOLD)
            print(f"{id_str} {badge}  {title_str}")

            if t.description:
                print(clr(f"        {t.description}", C.GRAY))

            meta = clr(f"        Created: {t.created_at}", C.DIM)
            if t.updated_at:
                meta += clr(f"  ·  Updated: {t.updated_at}", C.DIM)
            print(meta)
            divider("·", 62, C.GRAY)

        press_enter()

    # ── UPDATE ───────────────────────────────────────────────
    def update_task(self):
        _section_header("UPDATE TASK", "✎", C.YELLOW)
        self._quick_list()

        try:
            task_id = int(input(clr("\n  Enter Task ID to update: ", C.YELLOW)))
        except ValueError:
            print(clr("  ✕ Invalid ID — must be a number.", C.RED))
            press_enter(); return

        task = self._find(task_id)
        if not task:
            print(clr(f"  ✕ No task found with ID #{task_id}.", C.RED))
            press_enter(); return

        print(clr(f"\n  Editing: ", C.DIM) + clr(task.title, C.WHITE, C.BOLD) +
              f"  {task.status_badge()}")
        print(clr("  (Press Enter to keep current value)\n", C.DIM))

        print(clr("  What would you like to do?", C.CYAN))
        print(clr("    [1] Edit title / description", C.WHITE))
        print(clr("    [2] Mark as Completed", C.GREEN))
        print(clr("    [3] Mark as Pending", C.YELLOW))
        print(clr("    [0] Cancel\n", C.GRAY))

        choice = input(clr("  Choice: ", C.YELLOW)).strip()

        if choice == "1":
            new_title = input(clr(f"  New title [{task.title}]: ", C.CYAN)).strip()
            new_desc  = input(clr(f"  New description [{task.description or '—'}]: ", C.CYAN)).strip()
            task.update(
                title=new_title if new_title else None,
                description=new_desc if new_desc != "" else None
            )
            print(clr(f"\n  ✔ Task #{task.id} updated.", C.GREEN, C.BOLD))
        elif choice == "2":
            task.complete()
            print(clr(f"\n  ✔ Task #{task.id} marked as Completed!", C.GREEN, C.BOLD))
        elif choice == "3":
            task.status     = "Pending"
            task.updated_at = datetime.now().strftime("%d %b %Y  %H:%M")
            print(clr(f"\n  ✔ Task #{task.id} marked as Pending.", C.YELLOW))
        elif choice == "0":
            print(clr("\n  Cancelled.", C.GRAY))
        else:
            print(clr("\n  ✕ Invalid choice.", C.RED))

        press_enter()

    # ── DELETE ───────────────────────────────────────────────
    def delete_task(self):
        _section_header("DELETE TASK", "✕", C.RED)
        self._quick_list()

        try:
            task_id = int(input(clr("\n  Enter Task ID to delete: ", C.RED)))
        except ValueError:
            print(clr("  ✕ Invalid ID — must be a number.", C.RED))
            press_enter(); return

        task = self._find(task_id)
        if not task:
            print(clr(f"  ✕ No task found with ID #{task_id}.", C.RED))
            press_enter(); return

        print(clr(f"\n  About to delete: ", C.DIM) + clr(task.title, C.WHITE, C.BOLD))
        confirm = input(clr("  Are you sure? (yes/no): ", C.RED)).strip().lower()

        if confirm in ("yes", "y"):
            self.tasks.remove(task)
            print(clr(f"\n  ✔ Task #{task_id} deleted successfully.", C.GREEN))
        else:
            print(clr("\n  Deletion cancelled.", C.GRAY))

        press_enter()

    # ── SEARCH ───────────────────────────────────────────────
    def search_tasks(self):
        _section_header("SEARCH TASKS", "⌕", C.BLUE)
        keyword = input(clr("  Enter keyword: ", C.BLUE)).strip().lower()
        if not keyword:
            print(clr("  ✕ Keyword cannot be empty.", C.RED))
            press_enter(); return

        results = [
            t for t in self.tasks
            if keyword in t.title.lower() or keyword in t.description.lower()
        ]
        self.view_tasks(results, title=f'RESULTS FOR "{keyword.upper()}"')

    # ── FILTER ───────────────────────────────────────────────
    def filter_tasks(self):
        _section_header("FILTER TASKS", "▽", C.ORANGE)
        print(clr("    [1] Pending tasks only", C.YELLOW))
        print(clr("    [2] Completed tasks only", C.GREEN))
        print(clr("    [0] Back\n", C.GRAY))

        choice = input(clr("  Filter: ", C.ORANGE)).strip()
        if choice == "1":
            filtered = [t for t in self.tasks if t.status == "Pending"]
            self.view_tasks(filtered, title="PENDING TASKS")
        elif choice == "2":
            filtered = [t for t in self.tasks if t.status == "Completed"]
            self.view_tasks(filtered, title="COMPLETED TASKS")
        elif choice == "0":
            return
        else:
            print(clr("  ✕ Invalid choice.", C.RED))
            press_enter()

    # ── QUICK LIST (for update/delete prompts) ────────────────
    def _quick_list(self):
        if not self.tasks:
            print(clr("  No tasks available.", C.DIM))
            return
        print(clr("\n  ID    Status       Title", C.GRAY))
        divider("·", 50, C.GRAY)
        for t in self.tasks:
            badge = clr("✔", C.GREEN) if t.status == "Completed" else clr("◌", C.YELLOW)
            print(f"  {clr(f'#{t.id:<4}', C.ORANGE)} {badge} {'Done   ' if t.status == 'Completed' else 'Pending'}  {clr(t.title, C.WHITE)}")


# ─── UI Helpers ───────────────────────────────────────────────
def _section_header(title, icon, color):
    clear()
    divider("═", 62, color)
    print(clr(f"  {icon}  {title}", color, C.BOLD))
    divider("═", 62, color)
    print()

def show_banner():
    clear()
    print(clr("""
  ╔══════════════════════════════════════════════════════════╗
  ║                                                          ║
  ║    ████████╗ █████╗ ███████╗██╗  ██╗    ███╗   ███╗    ║
  ║       ██╔══╝██╔══██╗██╔════╝██║ ██╔╝    ████╗ ████║    ║
  ║       ██║   ███████║███████╗█████╔╝     ██╔████╔██║    ║
  ║       ██║   ██╔══██║╚════██║██╔═██╗     ██║╚██╔╝██║    ║
  ║       ██║   ██║  ██║███████║██║  ██╗    ██║ ╚═╝ ██║    ║
  ║       ╚═╝   ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝   ╚═╝     ╚═╝    ║
  ║                                                          ║
  ║           M A N A G E R   P R O  ·  v1.0               ║
  ╚══════════════════════════════════════════════════════════╝
""", C.CYAN, C.BOLD))
    typewrite(clr("  Initializing Task Engine...  ✦\n", C.DIM), delay=0.012)
    time.sleep(0.3)

def show_menu(manager: TaskManager):
    total, done, pending = manager._stats()
    clear()
    divider("═", 62, C.CYAN)
    print(clr("  ✦  TASK MANAGER PRO", C.CYAN, C.BOLD) +
          clr(f"              Total:{total}  ✔{done}  ◌{pending}", C.GRAY))
    divider("═", 62, C.CYAN)

    menu_items = [
        ("1", "Add Task",         "▲", C.GREEN),
        ("2", "View All Tasks",   "◆", C.MAGENTA),
        ("3", "Update Task",      "✎", C.YELLOW),
        ("4", "Delete Task",      "✕", C.RED),
        ("5", "Search Tasks",     "⌕", C.BLUE),
        ("6", "Filter Tasks",     "▽", C.ORANGE),
        ("0", "Exit",             "·", C.GRAY),
    ]

    for key, label, icon, col in menu_items:
        print(f"  {clr(f'[{key}]', C.WHITE, C.BOLD)}  {clr(icon, col)}  {clr(label, C.WHITE)}")

    divider("─", 62, C.GRAY)
    return input(clr("  Your choice: ", C.CYAN)).strip()


# ─── Main ─────────────────────────────────────────────────────
def main():
    show_banner()
    manager = TaskManager()
    time.sleep(0.5)

    handlers = {
        "1": manager.add_task,
        "2": manager.view_tasks,
        "3": manager.update_task,
        "4": manager.delete_task,
        "5": manager.search_tasks,
        "6": manager.filter_tasks,
    }

    while True:
        choice = show_menu(manager)

        if choice == "0":
            clear()
            print(clr("\n  ✦ Thank you for using Task Manager Pro. Goodbye!\n", C.MAGENTA, C.BOLD))
            break
        elif choice in handlers:
            handlers[choice]()
        else:
            print(clr("\n  ✕ Invalid option. Choose 0–6.", C.RED))
            time.sleep(1)


if __name__ == "__main__":
    main()