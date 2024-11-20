import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from math import ceil
from requests import Response
from requests.exceptions import HTTPError
from requests.sessions import Session


URL: str = r"https://api.vendas.gpa.digital/pa/search/category-page"

CATEGORIAS: list[str] = [
    "alimentos",
    "beleza-e-perfumaria",
    "bebidas",
    "bebidas-alcoolicas",
    "limpeza",
    "cuidados-pessoais"
]

REQUEST_HEADERS: dict[str, str] = {
    'Accept': 'application/json',
    'Content-Type': 'application/json'
    }

REQUEST_PAYLOAD: dict[str, str] = {
    'customerPlus': True,
    'department': "ecom",
    'multiCategory': None,
    'page': 1,
    'partner': "linx",
    'resultsPerPage': 100,
    'sortBy': "relevance",
    'storeId': 461
}

produtos_por_categoria: dict[list[dict[str, str]]] = {categoria: [] for categoria in CATEGORIAS}


def get_ids() -> dict[list[str]]:
    ids_por_categoria: dict[list[str]] = {categoria: [] for categoria in CATEGORIAS}
    
    for categoria, produtos in produtos_por_categoria.items():
        for produto in produtos:
            ids_por_categoria[categoria].append(produto['id'])
        
    return ids_por_categoria


def get_produtos(session: Session, payload: dict[str, str]) -> list[dict[str, str]]:
    response = session.post(URL, headers=REQUEST_HEADERS, data=json.dumps(payload))
    return list(response.json()['products'])


def get_paginas_categoria(requisicao: Response) -> int:
    return ceil(requisicao.json()['totalProducts'] / REQUEST_PAYLOAD['resultsPerPage'])


def get_payload(categoria: str = None, pagina: int = None) -> dict[str, str]:
    if categoria and pagina:
        return {**REQUEST_PAYLOAD, 'multiCategory': categoria, 'page': pagina}
    
    return {**REQUEST_PAYLOAD, 'multiCategory': categoria}


def requisicao(session: Session, categoria: str) -> Response:
    return session.post(
            url = URL, 
            headers = REQUEST_HEADERS, 
            data = json.dumps(get_payload(categoria))
        )
    

def main() -> None:
    with Session() as session:
        for categoria in CATEGORIAS:
            try:
                r: Response = requisicao(session, categoria)
                r.raise_for_status()
            except HTTPError: 
                continue
            else:
                futures: list[ThreadPoolExecutor] = []
                with ThreadPoolExecutor(max_workers = 5) as executor:
                    for pagina in range(1, get_paginas_categoria(r) + 1):
                        futures.append(executor.submit(get_produtos, session, get_payload(categoria, pagina)))

                    for future in as_completed(futures):
                        produtos_por_categoria[categoria].extend(future.result())
    return get_ids()
    
    
if __name__ == '__main__':
    main()