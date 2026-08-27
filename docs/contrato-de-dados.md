# 📋 Contrato de Dados — Dados Estatísticos do Transporte Aéreo (ANAC)

Documento que define a estrutura, os tipos e as regras de qualidade esperadas para os arquivos da fonte ANAC. Serve como referência para a ingestão (bronze) e como gabarito para a camada de qualidade.

---

## 1. Metadados da fonte

| Propriedade | Valor |
|---|---|
| **Origem** | ANAC — Dados Estatísticos do Transporte Aéreo (Microdados) |
| **Formato** | CSV |
| **Separador** | `;` (ponto e vírgula) |
| **Encoding** | `ISO-8859-1` (latin-1) — **não** é UTF-8 |
| **Separador decimal** | vírgula (`,`) — quando houver decimais |
| **Cabeçalho** | Sim, na primeira linha |
| **Nº de colunas** | 38 |
| **Grão** | Uma linha = agregação por empresa + rota (origem/destino) + natureza + grupo de voo + ano/mês |
| **Particionamento** | `ano=YYYY/mes=MM` |
| **Publicação** | Mensal; base subdividida por ano (2000–presente) |

---

## 2. Dicionário de colunas

Convenção de nomes canônicos: **snake_case**, minúsculas, sem acento, unidades como sufixo (`(KG)` → `_kg`).

Legenda de obrigatoriedade: **Sim** = não pode ser nula; **Não** = nula é aceita; **Condicional** = regra depende de outra coluna (detalhada na Parte 3).

### Empresa

| # | Nome original | Nome canônico | Tipo | Obrigatória | Observação |
|---|---|---|---|---|---|
| 1 | EMPRESA (SIGLA) | empresa_sigla | string | Sim | Chave confiável da empresa (código ICAO) |
| 2 | EMPRESA (NOME) | empresa_nome | string | Sim | Campo sujo: pode conter vírgula, ponto, tamanho variável |
| 3 | EMPRESA (NACIONALIDADE) | empresa_nacionalidade | string | Sim | Domínio: BRASILEIRA / ESTRANGEIRA |

### Tempo

| # | Nome original | Nome canônico | Tipo | Obrigatória | Observação |
|---|---|---|---|---|---|
| 4 | ANO | ano | integer | Sim | Chave de partição; 2000–presente |
| 5 | MÊS | mes | integer | Sim | Chave de partição; domínio 1–12 |

### Aeroporto de origem

| # | Nome original | Nome canônico | Tipo | Obrigatória | Observação |
|---|---|---|---|---|---|
| 6 | AEROPORTO DE ORIGEM (SIGLA) | aeroporto_origem_sigla | string | Sim | Todo voo tem origem física; vazio = erro → quarentena |
| 7 | AEROPORTO DE ORIGEM (NOME) | aeroporto_origem_nome | string | Não | Descritivo |
| 8 | AEROPORTO DE ORIGEM (UF) | aeroporto_origem_uf | string | Condicional | Obrigatória se país = BRASIL; vazia para estrangeiro é esperado |
| 9 | AEROPORTO DE ORIGEM (REGIÃO) | aeroporto_origem_regiao | string | Condicional | Idem UF |
| 10 | AEROPORTO DE ORIGEM (PAÍS) | aeroporto_origem_pais | string | Sim | Necessária para avaliar as regras condicionais |
| 11 | AEROPORTO DE ORIGEM (CONTINENTE) | aeroporto_origem_continente | string | Não | Descritivo |

### Aeroporto de destino

| # | Nome original | Nome canônico | Tipo | Obrigatória | Observação |
|---|---|---|---|---|---|
| 12 | AEROPORTO DE DESTINO (SIGLA) | aeroporto_destino_sigla | string | Sim | Vazio = erro → quarentena |
| 13 | AEROPORTO DE DESTINO (NOME) | aeroporto_destino_nome | string | Não | Descritivo |
| 14 | AEROPORTO DE DESTINO (UF) | aeroporto_destino_uf | string | Condicional | Obrigatória se país = BRASIL |
| 15 | AEROPORTO DE DESTINO (REGIÃO) | aeroporto_destino_regiao | string | Condicional | Idem UF |
| 16 | AEROPORTO DE DESTINO (PAÍS) | aeroporto_destino_pais | string | Sim | Necessária para as regras condicionais |
| 17 | AEROPORTO DE DESTINO (CONTINENTE) | aeroporto_destino_continente | string | Não | Descritivo |

### Classificação do voo

| # | Nome original | Nome canônico | Tipo | Obrigatória | Observação |
|---|---|---|---|---|---|
| 18 | NATUREZA | natureza | string | Sim | Domínio confirmado (2000/2012/2025): DOMÉSTICA / INTERNACIONAL |
| 19 | GRUPO DE VOO | grupo_voo | string | Sim | Domínio confirmado (2000/2012/2025): REGULAR / NÃO REGULAR / IMPRODUTIVO |

### Métricas

Todas não-obrigatórias: métrica vazia é ausência legítima (ex.: voo IMPRODUTIVO sem passageiros/carga), não erro. Tipos numéricos em `double` por segurança contra decimais com vírgula que aparecem em alguns anos (ex.: `horas_voadas` = 2,5 em 2025); apenas contagens (passageiros, decolagens, assentos) são `integer`.

| # | Nome original | Nome canônico | Tipo | Obrigatória | Observação |
|---|---|---|---|---|---|
| 20 | PASSAGEIROS PAGOS | passageiros_pagos | integer | Não | Contagem; zero legítimo |
| 21 | PASSAGEIROS GRÁTIS | passageiros_gratis | integer | Não | Contagem |
| 22 | CARGA PAGA (KG) | carga_paga_kg | double | Não | |
| 23 | CARGA GRÁTIS (KG) | carga_gratis_kg | double | Não | |
| 24 | CORREIO (KG) | correio_kg | double | Não | |
| 25 | ASK | ask | double | Não | Métrica derivada; pode vir vazia |
| 26 | RPK | rpk | double | Não | Métrica derivada |
| 27 | ATK | atk | double | Não | Métrica derivada |
| 28 | RTK | rtk | double | Não | Métrica derivada |
| 29 | COMBUSTÍVEL (LITROS) | combustivel_litros | double | Não | |
| 30 | DISTÂNCIA VOADA (KM) | distancia_voada_km | double | Não | |
| 31 | DECOLAGENS | decolagens | integer | Não | Contagem |
| 32 | CARGA PAGA KM | carga_paga_km | double | Não | |
| 33 | CARGA GRATIS KM | carga_gratis_km | double | Não | |
| 34 | CORREIO KM | correio_km | double | Não | |
| 35 | ASSENTOS | assentos | integer | Não | Contagem |
| 36 | PAYLOAD | payload | double | Não | Capacidade de carga |
| 37 | HORAS VOADAS | horas_voadas | double | Não | **Decimal com vírgula** em anos recentes (ex.: 2,5 / 1,533) |
| 38 | BAGAGEM (KG) | bagagem_kg | double | Não | |

---

## 3. Regras de qualidade

Regras verificadas na promoção bronze → prata. Uma violação de regra **bloqueante** envia a linha para quarentena; uma violação **de alerta** é registrada mas não bloqueia.

| # | Regra | Tipo | Ação |
|---|---|---|---|
| R1 | Arquivo deve ter exatamente 38 colunas | Bloqueante | Falha o arquivo |
| R2 | Encoding deve decodificar sem caracteres inválidos | Bloqueante | Falha o arquivo |
| R3 | `empresa_sigla` preenchida | Bloqueante | Quarentena da linha |
| R4 | `ano` e `mes` preenchidos; `mes` entre 1 e 12 | Bloqueante | Quarentena da linha |
| R5 | `aeroporto_origem_sigla` e `aeroporto_destino_sigla` preenchidas | Bloqueante | Quarentena da linha |
| R6 | `aeroporto_*_uf` e `_regiao` preenchidas **quando** `aeroporto_*_pais = BRASIL` | Recuperável | Tenta enriquecer; quarentena só se falhar |
| R7 | `natureza` ∈ {DOMÉSTICA, INTERNACIONAL} | Alerta | Registra valor novo |
| R8 | `grupo_voo` ∈ {REGULAR, NÃO REGULAR, IMPRODUTIVO} | Alerta | Registra valor novo |

> **Nota sobre R6 (recuperável, não bloqueante):** UF/região vazias em aeroporto brasileiro não descartam a linha de imediato. Como a sigla identifica o aeroporto, a linha é primeiro submetida ao enriquecimento (ver abaixo). Só vai para quarentena se a sigla não for resolvível — ou seja, um aeroporto brasileiro genuinamente não identificável. Isso evita descartar dado recuperável.

> **Nota sobre R7/R8 (alerta e não bloqueio):** os domínios foram confirmados em três pontos (2000/2012/2025), mas anos não inspecionados podem trazer valores novos. A regra alerta em vez de rejeitar, para não descartar dado legítimo — o valor novo é revisado e, se válido, incorporado ao domínio.

### Enriquecimento (a implementar na camada prata)

> **Pendência registrada para a prata:** aeroportos com sigla presente mas `uf`/`regiao` ausentes (e país = BRASIL) serão completados a partir de uma **tabela de referência de aeroportos**. Estratégia provável: derivar essa tabela do próprio dataset, coletando as combinações `sigla → uf, regiao, ...` das linhas onde já vêm preenchidas. A fonte e o método definitivos serão decididos na implementação da prata. Aeroportos estrangeiros permanecem sem UF/região (esperado, não é erro).

---

## 4. Tratamento de violações

| Situação | Destino | Racional |
|---|---|---|
| Regra bloqueante de arquivo (R1, R2) | Arquivo rejeitado, execução falha | Melhor não ingerir do que ingerir corrompido |
| Regra bloqueante de linha (R3–R5) | Linha isolada em **quarentena** | Preserva a linha para análise; não descarta |
| Regra recuperável (R6) | Enriquecimento; quarentena só se irrecuperável | Não descarta linha cuja sigla é resolvível |
| Regra de alerta (R7, R8) | Linha aceita + registro de alerta | Não bloqueia dado potencialmente válido |
| Limiar de quarentena excedido | Execução falha, prata não é publicada | Evita publicar mês majoritariamente inválido em camada de consumo |

> O **limiar** (percentual máximo de linhas em quarentena tolerado antes de falhar a carga) será definido na camada de qualidade. Princípio: é melhor não ter o mês do que publicá-lo majoritariamente inválido.