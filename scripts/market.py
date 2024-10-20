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
        
    def show(self) -> Image:
        image: Image = Image.open(BytesIO(requests.get(fr"{self.image}").content))
        image.show() # Show the image
        return image

class Market:
    def __init__(self, loc: str = r'.\data\produtos.csv'):
        self.df = pd.read_csv(loc, sep='|', encoding='utf-8')
        
        self.products: dict = {}
        for idx, row in self.df.iterrows():
            self.products[row['id']] = Produto(row)
        
    def random(self, ignore_case: list[Produto | int | str] = []) -> int:
        available: list[int] = [
            key for key, value in self.products.items() 
            if (key not in ignore_case) or (value not in ignore_case)
        ]
        product: Produto = self.products[random.choice(available)]
        return product

if __name__ == '__main__':
    m = Market()
    print(m.random())