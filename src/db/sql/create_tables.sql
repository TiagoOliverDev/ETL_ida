CREATE TABLE dim_variavel (
    id_variavel SERIAL PRIMARY KEY,
    nome_variavel VARCHAR(255) NOT NULL
);

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

CREATE TABLE fato_indicador (
    id_fato SERIAL PRIMARY KEY,
    id_tempo INTEGER NOT NULL,
    id_grupo_economico INTEGER NOT NULL,
    id_servico INTEGER NOT NULL,
    id_variavel INTEGER NOT NULL,
    valor FLOAT NOT NULL,
    CONSTRAINT fk_fato_tempo FOREIGN KEY (id_tempo) REFERENCES dim_tempo(id_tempo),
    CONSTRAINT fk_fato_grupo FOREIGN KEY (id_grupo_economico) REFERENCES dim_grupo_economico(id_grupo_economico),
    CONSTRAINT fk_fato_servico FOREIGN KEY (id_servico) REFERENCES dim_servico(id_servico),
    CONSTRAINT fk_fato_variavel FOREIGN KEY (id_variavel) REFERENCES dim_variavel(id_variavel)
);


CREATE OR REPLACE VIEW vw_taxa_variacao_ida AS
WITH indicador_filtrado AS (
  SELECT
    f.id_tempo,
    f.id_grupo_economico,
    f.id_servico,
    f.valor
  FROM fato_indicador f
  JOIN dim_variavel v ON f.id_variavel = v.id_variavel
  WHERE v.id_variavel = 11  -- Taxa de Resolvidas em 5 dias úteis
),

valores_mes AS (
  SELECT
    t.mes_ano,
    g.nome_grupo,
    s.nome_servico,
    AVG(f.valor) AS ida_medio
  FROM indicador_filtrado f
  JOIN dim_tempo t ON f.id_tempo = t.id_tempo
  JOIN dim_grupo_economico g ON f.id_grupo_economico = g.id_grupo_economico
  JOIN dim_servico s ON f.id_servico = s.id_servico
  GROUP BY t.mes_ano, g.nome_grupo, s.nome_servico
),

valores_com_anterior AS (
  SELECT
    vm.mes_ano,
    vm.nome_grupo,
    vm.nome_servico,
    vm.ida_medio,
    LAG(vm.ida_medio) OVER (PARTITION BY vm.nome_grupo, vm.nome_servico ORDER BY vm.mes_ano) AS ida_medio_anterior
  FROM valores_mes vm
),

taxas_variacao AS (
  SELECT
    mes_ano,
    nome_grupo,
    nome_servico,
    CASE 
      WHEN ida_medio_anterior IS NULL THEN NULL
      WHEN ida_medio_anterior = 0 THEN NULL
      ELSE ((ida_medio - ida_medio_anterior) / ida_medio_anterior) * 100
    END AS taxa_variacao
  FROM valores_com_anterior
),

media_mensal AS (
  SELECT
    mes_ano,
    nome_servico,
    AVG(taxa_variacao) AS taxa_variacao_media
  FROM taxas_variacao
  GROUP BY mes_ano, nome_servico
)

SELECT
  m.mes_ano AS mes,
  m.nome_servico AS servico,
  ROUND(m.taxa_variacao_media::numeric, 2) AS taxa_variacao_media,
  ROUND(MAX(CASE WHEN tv.nome_grupo = 'ALGAR' THEN tv.taxa_variacao END)::numeric, 2) AS algar,
  ROUND(MAX(CASE WHEN tv.nome_grupo = 'CLARO' THEN tv.taxa_variacao END)::numeric, 2) AS claro,
  ROUND(MAX(CASE WHEN tv.nome_grupo = 'NEXTEL' THEN tv.taxa_variacao END)::numeric, 2) AS nextel,
  ROUND(MAX(CASE WHEN tv.nome_grupo = 'OI' THEN tv.taxa_variacao END)::numeric, 2) AS oi,
  ROUND(MAX(CASE WHEN tv.nome_grupo = 'SERCOMTEL' THEN tv.taxa_variacao END)::numeric, 2) AS sercomtel,
  ROUND(MAX(CASE WHEN tv.nome_grupo = 'TIM' THEN tv.taxa_variacao END)::numeric, 2) AS tim,
  ROUND(MAX(CASE WHEN tv.nome_grupo = 'VIVO' THEN tv.taxa_variacao END)::numeric, 2) AS vivo,
  ROUND(MAX(CASE WHEN tv.nome_grupo = 'EMBRATEL' THEN tv.taxa_variacao END)::numeric, 2) AS embratel,
  ROUND(MAX(CASE WHEN tv.nome_grupo = 'NET' THEN tv.taxa_variacao END)::numeric, 2) AS net,
  ROUND(MAX(CASE WHEN tv.nome_grupo = 'SKY' THEN tv.taxa_variacao END)::numeric, 2) AS sky
FROM media_mensal m
LEFT JOIN taxas_variacao tv 
  ON tv.mes_ano = m.mes_ano 
  AND tv.nome_servico = m.nome_servico
GROUP BY m.mes_ano, m.nome_servico, m.taxa_variacao_media
ORDER BY m.mes_ano, m.nome_servico;


-- Comentários para as tabelas e colunas

COMMENT ON TABLE dim_variavel IS 'Dimensão que armazena as variáveis dos indicadores.';
COMMENT ON COLUMN dim_variavel.id_variavel IS 'Identificador único da variável.';
COMMENT ON COLUMN dim_variavel.nome_variavel IS 'Nome descritivo da variável do indicador.';

COMMENT ON TABLE dim_tempo IS 'Dimensão temporal, com ano, mês e mês/ano formatado.';
COMMENT ON COLUMN dim_tempo.id_tempo IS 'Identificador único da dimensão tempo.';
COMMENT ON COLUMN dim_tempo.ano IS 'Ano da data.';
COMMENT ON COLUMN dim_tempo.mes IS 'Mês da data.';
COMMENT ON COLUMN dim_tempo.mes_ano IS 'Ano e mês no formato YYYY-MM para agrupamento mensal.';

COMMENT ON TABLE dim_grupo_economico IS 'Dimensão que representa os grupos econômicos das operadoras.';
COMMENT ON COLUMN dim_grupo_economico.id_grupo_economico IS 'Identificador único do grupo econômico.';
COMMENT ON COLUMN dim_grupo_economico.nome_grupo IS 'Nome do grupo econômico.';

COMMENT ON TABLE dim_servico IS 'Dimensão dos serviços analisados.';
COMMENT ON COLUMN dim_servico.id_servico IS 'Identificador único do serviço.';
COMMENT ON COLUMN dim_servico.nome_servico IS 'Nome do serviço.';

COMMENT ON TABLE fato_indicador IS 'Tabela fato que armazena os valores dos indicadores por tempo, grupo, serviço e variável.';
COMMENT ON COLUMN fato_indicador.id_fato IS 'Identificador único da linha da tabela fato.';
COMMENT ON COLUMN fato_indicador.id_tempo IS 'Chave estrangeira para a dimensão tempo.';
COMMENT ON COLUMN fato_indicador.id_grupo_economico IS 'Chave estrangeira para a dimensão grupo econômico.';
COMMENT ON COLUMN fato_indicador.id_servico IS 'Chave estrangeira para a dimensão serviço.';
COMMENT ON COLUMN fato_indicador.id_variavel IS 'Chave estrangeira para a dimensão variável.';
COMMENT ON COLUMN fato_indicador.valor IS 'Valor do indicador para a combinação das dimensões.';

COMMENT ON VIEW vw_taxa_variacao_ida IS 
'View que calcula a taxa de variação mensal média do indicador IDA (Índice de Desempenho no Atendimento) e detalha a variação por grupo econômico. 
A taxa é calculada com base na variável 11, que representa a taxa de resolvidas em 5 dias úteis.';