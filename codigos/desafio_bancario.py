import textwrap


def menu():
    menu = """\n
    ====================   MENU  ===================
    [d] \tDeposit
    [s] \tDraw
    [e] \tExtract
    [na] \tNew Account
    [la] \tList accounts
    [nu] \tNew User
    [q] \tExit
    ===>>
    """
    return input(textwrap.dedent(menu))

def deposit(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor
        extrato += f"Deposit: R$ {valor:.2f}\n"
        print(f"Deposit: R$ {valor:.2f}\n with sucess!")
    else:
        print("\nInvalid value!")
    return saldo, extrato

def draw(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saques

    if excedeu_saldo:
        print("\nInsufficient funds!")

    elif excedeu_limite:
        print("\nLimit exceeded!")

    elif excedeu_saques:
        print("\nNumber of withdrawals exceeded!")

    elif valor > 0:
        saldo -= valor
        extrato += f"Withdraw: R$ {valor:.2f}\n"
        numero_saques += 1
        print(f"Withdraw: R$ {valor:.2f}\n with sucess!")

    else:
        print("\nInvalid value!")

    return saldo, extrato

def extract(saldo,/, *, extrato):  
    print("\n ======================   EXTRATO   ======================")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo: R$ {saldo:.2f}")
    print("===========================================================")

def new_user(usuarios):
    cpf = input("Enter your CPF: ")
    usuario = list_users(cpf, usuarios)

    if usuario:
        print("User already exists!")
        return  

    nome = input("Enter your name: ")
    data_nascimento = input("Enter your date of birth: ")
    endereco = input("Enter your address: ")

    usuarios.append({ "cpf": cpf, "nome": nome, "data_nascimento":data_nascimento, "endereco": endereco}) 

    print("User created with success!")

def list_users(cpf, usuarios):
    usuarios_filtrados = [user for user in usuarios if user["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None

def new_account(agencia, numero_conta,usuarios):  
    cpf= input("Enter your CPF: ")
    usuario = list_users(cpf, usuarios)

    if usuario:
        print("\nAccount created with success!")
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}

    print("\nUser not found!")

def list_accounts(contas):
    for conta in contas:
        linha = f"""\
        Agencia: {conta["agencia"]}
        Conta: {conta["numero_conta"]}
        Nome: {conta["usuario"]["nome"]}
        """
        print("=" *100)
        print(textwrap.dedent(linha))

def main():
    LIMITRE_SAQUES = 5
    AGENCIA = "0001"

    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    usuarios = []
    contas = []


    while True:

        opcao = menu()

        if opcao == "d":
            valor = float(input("Enter the deposit amount: "))

            saldo, extrato = deposit(saldo, valor, extrato)

        elif opcao == "s":
            valor = float(input("Enter the withdrawal amount:"))

            saldo, extrato = draw(
            saldo =saldo,
            valor=valor,
            extrato=extrato,
            limite=limite,
            numero_saques=numero_saques,
            limite_saques=LIMITRE_SAQUES
            )


        elif opcao == "e":
            extract(saldo, extrato=extrato)

        elif opcao == "nu":
            new_user(usuarios)
        
        elif opcao == "na":
            numero_conta = len(contas) + 1
            conta = new_account(AGENCIA, numero_conta, usuarios)

            if conta:
                contas.append(conta)

        elif opcao == "la":
            list_accounts(contas)

        elif opcao == "q":
            break

        else:
            print("Invalid operation, please select the desired operation again.")

main()
