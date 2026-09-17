# Hipótese e plano do projeto

## Objetivo

Prever o volume mensal de proposições apresentadas, segmentado por tipo documental e tema computacional. O resultado esperado é uma estimativa agregada para períodos futuros, útil para planejamento e análise de fluxo legislativo.

## Formulação supervisionada

Cada linha do conjunto de treinamento representará uma combinação de:

- mês de apresentação;
- tipo documental;
- tema computacional, quando disponível;
- quantidade de proposições apresentadas naquele mês.

O alvo será a quantidade no mês seguinte. Variáveis candidatas: mês do ano, ano, defasagens de 1, 3, 6 e 12 meses, médias móveis e indicadores de calendário legislativo quando houver fonte histórica confiável.

## Recorte inicial

Começar com propostas normativas, pois são mais homogêneas que requerimentos. Usar o maior período histórico disponível, evitando misturar campos criados ou atualizados depois do mês previsto.

## Avaliação

Separação temporal: treinar em meses anteriores e testar somente em meses posteriores. Comparar qualquer modelo com dois baselines: último valor observado e mesmo mês do ano anterior. Métricas: MAE e sMAPE por tipo e tema.

## Limites

A previsão é sobre quantidade agregada, não sobre aprovação, mérito, prioridade política, comportamento de parlamentares ou resultado de votação.