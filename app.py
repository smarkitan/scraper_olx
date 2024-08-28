from flask import Flask, send_from_directory
import script  # Importă scriptul de scraping

app = Flask(__name__)

@app.route('/scrape', methods=['GET'])
def scrape_and_serve_file():
    file_path = script.scrape_data()
    if file_path:
        return send_from_directory('.', file_path, as_attachment=True)
    return "Eroare la generarea fișierului CSV", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
