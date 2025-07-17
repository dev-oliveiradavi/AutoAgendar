import datetime
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import config
from webdriver_utils import get_element, get_click

def config_site():
    if config.navegador_driver is None:
        try:
            config.navegador_driver = webdriver.Chrome()
            config.navegador_wait = WebDriverWait(config.navegador_driver, config.TEMPO_LONGO)
            print("Navegador aberto.")
        except Exception as e:
            print(f"ERRO! Não foi possível abrir o navegador. {e}")
            return False

    try:
        config.navegador_driver.get(config.URL)
        time.sleep(config.TEMPO_MEDIO)
    except Exception as e:
        print(f"ERRO! Não foi possível abrir a URL. {e}")
        if config.navegador_driver:
            config.navegador_driver.quit()
            config.navegador_driver = None
            config.navegador_wait = None
        return False
            
    try:
        # page 1
        dropdown_categoria = Select(get_element(By.ID, "categoria", "Dropdown Categoria"))
        dropdown_categoria.select_by_visible_text(config.CATEGORIA)
        time.sleep(config.TEMPO_MEDIO)
        
        dropdown_servico = Select(get_element(By.ID, "servico", "Dropdown Serviço"))
        dropdown_servico.select_by_visible_text(config.SERVICO)
        time.sleep(config.TEMPO_MEDIO)

        get_click(By.XPATH, '//*[@id="escolha-servico"]/div/div[2]/div/button', "Botão 'Próximo' do serviço").click()
        time.sleep(config.TEMPO_MEDIO)

        # page 2
        dropdown_unidade = Select(get_element(By.ID, "unidade", "Dropdown Unidade"))
        dropdown_unidade.select_by_index(1)
        time.sleep(config.TEMPO_MEDIO)

        get_click(By.XPATH, '//*[@id="escolha-unidade"]/div/div[2]/div/button[2]', "Botão 'Próximo' da unidade").click()
        time.sleep(config.TEMPO_MEDIO)

        return True
    except Exception as e:
        print(f"ERRO! Não foi possível configurar o serviço/unidade. Detalhe: {e}")
        if config.navegador_driver:
            config.navegador_driver.quit()
            config.navegador_driver = None
            config.navegador_wait = None
        return False

def marcar_data(data):
    # page 3
    try:
        dropdown_data = Select(get_element(By.ID, "data", "Dropdown Data de Agendamento"))
        dropdown_data.select_by_visible_text(data)
        time.sleep(config.TEMPO_MEDIO)

        try:
            dropdown_horario = Select(get_element(By.ID, "horario", "Dropdown Horário")) 
            dropdown_horario.select_by_visible_text(config.hora_desejada)
            time.sleep(config.TEMPO_MEDIO)
        except (TimeoutException, NoSuchElementException, StaleElementReferenceException):
            print(f"OBS: Horário ({config.hora_desejada}) não está disponível para {data}")
            config.datas_processadas.add(data)
            return False
        
        get_element(By.ID, "nome", "Nome").send_keys(config.nome)
        time.sleep(0.5)
        
        dropdown_doc = Select(get_element(By.ID, "documento", "Dropdown Tipo de Documento"))
        dropdown_doc.select_by_visible_text(config.DOCUMENTO)
        
        get_element(By.ID, "numero", "CCPF").send_keys(config.cpf)
        time.sleep(0.5)
        
        get_element(By.ID, "telefone", "Telefone").send_keys(config.telefone)
        time.sleep(0.5)

        get_element(By.ID, "email", "Email").send_keys(config.email)
        time.sleep(0.5)

        get_click(By.XPATH, "//button[contains(., 'Agendar') and @type='submit']", "Botão Agendar").click()
        time.sleep(config.TEMPO_LONGO)

        try:
            btn_confirmar = get_click(By.XPATH, "//button[contains(., 'Confirmar agendamento') and @class='confirm']", "Botão Confirmar Agendamento")
            btn_confirmar.click()
            time.sleep(config.TEMPO_MEDIO)
        except (TimeoutException, NoSuchElementException):
            print("ERRO! Modal de confirmação não apareceu ou botão (Confirmar) não encontrado.")
            return False
        
        time.sleep(config.TEMPO_MEDIO)
        config.tot_agendados += 1
        config.datas_processadas.add(data)
        config.agendamento_concluidos.append(f"{data} | {config.hora_desejada}")
        print(f"Agendamento REALIZADO para ({data} às {config.hora_desejada}).")
        print(f"TOTAL: {config.tot_agendados}/{config.TOT_AGENDAMENTO}")
        return True
    except Exception as e:
        print(f"Agendamento falhou para {data} no horário {config.hora_desejada}!")
        print(e)
        config.datas_processadas.add(data)
        return False

def agendar():
    config.tot_agendados = 0
    config.datas_processadas.clear()
    config.agendamento_concluidos.clear()
    rodadas_sem_sucesso = 0

    print("INFO: Iniciando o processo automático de agendamento...")

    try:

        if not config_site():
            print("ERRO! Não foi possível iniciar o agendamento!")
            return False
        
        while config.tot_agendados < config.TOT_AGENDAMENTO:
            print(f"Tentativa de agendamento: {config.tot_agendados + 1}/{config.TOT_AGENDAMENTO}")
            print(f"[ {config.dia_desejado} (dia da semana) no horário {config.hora_desejada} ]")

            try:
                dropdown_datas = Select(get_element(By.ID, "data", "Dropdown Datas"))
                opcoes_datas = dropdown_datas.options
            except Exception as e:
                print(f"ERRO! Não foi possível obter as datas!")
                print(e)
                break

            datas_disponiveis = []
            for opcao in opcoes_datas:
                valor_data = opcao.get_attribute("value")
                if valor_data:
                    try:
                        obj_data = datetime.datetime.strptime(valor_data, '%Y-%m-%d').date()
                        texto_data = opcao.text.strip()
                        if (obj_data.weekday() == config.dia_desejado and
                             texto_data not in config.datas_processadas):
                            datas_disponiveis.append((obj_data, texto_data, valor_data))
                    except ValueError:
                        pass
            
            if not datas_disponiveis:
                print(f"OBS: Não há mais datas para {config.dia_desejado} no horário {config.hora_desejada}!")
                rodadas_sem_sucesso += 1
                if rodadas_sem_sucesso >= config.TOT_BUSCA_SEM_SUCESSO:
                    print(f"ERRO! Limite de {config.TOT_BUSCA_SEM_SUCESSO} busca sem sucesso atingido!")
                    break
                time.sleep(config.TEMPO_LONGO)
                continue
            
            datas_disponiveis.sort(key=lambda x: x[0])
            agendar = False
            for obj_data, texto_data, valor_data in datas_disponiveis:
                if config.tot_agendados >= config.TOT_AGENDAMENTO:
                    agendar = True
                    break

                sucesso = marcar_data(texto_data)
                if sucesso:
                    agendar = True
                    rodadas_sem_sucesso = 0
                    if config.tot_agendados < config.TOT_AGENDAMENTO:
                        print("Agendamento OK. Fazendo o próximo...")
                        if not config_site():
                            print("ERRO! Falha ao reiniciar o próximo agendamento!")
                            return False
                    break
                else:
                    print(f"ERRO! Tentativa para {texto_data} falhou!")
            
            if not agendar and config.tot_agendados < config.TOT_AGENDAMENTO:
                print("OBS: Nenhuma data foi agendada nesta rodada!")
                rodadas_sem_sucesso += 1
                if rodadas_sem_sucesso >= config.TOT_BUSCA_SEM_SUCESSO:
                    print(f"ERRO! Limite de {config.TOT_BUSCA_SEM_SUCESSO} busca sem sucesso atingido. Parando a busca!")
                    break
                time.sleep(config.TEMPO_LONGO)

        if config.tot_agendados == config.TOT_AGENDAMENTO:
            print(f"Todos os {config.TOT_AGENDAMENTO} agendamentos foram concluídos.")
        elif config.tot_agendados > 0:
            print(f"{config.tot_agendados} de {config.TOT_AGENDAMENTO} agendamentos foram feitos")
        else:
            print(f"ERRO! Nenhum agendamento foi feito. Verifique se há um erro nos seus dados!")
        return True
    except Exception as e:
        print(f"ERRO! Ocorreu um erro na automação!")
        print(e)
        return False
    finally:
        # relatorio
        print(f"\n|FIM DO PROCESSO|")
        print(f"Total agendado: {config.tot_agendados}")
        if config.agendamento_concluidos:
            print("\n| Relatório de Agendamentos Concluídos |")
            for agendamento in config.agendamento_concluidos:
                print(f" - {agendamento}")
            print("---")
        else:
            print("| Nenhum Agendamento foi registrado |")
        if config.navegador_driver:
            config.navegador_driver.quit()
