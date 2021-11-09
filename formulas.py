import numpy as np
import pandas as pd
import parser as par

alpha = np.array([0.005, 0.2, 0.7, 1.25, 0.7, 1.5])
q = 1.05

# t_f - текущий год, t_n - год последней диагностики (берутся с таблицы)
roadbed_type =
road_category =
road_climatic_zone =
zone =
# число полос
strip_count =
# фактический модуль упругости
E_fp = spreadsheet_not_numbered.iloc[hz, 6]
delta_t = t_f - t_n
spreadsheet_19 =

# запарсить средннее значение машин в сутки
def get_N_obsh(spreadsheet_19):
    car_data = np.zeros(6)
    car_data[0] = np.mean(np.array(spreadsheet_19.loc[:, 'Грузовые автомобили легкие']))
    car_data[1] = np.mean(np.array(spreadsheet_19.loc[:, 'Грузовые автомобили средние']))
    - np.mean(np.array(spreadsheet_19.loc[:, 4]))
    car_data[2] = -np.mean(np.array(spreadsheet_19.loc[:, 'Грузовые автомобили тяжелые']))
    + np.mean(np.array(spreadsheet_19.loc[:, 6]))
    car_data[3] = np.mean(np.array(spreadsheet_19.loc[:, 'Грузовые автомобили сверхтяжелые']))
    - np.mean(np.array(spreadsheet_19.loc[:, 8]))
    car_data[4] = np.mean(np.array(spreadsheet_19.loc[:, 'Автобусы']))
    car_data[5] = np.mean(np.array(spreadsheet_19.loc[:, 4])) + np.mean(np.array(spreadsheet_19.loc[:, 4]))
    + np.mean(np.array(spreadsheet_19.loc[:, 'Грузовые автомобили тяжелые']))
    return car_data


# запарсить массив среднего значения по типам
def get_N_j(spreadsheet_19):
    return np.mean(np.array(spreadsheet_19.loc[:, 11])) - np.mean(np.array(spreadsheet_19.loc[:, 10]))


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
    elif strip_count == 4 or a == 5:
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


def get_N_fp(N_obsh_n, strip_count, alpha, P):
    return N_obsh_n * get_f_n(strip_count) * np.sum(alpha * P)


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

K_H = get_T_0_K_H(roadbed_type, road_category, road_climatic_zone)[1]

def calculate_T_ost(q, roadbed_type, road_category, road_climatic_zone, strip_count, spreadsheet_19, alpha, delta_t, E_fp, K_H):
    omega = get_omega(roadbed_type, road_climatic_zone)
    gamma = get_gamma(roadbed_type)
    N_j = get_N_j(spreadsheet_19)
    N_obsh = get_N_obsh(spreadsheet_19)
    P = N_j / N_obsh
    N_fp = get_N_fp(N_obsh, strip_count, alpha, P)
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

calculate_T_ost(q, roadbed_type, road_category, road_climatic_zone, strip_count, spreadsheet_19, alpha, delta_t, E_fp, K_H)
#
#
#
# X_i
# E_i
# X
# T_ost
