"""Agent 2 : risques techniques dans les lignes modifiées."""
from .common import analyze, code_payload


def run(context, model):
    return analyze(model, 2,
        "Analyse le diff : erreurs logiques, cas limites, compatibilité et dépendances visibles. "
        "Sépare les faits des hypothèses. Cite fichier, ligne nouvelle si connue et extrait du diff. "
        "N'invente pas le contenu des autres fichiers. Ne calcule pas une complexité chiffrée sans outil."
        "Compare les noms de fonctions, signatures et comportements du diff aux exigences de l'issue. "
        "Signale les écarts concrets. "
        "Ne considère pas les fichiers non inspectés comme des défauts.",
        code_payload(context))
