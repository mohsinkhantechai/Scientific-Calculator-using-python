from flask import Flask, render_template, request, jsonify
import math

app = Flask(__name__)

# Evaluate mathematical expressions safely
def safe_eval(expr):
    allowed_names = {}
    allowed_names.update(math.__dict__)  # include math functions

    # Remove dangerous built-ins
    for name in ["__builtins__", "__import__", "eval", "exec", "open"]:
        allowed_names.pop(name, None)

    try:
        result = eval(expr, {"__builtins__": {}}, allowed_names)
    except Exception:
        result = "Error"
    return result


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    expression = data.get('expression', '')
    result = safe_eval(expression)
    return jsonify({"result": result})


if __name__ == '__main__':
    app.run(debug=True)
