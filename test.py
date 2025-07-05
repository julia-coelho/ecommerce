#Aluna: Júlia Coelho Rodrigues
#RA: 22408388

from tests import func_test_all_by_type

if __name__ == "__main__":
    

    while True:
        #apresenta o menu de opcoes
        print("\n----- TESTES DAS CLASSES -----\n")
        print("    MENU DE OPÇÕES\n")
        print("(1) - Testar Classes do Tipo Entidade\n")
        print("(2) - Testar Classes do Tipo DAO\n")
        #print("(3) - Testar Classes do Tipo Service\n")
        print("(4) - Testar Todas as Classes\n")
        print("(5) - Finalizar Programa\n")

        #usuario decide opcao 
        answer = input("Opção desejada: ")

        try:
            option = int(answer)
        except ValueError:
            print("\nErro: Digite apenas números válidos")
            continue

        try:
            #match-case para definir o que fazer
            match option:
                case 1:
                    func_test_all_by_type('entity')
                case 2:
                    func_test_all_by_type('dao')
                # case 3:
                #     func_test_all_by_type('service')
                case 4:
                    func_test_all_by_type('all')
                case 5:
                    break
                case _:
                    print("Opção inválida\n")

        except Exception as e:
            print(f"\n[Erro interno a test.py]: {e}\n")