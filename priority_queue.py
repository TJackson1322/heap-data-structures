"""Indexed heap for scheduling tasks by priority."""

from dataclasses import dataclass, replace


@dataclass(frozen=True)
class Task:
    task_id: str
    priority: int
    arrival_time: int
    deadline: int
    duration: int


class PriorityQueue:
    def __init__(self):
        self._heap = []
        self._positions = {}

    def is_empty(self):
        return not self._heap

    @staticmethod
    def _rank(task):
        return (-task.priority, task.arrival_time, task.task_id)

    def _swap(self, first, second):
        self._heap[first], self._heap[second] = self._heap[second], self._heap[first]
        self._positions[self._heap[first].task_id] = first
        self._positions[self._heap[second].task_id] = second

    def _sift_up(self, index):
        while index > 0:
            parent = (index - 1) // 2
            if self._rank(self._heap[parent]) <= self._rank(self._heap[index]):
                break
            self._swap(parent, index)
            index = parent

    def _sift_down(self, index):
        size = len(self._heap)
        while 2 * index + 1 < size:
            child = 2 * index + 1
            right = child + 1
            if right < size and self._rank(self._heap[right]) < self._rank(self._heap[child]):
                child = right
            if self._rank(self._heap[index]) <= self._rank(self._heap[child]):
                break
            self._swap(index, child)
            index = child

    def insert(self, task):
        if task.task_id in self._positions:
            raise ValueError(f"Duplicate task ID: {task.task_id}")
        index = len(self._heap)
        self._heap.append(task)
        self._positions[task.task_id] = index
        self._sift_up(index)

    def extract_max(self):
        if self.is_empty():
            raise IndexError("The priority queue is empty")
        self._swap(0, len(self._heap) - 1)
        task = self._heap.pop()
        del self._positions[task.task_id]
        if self._heap:
            self._sift_down(0)
        return task

    def change_priority(self, task_id, new_priority):
        index = self._positions[task_id]
        task = self._heap[index]
        self._heap[index] = replace(task, priority=new_priority)
        if new_priority > task.priority:
            self._sift_up(index)
        elif new_priority < task.priority:
            self._sift_down(index)


if __name__ == "__main__":
    queue = PriorityQueue()
    queue.insert(Task("A", 2, 0, 8, 3))
    queue.insert(Task("B", 5, 1, 9, 2))
    queue.insert(Task("C", 5, 2, 10, 1))
    queue.change_priority("A", 7)
    assert queue.extract_max().task_id == "A"
    queue.change_priority("B", 1)
    assert queue.extract_max().task_id == "C"
    assert queue.extract_max().task_id == "B"
    assert queue.is_empty()
    print("All priority queue checks passed.")
