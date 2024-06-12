from openai import OpenAI
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_pymongo import PyMongo
from scipy import spatial
import pandas as pd
import os
import tiktoken
from app import mongo


db = mongo.db


GPT_MODEL = "gpt-3.5-turbo"
EMBEDDING_MODEL = "text-embedding-3-small"
client = OpenAI()


class AskService:

    def __init__(self):
        pass

    @staticmethod
    def strings_ranked_by_relatedness(query: str, df: pd.DataFrame, top_n: int = 100) -> tuple[
        list[str], list[str], list[float]]:
        query_embedding_response = client.embeddings.create(model=EMBEDDING_MODEL, input=query)
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

    @staticmethod
    def num_tokens(text: str, model: str = GPT_MODEL) -> int:
        encoding = tiktoken.encoding_for_model(model)
        return len(encoding.encode(text))

    @staticmethod
    def query_message(query: str, df: pd.DataFrame, model: str, token_budget: int) -> tuple[str, str]:
        strings, file_names, relatednesses = AskService.strings_ranked_by_relatedness(query, df)
        introduction = 'You are a polite and expert knowledge retrieval assistant. Use the documents provided as a knowledge base to answer questions. If there are no answers, say "I don\'t know".'
        question = f"\n\nQuestion: {query}"
        message = introduction
        for string, file_name in zip(strings, file_names):
            next_article = f'\n"""\n{string}\nFrom: {file_name}\n"""'
            if AskService.num_tokens(message + next_article + question, model=model) > token_budget:
                break
            else:
                message += next_article
        return message + question, file_names[0]

    @staticmethod
    def ask(query: str, model: str = GPT_MODEL, token_budget: int = 4096 - 500) -> tuple[str, str]:
        encoded_files = db.EmbeddedPDF.find({}, {'text_chunk': 1, 'embedded_array': 1, 'file_name': 1, 'hash_key': 1})
        decoded_df = pd.DataFrame(encoded_files)
        response_message, file_name = AskService.query_message(query, df=decoded_df, model=model,
                                                               token_budget=token_budget)
        messages = [
            {"role": "system", "content": "You answer questions Academic details"},
            {"role": "user", "content": response_message},
        ]
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0
        )
        response_message = response.choices[0].message.content
        return response_message, file_name
