from datetime import date
from src.lavouras import baixa_lavouras
from src.estimativas import baixa_estimativas
from src.municípios import lista_municípios
from src.estados import lista_estados
import logging

#https://apisidra.ibge.gov.br/home/ajuda

logging.basicConfig(
    filename = 'Log.log',
    level = logging.DEBUG,
    format = '%(asctime)s | %(levelno)s - %(levelname)s :: %(lineno)d | %(message)s')

#Parâmetros paras as tabelas SIDRA
estados = lista_estados()
municípios = lista_municípios()

anoInicio = 2016
anoFim = date.today().year

paramSidraPerm = 1613, 82, 'Permanentes'
paramSidraTemp = 1612, 81, 'Temporárias'
paramSidraEst = 6588, 48, 'Estimativas'


if __name__ == '__main__':
    logging.info('---INICIANDO DOWNLOAD DOS ARQUIVOS---')
    
    logging.info('---PERMANENTES---')
    baixa_lavouras(paramSidraPerm[0], municípios, anoInicio, anoFim, paramSidraPerm[1], paramSidraPerm[2])

    logging.info('---TEMPORÁRIAS---')
    baixa_lavouras(paramSidraTemp[0], municípios, anoInicio, anoFim, paramSidraTemp[1], paramSidraTemp[2])

    logging.info('---ESTIMATIVAS---')
    baixa_estimativas(paramSidraEst[0], estados, paramSidraEst[1], paramSidraEst[2])

    logging.info('---TODOS OS ARQUIVOS FORAM BAIXADOS.---')