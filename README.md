# ✈️ Pipeline de Dados de Voos — ANAC

> Pipeline de engenharia de dados **end-to-end** que ingere, trata e modela o histórico público de voos da aviação civil brasileira (ANAC), desde os anos 2000, usando arquitetura medalhão (bronze/prata/ouro).

**Autor:** Rildo Claro

![Status](https://img.shields.io/badge/status-em%20construção-yellow)
![Stack](https://img.shields.io/badge/stack-PySpark%20|%20Delta%20|%20Airflow-blue)

---

## 📌 Sobre o projeto

Os dados de voos da ANAC são um caso realista de engenharia de dados: arquivos publicados ao longo de mais de duas décadas, com encoding legado, separadores e formatos numéricos no padrão brasileiro, nomes de coluna com acentos e caracteres especiais, e valores ausentes em campos que deveriam ser obrigatórios.

Este projeto constrói um pipeline completo que transforma esses arquivos crus em um **modelo dimensional pronto para análise**, respondendo perguntas como:

- Como evoluiu o volume de passageiros no Brasil ao longo dos anos?
- Qual foi o impacto real da pandemia na aviação civil (2019 → 2020 → recuperação)?
- Quais são as rotas domésticas mais movimentadas, e quais deixaram de existir?
- Como se distribui o market share entre as companhias aéreas ao longo do tempo?

O objetivo é duplo: **consolidar práticas de engenharia de dados fora de um ambiente gerenciado** (construindo orquestração, particionamento e idempotência "na mão") e servir como **projeto de portfólio** demonstrando domínio de ponta a ponta.

---

## 🏗️ Arquitetura

O pipeline segue a **arquitetura medalhão**, com três camadas de refinamento progressivo:

```
   Fonte ANAC (CSV anual)
            │
            ▼
   ┌─────────────────┐
   │     INGESTÃO    │  leitura dos CSVs baixados, parametrizada por ano
   └─────────────────┘
            │
            ▼
   ┌─────────────────┐
   │   🥉 BRONZE     │  dado cru, fiel à origem, sem tratamento
   └─────────────────┘
            │
            ▼
   ┌─────────────────┐
   │   🥈 PRATA      │  schema padronizado, limpo, tipado, idempotente
   └─────────────────┘
            │
            ▼
   ┌─────────────────┐
   │   🥇 OURO       │  modelo dimensional (fatos + dimensões)
   └─────────────────┘
            │
            ▼
      Análise / SQL / Dashboard
```

**Grão de partição:** o Bronze particiona por `ano=YYYY`, espelhando o arquivo de origem; a Prata e o Ouro refinam para `ano=YYYY/mes=MM`, o grão de consumo e reprocessamento. Quebrar o ano em meses já é uma transformação, por isso acontece na Prata, não na ingestão fiel do Bronze.

### Princípios de engenharia aplicados

| Princípio | Como é garantido |
|---|---|
| **Idempotência** | Reprocessar o mesmo período produz o mesmo resultado (escrita por partição com `replaceWhere` / `MERGE`) |
| **Reprocessabilidade** | Bronze preserva o dado cru; qualquer regra nova pode ser reaplicada do zero |
| **Data lógica** | Todo processamento é parametrizado por data de referência, nunca por "hoje" |
| **Qualidade** | Testes de schema, volume, domínio e unicidade antes de promover camada |
| **Rastreabilidade** | Metadados de ingestão (`_data_ingestao`, `_arquivo_origem`) gravados em cada linha |

---

## 🛠️ Stack

| Camada | Tecnologia |
|---|---|
| Processamento | **PySpark** (Spark 4.0.1) |
| Formato de tabela | **Delta Lake** (ACID, time travel, column mapping) |
| Orquestração | **Apache Airflow** |
| Análise | **SQL** |
| Ambiente | **Docker / Docker Compose** sobre **WSL2** |
| Versionamento | **Git / GitHub** |
| Linguagem | **Python** |

> A escolha por Docker Compose (em vez de um ambiente gerenciado ou Kubernetes) é **proposital**: o projeto expõe deliberadamente a orquestração, o particionamento e o gerenciamento de estado que plataformas gerenciadas abstraem, que é justamente o que se pretende praticar. Uma migração para Kubernetes está mapeada como extensão.

---

## 📂 Estrutura do repositório

> A estrutura abaixo é o **alvo final**. As pastas nascem à medida que cada etapa é implementada.

```
projeto-anac/
├── docker/                 # spark-defaults.conf (pacote e extensões Delta)
├── src/
│   ├── ingestao/           # leitura dos CSVs + escrita no bronze
│   ├── transformacao/      # bronze → prata → ouro
│   ├── qualidade/          # validações de dados
│   └── utils/              # config, logging, helpers
├── dags/                   # DAGs do Airflow
├── notebooks/              # exploração (não é produção)
├── tests/                  # testes unitários e de integração
├── docs/
│   ├── contrato-de-dados.md
│   └── arquitetura.md
├── dados-brutos/           # CSVs baixados da ANAC (fora do versionamento)
├── lake/                   # data lake local (fora do versionamento)
│   ├── bronze/
│   ├── prata/
│   └── ouro/
├── docker-compose.yml
├── .gitignore
└── README.md
```

---

## 🗺️ Roadmap

O projeto é desenvolvido em fases, versionadas por tags no Git:

- [x] **`v0.1` — Bronze:** ingestão parametrizada e escrita do dado cru ✅
- [ ] **`v0.2` — Prata:** padronização de schema, limpeza e idempotência
- [ ] **`v0.3` — Ouro:** modelo dimensional (fatos e dimensões)
- [ ] **`v0.4` — Airflow:** pipeline orquestrado com backfill
- [ ] **`v1.0` — Completo:** observabilidade, testes, documentação e dashboard

### Extensões planejadas
- Migração para nuvem (object storage + processamento gerenciado)
- Trilha Kubernetes (KubernetesExecutor + Helm)
- **Databricks como reforço:** reimplementar o pipeline (ou parte dele) no Databricks Free Edition, comparando a experiência com a construção "na mão", evidenciando domínio dos fundamentos que a plataforma abstrai
- dbt na camada ouro
- CI/CD com GitHub Actions

---

## 🚀 Como executar

### Pré-requisitos
- [Docker](https://www.docker.com/) e Docker Compose
- Em Windows, recomenda-se rodar sobre **WSL2**

### Passo a passo

1. Clone o repositório:
   ```bash
   git clone git@github.com:rldclaro/projeto-anac.git
   cd projeto-anac
   ```

2. Crie um arquivo `.env` na raiz do projeto com o token de acesso ao Jupyter:
   ```
   JUPYTER_TOKEN=escolha-um-token
   ```
   > O `.env` não é versionado (está no `.gitignore`), pois guarda configuração local. Cada pessoa define o seu.

3. Baixe os dados da ANAC (ver seção [Aquisição dos dados](#aquisição-dos-dados)) e coloque os CSVs em `dados-brutos/{ano}.csv`.

4. Suba o ambiente:
   ```bash
   docker compose up
   ```

5. Acesse o JupyterLab em `http://localhost:8888/lab`, usando o token definido no `.env`.

### Executando a ingestão Bronze

Com o ambiente no ar, a ingestão de um ano específico é feita por `spark-submit`:

```bash
docker compose exec jupyter spark-submit \
  /home/jovyan/work/src/ingestao/ingestao_bronze.py 2000
```

O ano entra como parâmetro (data lógica), e a escrita é idempotente: reprocessar o mesmo ano substitui apenas a partição correspondente, sem duplicar.

Para carregar todo o histórico de uma vez (backfill):

```bash
for ano in $(seq 2000 2026); do
  docker compose exec jupyter spark-submit \
    /home/jovyan/work/src/ingestao/ingestao_bronze.py $ano
done
```

Para encerrar o ambiente, use `docker compose down`.

---

## 📊 Fonte de dados

Dados públicos da **Agência Nacional de Aviação Civil (ANAC)**, disponíveis no portal de Dados e Estatísticas da agência. Os arquivos são de uso público, publicados em formato CSV, subdivididos por ano.

A estrutura, tipos e regras de qualidade esperadas da fonte estão documentados no [contrato de dados](docs/contrato-de-dados.md).

### Aquisição dos dados

O portal da ANAC protege o download contra automação (desafio anti-bot), o que impede baixar os CSVs via script diretamente. Por isso, a **aquisição** dos arquivos é feita manualmente (download dos CSVs anuais pelo portal), enquanto todo o **processamento** a partir daí é automatizado e reproduzível.

Essa separação é deliberada: aquisição e processamento são responsabilidades distintas. A limitação está na fonte, não no pipeline, que roda de ponta a ponta sobre os arquivos já baixados, colocados em `dados-brutos/{ano}.csv`.

---

## 📝 Licença

Projeto de estudo e portfólio. Dados de origem são públicos e de responsabilidade da ANAC.