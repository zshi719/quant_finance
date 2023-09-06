import os
import pandas as pd
import datetime

# Please complete the calculate_sentiment function below
# It takes in the dataframe "df_sa" with polarity scores
# Please achieve the following:
# 1. Calculate the mean of the "compound" column and round it to 2 decimal place for each ticker, and we treat this value as the mean sentiment of that stock
# 2. Create a new dataframe with 2 columns: 'Ticker' and 'Mean Sentiment'
# 3. Sort the new dataframe by mean sentiment in decending order
# 4. Return the sorted dataframe
# HINT: You might want to take a look at the given dataframe "df_sa" first

def calculate_sentiment(df_sa):
    # You need to get a list of the tickers contained in the provided dataframe
    unique_ticker = list(set(df_sa['Ticker']))
    # Creat an empty list to store the mean value
    values = []
    # Iterate each ticker and calculate the mean sentiment
    for ticker in unique_ticker:
        # Filter the rows containing the ticker
        dataframe = df_sa[df_sa['Ticker']==ticker]
        # Set the new index as "Ticker"
        dataframe = dataframe.set_index('Ticker')
        # Remove the "Headline" column
        dataframe = dataframe.drop(columns = ['Headline'])

        # Calculate the mean of the "compound" column and round it to 2 decimal places
        mean = round(dataframe['compound'].mean(), 6)
        # Append the mean to the list "values"
        values.append(mean)

    # Create a new dataframe that maps the ticker and its mean sentiment
    df = pd.DataFrame(list(zip(unique_ticker, values)), columns =['Ticker', 'Mean Sentiment'])
    # Set the index as "Ticker"
    df = df.set_index('Ticker')
    # Sort the dataframe by mean sentiment in decending order
    df = df.sort_values('Mean Sentiment', ascending=False)
    df = round(df, 2)
    return df


def test1(df_sa):
    c = calculate_sentiment(df_sa)
    fptr.write(c.to_string())

def test2(df_sa):
    c = calculate_sentiment(df_sa)
    fptr.write(c.to_string())

def test3(df_sa):
    c = calculate_sentiment(df_sa)
    fptr.write(c.to_string())

def test4(df_sa):
    c = calculate_sentiment(df_sa)
    fptr.write(c.to_string())


if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')
    tmp = input()
    rows_num = int(input().strip())

    data = []
    colnames = list(map(str, input().rstrip().split('\t')))
    for i in range(rows_num):
        line = list(map(str, input().split('\t')))
        line[0] = line[0]
        line[1] = line[1]
        line[2] = line[2]
        line[3] = line[3]
        line[4] = line[4]
        line[5] = line[5]
        line[6] = float(line[6])
        line[7] = float(line[7])
        line[8] = float(line[8])
        line[9] = float(line[9])
        data.append(line)

    df_sa = pd.DataFrame(data, columns = colnames)

    if tmp == '1':
        test1(df_sa)
    elif tmp == '2':
        test2(df_sa)
    elif tmp == '3':
        test3(df_sa)
    elif tmp == '4':
        test4(df_sa)
    else:
        raise RuntimeError('invalid input')