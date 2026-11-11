# GitHub Actions — Revue de code IA

Le projet utilise trois workflows GitHub Actions pour automatiser les tests, la collecte des preuves et la revue de code par les sept agents IA.

## Workflows

| Workflow | Rôle |
|---|---|
| `tests.yml` — Reviewer Unit Tests | Exécute les tests unitaires du robot et la démonstration. |
| `evidence.yml` — PR Evidence Checks | Exécute Ruff, Bandit, Gitleaks et pytest sur le code de la PR. |
| `ai-review.yml` — AI Code Review | Lance les sept agents avec Ollama et publie la synthèse sur GitHub. |

## Fonctionnement

1. Une Pull Request est créée ou mise à jour avec une GitHub Issue liée (`Closes #N`).
2. Les tests du robot et la collecte des preuves sont lancés automatiquement.
3. Les preuves sont générées dans un conteneur Docker isolé.
4. À la fin de la collecte, le workflow IA récupère le diff, l'issue et les résultats des contrôles.
5. Les sept agents analysent ces informations avec Ollama.
6. Un commentaire de synthèse est publié ou actualisé sur la PR. Les rapports Markdown et JSON sont conservés comme artefacts GitHub Actions.

Le workflow IA peut s'exécuter même lorsque les contrôles du code ont échoué, afin de signaler les problèmes détectés.

## Exécution et sécurité

Les workflows s'exécutent sur des runners GitHub temporaires. Aucune installation locale ni configuration de jeton personnel n'est nécessaire.

La collecte des preuves utilise un conteneur Docker sans accès réseau. Elle est séparée du workflow IA, qui dispose des permissions nécessaires pour publier un commentaire sur GitHub.

Le modèle Ollama utilisé est `qwen2.5-coder:7b`, exécuté sur CPU.

## Limites

- Seules les PRs provenant du même dépôt sont automatiquement analysées.
- Une seule GitHub Issue est prise en compte par revue.
- Le périmètre de l'analyse statique et de la couverture est défini dans `evidence.yml` (actuellement `example_app`).
- Les résultats IA constituent une aide à la revue, pas une approbation automatique.

Les workflows peuvent être adaptés directement dans les fichiers `.github/workflows/`.