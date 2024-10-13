# import logging
#
# logging.basicConfig(
#     level=logging.INFO,
#     format='%(asctime)s - %(processName)s - %(threadName)s - %(filename)s - %(funcName)s - %(levelname)s - %(message)s'
# )
#
# logger = logging.getLogger(__name__)
import inspect
import os
import threading
import time


def info(message):
    frame = inspect.currentframe().f_back
    code = frame.f_code

    # 获取所需的信息
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    process_name = os.getpid()  # 获取当前进程ID
    thread_name = threading.current_thread().name  # 获取当前线程名称
    filename = os.path.basename(code.co_filename)  # 获取文件名
    func_name = code.co_name  # 获取函数名
    levelname = "INFO"  # 假设日志级别为INFO，你可以根据需要调整

    # 构建输出格式
    output = f"{timestamp} - {process_name} - {thread_name} - {filename} - {func_name} - {levelname} - {message}"
    print(output)

def error(message):
    print(message)