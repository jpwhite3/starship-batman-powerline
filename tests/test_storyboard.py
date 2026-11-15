import unittest
from scripts.storyboard import get_terminal_state, TOTAL_FRAMES, FPS, PALETTE


class TestStoryboard(unittest.TestCase):
    def test_total_frames(self):
        self.assertEqual(TOTAL_FRAMES, 300)
        self.assertEqual(FPS, 30)

    def test_initial_state(self):
        state = get_terminal_state(0)
        self.assertEqual(state["segments"][0]["text"], "jpwhite")
        self.assertEqual(state["segments"][0]["bg"], "#805ad5")
        self.assertEqual(state["segments"][1]["text"], "~")
        self.assertEqual(state["segments"][1]["bg"], "#0f3460")
        self.assertEqual(state["command"], "")

    def test_repo_navigation_state(self):
        state = get_terminal_state(70)
        # Should be inside gotham-app with git and node runtime
        seg_texts = [s["text"] for s in state["segments"]]
        self.assertIn("…/gotham-app", seg_texts)
        self.assertIn("main", seg_texts)

    def test_docker_context_state(self):
        state = get_terminal_state(180)
        # Should show alert_crimson docker segment
        docker_segs = [s for s in state["segments"] if s["bg"] == "#c53030"]
        self.assertEqual(len(docker_segs), 1)
        self.assertIn("batcave", docker_segs[0]["text"])

    def test_final_rest_state(self):
        state = get_terminal_state(299)
        self.assertTrue(len(state["history"]) >= 4)
        self.assertEqual(state["command"], "")

    def test_all_frames_schema_and_validity(self):
        """Verify that every single frame from 0 to 299 produces valid schema."""
        for frame_idx in range(TOTAL_FRAMES):
            state = get_terminal_state(frame_idx)
            self.assertIsInstance(state, dict)
            self.assertIn("segments", state)
            self.assertIn("command", state)
            self.assertIn("cursor", state)
            self.assertIn("history", state)

            self.assertIsInstance(state["command"], str)
            self.assertIsInstance(state["cursor"], bool)
            self.assertIsInstance(state["segments"], list)
            self.assertIsInstance(state["history"], list)
            self.assertGreater(len(state["segments"]), 0)

            for seg in state["segments"]:
                self.assertIn("text", seg)
                self.assertIn("bg", seg)
                self.assertIn("fg", seg)
                self.assertIn("icon", seg)
                self.assertTrue(seg["bg"].startswith("#"))
                self.assertTrue(seg["fg"].startswith("#"))

            for hist in state["history"]:
                self.assertIsInstance(hist, dict)
                self.assertIn("command", hist)
                self.assertIn("output", hist)
                self.assertIn("segments", hist)
                self.assertIsInstance(hist["output"], list)

    def test_palette_tokens(self):
        """Verify all Batman TAS palette tokens match starship.toml verbatim."""
        expected = {
            "joker_purple": "#805ad5",
            "cape_blue": "#0f3460",
            "signal_yellow": "#ecc94b",
            "robin_green": "#2f855a",
            "alert_crimson": "#c53030",
            "gotham_midnight": "#16213e",
            "gotham_dark": "#1a1a2e",
            "gotham_fog": "#e2e8f0",
            "silver_highlight": "#cbd5e0",
        }
        for token, hex_code in expected.items():
            self.assertEqual(PALETTE[token], hex_code)

    def test_frame_boundary_clamping(self):
        """Verify negative frame and excessive frame clamp safely."""
        state_neg = get_terminal_state(-10)
        state_0 = get_terminal_state(0)
        self.assertEqual(state_neg, state_0)

        state_over = get_terminal_state(500)
        state_299 = get_terminal_state(299)
        self.assertEqual(state_over, state_299)

    def test_known_icons(self):
        """Verify only allowed standard icons are emitted."""
        allowed_icons = {"", "branch", "node", "docker", "heart"}
        for frame_idx in range(TOTAL_FRAMES):
            state = get_terminal_state(frame_idx)
            for seg in state["segments"]:
                self.assertIn(seg["icon"], allowed_icons)

    def test_typing_progression(self):
        """Verify commands type smoothly during Phase 1."""
        lengths = [len(get_terminal_state(f)["command"]) for f in range(15, 43)]
        # Must be non-decreasing
        self.assertTrue(all(lengths[i] <= lengths[i + 1] for i in range(len(lengths) - 1)))
        self.assertEqual(lengths[0], 0)
        self.assertEqual(lengths[-1], len("cd gotham-app"))


if __name__ == "__main__":
    unittest.main()
