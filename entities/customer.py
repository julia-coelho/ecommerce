#Aluna: Júlia Coelho Rodrigues
#RA: 22408388

from typing import List

from utils import Validator as v
from entities import Date
from entities import Address

#classe entidade customer
class Customer:
    def __init__(
            self, 
            name: str, 
            email: str, 
            password_hash: str, 
            birthday: Date, 
            phone: str, 
            address: Address, 
            id: int|None = None, 
            register_day: Date|None = None
    ) -> None:
        #validacao basica:
        if id is not None:
            v.validate_id(id)
        v.validate_name(name)
        v.validate_email(email)
        v.validate_name(password_hash)
        Date.validate_date(birthday)
        v.validate_phone(phone)
        Address.validate_address(address)
        if register_day is None:
            register_day = Date.today()
        Date.validate_date(register_day)

        #atribuicoes
        self.id = id
        self.name = name
        self.email = email
        self.password_hash = password_hash
        self.birthday = birthday
        self.phone = phone
        self.address = address
        self.register_day = register_day
        self.orders = []
    
    
    def __str__(self) -> str:
        return (
            f"Cliente {self.name} (ID: {self.id})\n"
            f"E-mail: {self.email}\n"
            f"Telefone: {self.phone}\n"
            f"Date de Cadastro: {self.register_day}\n"
            f"Aniversário: {self.birthday}\n"
            f"Endereço: \n{self.address}"
        )

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Customer):
            if (self.id == None) or (other.id == None):
                return False
            return self.id == other.id
        return False
    
    def add_order(self, order: "Order") -> None:
        "adciona uma order em customer.orders, que eh uma lista de orders que o customer ja fez"
        from entities.order import Order
        Order.validate_order(order)
        if order.customer.id != self.id:
            raise ValueError(f"Inconsistente: o cliente ID {order.customer.id} que fez o pedido #{order.id} não é o cliente ID {self.id}, em cujo histórico o pedido está tentando ser colocado.")
        self.orders.append(order)

    def get_order_history(self) -> List["Order"]:
        "retorna lista com todas as orders que o customer ja fez"
        from entities.order import Order
        return self.orders
    
    def get_last_order(self) -> "Order":
        "retorna apenas a ultima order do customer"
        from entities.order import Order
        return self.orders[-1]


    @staticmethod
    def validate_customer(customer: object) -> None:
        if not isinstance(customer, Customer):
            raise TypeError("customer deve ser um objeto da classe Customer")