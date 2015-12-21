from test_utils import TempDirectoryContext

from shedclient import task_tracker


def test_task_tracker():
    with TempDirectoryContext() as context:
        config = dict(
            task_tracking_directory=context.temp_directory
        )
        tracker = task_tracker.build_task_tracker(config)
        assert len(tracker.list_active_tasks()) == 0

        task0_id = tracker.register_task({"state": "new"})
        assert len(tracker.list_active_tasks()) == 1

        task0_state0 = tracker.read_task(task0_id)
        assert task0_state0["state"] == "new"

        tracker.delete_task(task0_id)
        assert len(tracker.list_active_tasks()) == 0

        task1_id = tracker.register_task({"state": "new"})
        assert len(tracker.list_active_tasks()) == 1

        tracker.update_task(task1_id, {"state": "queued", "name": "task 1"})
        task1_state0 = tracker.read_task(task1_id)
        assert task1_state0["state"] == "queued"
        assert task1_state0["name"] == "task 1"
