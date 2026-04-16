#!/usr/bin/env python3
import sys
import subprocess

# 尝试导入requests，如果失败则安装
try:
    import requests
    print("✅ requests模块已安装")
except ImportError:
    print("❌ requests模块未安装，尝试安装...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
        import requests
        print("✅ requests模块安装成功")
    except Exception as e:
        print(f"❌ 安装失败: {e}")
        sys.exit(1)

# 测试Discogs API
token = 'SPNqBXXqaxguKEtomolGIDuAKNinRnqrJFImObIe'
headers = {'Authorization': f'Discogs token={token}', 'User-Agent': 'TestBot/1.0'}

params = {
    'q': '',
    'type': 'release',
    'style': 'House',
    'sort': 'date_changed',
    'order': 'desc',
    'per_page': 1,
    'page': 1
}

print("\n🔍 测试Discogs API连接...")
try:
    response = requests.get('https://api.discogs.com/database/search', params=params, headers=headers, timeout=30)
    
    if response.status_code == 200:
        data = response.json()
        if data.get('results') and len(data['results']) > 0:
            result = data['results'][0]
            print('✅ API测试成功！')
            print(f'   标题: {result.get("title", "未知")}')
            print(f'   艺术家: {result.get("artist", "未知")}')
            print(f'   年份: {result.get("year", "未知")}')
            print(f'   风格: {", ".join(result.get("style", ["未知"]))}')
            print(f'   ID: {result.get("id", "未知")}')
            print(f'   链接: https://www.discogs.com/release/{result.get("id")}')
            
            # 测试详细信息
            print("\n🔍 测试详细信息获取...")
            release_id = result.get('id')
            if release_id:
                detail_response = requests.get(f'https://api.discogs.com/releases/{release_id}', headers=headers, timeout=30)
                if detail_response.status_code == 200:
                    detail_data = detail_response.json()
                    print(f'✅ 详细信息获取成功')
                    print(f'   发行标题: {detail_data.get("title", "未知")}')
                    print(f'   艺术家: {", ".join([a.get("name", "") for a in detail_data.get("artists", [])])}')
                    print(f'   曲目数量: {len(detail_data.get("tracklist", []))}')
                else:
                    print(f'⚠️ 详细信息获取失败: {detail_response.status_code}')
        else:
            print('❌ 未找到结果')
    else:
        print(f'❌ API请求失败: {response.status_code}')
        print(f'   响应: {response.text[:200]}...')
        
except Exception as e:
    print(f'❌ 测试过程中发生错误: {str(e)}')