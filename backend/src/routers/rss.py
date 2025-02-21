from feedgen.feed import FeedGenerator
from fastapi import APIRouter, HTTPException, status, Response as FResponse
from src.routers.vuli import get_new_vulti, START, LENGTH


router = APIRouter()


@router.get("/vuli", include_in_schema=False)
async def feed():
    data = await get_new_vulti(START, LENGTH)
    if data == 'error':
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="error",
        )
    else:
        fg = FeedGenerator()
        fg.id('https://sec.cafe/feed/vuli')
        fg.title('SEC.CAFE 安全咖啡 - 漏洞情报')
        fg.link(href='https://sec.cafe/feed/vuli', rel='alternate')
        fg.link(href='https://sec.cafe/feed/vuli', rel='self')
        fg.subtitle('安全本应纯粹，规避内卷，用一杯咖啡回归安全的乐趣！SEC.CAFE 安全咖啡是一个安全爱好者的服务平台与社区。')
        fg.language('zh-CN')
        fg.generator(generator='sec.cafe', version=None, uri=None)
        for _ in data:
            fe = fg.add_entry()
            fe.title(_['title'])
            fe.summary(_['descript'])
            url = 'https://sec.cafe/url/{}'.format(_['tinyurl'])
            fe.link(href=url)
            fe.id(url)
            fe.published('{}T00:00:00+08:00'.format(_['publish_time']))
        atom_feed_str = fg.atom_str(pretty=True, xml_declaration=False)
        atom_feed_str = str(atom_feed_str, encoding="utf-8")
        return FResponse(content=atom_feed_str, media_type="application/xml")
