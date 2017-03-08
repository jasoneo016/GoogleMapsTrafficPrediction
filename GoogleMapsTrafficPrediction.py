from flask import Flask
from flask import request
from flask import render_template
from sklearn.linear_model import Ridge
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline

app = Flask(__name__)

#<road id, direction, dayOfWeek, timeOfDay> => <traffic status>

dataset1 = [10, 0, 1, 8]
dataset2 = [10, 0, 2, 9]
dataset3 = [10, 1, 1, 13]
dataset4 = [5, 0 , 1, 15]
dataset5 = [5, 1, 5, 16]
dataset6 = [5, 1, 6, 18]
datasets = [dataset1, dataset2, dataset3, dataset4, dataset5, dataset6]

trafficStatus = [8, 7, 5, 6, 9, 9]

model = make_pipeline(PolynomialFeatures(4), Ridge())
model.fit(datasets, trafficStatus)

print model.predict( [ [10, 0, 3, 12] ] )

@app.route('/')
def hello_world():
    return app.send_static_file('index.html')


@app.route('/receivedata', methods=['GET', 'POST'])
def receive_data():
    resp = None
    if request.method == 'POST':
        roadID = int(request.form['roadid'])
        direction = int(request.form['direction'])
        dayOfWeek = int(request.form['dayofweek'])
        timeOfDay = int(request.form['timeofday'])

        dataset = [roadID, direction, dayOfWeek, timeOfDay]

        global datasets
        datasets.append(dataset)

        tempTrafficStatus = int(request.form['trafficstatus'])
        global trafficStatus
        trafficStatus.append(tempTrafficStatus)

        model.fit(datasets, trafficStatus)

        resp = "Data Inputted Successfully"

    return render_template('receive_data.html', response = resp)

@app.route('/predict', methods=['GET', 'POST'])
def make_prediction():
    resp = None
    if request.method == 'POST':
        roadID = int(request.form['roadid'])
        direction = int(request.form['direction'])
        dayOfWeek = int(request.form['dayofweek'])
        timeOfDay = int(request.form['timeofday'])

        dataset = [roadID, direction, dayOfWeek, timeOfDay]
        resp = "Predicted Traffic Status = " + str(model.predict([dataset]))

    return render_template('predict.html', response = resp)

if __name__ == '__main__':
    app.run(host = '0.0.0.0')
