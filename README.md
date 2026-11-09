# Revue de code GitHub — 7 agents IA

Ce prototype utilise **sept agents IA spécialisés** pour analyser les Pull Requests GitHub à partir des exigences d'une GitHub Issue. Il combine les contrôles Ruff, Bandit, Gitleaks et pytest avec une analyse effectuée par Ollama.

GitHub Actions automatise la collecte des preuves, l'exécution des agents et la publication d'un commentaire de revue. Les rapports complets sont disponibles en Markdown et JSON.

## Démarrage rapide (GitHub uniquement)

1. Assurez-vous que les workflows sont présents sur la branche `main`.
2. Créez une **GitHub Issue** décrivant les exigences et critères d'acceptation.
3. Créez une branche **dans le même dépôt**, effectuez vos modifications et ouvrez une Pull Request.
4. Ajoutez `Closes #12` dans la description de la PR (remplacez `12` par le numéro de votre issue).
5. Dans **Actions**, suivez `PR Evidence Checks`, puis `AI Code Review`.

**Aucune installation locale ni configuration de secrets n'est nécessaire.** GitHub Actions utilise automatiquement `GITHUB_TOKEN` et exécute Ollama avec le modèle `qwen2.5-coder:1.5b`. Les paramètres du prototype sont définis dans les fichiers `.github/workflows/`.

Par défaut, le modèle est `qwen2.5-coder:1.5b` afin de limiter le coût CPU. Il peut être changé dans **Settings → Secrets and variables → Actions → Variables** avec `REVIEW_OLLAMA_MODEL`.

La publication nécessite les permissions GitHub prévues dans `ai-review.yml`, notamment `issues: write` et `pull-requests: write`.

### Déroulement

- `tests.yml` — **Reviewer Unit Tests** : exécute les tests unitaires du robot et sa démonstration. Peut également être lancé manuellement.
- `evidence.yml` — **PR Evidence Checks** : analyse le code de la PR avec Ruff, Bandit, Gitleaks et pytest dans un conteneur isolé. Les preuves sont enregistrées dans un artefact associé au commit.
- `ai-review.yml` — **AI Code Review** : récupère les preuves, lit l'issue GitHub et le diff, puis exécute les sept agents avec Ollama. Il publie ou actualise un commentaire sur la PR et conserve les rapports complets pendant 14 jours.

Le contrôle des preuves peut échouer tout en produisant un artefact exploitable par les agents. Une analyse incomplète reste signalée comme telle.

**La décision est une recommandation uniquement : aucune approbation ou fusion automatique.**

## Limitations

- Les revues automatiques concernent uniquement les PRs provenant du même dépôt. Les forks externes sont ignorés.
- Chaque PR doit référencer une GitHub Issue avec `Closes #N`, `Fixes #N` ou `Resolves #N`. Une seule issue est analysée.
- L'analyse repose principalement sur le diff, les exigences et les résultats des outils. Elle ne couvre pas nécessairement tout le dépôt.
- Ollama fonctionne sur CPU dans GitHub Actions. L'exécution peut être relativement longue.
- Les constats IA sont indicatifs et doivent être validés par une personne.

## Mode local facultatif

Installer le projet et exécuter la démonstration :

```bash
python -m pip install -e .
python -m unittest discover -s tests -v
python -m review.cli demo
```

Pour analyser une PR manuellement, configurez `GITHUB_TOKEN` et démarrez Ollama :

```bash
python -m review.cli review --repo OWNER/REPO --pr 2 --standards examples/STANDARDS.md
```

L'option `--issue` est facultative lorsque la PR référence explicitement une issue. L'option `--publish` permet de publier le rapport sur GitHub.


## Structure du projet

- `review/agents/` : les sept agents spécialisés et leurs instructions.
- `review/orchestrator.py`, `models.py`, `llm.py` : orchestration, modèles de données et communication avec Ollama.
- `review/connectors.py`, `publish.py`, `report.py` : intégration GitHub et génération des rapports.
- `review/ci.py`, `scripts/collect_evidence.py`, `Dockerfile.runner` : collecte et validation des preuves.
- `.github/workflows/` : automatisation GitHub Actions.
- `example_app/`, `examples/`, `tests/` : application de démonstration, exemples et tests.

Voir [docs/GITHUB_ACTIONS.md](docs/GITHUB_ACTIONS.md) pour les détails techniques des workflows.