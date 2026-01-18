from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import os
from PIL import Image
import io, base64
import matplotlib.pyplot as plt

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), 'uploads')
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Load metadata
metadata = pd.read_csv('metadata.csv')

@app.route('/', methods=['GET'])
def welcome():
    # landing page with intro; Continue -> /app
    return render_template('welcome.html')


@app.route('/app', methods=['GET', 'POST'])
def app_route():
    error = None
    if request.method == 'POST':
        f = request.files.get('image')
        if not f or f.filename == '':
            error = 'No file uploaded.'
            return render_template('index.html', error=error)
        filename = f.filename
        save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        f.save(save_path)

        if filename not in metadata['filename'].values:
            error = 'Image not found in dataset.'
            return render_template('index.html', error=error)

        row = metadata[metadata['filename'] == filename].iloc[0]

        # prepare image data for embedding
        with open(save_path, 'rb') as imf:
            img_b64 = base64.b64encode(imf.read()).decode('utf-8')

        # create plot
        days = list(range(0, 15))
        regen_signal = [min(1.0, row['dose'] * d * 0.8) for d in days]
        inhibitor_signal = [max(0, 1.0 - d * 0.07) for d in days]

        fig, ax = plt.subplots(figsize=(8,4))
        ax.plot(days, regen_signal, label=f"{row['chemical']} (Regeneration Signal)", linewidth=3)
        ax.plot(days, inhibitor_signal, label='Inhibitory Molecules (Nogo-A / MAG / CSPGs)', linewidth=3)
        ax.axvspan(3, row['days_until_next'], color='green', alpha=0.25, label='Optimal Treatment Window')
        ax.set_xlabel('Days After Injury')
        ax.set_ylabel('Signal Strength')
        ax.set_title('Neural Repair Dynamics')
        ax.legend()
        ax.grid(True)

        buf = io.BytesIO()
        fig.savefig(buf, format='png', bbox_inches='tight')
        buf.seek(0)
        plot_b64 = base64.b64encode(buf.read()).decode('utf-8')
        plt.close(fig)

        return render_template('result.html', row=row.to_dict(), img_b64=img_b64, plot_b64=plot_b64)

    return render_template('index.html', error=error)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
