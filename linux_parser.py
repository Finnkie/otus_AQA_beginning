import subprocess
from datetime import datetime

# Файл для просмотра сырого вывода ps aux
RAW_OUTPUT_FILE = "/home/igrad/Python/otus_AQA_beginning/ps_scan_result.txt"


def check_processes():
    result = subprocess.run(["ps", "aux"], capture_output=True, text=True, check=True)

    with open(RAW_OUTPUT_FILE, "w", encoding="utf-8") as file:
        file.write(result.stdout)

    lines = result.stdout.strip().split("\n")[1:]

    processes = []
    for line in lines:
        columns = line.split(None, 10)
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
    users = []
    counts = {}
    for process in processes:
        user = process["user"]
        if user not in counts:
            counts[user] = 0
            users.append(user)
        counts[user] += 1
    # Память
    total_mem = 0.0
    total_cpu = 0.0
    for process in processes:
        total_mem += process["mem"]
        total_cpu += process["cpu"]
    # Процессы
    top_mem_process = processes[0]
    top_cpu_process = processes[0]
    for process in processes:
        if process["mem"] > top_mem_process["mem"]:
            top_mem_process = process
        if process["cpu"] > top_cpu_process["cpu"]:
            top_cpu_process = process

    users_list = ", ".join(f"'{user}'" for user in sorted(users))

    top_mem_name = top_mem_process["command"].split()[0]
    top_cpu_name = top_cpu_process["command"].split()[0]

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
        f"Больше всего памяти использует: {top_mem_name[:20]}",
        f"Всего CPU используется: {total_cpu:.1f}%",
        f"Больше всего CPU использует: {top_cpu_name[:20]}",
    ]
    return "\n".join(lines)


def main():
    processes = check_processes()
    report = build_report(processes)

    print(report)

    filename = datetime.now().strftime("Отчёт %d-%m-%Y-%H:%M.txt")
    with open(filename, "w", encoding="utf-8") as file:
        file.write(report)
    print(f'\nОтчёт сохранён в файл: "{filename}"')
    print(f"Сырой вывод ps aux сохранён в файл: {RAW_OUTPUT_FILE}")


if __name__ == "__main__":
    main()
