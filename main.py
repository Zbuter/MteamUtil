import mteam
import qb_util
from log_util import logger

try:
    logger.info("开始获取未读消息")
    messageList = mteam.unread_messages()
    logger.info(f"获取到 {len(messageList)} 条未读消息")

    dmms = mteam.extract_dmm_id_from_messages(messageList)
    if len(dmms) == 0:
        logger.info('没有dmm相关的未读消息')

    for data in dmms:

        logger.info(f"处理未读DMM消息 【{data['title']}】 ID: {data['dmm_id']}")
        latest = mteam.get_dmm_latest(data['dmm_id'])

        actress_count = len(latest['dmmInfo']['actressList'])
        size = latest['size']

        if actress_count > 4 or int(size) > 15 * 1024 * 1024 * 1024:
            # 4人以上 或者大于 15GB 忽略
            logger.info(f"DMM ID {data['dmm_id']} 被忽略 - 演员数: {actress_count}, 大小: {size} bytes")
            mteam.unadded_notify(latest)
            # 标记已读
            mteam.make_read(data['id'])
            logger.info(f"未下载 DMM消息已读 - 【{data['title']}】 ID: {data['id']}")

            continue

        torrentId = latest['id']
        code = latest['dmmInfo']['productNumber']
        logger.info(f"开始添加种子下载 - ID: {torrentId}, [{code}] 标题: {latest.get('name', 'Unknown')}")

        browse = mteam.update_last_browse()
        if browse is None:
            logger.info("更新最后浏览时间成功")

        # 添加种子下载
        qb_util.add_metatube(mteam.torrent_link(latest['id']))
        logger.info(f"种子下载已添加 -  [{code}] 标题: {latest.get('name', 'Unknown')}")

        mteam.added_notify(latest)
        logger.info(f"通知已发送 -  [{code}] 标题: {latest.get('name', 'Unknown')}")

        # 标记删除
        mteam.msg_delete(data['id'])
        logger.info(f"开始下载 DMM消息已删除 - 【{data['title']}】 ID: {data['id']}")
    logger.info("========================== 处理完成 ==========================")
except Exception as e:
    error_msg = f'程序执行出错: {str(e)}'
    logger.error(error_msg,exc_info=e, stack_info=True)
    mteam.bark_push('错误', str(e), group='error')
