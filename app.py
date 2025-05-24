from flask import Flask, render_template, request
import sympy as sp
import json

app = Flask(__name__)

def secant_method(expr_str, x0, x1, max_iter, tol):
    x = sp.symbols('x')
    try:
        f_expr = sp.sympify(expr_str)
    except sp.SympifyError as e:
        return {'error': 'Fungsi tidak valid: ' + str(e)}

    f = sp.lambdify(x, f_expr, modules=['math'])
    results = []

    for i in range(max_iter):
        try:
            fx0 = f(x0)
            fx1 = f(x1)
            denominator = fx1 - fx0
            if denominator == 0:
                return {'error': 'Pembagian dengan nol terjadi pada iterasi ke-{}'.format(i+1)}

            x2 = x1 - fx1 * (x1 - x0) / denominator
            error = abs(x2 - x1)

            results.append({
                'iter': i + 1,
                'x': x2,
                'f_x': f(x2),
                'error': error
            })

            if error < (tol / (10**tol)):
                break

            x0, x1 = x1, x2
        except Exception as e:
            return {'error': 'Error pada iterasi ke-{}: {}'.format(i+1, str(e))}

    return results

@app.route('/', methods=['GET', 'POST'])
def index():
    results = []
    error = None
    iterations = []
    x_values = []
    errors = []

    if request.method == 'POST':
        func_str = request.form.get('function', '')
        try:
            x0 = float(request.form.get('x0', '0'))
            x1 = float(request.form.get('x1', '0'))
            max_iter = int(request.form.get('max_iter', '10'))
            tol = int(request.form.get('tol', '9'))

            results = secant_method(func_str, x0, x1, max_iter, tol)

            if isinstance(results, dict) and 'error' in results:
                error = results['error']
            else:
                iterations = [r['iter'] for r in results]
                x_values = [r['x'] for r in results]
                errors = [r['error'] for r in results]
        except ValueError as e:
            error = 'Input angka tidak valid: ' + str(e)

    return render_template(
        'index.html',
        results=results,
        error=error,
        iterations=json.dumps(iterations),
        x_values=json.dumps(x_values),
        errors=json.dumps(errors)
    )

if __name__ == '__main__':
    app.run(debug=True)
