from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

import run_equitylens as launcher


class LauncherTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="equitylens project ")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.python = launcher.environment_python(self.root)
        self.python.parent.mkdir(parents=True)
        self.python.touch()
        (self.root / "app.py").touch()

    def invoke(self, args):
        with redirect_stdout(StringIO()), redirect_stderr(StringIO()):
            return launcher.main(args, root=self.root)

    def test_missing_environment_does_not_launch_or_install(self):
        self.python.unlink()
        with patch.object(launcher.subprocess, "run") as run:
            self.assertEqual(self.invoke([]), 2)
            run.assert_not_called()

    def test_check_uses_project_python_and_starts_no_server(self):
        with patch.object(launcher.subprocess, "run", return_value=subprocess.CompletedProcess([], 0, "OK", "")) as run:
            self.assertEqual(self.invoke(["--check"]), 0)
            self.assertEqual(run.call_count, 1)
            self.assertEqual(run.call_args.args[0][0], str(self.python))
            self.assertEqual(run.call_args.kwargs["cwd"], self.root.resolve())

    def test_package_origin_guard_survives_python_optimization(self):
        # Stub dependencies isolate the origin check from their import time.
        source = self.root / "src"
        package = source / "equitylens"
        package.mkdir(parents=True)
        (package / "__init__.py").write_text("", encoding="utf-8")
        for name in ("streamlit", "pandas", "numpy", "plotly"):
            (source / f"{name}.py").write_text("", encoding="utf-8")
        for optimize in ([], ["-O"], ["-OO"]):
            for correct_checkout in (True, False):
                with self.subTest(optimize=optimize, correct_checkout=correct_checkout):
                    expected = self.root if correct_checkout else self.root / "another checkout"
                    result = subprocess.run(
                        [sys.executable, "-B", *optimize, "-c", launcher.ENVIRONMENT_PROBE, str(expected)],
                        cwd=source, capture_output=True, text=True, timeout=15,
                    )
                    if correct_checkout:
                        self.assertEqual(result.returncode, 0, result.stderr)
                        self.assertIn(str(package), result.stdout)
                    else:
                        self.assertNotEqual(result.returncode, 0)
                        self.assertIn("another installation", result.stderr)
                        self.assertNotIn("Project package:", result.stdout)

    def test_failed_import_stops_before_server(self):
        with patch.object(launcher.subprocess, "run", return_value=subprocess.CompletedProcess([], 1, "", "Missing package")) as run:
            self.assertEqual(self.invoke([]), 2)
            self.assertEqual(run.call_count, 1)

    def test_launch_pins_environment_directory_address_and_port(self):
        with patch.object(launcher.subprocess, "run", side_effect=[subprocess.CompletedProcess([], 0, "OK", ""), subprocess.CompletedProcess([], 7)]) as run:
            self.assertEqual(self.invoke(["--port", "8502"]), 7)
            self.assertEqual(run.call_args.args[0], [str(self.python), "-m", "streamlit", "run", str(self.root / "app.py"), "--server.address", "127.0.0.1", "--server.port", "8502"])
            self.assertEqual(run.call_args.kwargs["cwd"], self.root.resolve())

    def test_invalid_port_does_not_start_a_process(self):
        with patch.object(launcher.subprocess, "run") as run:
            with self.assertRaises(SystemExit):
                self.invoke(["--port", "70000"])
            run.assert_not_called()

    def test_timeout_and_launch_errors_are_controlled(self):
        for error in (subprocess.TimeoutExpired("check", 30), OSError("not executable")):
            with self.subTest(error=error):
                with patch.object(launcher.subprocess, "run", side_effect=error):
                    self.assertEqual(self.invoke(["--check"]), 2)


if __name__ == "__main__":
    unittest.main()
