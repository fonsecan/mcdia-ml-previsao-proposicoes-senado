# Base de entrada da PoC 5

## Arquivo versionado

`propostas_normativas_20210916_a_20260916.csv` contém 8.651 proposições normativas apresentadas de 16/09/2021 a 15/09/2026, extraídas da API GraphQL de Dados Abertos do Senado.

Cada linha é uma proposição. As colunas são:

- `id`: identificador do processo na fonte;
- `identificacao`: identificação legislativa exibida pela fonte;
- `ementa`: resumo oficial da proposição;
- `indexacao`: termos de indexação fornecidos pela fonte;
- `tipoDocumento`: nome do tipo documental;
- `dataApresentacaoDocumento`: data de apresentação;
- `urlDocumento`: endereço público do documento.

O arquivo `.metadata.json` registra período, tipos selecionados, momento da coleta e URL de origem. Ele deve acompanhar o CSV em qualquer atualização.

## Uso no notebook

Carregue o CSV com `pandas.read_csv("../data/propostas_normativas_20210916_a_20260916.csv")`. Para a primeira série temporal, agregue `dataApresentacaoDocumento` por mês e `tipoDocumento`. A etapa posterior poderá derivar temas computacionais de `ementa` e `indexacao`.

`data/raw/` continua reservado a insumos temporários e não é versionado.