# /// script
# requires-python = ">=3.11"
# ///
"""Unit tests for scripts/goal_rollup.py — Done != Achieved (see #166).

Usage:
    uv run tests/test_goal_rollup.py
"""
from __future__ import annotations

import importlib.util
import pathlib
import unittest
from unittest import mock

ROOT = pathlib.Path(__file__).resolve().parent.parent
_spec = importlib.util.spec_from_file_location(
    "goal_rollup", ROOT / "scripts" / "goal_rollup.py"
)
goal_rollup = importlib.util.module_from_spec(_spec)
assert _spec.loader is not None
_spec.loader.exec_module(goal_rollup)


class RenderOutcomeTests(unittest.TestCase):
    def test_closed_but_not_achieved_kr_is_not_counted_as_achieved(self):
        goals = [
            {
                "id": "G01",
                "objective": "test objective",
                "key_results": [
                    {
                        "id": "G01-KR1",
                        "statement": "a probe that came back negative",
                        "issue": 1,
                        "outcome": "not-achieved",
                    },
                ],
            }
        ]
        with mock.patch.object(goal_rollup, "issue_state", return_value="closed"):
            out = goal_rollup.render(goals)

        self.assertIn("0/1 KRs achieved", out)
        self.assertIn("1/1 resolved", out)
        self.assertIn("not-achieved", out)
        self.assertNotIn("[x] `G01-KR1`", out)

    def test_closed_with_achieved_outcome_is_counted(self):
        goals = [
            {
                "id": "G01",
                "objective": "test objective",
                "key_results": [
                    {
                        "id": "G01-KR1",
                        "statement": "a metric that hit target",
                        "issue": 2,
                        "outcome": "achieved",
                    },
                ],
            }
        ]
        with mock.patch.object(goal_rollup, "issue_state", return_value="closed"):
            out = goal_rollup.render(goals)

        self.assertIn("1/1 KRs achieved", out)
        self.assertIn("[x] `G01-KR1`", out)

    def test_closed_with_no_outcome_renders_unknown_not_achieved(self):
        goals = [
            {
                "id": "G01",
                "objective": "test objective",
                "key_results": [
                    {
                        "id": "G01-KR1",
                        "statement": "closed without recording an outcome",
                        "issue": 3,
                    },
                ],
            }
        ]
        with mock.patch.object(goal_rollup, "issue_state", return_value="closed"):
            out = goal_rollup.render(goals)

        self.assertIn("0/1 KRs achieved", out)
        self.assertIn("outcome unknown", out)
        self.assertNotIn("[x] `G01-KR1`", out)

    def test_issue_state_passes_repo_flag(self):
        with mock.patch.object(goal_rollup.subprocess, "run") as run:
            run.return_value = mock.Mock(stdout="closed\n")
            goal_rollup.issue_state(42)
        args = run.call_args[0][0]
        self.assertIn("--repo", args)


if __name__ == "__main__":
    unittest.main()
