import flet as ft
from router.FletRouter import Router


async def main(page: ft.Page):
    page.title = 'QUiz: Battle'
    page.theme_mode = "light"
    page.scroll = 'HIDDEN'
    page.padding = 0
    page.bgcolor = ft.Colors.TRANSPARENT
    page.platform = ft.PagePlatform.ANDROID
    page.window.width = 440
    page.window.height = 956
    page.adaptive = True
    myRouter = Router(page)
    page.on_route_change = myRouter.route_change
    await page.push_route('/app_registration')


if __name__ == "__main__":
    ft.run(
        main=main,
        assets_dir="assets",
    )

