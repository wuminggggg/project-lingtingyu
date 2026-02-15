import logging

logging.basicConfig(
    level=logging.INFO,  # 设置日志级别（INFO, DEBUG, WARNING, ERROR）
    format='%(asctime)s - [%(levelname)s] - %(message)s', # 定义格式：时间 - 级别 - 内容
    datefmt='%H:%M:%S',  # 时间格式：时:分:秒
    handlers = [
        logging.FileHandler("assets/agent.log", encoding='utf-8'),  # 存入文件
        logging.StreamHandler()  # 同时打印到屏幕
    ]
)

import yaml
from src.core import capture,llm_api,startup


logging.info("my_agent已经启动 √")

config = startup.load_config()
logging.info("成功导入config文件")

img_str = llm_api.encode_image(capture.prt_sc())
logging.info("成功转换base64编码")

window_title = capture.get_window_name()
logging.info("正在取得窗口名...成功")
logging.debug(f"窗口名：{window_title}")

payload =  llm_api.call_llm_api(config['input_text'],config['personal_prompt'],img_str,window_title,config['model'])
logging.info("成功拼接字典！")

ai_response = llm_api.post_litter(payload,config['base_url'],config['api_key'])
logging.info(f"ai回复生成完毕，回复内容:{ai_response}")
