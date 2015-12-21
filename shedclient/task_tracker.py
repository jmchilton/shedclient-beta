import os
import json
import uuid
import tempfile

from galaxy.util import is_uuid


def build_task_tracker(config):
    return TaskTracker(config)


# Iteration 2, bring in update times.
# Iteration 3, optimized variant of this that uses a database.
class TaskTracker(object):
    """ Tracks the state a task is in and maps to task framework
    ids.
    """

    def __init__(self, config):
        task_tracking_directory = config.get("task_tracking_directory", None)
        if task_tracking_directory is None:
            task_tracking_directory = tempfile.mkdtemp()
        self.task_tracking_directory = task_tracking_directory

    def list_active_tasks(self):
        task_files = os.listdir(self.task_tracking_directory)
        return task_files

    def register_task(self, state):
        task_id = str(uuid.uuid4())
        self._write_task_state(task_id, state)
        return task_id

    def update_task(self, task_id, attributes):
        state = self._read_task_state(task_id)
        state.update(attributes)
        self._write_task_state(task_id, state)

    def read_task(self, task_id):
        return self._read_task_state(task_id)

    def delete_task(self, task_id):
        task_file = self._task_file(task_id)
        if not os.path.exists(task_file):
            return False
        else:
            os.remove(task_file)
            return True

    def _read_task_state(self, task_id):
        with open(self._task_file(task_id), 'r') as f:
            state = json.load(f)

        return state

    def _write_task_state(self, task_id, state):
        with open(self._task_file(task_id), 'w') as f:
            json.dump(state, f)

    def _task_file(self, task_id):
        self._ensure_task_id(task_id)
        return os.path.join(self.task_tracking_directory, task_id)

    def _ensure_task_id(self, task_id):
        if not is_uuid(task_id):
            raise ValueError("Invalid task id %s" % task_id)
