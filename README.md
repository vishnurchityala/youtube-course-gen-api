# YouTube Video Chatbot API

This project creates a Flask API that leverages LangChain, Google's Gemini AI, and Pinecone to store and interact with YouTube video data. Users can provide YouTube video URLs, which are then transcribed, stored, and used to interact with via chat prompts.

## Technologies Used

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-2.1.1-lightgrey?logo=flask)
![LangChain](https://img.shields.io/badge/LangChain-1.0-green?logo=langchain)
![Gemini](https://img.shields.io/badge/Google%20Gemini-1.0-yellow?logo=google)
![Pinecone](https://img.shields.io/badge/Pinecone-1.0-blue?logo=pinecone)

## Overview

The YouTube Video Chatbot API project is designed to provide an interactive way to engage with YouTube video content. By leveraging advanced AI technologies such as LangChain, Google's Gemini AI, and Pinecone, the API allows users to:

1. **Transcribe YouTube Videos**: Extract text content from YouTube videos using LangChain.
2. **Store Transcriptions**: Save the transcriptions in a Pinecone vector database for efficient retrieval and interaction.
3. **Chat with Video Data**: Use the stored transcriptions to interact and get responses based on the video content through API endpoints.

This project is ideal for educational purposes, allowing students and learners to ask questions and get detailed responses based on the content of YouTube videos. 

## Features

- **Transcribe YouTube Videos**: Convert video content into text using LangChain.
- **Store Transcriptions**: Save transcriptions in a Pinecone vector database.
- **Chat with Video Data**: Interact with the stored video data via API endpoints.

## Prerequisites

- Python 3.11
- Pinecone API Key
- Google Gemini API Key
