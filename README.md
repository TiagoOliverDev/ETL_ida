# ETL IDA - Pipeline de Dados do Índice de Desempenho no Atendimento

[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Airflow DAG](https://img.shields.io/badge/Airflow-DAG-blue)](http://localhost:8080)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-✔️-blue)](https://www.postgresql.org/)


Pipeline ETL para extração, transformação e carga dos dados do Índice de Desempenho no Atendimento (IDA) das operadoras de telecomunicações, usando Python, Apache Airflow e PostgreSQL.

---

## 📚 Visão Geral

- **Extração: Dados extraídos de arquivos ODS com informações de IDA.**
- **Transformação: Normalização, limpeza e tratamento dos dados com Pandas.** 
- **Carga: Inserção dos dados transformados em um banco PostgreSQL estruturado com modelo estrela (fato + dimensões).** 
- **Orquestração: Apache Airflow gerencia a execução diária do pipeline via DAG.** 

---

## 🗂️ Estrutura do Projeto

```bash
ETL_ida/                                              # Raiz do projeto ETL para IDA
├── config/                                           # Configurações globais do projeto
│   └── settings.py                                   # Parâmetros, paths e variáveis fixas
├── dags/                                             # DAGs do Airflow (pipelines)
│     └── etl_ida_dag.py                              # Definição da DAG principal de ETL
├── data/                                             # Diretórios para dados
│   ├── raw/                                          # Dados brutos coletados (ODS, CSV, etc)
│   └── processed/                                    # Dados transformados prontos para carga/análise
├── logs/                                             # Logs gerados em execução para auditoria/debug
├── plugins/                                          # Plugins e extensões personalizadas do Airflow
├── src/                                              # Código fonte principal
│   ├── db/                                           # Módulo de banco de dados
│   │   └── repositories/                             # Repositórios para acesso e manipulação das tabelas
│   │       └── base.py                               # Classe base de repositório genérico
│   │       └── dim_grupo_economico.py                # Repositório da dimensão grupo econômico
│   │       └── dim_servico.py                        # Repositório da dimensão serviço
│   │       └── dim_tempo.py                          # Repositório da dimensão tempo
│   │       └── dim_variavel.py                       # Repositório da dimensão variável
│   │       └── fato_ida.py                           # Repositório da tabela fato
│   │   └── sql/                                      # Scripts SQL brutos
│   │       └── create_tables.sql                     # Script de criação das tabelas no banco
│   │   └── create_tables.py                          # Script Python para criação das tabelas via SQLAlchemy (opcional)
│   │   └── database.py                               # Configuração de conexão e engine do banco
│   │   └── models.py                                 # Modelos ORM (SQLAlchemy) das tabelas
│   ├── etl/                                          # Pipeline ETL principal
│   │   ├── extract.py                                # Código para extrair dados da fonte
│   │   ├── load.py                                   # Código para carregar dados no banco
│   │   └── transform.py                              # Código para transformar e limpar os dados
│   ├── utils/                                        # Utilitários gerais
│   │   └── logger.py                                 # Configuração e inicialização do logger
│   │   └── utils.py                                  # Funções utilitárias variadas
│   └── main.py                                       # Script principal para executar o ETL localmente (batch)
├── tests/                                            # Testes automatizados do projeto
├── .env.example                                      # Exemplo de arquivo de variáveis ambiente para configurar o projeto
├── .gitignore                                        # Arquivos e pastas ignorados pelo git
├── .dockerignore                                     # Arquivos e pastas ignorados na construção da imagem Docker
├── Dockerfile-airflow                                # Dockerfile customizado para o container Airflow
├── docker-compose.yml                                # Orquestração Docker (Airflow, bancos, ETL, etc)
├── Dockerfile                                        # Dockerfile base para o ETL (Python, dependências)
├── requirements.txt                                  # Dependências Python do projeto
└── main_local.py                                     # Script alternativo para execução local do ETL
└── wait-for-postgres.sh                              # Script shell para aguardar o banco estar pronto no container
```

---

## ⚙️ Arquitetura do Processamento de dados

```bash
+----------------+        +---------------------+        +------------------+
| Dados ODS (raw)| -----> | Processamento ETL    | -----> | PostgreSQL (data) |
| (Extrair,      |        | (Transform + Load)  |        | (Modelo Estrela)  |
| Transformar)   |        | via Airflow DAG     |        +------------------+
+----------------+        +---------------------+

```

---

## ⚙️ Configuração do Ambiente

### 1. **Pré-requisitos**

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)
- Python 3.11+ (para execuções locais e testes)

---

### 2. **Clone o Repositório**

```bash
git clone https://github.com/TiagoOliverDev/ETL_ida
cd ETL_ida
```

---

### 3. **Crie o Arquivo `.env`**

Baseie-se no modelo `.env.example`.

---

### 4. **Suba o Ambiente com Docker Compose e aguarde alguns minutos até que tudo seja buildado**

```bash
docker-compose up --build
```

---

### 5. **Ative a DAG no Airflow**

1. Abra seu navegador e acesse a interface web do Airflow: [http://localhost:8080](http://localhost:8080)
2. Faça login usando as credenciais padrão:

    Usuário: admin
    Senha: admin

3. Ative a DAG chamada ida_etl (ou etl_ida_dag.py se aparecer assim na interface):

    Encontre a DAG na lista e clique no botão de chave (toggle) para ativá-la.

4. Configure a conexão com o banco de dados no Airflow:

    No menu superior, passe o mouse sobre Admin e selecione Connections.

    Clique no botão azul + para adicionar uma nova conexão.

    Preencha os campos da seguinte forma:

        ```
            Connection Id: local_postgres_conn

            Connection Type: Postgres

            Host: etl-db

            Schema: etl_db

            Login: etl_user

            Password: etl_pass

            Port: 5432
        ```


    Clique em Save para salvar a conexão e depois volte para a página inicial do Airflow.


5. Execute a DAG manualmente:

    Ao lado direito da DAG ida_etl, no menu Actions Selecione Trigger DAG (ícone de seta para a direita).

    Aguarde a execução ser concluída — o status ficará verde indicando sucesso.

6. Após processo finalizado e projeto rodando via docker você poderar acessar o banco localhost via dbeaver e consultar os dados nas tabelas e na view vw_taxa_variacao_ida

    ```
    dim_variavel

    dim_tempo

    dim_grupo_economico

    dim_servico

    fato_indicador

    vw_taxa_variacao_ida

    ```

---

## 🛠️ Execução Manual (fora do Airflow)

```bash
python main_local.py
```

---


## 📝 Observações

- O projeto inteiro roda via docker-compose mas também é possível rodar local (python main_local.py) após buildar as imagens 

- Em src\db\sql\create_tables.sql você encontra o SQL (usando COMMENT ON) que o projeto usa automaticamente após criar o banco para gerar as tabelas e a view

---

## 📚 Licença

Este projeto é open-source e está sob a licença [MIT](LICENSE).

---

## 👨‍💻 Desenvolvido por

**Tiago Oliveira**  
Analista desenvolvedor e Engenheiro de dados em formação

- 💼 [LinkedIn](https://www.linkedin.com/in/tiago-oliveira-49a2a6205/)
- 💻 [GitHub](https://github.com/TiagoOliverDev)