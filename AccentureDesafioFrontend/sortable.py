import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


try:
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    print("WebDriver iniciado com sucesso.")
except Exception as e:
    print(f"Ocorreu um erro ao iniciar o WebDriver: {e}")
    exit()


driver.maximize_window()

actions = ActionChains(driver)

try:
    print("Passo 1: Acessando o site https://demoqa.com/")
    driver.get("https://demoqa.com/")


    print("Passo 2: Clicando na categoria 'Interactions'...")

    interactions_card = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//h5[text()='Interactions']"))
    )

    driver.execute_script("arguments[0].scrollIntoView(true);", interactions_card)
    interactions_card.click()

    print("Passo 3: Clicando no submenu 'Sortable'...")

    sortable_menu_item = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//span[text()='Sortable']"))
    )
    sortable_menu_item.click()


    print("Passo 4: Reordenando a lista para a ordem crescente...")


    ordem_correta = ["One", "Two", "Three", "Four", "Five", "Six"]


    for i in range(len(ordem_correta)):

        texto_item_a_mover = ordem_correta[i]

        elemento_a_mover = driver.find_element(
            By.XPATH,
            f"//div[@id='demo-tabpane-list']//div[contains(@class, 'list-group-item') and text()='{texto_item_a_mover}']"
        )
        

        elemento_alvo_posicao = driver.find_element(
            By.XPATH,
            f"(//div[@id='demo-tabpane-list']//div[contains(@class, 'list-group-item')])[{i+1}]"
        )
        

        if elemento_a_mover.location != elemento_alvo_posicao.location:
            print(f"Movendo '{elemento_a_mover.text}' para a posição de '{elemento_alvo_posicao.text}'...")
            actions.drag_and_drop(elemento_a_mover, elemento_alvo_posicao).perform()

            time.sleep(0.5)

    print("\nLista ordenada com sucesso!")


    elementos_finais = driver.find_elements(By.XPATH, "//div[@id='demo-tabpane-list']/div/div")
    ordem_final = [elem.text for elem in elementos_finais]

    print(f"Ordem desejada: {ordem_correta}")
    print(f"Ordem obtida:   {ordem_final}")

    if ordem_final == ordem_correta:
        print("Verificação: A ordem está correta!")
    else:
        print("Verificação: A ordem está incorreta.")

    print("\nNavegador será fechado em 10 segundos...")
    time.sleep(10)

finally:

    driver.quit()
    print("Script finalizado e navegador fechado.")