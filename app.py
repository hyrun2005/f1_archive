from flask import Flask, jsonify, render_template, request
import requests
import json
app = Flask(__name__)


ERGAST_API_URL = "http://ergast.com/api/f1"

@app.route('/drivers', methods=['GET', 'POST'])
def get_drivers():
    def_year = '2024'
    year = request.args.get('drivers_year', def_year)
    response = requests.get(f"{ERGAST_API_URL}/{year}/drivers.json")
    print(year)
    if response.status_code == 200:
        data = response.json()
        drivers = data['MRData']['DriverTable']['Drivers']
        return render_template('drivers.html', drivers=drivers, current_year=year)
    else:
        return f"Error fetching data: {response.status_code}"

@app.route('/drivers/<number>')
def more_info(number):
    response = requests.get(f"https://api.openf1.org/v1/drivers?driver_number={number}&session_key=9158")
    if response.status_code == 200:
        data = response.json()
        full = ""
        return render_template('driver_info.html', driver=data, photo=full)
    else:
        return f"Error fetching data: {response.status_code}"


@app.route('/')
def main_page_handle():
    return render_template('main_page.html')

if __name__ == '__main__':
    app.run(debug=True)
