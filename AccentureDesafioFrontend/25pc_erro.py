import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

# --- Configuração do WebDriver com Opções de Estabilidade ---
chrome_options = Options()
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
wait = WebDriverWait(driver, 20)

try:
    print("1. Acessando https://demoqa.com/")
    driver.get("https://demoqa.com/")

    wait.until(EC.presence_of_element_located((By.TAG_NAME, "footer")))
    driver.execute_script("document.querySelector('footer').remove();")
    driver.execute_script("document.getElementById('fixedban').remove();")

    print("2. Clicando em 'Widgets'...")
    widgets_card = wait.until(EC.presence_of_element_located((By.XPATH, "//h5[text()='Widgets']")))
    driver.execute_script("arguments[0].scrollIntoView(true);", widgets_card)
    driver.execute_script("arguments[0].click();", widgets_card)
    
    # Pausa estratégica para a página se reconstruir
    time.sleep(1)

    print("3. Clicando em 'Progress Bar'...")
    progress_bar_menu_item = wait.until(EC.presence_of_element_located((By.XPATH, "//span[text()='Progress Bar']")))
    print('teste')
    driver.execute_script("arguments[0].click();", progress_bar_menu_item)
    print('teste1')
    # Pausa estratégica para o conteúdo principal carregar
    time.sleep(5)
    print('teste2')
    start_stop_button = (By.ID, "startStopButton")
    progress_bar = (By.CSS_SELECTOR, "div[role='progressbar']")

    # --- APLICANDO O PADRÃO DE OURO: presence_of_element_located + CLIQUE JS ---
    print("4. Clicando em 'Start' pela primeira vez...")
    start_button_element = wait.until(EC.presence_of_element_located(start_stop_button))
    driver.execute_script("arguments[0].click();", start_button_element)

    print("5. Monitorando a barra para parar em torno de 25%...")
    valor_atual = 0
    while valor_atual < 25:
        valor_atual = int(driver.find_element(*progress_bar).get_attribute("aria-valuenow"))
        time.sleep(0.05)
    
    stop_button_element = wait.until(EC.presence_of_element_located(start_stop_button))
    driver.execute_script("arguments[0].click();", stop_button_element)
    
    valor_final_parada = int(driver.find_element(*progress_bar).get_attribute("aria-valuenow"))
    print(f"6. Barra parada em: {valor_final_parada}%")
    assert valor_final_parada <= 25, "ERRO: O valor deveria ser <= 25%"
    print("   - VALIDAÇÃO OK: O valor é menor ou igual a 25%.")

    print("7. Clicando em 'Start' novamente e esperando atingir 100%...")
    start_again_element = wait.until(EC.presence_of_element_located(start_stop_button))
    driver.execute_script("arguments[0].click();", start_again_element)

    wait.until(EC.text_to_be_present_in_element_attribute(progress_bar, "aria-valuenow", "100"))
    print("   - Barra atingiu 100%!")

    print("8. Clicando em 'Reset'...")
    reset_button_element = wait.until(EC.presence_of_element_located(start_stop_button))
    driver.execute_script("arguments[0].click();", reset_button_element)
    
    time.sleep(0.5)
    valor_apos_reset = int(driver.find_element(*progress_bar).get_attribute("aria-valuenow"))
    print(f"   - Valor da barra após reset: {valor_apos_reset}%")
    assert valor_apos_reset == 0, "ERRO: A barra não resetou para 0."
    print("   - VALIDAÇÃO OK: A barra foi resetada corretamente.")

except Exception as e:
    print(f"Ocorreu um erro: {e}")

finally:
    print("\nExercício concluído! Fechando o navegador.")
    time.sleep(4)
    driver.quit()