import pandas as pd
import matplotlib.pyplot as plt
from decimal import *
import datetime
from sys import *

# Вычитание из элементов Tout элементы Других файлов:
def DataDifference(data1,data_tout,time1):

    diff_data = []
    diff_time = time1
    for i in range(len(data1)):
        diff_data.append([])
        for j in range(len(data1[0])):
            diff_data[i].append(data_tout[i][j]-data1[i][j])

    PandasWork(diff_data, diff_time)

    return diff_data, diff_time

# Считывание значений температур из переменной "line",
# которая хранит в себе текст из файла:
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
# "line", которая хранит в себе текст из файла:
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
# "pandas", а также последующее выведение этих данных на график:
def PandasWork(data_pd,time_pd):

    print(pd.DataFrame(data_pd, time_pd),'\n\n\n')
    ppp = pd.DataFrame(data_pd, time_pd)
    plt.title("Разность вычисленной (Tout) и измеренной (TPkni_out_A) температур")
    plt.xlabel("Дата")
    plt.ylabel("Температура")
    plt.plot(ppp)
    plt.xticks(rotation=45)
    plt.show()

def main():
    Tout = 'Tout.txt'
    TPkni_out_A = 'TPkni_out_A.txt'
    TPkni_out_B = 'TPkni_out_B.txt'
    TPkni_in = 'TPkni_in.txt'
    TPkni_oo = 'TPkni_oo.txt'

    data_Tout, time_Tout = ParserFunction(Tout)
    data_TPkni_out_A, time_TPkni_out_A = ParserFunction(TPkni_out_A)
    data_TPkni_out_B, time_TPkni_out_B = ParserFunction(TPkni_out_B)
    data_TPkni_in, time_TPkni_in = ParserFunction(TPkni_in)
    data_TPkni_oo, time_TPkni_oo = ParserFunction(TPkni_oo)

    DataDifference(data_TPkni_out_A,data_Tout,time_TPkni_out_A)

if __name__ == "__main__":
    main()