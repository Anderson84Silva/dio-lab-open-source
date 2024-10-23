from abc import ABC, abstractclassmethod,abstractproperty
from datetime import datetime
import textwrap


class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf
        

class Conta:
    def __init__(self,numero,cliente):
        self._saldo =0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente 
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico
    
    def sacar(self, valor):
        saldo = self.saldo
        excedeu_saldo = valor > saldo

        if excedeu_saldo:
            print("\nOperação falhou! O valor de saque excede o valor de saldo.")
        elif valor > 0:
            self._saldo -= valor
            print("\nSaque realizado com sucesso.")
            return True
        else:
            print("\nOperação falhou! O valor informado é inválido.")
        return False

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print
        else:
            print("\nOperação falhou! O valor informado é inválido.")
            return False
        return True

class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self._limite = limite
        self.limite_saques = limite_saques
    
    def sacar(self, valor):
        numero_saques =len(
            [transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__]
        )

        execedeu_limite = valor > self.limite
        execedeu_saques = numero_saques >= self.limite_saques9
        if execedeu_limite:
            print("\nOperação falhou! O valor de saque excede o valor de limite.")
        elif execedeu_saques:
            print("\nOperação falhou! Número máximo de saques excedido.")
        else:
            return super().sacar(valor)
        return False    
    
    def __str__(self):
        return f"""
        Agência: {self.agencia}
        C/C: {self.numero}
        Titular: {self.cliente.nome}
        """
    

class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
                "valor": transacao.valor,
                "tipo": transacao.__class__.__name__,
            }
        )

class Transacao:
    @property
    @abstractproperty
    def valor(self):
        pass
    
    @abstractclassmethod
    def registrar(self, conta):
        pass

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self._valor)
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self._valor)
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

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

def deposit(clientes):
    cpf = input("Enter your CPF: ")
    cliente = list_users(cpf, clientes)
    if not cliente:
        print("User not found")
        return
    valor = float(input("Enter the deposit amount: "))
    transacao = Deposito(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    cliente.realizar_transacao(conta, transacao)

def draw(clientes):
    cpf = input("Enter your CPF: ")
    cliente = list_users(cpf, clientes)
    if not cliente:
        print("User not found")
        return
    valor = float(input("Enter the withdrawal amount: "))
    transacao = Saque(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    cliente.realizar_transacao(conta, transacao)

def extract(clientes):
    cpf = input("Enter your CPF: ")
    cliente = list_users(cpf, clientes)
    if not cliente:
        print("User not found")
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    print("\n ======================   EXTRATO   ======================")
    transacaoes = conta.historico.transacoes

    extrato = ""
    if not transacaoes:
        extrato = "Não foram realizadas movimentações."
    else:
        for transacao in transacaoes:
            extrato += f"\n{transacao[tipo]}:\n\tR$ {transacao['valor']:.2f}"

    print(extrato)
    print(f"\nSaldo: R$ {conta.saldo:.2f}")
    print("===========================================================")
    
def new_user(clientes):
    cpf = input("Enter your CPF: ")
    cliente = list_users(cpf, clientes)

    if cliente:
        print("User already exists!")
        return  

    nome = input("Enter your name: ")
    data_nascimento = input("Enter your date of birth: ")
    endereco = input("Enter your address: ")

    cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)

    clientes.append(cliente) 

    print("User created with success!")


def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("You don't have an account yet!")
        return
    
    # FIXME:
    return cliente.contas[0]



def list_users(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf== cpf]
    return clientes_filtrados[0] if clientes_filtrados else None

def new_account(numero_conta, clientes, contas):  
    cpf= input("Enter your CPF: ")
    cliente = list_users(cpf, clientes)

    if not cliente:
        print("\nUser not found!")
        return

    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
    contas.append(conta)
    cliente.contas.append(conta)

    print("\nAccount created with success!")

    

def list_accounts(contas):
    for conta in contas:
        print("=" *100)
        print(textwrap.dedent(str(conta)))

def main():
    clientes = []
    contas = []


    while True:

        opcao = menu()

        if opcao == "d":
            deposit(clientes)

        elif opcao == "s":
            draw(clientes)


        elif opcao == "e":
            extract(clientes)

        elif opcao == "nu":
            new_user(clientes)
        
        elif opcao == "na":
            numero_conta = len(contas) + 1
            new_account(numero_conta, clientes, contas)


        elif opcao == "la":
            list_accounts(contas)

        elif opcao == "q":
            break

        else:
            print("Invalid operation, please select the desired operation again.")

main()
