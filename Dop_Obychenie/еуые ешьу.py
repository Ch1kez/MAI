# -*- coding: utf-8 -*-


#--- 46.2223961353302 seconds ---


from random import randint
import time
start_time = time.time()
# Функция нахождения минимального и максимального
# времени выполнения функции calcHist(tdata)
def calcMinMaxTime(resTime):

    minElem = 10000
    maxElem = -10000

    for val in resTime:

        if val > maxElem:
            maxElem = val

        if val < minElem:
            minElem = val

    return minElem, maxElem

# Функция нахождения среднего времени
# выполнения функции calcHist(tdata)
def calcAverageTime(resTime):

    sum = 0

    for val in resTime:
        sum += val

    avg = sum/100

    return avg

# Функция подсчета времени выполнения функции
# calcHist(tdata) каждую из 100 итераций
def calcTime(array):

    resTimeArr = []

    for i in range(0, 100):

        startTime = time.time()
        calcHist(array)
        endTime = time.time()

        resTimeArr.append(endTime - startTime)

        print('i = ', i + 1, ', Время выполнения = ', resTimeArr[i], '\n')

    avg = calcAverageTime(resTimeArr)
    min, max = calcMinMaxTime(resTimeArr)

    print('Максимальное время работы: ', max, '\n')
    print('Среднее время работы: ', avg, '\n')
    print('Минимальное время работы: ', min, '\n')

# функция подсчета частоты вхождения элементов
# в интервалы
def calcHist(tdata):

    hist = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    for i in range(0, 1000000):
        if tdata[i] >= 0 and tdata[i] <= 99:
            hist[0] += 1
        if tdata[i] >= 100 and tdata[i] <= 199:
            hist[1] += 1
        if tdata[i] >= 200 and tdata[i] <= 299:
            hist[2] += 1
        if tdata[i] >= 300 and tdata[i] <= 399:
            hist[3] += 1
        if tdata[i] >= 400 and tdata[i] <= 499:
            hist[4] += 1
        if tdata[i] >= 500 and tdata[i] <= 599:
            hist[5] += 1
        if tdata[i] >= 600 and tdata[i] <= 699:
            hist[6] += 1
        if tdata[i] >= 700 and tdata[i] <= 799:
            hist[7] += 1
        if tdata[i] >= 800 and tdata[i] <= 899:
            hist[8] += 1
        if tdata[i] >= 900 and tdata[i] <= 999:
            hist[9] += 1

# Функция заполнения массива из 1 000 000 элементов
# целыми числами от 0 до 999
def initListWithRandomNumbers():

    array = []

    for i in range(0,1000000):
        arr_buff = randint(0,999)
        array.append(arr_buff)

    calcTime(array)

def main():

    initListWithRandomNumbers()


if __name__ == '__main__':
    main()
    print("--- %s seconds ---" % (time.time() - start_time))