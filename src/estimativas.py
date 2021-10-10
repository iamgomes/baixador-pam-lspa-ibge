import sidrapy
import pandas as pd

# LAVOURAS ESTIMATIVAS table_code = 6588, classification = 48, 'Estimativas'

def baixa_estimativas(table_code, estados, anoMesInicio, anoMesFim, classification, name_classification):

    nEst = 0
    nRowsTotal = 0
    tabela = []

    for est in estados:
        
        nEst += 1
        
        api = sidrapy.get_table(table_code='{}'.format(table_code), territorial_level='3', ibge_territorial_code='{}'.format(est),
                                period='{}-{}'.format(anoMesInicio, anoMesFim), classification='48', categories='allxt', header='n')
        
        print('{} - {} - Estado de {}'.format(nEst, est, api['D1N'][0].upper()))

        nRows = 0
        for row in range(0,len(api)):
            dicionario = {'D2C':api['D2C'][row],'D1N':api['D1N'][row],'D1C':api['D1C'][row],'D3N':api['D3N'][row],
                        'D4N':api['D4N'][row],'V':api['V'][row]}

            nRows += 1
            nRowsTotal += 1

            tabela.append(dicionario)

        print('{} linhas\n'.format(nRows))
            
    anos = sorted(list(set([a['D2C'] for a in tabela])))
            
    print('{} Estados e {} linhas baixadas no total\nAnos {}\nLavouras de {}\n'.format(nEst, nRowsTotal, anos, name_classification))

    print('Convertendo tabela para DataFrame...\n')
    api = pd.DataFrame(data=tabela)

    print('Higienizando dados...')
    api['V'] = api['V'].apply(lambda x: str(x).replace('...', '').replace('-', ''))
    api['V'] = pd.to_numeric(api['V'])
    api['L'] = name_classification
    api['M'] = '9999999'

    print('Renomeando colunas...')
    df = api[['L','D2C','D1C','M','D3N','D4N','V']]
    df_final = pd.pivot_table(df,index=['L','D2C','D1C','M','D3N'],columns=['D4N'])
    df_temporaria = df_final.reset_index(col_level=1).rename(columns = {'L':'Lavoura','D2C':'Ano','D1C':'id_estado','M':'id_municipio','D3N':'Produto'})
    level_one  = df_temporaria.columns.get_level_values(1)
    df_temporaria.columns = level_one

    print('Exportando DataFrame para arquivo CSV...')
    df_temporaria.to_csv('LSPA {}-{} Estados.csv'.format(table_code,name_classification), sep=';')

    print('Arquivo exportado com sucesso!\n')