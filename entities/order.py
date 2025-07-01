#Aluna: Júlia Coelho Rodrigues
#RA: 22408388

from utils import Validator as v
from entities import Date

#classe entidade order
class Order:
    def __init__(
            self, 
            customer: "Customer",
            id: int|None = None,
            total: float = 0,
            full_price: float = 0,
            global_discount: float = 0,
            date: Date|None = None
    ) -> None:
        #validacao basica:
        if id is not None:
            v.validate_id(id)
        from entities.customer import Customer
        Customer.validate_customer(customer)
        v.validate_price(total)
        v.validate_price(full_price)
        v.validate_price(global_discount)
        if date is None:
            date = Date.today()
        Date.validate_date(date)

        #verificacao precos
        if global_discount > full_price:
            raise ValueError(f"O desconto total aplicado ao pedido #{id} (R$ {global_discount} é maior do que o preço total sem desconto do pedido (R$ {full_price})")
        if total != (full_price - global_discount):
            raise ValueError(f"Inconsistente: o preço final do pedido (R$ {total}) não é o total sem desconto do pedido (R$ {full_price}) - todo o desconto aplicado ao pedido (R$ {global_discount})")
        

        #atribuicoes
        self.id = id
        self.customer = customer
        self.total = total
        self.full_price = full_price
        self.global_discount = global_discount
        self.date = date
        self.payment = None
        self.items = []


    def __str__(self) -> str:
        status = self.get_payment_status()
        payment = f"Status do Pagamento: {status}"
        return f"Pedido #{self.id} - Total: {self.get_formatted_total()} - " + payment 
    
    def __eq__(self, other: object) -> bool:
        if isinstance(other, Order):
            if (self.id is None) or (other.id is None):
                return False
            return self.id == other.id
        return False
    
    def get_formatted_total(self) -> str:
        """retorna total de order com apenas duas casas decimais e com R$"""
        return f"R$ {self.total:.2f}"
    
    def get_customer_email(self) -> str:
        """retorna o e-mail do customer que fez a order"""
        from entities.customer import Customer
        return self.customer.email
    
    def add_order_discount(self, discount: float) -> None:
        """adciona um desconto a order, sem estar relacionado a nenhum batch ou product especifico"""
        v.validate_price(discount)
        discount_total = self.global_discount + discount
        if discount_total > self.full_price:
            raise ValueError(f"Não é possível acrescentar o desconto R$ {discount}: o desconto total do pedido R$ {discount_total} fica maior do que o preço do pedido sem desconto {self.full_price}")
        self.global_discount += discount
        self.total -= discount
    
    def add_order_item(self, item: "OrderItem") -> None:
        """adciona um orderitem no atributo items: list[OrderItem] da order - deve ser usada exclusivamente para orders que *nao* vieram do db"""
        from entities.order_item import OrderItem
        OrderItem.validate_order_item(item)
        if item.order.id != self.id:
            raise ValueError(f"Inconsistente: o pedido #{item.order.id} ao qual o item #{item.id} produto {item.product.name}, marca {item.product.brand}, faz parte não é o pedido #{self.id} no qual esse item está sendo colocado")
        #calcula o total de desconto dado em item e acrescenta ao global_discount da order
        self.global_discount += item.unit_discount * item.quantity
        #calcula o preco de item se nao houvesse nenhum desconto e soma ao full_price da order
        self.full_price += item.unit_price * item.quantity
        #calcula novo total
        self.total = self.full_price - self.global_discount
        #finalmente acrescenta item a lista de items da order
        self.items.append(item)

    def add_order_item_from_db(self, item: "OrderItem") -> None:
        """adciona um orderitem no atributo items: list[OrderItem] da order - deve ser usada exclusivamente para orders que *vieram* do db"""
        from entities.order_item import OrderItem
        OrderItem.validate_order_item(item)
        if item.order.id != self.id:
            raise ValueError(f"Inconsistente: o pedido #{item.order.id} ao qual o item #{item.id} produto {item.product.name}, marca {item.product.brand}, faz parte não é o pedido #{id} no qual esse item está sendo colocado")
        #soma o total de desconto dado em item aos descontos dados nos outros orderitems de order e verifica se essa soma eh maior do que o global_discount da order
        item_discount = item.unit_discount * item.quantity
        for i in self.items:
            item_discount += i.unit_discount * i.quantity
        if item_discount > self.global_discount:
            raise ValueError(f"Inconsistente: a soma do desconto dos itens ({item_discount}) do pedido é maior do que o desconto total do pedido ({self.global_discount})")
        #soma o preco sem desconto de item ao preco sem desconto dos outros orderitems de order e verifica se essa soma eh maior do que o full_price da order
        item_price = item.unit_price * item.quantity
        for i in self.items:
            item_price += i.unit_price * i.quantity
        if item_price > self.full_price:
            raise ValueError(f"Inconsistente: a soma do preço sem desconto dos itens ({item_price}) do pedido é maior do que o total sem desconto do pedido ({self.full_price})")
        #finalmente acrescenta item a lista de items da order
        self.items.append(item)    

    def set_payment(self, payment: "Payment") -> None:
        """seta o payment da order"""
        from entities.payment import Payment
        from entities import PaymentStatus
        #se a order for de graca, nao tem payment
        if self.total == 0:
            raise ValueError("Pedido GRATUITO, não há necessidade de pagamento")
        Payment.validate_payment(payment)
        #order so aceita payment com status "pending", so depois de estar ligada a order eh que eh para o status do payment mudar
        if payment.status != PaymentStatus.PENDING:
            raise ValueError(f"Pagamento de status {payment.status} não pode ser ligado a um pedido, apenas pagamentos de status 'pendente' podem ser ligados a pedidos")
        if payment.order.id != self.id:
            raise ValueError(f"Inconsistente: o pedido #{payment.order.id} a qual o pagamento (ID {payment.id}) está relacionado não é o pedido #{self.id}, que está tentando receber o pagamento")
        if payment.total != self.total:
            raise ValueError(f"Inconsistente: o total ({payment.get_formatted_total()}) do pagamento ID {payment.id} é diferente do total ({self.get_formatted_total()}) do pedido #{self.id}, que está tentando receber o pagamento")
        self.payment = payment

    def get_payment_status(self) -> str:
        """retorna o status do payment da order"""
        from entities.payment import Payment
        if self.total == 0:
            payment_status = f"GRATUITO"
        else:
            if self.payment is not None:
                payment_status = self.payment.status
            else:
                payment_status = "Pagamento não iniciado"
        return payment_status
        
    @staticmethod
    def validate_order(order: object) -> None:
        if not isinstance(order, Order):
            raise TypeError("order deve ser um objeto da classe Order")