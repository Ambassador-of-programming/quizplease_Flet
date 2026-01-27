import flet as ft
from router.flet_router import routers


async def main(page: ft.Page):
    page.title = 'Quizoboynya: Battle'
    page.theme_mode = "light"
    page.scroll = None
    page.padding = 0
    page.bgcolor = ft.Colors.TRANSPARENT
    page.platform = ft.PagePlatform.ANDROID
    page.window.height = 956
    page.window.width = 440
    page.adaptive = True
    myRouter = routers(page)
    page.on_route_change = myRouter.route_change
    page.go('/login')

if __name__ == "__main__":
    ft.app(
        target=main,
        assets_dir="assets",
    )

