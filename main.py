# Import necessary packages
from llama_index import GPTVectorStoreIndex , Document, SimpleDirectoryReader, load_index_from_storage, LLMPredictor, PromptHelper
from llama_index.storage.storage_context import StorageContext
from langchain.llms import AzureOpenAI
from langchain.embeddings import OpenAIEmbeddings
from llama_index import LangchainEmbedding, ServiceContext

import requests
import json
import os
import openai

os.environ['OPENAI_API_BASE'] = 'https://kgsazureai.openai.azure.com/'
os.environ['OPENAI_API_KEY'] = '21c32eb89c9a48c784fa2936c059cb6e'
os.environ['OPENAI_API_BASE'] = 'azure'
os.environ['OPENAI_API_VERSION'] = '2023-03-15-preview'

openai.api_base = 'https://kgsazureai.openai.azure.com/'
openai.api_key = '21c32eb89c9a48c784fa2936c059cb6e'
openai.api_type = 'azure'
openai.api_version = '2023-03-15-preview'

deployment_name = 'TestPOC'

llm = AzureOpenAI(engine = deployment_name, model = "text-embadding-ada-002")
llm_predictor = LLMPredictor(llm=llm)
embedding_llm = LangchainEmbedding(OpenAIEmbeddings(model = "text-embadding-ada-002",
deployment = 'TestPOC',
openai_api_key=openai.api_key,
openai_api_base=openai.api_base,
openai_api_type=openai.api_type,
openai_api_version=openai.api_version))
# #send a completion call to generate an answer
# print('Sending a test completion job')
# start_phrase = 'what is mount everest height?'
# response = openai.Completion.create(engine=deployment_name,prompt =start_phrase, max_tokens=100)
# print(response)
# Define prompt helper
max_input_size = 3000
num_output = 256
chunk_size_limit = 1000 # token window size per document
max_chunk_overlap = 20 # overlap for each token fragment
prompt_helper = PromptHelper()

from llama_index import set_global_service_context
service_context = ServiceContext.from_defaults(
    llm=llm,
    embed_model=embedding_llm,
)
set_global_service_context(service_context)

# Loading from a directory
documents = SimpleDirectoryReader(r'documentSearch\data').load_data()
print("document  read successful")

# Construct a simple vector index
index = GPTVectorStoreIndex.from_documents(documents, model = "TestPOC", llm_predictor=llm_predictor, embed_model=embedding_llm, prompt_helper=prompt_helper)
query_engine = index.as_query_engine()
ip= input('Hi i am Mr.X, how can i help you?\n')
print(ip)
response = query_engine.query(ip)
print(f"Response: {response} \n")

# # Save your index to a index.json file
# index.storage_context.persist(persist_dir=r'documentSearch\tranied_index\index1.json')

# def bot(indexPath):
#   storage_context = StorageContext.from_defaults(persist_dir=r'documentSearch\tranied_index\index1.json')
#   index = load_index_from_storage(storage_context)
#   query_engine = index.as_query_engine()
#   # index = GPTVectorStoreIndex.load_from_disk(r'documentSearch\tranied_index\index1.json')
#   while True:
#     ip= input('Hi i am Mr.X, how can i help you?')
#     response = query_engine.query(ip)

#     # response = index.query(ip)
#     print(f"Response: {response} \n")

# bot('documentSearch\tranied_index\index1.json')


# #
# # def print_hi(name):
# #     # Use a breakpoint in the code line below to debug your script.
# #     print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.
# #
# #
# # # Press the green button in the gutter to run the script.
# # if __name__ == '__main__':
# #     print_hi('PyCharm')
# #
# # # See PyCharm help at https://www.jetbrains.com/help/pycharm/
