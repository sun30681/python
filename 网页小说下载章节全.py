#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import requests
from bs4 import BeautifulSoup
import chardet
import re
from urllib.parse import urljoin

# 目标网页URL
base_url = 'http://www.qiqixs.net/34211/'
filename='万相之王全.txt'
output_folder = '万相之王全_chapters'
# 发送HTTP请求并确保使用正确的编码
try:
    response = requests.get(base_url)
    response.raise_for_status()  # 检查请求是否成功
    detected_encoding = chardet.detect(response.content)['encoding']
    if detected_encoding.lower() in ['gb2312', 'gbk']:
        response.encoding = 'gb18030'  # 更全面的GBK兼容编码
    else:
        response.encoding = detected_encoding or 'utf-8'  # 自动检测编码

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
            # 使用 urljoin 处理相对路径和绝对路径
            chapter_link = urljoin(base_url, href)
            chapter_links.append((chapter_link, text))  # 保存链接和章节标题
            print(f"Found chapter link: {chapter_link}")  # 调试信息

    if not chapter_links:
        print("No chapter links found.")
    else:
        print(f"Total {len(chapter_links)} chapter links found.")

        # 创建保存章节文件的文件夹

        os.makedirs(output_folder, exist_ok=True)

        # 创建一个文件来保存所有章节的内容
        output_file = os.path.join(output_folder, filename)

        with open(output_file, "w", encoding='utf-8') as fo:
            for i, (chapter_link, chapter_title) in enumerate(chapter_links):
                print(f"chapter_url: {chapter_link}")
                try:
                    chapter_response = requests.get(chapter_link)
                    chapter_response.raise_for_status()  # 检查请求是否成功
                    detected_chapter_encoding = chardet.detect(chapter_response.content)['encoding']
                    if detected_chapter_encoding.lower() in ['gb2312', 'gbk']:
                        chapter_response.encoding = 'gb18030'  # 更全面的GBK兼容编码
                    else:
                        chapter_response.encoding = detected_chapter_encoding or 'utf-8'  # 自动检测编码

                    chapter_soup = BeautifulSoup(chapter_response.text, 'html.parser')

                    # 尝试不同的选择器来获取章节内容
                    content_div = chapter_soup.find('div', id='content') or chapter_soup.find('div',
                                                                                          class_='content') or chapter_soup.find(
                        'div', class_='read-content')
                    if content_div is not None:
                        chapter_content = content_div.get_text(separator='\n\n', strip=True)  # 使用双换行分隔段落
                    else:
                        # 可选：尝试从其他地方获取内容，例如 <p> 标签
                        paragraphs = chapter_soup.find_all('p')
                        chapter_content = '\n\n'.join(p.get_text(strip=True) for p in paragraphs)  # 使用双换行分隔段落

                    if chapter_content:  # 检查章节内容是否为空
                        # 写入章节标题
                        fo.write(f"{chapter_title}\n\n")
                        # 写入章节内容
                        fo.write(f"{chapter_content}\n\n")
                        # 写入章节分隔线
                        fo.write("=" * 80 + "\n\n")
                        print(
                            f"Downloaded chapter {i + 1}: {chapter_link}, File size: {os.path.getsize(output_file)} bytes")
                    else:
                        print(f"Chapter {i + 1} content could not be found: {chapter_link}")
                except requests.exceptions.RequestException as e:
                    print(f"Failed to retrieve chapter {i + 1}. Error: {e}")
                except Exception as e:
                    print(f"An unexpected error occurred while processing chapter {i + 1}: {e}")

        print(f'All chapters have been downloaded into file: {output_file}')
except requests.exceptions.RequestException as e:
    print(f"An error occurred while fetching the URL: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
