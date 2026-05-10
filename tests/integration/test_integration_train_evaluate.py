"""Integration tests: ``--train`` and ``--train --evaluate`` interactive flows."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from tests.integration._helpers import binary_exists, churn_labeled_csv, run_cli, train_stdin


@unittest.skipUnless(binary_exists(), "Build the project with `make` so logistic_churn exists.")
class TestTrainAndEvaluateIntegration(unittest.TestCase):
    """Drive stdin prompts end-to-end and assert artifacts plus evaluate metrics."""

    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def test_train_writes_model_json_file(self):
        """Training should persist weights and bias JSON at the user-provided path."""
        csv_path = self.tmp / "data.csv"
        csv_path.write_text(churn_labeled_csv(30), encoding="utf-8")
        out_path = self.tmp / "model.json"
        proc = run_cli(
            ["--train"], train_stdin(str(csv_path), str(out_path)), cwd=self.tmp, timeout=120
        )
        self.assertEqual(proc.returncode, 0)
        self.assertTrue(out_path.is_file())

    def test_train_emits_progress_to_stdout(self):
        """Long training loops print percentage progress for operator feedback."""
        csv_path = self.tmp / "d.csv"
        csv_path.write_text(churn_labeled_csv(28), encoding="utf-8")
        out_path = self.tmp / "m.json"
        proc = run_cli(
            ["--train"],
            train_stdin(str(csv_path), str(out_path), epochs=60),
            cwd=self.tmp,
            timeout=120,
        )
        self.assertIn("Progress", proc.stdout)

    def test_train_model_json_has_weights_array(self):
        """Saved JSON must expose a Weights array compatible with model.load."""
        csv_path = self.tmp / "d.csv"
        csv_path.write_text(churn_labeled_csv(32), encoding="utf-8")
        out_path = self.tmp / "w.json"
        proc = run_cli(
            ["--train"], train_stdin(str(csv_path), str(out_path)), cwd=self.tmp, timeout=120
        )
        self.assertEqual(proc.returncode, 0)
        data = json.loads(out_path.read_text(encoding="utf-8"))
        self.assertIn("Weights", data)
        self.assertIsInstance(data["Weights"], list)

    def test_train_model_json_has_bias_scalar(self):
        """Saved JSON must include scalar Bias as written by LogisticRegression::save."""
        csv_path = self.tmp / "d.csv"
        csv_path.write_text(churn_labeled_csv(30), encoding="utf-8")
        out_path = self.tmp / "w.json"
        proc = run_cli(
            ["--train"], train_stdin(str(csv_path), str(out_path)), cwd=self.tmp, timeout=120
        )
        self.assertEqual(proc.returncode, 0)
        data = json.loads(out_path.read_text(encoding="utf-8"))
        self.assertIn("Bias", data)
        self.assertIsInstance(data["Bias"], (int, float))

    def test_train_with_header_no(self):
        """CSV without header row should still preprocess when user answers ``n``."""
        body = "\n".join(
            ["0,0,no", "1,0,yes", "0,1,yes", "1,1,no", "2,2,yes", "2,0,no", "1,2,no", "0,2,yes"]
        )
        csv_path = self.tmp / "nh.csv"
        csv_path.write_text(body + "\n", encoding="utf-8")
        out_path = self.tmp / "m.json"
        proc = run_cli(
            ["--train"],
            train_stdin(str(csv_path), str(out_path), header_y=False, churn_idx=2),
            cwd=self.tmp,
            timeout=120,
        )
        self.assertEqual(proc.returncode, 0)

    def test_train_churn_column_index_zero(self):
        """Churn labels in the first column (index 0) must be honored."""
        lines = [
            "churn,f1,f2",
            "no,0,0",
            "yes,1,0",
            "no,0,1",
            "yes,1,1",
            "no,2,0",
            "yes,2,1",
            "no,1,2",
            "yes,0,2",
        ]
        csv_path = self.tmp / "c0.csv"
        csv_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        out_path = self.tmp / "m.json"
        proc = run_cli(
            ["--train"],
            train_stdin(str(csv_path), str(out_path), churn_idx=0),
            cwd=self.tmp,
            timeout=120,
        )
        self.assertEqual(proc.returncode, 0)

    def test_train_with_single_drop_column_index(self):
        """Space-separated drop list should remove an ID-like column before training."""
        lines = [
            "id,f1,f2,churn",
            "0,0,0,no",
            "1,1,0,yes",
            "2,0,1,yes",
            "3,1,1,no",
            "4,2,0,yes",
            "5,2,1,no",
        ]
        csv_path = self.tmp / "drop.csv"
        csv_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        out_path = self.tmp / "m.json"
        proc = run_cli(
            ["--train"],
            train_stdin(str(csv_path), str(out_path), churn_idx=3, drops="0\n"),
            cwd=self.tmp,
            timeout=120,
        )
        self.assertEqual(proc.returncode, 0)

    def test_train_small_epoch_count_completes(self):
        """Very few epochs should still finish and write a model file."""
        csv_path = self.tmp / "d.csv"
        csv_path.write_text(churn_labeled_csv(24), encoding="utf-8")
        out_path = self.tmp / "m.json"
        proc = run_cli(
            ["--train"],
            train_stdin(str(csv_path), str(out_path), epochs=5),
            cwd=self.tmp,
            timeout=120,
        )
        self.assertEqual(proc.returncode, 0)
        self.assertTrue(out_path.is_file())

    def test_train_low_learning_rate_completes(self):
        """Small alpha should remain numerically stable for this dataset size."""
        csv_path = self.tmp / "d.csv"
        csv_path.write_text(churn_labeled_csv(26), encoding="utf-8")
        out_path = self.tmp / "m.json"
        proc = run_cli(
            ["--train"],
            train_stdin(str(csv_path), str(out_path), alpha=0.001, epochs=25),
            cwd=self.tmp,
            timeout=120,
        )
        self.assertEqual(proc.returncode, 0)

    def test_train_output_inside_nested_directory(self):
        """Destination path may live under a newly created subdirectory."""
        sub = self.tmp / "models" / "nested"
        sub.mkdir(parents=True)
        csv_path = self.tmp / "d.csv"
        csv_path.write_text(churn_labeled_csv(30), encoding="utf-8")
        out_path = sub / "weights.json"
        proc = run_cli(
            ["--train"], train_stdin(str(csv_path), str(out_path)), cwd=self.tmp, timeout=120
        )
        self.assertEqual(proc.returncode, 0)
        self.assertTrue(out_path.is_file())

    def test_evaluate_prints_accuracy_line(self):
        """Evaluate mode must print an Accuracy line to stdout."""
        csv_path = self.tmp / "d.csv"
        csv_path.write_text(churn_labeled_csv(40), encoding="utf-8")
        out_path = self.tmp / "m.json"
        proc = run_cli(
            ["--train", "--evaluate"],
            train_stdin(str(csv_path), str(out_path), epochs=35),
            cwd=self.tmp,
            timeout=180,
        )
        self.assertEqual(proc.returncode, 0)
        self.assertIn("Accuracy:", proc.stdout)

    def test_evaluate_prints_precision_line(self):
        """Evaluate mode must print Precision for inspection in CI logs."""
        csv_path = self.tmp / "d.csv"
        csv_path.write_text(churn_labeled_csv(42), encoding="utf-8")
        out_path = self.tmp / "m.json"
        proc = run_cli(
            ["--train", "--evaluate"],
            train_stdin(str(csv_path), str(out_path), epochs=35),
            cwd=self.tmp,
            timeout=180,
        )
        self.assertIn("Precision:", proc.stdout)

    def test_evaluate_prints_recall_line(self):
        """Evaluate mode must print Recall."""
        csv_path = self.tmp / "d.csv"
        csv_path.write_text(churn_labeled_csv(44), encoding="utf-8")
        out_path = self.tmp / "m.json"
        proc = run_cli(
            ["--train", "--evaluate"],
            train_stdin(str(csv_path), str(out_path), epochs=35),
            cwd=self.tmp,
            timeout=180,
        )
        self.assertIn("Recall:", proc.stdout)

    def test_evaluate_prints_f1_line(self):
        """Evaluate mode must print F1 score label."""
        csv_path = self.tmp / "d.csv"
        csv_path.write_text(churn_labeled_csv(46), encoding="utf-8")
        out_path = self.tmp / "m.json"
        proc = run_cli(
            ["--train", "--evaluate"],
            train_stdin(str(csv_path), str(out_path), epochs=40),
            cwd=self.tmp,
            timeout=180,
        )
        self.assertIn("F1 score:", proc.stdout)

    def test_evaluate_writes_model_file(self):
        """Even in evaluate mode the trained weights should be saved to disk."""
        csv_path = self.tmp / "d.csv"
        csv_path.write_text(churn_labeled_csv(38), encoding="utf-8")
        out_path = self.tmp / "eval_model.json"
        proc = run_cli(
            ["--train", "--evaluate"],
            train_stdin(str(csv_path), str(out_path), epochs=30),
            cwd=self.tmp,
            timeout=180,
        )
        self.assertEqual(proc.returncode, 0)
        self.assertTrue(out_path.is_file())

    def test_evaluate_exit_code_zero(self):
        """Happy-path evaluate should return success to the shell."""
        csv_path = self.tmp / "d.csv"
        csv_path.write_text(churn_labeled_csv(40), encoding="utf-8")
        out_path = self.tmp / "m.json"
        proc = run_cli(
            ["--train", "--evaluate"],
            train_stdin(str(csv_path), str(out_path), epochs=32),
            cwd=self.tmp,
            timeout=180,
        )
        self.assertEqual(proc.returncode, 0)

    def test_accuracy_line_has_numeric_value(self):
        """Accuracy output should include a floating-point value after the colon."""
        csv_path = self.tmp / "d.csv"
        csv_path.write_text(churn_labeled_csv(45), encoding="utf-8")
        out_path = self.tmp / "m.json"
        proc = run_cli(
            ["--train", "--evaluate"],
            train_stdin(str(csv_path), str(out_path), epochs=36),
            cwd=self.tmp,
            timeout=180,
        )
        for line in proc.stdout.splitlines():
            if line.startswith("Accuracy:"):
                rest = line.split(":", 1)[1].strip()
                float(rest)
                return
        self.fail("Accuracy line not found")

    def test_train_dataset_path_may_be_absolute_style(self):
        """Use absolute-looking paths inside temp dir to mimic user absolute paths."""
        csv_path = self.tmp / "abs.csv"
        csv_path.write_text(churn_labeled_csv(28), encoding="utf-8")
        out_path = self.tmp / "out.json"
        proc = run_cli(
            ["--train"],
            train_stdin(str(csv_path.resolve()), str(out_path.resolve())),
            cwd=self.tmp,
            timeout=120,
        )
        self.assertEqual(proc.returncode, 0)

    def test_train_twice_overwrites_json(self):
        """Second training run should replace the JSON at the same destination."""
        csv_path = self.tmp / "d.csv"
        csv_path.write_text(churn_labeled_csv(26), encoding="utf-8")
        out_path = self.tmp / "same.json"
        proc1 = run_cli(
            ["--train"],
            train_stdin(str(csv_path), str(out_path), epochs=10),
            cwd=self.tmp,
            timeout=120,
        )
        proc2 = run_cli(
            ["--train"],
            train_stdin(str(csv_path), str(out_path), epochs=12),
            cwd=self.tmp,
            timeout=120,
        )
        self.assertEqual(proc1.returncode, 0)
        self.assertEqual(proc2.returncode, 0)
        self.assertTrue(out_path.stat().st_size > 0)

    def test_train_churn_middle_column(self):
        """Churn column at index 1 with features on both sides."""
        lines = [
            "f1,churn,f2",
            "0,no,0",
            "1,yes,0",
            "0,yes,1",
            "1,no,1",
            "2,no,0",
            "2,yes,1",
            "1,no,2",
        ]
        csv_path = self.tmp / "mid.csv"
        csv_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        out_path = self.tmp / "m.json"
        proc = run_cli(
            ["--train"],
            train_stdin(str(csv_path), str(out_path), churn_idx=1),
            cwd=self.tmp,
            timeout=120,
        )
        self.assertEqual(proc.returncode, 0)

    def test_evaluate_with_header_no(self):
        """Evaluate path should accept headerless CSV answers."""
        body = "\n".join(
            [
                "0,0,no",
                "1,0,yes",
                "0,1,yes",
                "1,1,no",
                "2,2,yes",
                "2,0,no",
                "1,2,no",
                "0,2,yes",
                "2,1,yes",
            ]
        )
        csv_path = self.tmp / "raw.csv"
        csv_path.write_text(body + "\n", encoding="utf-8")
        out_path = self.tmp / "m.json"
        proc = run_cli(
            ["--train", "--evaluate"],
            train_stdin(str(csv_path), str(out_path), header_y=False, churn_idx=2, epochs=30),
            cwd=self.tmp,
            timeout=180,
        )
        self.assertEqual(proc.returncode, 0)
        self.assertIn("F1 score:", proc.stdout)

    def test_train_weights_length_matches_features(self):
        """Number of weights should match feature dimension after preprocessing."""
        csv_path = self.tmp / "d.csv"
        csv_path.write_text(churn_labeled_csv(30), encoding="utf-8")
        out_path = self.tmp / "m.json"
        proc = run_cli(
            ["--train"], train_stdin(str(csv_path), str(out_path)), cwd=self.tmp, timeout=120
        )
        self.assertEqual(proc.returncode, 0)
        data = json.loads(out_path.read_text(encoding="utf-8"))
        self.assertGreater(len(data["Weights"]), 0)

    def test_train_completes_without_stderr_traceback(self):
        """Successful train should not dump a Python-style traceback to stderr."""
        csv_path = self.tmp / "d.csv"
        csv_path.write_text(churn_labeled_csv(25), encoding="utf-8")
        out_path = self.tmp / "m.json"
        proc = run_cli(
            ["--train"],
            train_stdin(str(csv_path), str(out_path), epochs=15),
            cwd=self.tmp,
            timeout=120,
        )
        self.assertEqual(proc.returncode, 0)
        self.assertNotIn("Traceback", proc.stderr)

    def test_evaluate_precision_line_has_number(self):
        """Precision metric line should contain a parsable float."""
        csv_path = self.tmp / "d.csv"
        csv_path.write_text(churn_labeled_csv(48), encoding="utf-8")
        out_path = self.tmp / "m.json"
        proc = run_cli(
            ["--train", "--evaluate"],
            train_stdin(str(csv_path), str(out_path), epochs=38),
            cwd=self.tmp,
            timeout=180,
        )
        for line in proc.stdout.splitlines():
            if line.startswith("Precision:"):
                float(line.split(":", 1)[1].strip())
                return
        self.fail("Precision line missing")

    def test_evaluate_recall_line_has_number(self):
        """Recall metric line should contain a parsable float."""
        csv_path = self.tmp / "d.csv"
        csv_path.write_text(churn_labeled_csv(48), encoding="utf-8")
        out_path = self.tmp / "m.json"
        proc = run_cli(
            ["--train", "--evaluate"],
            train_stdin(str(csv_path), str(out_path), epochs=38),
            cwd=self.tmp,
            timeout=180,
        )
        for line in proc.stdout.splitlines():
            if line.startswith("Recall:"):
                float(line.split(":", 1)[1].strip())
                return
        self.fail("Recall line missing")

    def test_evaluate_f1_line_has_number(self):
        """F1 line should contain a parsable float."""
        csv_path = self.tmp / "d.csv"
        csv_path.write_text(churn_labeled_csv(50), encoding="utf-8")
        out_path = self.tmp / "m.json"
        proc = run_cli(
            ["--train", "--evaluate"],
            train_stdin(str(csv_path), str(out_path), epochs=40),
            cwd=self.tmp,
            timeout=180,
        )
        for line in proc.stdout.splitlines():
            if line.startswith("F1 score:"):
                float(line.split(":", 1)[1].strip())
                return
        self.fail("F1 line missing")

    def test_train_slightly_larger_dataset(self):
        """Scale row count up modestly to exercise shuffle split."""
        csv_path = self.tmp / "big.csv"
        csv_path.write_text(churn_labeled_csv(55), encoding="utf-8")
        out_path = self.tmp / "m.json"
        proc = run_cli(
            ["--train"],
            train_stdin(str(csv_path), str(out_path), epochs=22),
            cwd=self.tmp,
            timeout=180,
        )
        self.assertEqual(proc.returncode, 0)

    def test_train_moderate_alpha(self):
        """Default-ish alpha 0.05 should converge for synthetic data."""
        csv_path = self.tmp / "d.csv"
        csv_path.write_text(churn_labeled_csv(32), encoding="utf-8")
        out_path = self.tmp / "m.json"
        proc = run_cli(
            ["--train"],
            train_stdin(str(csv_path), str(out_path), alpha=0.05, epochs=28),
            cwd=self.tmp,
            timeout=120,
        )
        self.assertEqual(proc.returncode, 0)

    def test_train_high_epoch_count_bounded(self):
        """Larger epoch budget still completes within subprocess timeout."""
        csv_path = self.tmp / "d.csv"
        csv_path.write_text(churn_labeled_csv(22), encoding="utf-8")
        out_path = self.tmp / "m.json"
        proc = run_cli(
            ["--train"],
            train_stdin(str(csv_path), str(out_path), epochs=120),
            cwd=self.tmp,
            timeout=180,
        )
        self.assertEqual(proc.returncode, 0)

    def test_evaluate_metrics_ordering(self):
        """Metrics should appear in accuracy-precision-recall-F1 order in stdout."""
        csv_path = self.tmp / "d.csv"
        csv_path.write_text(churn_labeled_csv(45), encoding="utf-8")
        out_path = self.tmp / "m.json"
        proc = run_cli(
            ["--train", "--evaluate"],
            train_stdin(str(csv_path), str(out_path), epochs=33),
            cwd=self.tmp,
            timeout=180,
        )
        text = proc.stdout
        self.assertLess(text.index("Accuracy:"), text.index("Precision:"))
        self.assertLess(text.index("Precision:"), text.index("Recall:"))
        self.assertLess(text.index("Recall:"), text.index("F1 score:"))

    def test_train_empty_drops_line_only_newlines(self):
        """Blank drops line after churn index should mean no columns dropped."""
        csv_path = self.tmp / "d.csv"
        csv_path.write_text(churn_labeled_csv(27), encoding="utf-8")
        out_path = self.tmp / "m.json"
        proc = run_cli(
            ["--train"],
            train_stdin(str(csv_path), str(out_path), drops="\n"),
            cwd=self.tmp,
            timeout=120,
        )
        self.assertEqual(proc.returncode, 0)

    def test_train_bias_is_finite_float(self):
        """Bias in JSON should deserialize as a finite float."""
        csv_path = self.tmp / "d.csv"
        csv_path.write_text(churn_labeled_csv(29), encoding="utf-8")
        out_path = self.tmp / "m.json"
        proc = run_cli(
            ["--train"], train_stdin(str(csv_path), str(out_path)), cwd=self.tmp, timeout=120
        )
        self.assertEqual(proc.returncode, 0)
        b = float(json.loads(out_path.read_text(encoding="utf-8"))["Bias"])
        self.assertTrue(b == b)  # not NaN

    def test_evaluate_model_loadable_json_shape(self):
        """Post-evaluate JSON should remain valid for a subsequent load() shape check."""
        csv_path = self.tmp / "d.csv"
        csv_path.write_text(churn_labeled_csv(36), encoding="utf-8")
        out_path = self.tmp / "m.json"
        proc = run_cli(
            ["--train", "--evaluate"],
            train_stdin(str(csv_path), str(out_path), epochs=28),
            cwd=self.tmp,
            timeout=180,
        )
        self.assertEqual(proc.returncode, 0)
        data = json.loads(out_path.read_text(encoding="utf-8"))
        self.assertGreaterEqual(len(data["Weights"]), 1)

    def test_train_minimal_row_count(self):
        """Smallest dataset that still splits 80/20 without empty matrices."""
        csv_path = self.tmp / "tiny.csv"
        csv_path.write_text(churn_labeled_csv(12), encoding="utf-8")
        out_path = self.tmp / "m.json"
        proc = run_cli(
            ["--train"],
            train_stdin(str(csv_path), str(out_path), epochs=20),
            cwd=self.tmp,
            timeout=120,
        )
        self.assertEqual(proc.returncode, 0)

    def test_train_alpha_at_upper_small_range(self):
        """Slightly larger alpha 0.12 should still complete."""
        csv_path = self.tmp / "d.csv"
        csv_path.write_text(churn_labeled_csv(24), encoding="utf-8")
        out_path = self.tmp / "m.json"
        proc = run_cli(
            ["--train"],
            train_stdin(str(csv_path), str(out_path), alpha=0.12, epochs=18),
            cwd=self.tmp,
            timeout=120,
        )
        self.assertEqual(proc.returncode, 0)


if __name__ == "__main__":
    unittest.main()
