from openai import OpenAI

from src.utils.logger import logging
from src.config.app_config import CryptoConfig as cc

def get_client(api_key, url):
    logging.info('Getting client ...')
    return OpenAI(
        api_key=api_key,
        base_url=url
    )

def get_chat_response(client, model_name, messages):
    logging.info('Getting chat response ...')
    input_messages = []
    for message in messages:
        input_messages.append({'role': message['role'], 'content': message['content']})
    
    response = client.chat.completions.create(
        model=model_name,
        messages=input_messages,
        temperature=cc.temperature,
        top_p=cc.top_p,
        max_tokens=cc.max_tokens
    ).choices[0].message.content

    return response