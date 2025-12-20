import flet as ft


async def login_page(page: ft.Page):
    """
    Login page with gradient background and КВИЗО БОЙНЯ logo
    """
    
    def on_login_click(e):
        """Handle login button click"""
        email = email_field.value
        password = password_field.value
        
        if not email or not password:
            error_snackbar.content.value = "Пожалуйста, заполните все поля"
            error_snackbar.open = True
            page.update()
            return
        
        success_snackbar.content.value = f"Попытка входа: {email}"
        success_snackbar.open = True
        page.update()
    
    def on_forgot_password_click(e):
        """Handle forgot password link click"""
        info_snackbar.content.value = "Переход к сбросу пароля"
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
        hint_text="Value",
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
        hint_text="Value",
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
        content=ft.Text(
            "Вход",
            size=16,
            weight="w400",
            color="#FFFFFF",
            text_align=ft.TextAlign.CENTER,
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
                                src="src/photo/login.png",
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
    
    # Form container
    form_container = ft.Container(
        content=ft.Column(
            controls=[
                email_container,
                password_container,
                login_button,
                forgot_password_link,
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