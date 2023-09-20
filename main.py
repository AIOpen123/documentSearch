# Import necessary packages
from llama_index import GPTVectorStoreIndex, download_loader,  VectorStoreIndex , Document, SimpleDirectoryReader, load_index_from_storage, LLMPredictor, PromptHelper
from llama_index.storage.storage_context import StorageContext
from langchain.llms import AzureOpenAI
from langchain.embeddings import OpenAIEmbeddings
from llama_index import LangchainEmbedding, ServiceContext

import requests
import json
import os
import openai

from llama_index.memory import ChatMemoryBuffer

memory = ChatMemoryBuffer.from_defaults(token_limit=1500)



os.environ['OPENAI_API_BASE'] = 'https://kgsazureai.openai.azure.com/'
os.environ['OPENAI_API_KEY'] = '21c32eb89c9a48c784fa2936c059cb6e'
os.environ['OPENAI_API_BASE'] = 'azure'
os.environ['OPENAI_API_VERSION'] = '2023-03-15-preview'

openai.api_base = 'https://kgsazureai.openai.azure.com/'
openai.api_key = '21c32eb89c9a48c784fa2936c059cb6e'
openai.api_type = 'azure'
openai.api_version = '2023-03-15-preview'

deployment_name = 'TestPoc'
gpt_model = 'gpt-35-turbo'
ada_model = "text-embedding-ada-002"

llm = AzureOpenAI(openai_api_base=openai.api_base, engine = deployment_name, model = gpt_model)
llm_predictor = LLMPredictor(llm=llm)
embedding_llm = LangchainEmbedding(OpenAIEmbeddings(model = "text-embedding-ada-002",
deployment = 'text-embedding-ada-002',
chunk_size=256, 
openai_api_key=openai.api_key,
openai_api_base=openai.api_base,
openai_api_type=openai.api_type,
openai_api_version=openai.api_version), embed_batch_size=4)

# print('Sending a test completion job')
# start_phrase = 'what is mount everest height?'
# response = openai.Completion.create(engine=deployment_name,prompt =start_phrase, max_tokens=100)
# print(response)

context_window = 3000
chunk_overlap_ratio = 0.5
max_input_size = 3000
num_output = 1
chunk_size_limit = 1000 
max_chunk_overlap = 20 
prompt_helper = PromptHelper(num_output = num_output, chunk_size_limit = chunk_size_limit, 
                             chunk_overlap_ratio = chunk_overlap_ratio, context_window = context_window)

from llama_index import set_global_service_context
service_context = ServiceContext.from_defaults(
    llm=llm,
    embed_model=embedding_llm,
    prompt_helper = prompt_helper
)
set_global_service_context(service_context)


# # UnstructuredReader = download_loader('UnstructuredReader')
# PDFReader = download_loader("PDFReader")
# dir_reader = SimpleDirectoryReader(r'documentSearch\data', file_extractor={".pdf": PDFReader()})
# documents = dir_reader.load_data()
# print(documents)

documents = SimpleDirectoryReader(r'documentSearch\data').load_data()
# print(documents)
# print("document  read successful")


index = GPTVectorStoreIndex.from_documents(documents, model = "text-embedding-ada-002", llm_predictor=llm_predictor, embed_model=embedding_llm, prompt_helper=prompt_helper)
# index = VectorStoreIndex.from_documents(documents, model = "text-embedding-ada-002", llm_predictor=llm_predictor, embed_model=embedding_llm, prompt_helper=prompt_helper)

# ip= input('Hi i am Mr.X, how can i help you?\n')
# print(ip)

# query_engine = index.as_query_engine(service_context = service_context)
# response = query_engine.query(ip)
# print(f"Response: {response} \n")

# query_engine = index.as_query_engine(streaming=True)
# streaming_response = query_engine.query(ip)
# streaming_response.print_response_stream() 

# index.storage_context.persist(persist_dir=r'documentSearch\tranied_index\index1.json')

#
#   storage_context = StorageContext.from_defaults(persist_dir=r'documentSearch\tranied_index\index1.json')
#   index = load_index_from_storage(storage_context)
#   query_engine = index.as_query_engine()
#   # index = GPTVectorStoreIndex.load_from_disk(r'documentSearch\tranied_index\index1.json')
#   while True:
#     ip= input('Hi i am Mr.X, how can i help you?')
#     response = query_engine.query(ip)

#     # response = index.query(ip)
#     print(f"Response: {response} \n")


chat_engine = index.as_chat_engine(
    chat_mode="context",
    memory=memory,
    system_prompt="You are a chatbot, able to have normal interactions",
)
# uncomment 83 for commenting this
query_engine = index.as_query_engine( similarity_top_k=5, response_mode="no_text" ) 
print("Bot: how can i assist you?")
while True:
    # ip = input("user prompt:")
    # response = chat_engine.chat(ip)
    # print(response)
    # response = query_engine.query(ip)
    # print(f"Bot: {response[0]} \n")
    
    init_response = query_engine.query("your query") 
    resp_nodes = [n.node for n in init_response.source_nodes]

# while True:
#   ip= input('Hi i am Mr.X, how can i help you?\n')
#   print(ip)
#   response = query_engine.query(ip)
#   print(f"Response: {response} \n")

# bot('documentSearch\tranied_index\index1.json')

