import OpenOPC
import datetime
import time
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
import shutil
from wellmodel import calc_debit_total, V_crack_prop_port, alpha_crack_recover

MIN_PAUSE_SEC = 0.01
MAX_PAUSE_SEC = 1

read_params = ['O4W-0_port{0}_Pos.PT'.format(i + 1) for i in range(3)]
V_CRACK_INITIAL = V_crack_prop_port * alpha_crack_recover
PORTS_COUNT = 3
PORTS_PROD = [0.65, 0.3, 0.05]  # продуктивность по портам в долях
A_IPR_TOTAL = 3.64e13

copy_files = False
input_dir = r'D:\Ansys_Projects\olga\10005\gaslift\gaslift_python_1'
out_dir = r'D:\Ansys_Projects\olga\10005\gaslift\gaslift_python_1\res'
varnum = 1


def server_connect():
    opc = OpenOPC.client()
    servers = opc.servers()
    opc.connect(servers[0])
    return opc


def calc_timestep(olgaserver, modelname='modulename.modelname.', timestep=10):
    """
    Функция для расчета одного timestep, задаваемого пользователем (оно не равно количеству итераций внутри самой Ольги)

    :param olgaserver: текущий сервер модели
    :param modelname: название модели в виде: имя_модуля.имя_модели.
    :param timestep: длительность пользовательской итерации симуляции
    :return: none
    """

    # Здесь кусочек кода, который показать не могу

    # если разность между заданным временем симуляции и текущим временем симуляции <= 0, то симуляции успешно прошла
    # и можем задавать новое время симуляции
    if delta_time.total_seconds() <= 0:
        pass
    else:
        # в противном случае нам надо подождать, пока симуляция пройдет
        simulation = True
        while simulation:
            sim_time_olga_str = olgaserver.read(modelname + 'SIMTIME', include_error=True)[0].split('+')[0].split('.')[0]
            sim_time_olga = datetime.datetime.strptime(sim_time_olga_str, '%Y-%m-%d %H:%M:%S')
            delta_time = external_time_olga - sim_time_olga
            if delta_time.total_seconds() <= 0:
                break

            # Кусочек кода для настройки обращения к OLGA


def calc_model(olgaserver, modelname='gaslift.gaslift.', modeling_time: float = 24, timestepdict={'0': 10, '3600': 60},
               timestep_initial=1):
    """
    Расчет модели на заданное время

    :param olgaserver: текущий сервер модели
    :param modelname: название модели в виде: имя_модуля.имя_модели.
    :param modeling_time: время моделирования, ч
    :param timestepdict: словарь временных шагов, в качестве ключей значения времени, когда timestep меняется
    :param timestep_initial: начальное значение внешнего шага моделирования
    :return: none
    """
    # ========== Инициализация модели ==========
    Qwaccum_0 = [0] * PORTS_COUNT
    Qgaccum_0 = [0] * PORTS_COUNT
    Vwat_crack_lost = [V_CRACK_INITIAL] * PORTS_COUNT
    omega = [1] * PORTS_COUNT
    massflow = [0] * PORTS_COUNT
    G_crack = [0]
    k_water = [1]
    timevector = [0]
    # ==========
    simtime = 0
    finaltime = modeling_time * 3600
    timestamps = [float(current_t) for current_t in timestepdict.keys()]
    timestamp_value = [int(current_dt) for current_dt in timestepdict.values()]
    timestamp_count = len(timestamps)
    timestep = timestep_initial
    i = 0
    crack_empty = True
    crack_empty_time = 0
    while simtime <= finaltime:
        if i < timestamp_count:
            if simtime >= timestamps[i]:
                timestep = timestamp_value[i]
                i += 1
        # ========== Задание расчетных параметров моделей в этом куске кода ==========
       # Кусочек кода


def modify_model(olgaserver, modelname='modulename.modelname.', modify_params=dict()):
    """
    Функция модификации параметров модели

    :param olgaserver: текущий сервер модели
    :param modelname: название модели в виде: имя_модуля.имя_модели.
    :param modify_params: словарь параметров, которые надо менять на текущий момент
    :return: none
    """
    if len(modify_params) > 0:
        for current_param in modify_params.keys():
            olgaserver.write((modelname + current_param, modify_params[current_param]), include_error=True)


def read_model(olgaserver, modelname='modulename.modelname.', read_params=[]):
    """
    Функция чтения параметров модели

    :param olgaserver: текущий сервер модели
    :param modelname: название модели в виде: имя_модуля.имя_модели.
    :param read_params: словарь параметров, которые нужно считать
    :return: словарь значений считанных параметров
    """
    out_data = dict()
    if len(read_params) > 0:
        for current_param in read_params:
            out_data[current_param] = olgaserver.read(modelname + current_param, include_error=True)[0]
    return out_data


# Кусочек кода

olgaserver = server_connect()
timestart = time.time()
G_vector, k_vector, t_vector, t_crack_work = calc_model(olgaserver=olgaserver, modelname='gaslift.gaslift.', modeling_time=16, timestep_initial=5, timestepdict={'0': 5, '3600': 10, '87000': 300})
timefinal = time.time()
print('Время работы трещины = {0} с'.format(t_crack_work))
#data = pd.DataFrame([t_vector, G_vector, k_vector], columns=['t, ч', 'Qтрещины, м3/сут', 'k'])
#data.to_excel(r'D:\Ansys_Projects\olga\10005\gaslift\приток_трещина.xlsx')
#plt.plot(np.array(t_vector) / 3600, np.array(G_vector) / 1000 * 86400)
#plt.xlabel('t, ч')
#plt.ylabel('Gтр, м3/сут')
#plt.show()
#calc_timestep(olgaserver=olgaserver, modelname='flowline.flowline.')
                filename, filetype = filename.split('.')
                os.rename(out_dir + '\\' + 'var_{0}\\'.format(varnum) + current_file.split('\\')[-1],
                          out_dir + '\\' + 'var_{0}\\var_{0}.'.format(varnum) + filetype)


olgaserver = server_connect()
timestart = time.time()
G_vector, k_vector, t_vector, t_crack_work = calc_model(olgaserver=
