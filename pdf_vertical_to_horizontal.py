#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
PDF 縱書（たて書き）轉橫書（よこ書き）並轉換為 Markdown
使用方式: python pdf_vertical_to_horizontal.py [PDF檔案路徑]

功能:
1. 讀取 PDF 檔案
2. 將縱書文字轉換為橫書文字
3. 在原資料夾生成 Markdown 檔案

依賴: pymupdf (pip install pymupdf)
"""

import sys
import os
import pymupdf


def convert_pdf_to_markdown(pdf_path: str) -> str:
    """
    將 PDF 檔案從縱書轉換為橫書，並生成 Markdown 檔案。
    
    Args:
        pdf_path: PDF 檔案的完整路徑
        
    Returns:
        生成的 Markdown 檔案路徑
    """
    # 檢查檔案是否存在
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"找不到檔案: {pdf_path}")
    
    # 檢查副檔名
    if not pdf_path.lower().endswith('.pdf'):
        raise ValueError("請提供 PDF 檔案路徑")
    
    # 獲取原檔案的目錄和檔名
    original_dir = os.path.dirname(os.path.abspath(pdf_path))
    original_name = os.path.splitext(os.path.basename(pdf_path))[0]
    
    # 生成 Markdown 檔案路徑（在原資料夾）
    markdown_path = os.path.join(original_dir, f"{original_name}.md")
    
    print(f"讀取 PDF: {pdf_path}")
    
    # 讀取 PDF
    doc = pymupdf.open(pdf_path)
    total_pages = len(doc)
    print(f"總頁數: {total_pages}")
    
    # 準備 Markdown 內容
    markdown_lines = []
    
    # 提取 PDF 標題（從第一頁獲取）
    title = extract_title(doc)
    if title:
        markdown_lines.append(f"# {title}")
        markdown_lines.append("")
    
    print("開始轉換文字...")
    
    # 逐頁處理
    for page_num in range(total_pages):
        page = doc[page_num]
        blocks = page.get_text('blocks')
        
        # 收集所有文字區塊
        col_data = []
        for block in blocks:
            x0, y0, x1, y1, text, block_no, block_type = block
            if text.strip():
                # 計算區塊的 X 中心位置
                cx = (x0 + x1) / 2
                col_data.append((cx, text.strip()))
        
        # 從右到左排序（日文縱書閱讀順序）
        col_data.sort(key=lambda x: x[0], reverse=True)
        
        # 將每列的縱書文字轉換為橫書（移除換行符號）
        for cx, text in col_data:
            horizontal_text = text.replace('\n', '')
            if horizontal_text.strip():
                markdown_lines.append(horizontal_text)
        
        # 每頁之間加分隔線
        markdown_lines.append("---")
        markdown_lines.append("")
    
    # 關閉 PDF
    doc.close()
    
    # 寫入 Markdown 檔案
    print(f"寫入 Markdown: {markdown_path}")
    with open(markdown_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(markdown_lines))
    
    # 獲取檔案大小
    file_size = os.path.getsize(markdown_path)
    file_size_mb = file_size / (1024 * 1024)
    
    print(f"\n轉換完成！")
    print(f"輸出檔案: {markdown_path}")
    print(f"檔案大小: {file_size_mb:.2f} MB")
    print(f"總頁數: {total_pages}")
    
    return markdown_path


def extract_title(doc: pymupdf.Document) -> str:
    """
    從 PDF 第一頁提取標題。
    
    Args:
        doc: pymupdf Document 物件
        
    Returns:
        標題文字，若無法提取則返回空字串
    """
    if len(doc) == 0:
        return ""
    
    page = doc[0]
    blocks = page.get_text('blocks')
    
    # 收集所有文字區塊
    col_data = []
    for block in blocks:
        x0, y0, x1, y1, text, block_no, block_type = block
        if text.strip():
            cx = (x0 + x1) / 2
            col_data.append((cx, text.strip()))
    
    # 從右到左排序
    col_data.sort(key=lambda x: x[0], reverse=True)
    
    # 提取前幾列的文字作為標題
    title_parts = []
    for cx, text in col_data[:10]:
        horizontal_text = text.replace('\n', '')
        if horizontal_text.strip():
            title_parts.append(horizontal_text)
    
    # 組合標題
    if title_parts:
        title = ' '.join(title_parts[:3])
        # 限制標題長度
        if len(title) > 100:
            title = title[:100] + "..."
        return title
    
    return ""


def main():
    """主程式入口"""
    if len(sys.argv) < 2:
        print("PDF 縱書（たて書き）轉橫書（よこ書き）並轉換為 Markdown")
        print("")
        print("使用方式:")
        print("  python pdf_vertical_to_horizontal.py [PDF檔案路徑]")
        print("")
        print("範例:")
        print('  python pdf_vertical_to_horizontal.py "C:\\Users\\Downloads\\sample.pdf"')
        print("")
        print("注意:")
        print("  - 需要安裝 pymupdf: pip install pymupdf")
        print("  - Markdown 檔案將生成在原 PDF 所在的資料夾")
        sys.exit(1)
    
    # 獲取 PDF 檔案路徑
    pdf_path = sys.argv[1]
    
    try:
        # 執行轉換
        convert_pdf_to_markdown(pdf_path)
    except FileNotFoundError as e:
        print(f"錯誤: {e}")
        sys.exit(1)
    except ValueError as e:
        print(f"錯誤: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"發生未知錯誤: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
