import re
import json
from unicodedata import normalize
from difflib import SequenceMatcher


class Endereco:
    abreviacoes = {}

    def __init__(self, texto: str):        
        def extrai_cep(arr: list, i: int) -> str:
            if i:
                palavras = re.split(r'(\W+)', arr[i-1])
                arr[i-1] = ' '.join(p for p in palavras if p != 'CEP')
            return arr.pop(i)
        logradouro, self.numero, *arr = re.split(
            r'(\d+)',
            re.sub('[-:,\.]', '', self.remove_acentos(texto))
        )
        self.CEP = next(
            (extrai_cep(arr, i)
            for i, c in enumerate(arr) 
            if i % 2 and len(c) == 8),
            ''
        )
        complemento = ' '.join(a for a in arr if a.strip())
        self.logradouro = self.substitui_abrev(logradouro)
        self.complemento = self.substitui_abrev(complemento)

    @classmethod
    def substitui_abrev(cls, texto: str) -> str:
        if not cls.abreviacoes:
            with open('abrev.json', 'r') as f:
                cls.abreviacoes = json.load(f)
        palavras = [cls.abreviacoes.get(t.upper(), t)
            for t in texto.split() if t.strip()]
        return ' '.join(palavras)

    @staticmethod
    def remove_acentos(texto: str) -> str:
        return normalize('NFD', texto).encode('ascii', 'ignore').decode('utf-8')

    def resumo(self):
        palavras = self.logradouro.split() + self.complemento.split()
        return ' '.join(p for p in sorted(palavras))

    def __eq__(self, outro):
        if self.numero != outro.numero:
            return False
        txt1, txt2 = [e.resumo() for e in [self, outro]]
        return SequenceMatcher(None, txt1, txt2).ratio() > 0.66
