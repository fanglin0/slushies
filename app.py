import os
import uuid
import pandas as pd
from flask import Flask, render_template, redirect, url_for, request, Response, send_from_directory, jsonify

app = Flask(__name__, template_folder='templates')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method=='GET':
        return render_template('index.html')
    elif request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username =='kitty' and password =='password':
            return 'Success'
    else:
        return 'Method Not Allowed', 405

@app.route('/file_upload', methods=['POST'])
def file_upload():
    file = request.files['file']
    if not file:
        return "No file uploaded", 400

    if file.content_type =='text/plain':
        return file.read().decode()
    elif file.content_type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' or file.content_type=='application/vnd.ms-excel':
        df = pd.read_excel(file)
        return df.to_html()
    return "Unsupported file type", 400

@app.route('/convert_csv', methods=['POST'])
def convert_csv():
    file = request.files['file']
    if not file:
        return "No file uploaded", 400
    df = pd.read_excel(file)
    response = Response(
        df.to_csv(),
        mimetype='text/csv', #content type
        headers ={
            'Content-Disposition': 'attachment; filename=result.csv' #return name
        }     
    )
    return response

@app.route('/convert_csv_two', methods=['POST'])
def convert_csv_two():
    file = request.files['file']
    df = pd.read_excel(file)

    if not os.path.exists('downloads'):
        os.makedirs('downloads')

    filename = f'{uuid.uuid4()}.csv'
    df.to_csv(os.path.join('downloads', filename))
    return render_template('download.html', filename=filename)

@app.route('/download/<filename>')
def download(filename):
    return send_from_directory('downloads', filename, download_name='result.csv')

@app.route('/handle_post', methods=['POST'])
def handle_post():
    greeting = request.json['greeting']
    name = request.json['name']

    with open('file.txt', 'w') as f:
        f.write(f'{greeting}, {name}')
    return jsonify({'message': 'Succesfully written!'})

# CRUD functionalites
DB_FILE = 'data.csv'
if not os.path.exists(DB_FILE):
    pd.DataFrame(columns=['id', 'name']).to_csv(DB_FILE, index=False)
@app.route('/add', methods=['POST'])
def add():
    name = request.form.get('name')
    df = pd.read_csv(DB_FILE)

    new_row = {'id': len(df) + 1, 'name': name}
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

    df.to_csv(DB_FILE, index=False)
    return redirect('/')
@app.route('/items')
def items():
    df = pd.read_csv(DB_FILE)
    return df.to_html()
@app.route('/update/<int:item_id>', methods=['POST'])
def update(item_id):
    df = pd.read_csv(DB_FILE)
    new_name = request.form.get('name')

    df.loc[df['id'] == item_id, 'name'] = new_name
    df.to_csv(DB_FILE, index=False)

    return redirect('/items')
@app.route('/delete/<int:item_id>')
def delete(item_id):
    df = pd.read_csv(DB_FILE)
    df = df[df['id'] != item_id]

    df.to_csv(DB_FILE, index=False)
    return redirect('/items')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port='5001')
   

# @app.route('/other')
# def other():
#     some_text = 'Hello World'
#     return render_template('other.html', some_text = some_text)

# @app.route('/redirect_endpoint')
# def redirect_endpoint():
#     return redirect(url_for('other'))

# @app.template_filter('reverse_string')
# def reverse_string(s):
#     return s[::-1]

# @app.template_filter('repeat')
# def repeat(s, times=2):
#     return s * times

# @app.template_filter('alternate_case')
# def alternate_case(s):
#     return ''.join([c.upper() if i%2 ==0 else c.lower() for i,c in enumerate(s)])

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', debug=True, port=5001)