import os
import subprocess
import random
from datetime import datetime, timedelta

# ============================================
# GitHub Green Calendar Script
# - Weekdays only (skip Sat/Sun)
# - 1-2 commits per day
# - Real file changes (not just README)
# ============================================

# Different types of changes to make it look real
CHANGES = [
    {
        "folder": "logs",
        "ext": ".log",
        "content": lambda d: f"[{d}] Server started successfully\nStatus: OK\nMemory: {random.randint(40,90)}%\nCPU: {random.randint(10,80)}%\n"
    },
    {
        "folder": "notes",
        "ext": ".txt",
        "content": lambda d: f"Date: {d}\nTask: {random.choice(['Bug fix','Feature update','Code review','Testing','Optimization','Refactoring','Documentation'])}\nStatus: {random.choice(['Done','In Progress','Completed'])}\nPriority: {random.choice(['High','Medium','Low'])}\n"
    },
    {
        "folder": "config",
        "ext": ".cfg",
        "content": lambda d: f"# Config updated on {d}\nDEBUG={random.choice(['True','False'])}\nVERSION=1.{random.randint(0,9)}.{random.randint(0,99)}\nMAX_CONNECTIONS={random.randint(50,500)}\nTIMEOUT={random.randint(10,120)}\n"
    },
    {
        "folder": "data",
        "ext": ".json",
        "content": lambda d: f'{{"date": "{d}", "records": {random.randint(10,500)}, "status": "{random.choice(["active","updated","synced"])}", "version": "{random.randint(1,5)}.{random.randint(0,9)}"}}\n'
    },
    {
        "folder": "tests",
        "ext": ".py",
        "content": lambda d: f'# Test file - {d}\nimport unittest\n\nclass Test_{d.replace("-","_")}(unittest.TestCase):\n    def test_status(self):\n        self.assertEqual({random.randint(1,100)}, {random.randint(1,100)})\n\nif __name__ == "__main__":\n    unittest.main()\n'
    },
]

COMMIT_MESSAGES = [
    "fix: resolve minor bug in module",
    "feat: add new utility function",
    "refactor: clean up code structure",
    "chore: update configuration",
    "docs: update project notes",
    "test: add unit test cases",
    "fix: patch security issue",
    "feat: improve performance",
    "chore: update dependencies",
    "refactor: optimize database queries",
    "fix: handle edge case in validation",
    "feat: add error logging",
    "chore: clean up temp files",
    "test: add integration tests",
    "fix: correct data format issue",
    "feat: add data export feature",
    "refactor: simplify helper functions",
    "docs: add inline comments",
    "fix: resolve merge conflict",
    "chore: update project config",
]


def run_cmd(cmd, cwd=None, env=None):
    """Run a shell command"""
    full_env = os.environ.copy()
    if env:
        full_env.update(env)
    result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True, env=full_env)
    return result.returncode, result.stdout, result.stderr


def get_weekdays(start_date, end_date):
    """Get all weekdays between two dates"""
    days = []
    current = start_date
    while current <= end_date:
        # 0=Monday ... 4=Friday, 5=Saturday, 6=Sunday
        if current.weekday() < 5:
            days.append(current)
        current += timedelta(days=1)
    return days


def make_commit(project_path, date, commit_num):
    """Make a single backdated commit with real file changes"""
    change = random.choice(CHANGES)
    folder_path = os.path.join(project_path, change["folder"])
    os.makedirs(folder_path, exist_ok=True)

    # Create/modify a file
    date_str = date.strftime("%Y-%m-%d")
    filename = f"{date_str}_v{commit_num}{change['ext']}"
    filepath = os.path.join(folder_path, filename)

    with open(filepath, "w") as f:
        f.write(change["content"](date_str))

    # Random time during work hours (9 AM - 6 PM)
    hour = random.randint(9, 18)
    minute = random.randint(0, 59)
    second = random.randint(0, 59)
    commit_date = date.replace(hour=hour, minute=minute, second=second)
    date_iso = commit_date.strftime("%Y-%m-%dT%H:%M:%S")

    # Git add and commit with backdated date
    run_cmd('git add .', cwd=project_path)

    commit_msg = random.choice(COMMIT_MESSAGES)
    date_env = {
        "GIT_AUTHOR_DATE": date_iso,
        "GIT_COMMITTER_DATE": date_iso,
        "GIT_AUTHOR_NAME": "mabdullah525",
        "GIT_AUTHOR_EMAIL": "abdullahbinabdullah005@gmail.com",
        "GIT_COMMITTER_NAME": "mabdullah525",
        "GIT_COMMITTER_EMAIL": "abdullahbinabdullah005@gmail.com",
    }
    cmd = f'git commit -m "{commit_msg}"'
    code, out, err = run_cmd(cmd, cwd=project_path, env=date_env)

    if code == 0:
        print(f"  [OK] {date_str} | Commit #{commit_num} | {commit_msg}")
    else:
        print(f"  [FAIL] {date_str} | {err.strip()}")


def main():
    print("=" * 55)
    print("  GitHub Green Calendar - Backdated Commits Script")
    print("=" * 55)

    # Get project path
    script_dir = os.path.dirname(os.path.abspath(__file__))
    print(f"\n  Project folder: {script_dir}")

    # Check if git repo exists
    if not os.path.exists(os.path.join(script_dir, ".git")):
        print("\n  [!] No .git folder found. Initializing git...")
        run_cmd("git init", cwd=script_dir)

    # Get date range from user
    print("\n  Enter date range (format: YYYY-MM-DD)")
    print("  Example: 2025-01-01")
    print()

    while True:
        start_input = input("  Start date: ").strip()
        try:
            start_date = datetime.strptime(start_input, "%Y-%m-%d")
            break
        except ValueError:
            print("  [!] Wrong format! Use YYYY-MM-DD")

    while True:
        end_input = input("  End date:   ").strip()
        try:
            end_date = datetime.strptime(end_input, "%Y-%m-%d")
            if end_date >= start_date:
                break
            else:
                print("  [!] End date must be after start date!")
        except ValueError:
            print("  [!] Wrong format! Use YYYY-MM-DD")

    # Get weekdays
    weekdays = get_weekdays(start_date, end_date)
    total_commits = 0

    print(f"\n  Total weekdays found: {len(weekdays)}")
    print(f"  Estimated commits: {len(weekdays)} - {len(weekdays) * 2}")
    print()

    confirm = input("  Start? (y/n): ").strip().lower()
    if confirm != "y":
        print("  Cancelled!")
        return

    print("\n" + "-" * 55)
    print("  Creating commits...")
    print("-" * 55)

    for day in weekdays:
        num_commits = random.randint(1, 2)
        for i in range(1, num_commits + 1):
            make_commit(script_dir, day, i)
            total_commits += 1

    print("\n" + "=" * 55)
    print(f"  DONE! Total commits created: {total_commits}")
    print(f"  Weekdays covered: {len(weekdays)}")
    print("=" * 55)

    print("\n  Next steps:")
    print("  1. Create a new PUBLIC repo on GitHub")
    print("  2. Run these commands:")
    print(f"     git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git")
    print(f"     git branch -M main")
    print(f"     git push -u origin main")
    print()


if __name__ == "__main__":
    main()
