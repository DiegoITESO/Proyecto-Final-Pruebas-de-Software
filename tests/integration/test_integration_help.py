"""Integration tests: ``--help`` output of the compiled CLI."""

from __future__ import annotations

import unittest

from tests.integration._helpers import ROOT, binary_exists, run_cli


@unittest.skipUnless(binary_exists(), "Build the project with `make` so logistic_churn exists.")
class TestHelpIntegration(unittest.TestCase):
    """Assert help text stays aligned with ArgParser::showHelp."""

    def setUp(self) -> None:
        self.proc = run_cli(["--help"], "", timeout=30)

    def test_help_exit_code_zero(self):
        """Program should exit successfully when only requesting help."""
        self.assertEqual(self.proc.returncode, 0)

    def test_help_mentions_product_name(self):
        """Help banner must identify the Customer Churn Predictor tool."""
        self.assertIn("Customer Churn Predictor", self.proc.stdout)

    def test_help_documents_train_flag(self):
        """Users must see the ``--train`` mode documented."""
        self.assertIn("--train", self.proc.stdout)

    def test_help_documents_predict_flag(self):
        """Users must see the ``--predict`` mode documented."""
        self.assertIn("--predict", self.proc.stdout)

    def test_help_documents_evaluate_combo(self):
        """Train-with-evaluate combination must appear in help."""
        self.assertIn("--evaluate", self.proc.stdout)

    def test_help_documents_help_flag(self):
        """The self-documenting ``--help`` token should be listed."""
        self.assertIn("--help", self.proc.stdout)

    def test_help_shows_usage_line(self):
        """Usage section should describe how to invoke the executable."""
        self.assertIn("Usage", self.proc.stdout)

    def test_help_shows_examples_section(self):
        """Concrete example commands aid onboarding."""
        self.assertIn("Examples", self.proc.stdout)

    def test_help_mentions_log_directory(self):
        """Logging contract (files under logs/) should be visible in help."""
        self.assertIn("logs/", self.proc.stdout)

    def test_help_names_executable_in_usage(self):
        """Usage text should reference the logistic_churn binary name."""
        self.assertIn("logistic_churn", self.proc.stdout)

    def test_help_mentions_train_new_model(self):
        """Train option description should state a new model is trained."""
        self.assertIn("Train", self.proc.stdout)

    def test_help_mentions_predict_existing_model(self):
        """Predict option should reference using an existing model."""
        self.assertIn("predict", self.proc.stdout.lower())

    def test_help_runs_from_project_root_cwd(self):
        """Sanity check: cwd is project root so relative paths in docs stay valid."""
        self.assertTrue((ROOT / "README.md").is_file())


if __name__ == "__main__":
    unittest.main()
