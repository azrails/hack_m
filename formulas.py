import numpy as np

alpha = np.array([0.005, 0.2, 0.7, 1.25, 0.7, 1.5])


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
def Formula_1_01(T_ost, t_f, t_n):
    return T_ost - t_f + t_n


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
def Giga_Formula(T_ost, delta_t, K_pr, K_reg, K_z, K_cu, X_i, gamma, omega, N_fp, q, delta_KP):
    E_cp = 125 + 68 * np.log10(((gamma * omega * N_fp * q ** delta_t * q ** T_ost - 1) / (q - 1)) - 1)
    if T_ost < delta_t:
        E_f = 108.7*K_pr*K_reg*K_z*K_cu
        E_tr = (E_cp * K_pr * K_reg * K_z * K_cu)/X_i
    else:
        E_i = 125 + 68*(np.log10((gamma * omega * N_fp * q * q**T_ost - q**delta_t)/(q - 1)) - 1)
        E_f = (E_i * K_pr * K_reg * K_z * K_cu)/X_i
        if delta_KP > T_ost:
            E_tr = (E_cp * K_pr * K_reg * K_z * K_cu)/X_i
        else:
            E_tr = (E_i * K_pr * K_reg * K_z * K_cu)/X_i

    return E_f, E_tr