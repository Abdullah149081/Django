# run.py
import os
import sys
import subprocess
from pathlib import Path
import shutil

VENV_DIR = "venv"
TAILWIND_DIR = "theme"

IS_WINDOWS = os.name == "nt"

COMMANDS = {
    "migrate": "python manage.py migrate",
    "makemigrations": "python manage.py makemigrations",
    "runserver": "python manage.py runserver",
    "tailwind": "python manage.py tailwind start",
    "start": "combined_start",
}


def run_shell(cmd, check=True):
    print(f"\n▶ {cmd}")
    try:
        subprocess.run(cmd, shell=True, check=check)
    except subprocess.CalledProcessError as e:
        print(f"❌ Command failed: {e}")
        sys.exit(e.returncode)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)


def venv_exists():
    venv_path = Path(VENV_DIR)
    if IS_WINDOWS:
        return (venv_path / "Scripts" / "activate").exists()
    else:
        return (venv_path / "bin" / "activate").exists()


def tailwind_dir_exists():
    return Path(TAILWIND_DIR).is_dir()


def combined_start():
    if not venv_exists():
        print(f"❌ Virtual environment not found in '{VENV_DIR}'.")
        sys.exit(1)
    if not tailwind_dir_exists():
        print(f"❌ Tailwind directory '{TAILWIND_DIR}' not found.")
        sys.exit(1)

    tailwind_path = Path(TAILWIND_DIR).resolve()
    venv_path = Path(VENV_DIR).resolve()

    if IS_WINDOWS:
        activate = venv_path / "Scripts" / "Activate.ps1"
        if not activate.exists():
            print(f"❌ Activate script not found: {activate}")
            sys.exit(1)
        tailwind_cmd = (
            f"start powershell -NoExit -Command \"cd '{tailwind_path}'; "
            f"& '{activate}'; npm run dev\""
        )
    else:
        activate = venv_path / "bin" / "activate"
        if not activate.exists():
            print(f"❌ Activate script not found: {activate}")
            sys.exit(1)
        terminal = (
            shutil.which("gnome-terminal")
            or shutil.which("x-terminal-emulator")
            or shutil.which("konsole")
        )
        if not terminal:
            print("❌ No supported terminal emulator found.")
            sys.exit(1)
        tailwind_cmd = (
            f'{terminal} -- bash -c \'cd "{tailwind_path}" && '
            f'source "{activate}" && npm run dev; exec bash\''
        )

    print("🎨 Starting Tailwind watcher...")
    try:
        subprocess.Popen(tailwind_cmd, shell=True)
    except Exception as e:
        print(f"❌ Failed to start Tailwind watcher: {e}")
        sys.exit(1)

    print("🚀 Starting Django development server...")
    run_shell("python manage.py runserver")


def main():
    if len(sys.argv) < 2:
        print("Usage: python run.py <command>")
        print("Available commands:", ", ".join(COMMANDS.keys()))
        sys.exit(1)

    cmd = sys.argv[1]
    if cmd not in COMMANDS:
        print(f"❌ Unknown command: {cmd}")
        print("Available commands:", ", ".join(COMMANDS.keys()))
        sys.exit(1)

    if COMMANDS[cmd] == "combined_start":
        combined_start()
    else:
        run_shell(COMMANDS[cmd])


if __name__ == "__main__":
    main()
