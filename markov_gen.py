#Markov matrix generator for Markov Time Series

import pandas as pd

#Main method. Returns the matrix with all values filled in
def getMatrix(bound, intervals, prices, period):
    #initialize return value as empty matrix of correct size
    ret = init_matrix(intervals)

    #get the interval values
    ints = getIntervals(bound, intervals)
    #initilize prev as percent change in first 7 days
    prev = 100 * (1 - (prices[period] / prices[0]))
    #loop through prices in 7 day increments, filling out the matrix
    for i in range(1, len(prices) / period):

        # regarding return formula: correct but confusing .. standard practice for calculating return would be the following
            # 100 * (prices[period * (i+1)] / (prices[period * i])
        # however i did not want to change it because youre correct
        if(period * (i+1) >= len(prices)):
            break
        change = 100 * (1 - (prices[period * i] / prices[period * (i+1)]))
        first, second = interval(prev, ints), interval(change, ints)
        ret[first][second] += 1
        prev = change
    return matricize(ret), ints


def getIntervals(bound, intervals):
    dif = bound * 2 / intervals
    ret = [-bound]
    prev = -bound
    for i in range(intervals):
        ret.append((prev, prev + dif))
        prev += dif
    ret.append(bound)
    return ret

def interval(perc_change, intervals):
    if perc_change < intervals[0]:
        return 0
    elif perc_change >= intervals[-1]:
        return len(intervals) - 1
    for i in range(1, len(intervals)-1):
        if perc_change >= intervals[i][0] and perc_change < intervals[i][1]:
            return i - 1

def init_matrix(intervals):
    ret = []
    line = []
    for i in range(intervals+2):
        for n in range(intervals+2):
            line.append(0)
        ret.append(line)
        line = []
    return ret

def matricize(matrix):
    ret = []
    line = []
    for i in matrix:
        total = sum(i)
        if total == 0:
            for n in range(len(i)):
                line.append(0)
            ret.append(line)
            line = []
            continue
        for n in i:
            line.append(float(n) / total)
        ret.append(line)
        line = []
    return ret

if __name__ == '__main__':
    hist = pd.read_csv('ETH Hist.csv')
    prices = list()
    for i in hist['Close']:
        prices.insert(0, i)
    a = getMatrix(15, 6, prices, 7)
    for i in a:
        print i
