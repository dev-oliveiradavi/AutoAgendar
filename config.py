URL = "https://agendamento.vitoria.es.gov.br/"

TEMPO_LONGO = 10
TEMPO_MEDIO = 5

# 4 dias agendados
TOT_AGENDAMENTO = 4
TOT_BUSCA_SEM_SUCESSO = 3

CATEGORIA = "Esportes e Lazer"
SERVICO = "Campo de Futebol do Parque Pedra da Cebola"

nome = ""
DOCUMENTO = "CPF"
cpf = ""
telefone = ""
email = ""
dia_desejado = -1
hora_desejada = ""

navegador_driver = None
navegador_wait = None

tot_agendados = 0
datas_processadas = set()
agendamento_concluidos = []
