"""Integration tests: invalid CLI arguments and error handling."""

from __future__ import annotations

import subprocess
import unittest

from tests.integration._helpers import ROOT, binary_exists, binary_path, cli_subprocess_env, run_cli


@unittest.skipUnless(binary_exists(), "Build the project with `make` so logistic_churn exists.")
class TestInvalidCliIntegration(unittest.TestCase):
    """Cover ArgParser failures for unsupported primary options."""

    def test_unknown_primary_option_nonzero_exit(self):
        """Passing an unrecognized first flag should terminate with an error code."""
        proc = run_cli(["--not-a-real-option"], "", timeout=30)
        self.assertNotEqual(proc.returncode, 0)

    def test_unknown_option_message_on_stderr_or_stdout(self):
        """Runtime error text should mention the unknown token for debugging."""
        proc = run_cli(["--bogusflag"], "", timeout=30)
        blob = proc.stdout + proc.stderr
        self.assertIn("Unknown", blob)

    def test_another_unknown_token(self):
        """Different garbage flag should still fail fast."""
        proc = run_cli(["--xyz123"], "", timeout=30)
        self.assertNotEqual(proc.returncode, 0)

    def test_typo_train_missing_hyphens(self):
        """``train`` without dashes should not be accepted as ``--train``."""
        proc = run_cli(["train"], "", timeout=30)
        self.assertNotEqual(proc.returncode, 0)

    def test_double_hyphen_only_is_invalid(self):
        """Bare ``--`` is not a supported mode selector."""
        proc = run_cli(["--"], "", timeout=30)
        self.assertNotEqual(proc.returncode, 0)

    def test_help_subcommand_not_used(self):
        """``help`` without leading dashes must not silently map to ``--help``."""
        proc = run_cli(["help"], "", timeout=30)
        self.assertNotEqual(proc.returncode, 0)

    def test_help_with_trailing_token_still_succeeds(self):
        """``--help`` path ignores extra argv; process should still exit zero."""
        proc = run_cli(["--help", "ignored"], "", timeout=30)
        self.assertEqual(proc.returncode, 0)

    def test_binary_invoked_with_absolute_path(self):
        """Ensure absolute path invocation behaves like a normal argv[0] rename."""
        proc = subprocess.run(
            [str(binary_path()), "--help"],
            capture_output=True,
            text=True,
            cwd=str(ROOT),
            timeout=30,
            check=False,
            env=cli_subprocess_env(),
        )
        self.assertEqual(proc.returncode, 0)


if __name__ == "__main__":
    unittest.main()
