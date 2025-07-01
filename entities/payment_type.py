#Aluna: Júlia Coelho Rodrigues
#RA: 22408388

#enum de PaymentType para type em Payment
class PaymentType:
    DEBITO = "debito"
    CREDITO = "credito"
    BOLETO = "boleto"
    PIX = "pix"
    PAYPAL = "paypal"


    @staticmethod
    def is_valid(type: str) -> bool:
        return type in {
            PaymentType.DEBITO,
            PaymentType.CREDITO,
            PaymentType.BOLETO,
            PaymentType.PIX,
            PaymentType.PAYPAL
        }