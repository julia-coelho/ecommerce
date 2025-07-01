#Aluna: Júlia Coelho Rodrigues
#RA: 22408388

from tests import teste_construtor, teste_metodo

def test_payment():
    """teste da classe-entidade Payment"""

    from entities import Date, Category, Product
    from entities.address import Address
    from entities.customer import Customer
    from entities.order import Order
    from entities.payment import Payment
    from entities.payment_type import PaymentType
    from entities.payment_status import PaymentStatus
    from entities.order_item import OrderItem

    print("\n===========================")
    print("Testes da classe Payment")
    print("===========================\n")

    # os testes completos do construtor e metodos virao em seguida
    # objetos auxiliares
    endereco = Address("70000-000", "DF", "Brasília", "Asa Norte", "Rua A", "10")
    cliente = Customer("Paciente Zero", "paz@email.com", "hash123", Date(1,1,1990), "61999999999", endereco, id=1)
    pedido = Order(customer=cliente, id=999, total=20.0, full_price=25.0, global_discount=5.0)
    data_futura = Date(1, 1, 2050)

    #construtor
    print("\n Testes do Construtor\n")

    # testes positivos
    pagamento_min = teste_construtor(lambda: Payment(order=pedido, type=PaymentType.PIX, transaction_id="TRX123", payer_name="Paciente Zero", account_identifier="CPF123"), "Payment válido com dados mínimos (sem id, sem status passado explicitamente, sem payment_date e sem total passado explicitamente)")
    pagamento_complete = teste_construtor(lambda: Payment(id=1, order=pedido, type=PaymentType.BOLETO, transaction_id="TRX456", payer_name="João", account_identifier="CPF000", total=pedido.total, status=PaymentStatus.PAID, payment_date=data_futura), "Payment válido com dados completos (com id, com payment_date, com total)")
    print("\n")

    # testes negativos - order
    base_kwargs = dict(type=PaymentType.PIX, transaction_id="TX", payer_name="A", account_identifier="X")
    teste_construtor(lambda: Payment(order="pedido", **base_kwargs), "Payment com order=str")
    teste_construtor(lambda: Payment(order=object(), **base_kwargs), "Payment com order=object")
    teste_construtor(lambda: Payment(order=None, **base_kwargs), "Payment com order=None")
    teste_construtor(lambda: Payment(type=PaymentType.PIX, transaction_id="TX", payer_name="A", account_identifier="X"), "Payment sem order")
    print("\n")

    # testes negativos - type
    base_kwargs = dict(order=pedido, transaction_id="TX", payer_name="A", account_identifier="X")
    teste_construtor(lambda: Payment(type="pagamento", **base_kwargs), "Payment com type=string inválida")
    teste_construtor(lambda: Payment(type="", **base_kwargs), "Payment com type=string inválida (vazia)")
    teste_construtor(lambda: Payment(type=123, **base_kwargs), "Payment com type=int")
    teste_construtor(lambda: Payment(type=object(), **base_kwargs), "Payment com type=object")
    teste_construtor(lambda: Payment(type=None, **base_kwargs), "Payment com type=None")
    teste_construtor(lambda: Payment(order=pedido, transaction_id="TX", payer_name="A", account_identifier="X"), "Payment sem type")
    print("\n")

    # testes negativos - transaction_id
    base_kwargs = dict(order=pedido, type=PaymentType.PIX, payer_name="A", account_identifier="X")
    teste_construtor(lambda: Payment(transaction_id="", **base_kwargs), "Payment com transaction_id=string inválida (vazia)")
    teste_construtor(lambda: Payment(transaction_id=123, **base_kwargs), "Payment com transaction_id=int")
    teste_construtor(lambda: Payment(transaction_id=object(), **base_kwargs), "Payment com transaction_id=object")
    teste_construtor(lambda: Payment(transaction_id=None, **base_kwargs), "Payment com transaction_id=None")
    teste_construtor(lambda: Payment(order=pedido, type=PaymentType.PIX, payer_name="A", account_identifier="X"), "Payment sem transaction_id")
    print("\n")

    # testes negativos - payer_name
    base_kwargs = dict(order=pedido, type=PaymentType.PIX, transaction_id="TX", account_identifier="X")
    teste_construtor(lambda: Payment(payer_name="", **base_kwargs), "Payment com payer_name=string inválida (vazia)")
    teste_construtor(lambda: Payment(payer_name=123, **base_kwargs), "Payment com payer_name=int")
    teste_construtor(lambda: Payment(payer_name=object(), **base_kwargs), "Payment com payer_name=object")
    teste_construtor(lambda: Payment(payer_name=None, **base_kwargs), "Payment com payer_name=None")
    teste_construtor(lambda: Payment(order=pedido, type=PaymentType.PIX, transaction_id="TX", account_identifier="X"), "Payment sem payer_name")
    print("\n")

    # testes negativos - account_identifier
    base_kwargs = dict(order=pedido, type=PaymentType.PIX, transaction_id="TX", payer_name="A")
    teste_construtor(lambda: Payment(account_identifier="", **base_kwargs), "Payment com account_identifier=string inválida (vazia)")
    teste_construtor(lambda: Payment(account_identifier=123, **base_kwargs), "Payment com account_identifier=int")
    teste_construtor(lambda: Payment(account_identifier=object(), **base_kwargs), "Payment com account_identifier=object")
    teste_construtor(lambda: Payment(account_identifier=None, **base_kwargs), "Payment com account_identifier=None")
    teste_construtor(lambda: Payment(order=pedido, type=PaymentType.PIX, transaction_id="TX", payer_name="A"), "Payment sem account_identifier")
    print("\n")

    # testes negativos - id
    base_kwargs = dict(order=pedido, type=PaymentType.PIX, transaction_id="TX", payer_name="A", account_identifier="X")
    teste_construtor(lambda: Payment(id=-1, **base_kwargs), "Payment com id negativo")
    teste_construtor(lambda: Payment(id="10", **base_kwargs), "Payment com id=str")
    teste_construtor(lambda: Payment(id=3.5, **base_kwargs), "Payment com id=float")
    teste_construtor(lambda: Payment(id=object(), **base_kwargs), "Payment com id=object")
    print("\n")

    # testes negativos - total
    base_kwargs = dict(order=pedido, type=PaymentType.PIX, transaction_id="TX", payer_name="A", account_identifier="X")
    teste_construtor(lambda: Payment(total=-5.0, **base_kwargs), "Payment com total negativo")
    teste_construtor(lambda: Payment(total=0.0, **base_kwargs), "Payment com total=0.0 (order deveria ser gratuita e nunca gerar payment)")
    teste_construtor(lambda: Payment(total="20.0", **base_kwargs), "Payment com total=string")
    teste_construtor(lambda: Payment(total=object(), **base_kwargs), "Payment com total=object")
    print("\n")

    # testes negativos - status
    base_kwargs = dict(order=pedido, type=PaymentType.PIX, transaction_id="TX", payer_name="A", account_identifier="X")
    teste_construtor(lambda: Payment(status="pagamento", **base_kwargs), "Payment com status=string inválida")
    teste_construtor(lambda: Payment(status="", **base_kwargs), "Payment com status=string inválida (vazia)")
    teste_construtor(lambda: Payment(status=123, **base_kwargs), "Payment com status=int")
    teste_construtor(lambda: Payment(status=object(), **base_kwargs), "Payment com status=object")
    teste_construtor(lambda: Payment(status=None, **base_kwargs), "Payment com status=None")
    print("\n")

    # metodos
    print("\n Testes dos Métodos\n")
    if pagamento_min and pagamento_complete:

        # __str__
        teste_metodo(lambda: str(pagamento_min), "__str__() de Payment válido com dados mínimos (sem id, sem status passado explicitamente, sem payment_date e sem total passado explicitamente)")
        teste_metodo(lambda: str(pagamento_complete), "__str__() de Payment válido com dados completos (com id, com status passado explicitamente, com payment_date e com total passado explicitamente)")
        print("\n")

        # __eq__
        igual = Payment(order=pedido, type=PaymentType.PIX, transaction_id="TX1", payer_name="Paciente Zero", account_identifier="CPF123", id=2)
        mesmo_id = Payment(order=pedido, type=PaymentType.PIX, transaction_id="TX1", payer_name="Paciente Zero", account_identifier="CPF123", id=2)
        diferente = Payment(order=pedido, type=PaymentType.PIX, transaction_id="TX2", payer_name="Outro", account_identifier="CPF999", id=3)
        sem_id = Payment(order=pedido, type=PaymentType.PIX, transaction_id="TX1", payer_name="Paciente Zero", account_identifier="CPF123")
        teste_metodo(lambda: igual == mesmo_id, "__eq__() com id igual")
        teste_metodo(lambda: igual == diferente, "__eq__() com id diferente")
        teste_metodo(lambda: igual == sem_id, "__eq__() com um Payment sem id")
        teste_metodo(lambda: igual == "string", "__eq__() Payment X string")
        teste_metodo(lambda: igual == object(), "__eq__() Payment X Object")
        teste_metodo(lambda: igual == None, "__eq__() Payment X None")
        print("\n")

        # get_formatted_total()
        teste_metodo(lambda: pagamento_min.get_formatted_total(), "get_formatted_total() de Payment válido com dados mínimos (sem id, sem status passado explicitamente, sem payment_date e sem total passado explicitamente)")
        teste_metodo(lambda: pagamento_complete.get_formatted_total(), "get_formatted_total() de Payment válido com dados completos (com id, com status passado explicitamente, com payment_date e com total passado explicitamente)")
        print("\n")

        # is_pending()
        pago = Payment(order=pedido, type=PaymentType.PIX, transaction_id="TRX789", payer_name="Paciente Zero", account_identifier="CPF123", total=pedido.total, status=PaymentStatus.PAID)
        cancelado = Payment(order=pedido, type=PaymentType.PIX, transaction_id="TRX000", payer_name="Paciente Um", account_identifier="CPF321", total=pedido.total, status=PaymentStatus.CANCELED)
        falha = Payment(order=pedido, type=PaymentType.PIX, transaction_id="TRXFAIL", payer_name="Paciente Dois", account_identifier="CPF456", total=pedido.total)
        cancel = Payment(order=pedido, type=PaymentType.PIX, transaction_id="TRXCANC", payer_name="Paciente Três", account_identifier="CPF654", total=pedido.total)
        disputa = Payment(order=pedido, type=PaymentType.PIX, transaction_id="TRXDISP", payer_name="Paciente Zero", account_identifier="CPF123", total=pedido.total, status=PaymentStatus.PAID)
        pendente = Payment(order=pedido, type=PaymentType.PIX, transaction_id="TRX111", payer_name="Paciente Um", account_identifier="CPF321", total=pedido.total, status=PaymentStatus.PENDING)
        pendente2 = Payment(order=pedido, type=PaymentType.PIX, transaction_id="TRX222", payer_name="Paciente Dois", account_identifier="CPF456", total=pedido.total, status=PaymentStatus.PENDING)
        teste_metodo(lambda: pendente.is_pending(), "is_pending() de Payment com status PENDING não-default")
        teste_metodo(lambda: pagamento_min.is_pending(), "is_pending() de Payment com status default (PENDING)")
        teste_metodo(lambda: pago.is_pending(), "is_pending() de Payment com status que não é PENDING (PAID)")
        teste_metodo(lambda: cancelado.is_pending(), "is_pending() de Payment com status que não é PENDING (é CANCELED)")
        print("\n")

        # is_successful()
        teste_metodo(lambda: pago.is_successful(), "is_successful() de Payment com status PAID (deve retornar True)")
        teste_metodo(lambda: pendente.is_successful(), "is_successful() de Payment com status PENDING (deve retornar False)")
        teste_metodo(lambda: cancelado.is_successful(), "is_successful() de Payment com status CANCELED (deve retornar False)")
        print("\n")

        # was_paid()
        pendente2=pendente
        teste_metodo(lambda: pendente.was_paid(), "was_paid() partindo de status PENDING (ok esperado)")
        teste_metodo(lambda: pendente.status, "Verificando status após was_paid() ('pago' esperado)")
        teste_metodo(lambda: pendente.was_paid(), "was_paid() partindo de status PAID (erro esperado)")
        teste_metodo(lambda: pendente.status, "Verificando status após was_paid() ('pago' esperado)")
        teste_metodo(lambda: cancelado.was_paid(), "was_paid() partindo de status CANCELED (erro esperado)")
        teste_metodo(lambda: cancelado.status, "Verificando status após was_paid() ('cancelado' esperado)")
        print("\n")

        # failed()
        teste_metodo(lambda: falha.failed(), "failed() partindo de status PENDING (ok esperado)")
        teste_metodo(lambda: falha.status, "Verificando status após failed() ('falhou' esperado)")
        teste_metodo(lambda: falha.failed(), "failed() partindo de status FAILED (erro esperado)")
        teste_metodo(lambda: falha.status, "Verificando status após failed() ('falhou' esperado)")
        teste_metodo(lambda: pendente.failed(), "failed() partindo de status PAID (erro esperado)")
        teste_metodo(lambda: pendente.status, "Verificando status após failed() ('pago' esperado)")
        print("\n")

        # was_canceled()
        teste_metodo(lambda: cancel.was_canceled(), "was_canceled() partindo de status PENDING (ok esperado)")
        teste_metodo(lambda: cancel.status, "Verificando status após was_canceled() ('cancelado' esperado)")
        teste_metodo(lambda: cancel.was_canceled(), "was_canceled() partindo de status CANCELED (erro esperado)")
        teste_metodo(lambda: cancel.status, "Verificando status após was_canceled() ('cancelado' esperado)")
        teste_metodo(lambda: pendente.was_canceled(), "was_canceled() partindo de status PAID (erro esperado)")
        teste_metodo(lambda: pendente.status, "Verificando status após was_canceled() ('pago' esperado)")
        print("\n")

        # was_disputed()
        teste_metodo(lambda: disputa.was_disputed(), "was_disputed() partindo de status PAID (ok esperado)")
        teste_metodo(lambda: disputa.status, "Verificando status após was_disputed() ('em disputa' esperado)")
        teste_metodo(lambda: disputa.was_disputed(), "was_disputed() partindo de status DISPUTED (erro esperado)")
        teste_metodo(lambda: disputa.status, "Verificando status após was_disputed() ('em disputa' esperado)")
        teste_metodo(lambda: cancelado.was_disputed(), "was_disputed() partindo de status CANCELED (erro esperado)")
        teste_metodo(lambda: cancelado.status, "Verificando status após was_disputed() ('cancelado' esperado)")
        print("\n")

        # won_dispute_change_to_paid()
        teste_metodo(lambda: disputa.won_dispute_change_to_paid(), "won_dispute_change_to_paid() após was_disputed() (ok esperado)")
        teste_metodo(lambda: disputa.status, "Verificando status após won_dispute_change_to_paid() ('pago' esperado)")
        teste_metodo(lambda: disputa.won_dispute_change_to_paid(), "won_dispute_change_to_paid() partindo de status PAID (erro esperado)")
        teste_metodo(lambda: disputa.status, "Verificando status após won_dispute_change_to_paid() ('pago' esperado)")
        teste_metodo(lambda: pendente2.won_dispute_change_to_paid(), "won_dispute_change_to_paid() partindo de status PENDING (erro esperado)")
        teste_metodo(lambda: pendente2.status, "Verificando status após won_dispute_change_to_paid() ('pendente' esperado)")
        print("\n")

        # lost_dispute_change_to_canceled()
        disputa2 = Payment(order=pedido, type=PaymentType.PIX, transaction_id="TRXPSID", payer_name="Paciente Zero", account_identifier="CPF123", total=pedido.total, status=PaymentStatus.DISPUTED)
        teste_metodo(lambda: disputa2.lost_dispute_change_to_canceled(), "lost_dispute_change_to_canceled() após was_disputed() (ok esperado)")
        teste_metodo(lambda: disputa2.status, "Verificando status após lost_dispute_change_to_canceled() ('cancelado' esperado)")
        teste_metodo(lambda: disputa2.lost_dispute_change_to_canceled(), "lost_dispute_change_to_canceled() partindo de status CANCELED (erro esperado)")
        teste_metodo(lambda: disputa2.status, "Verificando status após lost_dispute_change_to_canceled() ('cancelado' esperado)")
        teste_metodo(lambda: pendente2.lost_dispute_change_to_canceled(), "lost_dispute_change_to_canceled() partindo de status PENDING (erro esperado)")
        teste_metodo(lambda: pendente2.status, "Verificando status após lost_dispute_change_to_canceled() ('pendente' esperado)")
        print("\n")

        # validate_payment()
        teste_metodo(lambda: Payment.validate_payment(pagamento_min), "validate_payment() com objeto Payment válido com dados mínimos (sem id, sem status passado explicitamente, sem payment_date e sem total passado explicitamente)")
        teste_metodo(lambda: Payment.validate_payment(pagamento_complete), "validate_payment() com objeto Payment válido com dados completos (com id, com status passado explicitamente, com payment_date e com total passado explicitamente)")
        teste_metodo(lambda: Payment.validate_payment('string'), "validate_payment() com tipo inválido string")
        teste_metodo(lambda: Payment.validate_payment(123), "validate_payment() com tipo inválido int")
        teste_metodo(lambda: Payment.validate_payment(object()), "validate_payment() com tipo inválido objeto Object")
        teste_metodo(lambda: Payment.validate_payment(None), "validate_payment() com tipo inválido None")
        teste_metodo(lambda: Payment.validate_payment(), "validate_payment() sem argumento")
        print("\n")
