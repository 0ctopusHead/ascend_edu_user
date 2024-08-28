import concurrent.futures
import pandas as pd
import json
import os
import tiktoken
from openai import OpenAI
from scipy import spatial
from dotenv import load_dotenv


class AskServiceError(Exception):
    pass


class AskService:

    def __init__(self):
        OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
        os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
        self.client = OpenAI(api_key=OPENAI_API_KEY)

        self.GPT_MODEL = "gpt-3.5-turbo"
        self.EMBEDDING_MODEL = "text-embedding-3-small"

    def strings_ranked_by_relatedness(self, query: str, df: pd.DataFrame, top_n: int = 100) -> tuple[list[str], list[str], list[float]]:
        query_embedding_response = self.client.embeddings.create(model=self.EMBEDDING_MODEL, input=query)
        query_embedding = query_embedding_response.data[0].embedding
        strings_and_relatednesses = [
            (
                row["text_chunk"], row["file_name"],
                1 - spatial.distance.cosine(query_embedding, row["embedded_array"][0]))
            for i, row in df.iterrows()
        ]
        strings_and_relatednesses.sort(key=lambda x: x[2], reverse=True)
        strings, file_names, relatednesses = zip(*strings_and_relatednesses)
        return strings[:top_n], file_names[:top_n], relatednesses[:top_n]

    def num_tokens(self, text: str, model: str = None) -> int:
        if model is None:
            model = self.GPT_MODEL
        encoding = tiktoken.encoding_for_model(model)
        return len(encoding.encode(text))

    def query_message(self, query: str, df: pd.DataFrame, model: str = None, token_budget: int = 4096) -> tuple[str, str]:
        if model is None:
            model = self.GPT_MODEL
        strings, file_names, relatednesses = self.strings_ranked_by_relatedness(query, df)
        introduction = 'You are a polite and expert knowledge retrieval assistant. Use the documents provided as a knowledge base to answer questions. If there are no answers, say "I don\'t know".'
        question = f"\n\nQuestion: {query}"
        message = introduction
        for string, file_name in zip(strings, file_names):
            next_article = f'\n"""\n{string}\nFrom: {file_name}\n"""'
            if self.num_tokens(message + next_article + question, model=model) > token_budget:
                break
            else:
                message += next_article
        return message + question, file_names[0]

    def retrieve_json_from_openai(self, file_id):
        response = self.client.files.content(file_id)
        file_content = response.content.decode('utf-8')
        data = json.loads(file_content)
        return data

    def fetch_data_from_openai(self):
        try:
            files = self.client.files.list().data

            def fetch_file_data(file):
                return self.retrieve_json_from_openai(file. id)

            with concurrent.futures.ThreadPoolExecutor() as executor:
                all_data = list(executor.map(fetch_file_data, files))

            df = pd.DataFrame(all_data)
            normalize_df = pd.json_normalize(df[0])

            print(normalize_df.head())
            return normalize_df
        except Exception as e:
            raise AskServiceError(f"Error fetching data from OpenAI: {e}")

    def ask(self, query: str, model: str = None, token_budget: int = 4096 - 500) -> str:
        if model is None:
            model = self.GPT_MODEL
        data_df = self.fetch_data_from_openai()
        response_message, file_name = self.query_message(query, df=data_df, model=model, token_budget=token_budget)
        messages = [
            {"role": "system", "content": "You answer questions Academic details"},
            {"role": "user", "content": response_message},
        ]
        response = self.client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0
        )
        response_message = response.choices[0].message.content
        print(response_message)
        if response_message == "I don't know.":
            pass
        else:
            response_message = f"{response_message} \nReference: {file_name}"
        return response_message
