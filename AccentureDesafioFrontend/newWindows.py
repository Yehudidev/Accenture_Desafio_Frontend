import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# --- Configuração do WebDriver ---
try:
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    print("WebDriver iniciado com sucesso.")
except Exception as e:
    print(f"Ocorreu um erro ao iniciar o WebDriver: {e}")
    exit()

driver.maximize_window()

try:
    # ---------------------------------------------------------------------
    # Passo 1: Acessar o site https://demoqa.com/
    # ---------------------------------------------------------------------
    print("Passo 1: Acessando o site https://demoqa.com/")
    driver.get("https://demoqa.com/")

    # ---------------------------------------------------------------------
    # Passo 2: Escolher a opção Alerts, Frame & Windows
    # ---------------------------------------------------------------------
    print("Passo 2: Clicando na categoria 'Alerts, Frame & Windows'...")
    # Espera até que o elemento seja clicável
    alerts_card = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//h5[text()='Alerts, Frame & Windows']"))
    )
    # Rola a página até o elemento para garantir visibilidade
    driver.execute_script("arguments[0].scrollIntoView(true);", alerts_card)
    alerts_card.click()

    # ---------------------------------------------------------------------
    # Passo 3: Clicar no submenu Browser Windows
    # ---------------------------------------------------------------------
    print("Passo 3: Clicando no submenu 'Browser Windows'...")
    browser_windows_menu = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//span[text()='Browser Windows']"))
    )
    browser_windows_menu.click()

    # ---------------------------------------------------------------------
    # Passo 4: Clicar no botão New Window
    # ---------------------------------------------------------------------
    # É CRUCIAL guardar o identificador da janela original ANTES de abrir uma nova.
    janela_original = driver.current_window_handle
    print(f"Janela original identificada: {janela_original}")

    print("Passo 4: Clicando no botão 'New Window'...")
    new_window_button = driver.find_element(By.ID, "windowButton")
    new_window_button.click()

    # ---------------------------------------------------------------------
    # Passo 5: Validar que a nova janela foi aberta com a mensagem correta
    # ---------------------------------------------------------------------
    print("Passo 5: Verificando a nova janela e validando a mensagem...")
    
    # Espera até que o número de janelas abertas seja 2.
    WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2))
    
    # Pega os identificadores de TODAS as janelas abertas
    todas_as_janelas = driver.window_handles
    
    # Itera sobre os identificadores para encontrar a nova janela e mudar o foco para ela
    for janela in todas_as_janelas:
        if janela != janela_original:
            driver.switch_to.window(janela)
            print(f"Foco alterado para a nova janela: {janela}")
            break
            
    # Agora que o foco está na nova janela, podemos interagir com ela
    # Valida a mensagem na nova página
    mensagem_nova_janela = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "sampleHeading"))
    )
    
    texto_esperado = "This is a sample page"
    texto_obtido = mensagem_nova_janela.text
    
    print(f"Texto esperado: '{texto_esperado}'")
    print(f"Texto obtido:    '{texto_obtido}'")

    if texto_obtido == texto_esperado:
        print("Validação concluída com sucesso!")
    else:
        print("Falha na validação do texto!")

    # ---------------------------------------------------------------------
    # Passo 6: Fechar a nova janela aberta
    # ---------------------------------------------------------------------
    print("Passo 6: Fechando a nova janela...")
    # O comando driver.close() fecha a janela que está em foco no momento.
    driver.close()

    # ---------------------------------------------------------------------
    # Passo extra: Retornar o foco para a janela original
    # ---------------------------------------------------------------------
    print("Retornando o foco para a janela original...")
    driver.switch_to.window(janela_original)
    
    # Verificação final para garantir que voltamos
    print(f"Título da página atual: '{driver.title}'. Estamos de volta à página principal.")
    
    # Mantém o navegador aberto por 5 segundos para visualização
    print("\nNavegador será fechado em 5 segundos...")
    time.sleep(5)

finally:
    driver.quit()
    print("Script finalizado e navegador fechado.")