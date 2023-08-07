from bs4 import BeautifulSoup
import requests
import shutil
from mdutils.mdutils import MdUtils
import subprocess
import json
import time
import os


site = 'https://www.economist.com/weeklyedition'

def ArticleRequest():
    subprocess.check_output("./utils/articlefetch.sh")
    with open('./temp/articlelist.json') as f:
	    data = json.load(f)
    return data


def ArticleEbookConvert():
    if not os.path.exists('./temp'):
        os.makedirs('./temp')
    if not os.path.exists('./ebooks'):
        os.makedirs('./ebooks')
    articles = ArticleRequest()
    edition = GetEdition()
    mdFile = MdUtils(file_name=edition, title=edition)
    count = 0
    for article in articles['chapters']:
        if 'interactive' in str(article):
            continue
        time.sleep(1)
        site = requests.get(str(article['url']))
        if site.status_code == 200:
            print('Getting: ', str(article['url']))
            html = site.content
            soup = BeautifulSoup(html, 'lxml')
            header = str(soup.find('h1').text)
            sub_header = soup.find_all('h2')
            try:
                sub_header = str(sub_header[8].text)
            except IndexError:
                sub_header = str('')
                pass
            try:
                top_img = soup.find('img')
                top_img_src = top_img.attrs['src']
                r = requests.get(top_img_src, stream=True)
                if r.status_code == 200:
                    count+=1
                    with open('./temp/img'+ str(count) +'.png', 'wb') as f:
                        r.raw.decode_content = True
                        shutil.copyfileobj(r.raw, f)
            except requests.exceptions.MissingSchema or requests.exceptions.InvalidSchema:
                print('missing/invalid schema')
                continue
            print('Adding MD...')
            mdFile.new_header(level=1, title=header)
            mdFile.new_line(text=sub_header, bold_italics_code='b')
            mdFile.new_line(mdFile.new_inline_image(text='', path='./temp/img' + str(count) +'.png'))
            article_body = soup.find_all('p', class_ ='article__body-text')
            try:
                if 'our weekly' in article_body[-1].text:
                    article_body.pop()
                for p in article_body:
                    if 'Read more' in p.text:
                        continue
                    else:
                        mdFile.new_paragraph(p.text)
                mdFile.new_line()
            except IndexError:
                print('Index error')
                continue
        else:
            print('Failed Getting: ', str(article['url']), '\n', 'Error: ', site.status_code)
            continue
    try:
        mdFile.create_md_file()      
        print('SUCCESS: Markdown generated!')
        MdToEpub()
        print('SUCCESS: Markdown converted to Epub!')
        print("Enjoy!")
    finally:
        shutil.rmtree('./temp')
        os.remove('./' + edition + '.md')
        shutil.move('./' + edition + '.epub', './ebooks/')

    
def GetEdition():
    result = subprocess.run(["./utils/finalurl.sh" + " " + str(site)], shell=True, capture_output=True, text=True)
    return_url = result.stdout
    return str(return_url[-10:])

def MdToEpub():
    edition = GetEdition()
    subprocess.run(["./utils/mdtoepub.sh" + " " + edition + ".md" + " "  + edition + ".epub"], shell=True, capture_output=True, text=True)

ArticleEbookConvert()