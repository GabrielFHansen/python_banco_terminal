from datetime import date
from models import Conta, Historico, Tipos, engine, Status
from sqlmodel import Session, select
import matplotlib.pyplot as plt

# Valida se já existe uma conta com o mesmo banco, agência e conta
def create_account(conta: Conta):
    with Session(engine) as session:
        statement = select(Conta).where(Conta.banco == conta.banco, Conta.agencia == conta.agencia, Conta.conta == conta.conta)
        results = session.exec(statement).all()
        if results:
            print("Essa conta já existe")
            return
        session.add(conta)
        session.commit()
        return conta
    

def get_allAccounts():
    with Session(engine) as session:
        statement = select(Conta)
        results = session.exec(statement).all()
    return results
    
def deactivate_account(id):
    with Session(engine) as session:
        statement = select(Conta).where(Conta.id==id)
        conta = session.exec(statement).first()
        if conta.valor != 0:
            raise ValueError("Conta com saldo diferente de zero")
        conta.status = Status.INATIVO
        session.commit()
        
def transfer_value(id_origem, id_destino, valor):
    with Session(engine) as session:
        statement = select(Conta).where(Conta.id==id_origem)
        conta_origem = session.exec(statement).first()
        if conta_origem.valor < valor:
            raise ValueError("Saldo insuficiente")
        
        statement = select(Conta).where(Conta.id==id_destino)
        conta_destino = session.exec(statement).first()
        
        conta_origem.valor -= valor
        conta_destino.valor += valor
        session.commit()
        
def movimentar_dinheiro(historico: Historico):
    with Session(engine) as session:
        statement = select(Conta).where(Conta.id==historico.conta_id)
        conta = session.exec(statement).first()
        
        if historico.tipo == Tipos.ENTRADA:
            conta.valor += historico.valor
        else:
            if conta.valor < historico.valor:
                raise ValueError("Saldo insuficiente")
            conta.valor -= historico.valor

        session.add(historico)
        session.commit()
        return historico
    
def total_contas():
    with Session(engine) as session:
        statement = select(Conta)
        results = session.exec(statement).all()
        
    total = 0
    for conta in results:
        total += conta.valor
        
    return float(total)

def buscar_historicos_entre_datas(data_inicio: date, data_fim: date):
    with Session(engine) as session:
        statement = select(Historico).where(
            Historico.data >= data_inicio, 
            Historico.data <= data_fim
        )
        results = session.exec(statement).all()
        return results

def criar_grafico_por_conta():
    with Session(engine) as session:
        statement = select(Conta).where(Conta.status==Status.ATIVO)
        contas = session.exec(statement).all()
        bancos = [i.banco.value for i in contas]
        total = [i.valor for i in contas]
        
        plt.bar(bancos, total)
        plt.show()

#create_account(Conta(banco="NUBANK", agencia="0001", conta="123456", valor=1000))
#create_account(Conta(banco="INTER", agencia="0002", conta="123457", valor=1000))
#print(get_allAccounts())
#deactivate_account(1)
#transfer_value(1, 2, 500)
#print(total_contas())
#criar_grafico_por_conta()