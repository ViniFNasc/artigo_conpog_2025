## PREDIÇÃO DE VITÓRIAS DO TIME MANDANTE EM PARTIDAS DE FUTEBOL 

### MOTIVAÇÃO:
Este trabalho foi desenvolvido e submetido ao CONPOG 2025 como parte dos critérios para a conclusão do curso de Pós-Graduação em Ciência de Dados, ministrado pelo Instituto Federal de São Paulo – Campus Campinas.

### RESUMO:
O presente trabalho desenvolve um modelo de Aprendizado de Máquina (Machine Learning) para prever resultados de partidas de futebol, com foco na vitória do time da casa, a fim de apoiar decisões em apostas esportivas. Utilizando dados extraídos da plataforma Sofascore entre 2018 e 2025, foram considerados os principais campeonatos 
mundiais. A base foi construída a partir do desempenho médio das cinco partidas mais recentes de cada time, e a razão entre os desempenhos do mandante e visitante foi utilizada como input nos modelos. Foram avaliados algoritmos como árvore de decisão, random forest, XGBoost e LightGBM, com e sem otimizações. Os modelos LightGBM e XGBoost com Grid Search cv apresentaram as maiores precisões, superando 60%. O LightGBM com corte de probabilidade em 0,5 obteve o maior lucro final, validando sua eficácia para recomendações mais assertivas, mesmo com menor frequência de apostas. Os resultados indicam que a aplicação de técnicas de aprendizado de máquina pode contribuir para decisões mais racionais no mercado de apostas.
