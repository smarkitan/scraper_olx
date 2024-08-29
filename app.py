from flask import Flask, send_file, render_template_string, jsonify
import pandas as pd
import script  # Asigură-te că acest fișier conține funcțiile necesare pentru scraping
import os

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    try:
        # Apelează funcția de scraping care generează output.csv
        script.scrape_data()
        
        # Citește fișierul CSV într-un DataFrame Pandas
        df = pd.read_csv('output.csv')
        
        # Transformă coloana "Link" în linkuri clicabile
        df['Link'] = df['Link'].apply(lambda x: f'<a href="{x}" target="_blank">{x}</a>')
        
        # Creează HTML-ul pentru afișarea tabelului
        html_table = df.to_html(classes='table table-striped', index=False, escape=False)

        # Template-ul HTML pentru pagina principală
        html_template = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Scraper Results</title>
            <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css">
        </head>
        <body>
            <div class="container">
                <h1 class="mt-5">OLX Scraper Results</h1>
                <div class="mt-3">
                    <a href="/download" class="btn btn-primary">Download CSV File</a>
                </div>
                <div class="mt-3">
                    {html_table}
                </div>
            </div>
        </body>
        </html>
        """

        return render_template_string(html_template)
    except Exception as e:
        return jsonify({'error': str(e)}), 500




@app.route('/download', methods=['GET'])
def download_file():
    try:
        return send_file('output.csv', as_attachment=True)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port)

