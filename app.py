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
    if 'file' not in request.files:
        print("ERROR: No file provided", flush=True)
        return {'error': 'No file provided'}, 400

    file = request.files['file']
    data = request.form.to_dict()

    print(f"Received file: {file.filename}", flush=True)
    print(f"Received data fields: {list(data.keys())}", flush=True)
    print(f"Data values: {data}", flush=True)

    file_bytes = file.read()
    print(f"File bytes length: {len(file_bytes)}", flush=True)

    zip_input = io.BytesIO(file_bytes)
    zip_output = io.BytesIO()

    with zipfile.ZipFile(zip_input, 'r') as zin:
        with zipfile.ZipFile(zip_output, 'w', zipfile.ZIP_DEFLATED) as zout:
            for item in zin.infolist():
                content = zin.read(item.filename)

                if item.filename == 'word/document.xml':
                    xml = content.decode('utf-8')
                    print(f"NACHNAME in XML: {'NACHNAME' in xml}", flush=True)
                    for key, value in data.items():
                        placeholder = '{{' + key + '}}'
                        if placeholder in xml:
                            print(f"Replacing {placeholder} with {value}", flush=True)
                        else:
                            print(f"NOT FOUND: {placeholder}", flush=True)
                        xml = xml.replace(placeholder, value or '')
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
