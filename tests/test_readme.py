"""Tests for README.md links, asset paths, and structure."""

import os
import re
import unittest

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class TestReadme(unittest.TestCase):
    def setUp(self):
        self.readme_path = os.path.join(REPO_ROOT, "README.md")
        with open(self.readme_path, "r", encoding="utf-8") as f:
            self.content = f.read()

    def test_readme_file_exists(self):
        self.assertTrue(os.path.isfile(self.readme_path))

    def test_hero_animated_demo_present(self):
        """README must showcase the animated demo in the hero section."""
        self.assertIn("assets/demo.gif", self.content)
        self.assertIn("Starship Batman Powerline Animated Demo", self.content)

    def test_video_link_present(self):
        """README must mention and link to the MP4 video demo."""
        self.assertIn("assets/demo.mp4", self.content)

    def test_static_preview_retained(self):
        """README must retain the static preview SVG."""
        self.assertIn("assets/preview.svg", self.content)

    def test_palette_svg_retained(self):
        """README must retain the color palette SVG diagram."""
        self.assertIn("assets/palette.svg", self.content)

    def test_local_image_sources_exist(self):
        """All local <img src="..."> references must resolve to existing files."""
        img_srcs = re.findall(r'<img\s+[^>]*src=["\']([^"\']+)["\']', self.content)
        self.assertGreater(len(img_srcs), 0)
        for src in img_srcs:
            if src.startswith("http://") or src.startswith("https://"):
                continue
            path = os.path.join(REPO_ROOT, src)
            self.assertTrue(
                os.path.isfile(path),
                f"Image source '{src}' does not exist on disk at {path}",
            )

    def test_local_markdown_links_exist(self):
        """All local [text](path) or <a href="path"> links must resolve to existing files."""
        # Find markdown links: [text](path)
        md_links = re.findall(r'\[(?:[^\]]*)\]\(([^)]+)\)', self.content)
        # Find HTML hrefs: <a href="...">
        html_hrefs = re.findall(r'<a\s+[^>]*href=["\']([^"\']+)["\']', self.content)

        all_links = md_links + html_hrefs
        for link in all_links:
            # Strip anchors / query params
            clean_link = link.split("#")[0].split("?")[0]
            if not clean_link:
                continue
            if clean_link.startswith("http://") or clean_link.startswith("https://"):
                continue
            path = os.path.join(REPO_ROOT, clean_link)
            self.assertTrue(
                os.path.exists(path),
                f"Link target '{link}' does not exist on disk at {path}",
            )


if __name__ == "__main__":
    unittest.main()
