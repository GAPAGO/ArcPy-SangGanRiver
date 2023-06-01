import os
import pandas as pd
from tqdm import tqdm

input_folder = r"D:\ShenZeyu20230308\ArcPy_SangGanHe\attribute table"
output_folder = r'D:\ShenZeyu20230308\ArcPy_SangGanHe\calculated table'


def calculate(df: pd.DataFrame) -> pd.DataFrame:
    result = pd.DataFrame()
    # 读取唯一 cell 编号
    result['Cell_Index'] = df['Cell_Index'].unique()
    # 对四种草本植被循环
    for herb in ['HERB01', 'HERB02', 'HERB03', 'HERB04']:
        result[herb] = df[df['Assigned_c'] == herb]['Shape_Area'].sum() / df['Area'].iloc[0]
    result.fillna(0, inplace=True)
    return result


for filename in tqdm(os.listdir(input_folder), colour='green'):
    if filename.endswith('.csv'):
        file_path = os.path.join(input_folder, filename)
        df = pd.read_csv(file_path)
        # if 0 in df.groupby('Cell_Index').groups:
        #     print(df.groupby('Cell_Index').get_group(0))

        result = df.groupby('Cell_Index').apply(calculate).reset_index(drop=True)

        output_file_path = os.path.join(output_folder, filename)
        result.to_csv(output_file_path, index=False)
