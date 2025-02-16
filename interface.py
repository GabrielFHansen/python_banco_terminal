from datetime import datetime
from models import *
from view import *

class UI:
    def start(self):
        while True:
            print('''
                1 - Criar conta
                2 - Desativar Conta
                3 - Transferir Dinheiro
                4 - Movimentar Dinheiro
                5 - Total de Contas
                6 - Filtrar histórico
                7 - Gráfico
                0 - Sair
                ''')
            
            opcao = input("Escolha uma opção: ")
            
            if opcao == '1':
                self._criar_conta()
            elif opcao == '2':
                self._desativar_conta()
            elif opcao == '3':
                self._transferir_saldo()
            elif opcao == '4':
                self._movimentar_dinheiro()
            elif opcao == '5':
                self._total_contas()
            elif opcao == '6':
                self._filtrar_historico()
            elif opcao == '7':
                self._criar_grafico()
            elif opcao == '0':
                break
            else:
                break
            
            
            
    def _criar_conta(self):
        print("Digite o nome de algum dos bancos abaixo: ")
        for banco in Bancos:
            print(f"--- {banco.value} ---")
        
        banco = input().title()
        valor = float(input("Digite o valor disponível na conta: "))
        agencia = input("Digite a agência da conta: ")
        conta = input("Digite o número da conta: ")
        
        conta = Conta(banco=Bancos(banco), valor=valor, agencia=agencia, conta=conta)
        create_account(conta)
        print("Conta criada com sucesso.\n")



    def _desativar_conta(self):
        print("Escolha a conta que deseja desativar.")
        for i in get_allAccounts():
            print(f"ID: {i.id} - Banco: {i.banco.value} - Saldo: R$ {i.valor}")
                
        id_conta = int(input())
        
        try:
            deactivate_account(id_conta)
            print("Conta desativada com sucesso.")
        except ValueError:
            print("Conta com saldo diferente de zero. Retire o saldo para desativar a conta.")
            
            
            
    def _transferir_saldo(self):
        print("Escolha a conta a retirar o dinheiro.")
        for i in get_allAccounts():
            print(f"{i.id} -> {i.banco.value} -> R$ {i.valor}")
        
        conta_retirar_id = int(input())
        
        print("Escolha a conta para enviar dinheiro.")
        for i in get_allAccounts():
            if i.id != conta_retirar_id:
                print(f"{i.id} -> {i.banco.value} -> R$ {i.valor}")
                
        conta_enviar_id = int(input())
        
        valor = float(input("Digite o valor a ser transferido: "))
        transfer_value(conta_retirar_id, conta_enviar_id, valor)
        
        
        
    def _movimentar_dinheiro(self):
        print("Escolha a conta para movimentar dinheiro.")
        for i in get_allAccounts():
            print(f"{i.id} -> {i.banco.value} -> R$ {i.valor}")
            
        conta_id = int(input())
        
        valor = float(input("Digite o valor a ser movimentado: "))
        
        print("Selecione o tipo de movimentação")
        for tipo in Tipos:
            print(f"--- {tipo.value} ---")
            
        tipo = input().title()
        historico = Historico(conta_id=conta_id, valor=valor, tipo=Tipos(tipo), data=date.today())
        movimentar_dinheiro(historico)
        
        
        
    def _total_contas(self):
        print(f"Total nas contas: R$ {total_contas()}")
        
        
        
    def _filtrar_historico(self):
        data_inicio = input("Digite a data de início: ")
        data_fim = input("Digite a data de fim: ")
        
        data_inicio = datetime.strptime(data_inicio, "%d/%m/%Y").date()
        data_fim = datetime.strptime(data_fim, "%d/%m/%Y").date()
        
        for i in buscar_historicos_entre_datas(data_inicio, data_fim):
            print(f"{i.valor} - {i.tipo.value}")
            
            
            
    def _criar_grafico(self):
        criar_grafico_por_conta()
        
UI().start()
        