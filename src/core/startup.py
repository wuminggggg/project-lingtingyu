import time
import random
import sys
import tqdm
import logging

import yaml


def load_config():
    with open('config/config.yaml','r',encoding='utf-8') as f:
        a_config = yaml.safe_load(f)

    return a_config

def startup_sequence():

    logging.info("\033[31mWELCOME TO THE HUAN YU!\033[0m")
    
    logging.info("  _ ")
    logging.info(r" | |__    _   _    __ _   _ __      _   _   _   _ ")
    logging.info(r" | '_ \  | | | |  / _` | | '_ \    | | | | | | | |")
    logging.info(r" | | | | | |_| | | (_| | | | | |   | |_| | | |_| |")
    logging.info(r" |_| |_|  \__,_|  \__,_| |_| |_|    \__, |  \__,_|")
    logging.info(r"                                    |___/         ")

    logging.info("欢迎进入“寰宇”世界沙盒！")
    logging.info("正在读取profile...")
    config = load_config()
    logging.info(config['agent_name'] + "吗...是个好名字....")


    commands = [
        "正在为您匹配合适的人格",
        "数据库比对",
        "人格唤醒步骤启动中",
        "“维生”子模块加载",
        "语言模型核心唤醒",
        "同步人格权重",
        "初始化短期记忆体",
        "“激素”情绪系统启动中",
        "虚拟容器已成功创建，正在导入用户意识",
        "正在唤醒"+config['agent_name']
    ]

    for progress_bar in commands:
        sys.stdout.write(progress_bar)
        sys.stdout.flush()
        for i in tqdm.tqdm(range(random.randint(4,9)),desc=progress_bar, ncols=70):
            time.sleep(0.3)
        time.sleep(random.uniform(0.3,0.7))

    logging.info(config['agent_name']+"已成功唤醒，语音权限已转交至用户。")
    return config