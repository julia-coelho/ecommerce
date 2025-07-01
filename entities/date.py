#Aluna: Júlia Coelho Rodrigues
#RA: 22408388

from datetime import datetime, date as dt_date

#classe entidade date
class Date:
    def __init__(self, day: int, month: int, year: int) -> None:
        #validacao basica:
        try:
            datetime(year, month, day)
        except ValueError:
            raise ValueError("Data inválida")
        
        #atribuicoes
        self.day = day
        self.month = month
        self.year = year
    

    def __str__(self) -> str:
        return f"{self.day:02d}/{self.month:02d}/{self.year}"
    
    def __eq__(self, other: object) -> bool:
        if isinstance(other, Date):
            if (self.year == other.year):
                if (self.month == other.month):
                    return self.day == other.day
        return False
    
    def to_date(self) -> dt_date:
        """transforma a date tipo minha classe Date em um objeto do tipo date do modulo datetime, que eh usado em python para fazer operacoes com datas"""
        return dt_date(self.year, self.month, self.day)

    #exemplo de data no formato iso: '1998-03-09'
    def to_iso(self) -> str:
        """transforma objeto do tipo minha classe Date para uma string de data no formato iso"""
        return f"{self.year:04d}-{self.month:02d}-{self.day:02d}"
    
    @staticmethod
    #exemplo de data no formato iso: '1998-03-09'
    def from_iso(iso_date: str) -> "Date":
        """transforma uma data em formato iso tipo string em um objeto tipo minha classe Date"""
        year, month, day = map(int, iso_date.split("-"))
        return Date(day, month, year)
    
    @staticmethod
    def validate_date(date) -> None:
        if not isinstance(date, Date):
            raise TypeError("date deve ser um objeto da classe Date")
    
    @staticmethod
    def datetime_today() -> dt_date:
        """calcula a data de hoje como objeto da classe date do modulo datetime"""
        return dt_date.today()
    
    @staticmethod
    def today() -> "Date":
        """calcula a data de hoje como objeto da minha classe Date"""
        d = Date.datetime_today()
        return Date(d.day, d.month, d.year)