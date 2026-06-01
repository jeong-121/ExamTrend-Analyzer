"""Qt worker objects for long-running tasks."""

from __future__ import annotations

from typing import Callable, Generic, TypeVar

from PySide6.QtCore import QObject, QRunnable, Signal, Slot

T = TypeVar("T")

class WorkerSignals(QObject):
    finished = Signal(object)
    failed = Signal(str)

class FunctionWorker(QRunnable, Generic[T]):
    """Run a Python callable in QThreadPool and emit a result."""

    def __init__(self, function: Callable[[], T]) -> None:
        super().__init__()
        self.function = function
        self.signals = WorkerSignals()

    @Slot()
    def run(self) -> None:
        try:
            self.signals.finished.emit(self.function())
        except Exception as exc:  # noqa: BLE001 - 전달용 오류 메시지
            self.signals.failed.emit(str(exc))
