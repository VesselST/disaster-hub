import flet as ft
import plotly.graph_objects as go
from flet.plotly_chart import PlotlyChart  

from repositories.shelter_repository import ShelterRepository
from services.map_server import MapService

# ... 前面的 import 不變 ...

def main(page: ft.Page):
    page.title = "Disaster Hub - 內嵌 3D 監控"
    page.theme_mode = ft.ThemeMode.DARK
    
    # 這是右側的顯示區域
    main_content = ft.Column(
        [ft.Text("點擊按鈕載入 3D 地圖")], 
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        expand=True
    )

    def load_3d_map(e):
    # 1. 顯示讀取中
        main_content.controls.clear()
        main_content.controls.append(ft.ProgressRing())
        main_content.controls.append(ft.Text("正在產生 3D 模型...", color="blue"))
        page.update()

    try:
        # --- 測試用最簡化數據 (先確保圖表能顯示) ---
        fig = go.Figure(data=[go.Scatter3d(
            x=[1, 2, 3], 
            y=[4, 5, 6], 
            z=[7, 8, 9], 
            mode='markers',
            marker=dict(size=10, color='red')
        )])
        
        fig.update_layout(
            template="plotly_dark",
            margin=dict(l=0, r=0, b=0, t=0),
            scene=dict(
                xaxis_title='經度',
                yaxis_title='緯度',
                zaxis_title='容量'
            )
        )

        # 2. 準備 PlotlyChart 元件
        # 關鍵：加上明確的 height，有時候 Column 內縮放會導致高度變 0
        chart = PlotlyChart(fig, expand=True)

        # 3. 清除轉圈圈，放入圖表
        main_content.controls.clear()
        main_content.controls.append(chart)
        
    except Exception as ex:
        # 如果出錯，至少要把錯誤印出來
        main_content.controls.clear()
        main_content.controls.append(ft.Text(f"產生失敗: {str(ex)}", color="red"))
    
    # 4. 最後一次更新頁面
    page.update()
    # 佈局
    page.add(
        ft.Row([
            # 左側側邊欄
            # 左側側邊欄
            ft.Container(
                content=ft.Column([
                    ft.Text("監控面板", size=25, weight="bold"),
                    ft.ElevatedButton(
                        "載入/重整 3D 地圖", 
                        icon=ft.icons.REFRESH,  # 之前修正的拼字
                        on_click=load_3d_map    # 確保你的函式名稱與此一致
                    ),
                    ft.Divider(),
                    # 顏色建議直接用字串，如 "green" 或 "green600"
                    ft.Text("數據狀態: 50 筆已同步", color="green"),
                ]),
                width=250,
                padding=20,
                bgcolor="surfacevariant" # 修正這裡，改用字串避開 AttributeError
            ),
            # 右側地圖區
            ft.VerticalDivider(width=1),
            main_content
        ], expand=True)
    )

ft.app(target=main)