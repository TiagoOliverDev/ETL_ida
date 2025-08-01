CREATE TABLE dim_grupo_economico (
    id SERIAL PRIMARY KEY,
    nome TEXT UNIQUE NOT NULL
);

CREATE TABLE dim_servico (
    id SERIAL PRIMARY KEY,
    nome TEXT UNIQUE NOT NULL
);

CREATE TABLE dim_tempo (
    id SERIAL PRIMARY KEY,
    data_ref DATE NOT NULL,
    ano INT,
    mes INT
);

CREATE TABLE fato_ida (
    id SERIAL PRIMARY KEY,
    id_grupo_economico INT REFERENCES dim_grupo_economico(id),
    id_servico INT REFERENCES dim_servico(id),
    id_tempo INT REFERENCES dim_tempo(id),
    taxa_resolucao_5dias NUMERIC,
    total_reclamacoes INT
);
