from datetime import datetime, timezone
from pathlib import Path
import json
import time
import requests
import pandas as pd

ENDPOINT = "https://legis.senado.leg.br/dadosabertos/graphql"
INICIO, FIM = "2021-09-16", "2026-09-16"
MARCADORES_CODIFICACAO = (chr(0xC3), chr(0xC2))
TIPOS = ["PROJETO_LEI_ORDINARIA", "PROJETO_LEI_COMPLEMENTAR", "PROJETO_DECRETO_LEGISLATIVO", "PROJETO_RESOLUCAO", "MEDIDA_PROVISORIA", "PROPOSTA_EMENDA_CONSTITUICAO", "PROJETO_LEI_CONVERSAO", "PROJETO_LEI"]
QUERY = """query($limit: Int!, $offset: Int!, $inicio: Date!, $fim: Date!, $tipos: [String!]) { processos(filter: {dataInicioApresentacao: $inicio, dataFimApresentacao: $fim, siglaTipoDocumento: $tipos}, pageReq: {limit: $limit, offset: $offset, sortBy: [\"dataApresentacaoDocumento\"], order: [\"asc\"]}) { id identificacao ementa indexacao tipoDocumento dataApresentacaoDocumento urlDocumento } }"""
def normalizar_texto(valor):
    if not isinstance(valor, str) or not any(marcador in valor for marcador in MARCADORES_CODIFICACAO):
        return valor
    try:
        return valor.encode("latin-1").decode("utf-8")
    except UnicodeError:
        return valor

def normalizar_resposta(valor):
    if isinstance(valor, dict):
        return {chave: normalizar_resposta(item) for chave, item in valor.items()}
    if isinstance(valor, list):
        return [normalizar_resposta(item) for item in valor]
    return normalizar_texto(valor)

registros=[]
for offset in range(0, 10000, 100):
    resposta=requests.post(ENDPOINT, json={"query": QUERY, "variables": {"limit":100,"offset":offset,"inicio":INICIO,"fim":FIM,"tipos":TIPOS}}, timeout=30)
    resposta.raise_for_status()
    corpo=normalizar_resposta(json.loads(resposta.content.decode("utf-8")))
    if corpo.get("errors"): raise RuntimeError(corpo["errors"])
    pagina=corpo["data"]["processos"]; registros.extend(pagina)
    print(f"{offset}: {len(registros)}")
    if len(pagina)<100: break
    time.sleep(.15)
df=pd.DataFrame(registros)
if not df.id.is_unique or df.ementa.fillna("").str.strip().eq("").any():
    raise RuntimeError("Falha de qualidade")
padrao_mojibake = re.compile(r"(?:\u00c3[\x80-\xBF]|\u00c2[\x80-\xBF]|\ufffd)")
if df.select_dtypes(include=["object", "string"]).apply(lambda coluna: coluna.fillna("").map(lambda valor: bool(padrao_mojibake.search(str(valor)))).any()).any():
    raise RuntimeError("Texto com codificação inválida")
destino=Path(__file__).resolve().parents[1] / "data"
destino.mkdir(exist_ok=True)
arquivo=destino / "propostas_normativas_20210916_a_20260916.csv"
df.to_csv(arquivo,index=False,encoding="utf-8")
(destino / "propostas_normativas_20210916_a_20260916.metadata.json").write_text(json.dumps({"registros":len(df),"coletado_em_utc":datetime.now(timezone.utc).isoformat(),"inicio":INICIO,"fim":FIM,"tipos":TIPOS,"fonte":ENDPOINT},ensure_ascii=False,indent=2),encoding="utf-8")
print(arquivo, len(df))