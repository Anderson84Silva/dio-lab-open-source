menu = """

[d] Deposit
[s] Draw
[e] Extract
[q] Exit

=> """

saldo = 0
limite = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 5

while True:

    opcao = input(menu)

    if opcao == "d":
        valor = float(input("Enter the deposit amount: "))

        if valor > 0:
            saldo += valor
            extrato += f"Deposit: R$ {valor:.2f}\n"

        else:
            print("Operation failed! The value entered is invalid.")

    elif opcao == "s":
        valor = float(input("Enter the withdrawal amount:"))

        excedeu_saldo = valor > saldo

        excedeu_limite = valor > limite

        excedeu_saques = numero_saques >= LIMITE_SAQUES

        if excedeu_saldo:
            print("Operation failed! You don't have enough balance.")

        elif excedeu_limite:
            print("Operation failed! The withdrawal amount exceeds the limit.")

        elif excedeu_saques:
            print("Operation failed! Maximum number of withdrawals exceeded.")

        elif valor > 0:
            saldo -= valor
            extrato += f"Draw: R$ {valor:.2f}\n"
            numero_saques += 1

        else:
            print("Operation failed! The value entered is invalid.")

    elif opcao == "e":
        print("\n================ EXTRACT ================")
        print("No movements were carried out." if not extrato else extrato)
        print(f"\nBalance: R$ {saldo:.2f}")
        print("==========================================")

    elif opcao == "q":
        break

    else:
        print("Invalid operation, please select the desired operation again.")