import selenium 
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager # sustituye al archivo
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import warnings
warnings.filterwarnings('ignore')
import requests as req
from bs4 import BeautifulSoup as bs
import asyncio
PATH = ChromeDriverManager().install()

class google:
    def __init__(self):
        self.options=Options()
        self.options.add_experimental_option('excludeSwitches', ['enable-automation'])
        self.options.add_experimental_option('useAutomationExtension', False)
        self.options.add_argument('--start-maximized')         # comienza maximizado     # adblocker
        self.options.headless=True
        self.driver=webdriver.Chrome(PATH, options=self.options)
        self.url='https://www.google.es/search?q='
    def buscar(self,busqueda):
        self.driver.get(self.url+busqueda)
        time.sleep(3)
        try:
            self.driver.find_element(By.CSS_SELECTOR, '#W0wltc > div').click()
        except:
            pass
    def mostrar(self):
        ruta='div.yuRUbf'
        self.dic={e.find_element(By.CSS_SELECTOR, 'h3').text:e.find_element(By.CSS_SELECTOR, 'a').get_attribute('href') for e in self.driver.find_elements(By.CSS_SELECTOR, ruta) if e.text !='' }
        self.lista=[e.find_element(By.CSS_SELECTOR, 'h3').text for e in self.driver.find_elements(By.CSS_SELECTOR, ruta) if e.text !='']
        return self.lista
    def entrar_en_url(self,titulo,cookies=None):
        self.cookies=cookies
        self.driver.get(self.dic[self.lista[titulo]])
    def cerrar(self):
        self.driver.quit()

class google_academy:
    def __init__(self):
        self.options=Options()
        self.options.add_experimental_option('excludeSwitches', ['enable-automation'])
        self.options.add_experimental_option('useAutomationExtension', False)
        self.options.add_argument('--start-maximized')         # comienza maximizado     # adblocker
        self.options.headless=False
        self.driver=webdriver.Chrome(PATH, options=self.options)
        self.url='https://scholar.google.es/scholar?hl=es&as_sdt=0%2C5&as_vis=1&q='

    def asincrono(funcion):
        def eventos(*args, **kwargs):
            return asyncio.get_event_loop().run_in_executor(None, funcion, *args, **kwargs)
        return eventos
    
    def buscar(self):
        self.busqueda = input()
        self.driver.get(self.url+self.busqueda)
        time.sleep(3)
        try:
            self.driver.find_element(By.CSS_SELECTOR, '#W0wltc > div').click()
        except:
            pass
    @asincrono
    def diccionario(self):
        time.sleep(3)
        dic_1={}
        ls_1=[]
        pg=1
        while pg<=42:
            try:
                time.sleep(3)
                ruta = 'div.gs_ri'
                for e in self.driver.find_elements(By.CSS_SELECTOR, ruta): 
                    if e.text != '':
                        dic_1[e.find_element(By.CSS_SELECTOR, 'h3').text]=e.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
                        ls_1.append([e.find_element(By.CSS_SELECTOR, 'h3').text for e in self.driver.find_elements(By.CSS_SELECTOR, ruta) if e.text !=''])
                self.driver.find_element(By.CSS_SELECTOR, '#gs_n > center > table > tbody > tr > td:nth-child(12) > a > b').click()
                pg+=1
            except:
                respuesta=input()
                if respuesta=='stop':
                    return dic_1
            continue
        return dic_1
    @asincrono
    def info(self,listas):
        autores=[]
        descripcion=[]
        año=[]
        for link in listas:
            try:
                self.driver.get(link)
                time.sleep(3)
                todo=self.driver.find_element(By.CSS_SELECTOR,'#citation').text.split(self.driver.find_element(By.CSS_SELECTOR,'#citation').find_element(By.CSS_SELECTOR, 'i').text)[0]
                autores.append(''.join(todo.split()[:-2]))
                descripcion.append(self.driver.find_element(By.CSS_SELECTOR,'#citation').find_element(By.CSS_SELECTOR, 'i').text)
                año.append(todo.split()[-1].strip('.'))
            except:
                autores.append('NaN')
                descripcion.append('NaN')
                año.append('NaN')
            continue
        self.dic_2={'autores':autores,'descripcion':descripcion,'año':año}
        return self.dic_2

    def cerrar(self):
        self.driver.quit()