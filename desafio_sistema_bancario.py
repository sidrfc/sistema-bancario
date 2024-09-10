from datetime import datetime

menu = """
[1] Depositar
[2] Sacar
[3] Extrato
[4] Sair
"""

saldo = 0
limite = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3

while True:
    opcao = input(menu).strip()

    if opcao == "1":
        valor = float(input("Informe o valor de depósito: R$ "))

        if valor > 0:
            saldo += valor
            data = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            extrato += f"Depósito: R$ {valor:.2f} | Data e Hora: {data}\n"
            print(f"Depósito efetuado com sucesso! O valor depositado em sua conta foi: R$ {valor:.2f}")
        else:
            print("Operação falhou! O valor informado é inválido.")
        
    elif opcao == "2":
        valor = float(input("Informe o valor para saque: R$ "))

        excedeu_saldo = valor > saldo
        excedeu_saques = numero_saques >= LIMITE_SAQUES

        if excedeu_saldo:
            print("Operação falhou! Você não tem saldo suficiente.")
        elif excedeu_saques:
            print("Operação falhou! Número máximo de saques excedido.")
        elif valor > 0:
            saldo -= valor
            data = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            extrato += f"Saque: R$ {valor:.2f} | Data e Hora: {data} \n"
            numero_saques += 1
            print(f"Saque realizado com sucesso! O valor de saque foi de: R$ {valor:.2f}")
        else:
            print("Operação falhou! O valor informado é inválido.")
    
    elif opcao == "3":
        print("\n========== EXTRATO DA CONTA ==========\n")
        print("Movimentações realizadas em sua conta:\n")
        if not extrato:
            print("Não foram realizadas movimentações.")
        else:
            print(extrato)
        print(f"\nSaldo Atual: R$ {saldo:.2f}")
        print("=========================================")

    elif opcao == "4":
        print("Obrigado por utilizar os nossos serviços!")
        break

    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")
