from flask import Flask, render_template, request, redirect, url_for, send_file
from statistics import mean
import qrcode
from io import BytesIO

app = Flask(__name__)

# Read slider titles from the text file
def read_slider_titles():
    with open('slider_titles.txt', 'r') as file:
        titles = [line.strip() for line in file]
    return titles
#all Requests http moved to https
@app.before_request
def force_https():
    if not request.is_secure:
        url = request.url.replace("http://", "https://", 1)
        return redirect(url, code=301)
# Generate a QR code for the main page URL
@app.route('/qrcode')
def generate_qrcode():
    main_page_url = request.url_root  
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(main_page_url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    
  
    img_io = BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)
    
    return send_file(img_io, mimetype='image/png')
#The main function
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':

        selected_gender = request.form['gender']
        
        slider_values = {}
        slider_titles = read_slider_titles()
        for title in slider_titles:
            formatted_title = title.lower().replace(" ", "-")
            value = float(request.form[formatted_title])  # Assuming your sliders return float values
            slider_values[title] = value

        # Redirect to the result page with the data
        return redirect(url_for('result', selected_gender=selected_gender, slider_values=slider_values))

    slider_titles = read_slider_titles()
    formatted_titles = [title.lower().replace(" ", "-") for title in slider_titles]
    title_data = list(zip(slider_titles, formatted_titles))

    return render_template('main.html', title_data=title_data)
        # Calculate the average of slider values
@app.route('/result', methods=['POST'])
def result():
    if request.method == 'POST':

        selected_gender = request.form['gender']
        slider_values = {}
        slider_titles = read_slider_titles()
        for title in slider_titles:
            formatted_title = title.lower().replace(" ", "-")
            value = float(request.form[formatted_title])
            slider_values[title] = value
        

        average_value = mean(slider_values.values())
    
        return render_template('result.html', selected_gender=selected_gender, slider_values=slider_values, average_value=average_value)
    
    # Handle non-Post requests to /result (for initial page load)
    return render_template('result.html', selected_gender=None, slider_values={}, average_value=None)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, ssl_context=('your_cert.pem', 'your_key.pem'))
