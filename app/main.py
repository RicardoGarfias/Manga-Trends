"""
Nombre: Juan Ricardo Garfias Arellanes
grupo: 952
Fecha: 2/25/2025


1.Web Scraping de amazon porque mercadolibre no me agarro
"""""


import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
def amazon (busqueda,num_imagenes):
   driver = ChromeDriverManager().install()
   s = Service(driver)
   opc = Options()
   opc.add_argument("--window-size=1020,1200")
   navegador = webdriver.Chrome(service=s, options=opc)
   navegador.get("https://www.amazon.com.mx")
   time.sleep(10)
   searchbarra = navegador.find_element(By.ID, "twotabsearchtextbox")
   searchbarra.click()
   time.sleep(2)
   searchbarra.send_keys("Samsung s24")
   time.sleep(2)
   btnlupa = navegador.find_element(By.ID, "nav-search-submit-button")
   btnlupa.click()
   time.sleep(1)


   for index in range(num_imagenes):
       navegador.save_screenshot(f"imagenes/{busqueda}_{index}.png")
       time.sleep(1)
       link = navegador.find_element(By.LINK_TEXT, "Siguiente")
       link.click()
       time.sleep(1)
   navegador.close()


















if __name__ == "__main__":


     busqueda = "Samsung s24"


     num_imagenes = 3


     amazon(busqueda, num_imagenes)
