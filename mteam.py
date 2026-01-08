from typing import List
import re

import log_util
from api import post
from bark import bark_push
from translate import ai_translate


def bytes_to_readable(bytes_value) -> str:
    """
    将字节数转换为人类可读的格式
    """
    bytes_int = int(bytes_value)

    if bytes_int >= 1024 ** 4:  # 太字节 (TB)
        return f"{bytes_int / (1024 ** 4):.2f}TB"
    elif bytes_int >= 1024 ** 3:  # 吉字节 (GB)
        return f"{bytes_int / (1024 ** 3):.2f}GB"
    elif bytes_int >= 1024 ** 2:  # 兆字节 (MB)
        return f"{bytes_int / (1024 ** 2):.2f}MB"
    elif bytes_int >= 1024:  # 千字节 (KB)
        return f"{bytes_int / 1024:.2f}KB"
    else:  # 字节 (B)
        return f"{bytes_int}B"


def dmm_list(dmm_id, page=1, page_size=20):
    return post('/api/dmm/showcase/fetchList', {
        'id': dmm_id,
        'page': str(page),
        'pageSize': str(page_size)
    })


def extract_dmm_id_from_messages(messages) -> List[dict]:
    import re
    dmm_ids = []
    for item in messages:
        context = item.get('context', '')
        match = re.search(r'\[url=/showcaseDetail\?id=(\d+)\]', context)
        if match:
            dmm_ids.append({
                'id': item.get('id'),
                'title': item.get('title'),
                'dmm_id': int(match.group(1))
            })
    return dmm_ids


def get_dmm_latest(dmm_id, page_size=20):
    get_dmm_by_index(dmm_id, -1, page_size)


def get_dmm_total(dmm_id):
    return dmm_list(dmm_id, page=1, page_size=1)['detail']['count']


def search_dmm_actor(keyword='', search_type: str = 'cns', page_number=1, page_size=100):
    return post('/api/dmm/showcase/search', {
        'pageNumber': page_number,
        'pageSize': page_size,
        'searchType': search_type,
        'keyword': keyword
    })


def get_dmm_by_index(dmm_id, index, page_size=20):
    # 获取第一页数据以获取总数
    first_page_data = dmm_list(dmm_id, page=1, page_size=page_size)
    total = int(first_page_data['detail']['count'])

    # 处理空列表情况
    if total == 0:
        raise IndexError("列表为空")

    # 处理负数索引（-1 表示最后一个，-2 表示倒数第二个，以此类推）
    if index < 0:
        index = total + index

    # 处理索引超出范围的情况
    if index >= total:
        index = total - 1
    elif index < 0:
        index = 0  # 索引不能为负数

    # 计算目标数据所在的页数（从0开始）
    target_page = index // page_size + 1

    # 获取目标页的数据
    if target_page == 1:
        dmm_data = first_page_data
    else:
        dmm_data = dmm_list(dmm_id, page=target_page, page_size=page_size)

    # 计算在当前页中的索引
    index_in_page = index % page_size

    return dmm_data['list'][index_in_page]


def bt_detail(torrent_id):
    return post('/api/torrent/detail', {'id': torrent_id})


def get_bt_detail_images(torrent_id) -> list[str]:
    """
    从文本中提取所有 img 标签的地址
    """
    detail = bt_detail(torrent_id)
    desc = detail['descr']
    # 匹配 [img]...[/img] 格式
    img_pattern = r'\[img\]([^\[\]]+)\[\/img\]'

    urls = []
    # 提取 [img] 格式
    urls.extend(re.findall(img_pattern, desc))

    return urls


def get_messages(keyword='', page_number='1', page_size='10'):
    return post('/api/msg/search', {
        'box': '-2',  # 系统
        'pageNumber': page_number,
        'pageSize': page_size,
        'unread': True,
        'keyword': keyword
    })


def unread_messages():
    result = get_messages()
    return [item for item in result.get('data', []) if item.get('unread')]


def make_read(msg_ids):
    return post('/api/msg/markRead', {'msgIds': msg_ids})


def msg_delete(msg_ids):
    return post('/api/msg/delete', {'msgIds': msg_ids})


def profile(uid=None):
    return post('/api/member/profile', {'uid': uid})


def update_last_browse():
    log_util.logger.info('更新最后浏览时间')
    return post('/api/member/updateLastBrowse', ignore_status=True)


def search_torrent(data):
    # data = {
    #     "mode":"adult",
    #     "onlyFav":1,
    #     "visible":1,
    #     "categories":[],
    #     "pageNumber":1,
    #     "pageSize":100,
    # }
    return post('/api/torrent/search', data, is_json_data=True)


def torrent_detail(torrent_id):
    return post('/api/torrent/detail', {'id': torrent_id})


def torrent_link(torrent_id):
    return post('/api/torrent/genDlToken', {'id': torrent_id})


def category_list():
    return post('/api/torrent/categoryList')


def source_list():
    return post('/api/torrent/sourceList')


def detail_url(torrent_id):
    return 'https://kp.m-team.cc' + '/detail/' + str(torrent_id)


def added_notify(dmm_data):
    bark_push(f'已添加到下载队列：[{dmm_data['dmmInfo']['productNumber']}]', f"""
 id: {dmm_data['id']}
 文件大小： {bytes_to_readable(dmm_data['size'])}
  
 番号：{dmm_data['dmmInfo']['productNumber']}
 演员: {dmm_data['dmmInfo']['actressList']} 
 原标题: {dmm_data['name']}
 中文标题: {ai_translate(dmm_data['name'])}



 url: {detail_url(dmm_data['id'])}
""", group='metatube', url=f'{detail_url(dmm_data['id'])}')


def unadded_notify(dmm_data):
    bark_push(f'未下载：[{dmm_data['dmmInfo']['productNumber']}]', f"""
 id: {dmm_data['id']}
 文件大小： {bytes_to_readable(dmm_data['size'])}
 
 番号：{dmm_data['dmmInfo']['productNumber']}
 演员: {dmm_data['dmmInfo']['actressList']} 
 原标题: {dmm_data['name']}
 中文标题: {ai_translate(dmm_data['name'])}

url: {detail_url(dmm_data['id'])}
""", group='undownload', url=f'{detail_url(dmm_data['id'])}')


if __name__ == '__main__':
    # data = search_torrent({
    #     "mode": "movie",
    #     "visible": 1,
    #     "categories": [],
    #     "pageNumber": 1,
    #     "pageSize": 20
    # })

    # data = dmm_list(9797)
    data = update_last_browse()
    print(data)
