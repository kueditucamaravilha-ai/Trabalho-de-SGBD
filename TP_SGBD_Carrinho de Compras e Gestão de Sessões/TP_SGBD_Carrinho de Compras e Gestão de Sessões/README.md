Este trabalho foi desenvolvido para Avalição na cadeira de SGBD II.
O trabalho contou com o tema Conceção e Implementação de uma Camada de Persistência 
Poliglota para um Ecossistema de E-commerce de Alta Escala. 
Teve como subdominio Carrinho de Compras e Gestão de Sessões.

Estrutura em Arvore.

TP2_SGBD_ecommerce_session_management/
|
|---docker_sessao/
|          |----docker-compose.yml    # Configuração do Cluster de 3 nós MongoDB
|
|---Script_sessao/
|         |---povoamento_sesso.py  # Script do python para o povoamento da base de dados 
|         |---queries_sessao.js   # Script js para as consultas 
|
|---README.md # Manuel de instalação.

Justificativa da escolha do subdomínio.

O subdomínio Carrinho de Compras e Gestão de Sessões É um  sistema de altíssima disponibilidade e 
baixa latência para gerir o estado do carrinho de compras de milhões de utilizadores 
simultâneos, garantindo que não há perda de dados mesmo em caso de falha de nós. 

GUIA PARA A EXECUÇÃO DO PREOJECTO.
Para iniciar o cluster 
cd docker_sessao
docker compose up -d

Ativar a replicar .
docker exec -it mongo_sessao1 mongosh --port 27017 --eval "rs.initiate({_id: 'rs_sessao', members: [{_id: 0, host: 'mongo_sessao1:27017'}, {_id: 1, host: 'mongo_sessao2:27017'}, {_id: 2, host: 'mongo_sessao3:27017'}]})"
 Para fazer o povoamento do Scrit
 cd ..
python Script_sessao/povoamento_sessao.py


Para a execução das 5 consultas. 
Get-Content "./Script_sessao/queries_sessao.js" -Raw | docker exec -i mongo_sessao1 mongosh --port 27017

Para as consultas manual na base de dados 
docker exec -it mongo_sessao1 mongosh --port 27017
Dentro do console interativo, execute:
use session_db;
db.user_sessions.findOne();