
use session_db;

print("\n=== [INÍCIO DA EXECUÇÃO DAS CONSULTAS DO RELATÓRIO] ===\n");

db.user_sessions.insertOne({
  "_id": "sessao:token_uige_2026_x",
  "utilizador_id": 88123,
  "token_sessao": "7fa12b9c-4f12-426b-838c-04334d223fff",
  "status": "Ativo",
  "criado_em": new Date(),
  "ultima_atividade": new Date(),
  "carrinho": {
    "total_itens": 0,
    "valor_total": 0.0,
    "itens": []
  }
});



print("\n-> Executando Query 2: Adicionando de forma atómica um item ao carrinho...");
db.user_sessions.updateOne(
  { "_id": "sessao:token_uige_2026_x" },
  { 
    $push: { 
      "carrinho.itens": { 
        "sku": "PROD-LAP-101", 
        "nome": "Portátil Lenovo ThinkPad X1 Carbon", 
        "quantidade": 1, 
        "preco_unitario": 1249.99 
      } 
    },
    $set: { "ultima_atividade": new Date() },
    $inc: { "carrinho.total_itens": 1, "carrinho.valor_total": 1249.99 }
  }
);


print("\n-> Executando Query 3: Agregação estatística de carrinhos Abandonados...");
db.user_sessions.aggregate([
  { $match: { "status": "Abandonado" } },
  { $group: {
      "_id": "$status",
      "total_carrinhos_abandonados": { $sum: 1 },
      "capital_total_retido": { $sum: "$carrinho.valor_total" },
      "ticket_medio_abandonado": { $avg: "$carrinho.valor_total" }
  }}
]);


print("\n-> Executando Query 4: Atualização em massa de controlo sazonal (Sessões Inativas)...");
var dataLimite = new Date();
dataLimite.setDate(dataLimite.getDate() - 2); // 2 dias atrás

var resultadoUpdate = db.user_sessions.updateMany(
  { "status": "Inativo", "ultima_atividade": { $lt: dataLimite } },
  { $set: { "status": "Abandonado" } }
);
print("Resultado da atualização em lote: matched = " + resultadoUpdate.matchedCount + ", modified = " + resultadoUpdate.modifiedCount);



print("\n-> Executando Query 5: Pesquisa de alta performance orientada pelo índice único...");
db.user_sessions.find({ "token_sessao": "7fa12b9c-4f12-426b-838c-04334d223fff" }).pretty();

print("\n=== [FIM DA EXECUÇÃO DAS CONSULTAS COM SUCESSO] ===\n");