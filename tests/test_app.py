
import unittest
import app as task_app


class TaskManagerTests(unittest.TestCase):

    def setUp(self):
        task_app.app.config["TESTING"] = True
        task_app.tasks.clear()
        task_app.next_id = 1
        self.client = task_app.app.test_client()

    def test_home_page_loads(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Agile Task Manager", response.data)

    def test_add_task(self):
        response = self.client.post(
            "/add",
            data={"title": "Complete assignment"},
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(task_app.tasks), 1)
        self.assertEqual(
            task_app.tasks[0]["title"], "Complete assignment"
        )

    def test_empty_task_is_not_added(self):
        self.client.post("/add", data={"title": "   "})
        self.assertEqual(len(task_app.tasks), 0)

    def test_complete_task(self):
        self.client.post(
            "/add", data={"title": "Test application"}
        )
        task_id = task_app.tasks[0]["id"]

        self.client.post(f"/toggle/{task_id}")

        self.assertTrue(task_app.tasks[0]["completed"])

    def test_delete_task(self):
        self.client.post(
            "/add", data={"title": "Delete this task"}
        )
        task_id = task_app.tasks[0]["id"]

        self.client.post(f"/delete/{task_id}")

        self.assertEqual(len(task_app.tasks), 0)


if __name__ == "__main__":
    unittest.main()
