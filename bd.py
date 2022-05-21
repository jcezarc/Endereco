import itertools
from parser import Endereco


def contatos_duplicados(cliente: int, limite: int, conexao) -> list:
        query = """
        select 
            c.endereco, c.id
        from 
            contatos c 
        where 
            c.cliente = '{}'
        order by 
            c.dt_atualizacao desc
        limit {}
        """.format(cliente, limite)
        return [
            a.id for a, b in itertools.combinations([
                Endereco(*db) for db in conexao.execute(query)],
                2
            ) if a == b
        ]


if __name__ == '__main__':
    from conexao import Conexao
    print(exluir_contatos_duplicados(
        Conexao(usuario='root', senha='123'),
        cliente=35, limite=10)
    )
