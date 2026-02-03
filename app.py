import flet as ft
from repositories.shelter_repository import ShelterRepository

def main(page: ft.Page):
    page.title = "Disaster Hub"
    page.theme_mode = ft.ThemeMode.DARK
    page.scroll = ft.ScrollMode.ADAPTIVE  
    
    repo = ShelterRepository()
    
    # 標題
    header = ft.Text(
        " 東部避難所監控系統", 
        size=30, 
        weight=ft.FontWeight.BOLD, 
        color=ft.Colors.BLUE_200
    )

    # 取得資料
    try:
        shelters = repo.get_all_shelters()
        
        # 建立展示卡片清單
        shelter_list = ft.Column(spacing=10)
        
        for s in shelters:
            # 根據地區給予不同顏色標籤
            region_color = ft.Colors.ORANGE_400 if "[YILAN]" in s.name else ft.Colors.BLUE_400
            
            card = ft.Card(
                content=ft.Container(
                    padding=15,
                    content=ft.Column([
                        ft.ListTile(
                            leading=ft.Icon(ft.Icons.ROOFING, color=region_color),
                            title=ft.Text(s.name, weight=ft.FontWeight.BOLD),
                            subtitle=ft.Text(f"座標: {s.lat}, {s.lon}"),
                        ),
                        ft.Row([
                            ft.Text(f" 總容量: {s.total_vessel}", color=ft.Colors.GREY_400),
                            ft.VerticalDivider(),
                            ft.Text(f" 目前人數: {s.total_people}", 
                                   color=ft.Colors.RED_400 if s.total_people > 0 else ft.Colors.GREEN_400),
                        ], alignment=ft.MainAxisAlignment.START)
                    ])
                )
            )
            shelter_list.controls.append(card)

        # 把標題和清單加到頁面
        page.add(
            header,
            ft.Text(f"目前共計: {len(shelters)} 筆資料", color=ft.Colors.GREY_500),
            ft.Divider(),
            shelter_list
        )

    except Exception as e:
        page.add(ft.Text(f"發生錯誤: {e}", color="red"))

    page.update()

if __name__ == "__main__":
    ft.app(target=main)