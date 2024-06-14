from termcolor import colored

class Cliente:
    def __init__(self, nome, cpf):
        self.nome = nome
        self.cpf = cpf
        if len(str(self.cpf)) > 11:
            raise ValueError('Número de cpf inválido, máximo de 11 dígitos')

    def __repr__(self):
        return f'Cliente(nome={self.nome}, cpf={self.cpf})'

class Conta:
    def __init__(self, cliente, saldo_inicial=0):
        self.cliente = cliente
        self.saldo = saldo_inicial
        self.historico_transacoes = []

    def depositar(self, valor):
        self.saldo += valor
        self.historico_transacoes.append(('Depósito', valor))

    def sacar(self, valor):
        if valor <= self.saldo:
            self.saldo -= valor
            self.historico_transacoes.append(('Saque', valor))
        else:
            print(colored(f"Saldo insuficiente. Seu saldo é de {self.saldo} e você tentou sacar {valor}", 'red'))
            print(colored(f"Seu saldo atual é de: {self.saldo}", 'yellow'))

    def ver_saldo(self):
        print(colored(f"Saldo atual: {self.saldo}", 'blue'))

    def transferir(self, valor, conta_destino):
        if valor <= self.saldo:
            self.saldo -= valor
            conta_destino.depositar(valor)
            self.historico_transacoes.append(('Transferência', valor, conta_destino.cliente.nome))
        else:
            print(colored(f"Transferência não realizada. Saldo insuficiente: {self.saldo}", 'red'))

    def extrato(self):
        print(colored('----------------------------------------', 'blue'))
        print(colored(f"Extrato de transações para {self.cliente.nome}:", 'blue'))
        saldo_atual = self.saldo  # Saldo antes de qualquer transação
        contador = 1  # Inicializa um contador para as transações
        for transacao in self.historico_transacoes:
            tipo, valor = transacao[0], transacao[1]
            print(colored(f"Transação {contador}: Saldo anterior: {saldo_atual:.2f}", 'blue'))
            if tipo == 'Depósito':
                saldo_atual += valor
            elif tipo == 'Saque' or tipo == 'Transferência':
                saldo_atual -= valor
            if tipo == 'Transferência':
                destino = transacao[2]
                print(colored(f"{tipo} de {valor} para {destino}", 'green'))
            else:
                print(colored(f"{tipo} de {valor}", 'green'))
            contador += 1  # Incrementa o contador após cada transação
        print(colored(f"Saldo final: {saldo_atual:.2f}", 'magenta'))
        print(colored('----------------------------------------', 'blue'))

    def resumo_conta(self):
        return f"Nome: {self.cliente.nome}, CPF: {self.cliente.cpf}, Saldo: {self.saldo:.2f}"

class Transacao:
    def __init__(self, conta, valor, tipo, conta_destino=None):
        self.conta = conta
        self.valor = valor
        self.tipo = tipo
        self.conta_destino = conta_destino

    def executar(self):
        if self.tipo == 'deposito':
            self.conta.depositar(self.valor)
        elif self.tipo == 'saque':
            self.conta.sacar(self.valor)
        elif self.tipo == 'transferencia':
            if self.conta_destino:
                self.conta.transferir(self.valor, self.conta_destino)
            else:
                print(colored("Conta destino não especificada para transferência.", 'red'))

# Adicionando os novos clientes
cliente1 = Cliente('Gabriel', '11122233344')
cliente2 = Cliente('Rachel', '22255545487')
cliente3 = Cliente('Manuela', '98765432100')
cliente4 = Cliente('David', '12312312399')

# Criando contas para os novos clientes com saldos iniciais
conta1 = Conta(cliente1, 100000)  # Saldo inicial de Gabriel
conta2 = Conta(cliente2, 50000)   # Saldo inicial de Rachel
conta3 = Conta(cliente3, 15000)   # Saldo inicial de Manuela
conta4 = Conta(cliente4, 20000)   # Saldo inicial de David

# Transações de exemplo para os novos clientes
transacao1 = Transacao(conta1, 15000, 'deposito')
transacao1.executar()
transacao5 = Transacao(conta2, 50000, 'saque')
transacao5.executar()
transacao6 = Transacao(conta1, 20000, 'transferencia', conta2)
transacao6.executar()

# Exibindo o extrato das contas dos novos clientes
conta1.extrato()  # Mostra o extrato da conta1 (Gabriel)
conta2.extrato()  # Mostra o extrato da conta2 (Rachel)

# Exemplo de uso com os clientes existentes e a funcionalidade de extrato
transacao2 = Transacao(conta3, 10000, 'deposito')
transacao2.executar()
transacao3 = Transacao(conta4, 20000, 'saque')
transacao3.executar()
transacao4 = Transacao(conta3, 30000, 'transferencia', conta4)
transacao4.executar()

conta3.extrato()  # Mostra o extrato da conta3 (Manuela)
conta4.extrato()  # Mostra o extrato da conta4 (David)
