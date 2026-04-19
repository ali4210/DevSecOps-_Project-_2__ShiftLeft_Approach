from flask import Flask, request, render_template_string

app = Flask(__name__)

HTML = """
<html><body>
<h1>DevSecOps Lab App</h1>
<form method="GET">
  <input name="name" placeholder="Enter your name">
  <button type="submit">Greet</button>
</form>
{% if name %}
  <h2>Hello, {{ name }}!</h2>
{% endif %}
</body></html>
"""

@app.route('/')
def index():
    name = request.args.get('name', '')
    return render_template_string(HTML, name=name)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
