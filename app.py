from database import criar_banco, process_insert_or_update
import pandas as pd


def main():

    # criar a tabela no banco de dados
    criar_banco()

    # criar a leiutura do arquivo csv
    df_produtos_atualizar = pd.read_csv('produtos_atualizar.csv', sep=';')

    # realizar o merge entre dataframe ea tabela saida
    
    # Convertendo o DataFrame em lista de tuplas
    dados_para_inserir = list(df_produtos_atualizar.itertuples(index=False, name=None))

    process_insert_or_update(dados_para_inserir)


    
main()