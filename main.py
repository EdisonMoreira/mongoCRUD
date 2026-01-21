from fastapi import FastAPI, Depends, Request, Form 
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from uuid import uuid4

# Importações originais mantidas

# --- ROTA DE CRIAÇÃO CORRIGIDA --- 


from schemas.user import UserCreate, UserResponse
from domain.user import User
from persistence.repository import UserRepository
from persistence.mongo.user_repo import MongoUserRepository

app = FastAPI()

# Configuração do Jinja2
# Certifique-se de criar uma pasta chamada 'templates' no mesmo nível do main.py
templates = Jinja2Templates(directory="templates")

def get_user_repo() -> UserRepository:
    return MongoUserRepository()

# --- ROTAS DE INTERFACE (HTML/JINJA2) ---


@app.get("/", response_class=HTMLResponse)
async def list_users_view(
    request: Request, 
    repo: UserRepository = Depends(get_user_repo)
):
    """
    Rota para renderizar a página principal com a lista de usuários.
    O objeto 'u' aqui conterá campos extras se estiverem no banco.
    """
    users = await repo.list()
    return templates.TemplateResponse(
        "index.html", 
        {"request": request, "users": users}
    )

# --- ROTAS DE API (JSON) ORIGINAIS ---

@app.get("/api/users", response_model=list[UserResponse])
async def list_users_api(
    repo: UserRepository = Depends(get_user_repo)
):
    users = await repo.list()
    return [
        UserResponse(
            id=str(u.id),
            name=u.name,
            email=u.email,
            released=u.released,
            year=u.year
        )
        for u in users
    ]

@app.get("/create", response_class=HTMLResponse)
async def create_user_form(request: Request):
    return templates.TemplateResponse("create.html", {"request": request})


@app.post("/api/users", response_model=UserResponse)
async def create_user_api(

    # 2. Defina cada campo com Form(...) para ler do HTML
    name: str = Form(...),
    email: str = Form(...),
    released: str = Form(...), # Recebemos como string e o Pydantic converte depois
    year: int = Form(...),

    repo: UserRepository = Depends(get_user_repo)
):
    # 1. Validar e converter dados usando o seu Schema (UserCreate)
    # O Pydantic vai transformar a string 'released' numa data real aqui

    data = UserCreate(name=name, email=email, released=released, year=year)

# 2. Criar o objeto de Domínio (User)

    user = User(
            id=uuid4(),
            name=data.name,
            email=data.email,
            released=data.released,
            year=data.year
    )
    
    await repo.create(user)

    # 4. (Melhoria de UX) Em vez de devolver JSON, redirecionamos o navegador para a lista
    # Se preferir JSON, mantenha o return anterior
    return RedirectResponse(url="/", status_code=303)
