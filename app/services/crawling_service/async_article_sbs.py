import aiohttp
from bs4 import BeautifulSoup
from typing import Dict, Optional

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

SELECTORS = {
    "title": ['h1.article_main_tit#news-title', 'h1.article_main_tit', '.article_main_tit', 'h1'],
    "image": ['img.mainimg', '.mainimg img', '.article_img img', '.content_img img'],
    "content": ['div.text_area[itemprop="articleBody"]', '.text_area', '.article_content', '.content'],
    "reporter": ['span[itemprop="name"]', '.reporter', '.author', '.byline'],
    "published_time": ['div.date_area span', '.date_area span', '.date span', 'time'],
    "published_meta": ['div.date_area meta[itemprop="datePublished"]', 'meta[itemprop="datePublished"]'],
}

"""여러 셀렉터 중 하나를 선택하여 텍스트 반환"""
def select_one_text(soup: BeautifulSoup, selectors) -> Optional[str]:
    for sel in selectors:
        el = soup.select_one(sel)
        if el:
            return el.get_text(strip=True)
    return None

def get_image_url(soup: BeautifulSoup) -> Optional[str]:
    for selector in SELECTORS['image']:
        img_tag = soup.select_one(selector)
        if img_tag:
            # 1. srcset 우선
            srcset = img_tag.get('srcset') or img_tag.get('data-srcset')
            if srcset:
                if not isinstance(srcset, str):
                    srcset = ' '.join(srcset)
                candidates = [s.strip().split(' ')[0] for s in srcset.split(',') if s.strip()]
                if candidates:
                    src = candidates[-1]
                    if src.startswith('//'):
                        return f'https:{src}'
                    elif src.startswith('http'):
                        return src
                    else:
                        return f'https://img.sbs.co.kr{src}' if src.startswith('/') else src
            # 2. src
            src = img_tag.get('src')
            if isinstance(src, str) and src.strip():
                if src.startswith('//'):
                    return f'https:{src}'
                elif src.startswith('http'):
                    return src
                else:
                    return f'https://img.sbs.co.kr{src}' if src.startswith('/') else src
    return None

def get_content_text(soup: BeautifulSoup) -> Optional[str]:
    content_div = soup.select_one(SELECTORS['content'][0])  # 첫 번째 셀렉터 사용
    if content_div:
        # Remove all script/style tags
        for tag in content_div(['script', 'style']):
            tag.decompose()
        text = content_div.get_text(separator=' ', strip=True)
        return text if isinstance(text, str) and len(text) > 20 else None
    return None

def get_published_time(soup: BeautifulSoup) -> Optional[str]:
    # Prefer meta tag for machine-readable time
    for meta_selector in SELECTORS['published_meta']:
        meta = soup.select_one(meta_selector)
        if meta and meta.has_attr('content'):
            content_val = meta['content']
            if isinstance(content_val, str):
                return content_val
    # Fallback to visible text
    return select_one_text(soup, SELECTORS['published_time'])

async def extract_sbs_article_async(session: aiohttp.ClientSession, url: str) -> Dict[str, Optional[str]]:
    try:
        async with session.get(url, headers=HEADERS, timeout=aiohttp.ClientTimeout(total=10)) as response:
            if response.status != 200:
                raise Exception(f"HTTP {response.status}")
            html = await response.text()
            soup = BeautifulSoup(html, 'lxml')
            return {
                "title": select_one_text(soup, SELECTORS['title']),
                "url": url,
                "image_url": get_image_url(soup),
                "content": get_content_text(soup),
                "published_time": get_published_time(soup),
                "reporter_name": select_one_text(soup, SELECTORS['reporter']),
            }
    except Exception as e:
        print(f"      ❌ SBS 기사 추출 중 예외 발생: {e}")
        return {
            "title": None,
            "url": None,
            "image_url": None,
            "content": None,
            "published_time": None,
            "reporter_name": None,
            "error": str(e)
        }
