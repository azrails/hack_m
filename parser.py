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
def road_parserType1(x):
    road = r"hack/Дорога "
    road += str(x)
    road += r"/1_Ведомость категории дорог.xlsx"

    df = pd.read_excel(r'{}'.format(road))
    return df

def road_parserType2(x):
    road = r"hack/Дорога "
    road += str(x)
    road += r"/2_Ведомость конструкции дорожной одежды.xlsx"

    df = pd.read_excel(r'{}'.format(road))
    return df

def road_parserType3(x):
    road = r"hack/Дорога "
    road += str(x)
    road += r"/5_Ведомость дорожно-климат районирования.xlsx"

    df = pd.read_excel(r'{}'.format(road))
    return df

def road_parserType4(x):
    road = r"hack/Дорога "
    road += str(x)
    road += r"/9_Ведомость общих данных по дороге.xlsx"

    df = pd.read_excel(r'{}'.format(road))
    return df

def road_parserType5(x):
    road = r"hack/Дорога "
    road += str(x)
    road += r"/11_Ведомость ширины проезжей части.xlsx"
    if x == 2:
        print('no fifth type in second road found')
    else:
        df = pd.read_excel(r'{}'.format(road))
        return df

def road_parserType6(x):
    road = r"hack/Дорога "
    road += str(x)
    road += r"/19 Ведомость среднегодовой интенсивности и состава движения.xlsx"

    df = pd.read_excel(r'{}'.format(road))
    return df

def road_parserType7(x):
    road = r"hack/Дорога "
    road += str(x)
    road += r"/Ведомость_ состояния покрытия и дорожной одежды.xlsx"

    df = pd.read_excel(r'{}'.format(road))
    return df
