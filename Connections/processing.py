import time
import pandas as pd
import numpy as np
# from Connections.connections import Connection
from Connections.selenium_method import Connection



class Processing:
    
    def __init__(self, esporte=None, data=None):
        
        self.esporte = esporte
        self.data = data

        pass



    def confere_dict(self,x,dict_):

        try: 
            result = dict_[x]
        except:
            result = [np.nan]

        return result



    def get_matches(self,dict_torneio):

        try: 
            events = Connection().get_events(self.data)

            size_events = len(events)

            list_matches = []
            list_df_statistics = []

            for i in range(size_events):

                try:
                    status = events[i]['status']['type']
                    pais = events[i]['tournament']['category']['name']
                    torneio = events[i]['tournament']['name']

                    torneios_to_get = self.confere_dict(pais,dict_torneio)

                    if (status == 'finished') and (torneio in torneios_to_get):
                        
                        id = events[i]['id']
                        pais = events[i]['tournament']['category']['name']
                        torneio = events[i]['tournament']['name']
                        #esporte = events[i]['tournament']['category']['sport']['name']
                        ano = events[i]['season']['year']
                        temporada = events[i]['season']['name']
                        time_casa = events[i]['homeTeam']['name']
                        time_visitante = events[i]['awayTeam']['name']
                        gols_casa = events[i]['homeScore']['normaltime']
                        gols_visitante = events[i]['awayScore']['normaltime']
                        #rodada = events[i]['roundInfo']['round']

                        # Obtendo as odds
                        try:
                            odd_home_win,odd_draw,odd_away_win = self.get_full_time_odds(id)
                        except:
                            odd_home_win = np.nan
                            odd_draw = np.nan
                            odd_away_win = np.nan


                        #list_matches.append([id, self.data, pais, torneio, esporte, temporada, rodada, status, time_casa, time_visitante, gols_casa, gols_visitante])
                        list_matches.append([id, self.data, pais, torneio, time_casa, time_visitante, gols_casa, gols_visitante, odd_home_win, odd_draw, odd_away_win,temporada,ano])

                        try:
                            statistic = self.get_statistics(id)
                            statistic['id'] = id
                            list_df_statistics.append(statistic)
                            # time.sleep(1) # sleep para não sobrecarregar o banco do sofascore
                        except Exception as e:
                            print(f'id: {id}\nErro: {e}\n')


                except Exception as e:
                    
                    # print(f'id: {id}\nErro: {e}\n')
                    print(f'Erro: {e}\n')
                    pass

            if len(list_matches) > 0:

                df = pd.DataFrame(list_matches)
                df.columns = ['id', 'data', 'pais', 'torneio', 'time_casa', 'time_visitante', 'gols_casa', 'gols_visitante', 'odd_home_win', 'odd_draw', 'odd_away_win', 'temporada', 'ano']

                if len(list_df_statistics) > 0:

                    df_statistics = pd.concat(list_df_statistics)

                    return df, df_statistics
                
                else:
                    return df, pd.DataFrame()

            
            else:
                return pd.DataFrame(), pd.DataFrame()
            
        except:
            return pd.DataFrame(), pd.DataFrame()




    def get_full_time_odds(self, match_id):

        markets = Connection().get_markets(match_id)
        
        odd_escolha1_init = markets[0]['choices'][0]['initialFractionalValue']
        odd_escolhaX_init = markets[0]['choices'][1]['initialFractionalValue']
        odd_escolha2_init = markets[0]['choices'][2]['initialFractionalValue']

        return odd_escolha1_init, odd_escolhaX_init, odd_escolha2_init
    


    def get_statistics(self, match_id):

        statistics = Connection().get_statistics(match_id)
        full_time_statistics = statistics[0]
        full_time_statistics

        dict_statistics = {}

        size_stat_i = len(full_time_statistics['groups'])

        for i in range(size_stat_i):

            size_items = len(full_time_statistics['groups'][i]['statisticsItems'])

            for j in range(size_items):

                full_time_statistics['groups'][i]['statisticsItems'][j]

                name = full_time_statistics['groups'][i]['statisticsItems'][j]['name']
                home_value = full_time_statistics['groups'][i]['statisticsItems'][j]['home']
                away_value = full_time_statistics['groups'][i]['statisticsItems'][j]['away']

                dict_statistics[f'{name}_home'] = home_value
                dict_statistics[f'{name}_away'] = away_value

        df = pd.DataFrame(dict_statistics.values()).T
        df.columns = dict_statistics.keys()

        return df
    

    def get_season(self,match_id):

        events = Connection().get_season(match_id)

        temporada = events['season']['name']
        ano = events['season']['year']

        list_matches = []
        list_matches.append([match_id, temporada, ano])

        df = pd.DataFrame(list_matches)
        df.columns = ['id', 'temporada', 'ano']

        return df