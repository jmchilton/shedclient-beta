from .task_tracker import build_task_tracker
from .install_directory import InstallsDirectory


def ensure(context_or_dict):
    if not isinstance(context_or_dict, ShedClientContext):
        return ShedClientContext(**context_or_dict)
    else:
        return context_or_dict


class ShedClientContext(object):

    def __init__(self, **kwds):
        self.install_directory_path = kwds.get("install_directory", "database/shed_installs")
        self.task_tracker_directory = kwds.get("task_tracker_directory", None)

        self._task_tracker = None
        self._installs_directory = None

    def to_dict(self):
        return dict(
            install_directory=self.install_directory_path,
            task_tracker_directory=self.task_tracker_directory,
        )

    @property
    def task_tracker(self):
        # TODO: lock
        if self._task_tracker is None:
            self._task_tracker = build_task_tracker(
                task_tracker_directory=self.task_tracker_directory
            )
        return self._task_tracker

    @property
    def installs_directory(self):
        # TODO: lock
        if self._installs_directory is None:
            self._installs_directory = InstallsDirectory(
                self
            )
        return self._installs_directory
