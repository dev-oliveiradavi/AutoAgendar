from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import config

def get_element(by, value, element_name="elemento"):
    try:
        element = config.navegador_wait.until(EC.visibility_of_element_located((by, value)))
        return element
    except TimeoutException:
        print(f"ERRO! Tempo esgotado para {element_name}")
        raise
    except NoSuchElementException:
        print(f"ERRO! {element_name} não econtrado")
        raise

def get_click(by, value, element_name="elemento"):
    try:
        element = config.navegador_wait.until(EC.element_to_be_clickable((by, value)))
        return element
    except TimeoutException:
        print(f"ERRO! Tempo esgotado para {element_name}")
        raise
    except NoSuchElementException:
        print(f"ERRO! {element_name} não encontrado")
        raise
