# selenium-cicd-tp
1. Mise en place du projet
J'ai commencé par créer un dépôt GitHub nommé "selenium-cicd-tp" et structuré mon projet :
- src/ : contient l'application web (index.html, style.css, script.js)
- tests/ : contient les tests Selenium et le requirements.txt
- .github/workflows/ci-cd.yml : fichier de configuration du pipeline CI/CD

2. Configuration de Selenium
J'ai installé les dépendances (selenium, pytest, pytest-html, webdriver-manager) via pip.
Ensuite, j'ai écrit des tests en Python utilisant pytest et Selenium :
- Vérification du chargement de la page
- Test de l'addition
- Test de la division par zéro
- Test de toutes les opérations

3. Exécution locale des tests
J'ai exécuté `pytest` localement pour générer un rapport HTML et inspecté les résultats pour m'assurer que tout fonctionnait.


6. Exercices pratiques
- Ajout de tests pour les nombres décimaux et négatifs
- Vérification des aspects visuels (couleurs, tailles des composants)
- Refactorisation des tests selon le Page Object Pattern
