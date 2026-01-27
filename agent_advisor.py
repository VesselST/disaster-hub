# 💡 這部分之後會整合 OpenAI 或 Google Gemini API
def generate_ai_advice(shelter_name, area, distance):
    # 模擬 Agent 的大腦邏輯
    prompt = f"""
    [災害應變中心指令]
    目前偵測到使用者位於 {area} 附近。
    最近的安全避難所是：{shelter_name}。
    直線距離大約：{distance:.1f} 公尺。
    
    請以專業災防指揮官的口吻，給予使用者一段簡短、溫暖且具體的行動建議。
    """
    
    # 這裡我們先用 Print 模擬 AI 的回覆
    print("\n--- AI 災防指揮官建議 ---")
    print(f"「您好，偵測到您目前靠近 {area} 受災區域。別擔心，請立即前往【{shelter_name}】。")
    print(f"該中心目前運作正常，距離您僅約 {distance:.1f} 公尺。")
    print("沿途請避開可能倒塌的圍牆，注意安全，我們在避難所見！」")