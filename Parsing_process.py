import subprocess
import datetime


def parse_ps_aux():
    result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
    lines = result.stdout.split('\n')

    headers = lines[0].split()
    user_index = "USER"
    cpu_index = "%CPU"
    mem_index = "%MEM"
    command_index = "COMMAND"

    count_process = 0
    users = set()
    user_process_count = {}
    total_cpu = 0.0
    total_mem = 0.0
    max_cpu_process = ("", 0.0)
    max_mem_process = ("", 0.0)

    for line in lines[1:]:
        if not line.strip():  # Пропускаем пустые строки
            continue
        count_process += 1
        list_data = line.split(maxsplit=len(headers) - 1)
        # Сшиваю список из значений с заголовком(список из кортежей)->словарь
        dict_values = dict(zip(headers, list_data))

        user = dict_values[user_index]
        users.add(user)
        command = dict_values[command_index][:20]  # ограничение 20 символов срезом
        user_process_count[user] = user_process_count.get(user, 0) + 1
        total_cpu += float(dict_values[cpu_index])
        total_mem += float(dict_values[mem_index])
        cpu = float(dict_values[cpu_index])
        mem = float(dict_values[mem_index])

        if cpu > max_cpu_process[1]:
            max_cpu_process = (command, cpu)

        if mem > max_mem_process[1]:
            max_mem_process = (command, mem)

    timestamp = datetime.datetime.now().strftime("%d-%m-%Y-%H:%M")
    report_filename = f"{timestamp}-scan.txt"

    # Формируем текст отчёта
    report = (f"Отчёт о состоянии системы:\n"
              f"Пользователи системы: {', '.join(users)}\n"
              f"Процессов запущено: {count_process}\n\n"
              f"Пользовательских процессов:\n" +
              "\n".join(f"{user}: {count}" for user, count in
                        user_process_count.items()) +  # items возвращает список кортежей, вскрываем
              f"\n\nВсего памяти используется: {total_mem:.1f}%\n"
              f"Всего CPU используется: {total_cpu:.1f}%\n"
              f"Больше всего памяти использует: {max_mem_process[0]} ({max_mem_process[1]:.1f}%)\n"
              f"Больше всего CPU использует: {max_cpu_process[0]} ({max_cpu_process[1]:.1f}%)\n")

    print(report)

    # Сохраняем отчёт в файл
    with open(report_filename, "w", encoding='utf-8') as f:
        f.write(report)

    print(f"Отчёт сохранён в {report_filename}")


if __name__ == "__main__":
    parse_ps_aux()
