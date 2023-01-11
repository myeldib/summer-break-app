import os
import csv
import shutil
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename

if os.environ.get('ROOT_PRJ_DIR') is None:
    print('ROOT_PRJ_DIR must be set before starting\n')
    sys.exit(1)

from components.impl.processor.CSVTaxReportProcessor import CSVTaxReportProcessor

ROOT_DIR = os.path.dirname(os.path.abspath(__file__)) 
UPLOAD_FOLDER = ROOT_DIR + '/../../../build_output'
ALLOWED_EXTENSIONS = {'csv'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

cSVTaxReportProcessor = CSVTaxReportProcessor()

def create_build_output():

    if os.path.exists(UPLOAD_FOLDER):
        shutil.rmtree(UPLOAD_FOLDER)

    os.mkdir(UPLOAD_FOLDER)  

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/transactions',methods = ['POST'])
def transactions():
    create_build_output()
    file  = request.files['data']
    if file.filename == '':
        return "No selected file\n"
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        #wait for uploading the file
        while(not os.path.exists(file_path)):
            time.sleep(1)

        cSVTaxReportProcessor.run(file_path)
        return "Successfully processed your file.\n"
    else:
        return "We only support "+ str(ALLOWED_EXTENSIONS) + " files.\n"

@app.route('/report',methods = ['GET'])
def report():
    return{
    "gross-revenue": cSVTaxReportProcessor.get_gross_revenue(),
    "expenses": cSVTaxReportProcessor.get_expenses(),
    "net-revenue": cSVTaxReportProcessor.get_net_revenue()
} 