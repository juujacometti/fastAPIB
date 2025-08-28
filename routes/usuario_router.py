from fastapi import APIRouter

router = APIRouter()

@router.get("/api/vi/usuarios")
async def get_usuarios():
    return{"info": "Todos os usuarios"}