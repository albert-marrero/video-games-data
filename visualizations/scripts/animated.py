import time
import pandas as pd
import bar_chart_race as bcr

# decorator to calculate duration
# taken by any function.
def calculate_time(func):
     
    # added arguments inside the inner1,
    # if function takes any arguments,
    # can be added like this.
    def inner1(*args, **kwargs):
 
        # storing time before function execution
        begin = time.time()
         
        # getting the returned value
        returned_value = func(*args, **kwargs)
 
        # storing time after function execution
        end = time.time()
        print("Total time taken in : ", func.__name__, end - begin)

        # returning the value to the original frame
        return returned_value
 
    return inner1

@calculate_time
def vg_platform_history():
    #load JSON data
    df = pd.read_json('../../videogamegeek/games/2022-03-05.json')

    # remove unneessessary features
    df = df[['id', 'name', 'versions']]

    # transform versions list-like to a row, replicating index value
    df = df.explode('versions')

    # create a series based on versions columns
    # flatten object in versions columns
    versions = df['versions'].apply(pd.Series)

    # join columns of the version series
    df = df.join(versions)

    # convert the 'release_date' string column to datetime format
    df['release_date']= pd.to_datetime(df['release_date'], format='%Y-%m-%d', errors='coerce')

    # remove unneessessary features
    df = df[['id', 'name', 'release_date', 'platform']]

    # remove missing values
    df = df.dropna()

    # remove duplicate rows
    df = df.drop_duplicates()

    # can out csv for source data here
    df.to_csv('../../visualizations/data/vg_platform_history.csv', index = False)

    # remove unneessessary features
    df = df[['release_date', 'platform']]

   # reformat release date to year
    df['release_date']= df["release_date"].dt.strftime("%Y-%m")

    # number of rows by specific group
    df = df.groupby(['platform', 'release_date']).size().reset_index(name='counts')

    # pivot table on release date and platforms
    df = df.pivot_table(values = 'counts',index = ['release_date'], columns = 'platform')

    # replace missing values and sort by release date
    df = df.fillna(0)
    df = df.sort_values(list(df.columns))
    df = df.sort_index()

    # aggregate and clean the data
    df.iloc[:, 0:-1] = df.iloc[:, 0:-1].cumsum()

    # remove data that will never make top 10
    top_set = list()

    for index, row in df.iterrows():
        top_set.extend(row[row > 0].sort_values(ascending=False).head(10).index.tolist())

    # using set() to remove duplicated  from list 
    top_set = list(set(top_set))

    df = df[top_set]

    # create bar chart race movie
    bcr.bar_chart_race(
        df = df, 
        n_bars = 10, 
        sort = 'desc',
        title = 'Video Games Platform History',
        filename = '../charts/vg_platform_history.mp4',
        filter_column_colors = True
    )

@calculate_time
def vg_genre_history():
    #load JSON data
    df = pd.read_json('../../videogamegeek/games/2022-03-05.json')

    # remove unneessessary features
    df = df[['id', 'name', 'release_date', 'genre']]

    # transform versions list-like to a row, replicating index value
    df = df.explode('genre')

    # strip genre columns
    df['genre'] = df['genre'].str.split(':').str[0]

    # convert the 'release_date' string column to datetime format
    df['release_date']= pd.to_datetime(df['release_date'], format='%Y-%m-%d', errors='coerce')

    # remove missing values
    df = df.dropna()

    # remove duplicate rows
    df = df.drop_duplicates()

    # can out csv for source data here
    df.to_csv('../../visualizations/data/vg_genre_history.csv', index = False)

    # remove unneessessary features
    df = df[['release_date', 'genre']]

   # reformat release date to year
    df['release_date']= df["release_date"].dt.strftime("%Y-%m")

    # number of rows by specific group
    df = df.groupby(['genre', 'release_date']).size().reset_index(name='counts')

    # pivot table on release date and platforms
    df = df.pivot_table(values = 'counts',index = ['release_date'], columns = 'genre')

    # replace missing values and sort by release date
    df = df.fillna(0)
    df = df.sort_values(list(df.columns))
    df = df.sort_index()

    # aggregate and clean the data
    df.iloc[:, 0:-1] = df.iloc[:, 0:-1].cumsum()

    # remove data that will never make top 10
    top_set = list()

    for index, row in df.iterrows():
        top_set.extend(row[row > 0].sort_values(ascending=False).head(10).index.tolist())

    # using set() to remove duplicated  from list 
    top_set = list(set(top_set))

    df = df[top_set]

    # create bar chart race movie
    bcr.bar_chart_race(
        df = df, 
        n_bars = 10, 
        sort = 'desc',
        title = 'Video Games Genre History',
        filename = '../charts/vg_genre_history.mp4',
        filter_column_colors = True
    )

def main():
    vg_platform_history()
    vg_genre_history()

if __name__ == "__main__":
    main()