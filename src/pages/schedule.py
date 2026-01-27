import flet as ft
from typing import  List, Dict
import asyncio
from api.client import api_client

# Global variable to store selected event_id for registration
selected_event_id = None


async def schedule_page(page: ft.Page):
    """
    Schedule page displaying a list of quiz events
    """
    
    # Events data
    events: List[Dict] = []
    
    async def load_events():
        """Загружает список событий с API"""
        nonlocal events
        try:
            print("[DEBUG] Calling api_client.get_schedule()...")
            result = await api_client.get_schedule(limit=100)
            print(f"[DEBUG] API Response type: {type(result)}")
            print(f"[DEBUG] API Response: {result}")
            
            if isinstance(result, list):
                events = result
                print(f"[DEBUG] Events loaded as list: {len(events)} items")
            elif isinstance(result, dict):
                if "error" in result:
                    print(f"[DEBUG] API returned error: {result['error']}")
                    events = []
                else:
                    # Could be wrapped response
                    if "events" in result:
                        events = result["events"]
                    else:
                        events = []
                    print(f"[DEBUG] Events from dict: {len(events)} items")
            else:
                print(f"[DEBUG] Unexpected response type: {type(result)}")
                events = []
            
            print(f"[DEBUG] Final events count: {len(events)}")
            return events
        except Exception as e:
            print(f"[ERROR] Error loading events: {e}")
            import traceback
            traceback.print_exc()
            return []
    
    def on_signup_click(event_index: int):
        """Handle sign up button click"""
        def handler(e):
            async def signup_task():
                global selected_event_id
                try:
                    # Сохраняем ID события в глобальную переменную
                    if event_index < len(events):
                        event_data = events[event_index]
                        selected_event_id = event_data.get('id')

                        page.update()
                        
                        # Переходим на страницу регистрации команды
                        await asyncio.sleep(1)
                        print(f"[DEBUG] Navigating to team registration for event_id={selected_event_id}")
                        page.session.set("selected_event_id", selected_event_id)
                        page.go("/team_registration")
                except Exception as ex:
                    
                    page.update()
            
            page.run_task(signup_task)
        return handler
    
    def on_back_click(e):
        """Handle back button click"""
        page.go("/menu")

    async def update_events_view():
        while True:
            page.run_task(update_events_view)
            await asyncio.sleep(60) 
    
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
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
        padding=ft.padding.symmetric(horizontal=16, vertical=12),
    )
    
    # Event card builder
    def create_event_card(event: Dict, index: int) -> ft.Container:
        """Create a styled event card"""
        
        # Parse and format time
        try:
            from datetime import datetime
            start_time = event.get("start_time", "")
            if start_time:
                # Parse ISO format: '2025-12-24T07:23:26.231000'
                dt = datetime.fromisoformat(start_time.replace('Z', '+00:00'))
                time_str = dt.strftime("%d.%m.%Y %H:%M")
            else:
                time_str = "N/A"
        except Exception as e:
            time_str = event.get("start_time", "N/A")
        
        # Format cost
        cost_str = f"{event.get('cost', 0)} ₽" if event.get('cost') else "Бесплатно"
        
        # Info item with icon
        def create_info_item(icon: str, label: str, value: str) -> ft.Row:
            return ft.Row(
                controls=[
                    ft.Container(
                        content=ft.Icon(
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
                        content=ft.Text(
                            event["title"],
                            size=28,
                            weight="w800",
                            color="#000000",
                            text_align=ft.TextAlign.CENTER,
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
                                    event.get("location", "N/A")
                                ),
                                create_info_item(
                                    ft.Icons.SCHEDULE,
                                    "Время",
                                    time_str
                                ),
                                create_info_item(
                                    ft.Icons.STAR,
                                    "Стоимость",
                                    cost_str
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
                        content=ft.Container(
                            content=ft.Text(
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
    
    # Create columns for event cards - will be updated after loading
    scroll_content = ft.Column(
        controls=[],
        spacing=16,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )
    
    # Function to update the view with loaded events
    async def update_events_view():
        """Load events from API and update the view"""
        try:
            print("[DEBUG] Starting update_events_view...")
            # Check if user is logged in (has token)
            if not api_client.token:
                print("[DEBUG] User not logged in, skipping event loading")
                scroll_content.controls.clear()
                scroll_content.controls.append(
                    ft.Container(
                        content=ft.Text(
                            "Пожалуйста, залогиньтесь сначала",
                            size=18,
                            weight="w600",
                            color="#FFFFFF",
                            text_align=ft.TextAlign.CENTER,
                        ),
                        padding=ft.padding.symmetric(vertical=40),
                    )
                )
                page.update()
                return
            
            await load_events()
            print(f"[DEBUG] After load_events, events count: {len(events)}")
            
            # Clear existing controls
            scroll_content.controls.clear()
            
            if events:
                print(f"[DEBUG] Found {len(events)} events, creating cards...")
                # Create cards for each event
                for i, event in enumerate(events):
                    print(f"[DEBUG] Creating card for event {i}: {event.get('title', 'Unknown')}")
                    scroll_content.controls.append(create_event_card(event, i))
            else:
                print("[DEBUG] No events found, showing empty message...")
                # Show message if no events
                scroll_content.controls.append(
                    ft.Container(
                        content=ft.Text(
                            "Нет предстоящих событий",
                            size=18,
                            weight="w600",
                            color="#FFFFFF",
                            text_align=ft.TextAlign.CENTER,
                        ),
                        padding=ft.padding.symmetric(vertical=40),
                    )
                )

            page.update()
        except Exception as e:
            print(f"[ERROR] Error updating events view: {e}")
            # snackbar.content.value = f"Ошибка загрузки: {str(e)}"
            # snackbar.bgcolor = "#E53935"
            # snackbar.open = True
            page.update()
    
    asyncio.create_task(update_events_view())
    page.scroll = ft.ScrollMode.HIDDEN
    # Don't load events automatically - wait for user to refresh or navigate to page
    # Events will be loaded when user presses refresh button

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
        padding=ft.padding.only(
            top=35,  # отступ от челки
            bottom=20,  # отступ от кнопок навигации
            left=10,
            right=10
        ),
    )
    
    return main_container