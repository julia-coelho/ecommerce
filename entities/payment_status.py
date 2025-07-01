#Aluna: Júlia Coelho Rodrigues
#RA: 22408388

#enum de PaymentStatus para status em Payment
class PaymentStatus:
    PENDING = "pendente"
    PAID = "pago"
    FAILED = "falhou"
    CANCELED = "cancelado"
    DISPUTED = "em disputa"


    @staticmethod
    def is_valid(type: str) -> bool:
        return type in {
            PaymentStatus.PENDING,
            PaymentStatus.PAID,
            PaymentStatus.FAILED,
            PaymentStatus.CANCELED,
            PaymentStatus.DISPUTED
        }