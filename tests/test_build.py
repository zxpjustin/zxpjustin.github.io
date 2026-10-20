"""验证 Python 3 构建、中文内容和已发布 HTML 的一致性。"""

from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import re

ROOT = Path(__file__).resolve().parents[1]


class BuildTests(unittest.TestCase):
    """检查真实生成器输出，防止源文件和网页不同步。"""

    def test_pages_rebuild_exactly(self):
        """@brief 重新生成两个网页并与已保存的 HTML 逐字比较。"""
        build_root = ROOT / ".build-tests"
        build_root.mkdir(exist_ok=True)
        temporary = tempfile.mkdtemp(prefix="run-", dir=build_root)
        for name in ("index", "biography"):
            with self.subTest(page=name):
                output = Path(temporary) / f"{name}.html"
                result = subprocess.run(
                    [sys.executable, "-W", "error", "jemdoc.py", "-o", str(output), f"{name}.jemdoc"],
                    cwd=ROOT, capture_output=True, text=True, encoding="utf-8",
                )
                self.assertEqual(result.returncode, 0, result.stderr)
                html = output.read_text(encoding="utf-8")
                self.assertEqual(html, (ROOT / f"{name}.html").read_text(encoding="utf-8"))
                self.assertIn("张晓鹏", html)
                self.assertNotIn("Yuzhe Ma", html)
                self.assertNotIn("xpzhang[at]", html)

    def test_published_content_and_resources(self):
        """@brief 检查论文完整性、荣誉表列数与本地资源引用。"""
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        numbers = re.findall(r"<li><p>\[([JC]\d+)\]", html)
        self.assertEqual(numbers, ["J3", "J2", "J1"] + [f"C{i}" for i in range(11, 0, -1)])
        rows = re.findall(r"<tr\b[^>]*>(.*?)</tr>", html, re.S)
        self.assertEqual(len(rows), 6)
        self.assertTrue(all(len(re.findall(r"<td\b", row)) == 3 for row in rows))
        self.assertNotIn("DAC Young Fellow", html)
        self.assertIn("zxpjustin[at]gmail.com", html)
        self.assertIn("article 4, 2026", html)
        self.assertIn("1888–1901, 2022", html)
        self.assertIn('name="viewport"', html)
        self.assertNotIn("accepted by", html)
        for reference in re.findall(r'(?:src|href)="([^"]+)"', html):
            if not reference.startswith(("http:", "https:", "//", "#", "mailto:")):
                self.assertTrue((ROOT / reference).is_file(), reference)


if __name__ == "__main__":
    unittest.main()
