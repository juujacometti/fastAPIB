from fastapi import APIRouter

router = APIRouter()

@router.get("/api/vi/cursos")
async def get_cusos():
    return{"info": "Todos os cursos"}