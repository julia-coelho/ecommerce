#Aluna: Júlia Coelho Rodrigues
#RA: 22408388

from utils import Validator as v
from entities import Date
from entities import PaymentType
from entities import PaymentStatus

#classe entidade Payment
class Payment:
    def __init__(
            self, 
            order: "Order",
            type: str, 
            transaction_id: str, 
            payer_name: str, 
            account_identifier: str, 
            id: int|None = None, 
            status: str = PaymentStatus.PENDING, 
            payment_date: Date|None = None,
            total: float|None = None
    ) -> None:
        #verificacao basica
        if id is not None:
            v.validate_id(id)
        from entities.order import Order
        Order.validate_order(order)
        if total is None:
            total = order.total
        v.validate_price(total)
        v.validate_name(type)
        v.validate_name(transaction_id)
        v.validate_name(payer_name)
        v.validate_name(account_identifier)
        if payment_date is not None:
            Date.validate_date(payment_date)
        
        #valida logica pagamento so deve ser criado para pedidos nao-gratuitos
        if total == 0:
            raise ValueError(f"Total a ser pago de pagamento inválido: R$ {total:.2f}. Total de pagamento deve ser maior que R$ 0.00")
        #valida tipo de pagamento
        if not PaymentType.is_valid(type):
            raise ValueError(f"Tipo de pagamento inválido: {type}. Tipo de pagamento pode ser: 'debito', 'credito', 'boleto', 'pix' ou 'paypal'")
        
        #valida status
        if not PaymentStatus.is_valid(status):
            raise ValueError(f"Status de pagamento inválido: {status}. Status de pagamento pode ser 'pendente', 'pago', 'falhou', 'cancelado' ou 'em disputa'")
        
        #valida logica de consistencia
        if (status != PaymentStatus.PAID) and (payment_date is not None):
            raise ValueError("Data do pagamento só deve existir se o status do pagamento for 'pago'")               
        
        #atribuicoes
        self.id = id
        self.order = order
        self.total = total
        self.type = type
        self.status = status
        self.transaction_id = transaction_id
        self.payment_date = payment_date
        self.payer = payer_name
        self.account_identifier = account_identifier

    
    def __str__(self) -> str:
        return (
            f"Pagamento #{self.id or '(novo)'} - {self.type.upper()} - {self.status.upper()}\n"
            f"Total: {self.get_formatted_total()}\n"
            f"Transação: {self.transaction_id}\n"
            f"Pagador: {self.payer} ({self.account_identifier})\n"
            f"Data: {self.payment_date or 'Aguardando pagamento'}"
        )
    
    def __eq__(self, other: object) -> bool:
        if isinstance(other, Payment):
            if (self.id == None) or (other.id == None):
                return False
            return self.id == other.id
        return False
    
    def get_formatted_total(self) -> str:
        """retorna total a ser pago com apenas duas casas decimais e com R$"""
        return f"R$ {self.total:.2f}"
    
    def was_paid(self) -> None:
        """muda o estado do payment de 'pendente' para 'pago'"""
        if self.status != PaymentStatus.PENDING:
            raise ValueError(f"Apenas pagamentos em status 'pendente' podem ser pagos. Status atual do pagamento: {self.status}")
        self.status = PaymentStatus.PAID
        self.payment_date = Date.today()

    def failed(self) -> None:
        """muda o estado do payment de 'pendente' para 'falhou'"""
        if self.status != PaymentStatus.PENDING:
            raise ValueError(f"Apenas pagamentos em status 'pendente' podem falhar. Satatus atual do pagamento: {self.status}")
        self.status = PaymentStatus.FAILED

    def was_canceled(self) -> None:
        """muda o estado do payment de 'pendente' para 'cancelado'"""
        if self.status != PaymentStatus.PENDING:
            raise ValueError(f"Apenas pagamentos em status 'pendente' podem ser cancelados. Satatus atual do pagamento: {self.status}")
        self.status = PaymentStatus.CANCELED

    def was_disputed(self) -> None:
        """muda o estado do payment de 'paid' para 'em disputa'"""
        if self.status != PaymentStatus.PAID:
            raise ValueError(f"Apenas pagamentos em status 'pago' podem ser colocados em disputa. Status atual do pagamento: {self.status}")
        self.status = PaymentStatus.DISPUTED    

    def won_dispute_change_to_paid(self) -> None:
        """muda o estado do paymento de 'em disputa' para 'pago'"""
        if self.status != PaymentStatus.DISPUTED:
            raise ValueError(f"Apenas pagamentos em status 'em disputa' podem ganhar disputa para serem pagos. Status atual do pagamento: {self.status}")
        self.status = PaymentStatus.PAID
        self.payment_date = Date.today()

    def lost_dispute_change_to_canceled(self) -> None:
        """muda o estado do paymento de 'em disputa' para 'cancelado'"""
        if self.status != PaymentStatus.DISPUTED:
            raise ValueError(f"Apenas pagamentos em status 'em disputa' podem perder disputa para serem cancelados. Status atual do pagamento: {self.status}")
        self.status = PaymentStatus.CANCELED

    def is_successful(self) -> bool:
        """retorna true se o status de payment eh 'paid', false em qualquer outro caso"""
        return self.status == PaymentStatus.PAID
    
    def is_pending(self) -> bool:
        """retorna true se o status de payment eh 'pending', false em qualquer outro caso"""
        return self.status == PaymentStatus.PENDING
    
    @staticmethod
    def validate_payment(payment) -> None:
        if not isinstance(payment, Payment):
            raise TypeError("payment deve ser um objeto da classe Payment")
