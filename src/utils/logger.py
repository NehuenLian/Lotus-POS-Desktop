import logging
import os
import sys
from logging.handlers import TimedRotatingFileHandler


def get_logs_path():
    if getattr(sys, 'frozen', False):
        base_dir = os.path.dirname(sys.executable)
        logs_dir = os.path.join(base_dir, "logs")

    else:
        base_dir = os.path.abspath(".")
        logs_dir = os.path.join(base_dir, "src", "logs")

    return logs_dir

logs_dir = get_logs_path()
if not os.path.exists(logs_dir):
    os.makedirs(logs_dir)


# ============================
# ======== SETUP LOGS ======== 
# ============================

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s: %(message)s')
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

business_logs_path = os.path.join(logs_dir, 'business.log')
data_access_logs_path = os.path.join(logs_dir, 'data_access.log')
controller_logs_path = os.path.join(logs_dir, 'controller.log')

business_file_handler = TimedRotatingFileHandler(business_logs_path, when='midnight', interval=1, backupCount=7)
data_access_files_handler = TimedRotatingFileHandler(data_access_logs_path, when='midnight', interval=1, backupCount=7)
controller_file_handler = TimedRotatingFileHandler(controller_logs_path, when='midnight', interval=1, backupCount=7)

business_file_handler.setFormatter(formatter)
data_access_files_handler.setFormatter(formatter)
controller_file_handler.setFormatter(formatter)

console_logger = logging.getLogger('console')
console_logger.addHandler(console_handler)
console_logger.setLevel(logging.DEBUG)

business_logger = logging.getLogger('business')
business_logger.addHandler(business_file_handler)
business_logger.setLevel(logging.DEBUG)

data_access_logger = logging.getLogger('data_access')
data_access_logger.addHandler(data_access_files_handler)
data_access_logger.setLevel(logging.WARNING)

controller_logger = logging.getLogger('controller')
controller_logger.addHandler(controller_file_handler)
controller_logger.setLevel(logging.INFO)