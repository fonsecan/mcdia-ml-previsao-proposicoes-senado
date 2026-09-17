# Instruções para agentes

## Objetivo

Este repositório reúne o trabalho de Machine Learning do MCDIA para prever volumes mensais agregados de proposições normativas do Senado, utilizando Dados Abertos.

## Segurança e escopo

- Usar dados públicos e somente os campos necessários.
- Não criar perfis, rankings ou previsões sobre pessoas identificáveis.
- O objeto de previsão é agregado: mês, tipo documental e, futuramente, tema computacional.
- Não interpretar resultados como previsão de mérito, aprovação, intenção ou posição política.

## Reprodutibilidade

- Registrar fonte, endpoint, parâmetros, período de coleta, campos, transformações e método de avaliação.
- Manter os dados de entrada versionados em `data/` quando o tamanho e a licença permitirem.
- Não versionar credenciais, `.env`, dados temporários, ambientes virtuais, artefatos grandes nem saídas de execução.
- Preferir notebooks para exploração e scripts reutilizáveis em `scripts/` para extração.

## Dados

- Fonte legislativa: API GraphQL de Dados Abertos do Senado.
- A base inicial está em `data/propostas_normativas_20210916_a_20260916.csv`.
- O arquivo de metadados deve acompanhar qualquer atualização do CSV.

## Encoding

Todo arquivo textual deve ser UTF-8 sem BOM. Validar acentuação e evitar mojibake antes de concluir alterações.