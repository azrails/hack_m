import numpy
import pandas as pd


#существует 7 разных типов экселей и 10 дорог, называются по типу road_parcerType3(1) для третьего типа первой дороги:

# Категории дорог
# Кострукции дорожной одежды
# Дорожно-районный климат районирования
# Общие данные по дороге
# Ширина проезжей части
# Среднегодовая интенсивность
# Состояние покрытия и дорожной одежды

def main_parser(directoryname: str)->'dict[pd.dataframe]':
    datasets = {}
    for i in range(7):
        datasets[f'dataset{i + 1}'] = (eval(f'road_parserType{i + 1}(directoryname)'))
    return datasets
    

def road_parserType1(road):
    road += r"/1_Ведомость категории дорог.xlsx"
    df = pd.read_excel(r'{}'.format(road))
    return df

def road_parserType2(road):
    road += r"/2_Ведомость конструкции дорожной одежды.xlsx"

    df = pd.read_excel(r'{}'.format(road))
    return df

def road_parserType3(road):
    road += r"/5_Ведомость дорожно-климат районирования.xlsx"

    df = pd.read_excel(r'{}'.format(road))
    return df

def road_parserType4(road):
    road += r"/9_Ведомость общих данных по дороге.xlsx"

    df = pd.read_excel(r'{}'.format(road))
    return df

def road_parserType5(road):
    road += r"/11_Ведомость ширины проезжей части.xlsx"
    if x == 2:
        print('no fifth type in second road found')
    else:
        df = pd.read_excel(r'{}'.format(road))
        return df

def road_parserType6(road):
    road += r"/19_Ведомость среднегодовой интенсивности и состава движения.xlsx"

    df = pd.read_excel(r'{}'.format(road))
    return df

def road_parserType7(road):
    road += r"/Ведомость_ состояния покрытия и дорожной одежды.xlsx"

    df = pd.read_excel(r'{}'.format(road))
    return df
