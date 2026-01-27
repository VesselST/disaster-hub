import json
import os

def process_roads():  
    file_path = "roads_sample.json"
    
    if not os.path.exists(file_path):
        print(f"cannot find floder {file_path}")
        return

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            roads_list = json.load(f)  
        
        print(f"read success {file_path} total  {len(roads_list)} 's raods")
        print("-" * 35)

        area_map = {}          
        for r in roads_list:
            area = r.get('Area', '未知')
            name = r.get('Rd_Name', '未命名')
            if area not in area_map:
                area_map[area] = []
            area_map[area].append(name)

        while True:
            target = input("\nenter the area you want,enter exit exit ").strip()
            
            if target.lower() == 'exit':
                break
            elif target in area_map:
                print(f"  【{target}】 main road: {', '.join(area_map[target])}")
            else:
                print(f"cannot find '{target}'。the databses include:{', '.join(area_map.keys())}")

    except Exception as e:
        print(f"error {e}")

if __name__ == "__main__":
    process_roads()