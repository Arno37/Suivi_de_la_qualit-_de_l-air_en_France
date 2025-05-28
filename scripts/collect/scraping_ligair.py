import time
import json
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
import logging

# Configuration du logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class LigAirSeleniumScraperImproved:
    """Version améliorée du scraper Selenium pour Lig'Air"""
    
    def __init__(self, headless=False):  # Mode visible par défaut pour debug
        self.headless = headless
        self.driver = None
        self.setup_driver()
    
    def setup_driver(self):
        """Configuration du driver Chrome avec installation automatique"""
        try:
            print("🔄 Installation automatique de ChromeDriver...")
            
            service = Service(ChromeDriverManager().install())
            
            chrome_options = Options()
            if self.headless:
                chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--window-size=1920,1080")
            chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
            
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.driver.implicitly_wait(10)
            
            print("✅ Driver Chrome initialisé avec succès")
            
        except Exception as e:
            print(f"❌ Erreur lors de l'initialisation du driver: {e}")
            raise
    
    def wait_for_map_to_load(self):
        """Attendre que la carte et les données soient complètement chargées"""
        try:
            wait = WebDriverWait(self.driver, 60)  # Encore plus de temps
            
            print("⏳ Attente du chargement de la carte...")
            # Attendre que la carte Leaflet soit présente
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, "leaflet-container")))
            print("✅ Conteneur Leaflet trouvé")
            
            # Attendre que les tuiles de la carte se chargent
            print("⏳ Attente des tuiles de la carte...")
            time.sleep(8)
            
            # Attendre et vérifier périodiquement les données
            print("⏳ Attente des données d'indices (vérification toutes les 5 secondes)...")
            
            max_attempts = 12  # 12 x 5 secondes = 1 minute
            for attempt in range(max_attempts):
                print(f"   🔍 Tentative {attempt + 1}/{max_attempts}...")
                
                # Vérifier si des indices apparaissent dans le DOM
                page_source = self.driver.page_source
                
                # Rechercher des mots-clés d'indices
                indices_keywords = ["Bon", "Moyen", "Mauvais", "Dégradé", "Très bon", "Très mauvais"]
                indices_found = []
                
                for keyword in indices_keywords:
                    if keyword in page_source:
                        indices_found.append(keyword)
                
                if indices_found:
                    print(f"   ✅ Indices trouvés: {', '.join(indices_found)}")
                    
                    # Vérifier si on a des données spécifiques aux villes
                    villes_avec_indices = 0
                    villes = ["Bourges", "Chartres", "Châteauroux", "Tours", "Blois", "Orléans"]
                    
                    for ville in villes:
                        # Chercher des patterns comme "Ville: Indice" ou "Ville Indice"
                        for indice in indices_keywords:
                            if f"{ville}" in page_source and indice in page_source:
                                # Vérifier si ils sont proches dans le texte
                                ville_pos = page_source.find(ville)
                                indice_pos = page_source.find(indice, ville_pos)
                                if indice_pos != -1 and (indice_pos - ville_pos) < 200:  # Dans les 200 caractères
                                    villes_avec_indices += 1
                                    print(f"   ✅ {ville} semble avoir un indice")
                                    break
                    
                    if villes_avec_indices >= 3:
                        print(f"   🎉 {villes_avec_indices} villes avec indices détectées!")
                        return True
                
                # Vérifier les marqueurs
                try:
                    markers = self.driver.find_elements(By.CSS_SELECTOR, ".leaflet-marker-icon, .leaflet-div-icon, .leaflet-marker")
                    if markers:
                        print(f"   📍 {len(markers)} marqueurs détectés")
                        
                        # Essayer de cliquer sur un marqueur pour voir si ça donne plus d'infos
                        if attempt == 5:  # À mi-parcours, essayer de cliquer
                            print("   🖱️ Test de clic sur un marqueur...")
                            try:
                                self.driver.execute_script("arguments[0].click();", markers[0])
                                time.sleep(2)
                                
                                # Vérifier si une popup avec plus d'infos apparaît
                                popup = self.driver.find_element(By.CSS_SELECTOR, ".leaflet-popup-content")
                                if popup and popup.is_displayed():
                                    popup_text = popup.text
                                    print(f"   💬 Popup: {popup_text[:100]}...")
                                    
                                    # Fermer la popup
                                    try:
                                        close_btn = self.driver.find_element(By.CSS_SELECTOR, ".leaflet-popup-close-button")
                                        close_btn.click()
                                    except:
                                        self.driver.execute_script("document.body.click();")
                            except:
                                print("   ⚠️ Impossible de cliquer sur le marqueur")
                except:
                    pass
                
                # Attendre avant la prochaine vérification
                if attempt < max_attempts - 1:
                    time.sleep(5)
            
            print("⚠️ Timeout atteint, mais on continue avec les données disponibles...")
            return True
            
        except TimeoutException:
            print("⚠️ Timeout lors du chargement, mais on continue quand même...")
            return True
        except Exception as e:
            print(f"❌ Erreur lors du chargement: {e}")
            return False
    
    def find_and_click_markers(self):
        """Trouver et cliquer sur tous les marqueurs de la carte"""
        markers_data = []
        
        try:
            # Différents sélecteurs pour les marqueurs
            marker_selectors = [
                ".leaflet-marker-icon",
                ".leaflet-div-icon", 
                ".leaflet-marker",
                "[class*='marker']",
                "[class*='leaflet-marker']"
            ]
            
            all_markers = []
            for selector in marker_selectors:
                markers = self.driver.find_elements(By.CSS_SELECTOR, selector)
                all_markers.extend(markers)
            
            # Supprimer les doublons
            unique_markers = list(set(all_markers))
            
            print(f"🎯 Trouvé {len(unique_markers)} marqueurs potentiels")
            
            for i, marker in enumerate(unique_markers):
                try:
                    print(f"🔍 Test du marqueur {i+1}...")
                    
                    # Scroll vers le marqueur pour qu'il soit visible
                    self.driver.execute_script("arguments[0].scrollIntoView(true);", marker)
                    time.sleep(0.5)
                    
                    # Essayer de cliquer
                    self.driver.execute_script("arguments[0].click();", marker)
                    time.sleep(2)
                    
                    # Chercher une popup
                    popup_selectors = [
                        ".leaflet-popup-content",
                        ".leaflet-popup",
                        "[class*='popup']",
                        "[class*='tooltip']"
                    ]
                    
                    popup_found = False
                    for popup_selector in popup_selectors:
                        try:
                            popup = self.driver.find_element(By.CSS_SELECTOR, popup_selector)
                            if popup.is_displayed():
                                popup_text = popup.text.strip()
                                if popup_text:
                                    print(f"✅ Popup trouvée: {popup_text[:100]}...")
                                    markers_data.append({
                                        "marqueur": i+1,
                                        "contenu": popup_text,
                                        "selector_used": popup_selector
                                    })
                                    popup_found = True
                                    
                                    # Fermer la popup
                                    try:
                                        close_btn = self.driver.find_element(By.CSS_SELECTOR, ".leaflet-popup-close-button, .popup-close, [class*='close']")
                                        close_btn.click()
                                    except:
                                        # Cliquer ailleurs pour fermer
                                        self.driver.execute_script("document.body.click();")
                                    
                                    time.sleep(1)
                                    break
                        except:
                            continue
                    
                    if not popup_found:
                        print(f"❌ Pas de popup pour le marqueur {i+1}")
                        
                except Exception as e:
                    print(f"⚠️ Erreur avec le marqueur {i+1}: {e}")
                    continue
            
            return markers_data
            
        except Exception as e:
            print(f"❌ Erreur lors de la recherche des marqueurs: {e}")
            return []
    
    def extract_javascript_data(self):
        """Extraire les données directement depuis JavaScript"""
        try:
            print("🔍 Extraction des données JavaScript...")
            
            js_data = self.driver.execute_script("""
                var result = {
                    mapHandler_exists: typeof mapHandler !== 'undefined',
                    window_vars: [],
                    map_data: null
                };
                
                // Recherche de variables globales intéressantes
                for (var prop in window) {
                    if (typeof window[prop] === 'object' && window[prop] !== null) {
                        if (prop.toLowerCase().includes('map') || 
                            prop.toLowerCase().includes('data') || 
                            prop.toLowerCase().includes('indice')) {
                            result.window_vars.push(prop);
                        }
                    }
                }
                
                // Essayer d'accéder aux données de la carte
                if (typeof mapHandler !== 'undefined') {
                    try {
                        if (mapHandler.mapInitialization && mapHandler.mapInitialization.map) {
                            var layers = [];
                            mapHandler.mapInitialization.map.eachLayer(function(layer) {
                                if (layer.options && (layer.options.title || layer.options.alt)) {
                                    layers.push({
                                        title: layer.options.title || layer.options.alt,
                                        type: layer.constructor.name
                                    });
                                }
                            });
                            result.map_layers = layers;
                        }
                    } catch(e) {
                        result.map_error = e.toString();
                    }
                }
                
                return result;
            """)
            
            return js_data
            
        except Exception as e:
            print(f"⚠️ Erreur lors de l'extraction JavaScript: {e}")
            return {}
    
    def extract_data_from_dom(self):
        """Extraire les données directement du DOM sans cliquer"""
        try:
            print("🔍 Extraction directe depuis le DOM...")
            
            data_found = []
            page_source = self.driver.page_source
            villes = ["Bourges", "Chartres", "Châteauroux", "Tours", "Blois", "Orléans"]
            indices_keywords = ["Bon", "Moyen", "Mauvais", "Dégradé", "Très bon", "Très mauvais", "Extrêmement mauvais"]
            
            # 1. Recherche avancée d'indices pour chaque ville
            for ville in villes:
                print(f"   🔍 Recherche détaillée pour {ville}...")
                
                # Méthode 1: Recherche par XPath avec contexte
                try:
                    # Chercher des éléments contenant la ville
                    ville_elements = self.driver.find_elements(By.XPATH, f"//*[contains(text(), '{ville}')]")
                    
                    for ville_element in ville_elements:
                        # Chercher dans l'élément parent et ses voisins
                        try:
                            parent = ville_element.find_element(By.XPATH, "..")
                            parent_text = parent.text.strip()
                            
                            # Vérifier si un indice est mentionné près de la ville
                            for indice in indices_keywords:
                                if indice in parent_text and ville in parent_text:
                                    data_found.append({
                                        "ville": ville,
                                        "indice_detecte": indice,
                                        "contenu_complet": parent_text,
                                        "methode": "xpath_parent_context"
                                    })
                                    print(f"   ✅ {ville} -> {indice} (contexte parent)")
                                    break
                            
                            # Chercher dans les éléments suivants/précédents
                            try:
                                next_sibling = ville_element.find_element(By.XPATH, "following-sibling::*[1]")
                                next_text = next_sibling.text.strip()
                                for indice in indices_keywords:
                                    if indice in next_text:
                                        data_found.append({
                                            "ville": ville,
                                            "indice_detecte": indice,
                                            "contenu_complet": f"{ville} -> {next_text}",
                                            "methode": "xpath_sibling_context"
                                        })
                                        print(f"   ✅ {ville} -> {indice} (élément suivant)")
                                        break
                            except:
                                pass
                                
                        except:
                            continue
                            
                except:
                    continue
                
                # Méthode 2: Recherche par proximité dans le texte brut
                ville_positions = []
                start = 0
                while True:
                    pos = page_source.find(ville, start)
                    if pos == -1:
                        break
                    ville_positions.append(pos)
                    start = pos + 1
                
                for pos in ville_positions:
                    # Extraire un contexte de 300 caractères autour de la ville
                    context_start = max(0, pos - 150)
                    context_end = min(len(page_source), pos + 150)
                    context = page_source[context_start:context_end]
                    
                    for indice in indices_keywords:
                        if indice in context:
                            data_found.append({
                                "ville": ville,
                                "indice_detecte": indice,
                                "contexte": context.replace('\n', ' ').strip(),
                                "methode": "text_proximity_search"
                            })
                            print(f"   ✅ {ville} -> {indice} (proximité texte)")
                            break
            
            # 2. Recherche dans les attributs des éléments
            try:
                print("   🔍 Recherche dans les attributs des éléments...")
                
                # Chercher des éléments avec des attributs contenant des villes ou indices
                for ville in villes:
                    elements_with_ville = self.driver.find_elements(By.CSS_SELECTOR, f"[title*='{ville}'], [alt*='{ville}'], [data-city*='{ville}']")
                    
                    for element in elements_with_ville:
                        # Vérifier tous les attributs
                        attributes = self.driver.execute_script("""
                            var attrs = {};
                            for (var i = 0; i < arguments[0].attributes.length; i++) {
                                var attr = arguments[0].attributes[i];
                                attrs[attr.name] = attr.value;
                            }
                            return attrs;
                        """, element)
                        
                        element_text = element.text.strip()
                        
                        # Chercher des indices dans les attributs ou le texte
                        for indice in indices_keywords:
                            if any(indice in str(value) for value in attributes.values()) or indice in element_text:
                                data_found.append({
                                    "ville": ville,
                                    "indice_detecte": indice,
                                    "element_attributes": attributes,
                                    "element_text": element_text,
                                    "methode": "element_attributes_search"
                                })
                                print(f"   ✅ {ville} -> {indice} (attributs élément)")
                                break
                                
            except Exception as e:
                print(f"   ⚠️ Erreur dans la recherche par attributs: {e}")
            
            # 3. Recherche dans les scripts JavaScript pour des données JSON
            try:
                print("   🔍 Recherche dans les scripts JavaScript...")
                scripts = self.driver.find_elements(By.TAG_NAME, "script")
                for script in scripts:
                    script_content = script.get_attribute("innerHTML")
                    if script_content:
                        # Chercher des patterns JSON avec villes et indices
                        import re
                        
                        # Pattern pour des objets JSON contenant des villes
                        for ville in villes:
                            if ville in script_content:
                                # Extraire le contexte autour de la ville dans le script
                                ville_pos = script_content.find(ville)
                                context_start = max(0, ville_pos - 200)
                                context_end = min(len(script_content), ville_pos + 200)
                                js_context = script_content[context_start:context_end]
                                
                                for indice in indices_keywords:
                                    if indice in js_context:
                                        data_found.append({
                                            "ville": ville,
                                            "indice_detecte": indice,
                                            "js_context": js_context,
                                            "methode": "javascript_context_search"
                                        })
                                        print(f"   ✅ {ville} -> {indice} (JavaScript)")
                                        break
                                        
            except Exception as e:
                print(f"   ⚠️ Erreur dans la recherche JavaScript: {e}")
            
            print(f"   📊 Total: {len(data_found)} associations ville-indice trouvées")
            return data_found
            
        except Exception as e:
            print(f"⚠️ Erreur lors de l'extraction DOM: {e}")
            return []
    
    def scrape_complete_data(self):
        """Scraping complet avec toutes les méthodes"""
        try:
            url = "https://www.ligair.fr/"
            print(f"🌐 Chargement de {url}")
            
            self.driver.get(url)
            
            # Attendre le chargement complet
            if not self.wait_for_map_to_load():
                print("❌ Impossible de charger la carte")
                return None
            
            data = {
                "date_collecte": datetime.now().isoformat(),
                "source": "ligair_selenium_improved",
                "url": url,
                "villes_dans_source": [],
                "marqueurs_data": [],
                "javascript_data": {},
                "page_title": self.driver.title
            }
            
            # 1. Recherche des villes dans le source après JS
            page_source = self.driver.page_source
            villes_connues = ["Bourges", "Chartres", "Châteauroux", "Tours", "Blois", "Orléans"]
            for ville in villes_connues:
                if ville in page_source:
                    data["villes_dans_source"].append(ville)
            
            # 2. Cliquer sur les marqueurs
            print("\n🎯 Recherche et clic sur les marqueurs...")
            data["marqueurs_data"] = self.find_and_click_markers()
            
            # 2.5. Extraction directe du DOM (nouvelle méthode)
            print("\n🔍 Extraction directe depuis le DOM...")
            data["dom_data"] = self.extract_data_from_dom()
            
            # 3. Extraction JavaScript
            print("\n⚡ Extraction des données JavaScript...")
            data["javascript_data"] = self.extract_javascript_data()
            
            # 4. Screenshot pour debug
            if not self.headless:
                screenshot_path = f"data_output/ligair_screenshot_{datetime.now().strftime('%Y%m%d_%H%M')}.png"
                self.driver.save_screenshot(screenshot_path)
                print(f"📸 Screenshot sauvegardé: {screenshot_path}")
            
            print(f"\n📊 Résultats:")
            print(f"   - Villes trouvées: {len(data['villes_dans_source'])}")
            print(f"   - Marqueurs avec données: {len(data['marqueurs_data'])}")
            print(f"   - Données DOM extraites: {len(data['dom_data'])}")
            print(f"   - Variables JS trouvées: {len(data['javascript_data'].get('window_vars', []))}")
            
            return data
            
        except Exception as e:
            print(f"❌ Erreur lors du scraping: {e}")
            return None
    
    def save_data_to_json(self, data, filename):
        """Sauvegarde les données en JSON"""
        try:
            os.makedirs('data_output', exist_ok=True)
            filepath = f"data_output/{filename}"
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            print(f"💾 Données sauvegardées dans {filepath}")
            
        except Exception as e:
            print(f"❌ Erreur lors de la sauvegarde: {e}")
    
    def close(self):
        """Fermer le driver"""
        if self.driver:
            self.driver.quit()
            print("🔒 Driver fermé")

def main():
    """Fonction principale"""
    scraper = None
    try:
        print("=== SCRAPER LIG'AIR AMÉLIORÉ ===")
        print("Mode: Fenêtre visible pour debug")
        
        scraper = LigAirSeleniumScraperImproved(headless=False)
        
        print("\n🔄 Début du scraping amélioré...")
        data = scraper.scrape_complete_data()
        
        if data:
            filename = f"ligair_selenium_improved_{datetime.now().strftime('%Y%m%d_%H%M')}.json"
            scraper.save_data_to_json(data, filename)
            print(f"\n🎉 Scraping terminé ! Données dans data_output/{filename}")
            
            # Affichage des résultats
            if data["marqueurs_data"]:
                print("\n📍 DONNÉES DES MARQUEURS TROUVÉES:")
                for marqueur in data["marqueurs_data"]:
                    print(f"   {marqueur['marqueur']}: {marqueur['contenu'][:100]}...")
            else:
                print("\n⚠️ Aucune donnée de marqueur trouvée")
            
            if data["dom_data"]:
                print("\n🔍 DONNÉES DOM TROUVÉES:")
                for dom_item in data["dom_data"]:
                    if "ville" in dom_item and "indice_detecte" in dom_item:
                        print(f"   {dom_item['ville']}: {dom_item['indice_detecte']} ({dom_item['methode']})")
                    elif "ville" in dom_item:
                        contenu = dom_item.get('contenu_complet', dom_item.get('contenu', str(dom_item)))
                        print(f"   {dom_item['ville']}: {contenu[:100]}...")
                    else:
                        print(f"   {dom_item['methode']}: {str(dom_item)[:100]}...")
            else:
                print("\n⚠️ Aucune donnée DOM trouvée")
        else:
            print("❌ Échec du scraping")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        
    finally:
        if scraper:
            scraper.close()

if __name__ == "__main__":
    main() 