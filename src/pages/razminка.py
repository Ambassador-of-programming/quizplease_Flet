import flet as ft
from typing import Callable, List, Dict


async def razminка_page(page: ft.Page, on_back:  Callable = None):
    """
    Warmup (Разминка) page displaying quiz questions with multiple choice answers
    """
    
    # Sample quiz data
    quizzes:  List[Dict] = [
        {
            "question": "Какой из этих городов южнее? ",
            "answers": ["Каир", "Токио", "Рим", "Мадрид"],
            "correct_index": 0
        },
        {
            "question": "Какая столица самая большая?",
            "answers": ["Париж", "Берлин", "Лондон", "Москва"],
            "correct_index": 3
        },
        {
            "question": "Какой океан самый большой?",
            "answers": ["Атлантический", "Индийский", "Северный Ледовитый", "Тихий"],
            "correct_index": 3
        },
    ]
    
    current_quiz_index = [0]  # Using list to allow modification in nested function
    
    def on_answer_click(answer_text: str, is_correct: bool):
        """Handle answer button click"""
        def handler(e):
            if is_correct:
                snackbar. content. value = f"✓ Правильно!  {answer_text}"
                snackbar.bgcolor = "#43A047"
            else:
                snackbar. content.value = f"✗ Неправильно!  Правильный ответ: {quizzes[current_quiz_index[0]]['answers'][quizzes[current_quiz_index[0]]['correct_index']]}"
                snackbar. bgcolor = "#E53935"
            
            snackbar.open = True
            page.update()
            
            # Move to next question after 2 seconds
            if current_quiz_index[0] < len(quizzes) - 1:
                import asyncio
                async def next_question():
                    await asyncio.sleep(2)
                    current_quiz_index[0] += 1
                    update_quiz_display()
                
                # Schedule the next question
                page.run_task(next_question)
        
        return handler
    
    def on_back_click(e):
        """Handle back button click"""
        if on_back:
            on_back()
    
    def update_quiz_display():
        """Update the quiz display with current question"""
        current_quiz = quizzes[current_quiz_index[0]]
        
        # Update question
        question_text. value = current_quiz["question"]
        
        # Update answer buttons
        answer_buttons. controls.clear()
        for i, answer in enumerate(current_quiz["answers"]):
            is_correct = (i == current_quiz["correct_index"])
            answer_buttons. controls.append(
                create_answer_button(answer, is_correct)
            )
        
        page.update()
    
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
                    "Разминка",
                    size=24,
                    weight="w600",
                    color="#FFFFFF",
                    expand=True,
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Container(width=40),  # Spacer for alignment
            ],
            alignment=ft.MainAxisAlignment. START,
        ),
        padding=ft.padding.symmetric(horizontal=16, vertical=12),
    )
    
    # Question container
    question_text = ft.Text(
        quizzes[0]["question"],
        size=32,
        weight="w700",
        color="#FFFFFF",
        text_align=ft.TextAlign. CENTER,
    )
    
    question_container = ft.Container(
        content=question_text,
        bgcolor="#1F67AF",
        border_radius=16,
        padding=ft.padding.symmetric(vertical=40, horizontal=20),
        margin=ft.margin.symmetric(horizontal=16, vertical=16),
    )
    
    # Answer button builder
    def create_answer_button(answer_text: str, is_correct:  bool) -> ft.Container:
        """Create a styled answer button"""
        return ft.Container(
            content=ft.Text(
                answer_text,
                size=28,
                weight="w700",
                color="#FFFFFF",
                text_align=ft. TextAlign.CENTER,
            ),
            bgcolor="#E60189",
            border_radius=16,
            padding=ft.padding.symmetric(vertical=16, horizontal=20),
            alignment=ft.alignment.center,
            on_click=on_answer_click(answer_text, is_correct),
            ink=True,
            margin=ft.margin.symmetric(horizontal=16, vertical=8),
        )
    
    # Answer buttons container
    answer_buttons = ft. Column(
        controls=[
            create_answer_button(answer, i == quizzes[0]["correct_index"])
            for i, answer in enumerate(quizzes[0]["answers"])
        ],
        spacing=8,
    )
    
    # Snackbar for notifications
    snackbar = ft. SnackBar(
        content=ft.Text("", size=14, color="#FFFFFF"),
        bgcolor="#43A047",
        duration=2000,
    )
    page.overlay.append(snackbar)
    
    # Progress indicator
    progress_text = ft.Text(
        f"{current_quiz_index[0] + 1} / {len(quizzes)}",
        size=14,
        weight="w500",
        color="#FFFFFF",
        text_align=ft. TextAlign.CENTER,
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
        width=page.window. width,
        height=page. window.height,
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