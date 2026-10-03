import json
import os
import urllib.parse

# 1. 定义你的 Cloudflare 专属域名（尾部不要加斜杠）
CF_DOMAIN = "https://tvbox-api.hhmm.kdns.fr" 

def generate_duocang():
    list_path = 'list.txt'
    output_path = 'duocang.json'
    
    # 对中文文件名进行标准的 URL 编码，防止影视仓识别中文路径报错
    url_db = urllib.parse.quote("tvbox/海量点播聚合接口.json")
    url_zb = urllib.parse.quote("tvbox/海量直播聚合接口.json")
    url_py = urllib.parse.quote("tvbox/海量py聚合接口.json")

    # 基础核心聚合仓
    urls_list = [
        {"name": "🔥 海量点播 自动去重聚合", "url": f"{CF_DOMAIN}/{url_db}"},
        {"name": "📺 海量直播 5层穿透聚合", "url": f"{CF_DOMAIN}/{url_zb}"},
        {"name": "🐍 海量Py爬虫 聚合接口", "url": f"{CF_DOMAIN}/{url_py}"}
    ]
    
    # 2. 自动读取 list.txt，追加其他 90+ 条独立线路
    if os.path.exists(list_path):
        with open(list_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                if ',' in line:
                    parts = line.split(',', 1)
                    name = parts[0].strip()
                    url_part = parts[1].strip()
                    
                    # 补全相对路径
                    if not url_part.startswith('http'):
                        # 对含中文的文件路径进行安全编码
                        safe_url_part = urllib.parse.quote(url_part)
                        final_url = f"{CF_DOMAIN}/{safe_url_part}"
                    else:
                        final_url = url_part
                        
                    urls_list.append({"name": f"⭐ {name} 独立单线", "url": final_url})
                    
    # 构建多仓规范格式
    duocang_data = {"urls": urls_list}
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(duocang_data, f, ensure_ascii=False, indent=2)
    print("🎉 影视仓安全多仓配置文件组装成功！")

if __name__ == "__main__":
    generate_duocang()
