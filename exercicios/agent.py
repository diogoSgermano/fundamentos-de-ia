import os
from dotenv import load_dotenv, find_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from langchain_core.exceptions import LangChainException

env_path = find_dotenv()
load_dotenv(env_path)

if not os.getenv("GROQ_API_KEY"):
    print(f"DEBUG: Arquivo .env localizado em: '{env_path}'")
    print("Erro: A variável de ambiente GROQ_API_KEY não foi definida.")
    print("Verifique se o arquivo .env existe e não está nomeado como .env.txt.")
    exit()

chat = ChatGroq(model="llama-3.3-70b-versatile")

template = ChatPromptTemplate.from_messages([
    ("system", "Você é um assistente que sempre responde com piadas"),
    ("user", "Explique {assuntoBiologia} de forma {tipoExplicacao}")
])

output_parser = StrOutputParser()

chain = template | chat | output_parser

try:
    resposta = chain.invoke({
        "assuntoBiologia": "Citologia",
        "tipoExplicacao": "resumido"
    })

    print(resposta)
except LangChainException as e:
    print(f"Ocorreu um erro ao invocar a chain: {e}")
except Exception as e:
    print(f"Ocorreu um erro inesperado: {e}")