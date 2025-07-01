#Aluna: Júlia Coelho Rodrigues
#RA: 22408388

import re

#classe utilitaria para juntar as verificacoes comuns feitas nas classes
class Validator:
    #validacoes de id
    @staticmethod
    def validate_id(id) -> None:
        if not isinstance(id, int):
            raise TypeError(f"ID {id} não é válida. ID deve ser um valor inteiro")
        if id <= 0:
            raise ValueError(f"ID {id} não é válida. ID deve ser um valor positivo")
    
    @staticmethod
    def validate_id_size(id: int) -> None:
        if len(str(id)) > 6:
            raise ValueError("ID não é válida: o valor máximo possivel de uma ID é 999,999")
        

    #validacoes de nome
    @staticmethod
    def validate_name(name) -> None:
        if not isinstance(name, str):
            raise TypeError(f"Nome {name} não é válido: deve ser do tipo string")
        if not name.strip():
            raise ValueError(f"Nome {name} não é válido. Nome não pode ser vazio")
        
    @staticmethod
    def validate_name_size(name: str) -> None:
        if len(name.strip()) > 75:
            raise ValueError("Nome não é válido: nomes podem ter até 75 caracteres")
        

    #validacoes de preco
    @staticmethod
    def validate_price(price) -> None:
        if not isinstance(price, float|int):
            raise TypeError(f"{price} não é um preço válido. Preços devem ser valores reais")
        if price < 0:
            raise ValueError(f"{price} não é um preço válido. Preços não podem ser negativos")
    
    @staticmethod
    def validate_price_size(price: float|int) -> None:
        if len(str(price)) > 6:
            raise ValueError("Preço não é válido: o valor máximo possível de um preço é 999,999")
    

    #validacoes de quantidade
    @staticmethod
    def validate_quantity(quantity) -> None:
        if not isinstance(quantity, int):
            raise TypeError(f"Quantidade {quantity} não é válida. Quantidades devem ser valores inteiros")
        if quantity < 0:
            raise ValueError(f"Quantidade {quantity} não é válida. Quantidades não podem ser valores negativos")
        
    @staticmethod
    def validate_quantity_size(quantity: int) -> None:
        if len(str(quantity)) > 6:
            raise ValueError("Quantidade não é válida: o valor máximo de uma quantidade é 999,999")
        
    
    #validacao de codigo alfanumerico
    @staticmethod
    def validate_alpha_numeric(number) -> None:
        if not isinstance(number, str):
            raise TypeError(f"{number} não é um código alfanumérico válido: deve ser do tipo string")
        
        number = number.strip().upper()

        if not number:
            raise ValueError("Código alfanumérico não pode ser vazio")
        
        #aceita valores como '123', '45-B' 'S/N', '1000/102'
        if not re.fullmatch(r"[0-9A-Z/-]+", number):
            raise ValueError(f"{number} não é uma opção válida: deve ser um código alfanumérico válido(ex: '123A', 'S/N' '1000/2')")
        
    
    #validacoes de endereco
    @staticmethod
    def validate_cep(cep) -> None:
        if not isinstance(cep, str):
            raise TypeError(f"{cep} não é um CEP válido: deve ser do tipo string")
        
        if not re.fullmatch(r"\d{5}-?\d{3}", cep):
            raise ValueError(f"{cep} não é um CEP válido: deve ter o formato 00000-000 ou 00000000")
        
    @staticmethod
    def validate_state(state) -> None:
        if not isinstance(state, str):
            raise TypeError(f"{state} não é uma opção de estado válida: deve ser do tipo string")
        
        state = state.strip().upper()

        valid_ufs = {
            "AC", "AL", "AP", "AM", 
            "BA", 
            "CE", 
            "DF", 
            "ES", 
            "GO", 
            "MA", "MG", "MT", "MS", 
            "PA", "PB", "PE", "PI", "PR", 
            "RJ", "RN", "RO", "RR", "RS", 
            "SC", "SE", "SP", 
            "TO"
        } 
        
        if state not in valid_ufs:
            raise ValueError(f"{state} não é uma opção válida: deve ser uma sigla UF válida (ex: 'sp', 'rj', 'df')")
        
    
    #validacao de email
    @staticmethod
    def validate_email(email) -> None:
        if not isinstance(email, str):
            raise TypeError(f"{email} não é um e-mail válido: deve ser do tipo string")
        
        email = email.strip()

        pattern = r"^[\w\.-]+@[\w\.-]+\.\w{2,}$"
        if not re.fullmatch(pattern, email):
            raise ValueError(f"E-mail {email} não é válido: não respeita formato geral de e-mail parte_local@dominio.extensao (ex: exemplina@exemplo.com)")
        

    #validacao de telefone
    @staticmethod
    def validate_phone(phone_number) -> None:
        if not isinstance(phone_number, str):
            raise TypeError(f"{phone_number} não é um telefone válido: deve ser do tipo string")
        
        phone_number = phone_number.strip()

        #remove espacos, parenteses e hifens, se houver
        phone_number_clean = re.sub(r"[ \-\(\)]", "", phone_number)

        #agora deve conter apenas numeros
        if not phone_number_clean.isdigit():
            raise ValueError(f"{phone_number} não é um número de telefone válido. Números de telefone devem conter devem conter apenas dígitos numéricos, hífen ou parênteses") 

        if len(phone_number_clean) != 11:
            raise ValueError(f"Número de telefone {phone_number} inválido: deve ter exatamente 11 digitos (ddd + numero)")
        
        ddd = phone_number_clean[:2]
        number = phone_number_clean[2:]

        #validacao basica de ddds possiveis no brasil
        valid_ddds = {
            "11", "12", "13", "14", "15", "16", "17", "18", "19",
            "21", "22", "24", "27", "28",
            "31", "32", "33", "34", "35", "37", "38",
            "41", "42", "43", "44", "45", "46", "47", "48", "49",
            "51", "53", "54", "55",
            "61", "62", "63", "64", "65", "66", "67", "68", "69",
            "71", "73", "74", "75", "77", "79",
            "81", "82", "83", "84", "85", "86", "87", "88", "89",
            "91", "92", "93", "94", "95", "96", "97", "98", "99"
        }

        if ddd not in valid_ddds:
            raise ValueError(f"DDD inválido: {ddd}")

        if number[0] not in {"6", "7", "8", "9"}:
            raise ValueError(f"Número de telefone {number} inválido: deve comecar com 6, 7, 8 ou 9")