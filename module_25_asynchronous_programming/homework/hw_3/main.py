import aiohttp
import asyncio
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

start_url = 'https://sales.skillbox.kz/sale/kz/sale2022/?utm_source=yandex&utm_medium=cpc&utm_campaign=all_all_yandex_cpc_poisk_sale_kz_brand_skillbox_81714641&utm_content=adg_5103900007%7Cad_13254321692%7Cph_42642848931%7Ckey_скилбокс%7Cdev_desktop%7Cpst_premium_1%7Crgnid_162_Алматы%7Cplacement_none%7Ccreative_%7Bcreative_name%7D&utm_term=скилбокс&yclid=2703854254718451711'
max_iterations = 3
output_file = 'found_links.txt'

visited_urls = set()

semaphore = asyncio.Semaphore(10)


async def fetch_and_parse(url, session, depth):
    async with semaphore:
        async with session.get(url) as response:
            if response.status == 200:
                content = await response.text()
                soup = BeautifulSoup(content, 'html.parser')

                links = [a['href'] for a in soup.find_all('a', href=True)]

                external_links = [urljoin(url, link) for link in links if urlparse(link).netloc != '']

                with open(output_file, 'a') as file:
                    for link in external_links:
                        file.write(link + '\n')

                if depth < max_iterations:
                    for link in external_links:
                        if link not in visited_urls:
                            visited_urls.add(link)
                            await fetch_and_parse(link, session, depth + 1)


async def main():
    visited_urls.add(start_url)
    async with aiohttp.ClientSession() as session:
        await fetch_and_parse(start_url, session, 1)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
