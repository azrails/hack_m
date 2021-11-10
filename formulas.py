import numpy as np
import pandas as pd
import parser as par
import datetime

alpha = np.array([0.005, 0.2, 0.7, 1.25, 0.7, 1.5])
q = 1.05


def segmenter(segs, lens, points, data, write):
    counts = 0
    for i in range(len(segs)):
        if points[counts] - segs[i] <= lens[i]:
            write[i] = data[counts]
        else:
            counts += 1
            write[i] = data[counts]

def get_data(df1, df2, df5, df9, df11, df19, df_not_numbered):
    alpha = np.array([0.005, 0.2, 0.7, 1.25, 0.7, 1.5])
    _t_p = int(df9.iloc[0, 9])
    _t_f = int(datetime.datetime.now().year)
    lens = np.array(len(df1), len(df2), len(df5), len(df9), len(df11), len(df19), len(df_not_numbered))
    names = ("df1", "df2", "df5", "df9", "df11", "df19", "df_not_numbered")
    string1 = names[np.argmax(lens)] + ".iloc[:, 0:3].to_numpy()"
    segments_with_meters = eval(string1)
    # в segments хранятся 0 - начало участка в км 1 - длина в км 2 - road category 3 - strip_count
    # 4 - climatic zore 5 - roadbed 6 - E_fp 7 -  alpha_prod_P 8 - N_obsh
    # FIXME какой индекс в np.shape дает количество строк в таблице
    segments = np.zeros((np.shape(segments_with_meters)[kakoyto], 8))
    segments[0] = segments_with_meters[0]+segments_with_meters[1]*0.001
    segments[1] = -segments[0] + segments_with_meters[2]+segments_with_meters[3]*0.001-segments[0]

    category = df1.iloc[:, 4].to_numpy()
    strips = df1.iloc[:, 6].to_numpy()
    df1_points = df1.iloc[:, 0].to_numpy() + df1.iloc[:, 1].to_numpy()*0.001
    segmenter(segments[0], segments[1], df1_points, category, segments[2])
    segmenter(segments[0], segments[1], df1_points, strips, segments[3])

    climatic_zone = df5.iloc[:, 4].to_numpy()
    df5_points = df5.iloc[:, 0].to_numpy() + df5.iloc[:, 1].to_numpy() * 0.001
    segmenter(segments[0], segments[1], df5_points, climatic_zone, segments[4])

    roadbed = df_not_numbered.iloc[:, 4].to_numpy()
    E_modula = df_not_numbered.iloc[:, 6].to_numpy()
    df_not_numbered_points = df_not_numbered.iloc[:, 0].to_numpy() + df_not_numbered.iloc[:, 1].to_numpy()*0.001
    segmenter(segments[0], segments[1], df_not_numbered_points, roadbed, segments[5])
    segmenter(segments[0], segments[1], df_not_numbered_points, E_modula, segments[6])

    df19_points = df19.iloc[:, 0].to_numpy() + df19.iloc[:, 1].to_numpy() * 0.001
    A_P_P, obsh = get_alpha_prod_P(df19, alpha)
    segmenter(segments[0], segments[1], df19_points, A_P_P, segments[7])
    segmenter(segments[0], segments[1], df19_points, obsh, segments[8])
    return segments, _t_f, _t_p


def get_alpha_prod_P(df_19, alph):
    car_data = []
    car_data.append(df_19.loc[:, 'Грузовые автомобили легкие'].to_numpy())
    car_data.append(df_19.loc[:, 'Грузовые автомобили средние'].to_numpy() - df_19.loc[:, 4].to_numpy())
    car_data.append(-df_19.loc[:, 'Грузовые автомобили тяжелые'].to_numpy() + df_19.loc[:, 6].to_numpy())
    car_data.append(df_19.loc[:, 'Грузовые автомобили сверхтяжелые'] - df_19.loc[:, 8].to_numpy())
    car_data.append(df_19.loc[:, 'Автобусы'].to_numpy())
    car_data.append(df_19.loc[:, 4].to_numpy() + df_19.loc[:, 8].to_numpy() + df_19.loc[:, 'Грузовые автомобили тяжелые'].to_numpy())
    car_data_array = np.array(car_data)
    car_N_j = df_19.loc[:, 11] - df_19.loc[:, 10]
    P = np.array(0, 0, 0, 0, 0, 0)
    aplha_prod_P = np.zeros(len(P[0]))
    for i in range(6):
        P[i] = np.divide(car_data_array[i], car_N_j)
    for i in range(len(P[0])):
        aplha_prod_P[i] = np.sum(P[:, i], alph)
    return aplha_prod_P, car_N_j


def get_gamma(roadbed_type):
    if roadbed_type == 1:
        return 0.12
    elif roadbed_type == 2:
        return 0.148
    elif roadbed_type == 3:
        return 0.171
    else:
        print("error at formulas.get_gamma")


def get_omega(roadbed_type, road_climatic_zone):
    omegas = ((1.3, 1.39, 1.00), (1.14, 1.17, 1.00), (1.00, 1.00, 1.00), (0.89, 0.86, 1.00), (0.79, 0.74, 1.00))
    return omegas[road_climatic_zone][roadbed_type]


def get_T_0_K_H(roadbed_type, road_category, road_climatic_zone):
    T_0es = (((12, 12, 5), (12, 12, 5), (12, 12, 5), (12, 10, 5), (12, 10, 5)),
             ((14, 12, 5), (12, 12, 5), (12, 12, 5), (12, 10, 5), (12, 10, 5)),
             ((18, 12, 5), (15, 12, 5), (15, 12, 5), (12, 12, 5), (12, 12, 5)))
    K_Hes = (((0.98, 0.86, 0.82), (0.95, 0.86, 0.82), (0.92, 0.86, 0.82), (0.85, 0.85, 0.82), (0.85, 0.82, 0.65)),
             ((0.95, 0.85, 0.80), (0.92, 0.85, 0.80), (0.90, 0.85, 0.80), (0.84, 0.84, 0.80), (0.84, 0.80, 0.60)),
             ((0.88, 0.84, 0.77), (0.88, 0.84, 0.77), (0.85, 0.84, 0.77), (0.83, 0.82, 0.77), (0.83, 0.79, 0.58)))
    return T_0es[road_climatic_zone][road_category][roadbed_type], K_Hes[road_climatic_zone][road_category][
        roadbed_type]


def get_K_cu(roadbed_type, road_climatic_zone):
    keys = ((1.54, 1.42, 1.35), (1.38, 1.34, 1.28), (1.0, 1.0, 1.0))
    return keys[roadbed_type][road_climatic_zone]


def get_K_pr(road_category, roadbed_type):
    if roadbed_type == 1:
        if road_category < 3:
            return 1.00
        else:
            return 0.94
    else:
        return 0.77


def get_K_reg(road_climatic_zone):
    if road_climatic_zone == 5:
        return 0.85
    else:
        return 1.00


# расчет 1

def get_f_n(strip_count):
    r = 0.3
    if strip_count == 1:
        r = 1
    elif strip_count == 2:
        r = 0.55
    elif strip_count == 3:
        r = 0.5
    elif strip_count == 4 or strip_count == 5:
        r = 0.35
    return r


def get_T_ost(q, X, gamma, omega, N_fp):
    return 1 / (np.log10(q)) * np.log10(10 ** X * (q - 1) / (gamma * omega * N_fp * q) + 1)


def get_X_i(K_H):
    0.96 / (1 - K_H) ** 0.128


def get_X(E_i):
    return (E_i - 125) / 68 - 1


def get_E_i(E_fp, X_i, K_pr, K_reg, K_z, K_cu):
    return (E_fp * X_i) / (K_pr * K_reg * K_z * K_cu)


# T_ф_ост
def get_remaining_time(T_ost, delta_t):
    return T_ost - delta_t


def get_K_z(N):
    if N >= 1000:
        return 0.0000175 * N + 0.98
    elif N > 0:
        return 0.98 - 6.9 / N
    else:
        return 0.98 - 6.9


def get_N(N_fp, q, delta_t):
    return N_fp * q ** delta_t


def get_N_fp(N_obsh_n, strip_count, alpha_pr_P):
    return N_obsh_n * get_f_n(strip_count) * alpha_pr_P


# Ебейшая формула из большой таблицы
def Giga_Formula(T_ost, delta_t, K_pr, K_reg, K_z, K_cu, X_i, gamma, omega, N_fp, q, delta_KP, T_0):
    E_cp = 125 + 68 * np.log10(((gamma * omega * N_fp * q ** delta_t * q ** T_0 - 1) / (q - 1)) - 1)
    if T_ost < delta_t:
        E_f = 108.7 * K_pr * K_reg * K_z * K_cu
        E_tr = (E_cp * K_pr * K_reg * K_z * K_cu) / X_i
    else:
        E_i = 125 + 68 * (np.log10((gamma * omega * N_fp * q * q ** T_0 - q ** delta_t) / (q - 1)) - 1)
        E_f = (E_i * K_pr * K_reg * K_z * K_cu) / X_i
        if delta_KP > T_0:
            E_tr = (E_cp * K_pr * K_reg * K_z * K_cu) / X_i
        else:
            E_tr = (E_i * K_pr * K_reg * K_z * K_cu) / X_i

    return E_f, E_tr



def calculate_T_ost(roadbed_type, road_category, road_climatic_zone, strip_count, alpha_product_P, delta_t, E_fp, N_obsh):
    K_H = get_T_0_K_H(roadbed_type, road_category, road_climatic_zone)[1]
    q = 1.05
    omega = get_omega(roadbed_type, road_climatic_zone)
    gamma = get_gamma(roadbed_type)
    N_fp = get_N_fp(N_obsh, strip_count, alpha_product_P)
    N = get_N(N_fp, q, delta_t)
    K_pr = get_K_pr(road_category, roadbed_type)
    K_cu = get_K_cu(roadbed_type, road_climatic_zone)
    K_reg = get_K_reg(road_climatic_zone)
    K_z = get_K_z(N)
    X_i = get_X_i(K_H)
    E_i = get_E_i(E_fp, X_i, K_pr, K_reg, K_z, K_cu)
    X = get_X(E_i)
    T_ost = get_T_ost(q, X, gamma, omega, N_fp)
    result = get_remaining_time(T_ost, delta_t)


