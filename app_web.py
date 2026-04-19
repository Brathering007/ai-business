from flask import Flask, request, render_template_string
import os
from openai import OpenAI

app = Flask(__name__)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Business Generator</title>
</head>
<body>

<h1>Business Generator</h1>

<form method="post">
    <input type="text" name="topic" placeholder="Thema eingeben" required>
    <button type="submit">Generieren</button>
</form>

{% if ideas %}
<h2>Ergebnis:</h2>
<pre>{{ ideas }}</pre>
{% endif %}

</body>
</html>
"""

def generate_business(topic):
    prompt = f"Erstelle eine Geschäftsidee für: {topic}"

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )
    return response.choices[0].message.content

@app.route("/", methods=["GET", "POST"])
def home():
    ideas = None
    if request.method == "POST":
        topic = request.form["topic"]
        ideas = generate_business(topic)

    return render_template_string(HTML, ideas=ideas)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

