import pymongo
import random
import uuid
from datetime import datetime, timedelta
from faker import Faker


fake = Faker(['pt_PT'])



print("A estabelecer ligação segura com o cluster NoSQL (Porta 28017)...")
client = pymongo.MongoClient("mongodb://localhost:28017/?directConnection=true")
db = client["session_db"]
collection = db["user_sessions"]

print("Ligação estabelecida! A iniciar o povoamento massivo de 100.000 sessões de carrinhos...")

produtos_pool = [
    {"sku": "PROD-LAP-101", "nome": "Portátil Lenovo ThinkPad X1 Carbon", "preco": 1249.99, "cat": "Computadores"},
    {"sku": "PROD-MNT-102", "nome": "Monitor Gaming ASUS ROG 27'' Curved", "preco": 349.50, "cat": "Monitores"},
    {"sku": "PROD-KEY-103", "nome": "Teclado Mecânico Logitech G Pro X", "preco": 129.90, "cat": "Periféricos"},
    {"sku": "PROD-MSE-104", "nome": "Rato Sem Fios Razer DeathAdder V3", "preco": 85.00, "cat": "Periféricos"},
    {"sku": "PROD-CHR-105", "nome": "Cadeira Gaming Alpha Gamer Vega", "preco": 199.99, "cat": "Escritório"},
    {"sku": "PROD-HDD-106", "nome": "Disco SSD Externo Kingston 1TB NVMe", "preco": 79.99, "cat": "Armazenamento"}
]

batch_size = 5000
buffer = []

for i in range(1, 100001):
    token = str(uuid.uuid4())
    utilizador_id = random.randint(10000, 99999)
    status = random.choice(["Ativo", "Inativo", "Abandonado"])
   
    data_criacao = fake.date_time_between(start_date='-5d', end_date='now')
    data_atividade = data_criacao + timedelta(minutes=random.randint(5, 120))
    
    
    num_itens = random.randint(1, 4)
    itens_carrinho = []
    valor_total = 0.0
    
  
    produtos_escolhidos = random.sample(produtos_pool, num_itens)
    for p in produtos_escolhidos:
        qtd = random.randint(1, 2)
        subtotal = round(p["preco"] * qtd, 2)
        valor_total += subtotal
        
        itens_carrinho.append({
            "sku": p["sku"],
            "nome": p["nome"],
            "quantidade": qtd,
            "preco_unitario": p["preco"]
        })
        

    sessao_doc = {
        "_id": f"sessao:token_{token[:8]}_{i}",
        "utilizador_id": utilizador_id,
        "token_sessao": token,
        "status": status,
        "criado_em": data_criacao,
        "ultima_atividade": data_atividade,
        "carrinho": {
            "total_itens": len(itens_carrinho),
            "valor_total": round(valor_total, 2),
            "itens": itens_carrinho
        }
    }
    
    buffer.append(sessao_doc)
    
    
    if len(buffer) == batch_size:
        collection.insert_many(buffer)
        buffer = []
        print(f"Progresso: {i} / 100.000 documentos indexados com sucesso...")


if buffer:
    collection.insert_many(buffer)

print("Criação de índices de performance e otimização operacional...")

collection.create_index([("token_sessao", 1)], unique=True)
collection.create_index([("status", 1), ("ultima_atividade", -1)])

print("\nPovoamento concluído com absoluto sucesso!")
print(f"Total na base de dados: {collection.count_documents({})} registos.")