import flet as ft
from typing import List, Dict
from api.client import api_client


async def rating_page(page: ft.Page):
    """
    Team rating page displaying a list of teams with scores
    """
    
    # Sample team data - будет заменено на данные с API
    teams: List[Dict] = []
    
    async def load_teams():
        """Загружает список команд с API"""
        try:
            result = await api_client.get("/teams/")
            print(f"[DEBUG] Teams loaded: {result}")
            if isinstance(result, list):
                # Сортируем по рейтингу (если есть поле score или rating)
                return sorted(result, key=lambda t: t.get("score", 0) or t.get("rating", 0), reverse=True)
            return []
        except Exception as e:
            print(f"Error loading teams: {e}")
            return []
    
    def on_back_click(e):
        """Handle back button click"""
        page.go("/menu")
    
    # Header with back button
    header = ft.Container(
        content=ft.Row(
            controls=[
                ft.IconButton(
                    icon=ft.Icons.ARROW_BACK,
                    icon_size=24,
                    icon_color="#FFFFFF",
                    on_click=on_back_click,
                ),
                ft.Text(
                    "Рейтинг команд",
                    size=24,
                    weight="w600",
                    color="#FFFFFF",
                    expand=True,
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Container(width=40),  # Spacer for alignment
            ],
            alignment=ft.MainAxisAlignment.START,
        ),
        padding=ft.padding.symmetric(horizontal=16, vertical=12),
    )
    
    # Team card builder
    def create_team_card(team: Dict, index: int) -> ft.Container:
        """Create a styled team card with position, name and stats"""
        team_name = team.get("name", "Unknown Team")
        team_score = team.get("score", team.get("rating", 0))
        
        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.Text(
                        f"#{index + 1}",
                        size=20,
                        weight="w700",
                        color="#FFFFFF",
                        width=50,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Column(
                        controls=[
                            ft.Text(
                                team_name,
                                size=18,
                                weight="w600",
                                color="#FFFFFF",
                            ),
                            ft.Text(
                                f"Очков: {team_score}",
                                size=14,
                                weight="w500",
                                color="#FFD700",
                            ),
                        ],
                        expand=True,
                    ),
                    ft.Icon(
                        name=ft.Icons.EMOJI_EVENTS,
                        color="#FFD700" if index == 0 else ("#C0C0C0" if index == 1 else "#CD7F32"),
                        size=24,
                    ),
                ],
                spacing=12,
            ),
            bgcolor=ft.Colors.with_opacity(0.1, "#FFFFFF"),
            border_radius=16,
            padding=ft.padding.symmetric(vertical=12, horizontal=16),
            margin=ft.margin.symmetric(horizontal=16, vertical=8),
            border=ft.border.all(2, "#FFFFFF" if index < 3 else ft.Colors.TRANSPARENT),
        )
    
    # Team cards list container
    team_cards_column = ft.Column(
        controls=[],
        spacing=0,
    )
    
    # Scrollable content with ListView
    scroll_content = ft.ListView(
        controls=[team_cards_column],
        spacing=0,
        padding=ft.padding.symmetric(horizontal=0, vertical=16),
        expand=True,
    )
    
    # Main content with scroll
    main_content = ft.Column(
        controls=[
            header,
            scroll_content,
        ],
        expand=True,
        spacing=0,
    )
    
    # Main container with gradient background
    main_container = ft.Container(
        content=main_content,
        width=page.window.width,
        height=page.window.height,
        gradient=ft.LinearGradient(
            begin=ft.alignment.top_left,
            end=ft.alignment.bottom_right,
            colors=[
                "#5B4FFF",  # Blue-purple
                "#8B5FFF",  # Purple
                "#E5008C",  # Pink
                "#FF6B9D",  # Light pink
                "#FFB8A0",  # Peach
            ],
            stops=[0.0, 0.25, 0.5, 0.75, 1.0],
        ),
        alignment=ft.alignment.center,
    )
    
    # Load teams on page init
    async def init_page():
        """Initialize page by loading teams"""
        nonlocal teams
        teams = await load_teams()
        
        if teams:
            # Clear and populate team cards
            team_cards_column.controls.clear()
            for i, team in enumerate(teams):
                team_cards_column.controls.append(create_team_card(team, i))
            page.update()
        else:
            team_cards_column.controls.append(
                ft.Text(
                    "Нет данных о командах",
                    size=18,
                    weight="w600",
                    color="#FFFFFF",
                    text_align=ft.TextAlign.CENTER,
                )
            )
            page.update()
    
    # Start loading teams
    page.run_task(init_page)
    
    return main_container