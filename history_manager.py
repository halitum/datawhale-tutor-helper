import json
import os

file_path = "./history_list.json"

def add_to_json(key, value=None):
    # 读取现有的 JSON 数据
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    # 添加新的键值对到 JSON 数据中
    data[key] = value
    
    # 将更新后的数据写回文件
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
        
def read_from_json():    
    # 读取 JSON 数据
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    return data