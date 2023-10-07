from flask import Flask, render_template, request, jsonify
from pytube import YouTube
import openai
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

def generate_summary(url, summary_choice):
    try:
        video = YouTube(url)
        if video.length > 360: 
            return "Oops! Our AI's attention span is shorter than a sitcom episode. Keep the video under 6 minutes!"

        stream = video.streams.filter(only_audio=True).first()
        audiofilename = f"{video.title}.mp3"
        stream.download(filename=audiofilename)
        openai.api_key = os.getenv('OPENAI_API_KEY')

        audio_file= open(audiofilename, "rb")
        transcript = openai.Audio.transcribe("whisper-1", audio_file)["text"]

        summary_type = ["concise and comprehensive 50 words", "five bullet points"]

        prompt = f'''Summarize the video transcription delimited by triple quotes in {summary_type[int(summary_choice)]}.
        \n\"\"\"{transcript}\"\"\"
        '''

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ]
        )
        return f"{video.title}\n" + response['choices'][0]["message"]["content"]
    
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
        summary = generate_summary(youtube_url, summary_choice)
        cleanup_files(f"{YouTube(youtube_url).title}.mp3")
        return jsonify({"summary": summary.strip()})
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
