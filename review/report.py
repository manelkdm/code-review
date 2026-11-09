"""Generate Markdown and JSON review reports."""
from pathlib import Path
from .security import safe_markdown as safe


def markdown(review):
    lines = ["# Rapport de revue de code", "", f"Exécution : `{review.run_id}`", "",
        f"Dépôt : {safe(review.repository)} · PR {review.pr} · GitHub Issue #{review.issue_id}", "",
        f"Commit analysé : `{review.head_sha}`", "",
        f"**Recommandation : {review.decision}**", "",
        "Une personne doit vérifier les preuves et prendre la décision finale. Aucune fusion automatique.", ""]
    if review.demo:
        lines += ["**DÉMONSTRATION SIMULÉE — aucun modèle ni outil d'analyse exécuté.**", ""]
    lines += ["## Motifs", ""] + ["- " + safe(r) for r in review.reasons] + [""]
    lines += ["## Contrôles déterministes", "", "| Outil | État | Nombre de constats |", "|---|---|---:|"]
    for name in ("ruff", "pytest", "bandit", "gitleaks"):
        tool = review.tools.get(name)
        lines.append(f"| {name} | {tool.status if tool else 'not_run'} | {tool.total_findings if tool else 'inconnu'} |")
    lines += ["", f"Couverture de lignes : {review.coverage_percent if review.coverage_percent is not None else 'inconnue'}", ""]
    for result in review.results:
        lines += [f"## Agent {result.agent}", "", f"État : {result.status}", "", safe(result.summary), ""]
        for f in result.findings:
            location = f"{f.file or 'emplacement non fourni'}:{f.line or '?'}"
            lines += [f"- **{f.severity} — {safe(f.title)}** ({f.source})", f"  Emplacement : {safe(location)}. Preuve : {safe(f.evidence)}", f"  Action : {safe(f.recommendation)}"]
        if result.criteria:
            lines += ["", "| Critère | État | Preuve |", "|---|---|---|"]
            for c in result.criteria:
                values = [safe(c.id + ' ' + c.text), c.status, safe(c.evidence)]
                lines.append("| " + " | ".join(x.replace("\n", " ") for x in values) + " |")
        lines += [""] + ["- Limite : " + safe(x) for x in result.limitations] + [""]
    return "\n".join(lines)


def save(review, root: Path):
    root.mkdir(parents=True, exist_ok=True)
    dest = root / review.run_id
    dest.mkdir(mode=0o700)
    (dest / "review.json").write_text(review.model_dump_json(indent=2), encoding="utf-8")
    (dest / "report.md").write_text(markdown(review), encoding="utf-8")
    return dest


def publication_text(review):
    from .connectors import COMMENT_MARKER
    lines = [
        COMMENT_MARKER, "## Revue IA — sept agents", "",
        f"GitHub Issue : #{review.issue_id} · Commit : `{review.head_sha}`", "",
        f"**Recommandation : {review.decision}**", "",
        "Validation humaine obligatoire. Aucune fusion automatique.", "",
    ]
    if review.demo:
        lines += ["**Simulation sans modèle réel.**", ""]
    lines += ["### Motifs", ""] + ["- " + safe(x) for x in review.reasons[:12]]
    lines += ["", "### Agents", ""]
    for result in review.results:
        lines.append(
            f"- **Agent {result.agent}** : {result.status} — "
            f"{safe(result.summary)}"
        )
        for finding in result.findings[:3]:
            lines.append(f"  - {finding.severity} : {safe(finding.title)} ({safe(finding.file or 'fichier non précisé')})")
    lines += ["", "Le rapport complet (Markdown et JSON) est disponible dans les artefacts de cette exécution GitHub Actions."]
    return "\n".join(lines)[:55_000]
