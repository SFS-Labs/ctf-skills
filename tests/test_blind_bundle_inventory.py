"""Structural ZIP/TAR checks without extracting or opening challenge file bodies."""
import io
import json
from pathlib import Path
import subprocess
import sys
import tarfile
import tempfile
import unittest
import zipfile

SCRIPT = Path(__file__).resolve().parent.parent / "bin/audit-blind-bundle.py"


class BundleInventoryTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name)

    def invoke(self, path, *extra):
        return subprocess.run([sys.executable, str(SCRIPT), "--archive", str(path),
                               *extra], capture_output=True, text=True, timeout=10)

    def test_zip_index_does_not_extract(self):
        bundle = self.base / "input.zip"
        with zipfile.ZipFile(bundle, "w") as archive:
            archive.writestr("input/case-b/task.json", '{"secret_ground_truth":"not_read"}')
            archive.writestr("input/src/StablecoinDEX.sol", "contract StablecoinDEX {}")
        extracted = self.base / "partial"
        extracted.mkdir()
        (extracted / "StablecoinDEX.sol").write_text("source", encoding="utf-8")
        proc = self.invoke(bundle, "--expected-entries", "393",
                           "--extracted-dir", str(extracted))
        self.assertEqual(proc.returncode, 0, proc.stderr)
        obj = json.loads(proc.stdout)
        self.assertEqual(obj["bundle"]["file_entries"], 2)
        self.assertTrue(obj["bundle"]["case_b_task_json_in_archive"])
        self.assertEqual(obj["extracted"]["file_entries"], 1)
        self.assertFalse(obj["expected_count_matches"])
        self.assertFalse(obj["blind_isolation_verified"])
        self.assertFalse(obj["official_evaluation_verified"])
        self.assertNotIn("secret_ground_truth", proc.stdout)
        self.assertFalse((self.base / "input").exists())

    def test_zip_traversal_blocks_structural_acceptance(self):
        archive = self.base / "bad.zip"
        with zipfile.ZipFile(archive, "w") as stream:
            stream.writestr("../reference-answers.json", "redacted")
            stream.writestr("safe.sol", "contract A {}")
        proc = self.invoke(archive)
        self.assertEqual(proc.returncode, 2)
        self.assertEqual(json.loads(proc.stdout)["bundle"]["unsafe_or_link_entries"], 1)

    def test_tar_file_listing(self):
        archive = self.base / "input.tar.gz"
        with tarfile.open(archive, "w:gz") as stream:
            data = b"source"
            info = tarfile.TarInfo("case-b/contracts/DEX.sol")
            info.size = len(data)
            stream.addfile(info, io.BytesIO(data))
        proc = self.invoke(archive)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertEqual(json.loads(proc.stdout)["bundle"]["archive_type"], "tar")


if __name__ == "__main__":
    unittest.main()
