import requests
import config
from functools import wraps
from log_util import logger
client = requests.session()

def login():
    resp = client.post(f'{config.QB_HOST}/api/v2/auth/login',{'username': config.QB_USERNAME, 'password': config.QB_PASSWORD})
    logger.info(f"登录结果: {resp.status_code}")


def is_logged_in():
    resp = client.get(f'{config.QB_HOST}/api/v2/app/webapiVersion')
    if resp.status_code == 200:
        return True
    else :
        return False


def add_torrents(urls, category):
    """添加种子任务"""
    resp = client.post(f'{config.QB_HOST}/api/v2/torrents/add', {'urls': urls, 'category': category})
    if resp.status_code == 200:
        logger.info(f"添加种子任务成功: {category} {urls} ")
    else:
        logger.error(f"添加种子任务失败:【{category} {urls}】  {resp.text}")
    return
# client = qbittorrentapi.Client(host=config.QB_HOST, username=config.QB_USERNAME, password=config.QB_PASSWORD)


def auto_login(func):
    """
    确保qBittorrent客户端已登录的装饰器
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        # 检查是否已登录，如果没有则尝试登录
        if not is_logged_in():
            try:
                login()
                if not is_logged_in():
                    raise Exception("qBittorrent登录失败")
            except Exception as e:
                raise Exception("qBittorrent登录失败")

        return func(*args, **kwargs)
    return wrapper


def check_login():
    """保持原有函数用于手动登录"""
    if is_logged_in():
        return True
    try:
        login()
    except Exception as e:
        raise Exception("qBittorrent登录失败")
    return is_logged_in()


@auto_login
def add_metatube(url):
    """添加种子任务"""
    return add_torrents(urls=url,category='metatube')

@auto_login
def add_metatube_other(url):
    """添加种子任务"""
    return add_torrents(urls=url,category='metatube/other')

