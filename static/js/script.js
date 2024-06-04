function analyzeCode() {
    const code = document.getElementById('code-input').value;
    fetch('/analyze', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text: code })
    })
        .then(response => response.json())
        .then(data => {
            document.getElementById('results').textContent = data.formatted;
            const tokenList = document.getElementById('token-list');
            tokenList.innerHTML = '';  // Clear previous tokens
            data.tokens.forEach(token => {
                const li = document.createElement('li');
                li.textContent = token;
                tokenList.appendChild(li);
            });
            const tableBody = document.getElementById('token-table-body');
            tableBody.innerHTML = '';  // Limpiar la tabla antes de añadir nuevas filas
            let totalPR = 0, totalID = 0, totalSymbols = 0, totalError = 0, totalPython = 0, totalJava = 0, totalCpp = 0;

            data.tokens_list.forEach(token => {
                const row = tableBody.insertRow();

                // Celda para el valor del token
                const tokenCell = row.insertCell();
                tokenCell.textContent = token.value;
                tokenCell.className = 'border border-black px-4 py-2';

                // Celda para PR Python
                const prPythonCell = row.insertCell();
                prPythonCell.textContent = (token.type === 'PYTHON_RESERVED') ? 'X' : '';
                prPythonCell.className = 'border border-black px-4 py-2 text-center';
                if (token.type === 'PYTHON_RESERVED') totalPython++;

                // Celda para PR Java
                const prJavaCell = row.insertCell();
                prJavaCell.textContent = (token.type === 'JAVA_RESERVED') ? 'X' : '';
                prJavaCell.className = 'border border-black px-4 py-2 text-center';
                if (token.type === 'JAVA_RESERVED') totalJava++;

                // Celda para PR C++
                const prCppCell = row.insertCell();
                prCppCell.textContent = (token.type === 'CPP_RESERVED') ? 'X' : '';
                prCppCell.className = 'border border-black px-4 py-2 text-center';
                if (token.type === 'CPP_RESERVED') totalCpp++;

                // Celda para PR
                const prCell = row.insertCell();
                prCell.textContent = (['FOR', 'IF', 'DO', 'WHILE', 'ELSE', 'PROGRAMA', 'READ', 'INT', 'PRINTF'].includes(token.type)) ? 'X' : '';
                prCell.className = 'border border-black px-4 py-2 text-center';
                if (['FOR', 'IF', 'DO', 'WHILE', 'ELSE', 'PROGRAMA', 'READ', 'INT', 'PRINTF'].includes(token.type)) totalPR++;


                // Celda para ID
                const idCell = row.insertCell();
                idCell.textContent = (token.type === 'ID') ? 'X' : '';
                idCell.className = 'border border-black px-4 py-2 text-center';
                if (token.type === 'ID') totalID++;

                // Celda para Símbolo
                const symbolCell = row.insertCell();
                symbolCell.textContent = (token.type === 'LPAREN' || token.type === 'RPAREN' || token.type === 'SEMICOLON' || token.type === 'COMMA' || token.type === 'LBRACE' || token.type === 'RBRACE') ? 'X' : '';
                symbolCell.className = 'border border-black px-4 py-2 text-center';
                if (token.type === 'LPAREN' || token.type === 'RPAREN' || token.type === 'SEMICOLON' || token.type === 'COMMA' || token.type === 'LBRACE' || token.type === 'RBRACE') totalSymbols++;

                const errorCell = row.insertCell();
                errorCell.textContent = (token.type === 'ERROR') ? 'X' : '';
                errorCell.className = 'border border-black px-4 py-2 text-center';
                if (token.type === 'ERROR') totalError++;
            });

            // Añadir fila de totales al final
            const totalRow = tableBody.insertRow();
            totalRow.insertCell().textContent = "Total";
            totalRow.insertCell().textContent = totalPython;
            totalRow.insertCell().textContent = totalJava;
            totalRow.insertCell().textContent = totalCpp;
            totalRow.insertCell().textContent = totalPR;
            totalRow.insertCell().textContent = totalID;
            totalRow.insertCell().textContent = totalSymbols;
            totalRow.insertCell().textContent = totalError;


            totalRow.cells[0].className = 'border border-black px-4 py-2 font-bold';
            totalRow.cells[1].className = 'border border-black px-4 py-2 text-center';
            totalRow.cells[2].className = 'border border-black px-4 py-2 text-center';
            totalRow.cells[3].className = 'border border-black px-4 py-2 text-center';
            totalRow.cells[4].className = 'border border-black px-4 py-2 text-center';
            totalRow.cells[5].className = 'border border-black px-4 py-2 text-center';
            totalRow.cells[6].className = 'border border-black px-4 py-2 text-center';
            totalRow.cells[7].className = 'border border-black px-4 py-2 text-center';

        })
        .catch(error => console.error('Error:', error));
}