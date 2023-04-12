# Schéma de base de données

Celui-ci est inclut dans le fichier schema.sql, mais voici quelque détails additionnels.

### waitlist
| Colonne | Type | Description|
| ------------- | ------------- | ------------- |
| id | INTEGER | Clé primaire, s'incrémente automatiquement, identifie le patient |
| name | TEXT | Requis, le nom du patient |
| severity | INTEGER | Requis, un nombre qui représente la gravité de la maladie/blessure du patient |
| description | TEXT | Une petite description de la maladie/blessure du patient |
| arrival | TIMESTAMP | Rempli automatiquement, le temps d'arrivée du patient |
| in_progress | INTEGER | Rempli automatiquement, un statut booléen qui indique aux autre administrateurs si le patient est présentement avec un docteur ou non. |