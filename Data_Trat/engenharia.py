import pandas as pd
import numpy as np

class Engenharia:

    def __init__(self):
        pass

    

    def desempenho(self,df_i,n,nulos=True):

        if nulos == False:
            
            cols_keep = ['torneio','Corner kicks_home','Blocked shots_home','Goalkeeper saves_away','Ground duels_home','Big chances_away',
                    'Interceptions_home','Ground duels_away','Aerial duels_home','Free kicks_away','Crosses_home','Total saves_home',
                    'Duels_home','Shots on target_away','Clearances_home','Passes_away','time_visitante','Crosses_away','Hit woodwork_home',
                    'temporada','Tackles_home','Big chances_home','Fouls_home','Aerial duels_away','Tackles won_home',
                    'Long balls_home','Passes_home','Offsides_home', 'Total shots_away','Yellow cards_home','Dribbles_away','Shots inside box_away','Blocked shots_away',
                    'Goal kicks_away','Shots outside box_home','Long balls_away','Shots inside box_home','Shots off target_away','Hit woodwork_away','Ball possession_away',
                    'Shots outside box_away','Tackles won_away','Accurate passes_home','Tackles_away','ano','Free kicks_home','Interceptions_away','Shots on target_home',
                    'Throw-ins_home', 'Yellow cards_away', 'Total shots_home','Shots off target_home','Ball possession_home', 'gols_casa','Total saves_away','odd_draw','data',
                    'Fouled in final third_home','Total tackles_away','Dribbles_home','Fouls_away','Goalkeeper saves_home','gols_visitante','Final third entries_home',
                    'Final third entries_away', 'Dispossessed_home','Throw-ins_away','Goal kicks_home','Corner kicks_away','odd_away_win','Clearances_away','pais',
                    'Fouled in final third_away','Dispossessed_away','Duels_away','Offsides_away','odd_home_win','Accurate passes_away','time_casa','Total tackles_home']

            df_i = df_i[df_i['data'].dt.year >= 2018]
            df_i = df_i[df_i['temporada'].str.contains('17') == False]
            df_i = df_i[cols_keep]

        # Ajuste na nomenclatura da coluns de time para permitir script mais otimizado
        df = df_i.copy()
        df = df.rename(columns={'time_casa':'home_team',
                                'time_visitante':'away_team',
                                'gols_casa':'gols_home',
                                'gols_visitante':'gols_away'
                                })

        # eliminando as colunas de odds
        # df = df.drop(columns = ['odd_home_win', 'odd_draw', 'odd_away_win'])

        # Listando os teams e posicionando em uma única geral
        list_teams_home = list(df['home_team'].unique())
        list_teams_away = list(df['away_team'].unique())

        list_teams = list_teams_home + list_teams_away
        list_teams = list(set(list_teams))

        # Lista para salvar os desempenhos
        list_df_desempenho = []

        # Consolidando o Loop
        for team in list_teams:

            df_home = df.copy()
            df_away = df.copy()

            df_home = df_home[df_home['home_team'] == team]
            cols_home = ['data','ano'] + list(set(df_home.columns[df_home.columns.str.contains('home') == True]))
            df_home = df_home[cols_home]
            new_col_home = df_home.columns.str.replace('_home','')
            new_col_home = new_col_home.str.replace('home_','')
            df_home.columns = new_col_home

            df_away = df_away[df_away['away_team'] == team]
            cols_away = ['data', 'ano'] + list(set(df_away.columns[df_away.columns.str.contains('away') == True]))
            df_away = df_away[cols_away]
            new_col_away = df_away.columns.str.replace('_away','')
            new_col_away = new_col_away.str.replace('away_','')
            df_away.columns = new_col_away

            df_all = pd.concat([df_away,df_home])
            df_all = df_all.sort_values(by='data')

            # encontrando o desempenho por ano/temporadas
            n_partidas = n
            list_temporadas = df_all['ano'].unique()

            for temporada in list_temporadas:

                df_temporada = df_all.copy()
                df_temporada = df_temporada.reset_index(drop=True)
                df_temporada = df_temporada[df_temporada['ano'] == temporada]

                list_colunas = df_temporada.columns

                # deslocando 
                for col in list_colunas:

                    if (col != 'data') and (col != 'ano') and (col != 'team'):

                        df_temporada[col] = df_temporada[col].shift(1)
                        df_temporada = df_temporada.loc[1:]

                        if nulos == False:
                            # obs: Pode haver nulos no periodo de 5 partidas em determinadas colunas, portanto serão
                            # preenchidos com base na mediana da coluna, pois é menos influenciada por outlieres
                            mediana = df_temporada[col].median()
                            df_temporada[col] = df_temporada[col].fillna(mediana)

                        df_temporada[col] = df_temporada[col].rolling(n_partidas).mean()

                list_df_desempenho.append(df_temporada)


        df_desempenho = pd.concat(list_df_desempenho)

        if nulos == False:
            cols_na = list(set(df_desempenho.columns) - set(['data','team']))
            df_desempenho = df_desempenho.dropna(subset=cols_na) # Não remover os Nulos - Everton

        df_desempenho = df_desempenho.sort_values(by='data')

        return df_desempenho
        # return df
    


    def match_performance(self,df,df_desempenho,nulos=True):

        cols_perf = ['data','pais','temporada','ano','torneio','home_team','away_team','odd_home_win','odd_draw','odd_away_win','result']
        df = df.rename(columns = {'time_casa':'home_team','time_visitante':'away_team'})
        df = df[cols_perf]


        # Merge home
        df_desempenho_home = df_desempenho.copy()
        df_desempenho_home = df_desempenho_home.drop(columns = df_desempenho_home.columns[df_desempenho_home.columns.str.contains('odd')])
        df_desempenho_home = df_desempenho_home.drop(columns='ano')
        for col in df_desempenho_home.columns:

            if (col != 'data') and (col != 'ano') and (col.find('odd') < 0):

                df_desempenho_home = df_desempenho_home.rename(columns={f'{col}':f'home_{col}'})

        df = pd.merge(df,df_desempenho_home,how='left',on=['data','home_team'])


        # Merge away
        df_desempenho_away = df_desempenho.copy()
        df_desempenho_away = df_desempenho_away.drop(columns = df_desempenho_away.columns[df_desempenho_away.columns.str.contains('odd')])
        df_desempenho_away = df_desempenho_away.drop(columns='ano')
        for col in df_desempenho_away.columns:

            if (col != 'data') and (col != 'ano') and (col.find('odd') < 0):

                df_desempenho_away = df_desempenho_away.rename(columns={f'{col}':f'away_{col}'})

        df_match_performance = pd.merge(df,df_desempenho_away,how='left',on=['data','away_team'])

        if nulos == False:
            df_match_performance = df_match_performance.dropna()

        return df_match_performance
            

    def ratio(self,df,df_desempenho,nulos=True):

        df_ratio = df.copy()
        list_cols_ratio = df_desempenho.select_dtypes(include=['float', 'int']).columns.to_frame().sort_values(by=0)[0].unique()

        list_new_cols = []

        for col in list_cols_ratio:
            
            if col.find('odd') < 0:
                
                df_ratio[f'{col}_ratio'] = np.where((df_ratio[f'home_{col}'] == 0) & (df_ratio[f'away_{col}'] == 0), 1, #se ambos os times possuem 0, a performance é igual, portanto razaão precisa ser 1
                                                    np.where(df_ratio[f'away_{col}'] == 0,np.nan, # vazio pq o valor daria uma inconcistencia matemática (tratará a seguir)
                                                            df_ratio[f'home_{col}'] / df_ratio[f'away_{col}']))


                df_ratio = df_ratio.drop(columns=[f'home_{col}',f'away_{col}'])
                
                list_new_cols.append(f'{col}_ratio')


        # Corrigindo regra de negócio quando col_away é igual a zero
        # 1. Trata-se de uma inconscistência matemática 
        # 2. Por mais que utilize um valor proximo de zero, o resultado tende ao infinito tornando-o um outlier extremamente grande
        # 3. A solução é aproximar o resultado ao maior valor da base, estipulando assim um teto
        if nulos == False:
            for col in list_new_cols:

                max_col = df_ratio[col].max()
                df_ratio[col] = df_ratio[col].fillna(max_col)


        return df_ratio