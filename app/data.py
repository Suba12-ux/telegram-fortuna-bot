import os
from huggingface_hub import InferenceClient
from dotenv import load_dotenv
from . import models
from google import genai
from google.genai import types
from gigachat import GigaChat
from ollama import chat, ChatResponse

def FORTUNES_HF(first_name):
    '''Если что то будет не понятно смотереть оф.док https://huggingface.co/docs/inference-providers/guides/structured-output '''
    try:
        load_dotenv()
        client = InferenceClient(api_key=os.getenv("HF_TOKEN"))


        # Текст сообщения от пользователя но у меня оно статичное.
        paper_text = f"""
        Title: Предсказание на день
        Name_user: {first_name}

        Сгенерируй мне предсказание на день, что меня сегодня ждет ?
        """

        

        # Преобразуйте модель Pydantic в схему JSON и оберните её в словарь
        response_format = {
            "type": "json_schema",
            "json_schema": {
                "name": "PaperAnalysis",
                "schema": PaperAnalysis.model_json_schema(),
                "strict": True,
            },
        }

        # Определите свои сообщения с помощью системного и пользовательского запросов
        # Системный запрос — это описание задачи, которую должна выполнить модель
        # Пользовательский запрос — это входные данные, которые вы хотите обработать
        messages = [
            {
                "role": "system", 
                "content": f"Нужно сгенерировать предсказание на день в 20 слов для {first_name}."
            },
            {
                "role": first_name, 
                "content": paper_text
            }
        ]

        # Создание структурированного вывода с использованием модели deepseek-ai/DeepSeek-R1
        response = client.chat_completion(
            messages=messages,
            response_format=response_format,
            model="deepseek-ai/DeepSeek-R1",
        )

        # Ответ гарантированно соответствует вашей схеме
        structured_data = response.choices[0].message.content
        analysis = json.loads(structured_data.split('</think>')[1])

        return analysis
    except Exception as error:
        return None

def FORTUNES_GG(first_name):
    try:

        #load_dotenv()
        client = genai.Client()

        paper_text = f"""
        Title: Предсказание на день
        Name_user: {first_name}

        Сгенерируй мне предсказание на день, что меня сегодня ждет ?
        """

        messages = [
            {
                "role": "system", 
                "content": f"Нужно сгенерировать предсказание на день в 20 слов для {first_name}."
            },
            {
                "role": first_name, 
                "content": paper_text
            }
        ]

        response = client.models.generate_content(
            contents=paper_text,
            config=types.GenerateContentConfig(
                thinking_config=types.ThinkingConfig(thinking_budget=0) # Disables thinking
            ),
            model="gemini-2.5-flash",
        )
        return response.text
    except Exception as error:
        return error

def FORTUNES_Giga(first_name):

    try:
        paper_text = f"""
            Title: Предсказание на день
            Name_user: {first_name}
            Context: Предскозание должно быть не больше 20 слов, и с нотками таинственности 

            Сгенерируй мне предсказание на день, что меня сегодня ждет ?
        """
        load_dotenv()      
        # Укажите ключ авторизации, полученный в личном кабинете, в интерфейсе проекта GigaChat API
        with GigaChat(credentials=os.getenv("GigaChat"), verify_ssl_certs=False) as giga:
            response = giga.chat(paper_text)
            return response.choices[0].message.content
    except Exception as error:
        return None

def FORTUNES_Ollama(first_name):
    
    try:
        #Текст сообщения от пользователя но у меня оно статичное.
        paper_text = f"""
            Сгенерируй мне одно предсказание на день, что меня сегодня ждет ?
        """ 
        message = [
                {
                    "role": "system", 
                    "content": f"""
                        Нужно сгенерировать одно предсказание на день для пользователя по имени - {first_name}.
                        Предсказание должно быть не больше 20 слов.
                        Пиши предсказание так будто говоришь с пользоваетлем.
                    """
                },
                {
                    "role": first_name, 
                    "content": paper_text
                }
            ]

        response: ChatResponse = chat(
            model='gemma3:4b', 
            messages=message,
            stream=False,
            )
        return response['message']['content'] #response.message.content
    except Exception as error:
        return None