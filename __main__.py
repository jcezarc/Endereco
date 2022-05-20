from parser import Endereco


def teste_compara_enderecos():
    end1 = Endereco(
        'Av. José Cândido Simões, 666 - bl 25 CEP: 12345-678 ap.14'
    )
    end2 = Endereco(
        'Avenida Zé Candido Simoes 666 apartamento 14 bloco 25'
    )
    assert end1 == end2
    print('*** Teste OK ***')


teste_compara_enderecos()
