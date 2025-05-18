import pandas as pd
import datetime
import time
from Connections.processing import Processing

def main():

    ti = time.time()

    # esporte
    esporte = 'football'

    # torneios
    dict_torneios = {
        'England':['Premier League','Championship'],
        'Italy':['Serie A'],
        'Germany':['Bundesliga'],
        'Spain':['LaLiga'],
        'Brazil':['Brasileirão Betano'],
        'Belgium':['First Division A'],
        'USA':['MLS'],
        'Argentina':['Liga Profesional'],
        'France':['Ligue 1']
    }



    hoje = datetime.date.today()
    ontem = hoje - datetime.timedelta(days=1)
    
    data_f = ontem

    size = 1

    list_datas = []
    for i in range(int(size)):

        data_i = data_f - datetime.timedelta(days=i)
        list_datas.append(data_i)

    print(list_datas)

    # Carregando bases antigas
    df_antigo = pd.read_csv('base_de_dados/historico_odds.csv')
    df_stat_antigo = pd.read_csv('base_de_dados/historico_statistic.csv')

    list_df = []
    list_df_stat = []

    for data in list_datas:

        print(f'Coletando os dados de {data}')

        df,df_stat = Processing(esporte,data).get_matches(dict_torneios)

        if df.empty == False:

            list_df.append(df)
            list_df_stat.append(df_stat)

    
    print('Concatenando os dados e Salvando')

    list_df.append(df_antigo)
    list_df_stat.append(df_stat_antigo)

    df_concat = pd.concat(list_df)
    df_stat_concat = pd.concat(list_df_stat)

    # Salvando os resultados
    df_concat.to_csv('base_de_dados/historico_odds.csv',index=False)
    df_stat_concat.to_csv('base_de_dados/historico_statistic.csv',index=False)


    tf = time.time()
    tt = (tf - ti)/60
    print(f'Tempo total de execução: {tt:.2f} minutos!')

main()



