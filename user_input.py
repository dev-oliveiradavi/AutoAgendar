import config

def coletar_dados_pessoais():
    print("[Dados Pessoais]")
    config.nome = input("Digite seu nome completo: ").strip()
    while not config.nome:
        print("Nome não pode ser vazio!")
        config.nome = input("Digite seu nome completo: ").strip()
    
    config.cpf = input("Digite seu CPF (somente números): ").strip()
    while not (config.cpf.isdigit() and len(config.cpf) == 11):
        print("CPF inválido. Digite 11 números!")
        config.cpf = input("Digite seu CPF (somente números): ").strip()

    config.telefone = input("Digite seu telefone (ex: DDD123456789): ").strip()
    while not(config.telefone.isdigit() and 10 <= len(config.telefone) <= 11):
        print("Telefone inválido. Digite 10 ou 11 número (com DDD)!")
        config.telefone = input("Digite seu telefone (ex: DDD123456789): ").strip()

    config.email = input("Digite seu email: ").strip()
    while "@" not in config.email or "." not in config.email or len(config.email) < 5:
        print("Email inválido!")
        config.email = input("Digite seu email: ").strip()

    print("\n[Dados Pessoas Registrados]")
    print(f"Nome: {config.nome} | CPF: {config.cpf}")
    print(f"Telefone: {config.telefone} | email: {config.telefone}")

def coletar_dados_agendamento():
    print("[Detalhes do Agendamento]")
    print(f"Categoria: {config.CATEGORIA} | Serviço: {config.SERVICO}")

    while True:
        try:
            print("[0] Seg, [1] Terçca, [2] Quarta ... [6] Domingo")
            config.dia_desejado = input("Digite o dia da semana: ")
            dia = int(config.dia_desejado)
            if 0 <= dia <= 6:
                config.dia_desejado = dia
                break
            else:
                print("Número do dia inválido!")
        except:
            print("Entrada inválida. Digite um número inteiro!")

    config.hora_desejada = input("Digite o horário (ex: 14:00): ").strip()
    while not (len(config.hora_desejada) == 5 and config.hora_desejada[2] == ":"
           and config.hora_desejada[:2].isdigit() and config.hora_desejada[3:].isdigit()
           and 0 <= int(config.hora_desejada[:2]) <= 23 and 0 <= int(config.hora_desejada[3:]) <= 59):
        print("Horário inválido!")
        config.hora_desejada = input("Digite o horário (ex: 14:00): ").strip()

    
    print("\n[Dados do Agendamento Registrados]")
    print(f"Dia da Semana: {config.dia_desejado} | Horário Preferencial: {config.hora_desejada}")
    print(f"Agendamentos: {config.TOT_AGENDAMENTO}")
