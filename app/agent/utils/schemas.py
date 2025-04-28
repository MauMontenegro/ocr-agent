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
    tank_names: List[str] =Field(description="Lista de Nombres de tanques de gasolina")
    volumen: List[str] = Field(description="Lista de Volúmenes del tanques de gasolina")
    tc_combusti: List[str]  
    vacio_100: List[str]  
    altura:List[str]
    volumen_agua: List[str] = Field(description="Lista de Volúmenes de agua")
    temperatura: List[str] = Field(description="Lista de Temperaturas de tanques")

class TicketItem(BaseModel):
    product_name: str = Field(description="Nombre del producto comprado")
    quantity: int = Field(description="Cantidad comprada del producto")
    price: float = Field(description="Precio del producto comprado")
    
class TicketReceipt(BaseModel):
    store: str = Field(description="Nombre de tienda Oxxo")
    date: str = Field(description="Fecha de compra")
    time: str = Field(description="Hora de Compra")
    items: List[TicketItem]
    total: float = Field(description="Precios total de los productos comprados")
    payment_method: str = Field(description="Método de pago")
    payment_amount: float = Field(description="Cantidad pagada")
    change: float = Field(description="Cambio devuelto")

class EdenredReceipt(BaseModel):
    terminal : str = Field(description="Nombre de la terminal en donde")
    terminal_id: str = Field(description="Identificador de la terminal")
    date : str = Field(description=" Fecha de Compra")
    hour: str = Field(description="Hora de compra")
    auth_number: str =Field(description="Número de autorización")
    poduct : str = Field(description="Nombre del producto comprado")
    liters : str = Field(description="Total litros del producto comprado")
    unit_price : str = Field(description="Precio unitario del producto")
    importe : str = Field(description="Importe")
    discount : str = Field(description="Descuento del producto")
    total : str = Field(description="total de compra")

class DinamicaFacebook(BaseModel):
    date: str = Field(description="Fecha de compra")
    address: str = Field(description="Lugar de compra")
    station: str = Field(description="Sucursal de compra")
    total: str = Field(description="Pago total")
    quantity: str = Field(description="Cantidad de litros comprados")

class userQuery(BaseModel):
    user_query:str
    user_id: str
