from decouple import config
from supabase import create_client
import logging


class SupabaseClient:
    """A client class for interacting with Supabase.

    Attributes:
        supabase_url (str): The URL of the Supabase instance.
        supabase_key (str): The API key for the Supabase instance.
        supabase (SupabaseClient): The actual Supabase client instance.
    """

    def __init__(self):
        """Initialize the Supabase client with credentials."""
        self.supabase_url = config('SUPABASE_URL')
        self.supabase_key = config('SUPABASE_KEY')
        self.supabase = create_client(self.supabase_url, self.supabase_key)

    def insert_record(self, table: str, data: dict) -> dict:
        """Insert a new record into a Supabase table.

        Parameters:
            table (str): The name of the table where the record will be inserted.
            data (dict): The data that will be inserted into the table.

        Returns:
            dict: The data that was inserted, or None if an error occurred.
        """
        try:
            response = self.supabase.table(table).insert([data]).execute()
            if getattr(response, 'error', None):
                logging.error(f"Supabase error: {response.error}")
                return None
            return response.data
        except Exception as e:
            logging.error(f"Exception occurred while inserting record into {table}: {e}")
            return None
