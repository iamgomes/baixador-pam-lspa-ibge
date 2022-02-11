import sidrapy
import pandas as pd
import time

# LAVOURAS ESTIMATIVAS table_code = 6588, classification = 48, 'Estimativas'

def baixa_estimativas(table_code, estados, classification, name_classification):

    nEst = 0
    nRowsTotal = 0
    tabela = []

    for est in estados:
        try:         
            api = sidrapy.get_table(table_code='{}'.format(table_code), territorial_level='3', ibge_territorial_code='{}'.format(est),
                                    period='last 2', classification='{}'.format(classification), categories='allxt', header='n')
            nEst += 1
            print('{} - {} - Estado de {}'.format(nEst, est, api['D1N'][0].upper()))
        except:
            print('Conexão recusada pelo servidor...')
            print('Aguardando por 5 segundos')
            print('ZZzzzz...')
            time.sleep(5)
            print('Ótimo, continuando...')
            continue

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
    api = api[api['D3N'].str[0:2] != '1 ']

    print('Higienizando dados...')
    api['V'] = api['V'].apply(lambda x: str(x).replace('...', '').replace('-', ''))
    api['V'] = pd.to_numeric(api['V'],downcast='signed')
    api['L'] = name_classification
    api['M'] = '9999999'
    # adaptando os códigos dos estados conforme os dados das exportações
    api['MAP'] = api['D1C'].map({'11':'11','12':'12','13':'13','14':'14','15':'15','16':'16','17':'17','21':'21','22':'22','23':'23',
                                '24':'24','25':'25','26':'26','27':'27','28':'31','29':'32','31':'33','32':'34','33':'36','35':'41',
                                '41':'42','42':'44','43':'45','51':'52','52':'53','53':'54','50':'55'})

    api['D3N'] = api['D3N'].map({'1.1 Algodão herbáceo':'Algodão herbáceo (em caroço)', 
                             '1.2 Amendoim (1ª Safra)':'Amendoim (em casca)',
                            '1.3 Amendoim (2ª Safra)':'Amendoim (em casca)',
                             '1.4 Arroz':'Arroz (em casca)',
                             '1.5 Aveia':'Aveia (em grão)',
                             '1.6 Centeio':'Centeio (em grão)',
                             '1.7 Cevada':'Cevada (em grão)',
                             '1.8 Feijão (1ª Safra)':'Feijão (em grão)',
                             '1.9 Feijão (2ª Safra)':'Feijão (em grão)',
                             '1.10 Feijão (3ª Safra)':'Feijão (em grão)',
                             '1.11 Girassol':'Girassol (em grão)',
                             '1.12 Mamona':'Mamona (baga)',
                             '1.13 Milho (1ª Safra)':'Milho (em grão)',
                             '1.14 Milho (2ª Safra)':'Milho (em grão)',
                             '1.15 Soja':'Soja (em grão)',
                             '1.16 Sorgo':'Sorgo (em grão)',
                             '1.17 Trigo':'Trigo (em grão)',
                             '1.18 Triticale':'Triticale (em grão)',
                             '2 Abacaxi':'Abacaxi',
                             '3 Alho':'Alho',
                             '4 Banana':'Banana (cacho)',
                             '5 Batata - inglesa (1ª Safra)':'Batata-inglesa',
                             '6 Batata - inglesa (2ª Safra)':'Batata-inglesa',
                             '7 Batata - inglesa (3ª Safra)':'Batata-inglesa',
                             '8 Cacau':'Cacau (em amêndoa)',
                             '9/10 Café total':'Café (em grão) Total',
                             '9 Café arábica':'Café (em grão) Arábica',
                             '10 Café canephora':'Café (em grão) Canephora',
                             '11 Cana-de-açúcar':'Cana-de-açúcar',
                             '12 Castanha-de-caju':'Castanha de caju',
                             '13 Cebola':'Cebola',
                             '14 Coco-da-baía':'Coco-da-baía',
                             '5 Fumo':'Fumo (em folha)',
                             '16 Guaraná':'Guaraná (semente)',
                             '17 Juta':'Juta (fibra)',
                             '18 Laranja':'Laranja',
                             '19 Maçã':'Maçã',
                             '20 Malva':'Malva (fibra)',
                             '21 Mandioca':'Mandioca',
                             '22 Pimenta-do-reino':'Pimenta-do-reino',
                             '23 Sisal ou agave':'Sisal ou agave (fibra)',
                             '24 Tomate':'Tomate',
                             '25 Uva':'Uva'                             
                            }
                           )

    print('Renomeando colunas...')
    df = api[['L','D2C','D1C','M','MAP','D3N','D4N','V']]
    df_final = pd.pivot_table(df,index=['L','D2C','D1C','M','MAP','D3N'],columns=['D4N'])
    df_temporaria = df_final.reset_index(col_level=1).rename(columns = {'L':'Lavoura','D2C':'Ano','D1C':'id_estado','M':'id_municipio',
                                                                        'MAP':'id_estado_new','D3N':'Produto'})
    level_one  = df_temporaria.columns.get_level_values(1)
    df_temporaria.columns = level_one

    print('Exportando DataFrame para arquivo CSV...')
    df_temporaria.to_csv('LSPA {}-{} Estados.csv'.format(table_code,name_classification), sep=';')

    print('Arquivo exportado com sucesso!\n')