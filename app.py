from flask import Flask, render_template, request, session
from FinalModel import predict_furnace_temps

app = Flask(__name__)
app.secret_key = 'OSJ~x[(k--sGXH4{"sPbPnhy)g?o.&)X'  # Set a secret key for session management

@app.route("/")
def home_page():
    # Use session to store input values
    inputs = session.get('inputs', {
        'width': '',
        'thickness': '',
        'gsm_a': '',
        'hardness': ''
    })
    return render_template("InputForm.html", inputs=inputs)

@app.route("/predict", methods=['POST'])
def predict():
    try:
        # Retrieve inputs from the form
        inputs = {
            'width': float(request.form['width']),
            'thickness': float(request.form['thickness']),
            'gsm_a': float(request.form['gsm_a']),
            'hardness': float(request.form['hardness'])
        }
        
        # Store inputs in session
        session['inputs'] = inputs

        # Pass inputs for prediction
        result = predict_furnace_temps(**inputs)

        # Round the results to 2 decimal places
        result = {k: round(v) for k, v in result.items()}

        return render_template("Output.html", result=result, inputs=inputs)

    except Exception as e:
        return f"An error occurred: {str(e)}"

@app.route("/reset", methods=['POST'])
def reset():
    session.pop('inputs', None)
    return home_page()

if __name__ == '__main__':
    app.run(debug=True)
