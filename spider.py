from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import requests


# 对于常见的静态显示的网页，只需要使用函数fetch_and_save_content.参数url指定待爬取网页地址，filename指定文件路径以保存爬取到的内容
def fetch_and_save_content(url, filename):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # 提取标题  
        headings = [heading.get_text(strip=True) for heading in soup.find_all(['h2', 'h3'])]

        # 提取正文  
        paragraphs = [paragraph.get_text(strip=True) for paragraph in soup.find_all('h2', 'h3', 'p', 'pre')]

        # 提取代码块  
        code_blocks = [code_block.get_text(strip=True) for code_block in soup.find_all('pre')]

        # 写入文件  
        with open(filename, 'w', encoding='utf-8') as file:
            file.write("Headings:\n")
            for heading in headings:
                file.write(f"- {heading}\n")
            file.write("\nParagraphs:\n")
            for paragraph in paragraphs:
                file.write(f"- {paragraph}\n")
            file.write("\nCode Blocks:\n")
            for code in code_blocks:
                file.write(f"- {code}\n")
    else:
        print(f'请求失败，状态码：{response.status_code} 对于URL:{url}')

    # 对于csdn等动态显示的网页，需要使用下面的函数fetch_and_save_content_with_selenium.参数url指定待爬取网页地址，filename指定文件路径以保存爬取到的内容


def fetch_and_save_content_with_selenium(url, filename):
    # 使用ChromeDriver  
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    try:
        driver.get(url)
        # 可选：等待页面加载完成（这里使用简单的sleep代替复杂的等待条件）  
        # import time  
        # time.sleep(10)  # 根据需要调整等待时间  

        # 获取页面源码  
        html = driver.page_source
        # 使用BeautifulSoup解析  
        soup = BeautifulSoup(html, 'html.parser')

        # 约束范围
        main_tag = soup.find('main').find('div', attrs={'id':'article_content'})
        # 提取标题  
        headings = [heading.get_text(strip=True) for heading in main_tag.find_all(['h2', 'h3'])]

        # 提取正文  
        paragraphs = [paragraph.get_text(strip=True) for paragraph in main_tag.find_all(['ul','p'])]

        # 提取代码块  
        code_blocks = [code_block.get_text(strip=True) for code_block in main_tag.find_all('pre')]

        # 写入文件  
        with open(filename, 'w', encoding='utf-8') as file:
            file.write("Headings:\n")
            for heading in headings:
                file.write(f"- {heading}\n")
            file.write("\nParagraphs:\n")
            for paragraph in paragraphs:
                file.write(f"- {paragraph}\n")
            file.write("\nCode Blocks:\n")
            for code in code_blocks:
                file.write(f"- {code}\n")

    finally:
        # 无论是否发生异常，都关闭浏览器  
        driver.quit()


if __name__ == '__main__':
    fetch_and_save_content_with_selenium("https://blog.csdn.net/qq_44017116/article/details/141275550?spm=1001.2014.3001.5501", "./data/a.txt")
