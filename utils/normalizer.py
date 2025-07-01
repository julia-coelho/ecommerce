#Aluna: Júlia Coelho Rodrigues
#RA: 22408388

import unicodedata as uc

#classe utilitaria para normalizar palavras
class Normalizer:
    @staticmethod
    def normalize(text: str) -> str:
        """remove acentos e transforma em uppercase"""
        return ''.join(
            c for c in uc.normalize('NFD', text)
            if uc.category(c) != 'Mn'
        ).upper()
    
    @staticmethod
    def normalize_for_storage(text: str) -> str:
        """remove acentos e mantem caixa original - usada para colocar um registro no banco"""
        return ''.join(
            c for c in uc.normalize('NFD', text)
            if uc.category(c) != 'Mn'        
        )
    
    @staticmethod
    def normalize_match_keyword_sql(text: str) -> str:
        """remove acentos, transforma em lowercase e envolve com % para LIKE - feito para comparacoes *dentro* do sql"""
        text = Normalizer.normalize_for_storage(text)
        return f"%{text.lower()}%"

    @staticmethod
    def build_keyword_sql_clause(field_names: list[str]) -> str:
        """
        retorna uma clausula sql para busca com LIKE em campos especificados,
        como: "(LOWER(nome) LIKE ? OR LOWER(email) LIKE ?)"
        """
        clause = " OR ".join([f"LOWER({field}) LIKE ?" for field in field_names])
        return f"({clause})"

    @staticmethod
    def build_keyword_parameters_sql(keyword: str, count: int) -> list[str]:
        """
        retorna uma lista de parametros normalizados para LIKE,
        um para cada campo da cláusula construída
        """
        normalized = Normalizer.normalize_match_keyword_sql(keyword)
        return [normalized] * count
