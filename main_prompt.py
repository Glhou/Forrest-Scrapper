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
from download import download

#Install Driver
options = webdriver.ChromeOptions()
options.binary_location = "C:\Program Files\BraveSoftware\Brave-Browser\Application\Brave.exe"
#options.add_argument("--headless")
driver = webdriver.Chrome("./chromedriver.exe", options=options)

def init_course(title,data_cat):
    return {"title" : title,"data_cat":data_cat, "documents":[]}

def enregistrer(data):
    with open("data","w",encoding='utf-8') as f:
        f.write(pformat(data))


site = "https://forrest.ginfo.centrale-marseille.fr"

driver.get(site)
try:
    username = input("Entrez votre identifiant my : ")
    password = input("Entrez votre mot de passe my : ")
    ### Connexion à forrest via my
    driver.find_element_by_xpath("//a[@href=\"/login\"]").click()
    driver.find_element_by_xpath("//input[@id=\"username\"]").send_keys(username)
    driver.find_element_by_xpath("//input[@type=\"password\"]").send_keys(password)
    driver.find_element_by_xpath("//button[@id=\"_submit\"]").click()

    ### Fetch des matières
    cours = []
    # liste des cours 1A (à chercher à la mano sur Forrest malheureusement)
    data_cats = [34,35,103,104,105,109,110,106,107,108,72,158,111,112,114,157]
    #data_cats = [34] #temporaire
    for cat in data_cats :
        matieres = driver.find_element_by_xpath("//a[@data-cat=\""+ str(cat) +"\"]")
        titre = matieres.get_attribute('innerHTML')
        titre = " ".join(titre.split())
        cours.append(init_course(titre,cat))

    ### Fetch liste des documents par matière
    for matiere in cours :
        driver.get(site + "/browse/" + str(matiere["data_cat"]))
        time.sleep(0.5)
        docs = driver.find_elements_by_class_name("docu-tt")
        for doc in docs:
            nom = driver.find_element_by_xpath("//a[@href=\""+doc.get_attribute("href")[43:]+"\"]/li").text
            matiere["documents"].append((doc.get_attribute("href")," ".join(nom.split())[:-2]))
    enregistrer(cours)

    driver.close()

    ### Téléchargement des fichiers
    download(cours,username,password)



except(RuntimeError,TypeError,NameError):
    print("erreur : ", RuntimeError,TypeError,NameError)
