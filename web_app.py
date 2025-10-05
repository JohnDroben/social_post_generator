from flask import Flask, render_template, request
from openai_module import generate_post

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form.get('url')
        style = request.form.get('style', 'ироничный')
        # Here you would integrate the logic to fetch and process the URL
        # For now, we simulate with a placeholder
        page_text = "Пример текста страницы для URL: " + url
        post = generate_post(page_text, style=style)
        return render_template('index.html', post=post, url=url, style=style)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)