import flet as ft
from typing import Callable


async def menu_page(page: ft.Page):
    """
    Main menu page with gradient background and КВИЗО БОЙНЯ options
    """
    
    def on_schedule_click(e):
        """Handle schedule button click"""
        page.go("/schedule")
    
    def on_warmup_click(e):
        """Handle warm-up button click"""
        page.go("/warmup")
    
    def on_play_click(e):
        """Handle play button click"""
        page.go("/play")
        
    
    def on_rating_click(e):
        """Handle team rating button click"""
        page.go("/rating")
        
    
    # Logo container
    logo_container = ft. Container(
        content=ft.Column(
            controls=[
                ft.Container(
                    content=ft. Column(
                        controls=[
                            ft.Image(
                                src="src/photo/login.png",
                                width=190,
                                height=127,
                                fit=ft. ImageFit.CONTAIN,
                            ),
                        ],
                        spacing=5,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    bgcolor="#1C75BC",
                    padding=ft. padding.all(20),
                    border_radius=12,
                    shadow=ft.BoxShadow(
                        spread_radius=0,
                        blur_radius=30,
                        color=ft.Colors.with_opacity(0.4, "#000000"),
                        offset=ft.Offset(0, 6),
                    ),
                    rotate=ft. Rotate(-0.05),
                )
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        margin=ft.margin.only(bottom=30),
    )
    
    # Menu card builder
    def create_menu_card(title: str, image_path: str, on_click: Callable, gradient_color1: str, gradient_color2: str):
        """Create a styled menu card with image and button"""
        return ft.Container(
            content=ft.Stack(
                controls=[
                    # Background image
                    ft.Container(
                        content=ft. Image(
                            src=image_path,
                            fit=ft.ImageFit. COVER,
                            width=280,
                            height=140,
                        ),
                        border_radius=12,
                        clip_behavior=ft.ClipBehavior.HARD_EDGE,
                    ),
                    # Gradient overlay
                    ft.Container(
                        bgcolor=ft.Colors.with_opacity(0.3, "#000000"),
                        border_radius=12,
                        width=280,
                        height=140,
                    ),
                    # Button with gradient
                    ft.Container(
                        content=ft. Text(
                            title,
                            size=18,
                            weight="w600",
                            color="#FFFFFF",
                            text_align=ft.TextAlign. CENTER,
                        ),
                        gradient=ft.LinearGradient(
                            begin=ft.alignment.center_left,
                            end=ft.alignment.center_right,
                            colors=[gradient_color1, gradient_color2],
                        ),
                        border_radius=8,
                        padding=ft. padding.symmetric(horizontal=20, vertical=12),
                        alignment=ft.alignment.center,
                        on_click=on_click,
                        ink=True,
                        animate_opacity=200,
                        width=200,
                        height=50,
                    ),
                ],
                width=280,
                height=140,
                alignment=ft.alignment.center_right,
            ),
            border_radius=12,
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=20,
                color=ft.Colors.with_opacity(0.25, "#000000"),
                offset=ft.Offset(0, 4),
            ),
            width=280,
            height=140,
        )
    
    # Menu cards
    schedule_card = create_menu_card(
        "Расписание",
        "src/photo/Clip path group.png",
        on_schedule_click,
        "#1B75BB",
        "#2B2A80"
    )
    
    warmup_card = create_menu_card(
        "Разминка",
        "src/photo/Clip path group (1).png",
        on_warmup_click,
        "#1B75BB",
        "#2B2A80"
    )
    
    play_card = create_menu_card(
        "Играть",
        "src/photo/Clip path group (2).png",
        on_play_click,
        "#1B75BB",
        "#2B2A80"
    )
    
    # Team rating button with gradient background
    rating_container = ft.Container(
        content=ft.Row(
            controls=[
                ft.Text(
                    "Рейтинг команд",
                    size=18,
                    weight="w600",
                    color="#FFFFFF",
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        gradient=ft.LinearGradient(
            begin=ft.alignment. center_left,
            end=ft.alignment.center_right,
            colors=["#9B0773", "#EB008B"],
        ),
        border_radius=12,
        padding=ft.padding.symmetric(horizontal=30, vertical=16),
        shadow=ft.BoxShadow(
            spread_radius=0,
            blur_radius=20,
            color=ft.Colors.with_opacity(0.25, "#E40089"),
            offset=ft. Offset(0, 4),
        ),
        on_click=on_rating_click,
        ink=True,
        animate_opacity=200,
        width=250,
    )
    
    # Decorative elements (stars and shapes)
    decorative_star_1 = ft.Container(
        content=ft.Icon(
            name=ft.Icons.STAR,
            size=40,
            color=ft.Colors.with_opacity(0.7, "#E40089"),
        ),
        rotate=ft.Rotate(0.2),
        animate_rotation=300,
    )
    
    decorative_star_2 = ft.Container(
        content=ft.Icon(
            name=ft.Icons.STAR,
            size=30,
            color=ft.Colors.with_opacity(0.6, "#FFB8A0"),
        ),
        rotate=ft.Rotate(-0.1),
        animate_rotation=300,
    )
    
    # Main menu content
    menu_content = ft.Column(
        controls=[
            logo_container,
            schedule_card,
            warmup_card,
            play_card,
            ft.Container(height=20),  # Spacing
            rating_container,
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=20,
        expand=True,
    )
    
    # Main container with gradient background
    main_container = ft. Container(
        content=ft.Column(
            controls=[
                menu_content,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            expand=True,
        ),
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