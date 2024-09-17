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

# Gerador de relatórios
class ReportGenerator:
    def __init__(self, extrato):
        self.extrato = extrato.split('\n')
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

    def filter_by_type(self, trans_type):
        for line in self.extrato:
            if line.startswith(trans_type):
                yield line

# Iterador personalizado para contas
class Conta:
    def __init__(self, numero, saldo):
        self.numero = numero
        self.saldo = saldo
        self.transacoes = []  # Armazenar transações

    def adicionar_transacao(self, tipo, valor):
        self.transacoes.append({
            'tipo': tipo,
            'valor': valor,
            'data': datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        })

    def get_transacoes(self):
        return self.transacoes

class Banco:
    def __init__(self):
        self.contas = []

    def add_conta(self, conta):
        self.contas.append(conta)

    def __iter__(self):
        return ContaIterador(self.contas)

class ContaIterador:
    def __init__(self, contas):
        self.contas = contas
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index < len(self.contas):
            conta = self.contas[self.index]
            self.index += 1
            return f"Conta nº {conta.numero} - Saldo: R$ {conta.saldo:.2f}"
        else:
            raise StopIteration

@log_operation
def depositar(valor, saldo, extrato, transacoes, limite_transacoes):
    data_atual = datetime.now().strftime("%d/%m/%Y")
    transacoes_dia = [t for t in transacoes if t['data'].startswith(data_atual)]
    
    if len(transacoes_dia) >= limite_transacoes:
        return saldo, extrato, "Operação falhou! Você excedeu o número de transações permitidas para hoje."

    if valor > 0:
        saldo += valor
        data = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        extrato += f"Depósito: R$ {valor:.2f} | Data e Hora: {data}\n"
        transacoes.append({'tipo': 'Depósito', 'valor': valor, 'data': data})
        return saldo, extrato, "Depósito efetuado com sucesso!"
    else:
        return saldo, extrato, "Operação falhou! O valor informado é inválido."

@log_operation
def sacar(valor, saldo, extrato, transacoes, numero_saques, LIMITE_SAQUES, limite_transacoes):
    data_atual = datetime.now().strftime("%d/%m/%Y")
    transacoes_dia = [t for t in transacoes if t['data'].startswith(data_atual)]
    
    if len(transacoes_dia) >= limite_transacoes:
        return saldo, extrato, "Operação falhou! Você excedeu o número de transações permitidas para hoje."

    excedeu_saldo = valor > saldo
    excedeu_saques = numero_saques >= LIMITE_SAQUES

    if excedeu_saldo:
        return saldo, extrato, "Operação falhou! Você não tem saldo suficiente."
    elif excedeu_saques:
        return saldo, extrato, "Operação falhou! Número máximo de saques excedido."
    elif valor > 0:
        saldo -= valor
        data = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        extrato += f"Saque: R$ {valor:.2f} | Data e Hora: {data}\n"
        transacoes.append({'tipo': 'Saque', 'valor': valor, 'data': data})
        numero_saques += 1
        return saldo, extrato, "Saque realizado com sucesso!"
    else:
        return saldo, extrato, "Operação falhou! O valor informado é inválido."

# Configurações iniciais
saldo = 0
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3
LIMITE_TRANSACOES_DIA = 10

# Instanciação do banco e contas
banco = Banco()
conta1 = Conta(1, 1000)
conta2 = Conta(2, 1500)
banco.add_conta(conta1)
banco.add_conta(conta2)

menu = """
[1] Depositar
[2] Sacar
[3] Extrato
[4] Relatório de Contas
[5] Sair
"""

while True:
    opcao = input(menu).strip()

    if opcao == "1":
        valor = float(input("Informe o valor de depósito: R$ "))
        saldo, extrato, mensagem = depositar(valor, saldo, extrato, conta1.get_transacoes(), LIMITE_TRANSACOES_DIA)
        print(mensagem)

    elif opcao == "2":
        valor = float(input("Informe o valor para saque: R$ "))
        saldo, extrato, mensagem = sacar(valor, saldo, extrato, conta1.get_transacoes(), numero_saques, LIMITE_SAQUES, LIMITE_TRANSACOES_DIA)
        print(mensagem)

    elif opcao == "3":
        print("\n========== EXTRATO DA CONTA ==========\n")
        print("Movimentações realizadas em sua conta:\n")
        for line in ReportGenerator(extrato):
            print(line)
        print(f"\nSaldo Atual: R$ {saldo:.2f}")
        print("=========================================")

    elif opcao == "4":
        print("\n========== RELATÓRIO DE CONTAS ==========\n")
        for info in banco:
            print(info)
        print("=========================================")

    elif opcao == "5":
        print("Obrigado por utilizar os nossos serviços!")
        break

    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")
