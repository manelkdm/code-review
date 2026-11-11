# Guide d'utilisation

Ce guide présente les étapes nécessaires pour utiliser le prototype de revue automatisée avec GitHub Actions.

## 1. Préparer une GitHub Issue

Créer une issue décrivant la fonctionnalité attendue et ses critères d'acceptation.

Par exemple :

**Titre :** Ajouter une fonction de soustraction

**Description :** Ajouter une fonction `subtract(a, b)` dans `example_app/calculator.py`.

**Critères d'acceptation :**
- Retourner `a - b`.
- Prendre en charge les nombres positifs, négatifs et décimaux.

## 2. Créer une pull request

Créer une branche dans le dépôt, effectuer les modifications et ouvrir une pull request.

Dans la description, ajouter une référence explicite à l'issue :

```text
Closes #1
```

Le système récupère automatiquement les exigences de cette issue.

## 3. Consulter les workflows

L'ouverture ou la mise à jour de la pull request déclenche :

1. `Reviewer Unit Tests` : exécution des tests du prototype.
2. `PR Evidence Checks` : collecte des résultats Ruff, Bandit, Gitleaks et pytest.
3. `AI Code Review` : exécution des sept agents après la collecte des preuves.

Les workflows s'exécutent sur des runners GitHub hébergés.

L'onglet **Actions** permet de consulter leurs résultats et les journaux d'exécution.

## 4. Consulter la revue

Une fois l'analyse terminée, le prototype publie ou met à jour un commentaire sur la pull request.

Ce commentaire contient :

- La recommandation globale et ses motifs.
- L'état et le résumé des sept agents.
- Une sélection des principaux constats.

Le commentaire est une synthèse. Les rapports complets peuvent être téléchargés dans les artefacts de l'exécution **AI Code Review**.

## 5. Interpréter les résultats

Les observations générées par les agents ne constituent pas une approbation automatique.

Le développeur doit vérifier les constats, examiner les preuves et décider des corrections nécessaires.

Un résultat favorable ne garantit pas l'absence de défauts.

## 6. Limites et adaptation

Le prototype a été développé et testé principalement sur l'application `example_app`.

Les chemins d'analyse peuvent être configurés dans GitHub Actions, mais une intégration à un autre dépôt peut nécessiter des ajustements supplémentaires.

Les pull requests provenant de forks externes ne sont pas automatiquement analysées.

Le modèle utilisé dans les workflows est `qwen2.5-coder:7b`. Son exécution sur CPU peut être relativement longue.

## 7. Exécution locale facultative

Pour tester uniquement le fonctionnement du prototype :

```bash
python -m pip install -e .
python -m unittest discover -s tests -v
python -m review.cli demo
```

La commande `demo` utilise des réponses simulées. Elle ne lance pas Ollama et ne constitue pas une revue réelle.

L'utilisation normale du prototype ne nécessite aucune installation locale.

## Références

- [Dépôt GitHub](https://github.com/manelkdm/code-review)
- [Exemple de pull request analysée](https://github.com/manelkdm/code-review/pull/4)
- [GitHub Actions](GITHUB_ACTIONS.md)
- [Résultats de validation](VALIDATION.md)