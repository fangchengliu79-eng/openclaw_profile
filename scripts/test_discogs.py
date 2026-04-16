#!/usr/bin/env python3
"""
测试Discogs搜索功能
"""

import sys
import os

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from discogs_house_search import DiscogsHouseSearch

def test_search():
    """测试搜索功能"""
    print("🧪 测试Discogs搜索功能...")
    
    searcher = DiscogsHouseSearch()
    
    # 测试搜索
    print("1. 测试API搜索...")
    track_info = searcher.search_top_house_track()
    
    if track_info:
        print(f"✅ 搜索成功！")
        print(f"   标题: {track_info['title']}")
        print(f"   艺术家: {track_info['artist']}")
        print(f"   年份: {track_info['year']}")
        print(f"   风格: {track_info['style']}")
        print(f"   链接: {track_info['url']}")
        
        # 测试详细信息获取
        print("\n2. 测试详细信息获取...")
        if track_info['id']:
            details = searcher.get_release_details(track_info['id'])
            if details:
                print(f"✅ 详细信息获取成功")
                print(f"   发行ID: {details.get('id')}")
                print(f"   曲目数量: {len(details.get('tracklist', []))}")
            else:
                print("⚠️ 详细信息获取失败（可能API限制）")
        
        # 测试邮件内容生成
        print("\n3. 测试邮件内容生成...")
        email_content = searcher.generate_email_content(track_info)
        print(f"✅ 邮件内容生成成功")
        print(f"   内容长度: {len(email_content)} 字符")
        
        return True
    else:
        print("❌ 搜索失败")
        return False

if __name__ == "__main__":
    test_search()