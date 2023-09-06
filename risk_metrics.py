import os
import pandas as pd
import numpy as np


def histogram_weekly_losses(results):
    # create histogram for the weekly losses
    # use the folloing functions with bins=50
    #weekly_losses,_=np.histogram(weekly_losses,bins=50)
    results.index = pd.to_datetime(results.index)
    df_pnl = results['Pnl'].diff(5)
    df_loss = df_pnl[df_pnl < 0]
    weekly_losses, _ = np.histogram(df_loss, bins=50)
    return weekly_losses


def histogram_monthly_losses(results):
    # create histogram for the monthly losses
    # use the folloing functions with bins=50
    #weekly_losses,_=np.histogram(weekly_losses,bins=50)

    results.index = pd.to_datetime(results.index)
    df_month = results.Pnl.diff(20)
    df_month = df_month[df_month < 0]
    monthly_losses, _ = np.histogram(df_month, bins=50)
    return monthly_losses


def max_draw_down(results):
    equity_series = pd.Series(results.Pnl)

    # Calculate the running maximum equity value
    running_max = equity_series.cummax()

    # Calculate drawdowns
    drawdowns = equity_series - running_max

    # Get maximum drawdown
    max_drawdown = drawdowns.min()
    return round(max_drawdown,2)


def histogram_position_holding_times(results):
    #calculate histogram for the position holding times
    # Calculate position holding times

    position_holding_times = []
    holding_time = 0

    for position in results['Position']:
        if position != 0:  # Either a Buy or a Sell
            holding_time += 1
        if holding_time > 0 and position == 0:  # Exit position
            position_holding_times.append(holding_time)
            holding_time = 0


    histogram_position_holding_times,ht=np.histogram(position_holding_times,bins=50)
    pdf=pd.DataFrame(histogram_position_holding_times,
                     index=ht[:-1],columns=["count"])
    pdf.index.name="bins"
    return pdf

def volatility_summary(results):
    def stdev(x):
        return x.std()
    pnls = results['Pnl'].diff(5).dropna()
    weekly_pnls=pnls[::5]

    sharpe_ratio = weekly_pnls.mean() / stdev(weekly_pnls)
    downside_std_dev = stdev(weekly_pnls[weekly_pnls < 0])
    sortino_ratio = weekly_pnls.mean() / downside_std_dev

    # give the volatlity summary for:
    print('PnL Standard Deviation:', stdev(weekly_pnls))
    print('Sharpe ratio:', sharpe_ratio)
    print('Sortino ratio:', sortino_ratio)
    pdf=pd.DataFrame([stdev(weekly_pnls),sharpe_ratio,sortino_ratio],
                     index=['PnL Standard Deviation','Sharpe ratio:','Sortino ratio:'],columns=['Summary'])
    return pdf


def traded_volume_summary(results):
    # calculate the total traded volume
    return abs(results['Trades'] * 10).sum()


if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')
    test_function_name = input()
    rows_num = int(input().strip())
    data = []
    colnames = list(map(str, input().rstrip().split(',')))
    for i in range(rows_num):
        line = list(map(str, input().split(',')))
        line[0] = line[0]
        line[1] = float(line[1])
        line[2] = float(line[2])
        line[3] = float(line[3])
        line[4] = float(line[4])
        line[5] = float(line[5])
        line[6] = float(line[6])
        line[7] = float(line[7])
        line[8] = float(line[8])
        line[9] = float(line[9])
        line[10] = float(line[10])
        line[11] = float(line[11])
        line[12] = float(line[12])
        line[13] = float(line[13])

        data.append(line)

    results = pd.DataFrame(data, columns = colnames)
    results.index=results['Date']


    res=globals()[test_function_name](results)
    fptr.write(str(res))