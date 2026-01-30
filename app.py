import flet as ft
from repositories.shelter_repository import ShelterRepository

#flet物件語法
class ShelterCard(ft.Container):
    def __init__(self, shelter):
        super().__init__()
        remaining = shelter.capacity - shelter.current_ppl
        is_full = remaining <= 0
         
        icon_name = "home" if "activity center" in shelter.name else "school"
        
        self.content = ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.ListTile(
                        leading=ft.Icon(name=icon_name, color="blue"),
                        title=ft.Text(shelter.name, weight="bold"),
                        subtitle=ft.Text(f"local: {shelter.lat}, {shelter.lon}", size=12),
                    ),
                    ft.Container(
                        padding=10,
                        content=ft.Row([
                            ft.Text(f"Toatl: {shelter.capacity}"),
                            ft.Text(
                                "already full" if is_full else f"Else: {remaining}",
                                color="red" if is_full else "green",
                                weight="bold"
                            )
                        ], alignment="spaceBetween")
                    )
                ], spacing=0),
                width=300, 
                padding=10
            )
        )

def main(page: ft.Page):
    page.title = "災害預測模擬系統"
    page.scroll = "auto"
    page.theme_mode = "light"

    repo = ShelterRepository()
    all_shelters = repo.get_all_shelters()

    grid = ft.Row(wrap=True, spacing=20, run_spacing=20)

    for s in all_shelters:
        grid.controls.append(ShelterCard(s))

    page.add(
        ft.Text("避難所即時資訊", size=30, weight="bold"),
        ft.Divider(),
        grid
    )

if __name__ == "__main__":
    ft.app(target=main, view="web_browser", host="0.0.0.0", port=8501)