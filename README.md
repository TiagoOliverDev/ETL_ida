# Desafio Técnico - Índice de Desempenho no Atendimento (IDA)

Este projeto realiza a extração, transformação e carga (ETL) dos dados públicos de IDA das operadoras brasileiras, modelando-os em um Data Mart (modelo estrela) com PostgreSQL e criando uma view analítica com taxa de variação média.

## Tecnologias
- Python 3.11.12
- PostgreSQL 17.5
- Docker Compose

## Como executar
```bash
cp .env.example .env
docker-compose up --build
