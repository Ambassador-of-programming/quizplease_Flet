import flet as ft
from typing import Callable, List, Dict


async def schedule_page(page: ft.Page, on_back: Callable = None):
    """
    Schedule page displaying a list of quiz events
    """
    
    # Sample event data
    events: List[Dict] = [
        {
            "title": "Название игры",
            "time": "19:00 - 21:00",
            "location": "ул. Пушкина, 10",
            "cost": "500 ₽"
        },
        {
            "title": "Название игры",
            "time": "19:00 - 21:00",
            "location": "ул. Пушкина, 10",
            "cost": "500 ₽"
        },
        {
            "title": "Название игры",
            "time": "19:00 - 21:00",
            "location": "ул. Пушкина, 10",
            "cost": "500 ₽"
        },
    ]
    
    def on_signup_click(event_index: int):
        """Handle sign up button click"""
        def handler(e):
            snackbar.content.value = f"Записались на {events[event_index]['title']}"
            snackbar.open = True
            page.update()
        return handler
    
    def on_back_click(e):
        """Handle back button click"""
        if on_back:
            on_back()
    
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
                    "Расписание",
                    size=24,
                    weight="w600",
                    color="#FFFFFF",
                    expand=True,
                ),
            ],
            alignment=ft.MainAxisAlignment.START,
        ),
        padding=ft.padding.symmetric(horizontal=16, vertical=12),
    )
    
    # Event card builder
    def create_event_card(event: Dict, index: int) -> ft.Container:
        """Create a styled event card"""
        
        # Info item with icon
        def create_info_item(icon: str, label: str, value: str) -> ft.Row:
            return ft.Row(
                controls=[
                    ft.Container(
                        content=ft. Icon(
                            name=icon,
                            size=20,
                            color="#E60189",
                        ),
                        width=40,
                        height=40,
                        alignment=ft.alignment.center,
                    ),
                    ft.Column(
                        controls=[
                            ft.Text(
                                label,
                                size=12,
                                weight="w400",
                                color="#999999",
                            ),
                            ft.Text(
                                value,
                                size=16,
                                weight="w500",
                                color="#000000",
                            ),
                        ],
                        spacing=2,
                    ),
                ],
                spacing=12,
                vertical_alignment=ft.CrossAxisAlignment.START,
            )
        
        return ft.Container(
            content=ft.Column(
                controls=[
                    # Title
                    ft.Container(
                        content=ft. Text(
                            event["title"],
                            size=28,
                            weight="w800",
                            color="#000000",
                            text_align=ft.TextAlign. CENTER,
                        ),
                        padding=ft.padding.symmetric(vertical=12),
                    ),
                    
                    # Divider
                    ft.Divider(height=1, color="#E8E8E8"),
                    
                    # Info items
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                create_info_item(
                                    ft.Icons.LOCATION_ON,
                                    "Место",
                                    event["location"]
                                ),
                                create_info_item(
                                    ft.Icons.SCHEDULE,
                                    "Время",
                                    event["time"]
                                ),
                                create_info_item(
                                    ft.Icons.STAR,
                                    "Стоимость",
                                    event["cost"]
                                ),
                            ],
                            spacing=16,
                        ),
                        padding=ft.padding.symmetric(vertical=16, horizontal=16),
                    ),
                    
                    # Divider
                    ft.Divider(height=1, color="#E8E8E8"),
                    
                    # Sign up button
                    ft.Container(
                        content=ft. Container(
                            content=ft. Text(
                                "Записаться",
                                size=16,
                                weight="w500",
                                color="#FFFFFF",
                                text_align=ft.TextAlign.CENTER,
                            ),
                            gradient=ft.LinearGradient(
                                begin=ft.alignment.center_left,
                                end=ft.alignment.center_right,
                                colors=["#E60189", "#D10283"],
                            ),
                            border_radius=8,
                            padding=ft.padding.symmetric(vertical=12, horizontal=30),
                            alignment=ft.alignment.center,
                            on_click=on_signup_click(index),
                            ink=True,
                        ),
                        alignment=ft.alignment.center,
                        padding=ft.padding.symmetric(vertical=16),
                    ),
                ],
                spacing=0,
            ),
            bgcolor="#FFFFFF",
            border=ft.border.all(width=2, color="#1B75BB"),
            border_radius=16,
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=15,
                color=ft.Colors.with_opacity(0.15, "#000000"),
                offset=ft.Offset(0, 4),
            ),
            width=390,
            padding=0,
        )
    
    # Snackbar for notifications
    snackbar = ft. SnackBar(
        content=ft.Text("", size=14, color="#FFFFFF"),
        bgcolor="#43A047",
        duration=2000,
    )
    page.overlay. append(snackbar)
    
    # Event cards list
    event_cards = [create_event_card(event, i) for i, event in enumerate(events)]
    
    # Scrollable content
    scroll_content = ft.Column(
        controls=event_cards,
        spacing=16,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )
    
    # Main content with scroll
    main_content = ft.Column(
        controls=[
            header,
            ft.Container(
                content=scroll_content,
                expand=True,
                padding=ft.padding.symmetric(horizontal=16, vertical=16),
                clip_behavior=ft.ClipBehavior.HARD_EDGE,
            ),
        ],
        expand=True,
        spacing=0,
    )
    
    # Main container with gradient background
    main_container = ft. Container(
        content=main_content,
        width=page.window. width,
        height=page. window.height,
        gradient=ft.LinearGradient(
            begin=ft.alignment. top_left,
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