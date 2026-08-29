"""Automated tests for the command-line task manager."""

import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

import main


class TaskManagerTestCase(unittest.TestCase):
    """Run every test with an isolated tasks.json file."""

    def setUp(self):
        self.temp_directory = tempfile.TemporaryDirectory()
        self.tasks_file = Path(self.temp_directory.name) / "tasks.json"
        self.file_patch = patch.object(main, "TASKS_FILE", self.tasks_file)
        self.file_patch.start()

    def tearDown(self):
        self.file_patch.stop()
        self.temp_directory.cleanup()

    def capture_output(self, function, *args):
        output = io.StringIO()
        with redirect_stdout(output):
            function(*args)
        return output.getvalue()

    def test_load_tasks_creates_an_empty_file(self):
        self.assertEqual(main.load_tasks(), [])
        self.assertEqual(json.loads(self.tasks_file.read_text(encoding="utf-8")), [])

    def test_saved_tasks_can_be_loaded(self):
        tasks = [{"title": "Read a chapter", "completed": False}]
        main.save_tasks(tasks)
        self.assertEqual(main.load_tasks(), tasks)

    def test_invalid_json_is_handled(self):
        self.tasks_file.write_text("not valid json", encoding="utf-8")
        output = self.capture_output(main.load_tasks)
        self.assertIn("Warning", output)

    def test_list_with_an_invalid_task_is_rejected(self):
        self.tasks_file.write_text(
            json.dumps([{"title": "Keep this", "completed": False}, "not a task"]),
            encoding="utf-8",
        )

        output = self.capture_output(main.load_tasks)

        self.assertEqual(output.count("Warning"), 1)
        self.assertEqual(main.load_tasks(), [])

    @patch("builtins.input", return_value="Write a report")
    def test_add_task_saves_a_new_task(self, _mock_input):
        tasks = []
        output = self.capture_output(main.add_task, tasks)

        self.assertEqual(tasks, [{"title": "Write a report", "completed": False}])
        self.assertEqual(main.load_tasks(), tasks)
        self.assertIn("Task added", output)

    @patch("builtins.input", return_value="   ")
    def test_empty_task_is_rejected(self, _mock_input):
        tasks = []
        output = self.capture_output(main.add_task, tasks)

        self.assertEqual(tasks, [])
        self.assertIn("cannot be empty", output)

    def test_show_tasks_uses_completion_markers(self):
        tasks = [
            {"title": "First task", "completed": False},
            {"title": "Second task", "completed": True},
        ]
        output = self.capture_output(main.show_tasks, tasks)

        self.assertIn("1. [ ] First task", output)
        self.assertIn("2. [x] Second task", output)

    @patch("builtins.input", return_value="1")
    def test_complete_task_updates_and_saves_the_task(self, _mock_input):
        tasks = [{"title": "Finish homework", "completed": False}]
        output = self.capture_output(main.complete_task, tasks)

        self.assertTrue(tasks[0]["completed"])
        self.assertEqual(main.load_tasks(), tasks)
        self.assertIn("Task completed", output)

    @patch("builtins.input", return_value="word")
    def test_non_numeric_task_number_is_rejected(self, _mock_input):
        tasks = [{"title": "Keep this", "completed": False}]
        output = self.capture_output(main.delete_task, tasks)

        self.assertEqual(len(tasks), 1)
        self.assertIn("Invalid number", output)

    @patch("builtins.input", return_value="1")
    def test_delete_task_removes_and_saves_the_task(self, _mock_input):
        tasks = [{"title": "Remove this", "completed": False}]
        output = self.capture_output(main.delete_task, tasks)

        self.assertEqual(tasks, [])
        self.assertEqual(main.load_tasks(), [])
        self.assertIn("Task deleted", output)


if __name__ == "__main__":
    unittest.main()
