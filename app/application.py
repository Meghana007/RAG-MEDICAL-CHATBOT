#main code

from flask import Flask,render_template,request,session,redirect,url_for
from app.components.retriever import create_qa_chain
from dotenv import load_dotenv
import os

load_dotenv()
HF_TOKEN = os.environ.get("HF_TOKEN")

app = Flask(__name__)
app.secret_key = "mysecretkey007"

from markupsafe import Markup
def n12br(value):
    return Markup(value.replace("\n", "<br>\n"))

app.jinja_env.filters['n12br'] = n12br

@app.route("/", methods=["GET", "POST"])
def index():
    if "messages" not in session:
        session["messages"] = []

    messages = session["messages"]
  

    if request.method == "POST":
        user_input = request.form.get("prompt")

        if user_input:
            messages.append({"role": "user", "content": user_input})

            try:
                qa_chain = create_qa_chain()
                response = qa_chain.invoke({"query": user_input})
                result = response.get("result", "No response")

                messages.append({"role": "assistant", "content": result})

            except Exception as e:
                error_msg = f"Error : {str(e)}"
                return render_template(
                    "index.html",
                    messages=messages,
                    error=error_msg
                )

            session["messages"] = messages
            session.modified = True

        return redirect(url_for("index"))

    return render_template("index.html", messages=messages)
    

@app.route("/clear")
def clear():
    session.pop("messages", None)
    return redirect(url_for("index"))

if __name__=="__main__":
    app.run(host="0.0.0.0" , port=5000, debug=True, use_reloader = False)




