import basedosdados as bd

def lista_municípios2():
    query = """
    SELECT *
    FROM basedosdados.br_ibge_populacao.municipio
    WHERE ano >= 2021
    """

    print('Baixando lista dos municípios do Brasil...')
    df = bd.read_sql(query, billing_project_id='basedosdados-317714')

    municípios = df['id_municipio'].unique()
    print('{} municípios baixados!'.format(len(municípios)))

    return municípios