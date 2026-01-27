import flet as ft
from repositories.shelter_repository import ShelterRepository

# SOLID: 抽離卡片，但使用最基礎的語法
class ShelterCard(ft.Container):
    def __init__(self, shelter):
        super().__init__()
        remaining = shelter.capacity - shelter.current_ppl
        is_full = remaining <= 0
        
        # 避開 ft.icons，直接用字串
        icon_name = "home" if "活動中心" in shelter.name else "school"
        
        self.content = ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.ListTile(
                        leading=ft.Icon(name=icon_name, color="blue"),
                        title=ft.Text(shelter.name, weight="bold"),
                        subtitle=ft.Text(f"座標: {shelter.lat}, {shelter.lon}", size=12),
                    ),
                    ft.Container(
                        padding=10,
                        content=ft.Row([
                            ft.Text(f"總量: {shelter.capacity}"),
                            ft.Text(
                                "已滿" if is_full else f"剩餘: {remaining}",
                                color="red" if is_full else "green",
                                weight="bold"
                            )
                        ], alignment="spaceBetween") # 這裡也改用字串
                    )
                ], spacing=0),
                width=300, # 強制固定寬度，解決文字垂直縮排
                padding=10
            )
        )

def main(page: ft.Page):
    page.title = "災難避難所"
    page.scroll = "auto" # 解決大片灰色塊，改用字串設定
    page.theme_mode = "light"

    repo = ShelterRepository()
    all_shelters = repo.get_all_shelters()

    # 使用最基本的 Column 和 Row，GridView 有時候也會造成灰色區塊
    grid = ft.Row(wrap=True, spacing=20, run_spacing=20)

    for s in all_shelters:
        grid.controls.append(ShelterCard(s))

    page.add(
        ft.Text("🏢 避難所即時資訊", size=30, weight="bold"),
        ft.Divider(),
        grid
    )

if __name__ == "__main__":
    # 最後的保險：如果不指定顏色屬性，它就沒理由噴 'Colors' 錯誤
    ft.app(target=main, view="web_browser", host="0.0.0.0", port=8501)