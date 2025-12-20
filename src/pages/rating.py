import flet as ft
from typing import Callable, List, Dict


async def rating_page(page:  ft.Page, on_back:  Callable = None):
    """
    Team rating page displaying a list of teams with scores
    """
    
    # Sample team data
    teams:  List[Dict] = [
        {
            "name": "Название",
            "games": "100 игр",
            "points": "1000 баллов"
        },
        {
            "name": "Название",
            "games": "100 игр",
            "points":  "1000 баллов"
        },
        {
            "name": "Название",
            "games": "100 игр",
            "points": "1000 баллов"
        },
        {
            "name":  "Название",
            "games": "100 игр",
            "points": "1000 баллов"
        },
        {
            "name": "Название",
            "games": "100 игр",
            "points": "1000 баллов"
        },
        {
            "name": "Название",
            "games": "100 игр",
            "points": "1000 баллов"
        },
        {
            "name": "Название",
            "games": "100 игр",
            "points": "1000 баллов"
        },
        {
            "name": "Название",
            "games": "100 игр",
            "points": "1000 баллов"
        },
        {
            "name": "Название",
            "games": "100 игр",
            "points": "1000 баллов"
        },
    ]
    
    def on_back_click(e):
        """Handle back button click"""
        if on_back:
            on_back()
    
    # Header with back button
    header = ft. Container(
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
                    color="#000000",
                    expand=True,
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Container(width=40),  # Spacer for alignment
            ],
            alignment=ft.MainAxisAlignment.START,
        ),
        padding=ft.padding. symmetric(horizontal=16, vertical=12),
    )
    
    # Team card builder
    def create_team_card(team: Dict, index: int) -> ft.Container:
        """Create a styled team card"""
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(
                        team["name"],
                        size=18,
                        weight="w600",
                        color="#000000",
                    ),
                    ft.Text(
                        team["games"],
                        size=14,
                        weight="w500",
                        color="#E60189",
                    ),
                    ft.Text(
                        team["points"],
                        size=14,
                        weight="w500",
                        color="#E60189",
                    ),
                ],
                spacing=4,
            ),
            bgcolor="#FFFFFF",
            border_radius=16,
            padding=ft.padding.symmetric(vertical=16, horizontal=16),
            margin=ft.margin.symmetric(horizontal=16, vertical=8),
        )
    
    # Team cards list
    team_cards = [create_team_card(team, i) for i, team in enumerate(teams)]
    
    # Scrollable content with ListView
    scroll_content = ft.ListView(
        controls=team_cards,
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
    
    return main_container