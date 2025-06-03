from flask import Flask, render_template, request
import sympy as sp
import json # Ensure json is imported if you are using it elsewhere, though not directly for this change

app = Flask(__name__)

def secant_method(expr_str, x0, x1, max_iter, tol): # tol here is "Angka Benar"
    x = sp.symbols('x')
    try:
        f_expr = sp.sympify(expr_str)
    except sp.SympifyError as e:
        return {'error': 'Fungsi tidak valid: ' + str(e)}

    f = sp.lambdify(x, f_expr, modules=['math'])
    results = []

    # Use a consistent format string based on tol for display purposes
    # Ensure tol is an integer, which it should be from the route
    fmt_str = f".{int(tol)}f"

    results.append({
        'iter': 0,
        'x': x0,
        'f_x': f(x0),
        'error': 'N/A',
        'step_calc': 'Initial value x0'
    })
    results.append({
        'iter': 1,
        'x': x1,
        'f_x': f(x1),
        'error': 'N/A',
        'step_calc': 'Initial value x1'
    })

    current_x0 = x0
    current_x1 = x1

    for i in range(2, max_iter + 2):
        try:
            fx0 = f(current_x0)
            fx1 = f(current_x1)
            denominator = fx1 - fx0

            if denominator == 0:
                return {'error': 'Pembagian dengan nol terjadi pada iterasi ke-{}'.format(i)}

            x_next = current_x1 - fx1 * (current_x1 - current_x0) / denominator
            error = abs(x_next - current_x1)

            # Update step_calc to use the dynamic precision from tol
            step_calc = (
                f"x_{i} = x_{i-1} - f(x_{i-1}) * (x_{i-1} - x_{i-2}) / (f(x_{i-1}) - f(x_{i-2}))\n"
                f"x_{i} = {current_x1:{fmt_str}} - ({fx1:{fmt_str}}) * ({current_x1:{fmt_str}} - {current_x0:{fmt_str}}) / ({fx1:{fmt_str}} - {fx0:{fmt_str}})\n"
                f"x_{i} = {x_next:{fmt_str}}"
            )

            results.append({
                'iter': i,
                'x': x_next,
                'f_x': f(x_next),
                'error': error,
                'step_calc': step_calc
            })

            # The stopping condition uses 'tol' in its specific way
            # Ensure tol for calculation is what's intended.
            # If tol is purely for display decimal places, the stopping threshold might need a different logic
            # For now, sticking to your existing logic: error < (value_of_tol / (10**value_of_tol))
            # Here, 'tol' from the function argument is used.
            stopping_threshold_value = tol / (10**tol) if tol > 0 else 1e-9 # Avoid issues if tol is 0, though form has min="1"
            if error < stopping_threshold_value:
                break
            
            current_x0, current_x1 = current_x1, x_next
        except Exception as e:
            return {'error': 'Error pada iterasi ke-{}: {}'.format(i, str(e))}

    return results

@app.route('/', methods=['GET', 'POST'])
def index():
    results = []
    error = None
    # These lists for chart data should remain numbers, not formatted strings
    iterations_chart = []
    x_values_chart = []
    fx_values_chart = [] # Added for f(x) in chart if needed, as per your JS
    errors_chart = []


    request_form_data = {} # To store form data for re-populating and template use

    if request.method == 'POST':
        request_form_data = request.form # Store for re-populating form
        func_str = request.form.get('function', '')
        try:
            x0 = float(request.form.get('x0', '0'))
            x1 = float(request.form.get('x1', '0'))
            max_iter = int(request.form.get('max_iter', '10'))
            # 'tol' from the form is "Angka Benar", used for display precision and stopping condition
            tol_display_and_calc = int(request.form.get('tol', '4')) # Default to 4 for example

            # Basic validation for tol_display_and_calc to be at least 1 as per your form
            if tol_display_and_calc < 1:
                tol_display_and_calc = 1


            results_data = secant_method(func_str, x0, x1, max_iter, tol_display_and_calc)

            if isinstance(results_data, dict) and 'error' in results_data:
                error = results_data['error']
                results = [] # Ensure results is empty or handled if error
            else:
                results = results_data # Assign processed data to results for the template
                # Prepare data for the chart (raw numerical values)
                iterations_chart = [r['iter'] for r in results]
                x_values_chart = [r['x'] for r in results]
                fx_values_chart = [r['f_x'] for r in results] # For the f(x) line in chart
                errors_chart = [r['error'] for r in results if r['error'] != 'N/A']

        except ValueError as e:
            error = 'Input angka tidak valid: ' + str(e)
        except Exception as e: # Catch any other unexpected errors during form processing
            error = 'Terjadi kesalahan: ' + str(e)
    else:
        # For GET request, provide default values for form if needed
        request_form_data = {
            'function': '',
            'x0': '',
            'x1': '',
            'tol': '4', # Default "Angka Benar"
            'max_iter': '10'
        }


    return render_template(
        'index.html',
        results=results,
        error=error,
        request_form=request_form_data, # Pass the form data back to repopulate
        # Pass chart data as JSON strings
        iterations_chart=json.dumps(iterations_chart),
        x_values_chart=json.dumps(x_values_chart),
        fx_values_chart=json.dumps(fx_values_chart), # Pass f(x) values for chart
        errors_chart=json.dumps(errors_chart)
    )

if __name__ == '__main__':
    app.run(debug=True)