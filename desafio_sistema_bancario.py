from datetime import datetime

# Decorador para log
def log_operation(func):
    def wrapper(*args, **kwargs):
        data = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        operation = func.__name__.capitalize()
        result = func(*args, **kwargs)
        # Log da operação, sem imprimir no console
        with open("operations.log", "a") as log_file:
            log_file.write(f"{data} - {operation}: {args}\n")
        return result
    return wrapper

class Transacao:
    def __init__(self, tipo, valor):
        self.tipo = tipo
        self.valor = valor
        self.data = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

class Conta:
    def __init__(self, numero, usuario):
        self.numero = numero
        self.saldo = 0
        self.transacoes = []
        self.usuario = usuario

    def adicionar_transacao(self, tipo, valor):
        transacao = Transacao(tipo, valor)
        self.transacoes.append(transacao)

    def depositar(self, valor):
        if valor > 0:
            self.saldo += valor
            self.adicionar_transacao('Depósito', valor)
            return "Depósito efetuado com sucesso!"
        return "Operação falhou! O valor informado é inválido."

    def sacar(self, valor):
        if valor > self.saldo:
            return "Operação falhou! Você não tem saldo suficiente."
        self.saldo -= valor
        self.adicionar_transacao('Saque', valor)
        return "Saque realizado com sucesso!"

class Usuario:
    def __init__(self, nome, data_nascimento, cpf, endereco):
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf
        self.endereco = endereco

class Banco:
    def __init__(self):
        self.contas = []
        self.usuarios = []
        self.numero_conta = 1  # Inicia com o número da conta 1

    def add_usuario(self, nome, data_nascimento, cpf, endereco):
        if any(u.cpf == cpf for u in self.usuarios):
            return "Operação falhou! CPF já cadastrado."
        
        usuario = Usuario(nome, data_nascimento, cpf, endereco)
        self.usuarios.append(usuario)
        return "Usuário cadastrado com sucesso!"

    def add_conta(self, usuario):
        conta = Conta(self.numero_conta, usuario)
        self.numero_conta += 1
        self.contas.append(conta)
        return conta

    def __iter__(self):
        return iter(self.contas)

# Gerador de relatórios
class ReportGenerator:
    def __init__(self, extrato):
        self.extrato = extrato
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index < len(self.extrato):
            line = self.extrato[self.index]
            self.index += 1
            return line
        else:
            raise StopIteration

@log_operation
def depositar(valor, conta):
    return conta.depositar(valor)

@log_operation
def sacar(valor, conta):
    return conta.sacar(valor)

# Configurações iniciais
LIMITE_TRANSACOES_DIA = 10

# Instanciação do banco
banco = Banco()

# Menu para criar usuários e contas
menu = """
[1] Criar Usuário
[2] Criar Conta Corrente
[3] Depositar
[4] Sacar
[5] Extrato
[6] Relatório de Contas
[7] Sair
"""

while True:
    opcao = input(menu).strip()

    if opcao == "1":
        nome = input("Nome do usuário: ")
        data_nascimento = input("Data de nascimento (dd/mm/yyyy): ")
        cpf = input("CPF (somente números): ")
        endereco = input("Endereço (logradouro, número - bairro - cidade/sigla estado): ")
        resultado = banco.add_usuario(nome, data_nascimento, cpf, endereco)
        print(resultado)

    elif opcao == "2":
        cpf = input("Informe o CPF do usuário para criar a conta: ")
        usuario = next((u for u in banco.usuarios if u.cpf == cpf), None)
        if usuario:
            conta = banco.add_conta(usuario)
            print(f"Conta criada com sucesso! Número da conta: {conta.numero}")
        else:
            print("Usuário não encontrado.")

    elif opcao == "3":
        numero_conta = int(input("Informe o número da conta: "))
        valor = float(input("Informe o valor de depósito: R$ "))
        conta = next((c for c in banco.contas if c.numero == numero_conta), None)
        if conta:
            mensagem = depositar(valor, conta)
            print(mensagem)
        else:
            print("Conta não encontrada.")

    elif opcao == "4":
        numero_conta = int(input("Informe o número da conta: "))
        valor = float(input("Informe o valor para saque: R$ "))
        conta = next((c for c in banco.contas if c.numero == numero_conta), None)
        if conta:
            mensagem = sacar(valor, conta)
            print(mensagem)
        else:
            print("Conta não encontrada.")

    elif opcao == "5":
        numero_conta = int(input("Informe o número da conta: "))
        conta = next((c for c in banco.contas if c.numero == numero_conta), None)
        if conta:
            print("\n========== EXTRATO DA CONTA ==========\n")
            for transacao in conta.transacoes:
                print(f"{transacao.tipo}: R$ {transacao.valor:.2f} | Data e Hora: {transacao.data}")
            print(f"\nSaldo Atual: R$ {conta.saldo:.2f}")
            print("=========================================")
        else:
            print("Conta não encontrada.")

    elif opcao == "6":
        print("\n========== RELATÓRIO DE CONTAS ==========\n")
        for conta in banco:
            print(f"Conta nº {conta.numero} - Saldo: R$ {conta.saldo:.2f} - Cliente: {conta.usuario.nome}")
        print("=========================================")

    elif opcao == "7":
        print("Obrigado por utilizar os nossos serviços!")
        break

    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")
