# import all libraires
from io import BytesIO
from flask import Flask, render_template, request, Response, send_file
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import clean_data

# Initialize flask  and create sqlite database
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Upload(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(50))
    data = db.Column(db.LargeBinary)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        upload = Upload(filename=file.filename, data=file.read())
        db.session.add(upload)
        db.session.commit()
        return f'Uploaded: {file.filename}. Download here: <a href="/download/{upload.id}">download</a>'
    return render_template('index.html')


@app.route('/download/<upload_id>')
def download(upload_id):
    buffer = BytesIO()
    upload = Upload.query.filter_by(id=upload_id).first()
    file = BytesIO(upload.data)
    dataFile = file
    addressList = '/home/ajleitzke/mysite/addresses.xlsx'
    df_calls, df_address = clean_data.prepare(dataFile, addressList)
    df_joined = clean_data.join(df_calls, df_address)
    df_joined.to_excel(buffer, index=False)
    headers = {
        'Content-Disposition': 'attachment; filename=output.xlsx',
        'Content-type': 'application/vnd.ms-excel'
    }
    return Response(buffer.getvalue(), mimetype='application/vnd.ms-excel', headers=headers)
