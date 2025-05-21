# scraping/browser.py
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
import os

def init_browser():
    options = Options()
    options.add_argument("--window-size=1020,1200")

    # 1. Intento automático con webdriver_manager
    try:
        """
        from webdriver_manager.chrome import ChromeDriverManager
        service = Service(ChromeDriverManager().install())
        browser = webdriver.Chrome(service=service, options=options)
        print("[✓] Navegador iniciado automáticamente con webdriver_manager.")
        return browser
        #como a mi me sale un error tengo que comentar esto pero ustdes lo deben quitar para que les agarre 
        """
    except WebDriverException as e:
        print("[!] Falló el inicio automático del navegador con webdriver_manager.")
        print("   ➜ Intentando con ruta local del proyecto...")

    # 2. Intento automático con ruta fija local
    ruta_local = os.path.abspath(os.path.join(os.path.dirname(__file__), "../WebDrivers/chromedriver.exe"))
    if os.path.exists(ruta_local):
        try:
            service = Service(ruta_local)
            browser = webdriver.Chrome(service=service, options=options)
            print(f"[✓] Navegador iniciado con ruta local: {ruta_local}")
            return browser
        except Exception as e:
            print(f"[!] Error al usar chromedriver local: {e}")
    else:
        print(f"[!] No se encontró chromedriver en la ruta local esperada: {ruta_local}")

    # 3. Ruta manual si todo lo anterior falla
    chromedriver_path = input("👉 Ingresa la ruta manual del chromedriver.exe: ").strip()

    if not os.path.exists(chromedriver_path):
        raise FileNotFoundError(f"La ruta '{chromedriver_path}' no existe o es incorrecta.")

    try:
        service = Service(chromedriver_path)
        browser = webdriver.Chrome(service=service, options=options)
        print("[✓] Navegador iniciado manualmente con la ruta proporcionada.")
        return browser
    except Exception as ex:
        raise RuntimeError(f"[X] Error al iniciar el navegador manualmente: {ex}")
