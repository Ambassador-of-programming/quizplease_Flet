import flet as ft
from typing import Callable


async def registration_page(page: ft.Page, on_back: Callable = None):
    """
    Registration page for game sign up with all form fields
    """
    
    def on_back_click(e):
        """Handle back button click"""
        if on_back:
            on_back()
    
    def on_register_click(e):
        """Handle registration button click"""
        # Validate form
        if not team_name.value: 
            show_error("Введите название команды")
            return
        if not captain_name.value:
            show_error("Введите имя капитана")
            return
        if not email.value:
            show_error("Введите email")
            return
        if not phone.value:
            show_error("Введите телефон")
            return
        if not login.value:
            show_error("Введите логин")
            return
        if not password.value:
            show_error("Введите пароль")
            return
        if not team_size.value:
            show_error("Выберите количество человек")
            return
        if not feedback.value:
            show_error("Расскажите как вы узнали о нас")
            return
        if not checkbox1.value or not checkbox2.value:
            show_error("Согласитесь с условиями")
            return
        
        snackbar.content. value = f"✓ Команда '{team_name.value}' успешно зарегистрирована!"
        snackbar.bgcolor = "#43A047"
        snackbar.open = True
        page.update()
    
    def show_error(message: str):
        """Show error message"""
        snackbar.content. value = f"✗ {message}"
        snackbar.bgcolor = "#E53935"
        snackbar.open = True
        page. update()
    
    # Snackbar for notifications
    snackbar = ft. SnackBar(
        content=ft.Text("", size=14, color="#FFFFFF"),
        bgcolor="#43A047",
        duration=2000,
    )
    page.overlay. append(snackbar)
    
    # Form fields
    team_name = ft. TextField(
        hint_text="Введите название",
        border_color="#D9D9D9",
        filled=True,
        fill_color="#FFFFFF",
        border_radius=8,
        height=40,
        text_size=14,
    )
    
    captain_name = ft.TextField(
        hint_text="Введите имя",
        border_color="#D9D9D9",
        filled=True,
        fill_color="#FFFFFF",
        border_radius=8,
        height=40,
        text_size=14,
    )
    
    email = ft.TextField(
        hint_text="Введите почту",
        border_color="#D9D9D9",
        filled=True,
        fill_color="#FFFFFF",
        border_radius=8,
        height=40,
        text_size=14,
    )
    
    phone = ft.TextField(
        hint_text="+7",
        border_color="#D9D9D9",
        filled=True,
        fill_color="#FFFFFF",
        border_radius=8,
        height=40,
        text_size=14,
    )
    
    login = ft.TextField(
        hint_text="Введите логин",
        border_color="#D9D9D9",
        filled=True,
        fill_color="#FFFFFF",
        border_radius=8,
        height=40,
        text_size=14,
    )
    
    password = ft.TextField(
        hint_text="Введите пароль",
        border_color="#D9D9D9",
        filled=True,
        fill_color="#FFFFFF",
        border_radius=8,
        height=40,
        text_size=14,
        password=True,
    )
    
    # Team size dropdown
    team_size = ft.Dropdown(
        hint_text="Value",
        border_color="#D9D9D9",
        filled=True,
        fill_color="#FFFFFF",
        border_radius=8,
        options=[
            ft.dropdown. Option("3"),
            ft.dropdown.Option("4"),
            ft.dropdown. Option("5"),
            ft.dropdown.Option("6"),
            ft.dropdown.Option("7"),
            ft.dropdown.Option("8"),
        ],
    )
    
    # Feedback textarea
    feedback = ft.TextField(
        hint_text="Расскажите",
        border_color="#D9D9D9",
        filled=True,
        fill_color="#FFFFFF",
        border_radius=8,
        min_lines=3,
        max_lines=5,
        multiline=True,
    )
    
    # Checkboxes
    checkbox1 = ft.Checkbox(
        label="Мы играем в первый раз",
        value=True,
        label_position=ft.LabelPosition.RIGHT,
    )
    
    checkbox2 = ft.Checkbox(
        label="Оплатить на игре",
        value=True,
        label_position=ft.LabelPosition.RIGHT,
    )
    
    # Register button
    register_button = ft.Container(
        content=ft.Text(
            "Записаться",
            size=16,
            weight="w600",
            color="#FFFFFF",
            text_align=ft.TextAlign.CENTER,
        ),
        bgcolor="#E60189",
        border_radius=8,
        padding=ft.padding.symmetric(vertical=14, horizontal=30),
        alignment=ft.alignment.center,
        on_click=on_register_click,
        ink=True,
        width=200,
    )
    
    # Footer text
    footer_text = ft.Text(
        "Нажимая кнопку 'Записаться' вы согласиваетесь с политикой обработки персональных данных",
        size=12,
        weight="w400",
        color="#999999",
        text_align=ft.TextAlign. CENTER,
    )
    
    # Header
    header = ft.Container(
        content=ft.Row(
            controls=[
                ft.IconButton(
                    icon=ft.Icons.ARROW_BACK,
                    icon_size=24,
                    icon_color="#000000",
                    on_click=on_back_click,
                ),
                ft.Text(
                    "Записаться на игру",
                    size=20,
                    weight="w600",
                    color="#000000",
                    expand=True,
                    text_align=ft.TextAlign. CENTER,
                ),
                ft.Container(width=40),
            ],
            alignment=ft.MainAxisAlignment.START,
        ),
        padding=ft.padding.symmetric(horizontal=16, vertical=12),
    )
    
    # Form container
    form_content = ft. Column(
        controls=[
            # Team name
            ft.Text(
                "Название команды*",
                size=14,
                weight="w500",
                color="#1E1E1E",
            ),
            team_name,
            ft. Divider(height=16, color="transparent"),
            
            # Captain name
            ft.Text(
                "Имя капитана*",
                size=14,
                weight="w500",
                color="#1E1E1E",
            ),
            captain_name,
            ft.Divider(height=16, color="transparent"),
            
            # Email
            ft.Text(
                "E-mail*",
                size=14,
                weight="w500",
                color="#1E1E1E",
            ),
            email,
            ft. Divider(height=16, color="transparent"),
            
            # Phone
            ft.Text(
                "Телефон капитана*",
                size=14,
                weight="w500",
                color="#1E1E1E",
            ),
            phone,
            ft.Divider(height=16, color="transparent"),
            
            # Login
            ft.Text(
                "Логин*",
                size=14,
                weight="w500",
                color="#1E1E1E",
            ),
            login,
            ft.Divider(height=16, color="transparent"),
            
            # Password
            ft.Text(
                "Пароль*",
                size=14,
                weight="w500",
                color="#1E1E1E",
            ),
            password,
            ft.Divider(height=16, color="transparent"),
            
            # Team size
            ft.Text(
                "Количество человек в команде*",
                size=14,
                weight="w500",
                color="#1E1E1E",
            ),
            team_size,
            ft.Divider(height=16, color="transparent"),
            
            # Feedback
            ft. Text(
                "Откуда вы о нас узнали?  *",
                size=14,
                weight="w500",
                color="#1E1E1E",
            ),
            feedback,
            ft.Divider(height=24, color="transparent"),
            
            # Checkboxes
            checkbox1,
            ft.Divider(height=12, color="transparent"),
            checkbox2,
            ft. Divider(height=32, color="transparent"),
            
            # Register button
            ft.Container(
                content=register_button,
                alignment=ft.alignment.center,
            ),
            ft.Divider(height=16, color="transparent"),
            
            # Footer text
            footer_text,
        ],
        spacing=0,
    )
    
    # Scrollable form
    scroll_form = ft.Column(
        controls=[form_content],
        expand=True,
        scroll=ft.ScrollMode.AUTO,
    )
    
    # Main content with scroll
    main_content = ft. Column(
        controls=[
            header,
            ft.Container(
                content=scroll_form,
                expand=True,
                padding=ft.padding.symmetric(horizontal=20, vertical=16),
                clip_behavior=ft. ClipBehavior.HARD_EDGE,
            ),
        ],
        expand=True,
        spacing=0,
    )
    
    # Main container with gradient background
    main_container = ft. Container(
        content=main_content,
        width=page. window. width,
        height=page. window.height,
        gradient=ft.LinearGradient(
            begin=ft.alignment.top_left,
            end=ft.alignment.bottom_right,
            colors=[
                "#E8D5F2",  # Light purple
                "#F5D5E8",  # Light pink
                "#FFE8E0",  # Peach
            ],
            stops=[0.0, 0.5, 1.0],
        ),
        alignment=ft.alignment.center,
    )
    
    return main_container