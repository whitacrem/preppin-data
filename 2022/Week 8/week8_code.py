import pandas as pd
import numpy as np

# Import the stats data
stats = pd.read_excel('input_pkmn_stats_and_evolutions.xlsx', sheet_name='pkmn_stats')

# Remove height, weight, and evolves from columns
stats = stats.drop(columns=['height', 'weight', 'evolves_from'])

# Pivot stats so that all combat factors are one column
stats = stats.melt(id_vars=['name', 'pokedex_number', 'gen_introduced'], var_name='combat_factors', value_name='value')

# Sum together each pokemon's combat factors
stats = stats.groupby(['name', 'pokedex_number', 'gen_introduced']).sum().reset_index()

# Import evolutions data
evolutions = pd.read_excel('input_pkmn_stats_and_evolutions.xlsx', sheet_name='pkmn_evolutions')

# Look up combat factors for each pokemon at each stage
final = (evolutions.merge(stats, how='left', left_on='Stage_1', right_on='name')).drop('name', axis=1).rename(columns={'value':'initial_combat_power'})\
        .merge(stats, how='left', left_on='Stage_2', right_on='name').rename(columns={'value':'value_2'}).drop(['name', 'gen_introduced_y', 'pokedex_number_y'], axis=1)\
        .merge(stats, how='left', left_on='Stage_3', right_on='name').drop(['name', 'pokedex_number', 'gen_introduced'], axis=1)\
        .rename(columns={'value':'value_3', 'pokedex_number_x':'pokedex_number', 'gen_introduced_x':'gen_introduced'})

# If a pokemon doesn't evolve remove it from the dataset
final = final.dropna(subset=['Stage_2'])

# Find the combat power values relating to the pokemon's last stage
final['final_combat_power'] = np.where(final['Stage_3'].isna(), final['value_2'], final['value_3'])

# Find the percentage increase in power from the first to the last evolution stage
final['combat_power_increase'] = (final['final_combat_power'] - final['initial_combat_power']) / final['initial_combat_power']

# Sort ascending by percentage increase
final = final.sort_values(by='combat_power_increase')

# Format columns for output and output
final = final[['Stage_1', 'Stage_2', 'Stage_3', 'pokedex_number', 'gen_introduced', 'initial_combat_power', 'final_combat_power', 'combat_power_increase']]
final.to_csv('week8_output.csv')


