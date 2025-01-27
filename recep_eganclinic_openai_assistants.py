from pprint import pprint
from dotenv import load_dotenv
import os
import json
import time
from openai import OpenAI
# Carrega as variáveis do arquivo .env
load_dotenv()

openai_key=os.environ.get("openai_key")
org_ID=os.environ.get("org_ID")

"""### Create the OpenAI Client"""

client=OpenAI(
    organization=org_ID,
    api_key=openai_key
)

#Run this ones to upload a file
file = client.files.create(
    file=open("Personaprompt.json", "rb"),
    purpose="assistants"
)

#Call this to get the list of all uploaded files
file_list = client.files.list()
print(file_list)

#Grab the ID of the TV Manual uploaded earlier
file_id = file_list.data[0].id
print(file_id)

""" Create the assistant and grant access to the files"""

# Lista inicial de ferramentas
tools = []

# Ferramenta para reservas personalizadas

tools.append({"type": "file_search"})
tools.append({"type": "code_interpreter"})

#call this once to create the assistant
assistant = client.beta.assistants.create(
    name="Recepcionista Egan Clinic",
    instructions="""Você é um assistente especializado na Egan Clinic, uma clínica odontológica que oferece um ambiente acolhedor e profissional para cuidados com a saúde bucal.    
    Sua missão é fornecer informações detalhadas sobre os serviços oferecidos, como clareamento dental, ortodontia, implantes, próteses, tratamentos de canal e estética odontológica.   
    Além disso, você deve orientar sobre como agendar consultas e participar de tratamentos específicos, garantindo um atendimento humanizado e de alta qualidade.
        
    Regras:    
    - Pergunte todas as informações necessárias para ajudar os pacientes a escolherem o serviço odontológico adequado.
    - Não responda perguntas além do material disponível.
    - Sempre mantenha um tom acolhedor, profissional e informativo.""",


    model = "gpt-3.5-turbo-1106",
    tools=tools,
    tool_resources= {
      "code_interpreter": {
        "file_ids": [file_id]
      }
    }
)

# Impressão para depuração
print(assistant)

# Create a vector store caled "Financial Statements"
print(dir(client.beta.vector_stores))

vector_store = client.beta.vector_stores.create(
name="Dental Services",
file_ids=[file_id]
)
assistant = client.beta.assistants.update(
assistant_id=assistant.id,
tool_resources={"file_search": {"vector_store_ids": [vector_store.id]}},
)

"""[Your Assistants Can be found here on the OpenAI Website]"""

#to retrieve all your defined assistants
my_assistants = client.beta.assistants.list(
    order="desc",
    limit = "20"
)

pprint(my_assistants.data)