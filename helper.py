import numpy as np


def fetch_medal_tally(df, year, country):
    medal_df = df.drop_duplicates(
        subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal']
    )

    flag = 0
    if year == 'Overall' and country == 'Overall':
        temp_df = medal_df
    elif year == 'Overall' and country != 'Overall':
        flag = 1
        temp_df = medal_df[medal_df['region'] == country]
    elif year != 'Overall' and country == 'Overall':
        temp_df = medal_df[medal_df['Year'] == int(year)]
    else:
        temp_df = medal_df[(medal_df['Year'] == int(year)) & (medal_df['region'] == country)]

    if flag == 1:
        x = temp_df.groupby('Year')[['Gold', 'Silver', 'Bronze']].sum().reset_index()
    else:
        x = temp_df.groupby('region')[['Gold', 'Silver', 'Bronze']].sum().reset_index()

    x['total'] = x[['Gold', 'Silver', 'Bronze']].sum(axis=1)

    # Sort by total medals (descending)
    x = x.sort_values('total', ascending=False).reset_index(drop=True)

    return x


def country_year_list(df):
    years = sorted(df['Year'].unique().tolist())
    years.insert(0, 'Overall')

    countries = sorted(df['region'].dropna().unique().tolist())
    countries.insert(0, 'Overall')

    return years, countries


def data_over_time(df, col):
    temp = df.drop_duplicates(['Year', col])
    # Count occurrences by year
    result = temp['Year'].value_counts().reset_index()
    # Rename columns properly
    result.columns = ['Edition', col]
    # Sort by Edition (Year)
    result = result.sort_values('Edition')
    return result


def most_successful(df, sport):
    temp = df.dropna(subset=['Medal'])
    if sport != 'Overall':
        temp = temp[temp['Sport'] == sport]

    x = temp['Name'].value_counts().reset_index().head(15)
    x.columns = ['Name', 'Medals']
    result = x.merge(df, left_on='Name', right_on='Name', how='left') \
        [['Name', 'Medals', 'Sport', 'region']] \
        .drop_duplicates('Name') \
        .sort_values('Medals', ascending=False) \
        .reset_index(drop=True)
    return result


def yearwise_medal_tally(df, country):
    temp = df.dropna(subset=['Medal']).drop_duplicates(
        subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal']
    )
    new_df = temp[temp['region'] == country]
    result = new_df.groupby('Year')['Medal'].count().reset_index() \
        .sort_values('Year') \
        .rename(columns={'Medal': 'Count'})
    return result


def country_event_heatmap(df, country):
    temp = df.dropna(subset=['Medal']).drop_duplicates(
        subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal']
    )
    new_df = temp[temp['region'] == country]
    pivot_table = new_df.pivot_table(index='Sport', columns='Year',
                                     values='Medal', aggfunc='count').fillna(0)
    # Sort by total medals
    pivot_table['Total'] = pivot_table.sum(axis=1)
    pivot_table = pivot_table.sort_values('Total', ascending=False).drop('Total', axis=1)
    return pivot_table


def most_successful_countrywise(df, country):
    temp = df.dropna(subset=['Medal'])
    temp = temp[temp['region'] == country]

    x = temp['Name'].value_counts().reset_index().head(10)
    x.columns = ['Name', 'Medals']

    result = x.merge(df, on='Name', how='left')[['Name', 'Medals', 'Sport']] \
        .drop_duplicates('Name') \
        .sort_values('Medals', ascending=False) \
        .reset_index(drop=True)
    return result


def weight_v_height(df, sport):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    athlete_df['Medal'].fillna('No Medal', inplace=True)

    if sport != 'Overall':
        return athlete_df[athlete_df['Sport'] == sport]
    return athlete_df


def men_vs_women(df):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    men = athlete_df[athlete_df['Sex'] == 'M'].groupby('Year')['Name'].count().reset_index()
    women = athlete_df[athlete_df['Sex'] == 'F'].groupby('Year')['Name'].count().reset_index()

    final = men.merge(women, on='Year', how='outer')
    final.columns = ['Year', 'Male', 'Female']
    final = final.sort_values('Year').fillna(0)
    final['Male'] = final['Male'].astype(int)
    final['Female'] = final['Female'].astype(int)
    return final