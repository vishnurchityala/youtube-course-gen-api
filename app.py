import os

from flask import *
from flask_cors import CORS
from langchain_text_splitters import RecursiveCharacterTextSplitter

import response_generator
import pinecone
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_pinecone.vectorstores import PineconeVectorStore

import transcriptor

app = Flask(__name__)
CORS(app)

# In-memory database
users = []

# API keys
pinecone_api_key = '6f461048-2c2b-4d7a-b560-7966e7e51fa5'
gemini_api_key = "AIzaSyBpo8Y4D-vpHmZyp0NTr8XC7q08qdc6Y0Q"

# Creating Pinecone client
pinecone_client = pinecone.Pinecone(api_key=pinecone_api_key)

# Creating Index
# index = pinecone_client.Index(host="https://youtube-course-gen-00zocgp.svc.aped-4627-b74a.pinecone.io")
index = pinecone_client.Index(name="youtube-course-gen")

# Generating Embeddings
embeddings = GoogleGenerativeAIEmbeddings(google_api_key=gemini_api_key, model="models/embedding-001")

# Text-Splitter
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=150)


def extract_video_id(url):
    # Find the position of 'v=' in the URL
    video_id_start = url.find('v=') + 2
    # The video ID is typically 11 characters long
    video_id_end = video_id_start + 11

    # Extract the video ID using slicing
    video_id = url[video_id_start:video_id_end]

    # Ensure the extracted video ID is valid
    if '&' in video_id:
        video_id = video_id.split('&')[0]

    return video_id


@app.route('/')
def home():
    response = '''Response Generation API - V1 : The Response Generation API enables the creation of formal courses 
    using custom resources provided by instructors or users. It integrates with a vector database to manage resource 
    embeddings and employs AI to generate relevant prompts and responses based on these resources.'''

    return jsonify({'response': response})


@app.route('/api/v1', methods=['GET'])
def get_api_info():
    response = '''Response Generation API - V1 : The Response Generation API enables the creation of formal courses 
    using custom resources provided by instructors or users. It integrates with a vector database to manage resource 
    embeddings and employs AI to generate relevant prompts and responses based on these resources.'''

    return jsonify({'response': response})


# Adding Chat to VideoChats asset
@app.route('/api/v1/video-chats/<int:chatId>', methods=['POST'])
def create_video_chat(chatId):
    # Chat NameSpace in Vector Database
    chat_namespace = "chat-" + str(chatId)

    # Fetching data form payload
    data = request.get_json()
    source_url = data.get("sourceUrl")

    video_id = extract_video_id(source_url)

    # Inserting Vectors in Vector Database
    vectors = []
    source_transcript = transcriptor.get_transcript_from_youtube_with_url(source_url)
    splits = text_splitter.split_text(source_transcript)
    count = 1
    for split in splits:
        embedding = embeddings.embed_query(split)
        vector_name = str(video_id) + "-" + str(count)
        vector_source = source_url
        vectors.append((vector_name, embedding, {"vector_source": vector_source, "text_chunk": split}))
        count += 1
    index.upsert(
        vectors=vectors,
        namespace=chat_namespace
    )

    response = "Added Chat with namespace : " + chat_namespace + " Vector Count : " + str(count - 1)

    return jsonify({'response': response})


@app.route('/api/v1/video-chats/<int:chatId>', methods=['DELETE'])
def delete_video_chat(chatId):
    # Namespace for the chat
    chat_namespace = "chat-" + str(chatId)

    # Initialize PineconeVectorStore
    vectorstore = PineconeVectorStore(index=index, embedding=embeddings,
                                      namespace=chat_namespace, text_key="text_chunk")

    try:
        # Delete vectors
        vectorstore.delete(delete_all=True)

        response_message = f"Deleted Chat with namespace: {chat_namespace}"

        return jsonify({"response": response_message}), 200

    except Exception as e:
        return jsonify({"Video Chat Not Found": str(e)}), 404


@app.route('/api/v1/video-chats/<int:chatId>/prompt', methods=['POST'])
def get_response_chat(chatId):
    # Fetching prompt the request body
    data = request.get_json()
    prompt = data.get('prompt')
    prompt += ". keep it less than 65535 characters."
    chat_namespace = "chat-" + str(chatId)
    # Generating Prompt
    prompt_response = response_generator.get_response(
        namespace=chat_namespace,
        prompt=prompt,
        embeddings=embeddings,
        index=index,
        gemini_api_key=gemini_api_key
    )

    return jsonify(prompt_response), 200

@app.route('/api/v1/video-chats/<int:chatId>/source',methods=['DELETE'])
def delete_vectors_from_chat(chatId):
    data = request.get_json()
    source_url = data.get("sourceUrl")
    source_id = extract_video_id(source_url)
    chat_namespace = "chat-"+str(chatId)

    ids = index.list(prefix=source_id, limit=5, namespace=chat_namespace)
    while len(ids) != 0:
        index.delete(ids=ids, namespace=chat_namespace)
        ids = index.list(prefix=source_id, limit=5, namespace=chat_namespace)

    return "Deleted Source : " +source_url


if __name__ == '__main__':
    app.run(debug=True)
