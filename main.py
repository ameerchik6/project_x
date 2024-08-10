# import subprocess
# from stattg.background import keep_alive


# keep_alive()
# print("Запускаю проекты!")
# # Пути к вашим скриптам
project_1 = "stattg/main.py"
project_2 = "hamster/bot.py"
# # project_3 = "path/to/project_3.py"

# # Запуск проектов
# processes = []
# for project in [project_1, project_2]:
#     process = subprocess.Popen(['python', project], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
#     processes.append(process)

# # Функция для чтения и отображения логов
# def read_logs(process, project_name):
#     for stdout_line in iter(process.stdout.readline, ""):
#         print(f"[{project_name}] {stdout_line}", end="")
#     for stderr_line in iter(process.stderr.readline, ""):
#         print(f"[{project_name} ERROR] {stderr_line}", end="")

# # Чтение логов каждого процесса
# for process, project in zip(processes, [project_1, project_2]):
#     read_logs(process, project)

# # Ожидание завершения всех процессов
# for process in processes:
#     process.wait()

# print("Все проекты завершены.")

import threading
import subprocess

def run_script(script_name):
    subprocess.run(["python", script_name])

# Запуск файлов в отдельных потоках
thread1 = threading.Thread(target=run_script, args=(project_1,))
thread2 = threading.Thread(target=run_script, args=(project_2,))

thread1.start()
thread2.start()

thread1.join()
thread2.join()
