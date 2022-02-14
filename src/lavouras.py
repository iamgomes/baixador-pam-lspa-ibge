import sidrapy
import pandas as pd
import time

# LAVOURAS PERMANENTES table_code = 1613, classification = 82, 'Permanentes'
# LAVOURAS TEMPORÁRIAS table_code = 1612, classification = 81, 'TEMPORÁRIAS'


def baixa_lavouras(table_code, municípios, anoInicio, anoFim, classification, name_classification):

    nMun = 0
    nRowsTotal = 0
    tabela = []
        
    for mun in municípios:
        try:
            api = sidrapy.get_table(table_code='{}'.format(table_code), territorial_level='6', ibge_territorial_code='{}'.format(mun), 
                                    period='{}-{}'.format(anoInicio,anoFim), classification='{}'.format(classification), categories='allxt', header='n')
            nMun += 1
            print('{} - {} - Município de {}'.format(nMun, mun, api['D1N'][0].upper()))
        except:
            print('Conexão recusada pelo servidor...')
            print('Aguardando por 5 segundos')
            print('ZZzzzz...')
            time.sleep(5)
            print('Ótimo, continuando...')
            continue

        nRows = 0
        for row in range(0,len(api)):
            dicionario = {'D2N':api['D2N'][row],'D1N':api['D1N'][row],'D1C':api['D1C'][row],'D3N':api['D3N'][row],
                        'D4N':api['D4N'][row],'V':api['V'][row]}

            nRows += 1
            nRowsTotal += 1

            tabela.append(dicionario)

        print('{} linhas\n'.format(nRows))
            
    anos = sorted(list(set([a['D2N'] for a in tabela])))
        
    print('{} Municípios e {} linhas baixadas no total\nAnos {}\nLavouras {}\n'.format(nMun,nRowsTotal,anos,name_classification))

    print('Convertendo tabela para DataFrame...\n')
    api = pd.DataFrame(data=tabela)

    print('Higienizando dados...')
    api['V'] = api['V'].apply(lambda x: str(x).replace('...', '').replace('-', ''))
    api['V'] = pd.to_numeric(api['V'], downcast='float')
    api['UF'] = api['D1N'].str[-3:-1]
    api['L'] = name_classification


    print('Renomeando colunas...')
    df = api[['L','D2N','UF','D1C','D3N','D4N','V']]
    df_final = pd.pivot_table(df,index=['L','D2N','UF','D1C','D3N'],columns=['D4N'])
    df_temporaria = df_final.reset_index(col_level=1).rename(columns = {'L':'Lavoura', 'D2N':'Ano', 'D1C':'id_municipio', 'D3N':'Produto'})
    level_one  = df_temporaria.columns.get_level_values(1)
    df_temporaria.columns = level_one

    print('Exportando DataFrame para arquivo CSV...')
    df_temporaria.to_csv('PAM {}-{} Municípios.csv'.format(table_code,name_classification), sep=';')

    print('Arquivo exportado com sucesso!\n')