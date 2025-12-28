import flet as ft
from pages.login import login_page
from pages.menu import menu_page
from pages.schedule import schedule_page
from pages.razminка import razminка_page
from pages.rating import rating_page
from pages.registration import registration_page
from pages.app_registration import app_registration_page

class Router:
    def __init__(self, page: ft.Page):
            self.page = page
            self.routes = {
                '/login':  login_page,
                '/menu':  menu_page,
                '/schedule':  schedule_page,
                '/warmup':  razminка_page,
                '/rating':  rating_page,
                '/app_registration':  app_registration_page,
                '/team_registration':  registration_page,
                }
            self.current_route = None
            
    async def route_change(self, route):
        await self.remove_current_route()

        route_name = route.route
        if route_name in self.routes:
            if self.routes[route_name]:
                new_page = await self.routes[route_name](self.page)
                self.current_route = new_page
                self.page.add(new_page)
            else:
                self.page.go("/menu")
        else:
            self.page.go("/menu")


    async def remove_current_route(self):
        if self.current_route:
            # Вызываем метод очистки, если он существует
            if hasattr(self.current_route, 'cleanup') and callable(self.current_route.cleanup):
                await self.current_route.cleanup()
            self.page.remove(self.current_route)
            self.current_route = None