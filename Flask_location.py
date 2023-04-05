from flask import Flask, request, render_template
import requests

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        address = request.form['address']
        lat, long = location(address)
        air_data = current_air_pollution(lat, long)
        # air_data = location(address)
        return render_template('result.html', air_data=air_data)
    return render_template('index.html')


def current_air_pollution(lat, long):
    url = 'http://api.openweathermap.org/data/2.5/air_pollution?'
    params = {
        'lat': lat,
        'lon': long,
        'appid': 'ac3f6d382205bba950491a02692bf967',
    }
    r = requests.get(url, params=params).json()
    data = r['list']
    for x in data:
        pm10 = x['components']['pm10']
        pm2_5 = x['components']['pm2_5']
        no2 = x['components']['no2']
        co = x['components']['co']
        o3 = x['components']['o3']

    result = (f"tổng các hạt bụi lơ lửng có đường kính khí động học nhỏ hơn hoặc bằng 10 µm bằng: {pm10} μg/m3\n" +
              f"tổng các hạt bụi lơ lửng có đường kính khí động học nhỏ hơn hoặc bằng 2.5 µm bằng: {pm2_5} μg/m3\n" +
              f"nồng độ NO2 trong không khí đạt: {no2} μg/m3\n" +
              f"lượng khí CO trong không khí đạt: {co} μg/m3\n" +
              f"nồng độ OZON trong không khí đạt: {o3} μg/m3\n")

    if 90 <= pm10 <= 180 or 55 <= pm2_5 <= 110:
        result += 'một số loại bụi mịn trong không khí vượt mức an toàn, có thể ảnh hưởng đến sức khỏe\n'
        result += 'vui lòng đem theo khẩu trang khi ra đường\n'
    elif 200 <= no2 <= 400 or 180 <= o3 <= 240:
        result += '\nchất lượng không khí có thể gây ảnh hưởng xấu tới sức khỏe\n'
        result += '\nhãy trang bị khẩu trang trước khi ra đường\n'
    else:
        result += '\n chất lượng không khí nằm trong mức cho phép\n'

    return result


def location(address):
    url = 'http://dev.virtualearth.net/REST/v1/Locations'
    params = {
        'adminDistrict': 'VN',
        'locality': 'Ho Chi Minh',
        'postalCode': '700000',
        'addressLine': address,
        'countryRegion': 'VN',
        'key': 'AtEMO7JqvIrYPvX2_NAeiOU8-SwP_-vlUoI6IHnbukr_MgE-cmkuQfbXvdpDqsBd'
    }

    r = requests.get(url, params=params).json()
    data = r['resourceSets']
    for x in data:
        resources = x['resources']
    data2 = resources
    for y in data2:
        point = y['point']['coordinates']
    data3 = point
    lat = data3[0]
    long = data3[1]
    data = current_air_pollution(lat, long)
    return lat, long
    # current_air_pollution(lat, long)


if __name__ == '__main__':
    app.run(debug=True)
