from typing import List, Dict, Any, TypedDict, Optional, Union, Literal
from pydantic import BaseModel, Field

# Define your schemas as Pydantic models
class TankItem(BaseModel):
    Tanque: str = Field(description="Nombre del tanque de gasolina")
    VOLUMEN: int = Field(description="Volúmen del tanque de gasolina")
    TC_COMBUSTI: int
    VACIO_100: int = Field(..., alias="100% VACIO")
    ALTURA: float     
    VOLUMEN_AGUA: int = Field(..., alias="VOLUMEN AGUA")
    TEMPERATURA: float = Field(description="Temperatura del tanque")

class TankResponse(BaseModel):    
    tank_names: List[str] =Field(description="Nombres de tanques de gasolina")
    volumen: List[str] = Field(description="Volúmen del tanques de gasolina")
    tc_combusti: List[str]  
    vacio_100: List[str]  
    altura:List[str]
    volumen_agua: List[str] = Field(description="Volúmen de agua")
    temperatura: List[str] = Field(description="Temperatura del tanques")

class OxxoItem(BaseModel):
    product_name: str = Field(description="Nombre del producto comprado")
    quantity: int = Field(description="Cantidad comprada del producto")
    price: float = Field(description="Precio del producto comprado")
    
class OxxoReceipt(BaseModel):
    store: str = Field(description="Nombre de tienda Oxxo")
    date: str = Field(description="Fecha de compra")
    time: str = Field(description="Hora de Compra")
    items: List[OxxoItem]
    total: float = Field(description="Precios total de los productos comprados")
    payment_method: str = Field(description="Método de pago")
    payment_amount: float = Field(description="Cantidad pagada")
    change: float = Field(description="Cambio devuelto")

class userQuery(BaseModel):
    user_query:str
    user_id: str
