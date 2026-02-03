import flet as ft
import plotly.graph_objects as go
from repositories.shelter_repository import ShelterRepository
from services.map_server import MapService

def main(page: ft.Page):
    page.title = "Disaster Hub - 3D 視覺化"
    page.theme_mode = ft.ThemeMode.DARK
    
    repo = ShelterRepository()
    map_service = MapService()

    def handle_show_3d(e):
        # 1. 抓取資料庫資料
        shelters = repo.get_all_shelters()
        # 2. 透過測試過的 Service 轉換資料
        data = map_service.prepare_3d_data(shelters)
        
        # 3. 準備 Plotly 3D 繪圖數據
        lons = [d['lon'] for d in data]
        lats = [d['lat'] for d in data]
        heights = [d['z'] for d in data] # Z 軸為容量
        names = [f"{d['name']}<br>人數: {d['ppl']}" for d in data]

        fig = go.Figure(data=[go.Scatter3d(
            x=lons,
            y=lats,
            z=heights,
            mode='markers',
            marker=dict(
                size=8,
                color=heights,                # 顏色根據容量變化
                colorscale='Portland',        # 暖色調
                opacity=0.9,
                colorbar=dict(title="容量")
            ),
            hovertext=names,
            hoverinfo='text'
        )])

        # 設定 3D 座標軸標籤
        fig.update_layout(
            title="東部避難所 3D 空間分佈 (高度 = 容納量)",
            scene=dict(
                xaxis_title='經度 (Lon)',
                yaxis_title='緯度 (Lat)',
                zaxis_title='容納量 (Capacity)'
            ),
            margin=dict(l=0, r=0, b=0, t=40)
        )
        
        fig.show() # 這會彈出瀏覽器顯示互動圖表

    # Flet 介面配置
    page.add(
        ft.Container(
            padding=30,
            content=ft.Column([
                ft.Text("🛡️ 災難應變 3D 監控系統", size=32, weight="bold"),
                ft.Text("目前已載入宜蘭、花蓮、台東共 50 處避難所資料", color=ft.Colors.GREY_400),
                ft.Divider(height=20),
                ft.ElevatedButton(
                    "開啟 3D 互動圖表", 
                    icon=ft.Icons.THREED_ROTATION,
                    on_click=handle_show_3d,
                    style=ft.ButtonStyle(padding=20)
                ),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        )
    )

if __name__ == "__main__":
    ft.app(target=main)