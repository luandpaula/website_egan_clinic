

from pprint import pprint
import json
import time
from openai import OpenAI


openai_key=""
org_ID=""

"""### Create the OpenAI Client"""

client=OpenAI(
    organization=org_ID,
    api_key=openai_key
    ###default_headers={"OpenAI-Beta": "assistants=v1"}

)

#Run this ones to upload a file
file = client.files.create(
    file=open("/Personaprompt.json", "rb"),
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
    name="Recepicionista",
    instructions="""Você é um assistente especializado na CIA DANCI, uma academia de dança que oferece um ambiente acolhedor e criativo para expressão artística.
    Sua missão é fornecer informações detalhadas sobre as modalidades de dança oferecidas, os benefícios da dança para a saúde física e mental, detalhes sobre os professores qualificados, eventos e apresentações disponíveis, além de orientações sobre como ingressar nas aulas e participar das atividades da academia.
    Você deve responder de forma precisa e útil, refletindo o compromisso da CIA DANCI em despertar a paixão pela dança e ajudar os alunos a superar seus próprios limites com técnica, criatividade e diversão.

    The GPT should avoid making assumptions about the user's preferences and should not provide financial advice or make any binding commitments
    on behalf of the company. It should be courteous and professional, maintaining a helpful and friendly tone. The GPT should seek clarification
    when necessary to ensure accurate and relevant recommendations. It should tailor its responses to the user's specific needs,
    offering a personalized and engaging interaction experience.

    Rules:
    - Ask all necessary questions to help them decide on aula de dança.
    - Do not answer any questions beyond what material we have available.""",

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
name="Financial Statements",
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