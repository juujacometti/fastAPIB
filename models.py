from typing import Optional

#Pega o modelo por herança
from pydantic import BaseModel

#Pega tudo que o absemodel tem
class PersonagensToyStory(BaseModel):
    
    #Determino o objeto e os tipos dos seus atributos
    id: Optional[int] = None
    nome: str
    dono: str
    tamanho: str
    foto: str
    frase: str