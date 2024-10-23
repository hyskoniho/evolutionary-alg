import pandas as pd
import random
import requests
from PIL import Image
from io import BytesIO

class Produto:
    def __init__(self, info: dict):
        # Attributes:
        self.id: int = info['id']
        self.name: str = info['nome']
        self.sku: str = info['sku']
        self.price: float = info['preco']
        self.image: str = info['imagem']
        self.brand: str = info['marca']
        self.category: str = info['categoria']
        self.description: str = info['descricao']
        self.weight: float = info['pesoBruto']
        self.height: float = info['alturaProduto']
        self.width: float = info['larguraProduto']
        self.depth: float = info['profundidadeProduto']
        
    def __eq__(self, other: 'Produto') -> bool:
        return self.id == other.id
    
    def __str__(self) -> str:
        return f"Product Info\n{''.join([f'{key}: {var}\n' for key, var in vars(self).items()])}"
    
    def __repr__(self) -> str:
        return f"<Produto(id={self.id}>"
        
    def show(self, popup: bool = True) -> Image:
        image: Image = Image.open(BytesIO(requests.get(fr"{self.image}").content))
        if popup: image.show()
        return image

class Market:
    def __init__(self, loc: str = r'.\data\produtos.csv'):
        self.df = pd.read_csv(loc, sep='|', encoding='utf-8')
        
        self.products: list[Produto | None] = []
        for idx, row in self.df.iterrows():
            self.products.append(Produto(row))
        
    def random(self, ignore_case: list[Produto] = []) -> int:
        available: list[Produto] = [
            p for p in self.products 
            if p not in ignore_case
        ]
        
        product: Produto = random.choice(available)
        return product

if __name__ == '__main__':
    m = Market()
    produto = m.random()
    print(produto)	
    produto.show()	