# Import necessary packages
from llama_index import GPTVectorStoreIndex , Document, SimpleDirectoryReader
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


#send a completion call to generate an answer
print('Sending a test completion job')
start_phrase = 'mount everest height'
response = openai.Completion.create(engine=deployment_name,prompt =start_phrase, max_tokens=10)
print(response)



# # Loading from a directory
# documents = SimpleDirectoryReader('<<path_to_document_store_directory>>').load_data()
#
# # Construct a simple vector index
# index = GPTVectorStoreIndex(documents)
#
# # Save your index to a index.json file
# index.save_to_disk('<<filename_and_path_for_index_file>>')
#
# def bot(<<filename_and_path_for_index_file>>):
#   index = GPTSimpleVectorIndex.load_from_disk('<<filename_and_path_for_index_file>>')
#   while True:
#     input = input(‘How can I help? ‘)
#     response = vIndex.query(input)
#     print(f”Response: {response} \n”)
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
