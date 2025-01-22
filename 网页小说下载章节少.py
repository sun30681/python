#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import requests
from bs4 import BeautifulSoup
import chardet
import re

# 目标网页URL
url = 'http://www.qiqixs.net/txt/xiazai34211.html'

# 发送HTTP请求并确保使用正确的编码
response = requests.get(url)
detected_encoding = chardet.detect(response.content)['encoding']
if detected_encoding.lower() in ['gb2312', 'gbk']:
    response.encoding = 'gb18030'  # 更全面的GBK兼容编码
else:
    response.encoding = detected_encoding or 'utf-8'  # 自动检测编码

# 检查请求是否成功
if response.status_code == 200:
    # 解析HTML内容，使用html.parser解析器
    soup = BeautifulSoup(response.text, 'html.parser')

    # 获取所有的<a>标签
    links = soup.find_all('a', href=True)

    print('Found links:')

    # 获取小说章节链接
    chapter_links = []
    for link in links:
        href = link['href']
        text = link.get_text(strip=True)
        print(f"Link text: {text}, href: {href}")  # 调试信息

        # 尝试更灵活的匹配规则
        if 'html' in href and ('章' in text or 'chapter' in href.lower()):
            chapter_links.append((href, text))  # 保存链接和章节标题
            print(f"Found chapter link: {href}")  # 调试信息

    if not chapter_links:
        print("No chapter links found.")
    else:
        print(f"Total {len(chapter_links)} chapter links found.")

        # 创建保存章节文件的文件夹
        output_folder = '万相之王_chapters'
        os.makedirs(output_folder, exist_ok=True)

        # 下载每个章节的内容并保存到文件
        chapter_files = []
        for i, (chapter_link, chapter_title) in enumerate(chapter_links):
            # 处理相对路径
            if not chapter_link.startswith('http'):
                chapter_link = f"http://www.qiqixs.net{chapter_link}"
            chapter_url = chapter_link
            print(f"chapter_url: {chapter_url}")
            chapter_response = requests.get(chapter_url)
            detected_chapter_encoding = chardet.detect(chapter_response.content)['encoding']
            if detected_chapter_encoding.lower() in ['gb2312', 'gbk']:
                chapter_response.encoding = 'gb18030'  # 更全面的GBK兼容编码
            else:
                chapter_response.encoding = detected_chapter_encoding or 'utf-8'  # 自动检测编码

            if chapter_response.status_code == 200:
                chapter_soup = BeautifulSoup(chapter_response.text, 'html.parser')

                # 尝试不同的选择器来获取章节内容
                content_div = chapter_soup.find('div', id='content') or chapter_soup.find('div',
                                                                                          class_='content') or chapter_soup.find(
                    'div', class_='read-content')
                if content_div is not None:
                    chapter_content = content_div.get_text(separator='\n\n', strip=True)  # 使用双换行分隔段落
                    if chapter_content:  # 检查章节内容是否为空
                        # 清理章节标题以适合作为文件名
                        sanitized_title = re.sub(r'[\\/*?:"<>|]', '', chapter_title).strip()
                        sanitized_title = sanitized_title.replace('\n', '_').replace('\r', '_')  # 替换换行符等特殊字符
                        chapter_file = os.path.join(output_folder, f"{sanitized_title}.txt")
                        with open(chapter_file, "w", encoding='utf-8') as fo:
                            fo.write(f"{chapter_title}\n\n")  # 写入章节标题
                            fo.write(chapter_content)
                        chapter_files.append(chapter_file)
                        print(
                            f"Downloaded chapter {i + 1}: {chapter_url}, File size: {os.path.getsize(chapter_file)} bytes")
                    else:
                        print(f"Chapter {i + 1} content is empty: {chapter_url}")
                else:
                    print(f"Chapter {i + 1} does not have a content div: {chapter_url}")
                    # 可选：尝试从其他地方获取内容，例如 <p> 标签
                    paragraphs = chapter_soup.find_all('p')
                    chapter_content = '\n\n'.join(p.get_text(strip=True) for p in paragraphs)  # 使用双换行分隔段落
                    if chapter_content:
                        # 清理章节标题以适合作为文件名
                        sanitized_title = re.sub(r'[\\/*?:"<>|]', '', chapter_title).strip()
                        sanitized_title = sanitized_title.replace('\n', '_').replace('\r', '_')  # 替换换行符等特殊字符
                        chapter_file = os.path.join(output_folder, f"{sanitized_title}.txt")
                        with open(chapter_file, "w", encoding='utf-8') as fo:
                            fo.write(f"{chapter_title}\n\n")  # 写入章节标题
                            fo.write(chapter_content)
                        chapter_files.append(chapter_file)
                        print(
                            f"Downloaded chapter {i + 1} using fallback method: {chapter_url}, File size: {os.path.getsize(chapter_file)} bytes")
                    else:
                        print(f"Chapter {i + 1} content could not be found: {chapter_url}")
            else:
                print(f'Failed to retrieve chapter {i + 1}. Status code: {chapter_response.status_code}')

        print(f"All chapters have been downloaded into folder: {output_folder}")
else:
    print(f'Failed to retrieve the page. Status code: {response.status_code}')
