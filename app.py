from flask import Flask, request, jsonify, render_template
from analizador_lexico import lexer, parser_state
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
    parse_result = parser_state.parse(text)

    
    formatted_result = []
    tokens = []

    # Inicia la posición del caracter
    current_position = 0
    
    for tok in lexer:
        if not tok:
            break
        formatted_result.append(f"Linea: {tok.lineno}, Tipo: {tok.type}, Valor: {tok.value}, Posición: {current_position}")
        tokens.append({'line': tok.lineno, 'type': tok.type, 'value': tok.value, 'pos': current_position})

        # Actualiza la posición actual del caracter
        current_position = tok.lexpos

    if parser_state.last_error:
        return jsonify({
            'formatted': "\n".join(formatted_result),
            'tokens_list': tokens,
            'error': parser_state.last_error,
            'error_2' : parser_state.last_semantic_error,
            'parse_result': None
        })
    else:
        return jsonify({
            'formatted': "\n".join(formatted_result),
            'tokens_list': tokens,
            'parse_result': parse_result
        })


if __name__ == '__main__':
    app.run(debug=True)
