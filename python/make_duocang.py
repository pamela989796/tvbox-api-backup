import json
import os

# 定义你的 Cloudflare 专属域名（如果绑定了独立域名也可以填独立域名）
# 脚本会自动把这个变量拼接到多仓文件的首位
CF_DOMAIN = "https://tvbox-api.hhmm.kdns.fr" 

def generate_duocang():
    list_path = 'list.txt'
    output_path = 'duocang.json'
    
    # 基础聚合仓结构（先把项目最硬核的三个大聚合接口塞进去）
    urls_list = [
        {"name": "🔥 海量点播 自动去重聚合", "url": f"{CF_DOMAIN}/tvbox/海量点播聚合接口.json"},
        {"name": "📺 海量直播 5层穿透聚合", "url": f"{CF_DOMAIN}/tvbox/海量直播聚合接口.json"},
        {"name": "🐍 海量Py爬虫 聚合接口", "url": f"{CF_DOMAIN}/tvbox/海量py聚合接口.json"}
    ]
    
    # 读取 B 脚本生成的 list.txt，把 90+ 条独立线路也追加进多仓
    if os.path.exists(list_path):
        with open(list_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                # list.txt 格式通常为：接口名称,相对路径或URL
                if ',' in line:
                    parts = line.split(',', 1)
                    name = parts[0].strip()
                    url_part = parts[1].strip()
                    
                    # 如果是相对路径，拼上你的 Cloudflare 域名
                    if not url_part.startswith('http'):
                        final_url = f"{CF_DOMAIN}/{url_part}"
                    else:
                        final_url = url_part
                        
                    urls_list.append({"name": f"⭐ {name} 独立单线", "url": final_url})
                    
    # 构建影视仓标准多仓 JSON 格式
    duocang_data = {"urls": urls_list}
    
    # 落盘输出
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(duocang_data, f, ensure_ascii=False, indent=2)
    print("🎉 多仓自动组装完成！")

if __name__ == "__main__":
    generate_duocang()
