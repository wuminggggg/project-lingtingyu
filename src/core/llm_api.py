import io
import base64
import logging
import requests


def encode_image(image):
    image_io = io.BytesIO()
    logging.debug(f"原始分辨率{image.size}")
    image.save(image_io, format="JPEG",quality=50,optimize=True)
    img_str = base64.b64encode(image_io.getvalue()).decode('utf-8')
    logging.debug(f"压缩成功后字符串长度：{len(img_str)}")
    return img_str

def call_llm_api(input_text,personal_prompt,image_base64,window_title,model):
    prompt = f"你是一个通过用户输入和用户目前窗口以及截屏来进行辅助的智能管家，目前用户给予你的人设为：{personal_prompt}，用户目前窗口是:{window_title},请你结合用户截图分析内容并给出回答。"

    text_part = {"type":"text","text":f"{input_text}"}
    image_part = {"type":"image_url","image_url":{"url":f"data:image/jpeg;base64,{image_base64}"}}
    msg_system = {"role":"system","content":f"{prompt}"}
    msg_user = {"role":"user","content":[image_part]+[text_part]}
    payload = {"model":f"{model}","messages":[msg_system,msg_user],"stream":"false","thinking":{"type":"disabled"}}

    return payload

def post_litter(payload,url,api_key):
    headers = {"Content-Type":"application/json","Authorization":f"Bearer {api_key}"}
    try:
        response = requests.post(url,headers = headers, json = payload,timeout=120)
        if response.status_code == 200:
            result = response.json()
            ai_message = result['choices'][0]['message']['content']
        else:
            ai_message = f"发送失败了，错误码：{response.status_code},/n详细错误：{response.text}"

        return ai_message
    except Exception as e:
        logging.error(f"网络层致命错误：{e}")
        return None
