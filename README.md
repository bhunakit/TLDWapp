# TL;DW (Too Long Didn't Watch) (personal project to check out OpenAI api)

# YouTube Audio Summary App

The YouTube Audio Summary App is a Flask-based web application that allows you to generate text summaries from audio content in YouTube videos using OpenAI's GPT-3.5 Turbo model.

## Features

- Generate concise and comprehensive 50-word summaries or summaries in five bullet points.
- Translate the generated summaries into different languages.
- User-friendly web interface for easy interaction.
- Handles YouTube URLs with audio content (video duration should be no longer than 5 minutes).
- Automatic file cleanup to maintain a clean working directory.

## Prerequisites

Before running the app, ensure you have the following installed:

- Python (3.6+)
- Flask
- pytube
- openai
- You'll also need an OpenAI API key, which you can obtain from the OpenAI website. (put it in .env file in your root directory)


