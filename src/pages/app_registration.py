import flet as ft
import asyncio
from api.client import api_client


async def app_registration_page(page: ft.Page):
    """
    Application registration page - sign up for the app
    """
    
    def on_back_click(e):
        """Handle back button click"""
        page.go("/login")
    
    async def on_register_click(e):
        """Handle registration button click"""
        # Validate form
        if not username.value: 
            show_error("Введите имя пользователя")
            return
        if not full_name.value:
            show_error("Введите полное имя")
            return
        if not email.value:
            show_error("Введите email")
            return
        if not password.value:
            show_error("Введите пароль")
            return
        if len(password.value) < 6:
            show_error("Пароль должен быть не менее 6 символов")
            return
        if password.value != password_confirm.value:
            show_error("Пароли не совпадают")
            return
        
        # Show loading
        register_button.enabled = False
        page.update()
        
        try:
            # Подготавливаем данные пользователя
            user_data = {
                "username": username.value,
                "email": email.value,
                "full_name": full_name.value,
                "password": password.value,
            }
            
            # Регистрируем пользователя через API
            result = await api_client.register(
                username=user_data["username"],
                email=user_data["email"],
                password=user_data["password"]
            )
            
            if "error" in result:
                show_error(f"Ошибка: {result['error']}")
            else:
                snackbar.content.value = f"✓ Добро пожаловать, {user_data['username']}! Теперь войдите в аккаунт"
                snackbar.bgcolor = "#43A047"
                snackbar.open = True
                page.update()
                
                # Переходим на страницу логина после 2 секунд
                await asyncio.sleep(2)
                page.go("/login")
        except Exception as ex:
            show_error(f"Ошибка подключения: {str(ex)}")
        finally:
            register_button.enabled = True
            page.update()
    
    def show_error(message: str):
        """Show error message"""
        snackbar.content.value = f"✗ {message}"
        snackbar.bgcolor = "#E53935"
        snackbar.open = True
        page.update()
    
    # Snackbar for notifications
    snackbar = ft.SnackBar(
        content=ft.Text("", size=14, color="#FFFFFF"),
        bgcolor="#43A047",
        duration=2000,
    )
    page.overlay.append(snackbar)
    
    # Form fields
    username = ft.TextField(
        hint_text="Введите имя пользователя",
        border_color="#D9D9D9",
        filled=True,
        fill_color="#FFFFFF",
        border_radius=8,
        height=40,
        text_size=14,
    )
    
    full_name = ft.TextField(
        hint_text="Введите полное имя",
        border_color="#D9D9D9",
        filled=True,
        fill_color="#FFFFFF",
        border_radius=8,
        height=40,
        text_size=14,
    )
    
    email = ft.TextField(
        hint_text="Введите email",
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
    
    password_confirm = ft.TextField(
        hint_text="Повторите пароль",
        border_color="#D9D9D9",
        filled=True,
        fill_color="#FFFFFF",
        border_radius=8,
        height=40,
        text_size=14,
        password=True,
    )
    
    # Register button
    register_button = ft.Container(
        content=ft.Text(
            "Зарегистрироваться",
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
        width=250,
    )
    
    # Footer text
    footer_text = ft.Text(
        "Уже есть аккаунт?",
        size=12,
        weight="w400",
        color="#999999",
        text_align=ft.TextAlign.CENTER,
    )
    
    login_link = ft.TextButton(
        "Войти",
        style=ft.ButtonStyle(
            color="#2C2C2C",
            overlay_color=ft.Colors.TRANSPARENT,
        ),
        on_click=on_back_click,
    )
    
    footer_row = ft.Row(
        controls=[footer_text, login_link],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=4,
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
                    "Регистрация",
                    size=20,
                    weight="w600",
                    color="#000000",
                    expand=True,
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Container(width=40),
            ],
            alignment=ft.MainAxisAlignment.START,
        ),
        padding=ft.padding.symmetric(horizontal=16, vertical=12),
    )
    
    # Form container
    form_content = ft.Column(
        controls=[
            # Username
            ft.Text(
                "Имя пользователя (login)*",
                size=14,
                weight="w500",
                color="#1E1E1E",
            ),
            username,
            ft.Divider(height=16, color="transparent"),
            
            # Full name
            ft.Text(
                "Полное имя*",
                size=14,
                weight="w500",
                color="#1E1E1E",
            ),
            full_name,
            ft.Divider(height=16, color="transparent"),
            
            # Email
            ft.Text(
                "E-mail*",
                size=14,
                weight="w500",
                color="#1E1E1E",
            ),
            email,
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
            
            # Password confirm
            ft.Text(
                "Повторить пароль*",
                size=14,
                weight="w500",
                color="#1E1E1E",
            ),
            password_confirm,
            ft.Divider(height=32, color="transparent"),
            
            # Register button
            ft.Container(
                content=register_button,
                alignment=ft.alignment.center,
            ),
            ft.Divider(height=16, color="transparent"),
            
            # Footer text
            footer_row,
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
    main_content = ft.Column(
        controls=[
            header,
            ft.Container(
                content=scroll_form,
                expand=True,
                padding=ft.padding.symmetric(horizontal=20, vertical=16),
                clip_behavior=ft.ClipBehavior.HARD_EDGE,
            ),
        ],
        expand=True,
        spacing=0,
    )
    page.scroll = None
    
    # Main container with gradient background
    main_container = ft.Container(
        content=main_content,
        width=page.window.width,
        height=page.window.height,
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
        padding=ft.padding.only(
            top=35,  # отступ от челки
            bottom=20,  # отступ от кнопок навигации
            left=10,
            right=10
        ),

    )
    
    return main_container
