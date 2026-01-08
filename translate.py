import requests
import config
from log_util import logger

def ai_translate(text, *_args,
                 base_url=config.OPEN_AI_BASE_URL,
                 key=config.OPEN_AI_KEY,
                 model=config.OPEN_AI_MODEL):

    resp = requests.post(f'{base_url}/chat/completions'
                 , headers={
            'Authorization': f'Bearer {key}',
            'Content-Type': 'application/json'
        }, json={
            "model": f"{model}",
            "messages": [
                {"role": "system", "content": "翻译 用户提供的内容到简体中文， 除了用户提到的内容不要附加任何信息。"},
                {"role": "user", "content": f"{text}"}
            ],
            "stream": False
        })
    logger.info(f"OpenAI 翻译结果: {resp.json()}")
    try:
        if resp.status_code == 200:
            return resp.json()['choices'][0]['message']['content']
        elif 'data_inspection_failed' == resp.json()['error']['type']:
            logger.info("OpenAI 翻译失败，更换配置重试")
            # 更换配置重试
            return ai_translate(text,
                                base_url=config.OPEN_AI_BASE_URL_2,
                                key=config.OPEN_AI_KEY_2,
                                model=config.OPEN_AI_MODEL_2)
        else:
            # 翻译失败返回原文
            logger.info(f"翻译失败: {resp.json()}")
            return text
    except Exception as e:
        raise e

















if __name__ == '__main__':
    print(ai_translate('性処理ペットでも、肉オナホでも、ご主人様の命令とあらば完全合意で全力ご奉仕するドMボディメイド 伊藤舞雪'))