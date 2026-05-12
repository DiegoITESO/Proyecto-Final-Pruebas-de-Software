"""Integration tests: failure paths for CSV I/O and invalid stdin answers."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from tests.integration._helpers import (
    binary_exists,
    churn_labeled_csv,
    predict_stdin,
    run_cli,
    train_stdin,
)


@unittest.skipUnless(binary_exists(), "Build the project with `make` so logistic_churn exists.")
class TestCliErrorPaths(unittest.TestCase):
    """Assert the binary surfaces clear failures for bad files and invalid prompts."""

    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def test_train_missing_csv_file(self):
        """Nonexistent training CSV should make the process exit with an error."""
        bad = self.tmp / "does_not_exist.csv"
        out = self.tmp / "m.json"
        proc = run_cli(["--train"], train_stdin(str(bad), str(out)), cwd=self.tmp, timeout=60)
        self.assertNotEqual(proc.returncode, 0)

    def test_train_inconsistent_column_widths(self):
        """CSV rows with different column counts must be rejected during parsing."""
        bad_csv = self.tmp / "bad.csv"
        bad_csv.write_text("a,b,churn\n1,2,no\n1\n", encoding="utf-8")
        out = self.tmp / "m.json"
        proc = run_cli(["--train"], train_stdin(str(bad_csv), str(out)), cwd=self.tmp, timeout=60)
        self.assertNotEqual(proc.returncode, 0)

    def test_train_invalid_header_response(self):
        """Only ``y`` or ``n`` is valid for the header question."""
        csv_path = self.tmp / "ok.csv"
        csv_path.write_text(churn_labeled_csv(10), encoding="utf-8")
        out = self.tmp / "m.json"
        stdin = f"{csv_path}\n{out}\nx\n"
        proc = run_cli(["--train"], stdin, cwd=self.tmp, timeout=60)
        self.assertNotEqual(proc.returncode, 0)

    def test_train_invalid_churn_value_in_cell(self):
        """Churn column must contain yes/no tokens after preprocessing."""
        bad = self.tmp / "badchurn.csv"
        bad.write_text("f1,f2,churn\n0,0,maybe\n1,1,no\n", encoding="utf-8")
        out = self.tmp / "m.json"
        proc = run_cli(["--train"], train_stdin(str(bad), str(out)), cwd=self.tmp, timeout=60)
        self.assertNotEqual(proc.returncode, 0)

    def test_train_drop_too_many_columns_rejected(self):
        """Dropping all-but-churn features should violate preprocess validation."""
        lines = ["a,b,churn", "0,0,no", "1,1,yes"]
        p = self.tmp / "dropall.csv"
        p.write_text("\n".join(lines) + "\n", encoding="utf-8")
        out = self.tmp / "m.json"
        proc = run_cli(
            ["--train"],
            train_stdin(str(p), str(out), churn_idx=2, drops="0 1\n"),
            cwd=self.tmp,
            timeout=60,
        )
        self.assertNotEqual(proc.returncode, 0)

    def test_predict_missing_weights_file(self):
        """Predict mode should fail when the JSON weights path cannot be opened."""
        feat = self.tmp / "f.csv"
        feat.write_text("f1,f2\n0,0\n1,1\n", encoding="utf-8")
        out = self.tmp / "o.csv"
        missing = self.tmp / "missing.json"
        proc = run_cli(
            ["--predict"],
            predict_stdin(str(missing), str(feat), str(out)),
            cwd=self.tmp,
            timeout=60,
        )
        self.assertNotEqual(proc.returncode, 0)

    def test_predict_missing_dataset_file(self):
        """Predict should fail when the feature CSV path is invalid."""
        w = self.tmp / "w.json"
        w.write_text('{"Weights": [0.1, 0.2], "Bias": 0.0}', encoding="utf-8")
        out = self.tmp / "o.csv"
        proc = run_cli(
            ["--predict"],
            predict_stdin(str(w), str(self.tmp / "nope.csv"), str(out)),
            cwd=self.tmp,
            timeout=60,
        )
        self.assertNotEqual(proc.returncode, 0)

    def test_predict_invalid_header_response(self):
        """Invalid header answer during predict should abort."""
        w = self.tmp / "w.json"
        w.write_text('{"Weights": [0.1, 0.2], "Bias": 0.0}', encoding="utf-8")
        feat = self.tmp / "f.csv"
        feat.write_text("f1,f2\n0,0\n", encoding="utf-8")
        out = self.tmp / "o.csv"
        stdin = f"{w}\n{feat}\n{out}\nmaybe\n"
        proc = run_cli(["--predict"], stdin, cwd=self.tmp, timeout=60)
        self.assertNotEqual(proc.returncode, 0)

    def test_train_empty_file_is_invalid(self):
        """Empty CSV cannot be preprocessed into labeled matrices."""
        empty = self.tmp / "empty.csv"
        empty.write_text("", encoding="utf-8")
        out = self.tmp / "m.json"
        proc = run_cli(["--train"], train_stdin(str(empty), str(out)), cwd=self.tmp, timeout=60)
        self.assertNotEqual(proc.returncode, 0)

    def test_predict_corrupt_weights_json(self):
        """Malformed JSON at the weights path should fail during load."""
        w = self.tmp / "bad.json"
        w.write_text("{not json", encoding="utf-8")
        feat = self.tmp / "f.csv"
        feat.write_text("f1,f2\n0,0\n1,1\n", encoding="utf-8")
        out = self.tmp / "o.csv"
        proc = run_cli(
            ["--predict"], predict_stdin(str(w), str(feat), str(out)), cwd=self.tmp, timeout=60
        )
        self.assertNotEqual(proc.returncode, 0)


if __name__ == "__main__":
    unittest.main()
