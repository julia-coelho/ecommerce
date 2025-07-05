#Aluna: Júlia Coelho Rodrigues
#RA: 22408388

import json

from utils import Validator as v

#classe entidade address
class Address:
    def __init__(
            self, 
            cep: str, 
            state: str, 
            city: str, 
            district: str, 
            street: str, 
            number: str, 
            complement: str = ""
    ) -> None:
        #validacao basica:
        v.validate_cep(cep)
        v.validate_state(state)
        v.validate_name(city)
        v.validate_name(district)
        v.validate_name(street)
        v.validate_alpha_numeric(number)
        if complement.strip():
            v.validate_name(complement)

        #atribuicoes
        self.cep = cep
        self.state = state
        self.city = city
        self.district = district
        self.street = street
        self.number = number
        self.complement = complement

    
    def __str__(self) -> str:
        address = f"{self.street}, {self.number}"
        if self.complement.strip():
            address += f", {self.complement}"
        address += (
            f"\n{self.district}\n"
            f"{self.city} - {self.state}\n"
            f"CEP: {self.cep}")
        return address
    
    def to_dict(self) -> dict:
        """transforma o endereco em um dicionario"""
        dicionary_address = {
            "cep" : self.cep,
            "estado" : self.state.upper(),
            "cidade" : self.city.upper(),
            "bairro" : self.district.upper(),
            "logradouro" : self.street.upper(),
            "numero" : self.number.upper(),
        }
        if self.complement.strip():
            dicionary_address["complemento"] = self.complement   
        return dicionary_address
    
    #para salvar um endereco no banco
    def to_string_bank(self) -> str:
        "transforma o objeto, da classe Address, em uma string que o banco consegue gravar em uma unica celula"
        return json.dumps(self.to_dict())
    
    @staticmethod
    def validate_address(address) -> None:
        if not isinstance(address, Address):
            raise TypeError("address deve ser um objeto da classe Address")
        
    @staticmethod
    def from_string(address_string: str) -> "Address":
        "transforma o endereco saido do banco, que esta em formato string, em um objeto da classe Address"
        #transforma address_string em um dicionario
        dictionary_address = json.loads(address_string)

        return Address(
            cep = dictionary_address["cep"],
            state = dictionary_address["estado"],
            city = dictionary_address["cidade"],
            district = dictionary_address["bairro"],
            street = dictionary_address["logradouro"],
            number = dictionary_address["numero"],
            complement = dictionary_address.get("complemento", "")
        )
