import numpy as np

alpha = np.array([0.005, 0.2, 0.7, 1.25, 0.7, 1.5])


# расчет 1

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

