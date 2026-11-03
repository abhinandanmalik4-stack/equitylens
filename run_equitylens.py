"""Launch this checkout with its own environment, without activating a shell."""

import argparse
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
ENVIRONMENT_PROBE = """
import pathlib
import sys
import equitylens

actual = pathlib.Path(equitylens.__file__).resolve().parent
expected = pathlib.Path(sys.argv[1]).resolve() / 'src' / 'equitylens'
if actual != expected:
    raise SystemExit('equitylens imports from another installation')

import streamlit
import pandas
import numpy
import plotly
print('Python: ' + sys.executable)
print('Project package: ' + str(actual))
"""


def environment_python(root: Path) -> Path:
    return root / ".venv" / ("Scripts/python.exe" if sys.platform == "win32" else "bin/python")


def main(argv=None, *, root: Path = ROOT) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Check imports without starting a server")
    parser.add_argument("--port", type=int, default=8501, help="Local port (default: 8501)")
    args = parser.parse_args(argv)
    if not 1024 <= args.port <= 65535:
        parser.error("Choose a port between 1024 and 65535.")
    root = root.resolve()
    python = environment_python(root)
    if not python.is_file() or not (root / "app.py").is_file():
        print("The project needs app.py and a .venv environment. Follow docs/RUN_AND_LEARN.md for setup.", file=sys.stderr)
        return 2
    # Verify the local editable package rather than accepting another checkout.
    try:
        result = subprocess.run([str(python), "-c", ENVIRONMENT_PROBE, str(root)], cwd=root,
                                capture_output=True, text=True, timeout=30)
        if result.returncode:
            print(result.stderr.strip(), file=sys.stderr)
            print("Install the project into its own environment from the project folder:", file=sys.stderr)
            print(f'"{python}" -m pip install -r requirements-lock.txt -e .', file=sys.stderr)
            print("In PowerShell, put & before the quoted Python path.", file=sys.stderr)
            return 2
        print(result.stdout.strip(), flush=True)
        if args.check:
            print("Environment check passed. No server was started.")
            return 0
        command = [str(python), "-m", "streamlit", "run", str(root / "app.py"),
                   "--server.address", "127.0.0.1", "--server.port", str(args.port)]
        print(f"Starting EquityLens at http://127.0.0.1:{args.port}. Stop with Ctrl+C.", flush=True)
        return subprocess.run(command, cwd=root).returncode
    except subprocess.TimeoutExpired:
        print("The environment check timed out. Check .venv and try again.", file=sys.stderr)
        return 2
    except OSError as exc:
        print(f"Could not start the project environment: {exc}", file=sys.stderr)
        return 2
    except KeyboardInterrupt:
        return 130


if __name__ == "__main__":
    raise SystemExit(main())
