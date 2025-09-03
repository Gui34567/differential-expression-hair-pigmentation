import pandas as pd
import numpy as np
import io

def preprocess_geo_data(file_path):
    """
    Lê e pré-processa um arquivo de matriz de expressão do GEO,
    separando a matriz de expressão dos metadados.

    Args:
        file_path (str): O caminho para o arquivo .txt do GEO.

    Returns:
        tuple: Uma tupla contendo um DataFrame de expressão tratada e o dicionário de títulos de amostra.
    """
    # 1. Ler o arquivo para separar os metadados da matriz de dados.
    meta_info_raw = []
    data_lines = []
    found_data_start = False

    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            if line.startswith("!"):
                meta_info_raw.append(line.strip())
            else:
                if not found_data_start:
                    data_lines.append(line.strip())
                    found_data_start = True
                else:
                    data_lines.append(line.strip())

    # 2. Processar os metadados para encontrar os títulos das amostras
    sample_titles = {}
    for line in meta_info_raw:
        if line.startswith('!Sample_title'):
            titles = line.strip().split('\t')[1:]
            gsm_codes = [f"GSM{591265 + (i * 2)}" for i in range(len(titles))]
            sample_titles = dict(zip(gsm_codes, [t.replace('"', '') for t in titles]))
            break

    # 3. Usar StringIO para ler a matriz de dados como se fosse um arquivo
    data_matrix_string = "\n".join(data_lines)
    df_expression = pd.read_csv(io.StringIO(data_matrix_string), sep="\t", index_col=0)

    # 4. Limpar e organizar o DataFrame de expressão
    if not df_expression.empty and df_expression.index[-1] == '!series_matrix_table_end':
        df_expression = df_expression.iloc[:-1]

    df_expression = df_expression.T
    df_expression.index.name = "Sample_ID"

    # 5. Criar a coluna de grupos (Pigmented/Non-pigmented)
    def get_group(title):
        if pd.isna(title) or title == 'N/A':
            return 'irrelevant'
        if 'PB' in title or 'PU' in title:
            return 'pigmented'
        elif 'NB' in title or 'NU' in title:
            return 'non_pigmented'
        return 'irrelevant'

    df_expression['Sample_title'] = df_expression.index.map(lambda x: sample_titles.get(x, 'N/A'))
    df_expression['Grupo'] = df_expression['Sample_title'].apply(get_group)
    df_expression = df_expression[df_expression['Grupo'] != 'irrelevant'].drop(columns=['Sample_title'])

    # 6. Normalizar os dados CORRETAMENTE - SEM o clipping problemático
    numeric_cols = df_expression.select_dtypes(include=np.number).columns
    
    # Remover valores negativos ou zero antes do log2
    # Adicionar pseudocount para evitar log(0)
    pseudocount = 1
    df_expression[numeric_cols] = df_expression[numeric_cols].clip(lower=0.1)  # Valor mínimo de 0.1
    df_expression[numeric_cols] = np.log2(df_expression[numeric_cols] + pseudocount)
    
    return df_expression, sample_titles

def load_raw_data(file_path):
    """
    Carrega os dados brutos sem normalização para debug
    """
    meta_info_raw = []
    data_lines = []
    found_data_start = False

    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            if line.startswith("!"):
                meta_info_raw.append(line.strip())
            else:
                if not found_data_start:
                    data_lines.append(line.strip())
                    found_data_start = True
                else:
                    data_lines.append(line.strip())

    # Processar metadados
    sample_titles = {}
    for line in meta_info_raw:
        if line.startswith('!Sample_title'):
            titles = line.strip().split('\t')[1:]
            gsm_codes = [f"GSM{591265 + (i * 2)}" for i in range(len(titles))]
            sample_titles = dict(zip(gsm_codes, [t.replace('"', '') for t in titles]))
            break

    # Ler matriz de dados
    data_matrix_string = "\n".join(data_lines)
    df_expression = pd.read_csv(io.StringIO(data_matrix_string), sep="\t", index_col=0)

    if not df_expression.empty and df_expression.index[-1] == '!series_matrix_table_end':
        df_expression = df_expression.iloc[:-1]

    df_expression = df_expression.T
    df_expression.index.name = "Sample_ID"

    # Criar coluna de grupos
    def get_group(title):
        if pd.isna(title) or title == 'N/A':
            return 'irrelevant'
        if 'PB' in title or 'PU' in title:
            return 'pigmented'
        elif 'NB' in title or 'NU' in title:
            return 'non_pigmented'
        return 'irrelevant'

    df_expression['Sample_title'] = df_expression.index.map(lambda x: sample_titles.get(x, 'N/A'))
    df_expression['Grupo'] = df_expression['Sample_title'].apply(get_group)
    df_expression = df_expression[df_expression['Grupo'] != 'irrelevant'].drop(columns=['Sample_title'])
    
    return df_expression

