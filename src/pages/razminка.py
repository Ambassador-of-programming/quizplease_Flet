import flet as ft
from typing import  List, Dict
import asyncio
from api.client import api_client


async def razminка_page(page: ft.Page):
    """
    Warmup (Разминка) page displaying quiz questions with multiple choice answers
    """
    
    # State variables
    quizzes: List[Dict] = []
    current_quiz_index = [0]
    current_question_index = [0]
    answered_correctly = [0]  # Count of correct answers
    loading = [True]

    async def load_quizzes():
        """Загружает разминки с API"""
        try:
            result = await api_client.get("/quizzes/")
            print(f"[DEBUG] Quizzes loaded: {result}")
            if isinstance(result, list):
                # Filter only active quizzes with questions
                active_quizzes = [q for q in result if q.get("is_active") and q.get("questions")]
                return active_quizzes
            return []
        except Exception as e:
            print(f"Error loading quizzes: {e}")
            return []
    
    def on_answer_click(option_id: int, is_correct: bool, question_id: int):
        """Handle answer button click"""
        def handler(e):
            # Submit answer to API
            async def submit_answer():
                try:
                    result = await api_client.post(
                        "/answers/submit",
                        json={"question_id": question_id, "selected_option_id": option_id}
                    )
                    print(f"[DEBUG] Answer submitted: {result}")
                    
                    if is_correct:
                        answered_correctly[0] += 1
                        snackbar.content.value = "✓ Правильно!"
                        snackbar.bgcolor = "#43A047"
                    else:
                        snackbar.content.value = "✗ Неправильно!"
                        snackbar.bgcolor = "#E53935"
                    
                    snackbar.open = True
                    page.update()
                    
                    # Move to next question after 2 seconds
                    await asyncio.sleep(2)
                    move_to_next_question()
                    
                except Exception as err:
                    print(f"Error submitting answer: {err}")
                    snackbar.content.value = "Ошибка при отправке ответа"
                    snackbar.bgcolor = "#E53935"
                    snackbar.open = True
                    page.update()
            
            page.run_task(submit_answer)
            
            page.run_task(submit_answer)
        
        return handler
    
    def move_to_next_question():
        """Move to the next question or finish quiz"""
        current_quiz = quizzes[current_quiz_index[0]]
        current_question_index[0] += 1
        
        if current_question_index[0] < len(current_quiz["questions"]):
            update_quiz_display()
        else:
            # Quiz completed
            show_completion_screen()
    
    def on_back_click(e):
        """Handle back button click"""
        page.go("/menu")
    
    def update_quiz_display():
        """Update the quiz display with current question"""
        if not quizzes or current_quiz_index[0] >= len(quizzes):
            return
        
        current_quiz = quizzes[current_quiz_index[0]]
        questions = current_quiz.get("questions", [])
        
        if current_question_index[0] >= len(questions):
            show_completion_screen()
            return
        
        current_question = questions[current_question_index[0]]
        options = current_question.get("options", [])
        
        # Update question
        question_text.value = current_question["question_text"]
        
        # Update answer buttons
        answer_buttons.controls.clear()
        for option in options:
            is_correct = option.get("is_correct", False)
            answer_buttons.controls.append(
                create_answer_button(
                    option["option_text"],
                    is_correct,
                    option["id"],
                    current_question["id"]
                )
            )
        
        # Update progress
        total_questions = len(questions)
        progress_text.value = f"{current_question_index[0] + 1} / {total_questions}"
        
        page.update()
    
    def show_completion_screen():
        """Show quiz completion screen"""
        current_quiz = quizzes[current_quiz_index[0]]
        total_questions = len(current_quiz["questions"])
        percentage = int((answered_correctly[0] / total_questions * 100)) if total_questions > 0 else 0
        
        # Clear main content and show completion
        main_content.controls.clear()
        main_content.controls.extend([
            header,
            ft.Container(expand=True),  # Spacer
            ft.Column(
                controls=[
                    ft.Text(
                        "Разминка завершена!",
                        size=32,
                        weight="w700",
                        color="#FFFFFF",
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Container(height=20),
                    ft.Text(
                        f"Правильных ответов: {answered_correctly[0]}/{total_questions}",
                        size=24,
                        weight="w600",
                        color="#FFFFFF",
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Text(
                        f"{percentage}%",
                        size=48,
                        weight="w700",
                        color="#FFD700" if percentage >= 70 else "#FF6B9D",
                        text_align=ft.TextAlign.CENTER,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            ft.Container(expand=True),  # Spacer
            ft.Container(
                content=ft.ElevatedButton(
                    "Вернуться в меню",
                    width=200,
                    height=50,
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=12),
                        bgcolor="#E60189",
                        color="#FFFFFF",
                    ),
                    on_click=on_back_click,
                ),
                padding=ft.padding.symmetric(horizontal=16, vertical=16),
                alignment=ft.alignment.center,
            ),
        ])
        page.update()
    
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
                    "Разминка",
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
    
    # Question container
    question_text = ft.Text(
        "Загружаю вопросы...",
        size=32,
        weight="w700",
        color="#FFFFFF",
        text_align=ft.TextAlign.CENTER,
    )
    
    question_container = ft.Container(
        content=question_text,
        bgcolor="#1F67AF",
        border_radius=16,
        padding=ft.padding.symmetric(vertical=40, horizontal=20),
        margin=ft.margin.symmetric(horizontal=16, vertical=16),
    )
    
    # Answer button builder
    def create_answer_button(answer_text: str, is_correct: bool, option_id: int, question_id: int) -> ft.Container:
        """Create a styled answer button"""
        return ft.Container(
            content=ft.Text(
                answer_text,
                size=18,
                weight="w700",
                color="#FFFFFF",
                text_align=ft.TextAlign.CENTER,
            ),
            bgcolor="#E60189",
            border_radius=16,
            padding=ft.padding.symmetric(vertical=16, horizontal=20),
            alignment=ft.alignment.center,
            on_click=on_answer_click(option_id, is_correct, question_id),
            ink=True,
            margin=ft.margin.symmetric(horizontal=16, vertical=8),
        )
    
    # Answer buttons container
    answer_buttons = ft.Column(
        controls=[],
        spacing=8,
    )
    
    # Snackbar for notifications
    snackbar = ft.SnackBar(
        content=ft.Text("", size=14, color="#FFFFFF"),
        bgcolor="#43A047",
        duration=2000,
    )
    page.overlay.append(snackbar)
    
    # Progress indicator
    progress_text = ft.Text(
        "0 / 0",
        size=14,
        weight="w500",
        color="#FFFFFF",
        text_align=ft.TextAlign.CENTER,
    )
    
    progress_container = ft.Container(
        content=progress_text,
        padding=ft.padding.symmetric(horizontal=16, vertical=8),
    )
    
    # Main content
    main_content = ft.Column(
        controls=[
            header,
            progress_container,
            question_container,
            answer_buttons,
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
    
    # Load quizzes on page init
    async def init_page():
        """Initialize page by loading quizzes"""
        nonlocal quizzes
        quizzes = await load_quizzes()
        loading[0] = False
        
        if quizzes:
            current_quiz_index[0] = 0
            current_question_index[0] = 0
            answered_correctly[0] = 0
            update_quiz_display()
        else:
            question_text.value = "Нет доступных разминок"
            page.update()
    
    # Start loading quizzes
    page.run_task(init_page)
    page.scroll = ft.ScrollMode.HIDDEN
    
    return main_container