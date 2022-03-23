import re


def separa_endereço(endereço: str) -> dict:
    """
    [1] --- O endereço será separado em dígitos e textos,
        logradouro e número são os dois primeiros elementos.

    [2] --- Se encontrar um elemento de 8 dígitos, é o CEP

    [3] --- Remove no texto anterior ao cep, a palavra 'CEP'

    [4] --- O complemento é o que resta, menos o excesso de espaços.
    """
    def extrai_cep(arr: list, i: int) -> str:
        if i:  # -------------------------------------------------- [3]
            palavras = re.split(r'(\W+)', arr[i-1])
            arr[i-1] = ' '.join(p for p in palavras if p != 'CEP')
        return arr.pop(i)
    logradouro, número, *arr = re.split(  # ----------------------- [1]
        r'(\d+)',
        re.sub('[-:]', '', endereço)
    )
    CEP = next(  # ------------------------------------------------ [2]
        (extrai_cep(arr, i)
        for i, c in enumerate(arr) 
        if i % 2 and len(c) == 8),
        ''
    )
    complemento = re.sub(' +', ' ', ' '.join(arr)).strip()  # ----- [4]
    return {
        'logradouro': logradouro,
        'número': número,
        'CEP': CEP,
        'complemento': complemento
    }


if __name__ == '__main__':
    resposta = separa_endereço(
        'Av. dos Turucutus, 666 - CEPÊRA bloco 25 fundos CEP: 12345-678 ap.171'
    )
    esperado = {
        'logradouro': 'Av. dos Turucutus, ',
        'número': '666',
        'CEP': '12345678',
        'complemento': 'CEPÊRA bloco 25 fundos ap. 171'
    }
    assert resposta == esperado
    print('*** Teste OK ***')
