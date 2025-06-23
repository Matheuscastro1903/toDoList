import json
import re
import sys
import os
import time

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')


def login():
    with open("arquivo.json", "r", encoding="utf-8") as arquivo:
        dados = json.load(arquivo)

    dados_conta = dados.get("senha", {})

    print("Bem-vindo(a) à tela de Login To Do List 📝.")
    time.sleep(1)

    tentativas = 3
    while tentativas > 0:
        email_login = input("Digite seu email (ex: nome123@gmail.com): ").strip()
        senha_login = input("Digite sua senha: ").strip()

        if email_login in dados_conta and dados_conta[email_login] == senha_login:
            limpar_tela()
            menu(email_login)
            return
        else:
            print("EMAIL OU SENHA INCORRETOS.")
            tentativas -= 1
            print(f"Tentativas restantes: {tentativas}")

    print("Número máximo de tentativas excedido. Tente novamente mais tarde.")
    sys.exit()


def menu(email_login):
    limpar_tela()
    tentativas = 3
    print("BEM VINDO AO MENU PRINCIPAL DO TO DO LIST 📝.")
    print("-" * 60)

    print("\n╔════════════════════════════════════════════════════════════╗")
    print("║ 🌍 ESCOLHA UMA OPÇÃO NUMÉRICA                                ║")
    print("╠════════════════════════════════════════════════════════════╣")
    print("║ 1. Criar tarefa                                            ║")
    print("║ 2. Atualizar tarefa                                        ║")
    print("║ 3. Deletar tarefa                                         ║")
    print("║ 4. Ver tarefas                                            ║")
    print("║ 5. Sair do sistema                                        ║")
    print("╚════════════════════════════════════════════════════════════╝")

    while tentativas != 0:
        resposta = input("Digite o número da opção desejada: ").strip()

        if resposta == "1":
            criar_tarefa(email_login)
            menu(email_login)
            return
        elif resposta == "2":
            atualizar_tarefa(email_login)
            menu(email_login)
            return
        elif resposta == "3":
            deletar_tarefa(email_login)
            menu(email_login)
            return
        elif resposta == "4":
            ver_tarefas(email_login)
            menu(email_login)
            return
        elif resposta == "5":
            print("Saindo do sistema. Até logo!")
            sys.exit()
        else:
            tentativas -= 1
            print(f"Opção inválida. Tente novamente. Tentativas restantes: {tentativas}")

    print("Número máximo de tentativas excedido. Encerrando o sistema.")
    sys.exit()



def criar_tarefa(email_login):
    limpar_tela()
    print(f"=== Criar tarefa para {email_login} ===")
    print("Digite o nome da tarefa (máximo 80 caracteres). Para parar, pressione ENTER sem digitar nada.")

    with open("arquivo.json", "r", encoding="utf-8") as arquivo:
        dados = json.load(arquivo)

    tarefas_novas = []

    while True:
        nome_tarefa = input("Digite sua tarefa: ").strip()
        if nome_tarefa == "":
            break
        if len(nome_tarefa) > 80:
            print("Erro: A tarefa deve ter no máximo 80 caracteres. Tente novamente.")
            continue

        dados["fazer"][email_login].append(nome_tarefa)
        print(f"Tarefa '{nome_tarefa}' adicionada com sucesso.")

    with open("arquivo.json", "w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, indent=4, ensure_ascii=False)

    
    menu(email_login)
    return



def atualizar_tarefa(email_login):
    limpar_tela()
    print("=== Atualizar Tarefa ===")

    with open("arquivo.json", "r", encoding="utf-8") as arquivo:
        dados = json.load(arquivo)

    print("Você deseja mover a tarefa de:")
    print("1. Fazer → Fazendo")
    print("2. Fazendo → Feito")

    escolha = input("Digite 1 ou 2: ").strip()

    if escolha == "1":
        origem = "fazer"
        destino = "fazendo"
    elif escolha == "2":
        origem = "fazendo"
        destino = "feito"
    else:
        print("Opção inválida. Retornando ao menu.")
        input("Pressione ENTER para continuar.")
        return

    tarefas_origem = dados[origem][email_login]

    if not tarefas_origem:
        print(f"Você não tem tarefas na lista '{origem.upper()}'.")
        input("Pressione ENTER para voltar ao menu.")
        return

    print(f"\nTarefas em '{origem.upper()}':")
    for idx, tarefa in enumerate(tarefas_origem, start=1):
        print(f"{idx}. {tarefa}")

    tentativas = 3
    while tentativas > 0:
        try:
            indice = int(input(f"\nDigite o número da tarefa que deseja mover para '{destino.upper()}': "))
            if 1 <= indice <= len(tarefas_origem):
                tarefa_movida = tarefas_origem.pop(indice - 1)
                dados[destino][email_login].append(tarefa_movida)
                with open("arquivo.json", "w", encoding="utf-8") as arquivo:
                    json.dump(dados, arquivo, indent=4, ensure_ascii=False)
                print(f"Tarefa '{tarefa_movida}' movida com sucesso!")
                break
            else:
                print("Índice fora do intervalo.")
                tentativas -= 1
                print(f"Tentativas restantes: {tentativas}")

        except ValueError:
            print("Entrada inválida. Digite um número.")
            tentativas -= 1
            print(f"Tentativas restantes: {tentativas}")

    else:
        print("Número máximo de tentativas excedido.")

    input("Pressione ENTER para voltar ao menu.")


def deletar_tarefa(email_login):
    limpar_tela()
    print("=== Deletar Tarefa ===")

    with open("arquivo.json", "r", encoding="utf-8") as arquivo:
        dados = json.load(arquivo)

    tentativas_tipo = 3
    tipo = None

    while tentativas_tipo > 0:
        print("De qual tipo de lista deseja deletar a tarefa?")
        print("1. Fazer")
        print("2. Fazendo")
        print("3. Feito")
        escolha = input("Digite 1, 2 ou 3: ").strip()

        if escolha == "1":
            tipo = "fazer"
            break
        elif escolha == "2":
            tipo = "fazendo"
            break
        elif escolha == "3":
            tipo = "feito"
            break
        else:
            tentativas_tipo -= 1
            print(f"Opção inválida. Tentativas restantes: {tentativas_tipo}")

    else:
        print("Número máximo de tentativas excedido. Retornando ao menu.")
        input("Pressione ENTER para continuar.")
        return

    tarefas = dados[tipo][email_login]

    #verifica se a lista está vazia ou não
    if not tarefas:
        print(f"Você não tem tarefas na lista '{tipo.upper()}'.")
        input("Pressione ENTER para voltar ao menu.")
        return

    print(f"\nTarefas em '{tipo.upper()}':")
    for idx, tarefa in enumerate(tarefas, start=1):
        print(f"{idx}. {tarefa}")

    tentativas_indice = 3
    while tentativas_indice > 0:
        try:
            indice = int(input("\nDigite o número da tarefa que deseja deletar: "))
            if 1 <= indice <= len(tarefas):
                tarefa_removida = tarefas.pop(indice - 1)
                with open("arquivo.json", "w", encoding="utf-8") as arquivo:
                    json.dump(dados, arquivo, indent=4, ensure_ascii=False)
                print(f"Tarefa '{tarefa_removida}' removida com sucesso!")
                break
            else:
                print("Número fora do intervalo.")
        except ValueError:
            print("Entrada inválida. Digite apenas números.")

        tentativas_indice -= 1
        print(f"Tentativas restantes: {tentativas_indice}")

    else:
        print("Número máximo de tentativas excedido.")

    input("Pressione ENTER para voltar ao menu.")

    
    
    
def ver_tarefas(email_login):
    limpar_tela()

    with open("arquivo.json", "r", encoding="utf-8") as arquivo:
        dados = json.load(arquivo)

    tarefas_fazer = dados["fazer"][email_login]
    tarefas_fazendo = dados["fazendo"][email_login]
    tarefas_feito = dados["feito"][email_login]

    print(f"📋 Tarefas do usuário: {email_login}\n")
    
    print("📌 A FAZER:")
    if tarefas_fazer:
        for i, tarefa in enumerate(tarefas_fazer, 1):
            print(f"  {i}. {tarefa}")
    else:
        print("  Nenhuma tarefa pendente.")

    print("\n🔄 EM ANDAMENTO:")
    if tarefas_fazendo:
        for i, tarefa in enumerate(tarefas_fazendo, 1):
            print(f"  {i}. {tarefa}")
    else:
        print("  Nenhuma tarefa em andamento.")

    print("\n✅ CONCLUÍDAS:")
    if tarefas_feito:
        for i, tarefa in enumerate(tarefas_feito, 1):
            print(f"  {i}. {tarefa}")
    else:
        print("  Nenhuma tarefa concluída.")

    print("\n" + "-" * 50)
    input("Pressione ENTER para voltar ao menu.")



class Cadastro:
    def __init__(self):
        self.email = input("Digite seu email: ").strip()
        self.senha = input("Digite sua senha (mínimo 4, máximo 20 caracteres): ").strip()
        self.validar_senha()

    def validar_senha(self):
        tentativas = 3
        while tentativas > 0:
            if 4 <= len(self.senha) <= 20:
                self.validar_email()
                return
            else:
                print("Senha inválida. Deve ter entre 4 e 20 caracteres.")
                self.senha = input("Digite sua senha novamente: ").strip()
                tentativas -= 1
                print(f"Tentativas restantes: {tentativas}")
        print("Limite de tentativas excedido. Encerrando.")
        sys.exit()

    def validar_email(self):
        dominios_validos = ['gmail.com', 'outlook.com', 'hotmail.com', 'yahoo.com', 'icloud.com']
        tentativas = 3

        while tentativas > 0:
            if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', self.email):
                print("Formato de e-mail inválido.")
            else:
                dominio = self.email.split("@")[1]
                if dominio not in dominios_validos:
                    print("Domínio de e-mail não aceito.")
                else:
                    self.salvar_dados()
                    return

            self.email = input("Digite seu e-mail novamente: ").strip()
            tentativas -= 1
            print(f"Tentativas restantes: {tentativas}")

        print("Limite de tentativas excedido. Encerrando.")
        sys.exit()

    

    def salvar_dados(self):
        try:
            with open("arquivo.json", "r", encoding="utf-8") as arquivo:
                dados = json.load(arquivo)
        except FileNotFoundError:
            dados = {"senha": {}, "fazer": {}, "fazendo": {}, "feito": {}}

        # Aqui adiciona os dados sem verificar duplicidade
        dados["senha"][self.email] = self.senha
        dados["fazer"][self.email] = []
        dados["fazendo"][self.email] = []
        dados["feito"][self.email] = []

        with open("arquivo.json", "w", encoding="utf-8") as arquivo:
            json.dump(dados, arquivo, indent=4, ensure_ascii=False)

        print("Cadastro realizado com sucesso!")
        tentativas=3
        while tentativas>0:
            opcao = input("Digite 'login' para entrar ou 'sair' para encerrar: ").strip().lower()
            if opcao in ["login","logar"]:
                login()
            elif opcao in ["sair","sai","saida"]:
                print("Encerrando o sistema.")
                sys.exit()
            else:
                print("Resposta inválida")
                tentativas-=1
                print(f"Tentativas restantes {tentativas}")

        else:
            print("Número de tentativas extrapoladas")
            print("Encerrando o sistema.")
            sys.exit()






tentativas = 3  #  3 tentativas permitidas
while tentativas != 0:
    tipo_servico = input(
        "QUAL TIPO DE SERVIÇO VOCÊ DESEJA ??(LOGIN/CADASTRO) ").strip().lower()

    if tipo_servico in ["login", "entrar", "acessar", "fazer login"]:
        login()
        break  # Sai do loop e puxa a função login

    elif tipo_servico in ["cadastro", "cadastrar", "criar conta", "novo cadastro"]:
        novo_cadastro = Cadastro()
        break  # Sai do loop e puxa a função cadastro

    else:
    #OPÇÃO INVÁLIDA
        print("Serviço inválido. Por favor, tente novamente.")
        tentativas -= 1
        print(f"Tentativas restantes {tentativas}")

else:
    #LIMITE DE OPÇÕES ATINGIDO
    print("Limite de tentativas atingido. Reinicie o programa.")
    