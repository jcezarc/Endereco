import itertools
from parser import Endereco


def exluir_contatos_duplicados(cliente: int, limite: int, conexao) -> str:
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
        duplicados = [
            a.id for a, b in itertools.combinations([
                Endereco(*db) for db in conexao.execute(query)],
                2
            ) if a == b
        ]
        return 'DELETE FROM contatos WHERE id in ({})'.format(
            ','.join(duplicados)
        )


if __name__ == '__main__':
    from conexao import Conexao
    print(exluir_contatos_duplicados(
        Conexao(usuario='root', senha='123'),
        cliente=35, limite=10)
    )
