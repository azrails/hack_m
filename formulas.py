import numpy as np

alpha = np.array([0.005, 0.2, 0.7, 1.25, 0.7, 1.5])

delta_t = t_f - t_n


def get_gamma(roadbed_type):
    if roadbed_type == 1:
        return 0.12
    elif roadbed_type == 2:
        return 0.148
    elif roadbed_type == 3:
        return 0.171
    else:
        print("error at formulas.get_gamma")


def get_T_0_K_H(roadbed_type, road_category, road_climatic_zone):
    T_0es = (((12, 12, 5), (12, 12, 5), (12, 12, 5), (12, 10, 5), (12, 10, 5)),
             ((14, 12, 5), (12, 12, 5), (12, 12, 5), (12, 10, 5), (12, 10, 5)),
             ((18, 12, 5), (15, 12, 5), (15, 12, 5), (12, 12, 5), (12, 12, 5)))
    K_Hes = (((0.98, 0.86, 0.82), (0.95, 0.86, 0.82), (0.92, 0.86, 0.82), (0.85, 0.85, 0.82), (0.85, 0.82, 0.65)),
             ((0.95, 0.85, 0.80), (0.92, 0.85, 0.80), (0.90, 0.85, 0.80), (0.84, 0.84, 0.80), (0.84, 0.80, 0.60)),
             ((0.88, 0.84, 0.77), (0.88, 0.84, 0.77), (0.85, 0.84, 0.77), (0.83, 0.82, 0.77), (0.83, 0.79, 0.58)))
    return T_0es[road_climatic_zone][road_category][roadbed_type], K_Hes[road_climatic_zone][road_category][roadbed_type]


# расчет 1

def f_n(a):
    r = 0.3
    if a == 1:
        r = 1
    elif a == 2:
        r = 0.55
    elif a == 3:
        r = 0.5
    elif a == 4 or a == 5:
        r = 0.35
    return r


def T_oct(q, X, gamma, omega, N_fp):
    return 1 / (np.log10(q)) * np.log10(10 ** X * (q - 1) / (gamma * omega * N_fp * q) + 1)


def X(E_i):
    return (E_i - 125) / 68 - 1


def E_i(E_fp, X_i, K_pr, K_reg, K_z, K_cu):
    return (E_fp * X_i) / (K_pr * K_reg * K_z * K_cu)


# T_ф_ост
def Formula_1_01(T_ost, delta_t):
    return T_ost - delta_t


# K_z
def Formula_1_04(N):
    if N >= 1000:
        return 0.0000175 * N + 0.98
    elif N > 0:
        return 0.98 - 6.9 / N
    else:
        return 0.98 - 6.9


# N
def Formula_1_05(N_fp, q, delta_t):
    return N_fp * q ** delta_t


# N_fp
def Formula_1_08(N_obsh_n, f_n, alpha, P):
    return N_obsh_n * f_n * np.sum(alpha * P)


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
