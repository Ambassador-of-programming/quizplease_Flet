import httpx
from typing import Optional, Dict, Any


# Configuração do API
API_BASE_URL = "http://167.86.104.152:8000/api"
TIMEOUT = 10.0

class APIClient:
    """Cliente para comunicação com a API FastAPI"""
    
    def __init__(self):
        self.base_url = API_BASE_URL
        self.token: Optional[str] = None
        self.client = None
    
    async def get_client(self) -> httpx.AsyncClient:
        """Obtém ou cria um cliente HTTP assíncrono"""
        if self.client is None:
            self.client = httpx.AsyncClient(timeout=TIMEOUT)
        return self.client
    
    def set_token(self, token: str):
        """Define o token JWT para autenticação"""
        print(f"[DEBUG api_client] Setting token: {token[:20]}..." if token else "[DEBUG api_client] Setting empty token")
        self.token = token
    
    def get_headers(self) -> Dict[str, str]:
        """Retorna headers com autenticação se disponível"""
        headers = {"Content-Type": "application/json"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
            print(f"[DEBUG api_client] Using auth header with token: {self.token[:20]}...")
        else:
            print("[DEBUG api_client] No token set - requests will be unauthorized")
        return headers
    
    async def register(self, username: str, email: str, password: str) -> Dict[str, Any]:
        """Registra um novo usuário"""
        try:
            client = await self.get_client()
            response = await client.post(
                f"{self.base_url}/auth/register",
                json={
                    "username": username,
                    "email": email,
                    "password": password,
                    "full_name": username
                },
                headers=self.get_headers()
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            return {"error": str(e)}
    
    async def login(self, username: str, password: str) -> Dict[str, Any]:
        """Faz login do usuário"""
        try:
            print(f"[DEBUG api_client] Login attempt for user: {username}")
            client = await self.get_client()
            response = await client.post(
                f"{self.base_url}/auth/login",
                json={
                    "username": username,
                    "password": password
                },
                headers=self.get_headers()
            )
            response.raise_for_status()
            data = response.json()
            if "access_token" in data:
                print("[DEBUG api_client] Login successful, received token")
                self.set_token(data["access_token"])
            return data
        except httpx.HTTPError as e:
            print(f"[DEBUG api_client] Login error: {str(e)}")
            return {"error": str(e)}
    
    async def get_current_user(self) -> Dict[str, Any]:
        """Obtém dados do usuário autenticado"""
        try:
            client = await self.get_client()
            response = await client.get(
                f"{self.base_url}/auth/me",
                headers=self.get_headers()
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            return {"error": str(e)}
    
    async def get_main_menu(self) -> Dict[str, Any]:
        """Obtém dados do menu principal"""
        try:
            client = await self.get_client()
            response = await client.get(
                f"{self.base_url}/menu/main",
                headers=self.get_headers()
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            return {"error": str(e)}
    
    async def get_quizzes(self, skip: int = 0, limit: int = 10) -> Dict[str, Any]:
        """Obtém lista de quizzes"""
        try:
            client = await self.get_client()
            response = await client.get(
                f"{self.base_url}/quizzes/?skip={skip}&limit={limit}",
                headers=self.get_headers()
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            return {"error": str(e)}
    
    async def get_teams(self, skip: int = 0, limit: int = 10) -> Dict[str, Any]:
        """Obtém lista de times"""
        try:
            client = await self.get_client()
            response = await client.get(
                f"{self.base_url}/teams/?skip={skip}&limit={limit}",
                headers=self.get_headers()
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            return {"error": str(e)}
    
    async def create_team(self, team_data: Dict[str, Any]) -> Dict[str, Any]:
        """Создает новую команду (регистрация)"""
        try:
            client = await self.get_client()
            response = await client.post(
                f"{self.base_url}/teams/",
                json=team_data,
                headers=self.get_headers()
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            return {"error": str(e)}
    
    async def get_schedule(self, skip: int = 0, limit: int = 10) -> Dict[str, Any]:
        """Получает расписание квизов (событий)"""
        try:
            print(f"[DEBUG api_client] get_schedule called, token exists: {bool(self.token)}")
            client = await self.get_client()
            response = await client.get(
                f"{self.base_url}/events/?skip={skip}&limit={limit}",
                headers=self.get_headers()
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            print(f"[DEBUG api_client] get_schedule error: {str(e)}")
            return {"error": str(e)}
    
    async def get_event(self, event_id: int) -> Dict[str, Any]:
        """Получает деталь события"""
        try:
            client = await self.get_client()
            response = await client.get(
                f"{self.base_url}/events/{event_id}",
                headers=self.get_headers()
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            return {"error": str(e)}
    
    async def get_warmup_questions(self, limit: int = 10) -> Dict[str, Any]:
        """Получает вопросы для разминки"""
        try:
            client = await self.get_client()
            response = await client.get(
                f"{self.base_url}/quizzes/warmup?limit={limit}",
                headers=self.get_headers()
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            return {"error": str(e)}
    
    async def submit_answer(self, question_id: int, answer_id: int) -> Dict[str, Any]:
        """Отправляет ответ на вопрос"""
        try:
            client = await self.get_client()
            response = await client.post(
                f"{self.base_url}/answers/",
                json={
                    "question_id": question_id,
                    "answer_id": answer_id
                },
                headers=self.get_headers()
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            return {"error": str(e)}
    
    async def signup_event(self, event_id: int, team_data: Dict[str, Any]) -> Dict[str, Any]:
        """Записывает команду на событие и регистрирует её"""
        try:
            client = await self.get_client()
            response = await client.post(
                f"{self.base_url}/events/{event_id}/signup",
                json=team_data,
                headers=self.get_headers()
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            return {"error": str(e)}
    
    async def create_event(self, event_data: Dict[str, Any]) -> Dict[str, Any]:
        """Создает новое событие/игру"""
        try:
            client = await self.get_client()
            response = await client.post(
                f"{self.base_url}/events/",
                json=event_data,
                headers=self.get_headers()
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            return {"error": str(e)}
    
    async def close(self):
        """Fecha a conexão do cliente HTTP"""
        if self.client:
            await self.client.aclose()
    
    async def get(self, endpoint: str, headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """Универсальный GET запрос"""
        try:
            client = await self.get_client()
            if headers is None:
                headers = self.get_headers()
            response = await client.get(
                f"{self.base_url}{endpoint}" if not endpoint.startswith("http") else endpoint,
                headers=headers
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            return {"error": str(e)}
    
    async def post(self, endpoint: str, json: Dict[str, Any] = None, headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """Универсальный POST запрос"""
        try:
            client = await self.get_client()
            if headers is None:
                headers = self.get_headers()
            response = await client.post(
                f"{self.base_url}{endpoint}" if not endpoint.startswith("http") else endpoint,
                json=json,
                headers=headers
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            return {"error": str(e)}

# Instância global do cliente
api_client = APIClient()
