CREATE TABLE dim_tempo (
    id_tempo SERIAL PRIMARY KEY,
    ano INTEGER NOT NULL,
    mes INTEGER NOT NULL,
    mes_ano VARCHAR(7) NOT NULL
);

CREATE TABLE dim_grupo_economico (
    id_grupo_economico SERIAL PRIMARY KEY,
    nome_grupo VARCHAR(255) NOT NULL
);

CREATE TABLE dim_servico (
    id_servico SERIAL PRIMARY KEY,
    nome_servico VARCHAR(50) NOT NULL
);

CREATE TABLE fato_ida (
    id_fato SERIAL PRIMARY KEY,
    id_tempo INTEGER NOT NULL,
    id_grupo_economico INTEGER NOT NULL,
    id_servico INTEGER NOT NULL,
    valor_ida FLOAT NOT NULL,
    CONSTRAINT fk_fato_ida_tempo FOREIGN KEY (id_tempo) REFERENCES dim_tempo(id_tempo),
    CONSTRAINT fk_fato_ida_grupo_economico FOREIGN KEY (id_grupo_economico) REFERENCES dim_grupo_economico(id_grupo_economico),
    CONSTRAINT fk_fato_ida_servico FOREIGN KEY (id_servico) REFERENCES dim_servico(id_servico)
);


