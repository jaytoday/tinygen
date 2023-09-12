import os
import pandas as pd
from supabase_py import create_client, Client
from app.config import settings

supabase_url = settings.SUPABASE_URL
supabase_key = settings.SUPABASE_KEY
data_directory = os.path.join(os.path.dirname(__file__), "data")


class DataHelper:
    """Helper to manage test data in the database"""

    def __init__(self, supabase_url: str = supabase_url, supabase_key: str = supabase_key, data_directory: str = data_directory) -> None:
        self.client: Client = create_client(supabase_url, supabase_key)
        self.data_base_dir = data_directory

    def insert_from_csv(
        self,
        table_name: str,
        subdir_file_path: str,
        sep=",",
        quotechar='"',
        encoding="utf8",
    ):
        """Insert in a table the data read from a CSV file in a subdirectory of test data directory"""
        file_path = os.path.join(self.data_base_dir, subdir_file_path)
        df = pd.read_csv(
            filepath_or_buffer=file_path,
            sep=sep,
            quotechar=quotechar,
            encoding=encoding,
        )
        for _, row in df.iterrows():
            data = row.to_dict()
            self.client.table(table_name).insert(data)

    def delete_rows(self, table_name: str, ids: list[int]):
        self.client.table(table_name).delete().in_('id', ids).execute()

    def delete_all_rows(self, table_name: str):
        self.client.table(table_name).delete().execute()
