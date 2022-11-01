import pandas as pd
import matplotlib.pyplot as plt
from decimal import *
import datetime
import math
import numpy as np
from multipledispatch import dispatch

def Get_Indexes(file_name):

    kni_ind = []
    tout_ind = []
    read = False
    with open(file_name, encoding='utf-8') as file:
        lines = file.readlines()

    for line in lines:
        if line.find('# NTvs$pos_name') != -1:
            read = True
            continue

        if read == True:
            line = line.replace('\t', ' ')
            space_index = line.find(' ')
            if int(line[space_index:]) != 0:
                kni_ind.append(int(line[space_index:]))
                tout_ind.append(int(line[:space_index]))
    sort_ind = pd.DataFrame(tout_ind)
    sort_ind.loc[:,1] = kni_ind
    return sort_ind

# Устанавливается трубка сходимости для значений температуры
def Check(data_row):
    i = 0

    for val in data_row:

        if val > 35:
            if i == 0:
                data_row[i] = 0
            else:
                data_row[i] = data_row[i-1]

        if val < -35:
            if i == 0:
                data_row[i] = 0
            else:
                data_row[i] = data_row[i - 1]
        i += 1

    return data_row

# Вычисление разности температур Tout и TPkni_out_A/B
@dispatch(list,list,list,pd.DataFrame)
def DataDifference(data1,data_tout,time1,sort_ind):
    diff_data = []
    diff_time = time1
    diff_counter = -1
    diff_time = time1

    for i in range(len(data_tout)):
        diff_data.append([])
        diff_data_buff1 = []
        for j in range(len(sort_ind)):
            diff_data_buff1.append(data_tout[i][sort_ind[0][j]-1]-data1[i][sort_ind[1][j]-1])

        diff_data_buff2 = Check(diff_data_buff1)

        for k in range(len(data1[0])):
            diff_data[i].append(diff_data_buff2[k])

    return diff_data, diff_time

# Вычисление разности температур других файлов
@dispatch(list,list,list)
def DataDifference(data1,data2,time1):
    diff_data = []
    diff_time = []
    diff_counter = 0
    diff_time = time1

    for i in range(len(data1)):

        diff_data_buff1 = []
        diff_data.append([])

        for j in range(len(data1[0])):
            diff_data_buff1.append(data2[i][j]-data1[i][j])

        diff_data_buff2 = Check(diff_data_buff1)

        for k in range(len(data1[0])):
            diff_data[i].append(diff_data_buff2[k])
            # diff_data[i].append(diff_data_buff1[k])

        diff_counter += 1

    return diff_data, diff_time

# Считывание значений температур из переменной "line",
# которая хранит в себе текст из файла:print(diff_data)
def GetDataFromFile(line):
    num = 0
    line = line.replace('\t', ' ')
    line = line.replace(' ', '', 1)

    while line[num:]:
        if line[num] == ' ':
            num += 1
            line = line[num:]
            break
        num += 1

    line_data = line

    return line_data

# Считывание значений даты и времени из переменной
# "line", которая хранит в себе текст из файла
def GetTimeFromFile(line):
    point = 13
    line_time = ''
    line_time = line[point:]

    year = int(line_time[:4])
    line_time = line_time[5:]

    month = int(line_time[:2])
    line_time = line_time[3:]

    day = int(line_time[:2])
    line_time = line_time[3:]

    hour = int(line_time[:2])
    line_time = line_time[3:]

    minute = int(line_time[:2])
    line_time = line_time[3:]

    second = int(line_time[:2])

    date_and_time = datetime.datetime(year,month,day,hour,minute,second)

    return date_and_time

# Функция парсинга, в которой контролируется правильное
# считывание данных из файлов
def ParserFunction(file_name):
    data = []
    time = []
    sort_list = []
    data_i = data_j = -1
    time_buff = data_buff = ''
    reading = False
    null_str = False
    check = False
    count = 0

    with open(file_name, encoding='utf-8') as file:
        lines_file = file.readlines()

    for line in lines_file:
        if null_str == False and line == '\n':
            null_str = True
            continue

        sort_list.append(line)

        if line == '\n':
            reading = False
            continue

        if line.find("# Timepoint: ") != -1:
            time_buff = GetTimeFromFile(line)

        if line.find('# Param:') != -1:
            reading = True
            count = 0
            continue

        if reading == True:
            check = True
            if check == True and count == 0:
                data.append([])
                data_i += 1
                time.append(time_buff)
                check = False
                count = 1

            data_buff = Decimal(GetDataFromFile(line))
            data[data_i].append(data_buff)

    return data, time

# Функция, в которой реализована работа данных с библиотекой
# "pandas", а также последующее выведение этих данных на график
def PandasWork():
    Tout = 'Tout.txt'
    TPkni_out_A = 'TPkni_out_A.txt'
    TPkni_out_B = 'TPkni_out_B.txt'
    TPkni_in = 'TPkni_in.txt'
    TPkni_oo = 'TPkni_oo.txt'
    NKni_TW = 'NKni_TW.txt'
    NKni_TW_Ntp = 'NKni_TW_Ntp.txt'

    sort_indexes = Get_Indexes(NKni_TW)

    data_Tout, time_Tout = ParserFunction(Tout)
    data_TPkni_out_A, time_TPkni_out_A = ParserFunction(TPkni_out_A)
    data_TPkni_out_B, time_TPkni_out_B = ParserFunction(TPkni_out_B)
    data_TPkni_in, time_TPkni_in = ParserFunction(TPkni_in)
    data_TPkni_oo, time_TPkni_oo = ParserFunction(TPkni_oo)

    diff_data1, diff_time1 = DataDifference(data_TPkni_out_A, data_Tout, time_TPkni_out_A,sort_indexes)
    diff_data2, diff_time2 = DataDifference(data_TPkni_out_B, data_Tout, time_TPkni_out_B,sort_indexes)
    diff_data3, diff_time3 = DataDifference(data_TPkni_out_A, data_TPkni_out_B, time_TPkni_out_A)

    ppp1 = pd.DataFrame(diff_data1, diff_time1)
    ppp2 = pd.DataFrame(diff_data2, diff_time2)
    ppp3 = pd.DataFrame(diff_data3, diff_time3)

    fig = plt.figure()

    plt.title("\nГрафик 1: разность температур Tout и TPkni_out_A"
              "\nГрафик 2: разность температур Tout и TPkni_out_B"
              "\nГрафик 3: разность температур TPkni_out_A и TPkni_out_B")

    plt.xticks([])
    plt.yticks([])

    ax_1 = fig.add_subplot(3, 1, 1)
    plt.xlabel("Дата, гг-мм")
    plt.ylabel("Температура, °C")
    plt.plot(ppp1)
    plt.axhline(y = 35,linewidth = 3)
    plt.axhline(y = -35,linewidth = 3)
    plt.grid()

    ax_2 = fig.add_subplot(3, 1, 2)
    plt.xlabel("Дата, гг-мм")
    plt.ylabel("Температура, °C")
    plt.plot(ppp2)
    plt.axhline(y=35,linewidth = 3)
    plt.axhline(y=-35,linewidth = 3)
    plt.grid()

    ax_3 = fig.add_subplot(3, 1, 3)
    plt.xlabel("Дата, гг-мм")
    plt.ylabel("Температура, °C")
    plt.plot(ppp3)
    plt.axhline(y=20,linewidth = 3)
    plt.axhline(y=-20,linewidth = 3)
    plt.grid()

    plt.show()

if __name__ == "__main__":
    PandasWork()