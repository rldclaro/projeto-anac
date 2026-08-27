# ✈️ Pipeline de Dados de Voos — ANAC

> Pipeline de engenharia de dados **end-to-end** que ingere, trata e modela o histórico público de voos da aviação civil brasileira (ANAC), desde os anos 2000, usando arquitetura medalhão (bronze/prata/ouro).

**Autor:** Rildo Claro

![Status](https://img.shields.io/badge/status-em%20construção-yellow)
![Stack](https://img.shields.io/badge/stack-PySpark%20|%20Delta%20|%20Airflow-blue)

---

## 📌 Sobre o projeto

Os dados de voos da ANAC são um caso realista de engenharia de dados: arquivos mensais publicados ao longo de mais de duas décadas, com **schema que muda ao longo do tempo**, encoding legado, separadores e formatos numéricos no padrão brasileiro, e valores ausentes em campos que deveriam ser obrigatórios.

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
   Fonte ANAC (CSV mensal)
            │
            ▼
   ┌─────────────────┐
   │     INGESTÃO    │  download parametrizado por ano/mês
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

**Grão de partição:** `ano=YYYY/mes=MM` em todas as camadas — casa com o formato nativo da fonte, permite backfill granular e reprocessamento de um mês específico sem afetar o resto.

### Princípios de engenharia aplicados

| Princípio | Como é garantido |
|---|---|
| **Idempotência** | Reprocessar o mesmo mês produz o mesmo resultado (escrita por partição / `MERGE`) |
| **Reprocessabilidade** | Bronze preserva o dado cru; qualquer regra nova pode ser reaplicada do zero |
| **Data lógica** | Todo processamento é parametrizado por data de referência, nunca por "hoje" |
| **Qualidade** | Testes de schema, volume, domínio e unicidade antes de promover camada |
| **Rastreabilidade** | Metadados de ingestão e tabela de auditoria por execução |

---

## 🛠️ Stack

| Camada | Tecnologia |
|---|---|
| Processamento | **PySpark** |
| Formato de tabela | **Delta Lake** (ACID, time travel, schema evolution) |
| Orquestração | **Apache Airflow** |
| Análise | **SQL** |
| Ambiente | **Docker / Docker Compose** sobre **WSL2** |
| Versionamento | **Git / GitHub** |
| Linguagem | **Python** |

> A escolha por Docker Compose (em vez de um ambiente gerenciado ou Kubernetes) é **proposital**: o projeto expõe deliberadamente a orquestração, o particionamento e o gerenciamento de estado que plataformas gerenciadas abstraem — que é justamente o que se pretende praticar. Uma migração para Kubernetes está mapeada como extensão.

---

## 📂 Estrutura do repositório

> A estrutura abaixo é o **alvo final**. As pastas nascem à medida que cada etapa é implementada.

```
projeto-anac/
├── docker/                 # Dockerfile e docker-compose.yml
├── src/
│   ├── ingestao/           # download + escrita no bronze
│   ├── transformacao/      # bronze → prata → ouro
│   ├── qualidade/          # validações de dados
│   └── utils/              # config, logging, helpers
├── dags/                   # DAGs do Airflow
├── notebooks/              # exploração (não é produção)
├── tests/                  # testes unitários e de integração
├── docs/
│   ├── contrato-de-dados.md
│   └── arquitetura.md
├── lake/                   # data lake local (fora do versionamento)
│   ├── bronze/
│   ├── prata/
│   └── ouro/
├── .gitignore
└── README.md
```

---

## 🗺️ Roadmap

O projeto é desenvolvido em fases, versionadas por tags no Git:

- [ ] **`v0.1` — Bronze:** ingestão parametrizada e escrita do dado cru
- [ ] **`v0.2` — Prata:** padronização de schema, limpeza e idempotência
- [ ] **`v0.3` — Ouro:** modelo dimensional (fatos e dimensões)
- [ ] **`v0.4` — Airflow:** pipeline orquestrado com backfill
- [ ] **`v1.0` — Completo:** observabilidade, testes, documentação e dashboard

### Extensões planejadas
- Migração para nuvem (object storage + processamento gerenciado)
- Trilha Kubernetes (KubernetesExecutor + Helm)
- **Databricks como reforço:** reimplementar o pipeline (ou parte dele) no Databricks Free Edition, comparando a experiência com a construção "na mão" — evidencia domínio dos fundamentos que a plataforma abstrai
- dbt na camada ouro
- CI/CD com GitHub Actions

---

## 🚀 Como executar

> ⚠️ Em construção — as instruções de execução serão preenchidas conforme o ambiente é finalizado. O objetivo final é que o pipeline suba com um único `docker compose up`.

---

## 📊 Fonte de dados

Dados públicos da **Agência Nacional de Aviação Civil (ANAC)**, disponíveis no portal de Dados e Estatísticas da agência. Os arquivos são de uso público, publicados mensalmente em formato CSV.

---

## 📝 Licença

Projeto de estudo e portfólio. Dados de origem são públicos e de responsabilidade da ANAC.