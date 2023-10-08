from flask import Flask, render_template, request, jsonify
from pytube import YouTube
import openai
import os
import time
from dotenv import load_dotenv
import re

load_dotenv()

app = Flask(__name__)

def is_valid_youtube_url(url):
    if re.match(r'^https?://(www\.)?youtube\.com/', url) or re.match(r'^https?://(www\.)?youtu\.be/', url):
        return True
    else:
        return False

def generate_summary(url, summary_choice, lang):
    if not is_valid_youtube_url(url):
        return "Not URL"

    try:
        video = YouTube(url)
        
        if video.length > 360: 
            return "Oops! Our AI's attention span is shorter than a sitcom episode. Keep the video under 6 minutes!"

        stream = video.streams.filter(only_audio=True).first()
        audiofilename = f"/tmp/{video.title}.mpeg"
        stream.download(filename=audiofilename)
        openai.api_key = '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'

        audio_file= open(audiofilename, "rb")
        transcript = openai.Audio.transcribe("whisper-1", audio_file)["text"]

        summary_type = ["concise and comprehensive 50 words", "five bullet points (each bullet point no more than 20 words)"]
        lang_type = {"en": "English", "fr": "French", "es": "Spanish", "th": "Thai", "ja": "Japanese"}

        prompt = f'''Summarize the video transcription delimited by triple quotes in {summary_type[int(summary_choice)]} in {lang_type[lang]}.
        \n\"\"\"{transcript}\"\"\"\n\n

        Only output the content
        '''

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ]
        )
        return f"Summarization of {video.title}<br>" + response['choices'][0]["message"]["content"]
    
    except Exception as e:
        return f"Error: {str(e)}"


def cleanup_files(audiofilename):
    try:
        if os.path.exists(audiofilename):
            os.remove(audiofilename)
    except Exception as e:
        print(f"Error cleaning up files: {str(e)}")


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        youtube_url = request.form.get("youtube_url")
        summary_choice = request.form.get("summary_choice")
        translation_language = request.form.get("translation_language")
        summary = generate_summary(youtube_url, summary_choice, translation_language)
        cleanup_files(f"/tmp/{YouTube(youtube_url).title}.mpeg")
        return jsonify({"summary": summary.strip()})
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
