from datetime import date
from src.lavouras import baixa_lavouras
from src.estimativas import baixa_estimativas
from src.api_municípios import lista_municípios
from src.estados import lista_estados

#https://apisidra.ibge.gov.br/home/ajuda

#Parâmetros paras as tabelas SIDRA
estados = lista_estados()
municípios = lista_municípios()

anoIncio = 2016
anoFim = date.today().year

anoMesInicio = 202101
anoMesFim = int(date.today().strftime("%Y%m"))

paramSidraPerm = 1613, 82, 'Permanentes'
paramSidraTemp = 1612, 81, 'Temporárias'
paramSidraEst = 6588, 48, 'Estimativas'


if __name__ == '__main__':
    print('---INICIANDO DOWNLOAD DOS ARQUIVOS---\n')

#    baixa_lavouras(paramSidraPerm[0], municípios, anoIncio, anoFim, paramSidraPerm[1], paramSidraPerm[2])
#    baixa_lavouras(paramSidraTemp[0], municípios, anoIncio, anoFim, paramSidraTemp[1], paramSidraTemp[2])
    baixa_estimativas(paramSidraEst[0], estados, anoMesInicio, anoMesFim, paramSidraEst[1], paramSidraEst[2])

    print('\n\o/ MARAVILHA \o/\nTodos os arquivos foram baixados com sucesso!\n')