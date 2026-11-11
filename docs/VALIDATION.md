# Validation du prototype

Ce document présente les résultats des vérifications réalisées sur le prototype et les principales limites observées.

## Tests automatisés

La suite de tests du prototype comprend **55 tests unitaires réussis**.

Ces tests vérifient notamment :

- La validation des données et des réponses du modèle.
- La gestion des preuves manquantes ou invalides.
- Le contrôle des commits et du contexte analysé.
- Les règles de recommandation.
- Le fonctionnement des connecteurs GitHub simulés.
- La génération des rapports et la publication.

Ces tests utilisent principalement des services simulés. Ils permettent de vérifier les comportements programmés sans garantir la pertinence des observations produites par l'IAG.

## Vérifications du code analysé

L'exécution du workflow `PR Evidence Checks` sur la pull request nº 4 a produit les résultats suivants :

| Vérification | Résultat |
|---|---|
| pytest | 55 tests réussis |
| Couverture de `example_app` | 90 % |
| Ruff | Réussi, aucun constat |
| Bandit | Réussi, aucun constat |
| Gitleaks | Réussi, aucun constat |

La couverture dépasse le seuil de 80 % configuré dans le prototype. Elle concerne l'application de démonstration et non l'ensemble du code du système de revue.

## Exécution réelle des sept agents

Une revue a été effectuée le **9 novembre 2026**, avec `qwen2.5-coder:7b` sur la [pull request nº 4](https://github.com/manelkdm/code-review/pull/4).

Les sept agents ont terminé leur analyse. L'étape d'analyse et de publication a nécessité environ 15 minutes sur CPU.

La GitHub Issue demandait l'ajout d'une fonction `subtract(a, b)` prenant en charge les nombres positifs, négatifs et décimaux.

La pull request ajoutait :
- Une fonction `substract(a, b)` réalisant l'opération attendue, mais avec une erreur de nom.
- Une fonction `square_root(a)` non demandée.
- Deux tests pour `square_root`, sans test supplémentaire pour la soustraction.

Les agents ont détecté plusieurs écarts, notamment le non-respect du nom demandé et l'absence de tests de soustraction.

La recommandation finale était `corrections_recommandees`.

## Limites observées

Certaines analyses ont mal interprété le code. Plusieurs agents n'ont pas clairement établi le lien entre `substract` et la fonction `subtract` demandée.

D'autres ont signalé des erreurs dans des tests de soustraction qui n'avaient pas été ajoutés.

Les résultats montrent donc que le prototype peut détecter des problèmes fonctionnels, mais qu'il produit également des constats incorrects ou insuffisamment justifiés.

Une seule revue réelle ne permet pas de mesurer statistiquement la précision, le rappel ou le gain de productivité.

## Références des exécutions

- [Reviewer Unit Tests](https://github.com/manelkdm/code-review/actions/runs/42682511193)
- [PR Evidence Checks](https://github.com/manelkdm/code-review/actions/runs/42682510820)
- [AI Code Review](https://github.com/manelkdm/code-review/actions/runs/42682633819)
- [Pull request nº 4](https://github.com/manelkdm/code-review/pull/4)

Les résultats correspondent aux exécutions citées et ne garantissent pas un fonctionnement identique sur d'autres commits ou dépôts.