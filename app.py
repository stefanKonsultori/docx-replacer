from flask import Flask, request, send_file
import zipfile
import io
import os

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health():
    return {'status': 'ok'}

@app.route('/replace', methods=['POST'])
def replace():
    # Get the uploaded file
    if 'file' not in request.files:
        return {'error': 'No file provided'}, 400
    
    file = request.files['file']
    data = request.form.to_dict()  # All other form fields are replacements
    
    # Read the docx (which is a ZIP)
    file_bytes = file.read()
    zip_input = io.BytesIO(file_bytes)
    zip_output = io.BytesIO()
    
    # Open and process the ZIP
    with zipfile.ZipFile(zip_input, 'r') as zin:
        with zipfile.ZipFile(zip_output, 'w', zipfile.ZIP_DEFLATED) as zout:
            for item in zin.infolist():
                content = zin.read(item.filename)
                
                # Only do replacements in document.xml
                if item.filename == 'word/document.xml':
                    xml = content.decode('utf-8')
                    for key, value in data.items():
                        xml = xml.replace('{{' + key + '}}', value or '')
                    content = xml.encode('utf-8')
                
                zout.writestr(item, content)
    
    zip_output.seek(0)
    return send_file(
        zip_output,
        mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        as_attachment=True,
        download_name='filled_agreement.docx'
    )

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
