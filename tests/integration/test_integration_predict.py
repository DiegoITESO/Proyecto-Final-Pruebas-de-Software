"""Integration tests: ``--predict`` flow after a trained model exists."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from tests.integration._helpers import (
    binary_exists,
    churn_labeled_csv,
    features_only_csv,
    predict_stdin,
    run_cli,
    train_stdin,
)


@unittest.skipUnless(binary_exists(), "Build the project with `make` so logistic_churn exists.")
class TestPredictIntegration(unittest.TestCase):
    """Train a reference model once, then exercise prediction stdin and output CSV."""

    @classmethod
    def setUpClass(cls) -> None:
        cls._tmp = tempfile.TemporaryDirectory()
        cls.base = Path(cls._tmp.name)
        train_csv = cls.base / "train_data.csv"
        train_csv.write_text(churn_labeled_csv(40), encoding="utf-8")
        cls.model_path = cls.base / "shared_model.json"
        proc = run_cli(
            ["--train"],
            train_stdin(str(train_csv), str(cls.model_path), epochs=35),
            cwd=cls.base,
            timeout=180,
        )
        if proc.returncode != 0:
            raise RuntimeError(f"setUpClass train failed: {proc.stderr}\n{proc.stdout}")
        cls.feature_csv = cls.base / "predict_rows.csv"
        cls.feature_csv.write_text(features_only_csv(12), encoding="utf-8")

    @classmethod
    def tearDownClass(cls) -> None:
        cls._tmp.cleanup()

    def test_predict_creates_output_csv(self):
        """Prediction should write one score per input row to the output path."""
        out = self.base / "pred_out.csv"
        proc = run_cli(
            ["--predict"],
            predict_stdin(str(self.model_path), str(self.feature_csv), str(out)),
            cwd=self.base,
            timeout=120,
        )
        self.assertEqual(proc.returncode, 0)
        self.assertTrue(out.is_file())

    def test_predict_output_line_count_matches_rows(self):
        """Output row count must match the number of feature rows (excluding header)."""
        out = self.base / "lines.csv"
        proc = run_cli(
            ["--predict"],
            predict_stdin(str(self.model_path), str(self.feature_csv), str(out)),
            cwd=self.base,
            timeout=120,
        )
        self.assertEqual(proc.returncode, 0)
        n_body = len(self.feature_csv.read_text(encoding="utf-8").strip().splitlines()) - 1
        out_lines = [ln for ln in out.read_text(encoding="utf-8").splitlines() if ln.strip()]
        self.assertEqual(len(out_lines), n_body)

    def test_predict_each_line_is_float_probability(self):
        """Each prediction line should parse as a float in (0,1) for sigmoid outputs."""
        out = self.base / "floats.csv"
        proc = run_cli(
            ["--predict"],
            predict_stdin(str(self.model_path), str(self.feature_csv), str(out)),
            cwd=self.base,
            timeout=120,
        )
        self.assertEqual(proc.returncode, 0)
        for ln in out.read_text(encoding="utf-8").splitlines():
            if not ln.strip():
                continue
            v = float(ln.strip())
            self.assertGreaterEqual(v, 0.0)
            self.assertLessEqual(v, 1.0)

    def test_predict_exit_code_zero(self):
        """Happy-path predict should return shell success."""
        out = self.base / "ok.csv"
        proc = run_cli(
            ["--predict"],
            predict_stdin(str(self.model_path), str(self.feature_csv), str(out)),
            cwd=self.base,
            timeout=120,
        )
        self.assertEqual(proc.returncode, 0)

    def test_predict_with_header_no(self):
        """Headerless feature file should work when user selects ``n``."""
        raw = "\n".join(["0,0", "1,0", "0,1", "1,1", "2,0", "2,1", "1,2", "0,2", "2,2"]) + "\n"
        pcsv = self.base / "nh_feat.csv"
        pcsv.write_text(raw, encoding="utf-8")
        out = self.base / "nh_out.csv"
        proc = run_cli(
            ["--predict"],
            predict_stdin(str(self.model_path), str(pcsv), str(out), header_y=False),
            cwd=self.base,
            timeout=120,
        )
        self.assertEqual(proc.returncode, 0)

    def test_predict_empty_drops_line(self):
        """Blank drop-indices line should mean keep all feature columns."""
        out = self.base / "drops_empty.csv"
        proc = run_cli(
            ["--predict"],
            predict_stdin(str(self.model_path), str(self.feature_csv), str(out), drops="\n"),
            cwd=self.base,
            timeout=120,
        )
        self.assertEqual(proc.returncode, 0)

    def test_predict_output_not_empty_file(self):
        """Prediction file should contain non-whitespace bytes."""
        out = self.base / "nonempty.csv"
        proc = run_cli(
            ["--predict"],
            predict_stdin(str(self.model_path), str(self.feature_csv), str(out)),
            cwd=self.base,
            timeout=120,
        )
        self.assertEqual(proc.returncode, 0)
        self.assertGreater(out.stat().st_size, 0)

    def test_predict_twice_same_destination(self):
        """Second predict run can overwrite the same CSV path."""
        out = self.base / "twice.csv"
        proc1 = run_cli(
            ["--predict"],
            predict_stdin(str(self.model_path), str(self.feature_csv), str(out)),
            cwd=self.base,
            timeout=120,
        )
        proc2 = run_cli(
            ["--predict"],
            predict_stdin(str(self.model_path), str(self.feature_csv), str(out)),
            cwd=self.base,
            timeout=120,
        )
        self.assertEqual(proc1.returncode, 0)
        self.assertEqual(proc2.returncode, 0)

    def test_predict_smaller_feature_batch(self):
        """Fewer predict rows than training pool should still work."""
        small = self.base / "small_feat.csv"
        small.write_text(features_only_csv(4), encoding="utf-8")
        out = self.base / "small_out.csv"
        proc = run_cli(
            ["--predict"],
            predict_stdin(str(self.model_path), str(small), str(out)),
            cwd=self.base,
            timeout=120,
        )
        self.assertEqual(proc.returncode, 0)

    def test_predict_larger_feature_batch(self):
        """More predict rows stresses the per-row inference loop."""
        big = self.base / "big_feat.csv"
        big.write_text(features_only_csv(25), encoding="utf-8")
        out = self.base / "big_out.csv"
        proc = run_cli(
            ["--predict"],
            predict_stdin(str(self.model_path), str(big), str(out)),
            cwd=self.base,
            timeout=120,
        )
        self.assertEqual(proc.returncode, 0)

    def test_predict_absolute_paths_allowed(self):
        """Absolute paths inside temp for weights and IO should behave."""
        out = self.base / "abs_pred.csv"
        proc = run_cli(
            ["--predict"],
            predict_stdin(
                str(self.model_path.resolve()), str(self.feature_csv.resolve()), str(out.resolve())
            ),
            cwd=self.base,
            timeout=120,
        )
        self.assertEqual(proc.returncode, 0)

    def test_predict_no_stderr_traceback(self):
        """Successful predict must not emit a traceback to stderr."""
        out = self.base / "clean.csv"
        proc = run_cli(
            ["--predict"],
            predict_stdin(str(self.model_path), str(self.feature_csv), str(out)),
            cwd=self.base,
            timeout=120,
        )
        self.assertNotIn("Traceback", proc.stderr)

    def test_predict_output_subdirectory(self):
        """Prediction CSV may be written under a nested directory."""
        sub = self.base / "outdir"
        sub.mkdir(exist_ok=True)
        out = sub / "nested.csv"
        proc = run_cli(
            ["--predict"],
            predict_stdin(str(self.model_path), str(self.feature_csv), str(out)),
            cwd=self.base,
            timeout=120,
        )
        self.assertEqual(proc.returncode, 0)
        self.assertTrue(out.is_file())

    def test_predict_values_are_deterministic_shape(self):
        """All output lines should be single-token numeric strings."""
        out = self.base / "shape.csv"
        proc = run_cli(
            ["--predict"],
            predict_stdin(str(self.model_path), str(self.feature_csv), str(out)),
            cwd=self.base,
            timeout=120,
        )
        self.assertEqual(proc.returncode, 0)
        for ln in out.read_text(encoding="utf-8").splitlines():
            if not ln.strip():
                continue
            parts = ln.strip().split()
            self.assertEqual(len(parts), 1)

    def test_model_file_still_exists_after_many_predictions(self):
        """Weights file should remain readable after repeated predict calls."""
        out = self.base / "reuse.csv"
        for _ in range(3):
            proc = run_cli(
                ["--predict"],
                predict_stdin(str(self.model_path), str(self.feature_csv), str(out)),
                cwd=self.base,
                timeout=120,
            )
            self.assertEqual(proc.returncode, 0)
        self.assertTrue(self.model_path.is_file())


if __name__ == "__main__":
    unittest.main()
