from path import Path

LOG_PATH = Path(__file__).parent / 'mteam.log'

QB_USERNAME = 'admin'
QB_PASSWORD = 'adminadmin'
QB_HOST = 'http://bt'

BARK_KEY = '**************'
BARK_HOST = 'https://api.day.app'

# 翻译用 2 在 1 翻译失败会尝试这个模型
OPEN_AI_BASE_URL_2 = 'https://api.deepseek.com'
OPEN_AI_KEY_2 = 'sk-abcdefg'
OPEN_AI_MODEL_2 = 'deepseek-chat'
# 翻译用 1
OPEN_AI_BASE_URL = 'https://dashscope.aliyuncs.com/compatible-mode/v1'
OPEN_AI_KEY = 'sk-abcdefg'
OPEN_AI_MODEL = 'qwen-max'


# MTeam secret 根据官网获取
MT_SECRET = "HLkPcWmycL57mfJt"
MT_HOST = 'https://api.m-team.cc'
MT_HEADERS = {
    'origin': 'https://kp.m-team.cc',
    'referer': 'https://kp.m-team.cc',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',

    # 基本固定 网站不更新不会发生变更。
    'visitorid': '6d387da74bae999bbd222a958f81d428',
    'webversion': '1140',
    # 每次登陆后生成
    'did': '35070b81f1ed4abe96d8c954007a5c3d',
    'authorization': 'jwt'
}
