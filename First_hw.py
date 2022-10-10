# -*- coding: utf-8 -*-

from random import randint
import time

start_time = time.time() # Проверка скорости работы программы при построчном выводе и единовременном выводе программы
RES_TIME_ARR = [] # Список результирующего времени

# Нахождение мин. и макс. времени выполнения calcHistogram(data)
def calcMinMaxTime(resTime):

    minElem = 10000
    maxElem = -10000

    for val in resTime:
        if val > maxElem:
            maxElem = val
        if val < minElem:
            minElem = val

    return minElem, maxElem

# Нахождения среднего времени и выполнения функции calcHist(data)
def calcAverageTime(resTime):

    sum = 0

    for val in resTime:
        sum += val

    avg = sum/100

    return avg

# Подсчет времени выполнения функции для каждой из 100 итераций
def calcTime(array):

    output_res_arr = []
    for i in range(0, 100):
        #########__Расчет времени__##########
        startTime = time.time()
        calcHistogram(array)
        endTime = time.time()
        #########__Добавлне времени в массив__##########
        RES_TIME_ARR.append(endTime - startTime)
        ########__Заполнение массива для единовременного вывода__###########
        output_res ='i = ', i + 1, ', Время выполнения = ', RES_TIME_ARR[i], '\n'
        output_res_arr.append(output_res)
        ###################

    avg = calcAverageTime(RES_TIME_ARR)
    min, max = calcMinMaxTime(RES_TIME_ARR)
    ########Блок вывода в консоль###########
    for res in output_res_arr:
        print(res)
    print('Максимальное время работы: ', max, '\n')
    print('Среднее время работы: ', avg, '\n')
    print('Минимальное время работы: ', min, '\n')

# Подсчет частоты вхождения элементов
def calcHistogram(data):

    hist = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    for i in range(0, 1000000):
        if data[i] >= 0 and data[i] <= 99:
            hist[0] += 1
        if data[i] >= 100 and data[i] <= 199:
            hist[1] += 1
        if data[i] >= 200 and data[i] <= 299:
            hist[2] += 1
        if data[i] >= 300 and data[i] <= 399:
            hist[3] += 1
        if data[i] >= 400 and data[i] <= 499:
            hist[4] += 1
        if data[i] >= 500 and data[i] <= 599:
            hist[5] += 1
        if data[i] >= 600 and data[i] <= 699:
            hist[6] += 1
        if data[i] >= 700 and data[i] <= 799:
            hist[7] += 1
        if data[i] >= 800 and data[i] <= 899:
            hist[8] += 1
        if data[i] >= 900 and data[i] <= 999:
            hist[9] += 1

# Заполнение массива из 1 000 000 элементов целыми числами от 0 до 999
def initListWithRandomNumbers():

    array = []

    for i in range(0,1000000):
        arr_buff = randint(0,999)
        array.append(arr_buff)

    calcTime(array)

if __name__ == '__main__':
    initListWithRandomNumbers()
    print("--- %s seconds ---" % (time.time() - start_time))


