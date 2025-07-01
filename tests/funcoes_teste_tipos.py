#Aluna: Júlia Coelho Rodrigues
#RA: 22408388

from utils import Normalizer as n

from tests.test_entities.address_test import test_address
from tests.test_entities.category_test import test_category
from tests.test_entities.customer_test import test_customer
from tests.test_entities.date_test import test_date
from tests.test_entities.order_item_batch_test import test_order_item_batch
from tests.test_entities.order_item_test import test_order_item
from tests.test_entities.order_test import test_order
from tests.test_entities.payment_test import test_payment
from tests.test_entities.product_batch_test import test_product_batch
from tests.test_entities.product_test import test_product

from tests.test_dao.category_dao_test import test_category_dao
from tests.test_dao.product_dao_test import test_product_dao
from tests.test_dao.product_batch_dao_test import test_product_batch_dao

def func_test_all_by_type(type: str):

    #match-case para definir o que fazer
    match type:
        case 'entity':
            while True:
                #apresenta o menu de opcoes
                print("\n----- TESTES DAS CLASSES ENTIDADES -----\n")
                print("    MENU DE OPÇÕES\n")
                print("(1) - Testar Classe Address\n")
                print("(2) - Testar Classe Category\n")
                print("(3) - Testar Classe Customer\n")
                print("(4) - Testar Classe Date\n")
                print("(5) - Testar Classe OrderItemBatch\n")
                print("(6) - Testar Classe OrderItem\n")
                print("(7) - Testar Classe Order\n")
                print("(8) - Testar Classe Payment\n")
                print("(9) - Testar Classe ProductBatch\n")
                print("(10) - Testar Classe Product\n")
                print("(11) - Testar Todas as Classes do tipo Entidade\n")
                print("(12) - Retornar ao Menu Principal\n")            
                print("(13) - Finalizar Programa\n")            
                
                #usuario decide opcao 
                try:
                    option = int(input("Opção desejada: "))

                    #match-case para definir o que fazer
                    match option:
                        case 1:
                            func_test_entities('address')
                        case 2:
                            func_test_entities('category')
                        case 3:
                            func_test_entities('customer')
                        case 4:
                            func_test_entities('date')
                        case 5:
                            func_test_entities('order_item_batch')
                        case 6:
                            func_test_entities('order_item')
                        case 7:
                            func_test_entities('order')
                        case 8:
                            func_test_entities('payment')
                        case 9:
                            func_test_entities('product_batch')
                        case 10:
                            func_test_entities('product')
                        case 11:
                            print("\n========================")
                            print("Testes das Classes Entidade")
                            print("========================\n")
                            func_test_entities('all')
                        case 12:
                            return
                        case 13:
                            break
                        case _:
                            print("Opção inválida\n") 

                except ValueError:
                    print("\nErro: Digite apenas números válidos\n")

        case 'dao':  
            while True:
                #apresenta o menu de opcoes
                print("\n----- TESTES DAS CLASSES DAO -----\n")
                print("    MENU DE OPÇÕES\n")
                print("(1) - Testar Classe CategoryDAO\n")
                # print("(2) - Testar Classe \n")
                # print("(3) - Testar Classe \n")
                # print("(4) - Testar Classe \n")
                # print("(5) - Testar Classe \n")
                # print("(6) - Testar Classe \n")
                print("(7) - Testar Classe ProductBatchDAO\n")
                print("(8) - Testar Classe ProductDAO\n")
                print("(9) - Testar Todas as Classes do tipo DAO\n")
                print("(10) - Retornar ao Menu Principal\n")
                print("(11) - Finalizar o Programa\n")            
                
                #usuario decide opcao 
                try:
                    option = int(input("Opção desejada: "))

                    #match-case para definir o que fazer
                    match option:
                        case 1:
                            func_test_dao('category_dao')
                        # case 2:
                        #     func_test_dao('customer_dao')
                        # case 3:
                        #     func_test_dao('order_item_batch_dao')
                        # case 4:
                        #     func_test_dao('order_item_dao')
                        # case 5:
                        #     func_test_dao('order_dao')
                        # case 6:
                        #     func_test_dao('payment_dao')
                        case 7:
                            func_test_dao('product_batch_dao')
                        case 8:
                            func_test_dao('product_dao')
                        case 9:
                            import unicodedata
                            while True:
                                answer = input(f"Gostaria de limpar o banco de dados a cada classe DAO testada? Recomenda-se limpar o banco a cada classe DAO testada.\n")
                                answer = n.normalize(answer)
                                if answer=="SIM":
                                    print("\n========================")
                                    print("  Testes das Classes DAO  ")
                                    print("========================\n")
                                    func_test_dao('all clean')
                                elif answer=="NAO":
                                    print("\n========================")
                                    print("  Testes das Classes DAO  ")
                                    print("========================\n")
                                    func_test_dao('all not clean')
                                print("Por favor, insira uma resposta válida.\n")
                        case 10:
                            return
                        case 11:
                            break
                        case _:
                            print("Opção inválida\n")

                except ValueError:
                    print("\nErro: Digite apenas números válidos\n")

        # case 'service':  
        #     while True:
        #         #apresenta o menu de opcoes
        #         print("\n----- TESTES DAS CLASSES SERVICE -----\n")
        #         print("    MENU DE OPÇÕES\n")
        #         print("(1) - Testar Classe \n")
        #         print("(2) - Testar Classe \n")
        #         print("(3) - Testar Classe \n")
        #         print("(4) - Testar Classe \n")
        #         print("(5) - Testar Classe \n")
        #         print("(6) - Testar Classe \n")
        #         print("(7) - Testar Classe \n")
        #         print("(8) - Testar Classe \n")
        #         print("(9) - Testar Todas as Classes do tipo Service\n")
        #         print("(10) - Retornar ao Programa Principal\n")
        #         print("(10) - Finalizar Programa\n")            
                
        #         #usuario decide opcao 
        #         try:
        #             option = int(input("Opção desejada: "))
        #         except ValueError:
        #             print("\nErro: Digite apenas números válidos\n")
        #             continue

        #         #match-case para definir o que fazer
        #         match option:
        #             case 1:
        #             case 2:
        #             case 3:
        #             case 4:
        #             case 5:
        #             case 6:
        #             case 7:
        #             case 8:
        #             case 9:
        #                 print("\n========================")
        #                 print("Testes das Classes Service")
        #                 print("========================\n")
        #             case 10:
        #                 return
        #             case 11:
        #                 break
        #             case _:
        #                 print("Opção inválida\n")

        case 'all':  
            while True:

                answer = input(f"Gostaria de limpar o banco de dados a cada classe DAO testada? Recomenda-se limpar o banco a cada classe DAO testada.\n")
                answer = n.normalize(answer)
                if answer=="SIM":
                    print("\n========================")
                    print("Testes das Classes Entidade")
                    print("========================\n")
                    func_test_entities('all')

                    print("\n========================")
                    print("  Testes das Classes DAO  ")
                    print("========================\n")
                    func_test_dao('all clean')

                    print("\n========================")
                    print("Testes das Classes Service")
                    print("========================\n")

                    return
                
                elif answer=="NAO":
                    print("\n========================")
                    print("Testes das Classes Entidade")
                    print("========================\n")
                    func_test_entities('all')

                    print("\n========================")
                    print("  Testes das Classes DAO  ")
                    print("========================\n")
                    func_test_entities('all not clean')

                    print("\n========================")
                    print("Testes das Classes Service")
                    print("========================\n")

                    return
                
                print("Por favor, insira uma resposta válida.\n")


def func_test_entities(entity: str):
    """funcao para chamar os testes das classes-entidades"""

    match entity:
        case 'address':
            test_address()
            return
        case 'category':
            test_category()
            return
        case 'customer':
            test_customer()
            return
        case 'date':
            test_date()
            return
        case 'order_item_batch':
            test_order_item_batch()
            return
        case 'order_item':
            test_order_item()
            return
        case 'order':
            test_order()
            return
        case 'payment':
            test_payment()
            return
        case 'product_batch':
            test_product_batch()
            return
        case 'product':
            test_product()
            return
        case 'all':
            test_address()
            test_category()
            test_customer()
            test_date()
            test_order_item_batch()
            test_order_item()
            test_order()
            test_payment()
            test_product_batch()
            test_product()
            return
        case _:
            print("\nOpção inválida passada para func_test_entities() \n")
            return


def func_test_dao(dao: str):
    """funcao para chamar os testes das classes dao"""

    from banco import get_conexao, criar_tabelas, close_connection
    from tests import ask_if_clean_bank, clean_bank

    match dao:
        case 'category_dao':
            ask_if_clean_bank("CategoryDAO")
            conexao = get_conexao()
            criar_tabelas(conexao)
            test_category_dao(conexao)
            close_connection()
            return
        case 'customer_dao':
            return
        case 'order_dao':
            return
        case 'order_item_batch_dao':
            return
        case 'order_item_dao':
            return
        case 'payment_dao':
            return
        case 'product_batch_dao':
            ask_if_clean_bank("ProductBatchDAO)")
            conexao = get_conexao()
            criar_tabelas(conexao)
            test_product_batch_dao(conexao)
            close_connection()
            return
        case 'product_dao':
            ask_if_clean_bank("ProductDAO")
            conexao = get_conexao()
            criar_tabelas(conexao)
            test_product_dao(conexao)
            close_connection()
            return
        case 'all clean':
            clean_bank()
            conexao = get_conexao()
            criar_tabelas(conexao)
            test_category_dao(conexao)
            test_product_batch_dao(conexao)
            test_product_dao(conexao)
            return
        case 'all not clean':
            conexao = get_conexao()
            criar_tabelas(conexao)
            test_category_dao(conexao)
            test_product_batch_dao(conexao)
            test_product_dao(conexao)
            return
        case _:
            print("\nOpção inválida passada para func_test_dao() \n")
            return