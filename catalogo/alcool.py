"""Calcula o teor alcoólico aproximado de cada drink e a faixa (sem álcool,
leve, médio, forte). Mesma regra que o app vai usar; quem discordar corrige à
mão no cadastro, e a correção prevalece.

Uso: python3 -I alcool.py drinks-lote-01.json
"""
import json, sys, pathlib

AQUI = pathlib.Path(__file__).parent

# volume aproximado, em ml, de cada unidade que aparece nas receitas
UNIDADE_ML = {
    "ml": 1, "dash": 0.8, "gotas": 0.05, "colher de bar": 5, "colher de chá": 5,
    "cubo": 2, "ramos": 0, "folhas": 0,
    "completar": 90,   # completar um copo alto com gelo
    "splash": 20,      # "um pouco de"
}
# volume quando a unidade é "unidade" (uma fruta, uma clara)
UNIDADE_POR_INGREDIENTE = {"limao": 30, "limao-siciliano": 40, "ovo": 30}

# água que o gelo acrescenta, por técnica (fator sobre o volume da mistura)
DILUICAO = {"liquidificador": 1.6, "batido": 1.5, "mexido": 1.3, "macerado": 1.2, "montado": 1.15}

# faixas de teor no copo, em %
def faixa(teor):
    if teor == 0:
        return "sem álcool"
    if teor < 11:
        return "leve"
    if teor <= 22:
        return "médio"
    return "forte"


def volume(linha):
    if linha.get("lavagem"):           # rinse: o excesso é descartado
        return 2
    if linha["unid"] == "unidade":
        return UNIDADE_POR_INGREDIENTE.get(linha["ing"], 0) * linha.get("qtd", 1)
    base = UNIDADE_ML[linha["unid"]]
    return base * linha.get("qtd", 1) if linha["unid"] not in ("completar", "splash") else base


def calcular(drink, teores):
    diluicao = DILUICAO["liquidificador"] if drink.get("liquidificador") else max(
        DILUICAO[t] for t in drink["tecnica"])
    mistura = alcool = completa = 0.0
    for l in drink["ingredientes"]:
        if l.get("opcional"):
            continue
        v = volume(l)
        alcool += v * teores[l["ing"]] / 100
        if l.get("completa"):
            completa += v           # entra depois de bater/mexer, sem diluir
        else:
            mistura += v
    total = mistura * diluicao + completa
    teor = round(100 * alcool / total, 1) if total else 0
    return teor, faixa(teor)


if __name__ == "__main__":
    ings = json.load(open(AQUI / "ingredientes.json", encoding="utf-8"))
    teores = {i["id"]: i["teor"] for i in ings}
    drinks = json.load(open(sys.argv[1], encoding="utf-8"))
    faltando = sorted({l["ing"] for d in drinks for l in d["ingredientes"]} - set(teores))
    if faltando:
        sys.exit("ingredientes fora da lista controlada: " + ", ".join(faltando))
    for d in drinks:
        d["alcool_calc"], d["alcool"] = calcular(d, teores)
        print(f'{d["nome"]:<18} {d["alcool_calc"]:>5}%  {d["alcool"]}')
    json.dump(drinks, open(sys.argv[1], "w", encoding="utf-8"), ensure_ascii=False, indent=1)
