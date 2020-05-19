from decouple import config
import basilica
import pandas as pd

class BasilicaAPI():

    """
    Use API_KEY='SLOW_DEMO_KEY' if you do not have a basilica API_KEY
    """


    columns = ['from','subject', 'msg','content_type']

    def __init__(self, API_KEY=config("BASILICA_KEY"), columns=columns):
        self.API_KEY = API_KEY
        self.columns = columns

    def make_one_column(self):
        """
        This function will make a new column named 'joined_columns' from the columns given to the class.
        It will also look for a column named 'uid' to return that along with the other columns but not joined.
        """
        ids_email = self.df['uid']
        df_new = self.df[self.columns].copy()
        df_new['joined_columns'] = df_new[df_new.columns[1:]].apply(lambda x: ','.join(x.dropna().astype(str)), axis=1)
        df_new['id_email'] = ids_email
        self.df = df_new
        return None

    def embed_basilica_to_df(self):
        """
        This function will time how long basilica takes to run. For faster performance pass an API key that is functional.
        Returns the df with a column named 'embedded'.
        """
        self.make_one_column()
        from timeit import default_timer as timer
        start = timer()
        column_embedded = []
        for n in range(0, len(self.df['joined_columns']), 64):
            sentences = self.df['joined_columns'].iloc[n:n+64]
            with basilica.Connection(self.API_KEY) as c:
                embeddings = c.embed_sentences(sentences, model='email', version='default', opts={}, timeout=20)
                for e in embeddings:
                    column_embedded.append(e)
        self.df['embedded'] = column_embedded
        end = timer()
        print(end - start)
        return self.df