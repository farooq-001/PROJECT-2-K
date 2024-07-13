from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

# Function to list files and directories
def list_files(dir_path):
    try:
        files = []
        if os.path.isdir(dir_path):
            for file_name in os.listdir(dir_path):
                file_path = os.path.join(dir_path, file_name)
                is_dir = os.path.isdir(file_path)
                files.append({
                    'name': file_name,
                    'is_dir': is_dir
                })
        current_path = os.path.abspath(dir_path)
        return {'files': files, 'current_path': current_path}
    except Exception as e:
        return {'error': str(e)}

# Function to open a file and read its content
def open_file(file_path):
    try:
        with open(file_path, 'r') as file:
            content = file.read()
        return {'content': content}
    except Exception as e:
        return {'error': str(e)}

# Function to save content to a file
def save_file(file_path, content):
    try:
        with open(file_path, 'w') as file:
            file.write(content)
        return {'message': 'File saved successfully.'}
    except Exception as e:
        return {'error': str(e)}

# Route to render the file manager interface
@app.route('/')
def index():
    return render_template('file_manager.html')

# Route to list files and directories
@app.route('/list', methods=['POST'])
def list_files_route():
    dir_path = request.json.get('dir_path', '/')
    return jsonify(list_files(dir_path))

# Route to open and read a file
@app.route('/open', methods=['POST'])
def open_file_route():
    file_path = request.json.get('file_path', '')
    return jsonify(open_file(file_path))

# Route to save content to a file
@app.route('/save', methods=['POST'])
def save_file_route():
    file_path = request.form.get('file_path', '')
    content = request.form.get('content', '')
    return jsonify(save_file(file_path, content))

if __name__ == '__main__':
    app.run(debug=True)
