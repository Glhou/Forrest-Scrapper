import os
import selenium
from pprint import pprint, pformat
from selenium import webdriver
import time
from PIL import Image
import io
import requests
from webdrivermanager.chrome import ChromeDriverManager
from selenium.common.exceptions import ElementClickInterceptedException



def download(data,username,password):
    for matiere in data:
        download_dir = os.getcwd() + "\\" + matiere["title"] + "\\" # for linux/*nix, download_dir="/usr/Public"
        options = webdriver.ChromeOptions()
        profile = {"plugins.plugins_list": [{"enabled": False, "name": "Brave PDF Viewer"}], # Disable Chrome's PDF Viewer
                    "download.default_directory": download_dir , "download.extensions_to_open": "applications/pdf"}
        options.add_experimental_option("prefs", profile)
        options.add_argument("--headless")
        options.binary_location = "C:\Program Files\BraveSoftware\Brave-Browser\Application\Brave.exe"
        driver = webdriver.Chrome(options=options)
        ### On vas se connecter à sa session My
        ### On lance la page de co de my
        driver.get(matiere["documents"][0][0])
        ### Connexion à forrest via my
        driver.find_element_by_xpath("//input[@id=\"username\"]").send_keys(username)
        driver.find_element_by_xpath("//input[@type=\"password\"]").send_keys(password)
        driver.find_element_by_xpath("//button[@id=\"_submit\"]").click()
        if not os.path.exists(matiere["title"]):
            os.mkdir(matiere["title"])
        for doc in matiere["documents"]:
            doc_url = doc[0]
            doc_name = doc[1]
            ### Et on retourne sur la bonne page
            driver.get(doc_url)
            