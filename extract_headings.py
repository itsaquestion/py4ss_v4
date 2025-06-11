#!/usr/bin/env python3
"""
从_book目录中递归提取所有HTML文件的1、2、3级标题，并以Markdown格式保存。

该脚本会：
1. 递归遍历_book目录下的所有HTML文件
2. 提取每个文件中有章节编号的h1、h2和h3标题
3. 按章节编号排序后，将提取的标题按Markdown格式保存到文件中
"""

import os
import re
from pathlib import Path
from typing import List, Tuple, Optional
from bs4 import BeautifulSoup


class Heading:
    """表示一个标题的类"""
    
    def __init__(self, level: int, text: str, chapter_number: str, file_path: str):
        self.level = level
        self.text = text
        self.chapter_number = chapter_number
        self.file_path = file_path
    
    def __repr__(self):
        return f"Heading(level={self.level}, chapter_number='{self.chapter_number}', text='{self.text}')"


def parse_chapter_number(chapter_number: str) -> Tuple[List[int], str]:
    """
    解析章节编号，返回用于排序的数字列表和原始字符串。
    
    Args:
        chapter_number: 章节编号字符串，如 "1.2.3" 或 "12"
        
    Returns:
        (数字列表, 原始字符串) 例如: ([1, 2, 3], "1.2.3")
    """
    # 提取所有数字
    numbers = re.findall(r'\d+', chapter_number)
    try:
        return [int(n) for n in numbers], chapter_number
    except ValueError:
        return [999999], chapter_number  # 无法解析的放到最后


def extract_headings_from_html(file_path: str) -> List[Heading]:
    """
    从HTML文件中提取有章节编号的h1、h2和h3标题。
    
    Args:
        file_path: HTML文件的路径
        
    Returns:
        包含Heading对象的列表
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        soup = BeautifulSoup(content, 'html.parser')
        headings = []
        
        # 提取h1, h2, h3标题
        for level in [1, 2, 3]:
            tag_name = f'h{level}'
            for heading_tag in soup.find_all(tag_name):
                # 查找章节编号
                chapter_number = extract_chapter_number(heading_tag)
                
                if chapter_number:  # 只保留有章节编号的标题
                    # 提取纯文本，去除HTML标签和多余空白
                    text = heading_tag.get_text(strip=True)
                    if text:
                        headings.append(Heading(level, text, chapter_number, file_path))
                
        return headings
        
    except Exception as e:
        print(f"处理文件 {file_path} 时出错: {e}")
        return []


def extract_chapter_number(heading_tag) -> Optional[str]:
    """
    从标题标签中提取章节编号。
    
    Args:
        heading_tag: BeautifulSoup标签对象
        
    Returns:
        章节编号字符串，如果没有找到则返回None
    """
    # 方法1：查找 data-number 属性
    chapter_number = heading_tag.get('data-number')
    if chapter_number:
        return chapter_number
    
    # 方法2：查找包含 chapter-number 类的 span
    chapter_span = heading_tag.find('span', class_='chapter-number')
    if chapter_span:
        return chapter_span.get_text(strip=True)
    
    # 方法3：查找包含 header-section-number 类的 span
    section_span = heading_tag.find('span', class_='header-section-number')
    if section_span:
        return section_span.get_text(strip=True)
    
    # 方法4：使用正则表达式在文本中查找章节编号模式
    text = heading_tag.get_text()
    # 匹配开头的数字模式，如 "1 ", "1.2 ", "1.2.3 "
    match = re.match(r'^(\d+(?:\.\d+)*)\s+', text)
    if match:
        return match.group(1)
    
    return None


def find_html_files(directory: str) -> List[str]:
    """
    递归查找目录下所有的HTML文件。
    
    Args:
        directory: 要搜索的目录路径
        
    Returns:
        HTML文件路径列表
    """
    html_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.html'):
                html_files.append(os.path.join(root, file))
    return sorted(html_files)


def sort_headings(headings: List[Heading]) -> List[Heading]:
    """
    按章节编号对标题进行排序。
    
    Args:
        headings: 标题列表
        
    Returns:
        排序后的标题列表
    """
    def sort_key(heading: Heading):
        numbers, _ = parse_chapter_number(heading.chapter_number)
        return numbers
    
    return sorted(headings, key=sort_key)


def generate_markdown_content(headings: List[Heading], base_dir: str) -> str:
    """
    生成Markdown格式的内容。
    
    Args:
        headings: 排序后的标题列表
        base_dir: 基础目录路径，用于生成相对路径
        
    Returns:
        Markdown格式的字符串
    """
    markdown_lines = []
    markdown_lines.append("# 电子讲义标题目录\n")
    markdown_lines.append(f"本文档包含从 `{base_dir}` 目录提取的所有HTML文件的有章节编号的1、2、3级标题。")
    markdown_lines.append("标题按章节编号排序。\n")
    markdown_lines.append("---\n")
    
    current_file = None
    
    for heading in headings:
        # 获取相对于基础目录的路径
        relative_path = os.path.relpath(heading.file_path, base_dir)
        
        # 如果是新文件，添加文件标题
        if relative_path != current_file:
            current_file = relative_path
            markdown_lines.append(f"\n## 📁 文件: {relative_path}\n")
        
        # 添加标题，根据级别使用不同的Markdown格式
        if heading.level == 1:
            markdown_lines.append(f"# {heading.text}")
        elif heading.level == 2:
            markdown_lines.append(f"## {heading.text}")
        elif heading.level == 3:
            markdown_lines.append(f"### {heading.text}")
        
        markdown_lines.append("")  # 添加空行
    
    return "\n".join(markdown_lines)


def main():
    """
    主函数：执行标题提取和Markdown文件生成。
    """
    # 设置目录路径
    book_dir = "_book"
    output_file = "headings_extracted.md"
    
    # 检查_book目录是否存在
    if not os.path.exists(book_dir):
        print(f"错误：目录 '{book_dir}' 不存在！")
        return
    
    print(f"开始扫描 '{book_dir}' 目录...")
    
    # 查找所有HTML文件
    html_files = find_html_files(book_dir)
    
    if not html_files:
        print(f"在 '{book_dir}' 目录中未找到HTML文件！")
        return
    
    print(f"找到 {len(html_files)} 个HTML文件")
    
    # 提取所有标题
    print("正在提取有章节编号的标题...")
    all_headings = []
    
    for html_file in html_files:
        headings = extract_headings_from_html(html_file)
        all_headings.extend(headings)
    
    print(f"提取到 {len(all_headings)} 个有章节编号的标题")
    
    # 按章节编号排序
    print("正在按章节编号排序...")
    sorted_headings = sort_headings(all_headings)
    
    # 生成Markdown内容
    print("正在生成Markdown内容...")
    markdown_content = generate_markdown_content(sorted_headings, book_dir)
    
    # 保存到文件
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        
        print(f"✅ 标题提取完成！结果已保存到 '{output_file}'")
        print(f"📁 处理了 {len(html_files)} 个HTML文件")
        print(f"📑 提取了 {len(sorted_headings)} 个有章节编号的标题")
        
        # 显示一些统计信息
        level_counts = {1: 0, 2: 0, 3: 0}
        for heading in sorted_headings:
            level_counts[heading.level] += 1
        
        print(f"📊 标题统计: H1={level_counts[1]}, H2={level_counts[2]}, H3={level_counts[3]}")
        
    except Exception as e:
        print(f"❌ 保存文件时出错: {e}")


if __name__ == "__main__":
    main()