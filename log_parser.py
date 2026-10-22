import argparse
import json
import os
import re

HTTP_METHODS = ["GET", "POST", "PUT", "DELETE", "OPTIONS", "HEAD"]

# Шаблон строки логов
LINE_PATTERN = re.compile(
    r'^(\S+) \S+ \S+ \[([^\]]+)\] "(.*?)" (\d+) (\S+) "(.*?)" "(.*)" (\d+)$'
)


def parse_line(line):
    # Возвращает словарь с данными запроса или None
    match = LINE_PATTERN.match(line)
    if match is None:
        return None

    # Запрос вида "GET /index.html HTTP/1.1" - берём метод и URL
    request_parts = match.group(3).split()
    method = request_parts[0] if request_parts else ""
    url = request_parts[1] if len(request_parts) > 1 else ""

    return {
        "ip": match.group(1),
        "date_time": match.group(2),
        "method": method,
        "url": url,
        "duration": int(match.group(8)),
    }


def collect_stats(log_path):
    total_requests = 0
    method_counts = {}
    for method in HTTP_METHODS:
        method_counts[method] = 0

    ip_counts = {}
    top_requests = []

    with open(log_path, encoding="utf-8", errors="ignore") as file:
        for line in file:
            request = parse_line(line)
            if request is None:
                continue

            total_requests += 1

            if request["method"] in method_counts:
                method_counts[request["method"]] += 1

            ip = request["ip"]
            if ip not in ip_counts:
                ip_counts[ip] = 0
            ip_counts[ip] += 1

            if len(top_requests) < 3:
                top_requests.append(request)
            else:
                fastest_index = 0
                for i in range(1, 3):
                    if (
                        top_requests[i]["duration"]
                        < top_requests[fastest_index]["duration"]
                    ):
                        fastest_index = i
                if request["duration"] > top_requests[fastest_index]["duration"]:
                    top_requests[fastest_index] = request

    count_ip = []
    for ip, count in ip_counts.items():
        count_ip.append((count, ip))
    count_ip.sort(reverse=True)
    top_ips = [{"ip": ip, "requests": count} for count, ip in count_ip[:3]]

    top_requests.sort(key=get_duration, reverse=True)
    top_long = [
        {
            "method": request["method"],
            "url": request["url"],
            "ip": request["ip"],
            "duration_ms": request["duration"],
            "date_time": request["date_time"],
        }
        for request in top_requests
    ]

    return {
        "file": os.path.basename(log_path),
        "total_requests": total_requests,
        "methods": method_counts,
        "top_ips": top_ips,
        "top_long_requests": top_long,
    }


def get_duration(request):
    return request["duration"]


def save_file(stats, json_path):
    with open(json_path, "w", encoding="utf-8") as file:
        json.dump(stats, file, ensure_ascii=False, indent=2)


def find_log_files(path):
    if os.path.isfile(path):
        return [path]

    if os.path.isdir(path):
        log_files = []
        for name in sorted(os.listdir(path)):
            full_path = os.path.join(path, name)
            if name.endswith(".log") and os.path.isfile(full_path):
                log_files.append(full_path)
        return log_files
    return None


def main():
    parser = argparse.ArgumentParser(description="Парсер логов access.log")
    parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="файл лога или директория с логами (по умолчанию текущая)",
    )
    args = parser.parse_args()

    log_files = find_log_files(args.path)
    if not log_files:
        print(f"Не найдено файлов логов: {args.path}")
        raise SystemExit(1)

    for log_path in log_files:
        stats = collect_stats(log_path)
        json_path = log_path + ".json"
        save_file(stats, json_path)
        print(f"\tСтатистика сохранена: {json_path}\n")


if __name__ == "__main__":
    main()
