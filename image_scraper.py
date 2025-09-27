import nodriver
import re
import time
import json

from bs4 import BeautifulSoup

def find_images(api_out : str) -> list:
    img_urls = []
    s1 = api_out.find('{')
    s2 =api_out.find('{', s1 + 1)

    f1 = api_out[::-1].find('}')
    f2 = api_out[::-1].find('}', f1 + 1)
    f2 = len(api_out)- f2 - 1

    out = api_out[s2:f2 + 1]
    out = out.replace("'", '"')
    lc = out[::-1].find(',')
    lc = len(out) - lc - 1
    out = out[:lc] + out[lc+1:]

    out = out.replace('Date.now()', '""')
    try:
        out = json.loads(out)
    except json.JSONDecodeError as e:
        out = None
        print(e.msg)
        print(f"Problem Part : {out[e.pos -20:e.pos+20]}")
    
    images = out['colorImages']['initial']
    
    for data in images:
        img_urls.append(data['large'])

    return img_urls


async def product_images(url : str) -> list:
    images = []
    browser = await nodriver.start()
    page = await browser.get(url)
    time.sleep(5)
    page_cont = await page.get_content()

    with open('debug_page.html', 'w', encoding='utf-8') as f:
        f.write(page_cont)

    soup = BeautifulSoup(page_cont, 'lxml')
    result = soup.find('script', text=re.compile(r"P\.when\('A'\)\.register"))
    
    out = find_images(result.text)
    return out


if __name__ == '__main__':

    url = 'https://www.amazon.in/Peach-Cuddle-Cushion-Furnishing-Decorative/dp/B08ZNL62NS'
    out = nodriver.loop().run_until_complete(product_images(url))
    print(out)






