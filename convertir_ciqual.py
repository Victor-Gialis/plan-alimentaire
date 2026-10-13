"""Convertit la table Ciqual (fichier Excel) en ciqual.json pour le site.

Utilisation :
    pip install pandas xlrd
    python convertir_ciqual.py Table_Ciqual_XXXX.xls
Le fichier ciqual.json est créé à côté du script : à envoyer sur GitHub
à côté de index.html.
"""
import json, math, sys
import pandas as pd

if len(sys.argv) < 2:
    sys.exit("Usage : python convertir_ciqual.py fichier_ciqual.xls")

df = pd.read_excel(sys.argv[1], sheet_name=0)

def col(mot):
    for c in df.columns:
        if mot in str(c).replace("\n", " "):
            return c
    sys.exit("Colonne introuvable : " + mot)

cP, cC, cL = col("Protéines, N x 6.25"), col("Glucides"), col("Lipides")

def num(v):
    if v is None or (isinstance(v, float) and math.isnan(v)):
        return None
    if isinstance(v, (int, float)):
        return float(v)
    s = str(v).strip().replace(",", ".")
    if s in ("", "-"):
        return None
    if "trace" in s.lower():
        return 0.0
    if s.startswith("<"):
        try:
            return float(s[1:]) / 2
        except ValueError:
            return None
    try:
        return float(s)
    except ValueError:
        return None

groupes, data = [], []
for _, r in df.iterrows():
    p, c, l = num(r[cP]), num(r[cC]), num(r[cL])
    if p is None and c is None and l is None:
        continue
    g = r["alim_grp_nom_fr"]
    g = "" if (isinstance(g, float) and math.isnan(g)) else str(g)
    if g not in groupes:
        groupes.append(g)
    f = lambda x: round(x or 0, 1)
    data.append([str(r["alim_nom_fr"]).strip(), f(p), f(c), f(l), groupes.index(g)])

with open("ciqual.json", "w", encoding="utf-8") as fh:
    json.dump({"g": groupes, "d": data}, fh, ensure_ascii=False, separators=(",", ":"))
print(len(data), "aliments écrits dans ciqual.json")
