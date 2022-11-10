import pandas as pd
import matplotlib.pyplot as plt
from decimal import *
import datetime
from multipledispatch import dispatch

def Onespl(df, left, right):
    df_new = df.iloc[:, left:right]

    return df_new

# Разбиение данных(54 графика) и их сортировка
# на 6 групп по 9 графиков по cреднему значению
# в столбце
def SplittingData(df1, df2, title, df_Nakz):
    for i in range(len(df1.columns)-1):
        for j in range(len(df1.columns)-1):
            if df1[j].median() > df1[j+1].median():
                buff = df1[j]
                df1[j] = df1[j+1]
                df1[j+1] = buff

            if df2[j].median() > df2[j+1].median():
                buff = df2[j]
                df2[j] = df2[j+1]
                df2[j+1] = buff

    figure = CreateFigure(title)

    num = 1
    left = 0
    right = 9

    df11 = Onespl(df1, left, right)
    df21 = Onespl(df2, left, right)
    left = right
    right += 9

    df12 = Onespl(df1, left, right)
    df22 = Onespl(df2, left, right)
    left = right
    right += 9

    df13 = Onespl(df1, left, right)
    df23 = Onespl(df2, left, right)
    left = right
    right += 9

    df14 = Onespl(df1, left, right)
    df24 = Onespl(df2, left, right)
    left = right
    right += 9

    df15 = Onespl(df1, left, right)
    df25 = Onespl(df2, left, right)
    left = right
    right += 9

    df16 = Onespl(df1, left, right)
    df26 = Onespl(df2, left, right)

    y_lable = 'Температура, °C'

    PlotWork(df11,figure, num, y_lable, df_Nakz)
    PlotWork(df21, figure, num+1, y_lable, df_Nakz)
    num += 2

    PlotWork(df12, figure, num, y_lable, df_Nakz)
    PlotWork(df22, figure, num+1, y_lable, df_Nakz)
    num += 2

    PlotWork(df13, figure, num, y_lable, df_Nakz)
    PlotWork(df23, figure, num+1, y_lable, df_Nakz)
    num += 2

    PlotWork(df14, figure, num, y_lable, df_Nakz)
    PlotWork(df24, figure, num+1, y_lable, df_Nakz)
    num += 2

    PlotWork(df15, figure, num, y_lable, df_Nakz)
    PlotWork(df25, figure, num+1, y_lable, df_Nakz)
    num += 2

    PlotWork(df16, figure, num, y_lable, df_Nakz)
    PlotWork(df26, figure, num+1, y_lable, df_Nakz)

# Создание полотна, его заголовка и удаление обозначений по осям,
# которые стоят по умолчанию
def CreateFigure(title):
    fig = plt.figure()

    plt.title(title)

    plt.xticks([])
    plt.yticks([])
    plt.axis('off')

    return fig

# Добавление на полотно нового графика(subplot) и выведение
# на экран готового полотна
def PlotWork(df, fig, plt_count, y_label, df_Nakz):
    axis = fig.add_subplot(6, 2, plt_count)
    plt.xlabel("Дата, гг-мм-дд  чч:мм:сс")
    plt.ylabel(y_label)
    plt.plot(df)
    plt.grid()

    axis = axis.twinx()
    plt.ylabel('Мощность, Вт')
    plt.plot(df_Nakz)


# Чтение индексов соответствия номера конкретной ТВС
# номеру конкретной КНИ из файла "NKni_TW.txt"
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
def ConvergenceTube(data_row):
    df_data_row = pd.DataFrame(data_row)

    for i in range(len(df_data_row)):
        if float(df_data_row.iloc[i]) > 30 or float(df_data_row.iloc[i]) < -30:
            if i == 0:
                df_data_row.iloc[i] = 0
            else:
                df_data_row.iloc[i] = df_data_row.median()

        data_row[i] = float(df_data_row.iloc[i])

    return data_row

# Вычисление разности температур Tout и TPkni_out_A/B
@dispatch(list,list,list,pd.DataFrame, bool)
def DataDifference(data1,data_tout,time1,sort_ind, correct):
    diff_data = []
    diff_time = time1

    for i in range(len(data_tout)):
        diff_data.append([])
        diff_data_buff = []

        for j in range(len(sort_ind)):
            diff_data_buff.append(data_tout[i][sort_ind[0][j]-1]-data1[i][sort_ind[1][j]-1])

        if correct == True:
            diff_data_buff = ConvergenceTube(diff_data_buff)

        for k in range(len(data1[0])):
            diff_data[i].append(diff_data_buff[k])

    return diff_data, diff_time

# Вычисление разности температур других файлов
@dispatch(list,list,list)
def DataDifference(data1,data2,time1):
    diff_data = []
    diff_time = []
    diff_counter = 0
    diff_time = time1

    for i in range(len(data1)):

        diff_data_buff = []
        diff_data.append([])

        for j in range(len(data1[0])):
            diff_data_buff.append(data2[i][j]-data1[i][j])

        # diff_data_buff1 = ConvergenceTube(diff_data_buff1)

        for k in range(len(data1[0])):
            diff_data[i].append(diff_data_buff[k])

        diff_counter += 1

    return diff_data, diff_time

# Считывание значений температур из переменной "line",
# которая хранит в себе текст из файла:print(diff_data)
def GetDataFromFile(line):
    num = 0
    line = line.replace('\t', ' ')
    line = line.replace(' ', '', 1)
    print(line)
    while line[num:]:
        if line[num] == ' ':
            num += 1
            line = line[num:]
            break
        num += 1

    print(line)
    exit(0)
    return line

# Считывание значений даты и времени из переменной
# "line", которая хранит в себе текст из файла
def GetTimeFromFile(line):
    point = 13
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

if __name__ == "__main__":
    Tout = 'Tout.txt'
    TPkni_out_A = 'TPkni_out_A.txt'
    TPkni_out_B = 'TPkni_out_B.txt'
    TPkni_in = 'TPkni_in.txt'
    TPkni_oo = 'TPkni_oo.txt'
    NKni_TW = 'NKni_TW.txt'
    NKni_TW_Ntp = 'NKni_TW_Ntp.txt'
    Nakz = 'Nakz.txt'

    title = "Графики разностей температур Tout и TPkni_out_A, а также " \
            "график мощностей"

    sort_indexes = Get_Indexes(NKni_TW)

    data_Nakz, time_Nakz = ParserFunction(Nakz)
    data_Tout, time_Tout = ParserFunction(Tout)
    data_TPkni_out_A, time_TPkni_out_A = ParserFunction(TPkni_out_A)
    # data_TPkni_out_B, time_TPkni_out_B = ParserFunction(TPkni_out_B)
    # data_TPkni_in, time_TPkni_in = ParserFunction(TPkni_in)
    # data_TPkni_oo, time_TPkni_oo = ParserFunction(TPkni_oo)

    # diff_data2, diff_time2 = DataDifference(data_TPkni_out_B, data_Tout, time_TPkni_out_B,sort_indexes, False)
    # diff_data3, diff_time3 = DataDifference(data_TPkni_out_A, data_TPkni_out_B, time_TPkni_out_A)

    diff_data1, diff_time1 = DataDifference(data_TPkni_out_A, data_Tout, time_TPkni_out_A, sort_indexes, False)
    pd_df_1 = pd.DataFrame(diff_data1, diff_time1)

    diff_data1, diff_time1 = DataDifference(data_TPkni_out_A, data_Tout, time_TPkni_out_A,sort_indexes, True)
    pd_df_2 = pd.DataFrame(diff_data1, diff_time1)

    # pd_df_2 = pd.DataFrame(diff_data2, diff_time2)
    # pd_df_3 = pd.DataFrame(diff_data3, diff_time3)
    pd_df_Nakz = pd.DataFrame(data_Nakz, time_Nakz)

    SplittingData(pd_df_1, pd_df_2, title, pd_df_Nakz)



    plt.show()

    # SplittingData(pd_df_2, title)
    # SplittingData(pd_df_3, title)