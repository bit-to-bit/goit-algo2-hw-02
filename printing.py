from typing import List, Dict
from dataclasses import dataclass


@dataclass
class PrintJob:
    id: str
    volume: float
    priority: int
    print_time: int


@dataclass
class PrinterConstraints:
    max_volume: float
    max_items: int


def get_models_group(sorted_jobs: List[Dict], constraints: Dict) -> tuple:
    """
    Обирає групу моделей для включення в чергу друку

    Args:
        sorted_jobs: Відсортований за пріоритетом список завдань на друк
        constraints: Обмеження принтера

    Returns:
        Tuple з групою моделей, списком остатку завдань та часом на друк групи
    """

    max_volume = constraints.get("max_volume")
    max_items = constraints.get("max_items")

    group = []
    remaining_jobs = sorted_jobs.copy()

    time = 0
    volume = 0
    items = 0

    for job in sorted_jobs:
        if volume + job.get("volume") <= max_volume:
            items += 1
            volume += job.get("volume")
            remaining_jobs.remove(job)
            group.append(job.get("id"))
            time = max(time, job.get("print_time"))

        if items == max_items or volume == max_volume:
            break

    return (group, remaining_jobs, time)


def optimize_printing(print_jobs: List[Dict], constraints: Dict) -> Dict:
    """
    Оптимізує чергу 3D-друку згідно з пріоритетами та обмеженнями принтера

    Args:
        print_jobs: Список завдань на друк
        constraints: Обмеження принтера

    Returns:
        Dict з порядком друку та загальним часом
    """

    print_order = []
    total_time = 0

    sorted_jobs = sorted(print_jobs, key=lambda obj: obj["priority"])

    while len(sorted_jobs) > 0:
        group, sorted_jobs, time = get_models_group(sorted_jobs, constraints)
        print_order.extend(group)
        total_time += time

    return {"print_order": print_order, "total_time": total_time}
