# Import necessary packages
from llama_index import GPTVectorStoreIndex , Document, SimpleDirectoryReader, load_index_from_storage
from llama_index.storage.storage_context import StorageContext
import os
import openai
import requests
import json

#os.environ['OPENAI_API_KEY'] = 'sk-YOUR-API-KEY'

openai.api_base = 'https://kgsazureai.openai.azure.com/'
openai.api_key = '21c32eb89c9a48c784fa2936c059cb6e'
openai.api_type = 'azure'
openai.api_version = '2023-03-15-preview'

deployment_name = 'TestPOC'


# #send a completion call to generate an answer
# print('Sending a test completion job')
# start_phrase = 'what is mount everest height?'
# response = openai.Completion.create(engine=deployment_name,prompt =start_phrase, max_tokens=100)
# print(response)



# Loading from a directory
documents = SimpleDirectoryReader(r'documentSearch\data').load_data()
print("document  read successful")

# Construct a simple vector index
index = GPTVectorStoreIndex.from_documents(documents)

# Save your index to a index.json file
index.storage_context.persist(persist_dir=r'documentSearch\tranied_index\index1.json')

def bot(indexPath):
  storage_context = StorageContext.from_defaults(persist_dir=r'documentSearch\tranied_index\index1.json')
  index = load_index_from_storage(storage_context)
  query_engine = index.as_query_engine()
  # index = GPTVectorStoreIndex.load_from_disk(r'documentSearch\tranied_index\index1.json')
  while True:
    ip= input('Hi i am Mr.X, how can i help you?')
    response = query_engine.query(ip)

    # response = index.query(ip)
    print(f"Response: {response} \n")

bot('documentSearch\tranied_index\index1.json')


#
# def print_hi(name):
#     # Use a breakpoint in the code line below to debug your script.
#     print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.
#
#
# # Press the green button in the gutter to run the script.
# if __name__ == '__main__':
#     print_hi('PyCharm')
#
# # See PyCharm help at https://www.jetbrains.com/help/pycharm/
