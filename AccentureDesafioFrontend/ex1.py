import os
import random
import time
from faker import Faker

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

fake = Faker('pt_BR')

# --- Geração de Dados ---
first_name = fake.first_name()
last_name = fake.last_name()
email = fake.email()
mobile_number = fake.msisdn()[:10] 
date_of_birth = fake.date_of_birth(minimum_age=18, maximum_age=60).strftime("%d %b %Y") 
address = fake.address().replace("\n", ", ")

genders = ['Male', 'Female', 'Other']
hobbies = ['Sports', 'Reading', 'Music']
subject_list = ["Maths", "Physics", "English", "Chemistry", "Computer Science"]

try:
    current_dir = os.path.dirname(__file__)
    file_path = os.path.join(current_dir, 'uploads', 'arquivo_teste.txt')
    absolute_file_path = os.path.abspath(file_path)
except NameError:
    absolute_file_path = os.path.abspath(os.path.join('uploads', 'arquivo_teste.txt'))

print("Iniciando automatização no Chrome...")
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
driver.maximize_window()
wait = WebDriverWait(driver, 15) 

try:
    print('Acessando o site demoqa.com')
    driver.get('https://demoqa.com')

    print('Navegando para a seção Forms')
    forms_card = wait.until(EC.element_to_be_clickable((By.XPATH, "//h5[text()='Forms']")))
    driver.execute_script("arguments[0].scrollIntoView(true);", forms_card)
    forms_card.click()

    print('Clicando em Practice Form')
    practice_form_menu = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Practice Form']")))
    practice_form_menu.click()

    print('Preenchendo o formulário de cadastro com os dados aleatórios gerados...')
    
    driver.find_element(By.ID, 'firstName').send_keys(first_name) 
    driver.find_element(By.ID, 'lastName').send_keys(last_name)   
    driver.find_element(By.ID, 'userEmail').send_keys(email)      
    gender_choice = random.choice(genders)
    driver.find_element(By.XPATH, f"//label[text()='{gender_choice}']").click()

    driver.find_element(By.ID, 'userNumber').send_keys(mobile_number)

    date_input = driver.find_element(By.ID, "dateOfBirthInput")
    date_input.send_keys(Keys.CONTROL + "a")
    date_input.send_keys(Keys.BACKSPACE)
    date_input.send_keys(date_of_birth)
    date_input.send_keys(Keys.ESCAPE)

    subjects_input = driver.find_element(By.CSS_SELECTOR, "#subjectsContainer input")
    subject_choice = random.choice(subject_list) 
    subjects_input.send_keys(subject_choice)
    subjects_input.send_keys(Keys.ENTER)

    hobby_choice = random.choice(hobbies)
    driver.find_element(By.XPATH, f"//label[text()='{hobby_choice}']").click()

    print(f'Fazendo upload de um arquivo: {absolute_file_path}') 
    driver.find_element(By.ID, 'uploadPicture').send_keys(absolute_file_path)

    driver.find_element(By.ID, 'currentAddress').send_keys(address)

    state_container = driver.find_element(By.ID, "state")
    driver.execute_script("arguments[0].scrollIntoView(true);", state_container)
    state_container.click()
    state_input = driver.find_element(By.CSS_SELECTOR, "#state input")
    state_input.send_keys("NCR")
    state_input.send_keys(Keys.ENTER)

    print('Aguardando o campo -City- estar clicável...')
    city_container = wait.until(EC.element_to_be_clickable((By.ID, "city")))
    city_container.click()
    city_input = driver.find_element(By.CSS_SELECTOR, "#city input")
    city_input.send_keys("Delhi")
    city_input.send_keys(Keys.ENTER)

    print('Enviando o formulário...')
    submit_button = driver.find_element(By.ID, 'submit')
    driver.execute_script("arguments[0].click();", submit_button) 

    print('Aguardando o popup de confirmação...')
    modal_title = wait.until(EC.visibility_of_element_located((By.ID, 'example-modal-sizes-title-lg')))

    assert "Thanks for submitting the form" in modal_title.text
    print('Formulário enviado com sucesso!')

    print('Fechando o popup...')
    close_button = driver.find_element(By.ID, 'closeLargeModal')
    close_button.click()

    time.sleep(2)

except Exception as e:
    print(f'Ocorreu um erro durante a automação: {e}')

finally:
    print('Finalizando o navegador...')
    driver.quit()