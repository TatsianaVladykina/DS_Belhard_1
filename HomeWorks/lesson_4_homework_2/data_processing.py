import pandas as pd

class Data_processing:

    @staticmethod
    def DevideToColumns(file_path, sep='\t'):
        df = pd.read_csv(file_path, sep=sep)
        return df

    @staticmethod
    def EmptyData(dataset):
        column_names = dataset.columns.tolist()
        for column in column_names:
            nulls = dataset[column].isnull().sum()
            print(f'в столбце {column} - {nulls} пустых значений')

    @staticmethod
    def RemoveRowsWithMissingValues(dataset):
        return dataset.dropna(inplace=True)
