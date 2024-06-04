from flask import Flask, request, jsonify, render_template
from analizador_lexico import lexer
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods= ['POST'])
def analyze():
    data = request.get_json()
    text = data.get('text')
    lexer.input(text)
    formatted_result = []
    token_values = []
    tokens = []

    line_number = 1
    
    while True:
        tok = lexer.token()
        if not tok:
            break
        formatted_result.append(f"LINEA {line_number}\n\n<{tok.type}>    {tok.value}\n")
        token_values.append(tok.value)
        tokens.append({'type': tok.type, 'value': tok.value})
        line_number += 1
    
    return jsonify({
        'formatted': "\n".join(formatted_result),
        'tokens': token_values,
        'tokens_list': tokens
    })

if __name__ == '__main__':
    app.run(debug=True)