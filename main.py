import sys
import config

from user_input import coletar_dados_agendamento, coletar_dados_pessoais
from agendador import agendar

def menu_principal():
    while True:
        print("\n -------------")
        print("| AUTO AGENDA |")
        print(" -------------")

        status_pessoal = "CONFIGURADO" if (config.nome and config.cpf and
                                          config.telefone and config.email) else "PENDENTE"
        status_agendamento = "CONFIGURADO" if (config.dia_desejado != -1 and config.hora_desejada) else "PENDENTE"
        
        print(f"\n[ Status Dados Pessoais: {status_pessoal}  ]")
        print(f"[ Status Agendamento: {status_agendamento} ]")

        print("\n1 - Iniciar Agendamento Agora")
        print("2 - Configurar Seus Dados Pessoais")
        print("3 - Configurar Detalhes do Agendamento")
        print("4 - Sair do Programa")
        escolha = input("\nOpção -> ").strip()

        if escolha == '1':
            if not (config.nome and config.cpf and
                    config.telefone and config.email and
                    config.dia_desejado != -1 and config.hora_desejada):
                print("OBS: Configure Todos os dados antes de iniciar!")
                continue
            
            confirmar = input("Confirmar início do agendamento com os dados registrado? (S/N): ").upper().strip()
            if confirmar == 'S':
                agendar() 
            else:
                print("Início do agendamento cancelado!")
        elif escolha == '2':
            coletar_dados_pessoais()
        elif escolha == '3':
            coletar_dados_agendamento()
        elif escolha == '4':
            print("Saindo...")
            if config.navegador_driver:
                config.navegador_driver.quit()
            sys.exit(0)
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    menu_principal()
