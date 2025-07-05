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

    print("\n==========================")
    print(" Testes da classe Payment ")
    print("==========================\n")

    # objetos auxiliares
    endereco = Address("70000-000", "DF", "Brasília", "Asa Norte", "Rua A", "10")
    cliente = Customer("Paciente Zero", "paz@email.com", "hash123", Date(1,1,1990), "61999999999", endereco, id=1)
    pedido = Order(customer=cliente, id=999, total=20.0, full_price=25.0, global_discount=5.0)
    data_futura = Date(1, 1, 2050)

    #construtor
    print("\n Testes do Construtor\n")

    # testes positivos
    pagamento_min = teste_construtor(lambda: Payment(order=pedido, type=PaymentType.PIX, transaction_id="TRX123", payer_name="Paciente Zero", account_identifier="CPF123"), "Payment válido com dados mínimos (sem id e payment_date e sem status e total passados explicitamente) (OK esperado)")
    pagamento_complete = teste_construtor(lambda: Payment(id=1, order=pedido, type=PaymentType.BOLETO, transaction_id="TRX456", payer_name="João", account_identifier="CPF000", total=pedido.total, status=PaymentStatus.PAID, payment_date=data_futura), "Payment válido com dados completos (com id e payment_date e com status e total passados explicitamente) (OK esperado)")
    print("\n")

    # testes do construtor relacionados a atributos especificos
    # testes negativos - id (atributo opcional)
    base_kwargs = dict(order=pedido, type=PaymentType.PIX, transaction_id="TX", payer_name="A", account_identifier="X")
    teste_construtor(lambda: Payment(id="um", **base_kwargs), "Payment com id=str (ERRO esperado)")
    teste_construtor(lambda: Payment(id=0, **base_kwargs), "Payment com id=0 (ERRO esperado)")
    teste_construtor(lambda: Payment(id=-1, **base_kwargs), "Payment com id negativo (ERRO esperado)")
    teste_construtor(lambda: Payment(id=3.14, **base_kwargs), "Payment com id=float (ERRO esperado)")
    teste_construtor(lambda: Payment(id=object(), **base_kwargs), "Payment com id=object (ERRO esperado)")
    print("\n")

    # testes negativos - order
    base_kwargs = dict(type=PaymentType.PIX, transaction_id="TX", payer_name="A", account_identifier="X (ERRO esperado)")
    teste_construtor(lambda: Payment(order="pedido", **base_kwargs), "Payment com order=str (ERRO esperado)")
    teste_construtor(lambda: Payment(order=object(), **base_kwargs), "Payment com order=object (ERRO esperado)")
    teste_construtor(lambda: Payment(order=None, **base_kwargs), "Payment com order=None (ERRO esperado)")
    teste_construtor(lambda: Payment(type=PaymentType.PIX, transaction_id="TX", payer_name="A", account_identifier="X"), "Payment sem order (ERRO esperado)")
    print("\n")

    # testes negativos - type
    base_kwargs = dict(order=pedido, transaction_id="TX", payer_name="A", account_identifier="X")
    teste_construtor(lambda: Payment(type="pagamento", **base_kwargs), "Payment com type=string inválida (ERRO esperado)")
    teste_construtor(lambda: Payment(type="", **base_kwargs), "Payment com type=string inválida (vazia) (ERRO esperado)")
    teste_construtor(lambda: Payment(type=123, **base_kwargs), "Payment com type=int (ERRO esperado)")
    teste_construtor(lambda: Payment(type=object(), **base_kwargs), "Payment com type=object (ERRO esperado)")
    teste_construtor(lambda: Payment(type=None, **base_kwargs), "Payment com type=None (ERRO esperado)")
    teste_construtor(lambda: Payment(order=pedido, transaction_id="TX", payer_name="A", account_identifier="X"), "Payment sem type (ERRO esperado)")
    print("\n")

    # testes negativos - transaction_id
    base_kwargs = dict(order=pedido, type=PaymentType.PIX, payer_name="A", account_identifier="X")
    teste_construtor(lambda: Payment(transaction_id="", **base_kwargs), "Payment com transaction_id=string inválida (vazia) (ERRO esperado)")
    teste_construtor(lambda: Payment(transaction_id=123, **base_kwargs), "Payment com transaction_id=int (ERRO esperado)")
    teste_construtor(lambda: Payment(transaction_id=object(), **base_kwargs), "Payment com transaction_id=object (ERRO esperado)")
    teste_construtor(lambda: Payment(transaction_id=None, **base_kwargs), "Payment com transaction_id=None (ERRO esperado)")
    teste_construtor(lambda: Payment(order=pedido, type=PaymentType.PIX, payer_name="A", account_identifier="X"), "Payment sem transaction_id (ERRO esperado)")
    print("\n")

    # testes negativos - payer_name
    base_kwargs = dict(order=pedido, type=PaymentType.PIX, transaction_id="TX", account_identifier="X")
    teste_construtor(lambda: Payment(payer_name="", **base_kwargs), "Payment com payer_name=string inválida (vazia) (ERRO esperado)")
    teste_construtor(lambda: Payment(payer_name=123, **base_kwargs), "Payment com payer_name=int (ERRO esperado)")
    teste_construtor(lambda: Payment(payer_name=object(), **base_kwargs), "Payment com payer_name=object (ERRO esperado)")
    teste_construtor(lambda: Payment(payer_name=None, **base_kwargs), "Payment com payer_name=None (ERRO esperado)")
    teste_construtor(lambda: Payment(order=pedido, type=PaymentType.PIX, transaction_id="TX", account_identifier="X"), "Payment sem payer_name (ERRO esperado)")
    print("\n")

    # testes negativos - account_identifier
    base_kwargs = dict(order=pedido, type=PaymentType.PIX, transaction_id="TX", payer_name="A")
    teste_construtor(lambda: Payment(account_identifier="", **base_kwargs), "Payment com account_identifier=string inválida (vazia) (ERRO esperado)")
    teste_construtor(lambda: Payment(account_identifier=123, **base_kwargs), "Payment com account_identifier=int (ERRO esperado)")
    teste_construtor(lambda: Payment(account_identifier=object(), **base_kwargs), "Payment com account_identifier=object (ERRO esperado)")
    teste_construtor(lambda: Payment(account_identifier=None, **base_kwargs), "Payment com account_identifier=None (ERRO esperado)")
    teste_construtor(lambda: Payment(order=pedido, type=PaymentType.PIX, transaction_id="TX", payer_name="A"), "Payment sem account_identifier (ERRO esperado)")
    print("\n")

    # testes negativos - status (atributo opcional)
    base_kwargs = dict(order=pedido, type=PaymentType.PIX, transaction_id="TX", payer_name="A", account_identifier="X")
    teste_construtor(lambda: Payment(status="pagamento", **base_kwargs), "Payment com status=string inválida (ERRO esperado)")
    teste_construtor(lambda: Payment(status="", **base_kwargs), "Payment com status=string inválida (vazia) (ERRO esperado)")
    teste_construtor(lambda: Payment(status=123, **base_kwargs), "Payment com status=int (ERRO esperado)")
    teste_construtor(lambda: Payment(status=object(), **base_kwargs), "Payment com status=object (ERRO esperado)")
    teste_construtor(lambda: Payment(status=None, **base_kwargs), "Payment com status=None (ERRO esperado)")
    print("\n")

    # testes negativos - payment_date (atributo opcional)
    base_kwargs = dict(order=pedido, type=PaymentType.PIX, transaction_id="TX", payer_name="A", account_identifier="X")
    teste_construtor(lambda: Payment(payment_date="ontem", **base_kwargs), "Payment com payment_date=str (ERRO esperado)")
    teste_construtor(lambda: Payment(payment_date=123, **base_kwargs), "Payment com payment_date=int (ERRO esperado)")
    teste_construtor(lambda: Payment(payment_date=object(), **base_kwargs), "Payment com payment_date=object (ERRO esperado)")
    print("\n")

    # testes negativos - total (atributo opcional)
    base_kwargs = dict(order=pedido, type=PaymentType.PIX, transaction_id="TX", payer_name="A", account_identifier="X")
    teste_construtor(lambda: Payment(total=-5.0, **base_kwargs), "Payment com total negativo (ERRO esperado)")
    teste_construtor(lambda: Payment(total=0.0, **base_kwargs), "Payment com total=0.0 (order deveria ser gratuita e nunca gerar payment) (ERRO esperado)")
    teste_construtor(lambda: Payment(total="20.0", **base_kwargs), "Payment com total=string (ERRO esperado)")
    teste_construtor(lambda: Payment(total=object(), **base_kwargs), "Payment com total=object (ERRO esperado)")
    print("\n")


    # metodos
    print("\n Testes dos Métodos\n")
    if pagamento_min and pagamento_complete:

        # __str__
        teste_metodo(lambda: str(pagamento_min), "__str__() de Payment válido com dados mínimos (sem id, sem status passado explicitamente, sem payment_date e sem total passado explicitamente) (payment com transaction_id='TRX123' esperado)")
        teste_metodo(lambda: str(pagamento_complete), "__str__() de Payment válido com dados completos (com id, com status passado explicitamente, com payment_date e com total passado explicitamente) (payment com transaction_id='TRX456' esperado)")
        print("\n")

        # __eq__
        igual = Payment(order=pedido, type=PaymentType.PIX, transaction_id="TX1", payer_name="Paciente Zero", account_identifier="CPF123", id=2)
        mesmo_id = Payment(order=pedido, type=PaymentType.PIX, transaction_id="TX1", payer_name="Paciente Zero", account_identifier="CPF123", id=2)
        diferente = Payment(order=pedido, type=PaymentType.PIX, transaction_id="TX2", payer_name="Outro", account_identifier="CPF999", id=3)
        sem_id = Payment(order=pedido, type=PaymentType.PIX, transaction_id="TX1", payer_name="Paciente Zero", account_identifier="CPF123")
        teste_metodo(lambda: igual == mesmo_id, "__eq__() com id igual (True esperado)")
        teste_metodo(lambda: igual == diferente, "__eq__() com id diferente (False esperado)")
        teste_metodo(lambda: igual == sem_id, "__eq__() com um Payment sem id (False esperado)")
        teste_metodo(lambda: igual == "string", "__eq__() Payment X string (False esperado)")
        teste_metodo(lambda: igual == object(), "__eq__() Payment X Object (False esperado)")
        teste_metodo(lambda: igual == None, "__eq__() Payment X None (False esperado)")
        print("\n")

        # get_formatted_total()
        teste_metodo(lambda: pagamento_min.get_formatted_total(), "get_formatted_total() de Payment válido com dados mínimos (sem id, sem status passado explicitamente, sem payment_date e sem total passado explicitamente) ('R$ 20.00' esperado)")
        teste_metodo(lambda: pagamento_complete.get_formatted_total(), "get_formatted_total() de Payment válido com dados completos (com id, com status passado explicitamente, com payment_date e com total passado explicitamente) ('R$ 20.00' esperado)")
        print("\n")

        # is_pending()
        pago = Payment(order=pedido, type=PaymentType.PIX, transaction_id="TRX789", payer_name="Paciente Zero", account_identifier="CPF123", total=pedido.total, status=PaymentStatus.PAID)
        cancelado = Payment(order=pedido, type=PaymentType.PIX, transaction_id="TRX000", payer_name="Paciente Um", account_identifier="CPF321", total=pedido.total, status=PaymentStatus.CANCELED)
        falha = Payment(order=pedido, type=PaymentType.PIX, transaction_id="TRXFAIL", payer_name="Paciente Dois", account_identifier="CPF456", total=pedido.total)
        cancel = Payment(order=pedido, type=PaymentType.PIX, transaction_id="TRXCANC", payer_name="Paciente Três", account_identifier="CPF654", total=pedido.total)
        disputa = Payment(order=pedido, type=PaymentType.PIX, transaction_id="TRXDISP", payer_name="Paciente Zero", account_identifier="CPF123", total=pedido.total, status=PaymentStatus.PAID)
        pendente = Payment(order=pedido, type=PaymentType.PIX, transaction_id="TRX111", payer_name="Paciente Um", account_identifier="CPF321", total=pedido.total, status=PaymentStatus.PENDING)
        pendente2 = Payment(order=pedido, type=PaymentType.PIX, transaction_id="TRX222", payer_name="Paciente Zero", account_identifier="CPF123", total=pedido.total, status=PaymentStatus.PENDING)
        teste_metodo(lambda: pendente.is_pending(), "is_pending() de Payment com status PENDING não-default (True esperado)")
        teste_metodo(lambda: pagamento_min.is_pending(), "is_pending() de Payment com status default (PENDING) (True esperado)")
        teste_metodo(lambda: pago.is_pending(), "is_pending() de Payment com status que não é PENDING (é PAID) (False esperado)")
        teste_metodo(lambda: cancelado.is_pending(), "is_pending() de Payment com status que não é PENDING (é CANCELED) (False esperado)")
        print("\n")

        # is_successful()
        teste_metodo(lambda: pago.is_successful(), "is_successful() de Payment com status PAID (True esperado)")
        teste_metodo(lambda: pendente.is_successful(), "is_successful() de Payment com status PENDING (False esperado)")
        teste_metodo(lambda: cancelado.is_successful(), "is_successful() de Payment com status CANCELED (False esperado)")
        print("\n")

        # was_paid() (positivos)
        teste_metodo(lambda: pendente.was_paid(), "was_paid() partindo de status PENDING (OK esperado)")
        teste_metodo(lambda: pendente.status, "Verificando status após was_paid() ('pago' esperado)")

        # was_paid() (negativos)
        teste_metodo(lambda: pendente.was_paid(), "was_paid() partindo de status PAID (ERRO esperado)")
        teste_metodo(lambda: pendente.status, "Verificando status após was_paid() ('pago' esperado)")
        teste_metodo(lambda: cancelado.was_paid(), "was_paid() partindo de status CANCELED (ERRO esperado)")
        teste_metodo(lambda: cancelado.status, "Verificando status após was_paid() ('cancelado' esperado)")
        print("\n")

        # failed() (positivos)
        teste_metodo(lambda: falha.failed(), "failed() partindo de status PENDING (OK esperado)")
        teste_metodo(lambda: falha.status, "Verificando status após failed() ('falhou' esperado)")

        # failed() (negativos)
        teste_metodo(lambda: falha.failed(), "failed() partindo de status FAILED (ERRO esperado)")
        teste_metodo(lambda: falha.status, "Verificando status após failed() ('falhou' esperado)")
        teste_metodo(lambda: pendente.failed(), "failed() partindo de status PAID (ERRO esperado)")
        teste_metodo(lambda: pendente.status, "Verificando status após failed() ('pago' esperado)")
        print("\n")

        # was_canceled() (positivos)
        teste_metodo(lambda: cancel.was_canceled(), "was_canceled() partindo de status PENDING (OK esperado)")
        teste_metodo(lambda: cancel.status, "Verificando status após was_canceled() ('cancelado' esperado)")

        # was_canceled() (negativos)
        teste_metodo(lambda: cancel.was_canceled(), "was_canceled() partindo de status CANCELED (ERRO esperado)")
        teste_metodo(lambda: cancel.status, "Verificando status após was_canceled() ('cancelado' esperado)")
        teste_metodo(lambda: pendente.was_canceled(), "was_canceled() partindo de status PAID (ERRO esperado)")
        teste_metodo(lambda: pendente.status, "Verificando status após was_canceled() ('pago' esperado)")
        print("\n")

        # was_disputed() (positivos)
        teste_metodo(lambda: disputa.was_disputed(), "was_disputed() partindo de status PAID (OK esperado)")
        teste_metodo(lambda: disputa.status, "Verificando status após was_disputed() ('em disputa' esperado)")

        # was_disputed() (negativos)
        teste_metodo(lambda: disputa.was_disputed(), "was_disputed() partindo de status DISPUTED (ERRO esperado)")
        teste_metodo(lambda: disputa.status, "Verificando status após was_disputed() ('em disputa' esperado)")
        teste_metodo(lambda: cancelado.was_disputed(), "was_disputed() partindo de status CANCELED (ERRO esperado)")
        teste_metodo(lambda: cancelado.status, "Verificando status após was_disputed() ('cancelado' esperado)")
        print("\n")

        # won_dispute_change_to_paid() (positivos)
        teste_metodo(lambda: disputa.won_dispute_change_to_paid(), "won_dispute_change_to_paid() após was_disputed() (OK esperado)")
        teste_metodo(lambda: disputa.status, "Verificando status após won_dispute_change_to_paid() ('pago' esperado)")

        # won_dispute_change_to_paid() (negativos)
        teste_metodo(lambda: disputa.won_dispute_change_to_paid(), "won_dispute_change_to_paid() partindo de status PAID (ERRO esperado)")
        teste_metodo(lambda: disputa.status, "Verificando status após won_dispute_change_to_paid() ('pago' esperado)")
        teste_metodo(lambda: pendente2.won_dispute_change_to_paid(), "won_dispute_change_to_paid() partindo de status PENDING (ERRO esperado)")
        teste_metodo(lambda: pendente2.status, "Verificando status após won_dispute_change_to_paid() ('pendente' esperado)")
        print("\n")

        # lost_dispute_change_to_canceled() (positivos)
        disputa2 = Payment(order=pedido, type=PaymentType.PIX, transaction_id="TRXPSID", payer_name="Paciente Zero", account_identifier="CPF123", total=pedido.total, status=PaymentStatus.DISPUTED)
        teste_metodo(lambda: disputa2.lost_dispute_change_to_canceled(), "lost_dispute_change_to_canceled() após was_disputed() (OK esperado)")
        teste_metodo(lambda: disputa2.status, "Verificando status após lost_dispute_change_to_canceled() ('cancelado' esperado)")

        # lost_dispute_change_to_canceled() (negativos)
        teste_metodo(lambda: disputa2.lost_dispute_change_to_canceled(), "lost_dispute_change_to_canceled() partindo de status CANCELED (ERRO esperado)")
        teste_metodo(lambda: disputa2.status, "Verificando status após lost_dispute_change_to_canceled() ('cancelado' esperado)")
        teste_metodo(lambda: pendente2.lost_dispute_change_to_canceled(), "lost_dispute_change_to_canceled() partindo de status PENDING (ERRO esperado)")
        teste_metodo(lambda: pendente2.status, "Verificando status após lost_dispute_change_to_canceled() ('pendente' esperado)")
        print("\n")

        # validate_payment() (positivos)
        teste_metodo(lambda: Payment.validate_payment(pagamento_min), "validate_payment() com objeto Payment válido com dados mínimos (sem id, sem status passado explicitamente, sem payment_date e sem total passado explicitamente) (OK esperado)")
        teste_metodo(lambda: Payment.validate_payment(pagamento_complete), "validate_payment() com objeto Payment válido com dados completos (com id, com status passado explicitamente, com payment_date e com total passado explicitamente) (OK esperado)")

        # validate_payment() (negativos)
        teste_metodo(lambda: Payment.validate_payment('string'), "validate_payment() com tipo inválido string (ERRO esperado)")
        teste_metodo(lambda: Payment.validate_payment(123), "validate_payment() com tipo inválido int (ERRO esperado)")
        teste_metodo(lambda: Payment.validate_payment(object()), "validate_payment() com tipo inválido objeto Object (ERRO esperado)")
        teste_metodo(lambda: Payment.validate_payment(None), "validate_payment() com tipo inválido None (ERRO esperado)")
        teste_metodo(lambda: Payment.validate_payment(), "validate_payment() sem argumento (ERRO esperado)")
        print("\n")
