#Aluna: Júlia Coelho Rodrigues
#RA: 22408388

from utils import Normalizer as n


#funcoes para testar as classes, seus construtores e metodos

def teste_construtor(funcao_construtora, descricao):
    """funcao para testar os construtores das classes entidades"""
    try:
        objeto = funcao_construtora()
        print(f"[OK] {descricao} criado com sucesso")
        return objeto
    except Exception as e:
        print(f"[ERRO] {descricao} -> {e}")
        return None

def teste_metodo(chamada_metodo, descricao):
    """funcao para testar os metodos das classes entidades"""
    try:
        resultado = chamada_metodo()
        print(f"[OK] {descricao} retornou: {resultado}")
    except Exception as e:
        print(f"[ERRO] {descricao} -> {e}")


def teste_metodo_by_id_dao(chamada_metodo, descricao):
    try:
        success, resultado = chamada_metodo()
        if success:
            print(f"[OK] {descricao} retornou: {resultado}")
        if not success:
            print(f"[ERRO] {descricao} -> {resultado}")
    except Exception as e:
        print(f"[ERRO Exception] {descricao} -> {e}")

def ask_if_clean_bank(classe):
    while True:
        answer = input(f"Gostaria de limpar o banco de dados? Recomenda-se limpar o banco para testar a classe {classe} devidamente.\n")
        answer = n.normalize(answer)
        if answer=="SIM":
            clean_bank()
            return
        elif answer=="NAO":
            return
        print("\nPor favor, insira uma resposta válida.\n")
        
def clean_bank():
    import os
    if os.path.exists("ecommerce.db"):
        os.remove("ecommerce.db")

def ask_if_continue(classe) -> bool:
    while True:
        answer = input(f"Gostaria de seguir para o teste da {classe}?\n")
        answer = n.normalize(answer)
        if answer=="SIM":
            return True
        elif answer=="NAO":
            return False
        print("\nPor favor, insira uma resposta válida.\n")