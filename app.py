import flet as ft
from repositories.shelter_repository import ShelterRepository

def main(page: ft.Page):
    page.title = "Disaster Hub - 東部避難所監控系統"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 20
    
    # 建立 Repository 實例
    repo = ShelterRepository()
    
    # 標題
    header = ft.Text("🌲 東部避難所即時清單", style=ft.TextThemeStyle.HEADLINE_MEDIUM, color=ft.Colors.BLUE_200)

    # 取得資料庫資料
    try:
        shelters = repo.get_all_shelters()
        
        # 建立表格
        data_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("名稱")),
                ft.DataColumn(ft.Text("總容量"), numeric=True),
                ft.DataColumn(ft.Text("目前人數"), numeric=True),
                ft.DataColumn(ft.Text("經緯度")),
            ],
            rows=[
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(s.name)),
                        ft.DataCell(ft.Text(str(s.total_vessel))),
                        ft.DataCell(ft.Text(str(s.total_people))),
                        ft.DataCell(ft.Text(f"{s.lat:.4f}, {s.lon:.4f}")),
                    ]
                ) for s in shelters
            ],
        )

        # 用滾動視窗包裝表格
        list_view = ft.ListView(expand=True, spacing=10, padding=10)
        list_view.controls.append(data_table)

        page.add(
            header,
            ft.Divider(),
            list_view
        )

    except Exception as e:
        page.add(ft.Text(f"資料讀取失敗: {e}", color=ft.Colors.RED))

    page.update()

if __name__ == "__main__":
    ft.app(target=main)