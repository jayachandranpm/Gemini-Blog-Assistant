from flask import Flask, render_template, request
import os
import google.generativeai as genai

app = Flask(__name__)

# Set your API key
os.environ['GOOGLE_API_KEY'] = "your_api_key"

# Configure GenerativeAI library with the API key
genai.configure(api_key=os.environ['GOOGLE_API_KEY'])

@app.route('/', methods=['GET', 'POST'])
def homepage():
    if request.method == 'POST':
        topics = request.form['topics']
        total_words = int(request.form['content_length'])
        language = request.form.get('language', 'en')
        words_generated = 0
        generated_content = ""

        if not topics:
            return render_template('index.html', warning="Please enter a topic.")
        else:
            model = genai.GenerativeModel('gemini-pro')
            while words_generated < total_words:
                # Calculate remaining words to generate
                remaining_words = total_words - words_generated
                # Limit the request to maximum 1000 words
                words_to_generate = min(remaining_words, 1000)
                prompt = f"Generate content related to {topics} with a length of {words_to_generate} words in {language} language."
                response = model.generate_content(prompt)
                generated_content += response.parts[0].text
                words_generated += words_to_generate

            return render_template('index.html', topics=topics, content_length=total_words, language=language, generated_content=generated_content)

    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
