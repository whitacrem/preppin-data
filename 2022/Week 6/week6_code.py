import pandas as pd
import numpy as np

# Import the data
tiles = pd.read_csv('Scrabble_Scores.csv')
words = pd.read_csv('7_letter_words.csv')
scaffold = pd.read_csv('Scaffold.csv')

# Parse out the information in Scrabble Scores so there are three fields: tile, frequency, points
tiles[['Points', 'Tile']] = tiles['Scrabble'].str.split(':', expand=True)
tiles = tiles.drop(columns=['Scrabble'])
tiles['Tile'] = tiles['Tile'].str.split(',', expand=True).values.tolist()
tiles = tiles.explode('Tile')
tiles = tiles.dropna()
tiles['Points'] = tiles['Points'].map(lambda x: int(x.strip(' points')))
tiles['Frequency'] = tiles['Tile'].str.extract('(\d+)').astype('int')
tiles['Tile'] = tiles['Tile'].str.extract('(\w+)')

# Calculate the percent chance of drawing a particular tile and round to 2 decimal places
tiles['Percent Chance'] = (tiles['Frequency'] / tiles['Frequency'].sum()).round(2)

# Split each of the seven letter words into individual letters and count the frequency of each letter
words['Tile'] = words['7 letter word'].str.upper().str.split('').values.tolist()
words = words.explode('Tile')
words = words.replace('', np.nan)
words = words.dropna()
words['Count'] = words['Tile'].groupby([words['7 letter word'], words['Tile']]).transform('count')

# Join each letter to its scrabble tile
words = words.merge(tiles, on='Tile')

# Update % chance of drawing a tile based on the number of occurrences in each word
words = words.assign(New_Chance=lambda x: np.where(x['Count'] > x['Frequency'], 0, x['Percent Chance'] ** x['Count']))

# Calculate the total points each word would score
words = words.assign(Total_Points=lambda x: x['Points'] * x['Count'])

# Group by word and filter out words with a 0% chance
final = words.groupby('7 letter word').agg(Total_Chance=('New_Chance', 'prod'), Total_Points=('Total_Points', 'sum')).reset_index()
final = final[final['Total_Chance'] != 0.0]

# Rank the words by their percent chance and total points
final['Likelihood Rank'] = final['Total_Chance'].rank(method='dense').astype(int)
final['Points Rank'] = final['Total_Points'].rank(method='dense').astype(int)
final = final.sort_values(['Likelihood Rank', 'Points Rank'])
final = final.rename(columns={'Total_Chance':'% Chance', 'Total_Points':'Total Points'})
final = final[['Points Rank', 'Likelihood Rank', '7 letter word', '% Chance', 'Total Points']]

# Export to csv
final.to_csv('Week_6_output.csv')