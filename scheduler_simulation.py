"""Run a single-processor, nonpreemptive scheduling simulation."""

from statistics import mean
from priority_queue import PriorityQueue, Task


def simulate(tasks):
    arrivals = sorted(tasks, key=lambda task: task.arrival_time)
    ready = PriorityQueue()
    results = []
    clock = 0
    next_arrival = 0
    while next_arrival < len(arrivals) or not ready.is_empty():
        if ready.is_empty():
            clock = max(clock, arrivals[next_arrival].arrival_time)
        while next_arrival < len(arrivals) and arrivals[next_arrival].arrival_time <= clock:
            ready.insert(arrivals[next_arrival])
            next_arrival += 1
        task = ready.extract_max()
        finish = clock + task.duration
        wait = clock - task.arrival_time
        results.append((task.task_id, clock, finish, wait, finish > task.deadline))
        clock = finish
    return results


if __name__ == "__main__":
    tasks = [
        Task("A", 2, 0, 8, 4),
        Task("B", 5, 1, 7, 2),
        Task("C", 5, 2, 10, 3),
        Task("D", 1, 3, 8, 2),
        Task("E", 4, 12, 15, 2),
    ]
    results = simulate(tasks)
    print("Task  Start  Finish  Wait  Deadline missed?")
    for task_id, start, finish, wait, missed in results:
        status = "Yes" if missed else "No"
        print(f"{task_id:4} {start:5} {finish:7} {wait:5}  {status}")
    print(f"\nAverage wait: {mean(row[3] for row in results):.2f} time units")
    print(f"Deadlines missed: {sum(row[4] for row in results)}/{len(results)}")
