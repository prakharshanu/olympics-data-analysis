import numpy as np
import pandas as pd


def fetch_medal_tally(df,year,country):
    medal_df=df.drop_duplicates(subset=['Team','NOC','Year','Event','Medal'])
    flag=0
    if year=='Overall' and country=='Overall':
        temp_df=medal_df
    if year== 'Overall' and country!='Overall':
        flag = 1
        temp_df=medal_df[medal_df['region']==country]
    if year!='Overall' and country=='Overall':
        temp_df=medal_df[medal_df['Year']==int(year)]
    if year!='Overall' and country!='Overall':
        temp_df=medal_df[(medal_df['region']==country) & (medal_df['Year']==int(year))]
    if temp_df.empty:
        if flag == 1:
            result_df = pd.DataFrame({'Year': [int(year)], 'Gold': [0], 'Silver': [0], 'Bronze': [0], 'total': [0]})
        else:
            result_df = pd.DataFrame({'region': [country], 'Gold': [0], 'Silver': [0], 'Bronze': [0], 'total': [0]})
    else:
        if flag == 1:
            x = temp_df.groupby('Year').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Year').reset_index()
        else:
            x = temp_df.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold', ascending=False).reset_index()
        x['total'] = x['Gold'] + x['Silver'] + x['Bronze']
        result_df = x
    return result_df


def country_year_list(df):
    years = df['Year'].unique().tolist()
    years.sort()
    years.insert(0, 'Overall')
    country = np.unique(df['region'].dropna().values).tolist()
    country.sort()
    country.insert(0, 'Overall')
    return years, country


def data_over_time(df, col):
    nations_over_time = df.drop_duplicates(['Year', col])['Year'].value_counts().reset_index()
    nations_over_time.columns=['Edition', col]
    nations_over_time = nations_over_time.sort_values('Edition')
    return nations_over_time

def most_successful(df,sport):
    temp_df = df.dropna(subset=['Medal'])
    if sport != 'Overall':
        temp_df = temp_df[temp_df['Sport']==sport]
    athlete_medal_counts = temp_df['Name'].value_counts().reset_index().head(15)
    athlete_medal_counts.columns=['Name','Medals']
    x= athlete_medal_counts.merge(df, left_on='Name', right_on='Name', how='left')[['Name','Medals','Sport','region']]
    x = x.drop_duplicates('Name')
    x.columns = ['Name', 'Medals', 'Sports', 'region']
    return x


def yearwise_medal_tally(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset={'Team', 'NOC', 'Year', 'Event', 'Medal'}, inplace=True)

    new_df = temp_df[temp_df['region'] == country]
    final_df = new_df.groupby('Year').count()['Medal'].reset_index()
    return final_df

def country_event_heatmap(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset={'Team', 'NOC', 'Year', 'Event', 'Medal'}, inplace=True)

    new_df = temp_df[temp_df['region'] == country]
    pt=new_df.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0)
    return pt

def most_successful_countrywise(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df = temp_df[temp_df['region']==country]
    athlete_medal_counts = temp_df['Name'].value_counts().reset_index().head(10)
    athlete_medal_counts.columns=['Name','Medals']
    x= athlete_medal_counts.merge(df, left_on='Name', right_on='Name', how='left')[['Name','Medals','Sport']]
    x = x.drop_duplicates('Name')
    x.columns = ['Name', 'Medals', 'Sports']
    return x

def men_vs_women(df):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    men = athlete_df[athlete_df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    women = athlete_df[athlete_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()

    final = men.merge(women, on='Year', how='left')
    final.rename(columns={'Name_x': 'Male', 'Name_y': 'Female'}, inplace=True)

    final.fillna(0, inplace=True)

    return final

