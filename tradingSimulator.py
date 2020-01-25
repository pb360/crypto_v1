from markov_gen import getMatrix, interval
import pandas as pd

hist = pd.read_csv('ETH Hist.csv')
prices = list()
for i in hist['Close']:
    prices.insert(0, i)
previous_count = .5
position = [0, 0]

def simulate(mon, bounds, intervals):
    money = mon
    bnds = bounds
    intrvls = intervals
    previous = previous_count * len(prices)
    previous = int(previous)
    for i in prices[previous:]:
        decision = evaluate(prices[:previous], 7, money, bnds, intrvls)
        position[0] += decision[0]
        position[1] += decision[1]
        #print "Current position " + str(position[0]) + " ETH with $" + str(position[1])
        money += decision[1]
        previous += 1
    #print "$" + str(money) + " and " + str((position[0] * prices[-1])) + "ETH"
    return money + (position[0] * prices[-1])

def evaluate(previous_data, period, money, bounds, intervals):
    #takes an array of previous prices
    #RETURNS: tuple of (coins exchanged, investment)
    #A buy will be a negative investment, a sell will be a positive investment
    matrix, ints = getMatrix(bounds, intervals, previous_data, period)
    prev = 100 * (1 - (previous_data[-1] / previous_data[-period]))
    probs = interval(prev, ints)
    up_prob = sum(matrix[probs][intervals/2+1:])
    if up_prob > .6 and money > 0:
        return buy(money * up_prob, previous_data[-1], money)
    if up_prob < .1 and position[0] > 0:
        return sell(up_prob, previous_data[-1])
    return (0, 0)

def buy(dollar_amount, price, money):
    if dollar_amount > money:
        dollar_amount = money
    coins = dollar_amount / price
    #print "Bought " + str(coins) + " coins at $" + str(price)
    return coins, -dollar_amount

def sell(up_prob, price):
    #sell = (1-up_prob) * position[0]
    sell = position[0]
    #print "Sold  " + str(sell) + " coins at $" + str(price)
    return -sell, sell*price

if __name__ == '__main__':
    maxretrn = 0
    for i in range(10, 31):  #loop for bounds
        for j in range(2, 15):  #loop for intervals
            if (2 * i) % j == 0 and j<i:
                retrn = simulate(10000, i, j)
                if retrn > maxretrn:
                    maxretrn = retrn
                    maxBound = i
                    maxInt = j
    print("Money: " + str(maxretrn) + " | Bound: " + str(maxBound) + " | Intervals: " + str(maxInt))
                #print("Money: " + str(retrn) + " | Bound: " + str(i) + " | Intervals: " + str(j))
    #print simulate(10000, 15, 10)
    print("vs")
    print(str((10000/prices[int(previous_count * len(prices))]) * prices[-1]) + " return if held the entire time")