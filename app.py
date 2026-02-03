import flet as ft
import plotly.graph_objects as go
import plotly.offline as pyo
import time

def main(page: ft.Page):
    # --- 1. 頁面基礎設定 ---
    page.title = "Disaster Hub | 3D 穩定版"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 0
    page.bgcolor = "#111111"

    # 主顯示容器
    main_content = ft.Container(
        content=ft.Text("點擊按鈕載入地圖", color=ft.Colors.GREY_700),
        expand=True,
        alignment=ft.alignment.center,
    )

    # --- 2. 核心邏輯：產生 3D 地圖 HTML ---
    def get_3d_html():
        fig = go.Figure(data=[go.Scatter3d(
            x=[1, 2, 3], y=[4, 5, 6], z=[100, 300, 200],
            mode='markers',
            marker=dict(size=10, color='cyan')
        )])

        fig.update_layout(
            template="plotly_dark",
            margin=dict(l=0, r=0, b=0, t=0),
            paper_bgcolor='rgba(0,0,0,0)',
            scene=dict(camera=dict(eye=dict(x=1.5, y=1.5, z=1.5)))
        )
        # 使用 CDN 載入 plotly.js，避開本地環境衝突
        return pyo.plot(fig, include_plotlyjs='cdn', output_type='div')

    # --- 3. 事件處理 ---
    def load_map_action(e):
        main_content.content = ft.ProgressRing(width=40, height=40)
        page.update()
        
        try:
            html_content = get_3d_html()
            # 使用 HtmlView 是目前解決「全黑」與「JS 崩潰」最穩定的招式
            main_content.content = ft.HtmlView(
                html_content, 
                expand=True,
                key=f"map_{time.time()}"
            )
        except Exception as ex:
            main_content.content = ft.Text(f"錯誤: {ex}", color="red")
        
        page.update()

    # --- 4. UI 佈局 (修正所有 Attribute 錯誤) ---
    sidebar = ft.Container(
        content=ft.Column([
            ft.Text("監控面板", size=24, weight="bold"),
            ft.Divider(height=20, color="transparent"),
            ft.ElevatedButton(
                "載入 3D 地圖",
                icon=ft.icons.MAP, # 換成最基本的 MAP 圖示，確保不報錯
                on_click=load_map_action,
                height=50,
            ),
            ft.Text("系統就緒", color="green", size=12),
        ]),
        width=260,
        padding=25,
        bgcolor="#1E1E1E" # 棄用 surfacevariant，直接給顏色值
    )

    page.add(
        ft.Row([
            sidebar,
            ft.VerticalDivider(width=1, color="#333333"),
            main_content
        ], expand=True, spacing=0)
    )

if __name__ == "__main__":
    # 強制 localhost:8501 且使用瀏覽器模式
    ft.app(target=main, view=ft.AppView.WEB_BROWSER, port=8501, host="localhost")