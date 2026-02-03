import flet as ft
import plotly.graph_objects as go
import plotly.offline as pyo
import time

def main(page: ft.Page):
    page.title = "避難所即時資訊中心"
    page.theme_mode = ft.ThemeMode.LIGHT # 配合你截圖的淺色風格
    page.padding = 20

    # --- 1. 真實數據源 (來自你截圖中的資訊) ---
    shelters = [
        {"name": "花蓮縣立體育館", "lat": 23.9961, "lon": 121.5952, "total": 1500, "remain": 1500},
        {"name": "花蓮市中正體育館", "lat": 23.9782, "lon": 121.6115, "total": 600, "remain": 600},
        {"name": "花蓮市立圖書館", "lat": 23.9925, "lon": 121.6035, "total": 150, "remain": 150},
        {"name": "國風國中", "lat": 23.9745, "lon": 121.6015, "total": 300, "remain": 300},
        {"name": "自強國中", "lat": 23.9875, "lon": 121.5892, "total": 450, "remain": 450},
    ]

    # --- 2. 建立 UI 元件 ---
    # 右側 3D 監控區
    map_view = ft.Container(
        content=ft.Text("點擊避難所進行 3D 定位", color="grey"),
        expand=2,
        border=ft.border.all(1, ft.Colors.GREY_300),
        border_radius=10,
    )

    # --- 3. 3D 渲染邏輯 (新東西：數據與視角聯動) ---
    def render_3d_shelter(shelter=None):
        # 如果有選定特定避難所，則聚焦該點
        target_lat = shelter["lat"] if shelter else 23.98
        target_lon = shelter["lon"] if shelter else 121.60

        fig = go.Figure(data=[go.Scatter3d(
            x=[s["lon"] for s in shelters],
            y=[s["lat"] for s in shelters],
            z=[s["total"] for s in shelters],
            mode='markers+text',
            text=[s["name"] for s in shelters],
            marker=dict(
                size=10,
                color=[s["remain"] for s in shelters],
                colorscale='Viridis',
                showscale=True
            )
        )])

        fig.update_layout(
            scene=dict(
                xaxis_title="經度", yaxis_title="緯度", zaxis_title="容量",
                camera=dict(eye=dict(x=1.2, y=1.2, z=1.2), center=dict(x=0, y=0, z=0))
            ),
            margin=dict(l=0, r=0, b=0, t=0),
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        html_div = pyo.plot(fig, include_plotlyjs='cdn', output_type='div')
        map_view.content = ft.HtmlView(html_div, expand=True, key=str(time.time()))
        page.update()

    # --- 4. 建立左側列表 (這就是你截圖中的卡片進化版) ---
    def create_card(s):
        return ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.ListTile(
                        leading=ft.Icon(ft.icons.SCHOOL, color="blue"),
                        title=ft.Text(s["name"], weight="bold"),
                        subtitle=ft.Text(f"座標: {s['lat']}, {s['lon']}"),
                    ),
                    ft.Row([
                        ft.Text(f"總量: {s['total']}"),
                        ft.Text(f"剩餘: {s['remain']}", color="green", weight="bold"),
                    ], alignment=ft.MainAxisAlignment.SPACE_AROUND),
                    ft.TextButton("3D 定位監控", on_click=lambda _: render_3d_shelter(s))
                ], spacing=10),
                padding=10,
            )
        )

    shelter_list = ft.Column(
        [create_card(s) for s in shelters],
        scroll=ft.ScrollMode.ALWAYS,
        expand=1
    )

    # --- 5. 組合畫面 ---
    page.add(
        ft.Row([
            ft.Column([
                ft.Row([ft.Icon(ft.icons.APARTMENT), ft.Text("避難所清單", size=20, weight="bold")]),
                shelter_list
            ], expand=1),
            ft.VerticalDivider(width=1),
            ft.Column([
                ft.Row([ft.Icon(ft.icons.LANGUAGE), ft.Text("3D 空間分布與容量分析", size=20, weight="bold")]),
                map_view
            ], expand=2)
        ], expand=True)
    )

    # 初始載入全域圖
    render_3d_shelter()

if __name__ == "__main__":
    ft.app(target=main, view=ft.AppView.WEB_BROWSER, port=8501)