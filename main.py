from fastapi import FastAPI, HTTPException, status, Response, Depends
from models import PersonagensToyStory
from typing import Optional, Any
from routes import curso_router, usuario_router
import requests

app = FastAPI(title="API dos personagens de Toy Story - DS18", version="0.0.1", description="API feita com a DS18 para aprender FastAPI")

app.include_router(curso_router.router, tags=["Cursos"])
app.include_router(usuario_router.router, tags=["Usuários"])

# Utilizando API externa
@app.get("/pokemon/{name}")
def get_pokemon(name: str):
    response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{name}")
    if response.status_code == 200:
        return response.json()
    return{"Message": "Pokemon not found"}

def fake_db():
    try:
        print("Conectando com o banco")
    finally:
        print("Fechando o banco")

personagens = {
    1: {
        "nome": "Woody",
        "dono": "Andy",
        "tamanho": "Pequeno",
        "foto": "https://static.wikia.nocookie.net/herois/images/e/ed/Woody.6bdcd353.webp/revision/latest?cb=20250215000931&path-prefix=pt-br",
    },
    2: {
       "nome": "Buzz Lighter",
        "dono": "Bonnie",
        "tamanho": "Pequeno",
        "foto": "https://lumiere-a.akamaihd.net/v1/images/b_toystory_characterbanner_buzz_mobile_gradient_v2_14ddf7ec.jpeg?region=0,0,640,480" 
    }
}

# @ - É um decorator. 
@app.get("/")
async def raiz():
    return {"Mensagem": "Deu certo"}

@app.get("/personagens")
async def get_personagens(db: Any = Depends(fake_db)):
    return personagens

@app.get("/personagens/{personagem_id}")
async def get_personagem(personagem_id: int):
    try:
        personagem = personagens[personagem_id]
        return personagem
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Personagem não encontrado")
    
@app.post("/personagens", status_code=status.HTTP_201_CREATED)
async def post_personagem(personagem: Optional[PersonagensToyStory] = None):
    next_id = len(personagens) + 1
    personagens[next_id] = personagem
    del personagem.id
    return personagem

@app.put("/personagens/{personagem_id}", status_code=status.HTTP_202_ACCEPTED)
async def put_personagem(personagem_id:int, personagem: PersonagensToyStory):
    if personagem_id in personagens:
        personagens[personagem_id] = personagem
        personagem.id = personagem_id
        del personagem.id
        return personagem
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Personagem não encontrado")
    
@app.delete("/personagens/{personagem_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_personagem(personagem_id: int):
    if personagem_id in personagens:
        del personagens[personagem_id]
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Personagem não encontrado")
    
@app.get("/calcular")
async def calcular(a: int, b: int):
    soma = a + b
    return {"Resultado": soma}



if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", port=8001, log_level="info", reload=True)
    