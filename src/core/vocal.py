import os
import queue
import time
import json
import zipfile
import requests
import sounddevice as sd
import vosk


#检测是否存在模型，没有就下载
base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
model_path = os.path.join(base_dir, "vosk-model-small-cn-0.22")
zip_path = model_path + ".zip"

if os.path.exists(os.path.join(model_path, "conf")):
        print(f"模型已就绪: {model_path}")
else:
    url = f"https://alphacephei.com/vosk/models/vosk-model-small-cn-0.22.zip"
    print(f"正在从服务器拉取模型 (约 40MB)...")
    response = requests.get(url,stream=True)
    if response.status_code == 200:
        with open(zip_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print("下载完成，准备解压...")
    else:
        raise Exception(f"下载失败，状态码: {response.status_code}")
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        # 解压到项目根目录
        zip_ref.extractall(base_dir)

    os.remove(zip_path)  # 删掉压缩包省空间
    print(f"模型自动配置完成！")


#读取模型，开始加载
model = vosk.Model(r"C:\Users\25226\Desktop\project_lingtingyu\project_lingtingyu\vosk-model-small-cn-0.22")
rate = 16000
rec = vosk.KaldiRecognizer(model,rate)

audio_queue = queue.Queue()

def audio_call_call_back(indata,frames,time,status):
    audio_queue.put(bytes(indata))

def get_word():
    result_dict = json.loads(rec.Result())
    textgw = result_dict.get("text", "").replace(" ", "")
    return textgw

with sd.RawInputStream(samplerate=rate,blocksize=8000,dtype='int16',channels=1,callback=audio_call_call_back):
    print(">>>系统监听中---")

    while True:
        data = audio_queue.get()

        if rec.AcceptWaveform(data):
            text = get_word()
            if text == "说话":
                print("监听启动")
                try:
                    while True:
                        data = audio_queue.get(timeout=10)

                        if rec.AcceptWaveform(data):
                            text = get_word()
                            if text:
                                print(f"final text:{text}")

                                if "时间" in text:
                                    now = time.strftime("%H:%M", time.localtime())
                                    print(f"目前时间：{now}")
                                    break

                                elif "关机" in text:
                                    print("系统将关机")
                                    os.system("shutdown /s /t 0")
                                elif "重启" in text:
                                    print("重启")
                                    break
                except queue.Empty:
                    print("监听超时")
                    break

