import pytest                   # Framework de test en Python
import time                     # Pour mesurer le temps d’exécution
import os                       # Pour manipuler les chemins de fichiers et les variables d’environnement
from selenium import webdriver  # Pilote Selenium pour automatiser le navigateur
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager  # Pour télécharger automatiquement le bon ChromeDriver

class TestCalculator:
    # Fixture pytest : initialise et termine le driver une seule fois pour toute la classe de tests
    @pytest.fixture(scope="class")
    def driver(self):
        """Configuration du driver Chrome pour les tests"""
        chrome_options = Options()
        # Si on est en CI/CD (variable d’environnement CI définie), on lance Chrome en mode "headless"
        if os.getenv('CI'):
            chrome_options.add_argument('--headless')              # Pas d’interface graphique
            chrome_options.add_argument('--no-sandbox')            # Option de sécurité
            chrome_options.add_argument('--disable-dev-shm-usage') # Évite certains problèmes de mémoire
            chrome_options.add_argument('--disable-gpu')           # Désactive l’accélération GPU
            chrome_options.add_argument('--window-size=1920,1080')  # Taille de la fenêtre virtuelle

        # Télécharge ou réutilise le ChromeDriver adapté à la version de Chrome installée
        service = Service(ChromeDriverManager().install())
        # Lance le navigateur Chrome avec les options définies
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.implicitly_wait(10)  # Attend jusqu’à 10 secondes pour trouver un élément avant d’échouer
        yield driver              # Rend le driver disponible aux tests
        driver.quit()             # Ferme le navigateur à la fin des tests

    def test_page_loads(self, driver):
        """Test 1 : Vérifier que la page se charge correctement"""
        # Construit le chemin absolu vers le fichier index.html
        file_path = os.path.abspath("../src/index.html")
        driver.get(f"file://{file_path}")  # Ouvre la page dans le navigateur
        # Vérifie que le titre contient bien "Calculatrice Simple"
        assert "Calculatrice Simple" in driver.title
        # Vérifie que les champs et le bouton sont bien affichés
        assert driver.find_element(By.ID, "num1").is_displayed()
        assert driver.find_element(By.ID, "num2").is_displayed()
        assert driver.find_element(By.ID, "operation").is_displayed()
        assert driver.find_element(By.ID, "calculate").is_displayed()

    def test_addition(self, driver):
        """Test 2 : Tester l'addition"""
        file_path = os.path.abspath("../src/index.html")
        driver.get(f"file://{file_path}")
        # Saisit 10 dans le premier champ
        driver.find_element(By.ID, "num1").send_keys("10")
        # Saisit 5 dans le deuxième champ
        driver.find_element(By.ID, "num2").send_keys("5")
        # Sélectionne l’opération "add" dans la liste déroulante
        select = Select(driver.find_element(By.ID, "operation"))
        select.select_by_value("add")
        # Clique sur le bouton "calculate"
        driver.find_element(By.ID, "calculate").click()
        # Attend que le résultat apparaisse puis vérifie qu’il est correct
        result = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "result"))
        )
        assert "Résultat: 15" in result.text

    def test_division_by_zero(self, driver):
        """Test 3 : Tester la division par zéro"""
        file_path = os.path.abspath("../src/index.html")
        driver.get(f"file://{file_path}")
        # Récupère les éléments pour pouvoir les effacer ensuite
        num1_elem = driver.find_element(By.ID, "num1")
        num2_elem = driver.find_element(By.ID, "num2")
        # Efface les valeurs précédentes et saisit de nouvelles valeurs
        num1_elem.clear()
        num1_elem.send_keys("10")
        num2_elem.clear()
        num2_elem.send_keys("0")
        # Sélectionne la division
        select = Select(driver.find_element(By.ID, "operation"))
        select.select_by_value("divide")
        driver.find_element(By.ID, "calculate").click()
        # Vérifie que le message d’erreur s’affiche
        result = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "result"))
        )
        assert "Erreur: Division par zéro" in result.text

    def test_all_operations(self, driver):
        """Test 4 : Tester toutes les opérations avec une boucle"""
        file_path = os.path.abspath("../src/index.html")
        driver.get(f"file://{file_path}")
        # Liste des opérations à tester : (valeur de l’option, num1, num2, résultat attendu)
        operations = [
            ("add", "8", "2", "10"),
            ("subtract", "8", "2", "6"),
            ("multiply", "8", "2", "16"),
            ("divide", "8", "2", "4")
        ]
        for op, num1, num2, expected in operations:
            # Efface les anciens nombres
            elem1 = driver.find_element(By.ID, "num1")
            elem2 = driver.find_element(By.ID, "num2")
            elem1.clear()
            elem2.clear()
            # Saisit les nouvelles valeurs
            elem1.send_keys(num1)
            elem2.send_keys(num2)
            # Choisit l’opération dans le menu déroulant
            select = Select(driver.find_element(By.ID, "operation"))
            select.select_by_value(op)
            # Lance le calcul
            driver.find_element(By.ID, "calculate").click()
            # Vérifie le résultat
            result = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "result"))
            )
            assert f"Résultat: {expected}" in result.text
            time.sleep(1)  # Petite pause pour voir l’évolution (inutile en CI)
            
    def test_nombres_negatifs(self, driver):
        """Test 5 : Tester les nombres négatifs"""
        file_path = os.path.abspath("../src/index.html")
        driver.get(f"file://{file_path}")
        # Saisit -10 dans le premier champ
        driver.find_element(By.ID, "num1").send_keys("-10")
        # Saisit -5 dans le deuxième champ
        driver.find_element(By.ID, "num2").send_keys("-5")
        # Sélectionne l’opération "add"
        select = Select(driver.find_element(By.ID, "operation"))
        select.select_by_value("add")
        # Clique sur le bouton "calculate"
        driver.find_element(By.ID, "calculate").click()
        # Vérifie que le résultat est correct
        result = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "result"))
        )
        assert "Résultat: -15" in result.text
        
    def test_nombres_decimaux(self, driver):
        """Test 6 : Tester les nombres décimaux"""
        file_path = os.path.abspath("../src/index.html")
        driver.get(f"file://{file_path}")
        # Saisit 10.5 dans le premier champ
        driver.find_element(By.ID, "num1").send_keys("10.5")
        # Saisit 2.5 dans le deuxième champ
        driver.find_element(By.ID, "num2").send_keys("2.5")
        # Sélectionne l’opération "add"
        select = Select(driver.find_element(By.ID, "operation"))
        select.select_by_value("add")
        # Clique sur le bouton "calculate"
        driver.find_element(By.ID, "calculate").click()
        # Vérifie que le résultat est correct
        result = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "result"))
        )
        assert "Résultat: 13" in result.text
        
    def test_user_interface(self, driver, color, tailles):
        """Test 7 : Vérifier l'interface utilisateur"""
        file_path = os.path.abspath("../src/index.html")
        driver.get(f"file://{file_path}")
        # Vérifie que les champs ont la bonne couleur de fond
        num1_elem = driver.find_element(By.ID, "num1")
        num2_elem = driver.find_element(By.ID, "num2")
        assert num1_elem.value_of_css_property("background-color") == color
        assert num2_elem.value_of_css_property("background-color") == color
        # Vérifie que le bouton a la bonne taille
        button_elem = driver.find_element(By.ID, "calculate")
        assert button_elem.size['width'] == tailles['width']
        assert button_elem.size['height'] == tailles['height']

if __name__ == "__main__":
    # Permet de lancer les tests directement avec python test_selenium.py
    pytest.main(["-v", "--html=report.html", "--self-contained-html"])
