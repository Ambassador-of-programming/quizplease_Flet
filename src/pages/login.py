import flet as ft
import asyncio
from api.client import api_client


async def login_page(page: ft.Page):
    """
    Login page with gradient background and API integration
    """
    
    loading_indicator = ft.ProgressRing(visible=False)
    
    async def on_login_click(e):
        """Handle login button click with API call"""
        username = email_field.value
        password = password_field.value
        
        if not username or not password:
            error_snackbar.content.value = "Пожалуйста, заполните все поля"
            error_snackbar.open = True
            page.update()
            return
        
        # Show loading
        loading_indicator.visible = True
        login_button.enabled = False
        page.update()
        
        try:
            # Call API
            result = await api_client.login(username, password)
            
            if "error" in result:
                error_snackbar.content.value = f"Ошибка: {result['error']}"
                error_snackbar.open = True
            elif "access_token" in result:
                page.session.set("access_token", result['access_token'])
                success_snackbar.content.value = f"Добро пожаловать, {result.get('user', {}).get('username', username)}!"
                success_snackbar.open = True
                # Navigate to menu after 1 second
                await asyncio.sleep(1)
                
                page.go("/menu")
            else:
                error_snackbar.content.value = "Неудачный вход. Проверьте учетные данные"
                error_snackbar.open = True
        except Exception as ex:
            error_snackbar.content.value = f"Ошибка подключения: {str(ex)}"
            error_snackbar.open = True
        finally:
            loading_indicator.visible = False
            login_button.enabled = True
            page.update()
    
    def on_register_click(e):
        """Navigate to app registration page"""
        page.go("/app_registration")
    
    def on_team_registration_click(e):
        """Navigate to team registration page"""
        page.go("/team_registration")
    
    def on_forgot_password_click(e):
        """Handle forgot password link click"""
        info_snackbar.content.value = "Функция восстановления пароля в разработке"
        info_snackbar.open = True
        page.update()
    
    # Email input field
    email_label = ft.Text(
        "Логин",
        size=16,
        weight="w400",
        color="#1E1E1E"
    )
    
    email_field = ft.TextField(
        label="",
        hint_text="Введите логин",
        border_color="#D9D9D9",
        border_radius=8,
        border_width=1,
        content_padding=ft.padding.symmetric(horizontal=16, vertical=12),
        height=40,
        text_size=16,
        bgcolor="#FFFFFF",
        color="#1E1E1E",
        hint_style=ft.TextStyle(size=16, color="#B3B3B3"),
        cursor_color="#2C2C2C",
    )
    
    email_container = ft.Column(
        controls=[email_label, email_field],
        spacing=8,
        tight=True,
    )
    
    # Password input field
    password_label = ft.Text(
        "Пароль",
        size=16,
        weight="w400",
        color="#1E1E1E"
    )
    
    password_field = ft.TextField(
        label="",
        hint_text="Введите пароль",
        border_color="#D9D9D9",
        border_radius=8,
        border_width=1,
        content_padding=ft.padding.symmetric(horizontal=16, vertical=12),
        height=40,
        text_size=16,
        password=True,
        bgcolor="#FFFFFF",
        color="#1E1E1E",
        hint_style=ft.TextStyle(size=16, color="#B3B3B3"),
        cursor_color="#2C2C2C",
    )
    
    password_container = ft.Column(
        controls=[password_label, password_field],
        spacing=8,
        tight=True,
    )
    
    # Login button
    login_button = ft.Container(
        content=ft.Row(
            controls=[
                ft.Text(
                    "Вход",
                    size=16,
                    weight="w400",
                    color="#FFFFFF",
                    text_align=ft.TextAlign.CENTER,
                ),
                loading_indicator,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=10,
        ),
        bgcolor="#2C2C2C",
        border_radius=8,
        padding=ft.padding.symmetric(vertical=12, horizontal=12),
        alignment=ft.alignment.center,
        on_click=on_login_click,
        ink=True,
    )
    
    # Forgot password link
    forgot_password_link = ft.TextButton(
        "Забыли пароль?",
        style=ft.ButtonStyle(
            color="#1E1E1E",
            overlay_color=ft.Colors.TRANSPARENT,
        ),
        on_click=on_forgot_password_click,
    )
    
    # Logo container with text
    logo_container = ft.Container(
        content=ft.Column(
            controls=[
                ft.Container(
                    content=ft.Column(
                        controls=[

                            ft.Image(
                                src="images/login.png",
                                width=190,
                                height=127,
                                fit=ft.ImageFit.CONTAIN,
                            ),
                        ],
                        spacing=5,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    bgcolor="#1C75BC",
                    padding=ft.padding.all(20),
                    border_radius=12,
                    shadow=ft.BoxShadow(
                        spread_radius=0,
                        blur_radius=30,
                        color=ft.Colors.with_opacity(0.4, "#000000"),
                        offset=ft.Offset(0, 6),
                    ),
                    rotate=ft.Rotate(-0.05),
                )
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        margin=ft.margin.only(bottom=40),
    )
    
    # Registration link
    ft.TextButton(
        "Записаться на игру",
        style=ft.ButtonStyle(
            color="#2C2C2C",
            overlay_color=ft.Colors.TRANSPARENT,
        ),
        on_click=on_team_registration_click,
    )
    
    # App Registration link
    app_registration_link = ft.TextButton(
        "Зарегистрироваться",
        style=ft.ButtonStyle(
            color="#2C2C2C",
            overlay_color=ft.Colors.TRANSPARENT,
        ),
        on_click=on_register_click,
    )
    
    # Form container
    form_container = ft.Container(
        content=ft.Column(
            controls=[
                email_container,
                password_container,
                login_button,
                forgot_password_link,
                app_registration_link,
            ],
            spacing=24,
            tight=True,
        ),
        padding=24,
        bgcolor="#FFFFFF",
        border=ft.border.all(width=1, color="#D9D9D9"),
        border_radius=8,
        width=320,
        shadow=ft.BoxShadow(
            spread_radius=0,
            blur_radius=20,
            color=ft.Colors.with_opacity(0.15, "#000000"),
            offset=ft.Offset(0, 4),
        )
    )
    
    # Snackbars
    error_snackbar = ft.SnackBar(
        content=ft.Text("", size=14, color="#FFFFFF"),
        bgcolor="#E53935",
        duration=2000,
    )
    
    success_snackbar = ft.SnackBar(
        content=ft.Text("", size=14, color="#FFFFFF"),
        bgcolor="#43A047",
        duration=2000,
    )
    
    info_snackbar = ft.SnackBar(
        content=ft.Text("", size=14, color="#FFFFFF"),
        bgcolor="#1976D2",
        duration=2000,
    )
    
    page.overlay.extend([error_snackbar, success_snackbar, info_snackbar])
    page.scroll = None
    
    # Main container with gradient background
    main_container = ft.Container(
        content=ft.Column(
            controls=[
                logo_container,
                form_container,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            expand=True,
        ),
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