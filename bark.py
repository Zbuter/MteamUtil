import requests
import config
from typing import Optional, Dict, Any
from log_util import logger

class BarkNotifier:
    """
    Bark 推送通知功能
    """

    def __init__(self):
        """
        初始化 Bark 推送器
        """
        self.base_url = config.BARK_HOST.rstrip('/')

    def send(self,
             title: str,
             body: str,
             group: Optional[str] = None,
             url: Optional[str] = None,
             level: Optional[str] = None,
             icon: Optional[str] = None,
             badge: Optional[int] = None,
             auto_copy: Optional[bool] = None,
             copy: Optional[str] = None,
             sound: Optional[str] = None) -> Dict[str, Any]:
        """
        发送 Bark 推送消息

        Args:
            title: 消息标题
            body: 消息内容
            group: 分组名称
            url: 点击通知后跳转的 URL
            level: 通知优先级 (active, timeSensitive, passive)
            icon: 自定义图标 URL
            badge: 应用图标徽标数字
            auto_copy: 是否自动复制内容到剪贴板
            copy: 指定复制到剪贴板的内容
            sound: 通知声音

        Returns:
            推送结果字典
        """
        url_path = f"{self.base_url}/{config.BARK_KEY}"

        # 构建请求参数
        params = {
            'title': title,
            'body': body
        }

        if group:
            params['group'] = group
        if url:
            params['url'] = url
        if level:
            params['level'] = level
        if icon:
            params['icon'] = icon
        if badge is not None:
            params['badge'] = str(badge)
        if auto_copy is not None:
            params['automaticallyCopy'] = '1' if auto_copy else '0'
        if copy:
            params['copy'] = copy
        if sound:
            params['sound'] = sound

        try:
            response = requests.get(url_path, params=params, timeout=10)
            response.raise_for_status()
            logger.info(f"Bark 推送成功: title: {title}  body: {body}")
            return response.json()
        except requests.exceptions.RequestException as e:
            return {
                'success': False,
                'error': str(e)
            }

    def send_simple(self, title: str, body: str) -> Dict[str, Any]:
        """
        发送简单推送消息

        Args:
            title: 消息标题
            body: 消息内容

        Returns:
            推送结果字典
        """
        return self.send(title, body)


# 全局函数，便于直接调用
def bark_push(title: str, body: str, **kwargs) -> Dict[str, Any]:
    """
    Bark 推送函数

    Args:
        title: 消息标题
        body: 消息内容
        **kwargs: 其他可选参数

    Returns:
        推送结果字典
    """
    notifier = BarkNotifier()
    return notifier.send(title, body, **kwargs)

