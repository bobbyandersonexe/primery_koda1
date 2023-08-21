import matplotlib.pyplot as plt
import math
#import numpy as np
from scipy.optimize import fsolve

# константы
RHO_PROP = ***  # плотность проппанта
PHI_CRACK = ***  # эффективная пористость трещины 0,3
MU_WATER = ***  # вязкость воды, сП
PROP_LOST_COEFF = ***  # доля проппанта, который остается в трещине
OUT_WAT_ROCK_BASEMODEL = ***  # количество выносимой воды из пласта по базовой модели (группа А. В. Жонина)
A_BASE = ***  # коэффициент базовой модели
B_BASE = ***  # коэффициент базовой модели

# параметры, связанные с водой
V_port = ***  # суммарное количество воды, выносимое из порта
alpha_crack_recover = ***  # коэффициент выноса воды трещины

#  параметры пласт/трещина
k_rock = ***  # проницаемость пласта, мД
Fcd = ***  # безразмерная проводимость трещины
w_crack_ave = ***  # средняя ширина трещины
h_crack = ***  # высота трещины
n_crack = ***  # количество трещин
l_crack = ***  # полудлина трещины
m_prop = ***  # масса закачанного проппанта, кг

#  расчетные величины
V_crack_prop = m_prop / RHO_PROP / (1 - PHI_CRACK) * PHI_CRACK * PROP_LOST_COEFF  # суммарный объем воды во всех трещинах
V_crack_prop_port = V_crack_prop / n_crack  # объем воды в трещине на 1 порт
w_crack_prop = V_crack_prop / PHI_CRACK / h_crack / l_crack / 2 / n_crack  # ширина трещины по проппанту
k_crack = Fcd * l_crack / w_crack_prop * k_rock
V_rock = V_port - V_crack_prop_port * alpha_crack_recover  # количество воды, которое будет выноситься из пласта
k_wat_rock = V_rock / OUT_WAT_ROCK_BASEMODEL  # масштабный коэффициент модели воды из пласта на текущие параметры


def calc_filter_vel(delta_p: float = 30):
    """
    Расчет фильтрационной скорости для трещины по воде

    :param delta_p: средний перепад давлений, атм
    :return: фильтрационная скорость, м/с
    """
    if delta_p < 0:
        delta_p = 0
    return delta_p / l_crack * k_crack * 0.001 / MU_WATER * 0.01


def calc_water_flow_crack(w_filter: float = 1.0, w_crack: float = w_crack_prop, dwell: float = 0.15):
    """
    Расчет объемного расхода воды из трещины

    :param w_filter: фильтрационная скорость воды, м/с
    :param w_crack: ширина трещины, м
    :param dwell: диаметр горизонтального участка, м
    :return: объемный расход, м^3/с
    """
    return w_filter * 3.14159 * dwell * w_crack


def calc_accum_water_rock(Qgas_accum: float):
    """
    Расчет накопленного выноса воды из пласта по одному порту по модели ТРиЗ

    :param Qgas_accum: накопленный вынос газа, тыс. м^3
    :return: накопленный вынос воды на 1 порт, м^3
    """
    return k_wat_rock * A_BASE * Qgas_accum / (B_BASE + Qgas_accum)


def calc_debit_qudratic_IPR(pres: float = 112, pbot: float = 80, A_IPR: float = 3.64e13):
    """
    Расчет дебита по квадратичной зависимости

    :param pres: давление резервуара (пласта), атм
    :param pbot: давление забоя, атм
    :param A_IPR: коэффициент фильтрационного сопротивления, Па^2/(кг/с)
    :return: массовый расход газа, кг/с
    """
    G_IPR = (pres * pres - pbot * pbot) * 101325 * 101325 / A_IPR
    if G_IPR < 0:
        G_IPR = 0
    return G_IPR


def calc_debit_with_water_IPR(Qwaccum_0: float = 0, Qgaccum_0: float = 0, dt: float = 1,
                              pres: float = 112, pbot: float = 80, A_IPR: float = 3.64e13):
    """
    Расчет выноса воды и газа из пласта с учетом интегральной зависимости

    :param Qwaccum_0: накопленный вынос воды на момент времени t, м^3
    :param Qgaccum_0: накопленный вынос газа на момент времени t, тыс. м^3
    :param dt: шаг по времени, с
    :param pres: давление резервуара (пласта), атм
    :param pbot: давление забоя, атм
    :param A_IPR: коэффициент фильтрационного сопротивления, Па^2/(кг/с)
    :return: суммарный расход, кг/с; расход воды, кг/с; расход газа, кг/с; доля воды
    """
    G_total = calc_debit_qudratic_IPR(pres=pres, pbot=pbot, A_IPR=A_IPR)
    omega = fsolve(lambda x: calc_accum_water_rock(Qgaccum_0 + dt * G_total * (1 - x) / 0.7 / 1000) - Qwaccum_0 - dt * G_total * x / 1000, 0.0)[0]
    if omega > 1:
        omega = 1
    if omega < 0:
        omega = 0
    return G_total, G_total * omega, G_total * (1 - omega), omega

# И так далее
