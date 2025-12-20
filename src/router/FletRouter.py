import flet as ft
from pages.login import login_page
from pages.menu import menu_page
from pages.schedule import schedule_page
from pages.razminка import razminка_page
from pages.rating import rating_page
from pages.registration import registration_page

class Router:
    async def init(self, page: ft.Page):
        self.routes = {
            '/login': await login_page(page),
            '/menu': await menu_page(page),
            '/schedule': await schedule_page(page, on_back=lambda: page.go('/menu')),
            '/razminka': await razminка_page(page, on_back=lambda: page.go('/menu')),
            '/rating': await rating_page(page, on_back=lambda: page.go('/menu')),
            '/registration': await registration_page(page, on_back=lambda: page.go('/menu')),
        }
        self.body = ft.Container(expand=True)

    async def route_change(self, route):
        self.body.content = self.routes[route.route]
        self.body.update()