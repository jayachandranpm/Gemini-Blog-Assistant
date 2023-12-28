from flask import Flask, render_template, request
import os
import google.generativeai as genai

app = Flask(__name__)

# Set your API key
os.environ['GOOGLE_API_KEY'] = "AIzaSyAXdqL57ifjEXUyrrDsyQ8C3sU4VfOzcIg"

# Configure GenerativeAI library with the API key
genai.configure(api_key=os.environ['GOOGLE_API_KEY'])

@app.route('/', methods=['GET', 'POST'])
def homepage():
    if request.method == 'POST':
        topics = request.form['topics']
        content_length = int(request.form['content_length'])
        language = request.form.get('language', 'en')

        if not topics:
            return render_template('index.html', warning="Please enter a topic.")
        else:
            # Generate content using the Gemini LLM API
            model = genai.GenerativeModel('gemini-pro')
            prompt = f"Generate content related to {topics} with a length of {content_length} words in {language} language."
            response = model.generate_content(prompt)
            generated_content = response.parts[0].text

            return render_template('index.html', topics=topics, content_length=content_length, language=language, generated_content=generated_content)

    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
