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
    print("1. Acessando https://demoqa.com/progress-bar diretamente...")
    driver.get("https://demoqa.com/progress-bar")

    start_stop_button = (By.ID, "startStopButton")
    reset_button = (By.ID, "resetButton")
    progress_bar = (By.CSS_SELECTOR, "div[role='progressbar']")
    
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "footer")))
    driver.execute_script("document.querySelector('footer').remove();")
    
    print("4. Clicando em 'Start' pela primeira vez...")
    start_button_element = wait.until(EC.presence_of_element_located(start_stop_button))
    driver.execute_script("arguments[0].click();", start_button_element)

    print("5. Monitorando a barra para parar em torno de 25%...")
    while True:
        valor_atual = int(driver.find_element(*progress_bar).get_attribute("aria-valuenow"))
        if valor_atual >= 25:
            stop_button_element = wait.until(EC.presence_of_element_located(start_stop_button))
            driver.execute_script("arguments[0].click();", stop_button_element)
            break
            
    valor_final_parada = int(driver.find_element(*progress_bar).get_attribute("aria-valuenow"))
    print(f"6. Barra parada em: {valor_final_parada}%")
    assert valor_final_parada <= 25, "ERRO: O valor deveria ser <= 25%"
    print("   - VALIDAÇÃO OK: O valor é menor ou igual a 25%.")

    print("7. Clicando em 'Start' novamente e esperando atingir 100%...")
    start_again_element = wait.until(EC.presence_of_element_located(start_stop_button))
    driver.execute_script("arguments[0].click();", start_again_element)

    wait.until(EC.text_to_be_present_in_element_attribute(progress_bar, "aria-valuenow", "100"))
    print("   - Barra atingiu 100%!")
    
    time.sleep(2)

    print("8. Clicando em 'Reset'...")
    time.sleep(3)
    reset_button_element = wait.until(EC.presence_of_element_located(reset_button))
    driver.execute_script("arguments[0].click();", reset_button_element)
    
    time.sleep(3)
    valor_apos_reset = int(driver.find_element(*progress_bar).get_attribute("aria-valuenow"))
    print(f"   - Valor da barra após reset: {valor_apos_reset}%")
    assert valor_apos_reset == 0, "ERRO: A barra não resetou para 0."
    print("   - VALIDAÇÃO OK: A barra foi resetada corretamente.")

except Exception as e:
    print(f"Ocorreu um erro: {e}")

finally:
    print("\nExercício concluído com sucesso! Fechando o navegador.")
    time.sleep(4)
    driver.quit()