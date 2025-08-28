# ====== Explicação dos imports ====== 
    # FastAPI → Classe principal para criar a aplicação.
    # HTTPException → Usada para lançar erros (ex: 404 Not Found).
    # status → Contém códigos HTTP prontos (200, 201, 404...).
    # Response → Permite personalizar respostas HTTP.
    # Depends → Injeta dependências em endpoints (ex: conexão com banco).
    # Models → Importa o modelo de dados para validar e tipar os personagens.
    # Optional → Indica que um parâmetro pode ser opcional.
    # Any → Aceita qualquer tipo de dado.
    # Routes → Importa rotas organizadas em outros arquivos
    # Requests → Biblioteca para fazer requisições HTTP externas
from fastapi import FastAPI, HTTPException, status, Response, Depends
from models import PersonagensToyStory
from typing import Optional, Any
from routes import curso_router, usuario_router
import requests

# Criação da aplicação - Instancia a aplicação adicionando metadados (título, versão e descrição)
app = FastAPI(title="API dos personagens de Toy Story - DS18", version="0.0.1", description="API feita com a DS18 para aprender FastAPI")

# Rotas externas que foram definidas em outros arquivos
app.include_router(curso_router.router, tags=["Cursos"])    # As tags ajudam a organizar a documentação '/docs'
app.include_router(usuario_router.router, tags=["Usuários"])

# Utilizando API externa
@app.get("/pokemon/{name}")    # @ - Decorator: registra uma rota HTTP GET em /pokemon/<algum_nome>
def get_pokemon(name: str):    # Função que atende a rota; 'name' é o parâmetro de caminho
    response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{name}")    # Chamada HTTP síncrona usando 'requests' para consultar a PokeAPI
    
    # Caso o pokemon exista, o código retorna o json vindo da PokeAPI
    if response.status_code == 200:
        return response.json()
    return{"Message": "Pokemon not found"}    # Caso não exista, retorna a mensagem de erro

# Simulação de um banco de dados  (é usada como dependência com o Depends)
def fake_db():
    try:
        print("Conectando com o banco")
    finally:
        print("Fechando o banco")

# "Dados em memória" - Diconário que guarda os personagens como se fosse um banco de dados
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

# Endpoints
@app.get("/")    # Rota raíz 
async def raiz():
    return {"Mensagem": "Deu certo"}    # retorna mensagem de confirmação

@app.get("/personagens")    
async def get_personagens(db: Any = Depends(fake_db)):    # 'Depends(fake_db) executa a função 'fake_db()' sempre que esse endpoint for chamado 
    return personagens    # Retorna todos os personagens

# Retorna um personagem específico pelo id 
@app.get("/personagens/{personagem_id}")    
async def get_personagem(personagem_id: int):
    try:
        personagem = personagens[personagem_id]
        return personagem
    except KeyError:    # Caso o personagem não exista, retorna o erro 404
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Personagem não encontrado")

# Cria um novo personagem
@app.post("/personagens", status_code=status.HTTP_201_CREATED)    # Registra uma rota HTTP POST no caminho /personagens.
async def post_personagem(personagem: Optional[PersonagensToyStory] = None):    
    next_id = len(personagens) + 1    # Calcula um novo ID simples contando quantos itens existem no dicionário personagens e somando 1
    personagens[next_id] = personagem    # Insere no dicionário personagens
    del personagem.id
    return personagem

# Atualiza um personagem existente pelo id
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
    