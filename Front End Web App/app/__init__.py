from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Store results in memory (for demo; not persistent)
results = []

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html', results=results)

@app.route('/calculate', methods=['POST'])
def calculate():
    # Collect all form inputs
    data = {
        'overall_qual': request.form.get('overall_qual'),
        'garage_area': request.form.get('garage_area'),
        'gr_liv_area': request.form.get('gr_liv_area'),
        'first_flr_sf': request.form.get('first_flr_sf'),
        'garage_cars': request.form.get('garage_cars'),
        'total_baths': request.form.get('total_baths'),
        'year_built': request.form.get('year_built'),
        'total_bsmt_sf': request.form.get('total_bsmt_sf'),
        'year_remod_add': request.form.get('year_remod_add'),
        'garage_yr_blt': request.form.get('garage_yr_blt'),
        'fireplaces': request.form.get('fireplaces'),
    }
    # Placeholder for calculation result (replace with your model/prediction)
    data['result'] = 'TBD'
    results.append(data)
    return redirect(url_for('home'))
