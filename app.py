from flask import Flask, send_file, jsonify
import script  # Asigură-te că acest fișier conține funcțiile necesare pentru scraping

app = Flask(__name__)

@app.route('/scrape', methods=['GET'])
def scrape_and_serve_file():
    try:
        # Apelează funcția de scraping care generează output.csv
        script.scrape_data()  # Asigură-te că aceasta este funcția care creează output.csv
        
        # Servește fișierul CSV pentru descărcare
        return send_file('output.csv', as_attachment=True)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
