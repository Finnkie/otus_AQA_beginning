"""Парсер системных процессов команды ps aux.

Собирает отчёт о состоянии системы, выводит его в стандартный поток
вывода и сохраняет в txt-файл с именем текущей даты и времени.
"""
import subprocess
from datetime import datetime


def get_processes():
    """Возвращает список процессов из вывода команды ps aux."""
    result = subprocess.run(
        ["ps", "aux"], capture_output=True, text=True, check=True
    )
    lines = result.stdout.strip().split("\n")[1:]  # первая строка - заголовок

    processes = []
    for line in lines:
        # Разбиваем строку не более чем на 11 частей: команда с пробелами
        columns = line.split(None, 10)
        if len(columns) < 11:
            continue
        processes.append(
            {
                "user": columns[0],
                "cpu": float(columns[2]),
                "mem": float(columns[3]),
                "command": columns[10],
            }
        )
    return processes


def build_report(processes):
    """Составляет текстовый отчёт по списку процессов."""
    # Список пользователей и количество процессов у каждого
    users = []
    counts = {}
    for process in processes:
        user = process["user"]
        if user not in counts:
            counts[user] = 0
            users.append(user)
        counts[user] += 1

    # Суммарное потребление памяти и процессора
    total_mem = 0.0
    total_cpu = 0.0
    for process in processes:
        total_mem += process["mem"]
        total_cpu += process["cpu"]

    # Процессы, которые больше всего используют память и процессор
    top_mem_process = processes[0]
    top_cpu_process = processes[0]
    for process in processes:
        if process["mem"] > top_mem_process["mem"]:
            top_mem_process = process
        if process["cpu"] > top_cpu_process["cpu"]:
            top_cpu_process = process

    users_list = ", ".join(f"'{user}'" for user in sorted(users))

    lines = [
        "Отчёт о состоянии системы:",
        f"Пользователи системы: {users_list}",
        f"Процессов запущено: {len(processes)}",
        "",
        "Пользовательских процессов:",
    ]
    for user in sorted(users):
        lines.append(f"{user}: {counts[user]}")
    lines += [
        "",
        f"Всего памяти используется: {total_mem:.1f}%",
        f"Всего CPU используется: {total_cpu:.1f}%",
        f"Больше всего памяти использует: {top_mem_process['command'][:20]}",
        f"Больше всего CPU использует: {top_cpu_process['command'][:20]}",
    ]
    return "\n".join(lines)


def main():
    processes = get_processes()
    report = build_report(processes)

    print(report)

    filename = datetime.now().strftime("%d-%m-%Y-%H:%M-scan.txt")
    with open(filename, "w", encoding="utf-8") as file:
        file.write(report)
    print(f"\nОтчёт сохранён в файл: {filename}")


if __name__ == "__main__":
    main()
