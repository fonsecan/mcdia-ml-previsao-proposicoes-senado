# MCDIA ML — Previsão de proposições do Senado

Projeto de Machine Learning supervisionado para prever a quantidade mensal de proposições legislativas por tipo e tema computacional, usando séries temporais agregadas.

## Pergunta

Quantas proposições de cada tipo e tema devem ser apresentadas no próximo mês?

A unidade de previsão é uma contagem agregada por mês, tipo documental e tema. A PoC não prevê comportamento, posição, voto ou desempenho de pessoas.

## Conjunto de dados

A base inicial foi obtida em **17/09/2026**, a partir da API oficial de Dados Abertos do Senado:

- **Portal navegável:** [Dados Abertos — Projetos e Matérias](https://www12.senado.leg.br/dados-abertos/legislativo/projetos-e-materias)
- **Documentação da API:** [Swagger UI](https://legis.senado.leg.br/dadosabertos/api-docs/swagger-ui/index.html)
- **Especificação OpenAPI:** [JSON da API](https://legis.senado.leg.br/dadosabertos/v3/api-docs)
- **Operação REST aplicável no Swagger:** `GET /dadosabertos/processo`
- **Filtros de período:** `dataInicioApresentacao` e `dataFimApresentacao`, no formato `AAAA-MM-DD`
- **Exemplo de consulta:** [`GET /dadosabertos/processo?dataInicioApresentacao=2021-09-16&dataFimApresentacao=2022-09-16`](https://legis.senado.leg.br/dadosabertos/processo?dataInicioApresentacao=2021-09-16&dataFimApresentacao=2022-09-16)
- **Endpoint GraphQL usado pelo script:** [https://legis.senado.leg.br/dadosabertos/graphql](https://legis.senado.leg.br/dadosabertos/graphql). Esse endereço é uma API técnica e não deve ser aberto como uma página comum no navegador; ele requer uma requisição `POST` com uma consulta GraphQL.
- **Período das proposições:** de 16/09/2021 a 15/09/2026
- **Recorte:** propostas normativas dos tipos legislativos selecionados na consulta
- **Volume:** 8.651 registros, com identificadores únicos
- **Campos principais:** identificação, ementa, indexação, tipo documental, data de apresentação e URL pública do documento

A operação REST `/dadosabertos/processo` limita a pesquisa por período a, no máximo, um ano por consulta. Por isso, a extração de cinco anos deve ser feita em intervalos sucessivos ou reproduzida pelo script atual, que usa a consulta GraphQL paginada.

A resposta da API foi convertida para CSV para facilitar a exploração nos notebooks e o uso no JupyterLab. O arquivo está versionado em:

`data/propostas_normativas_20210916_a_20260916.csv`

Os detalhes da extração — período, tipos consultados, data da coleta e fonte — estão em:

`data/propostas_normativas_20210916_a_20260916.metadata.json`

O dicionário das colunas e instruções específicas de uso estão em [`data/README.md`](data/README.md). A extração pode ser reproduzida com [`scripts/extrair_historico.py`](scripts/extrair_historico.py).

## Organização

- `notebooks/`: caminho principal de exploração e treinamento, compatível com Jupyter e Colab.
- `docs/`: hipótese, decisões, dicionário e resultados.
- `data/`: base de entrada versionada e dados locais por estágio. Apenas `data/raw/` é ignorado pelo Git.
- `artifacts/`: modelos, métricas e previsões, ignorados pelo Git.
- `src/` e `tests/`: só receberão código quando uma lógica precisar ser reutilizada fora dos notebooks.

## Executar no Windows com Anaconda e JupyterLab

Este é o caminho recomendado para quem está começando. Os comandos abaixo devem ser executados no **Anaconda Prompt**, e não no PowerShell comum.

### 1. Obter o projeto

Se o projeto ainda não estiver no computador, abra o **Anaconda Prompt** pelo menu Iniciar do Windows e execute:

```powershell
git clone https://github.com/fonsecan/mcdia-ml-previsao-proposicoes-senado.git C:\mcdia\mcdia-ml-previsao-proposicoes-senado
```

Se o projeto já estiver em `C:\mcdia\mcdia-ml-previsao-proposicoes-senado`, não é necessário cloná-lo novamente.

### 2. Criar o ambiente do projeto

No mesmo Anaconda Prompt, entre na pasta do projeto e crie um ambiente isolado:

```powershell
cd C:\mcdia\mcdia-ml-previsao-proposicoes-senado
conda create --name mcdia-ml python=3.11
conda activate mcdia-ml
python -m pip install -r requirements.txt
```

Na primeira execução, o Anaconda poderá perguntar se deseja prosseguir. Digite `y` e pressione Enter.

O ambiente `mcdia-ml` separa as bibliotecas deste projeto dos demais ambientes do Anaconda. Normalmente, ele só precisa ser criado uma vez.

### 3. Abrir o JupyterLab na pasta correta

Ainda com o ambiente `mcdia-ml` ativado:

```powershell
cd C:\mcdia\mcdia-ml-previsao-proposicoes-senado
jupyter lab
```

O JupyterLab será aberto no navegador. Na coluna esquerda, abra a pasta `notebooks` e depois o arquivo:

`02_visualizacao_inicial.ipynb`

Abrir o JupyterLab a partir da pasta raiz do projeto é importante porque o notebook localiza a base CSV subindo pelas pastas até encontrar `data/`.

### 4. Escolher o kernel

Com o notebook aberto, observe o seletor de kernel no canto superior direito. Escolha:

`Python (mcdia-ml)`

ou uma opção equivalente que indique o ambiente `mcdia-ml`.

Se essa opção não aparecer, feche o JupyterLab, execute no Anaconda Prompt:

```powershell
conda activate mcdia-ml
python -m ipykernel install --user --name mcdia-ml --display-name "Python (mcdia-ml)"
jupyter lab
```

### 5. Executar o notebook

Há duas formas simples:

- executar célula por célula: clique na primeira célula de código e pressione `Shift + Enter`;
- executar tudo: use o menu `Run` → `Run All Cells`.

O notebook apresenta amostras dos registros, campos e valores ausentes, distribuição por tipo documental, volume mensal total e volume mensal por tipo.

As células não alteram o CSV original. Para salvar anotações, use `Ctrl + S`.

## Usar o Anaconda Navigator

Também é possível usar o Anaconda Navigator para abrir o JupyterLab:

1. Abra o **Anaconda Navigator** pelo menu Iniciar.
2. Na tela **Environments**, crie ou selecione o ambiente `mcdia-ml`.
3. Instale as dependências do projeto conforme o arquivo `requirements.txt`.
4. Na tela **Home**, selecione o ambiente `mcdia-ml` e clique em **Launch** no JupyterLab.
5. Navegue até `C:\mcdia\mcdia-ml-previsao-proposicoes-senado\notebooks` e abra `02_visualizacao_inicial.ipynb`.
6. Confirme que o kernel selecionado é `Python (mcdia-ml)`.

Para evitar problemas de localização da base, a abertura pelo **Anaconda Prompt**, usando os comandos da seção anterior, é a opção mais previsível.

## Problemas comuns

### `conda` ou `jupyter` não é reconhecido

Abra o **Anaconda Prompt**, que já configura os comandos do Anaconda. Se o JupyterLab ainda não estiver instalado, execute:

```powershell
conda activate mcdia-ml
conda install jupyterlab
```

### `ModuleNotFoundError: No module named 'pandas'` ou `matplotlib`

Ative o ambiente e instale novamente as dependências:

```powershell
cd C:\mcdia\mcdia-ml-previsao-proposicoes-senado
conda activate mcdia-ml
python -m pip install -r requirements.txt
```

### Erro informando que o CSV não foi encontrado

Feche o JupyterLab e abra-o novamente a partir da raiz do projeto:

```powershell
cd C:\mcdia\mcdia-ml-previsao-proposicoes-senado
conda activate mcdia-ml
jupyter lab
```

Depois abra `notebooks/02_visualizacao_inicial.ipynb`.

### Encerrar o JupyterLab

Feche a aba do navegador e, no Anaconda Prompt que está executando o JupyterLab, pressione `Ctrl + C`. Confirme com `y` quando solicitado.

## Próximo passo

Depois de explorar o notebook de visualização, transformar os registros em séries mensais por tipo e, depois, por tema computacional. A etapa seguinte deverá comparar previsões simples — último valor, média móvel e mesmo mês do ano anterior — antes de usar modelos de aprendizado de máquina.