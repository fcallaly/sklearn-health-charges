from flask import Flask, request
from flask_restx import Resource, Api, fields
import joblib

app = Flask(__name__)
api = Api(app)

ns = api.namespace('health_charges', description='Health Insurance Charges')

customer = api.model('customer', {
    'age': fields.Integer(required=True, description='Age'),
    'gender_code': fields.Integer(required=True, description='Gender Code - 0: F, 1: M'),
    'bmi': fields.Float(required=True, description='BMI'),
    'children': fields.Integer(required=True, description='Number of children'),
    'smoker_code': fields.Integer(required=True, description='Smoker Code - 0: No, 1: Yes')
    })

model = joblib.load('health_charges_classifier_model.joblib')

@ns.route('/')
class Review(Resource):
    def get(self):
        return {'response': 'health charges classifier is running'}

    @ns.expect(customer)
    def post(self):
        print('payload:')
        print(api.payload)

        prediction = model.predict_proba([[api.payload['age'],
                                           api.payload['gender_code'],
                                           api.payload['bmi'],
                                           api.payload['children'],
                                           api.payload['smoker_code']]])[0]
        print('prediction: ' + str(prediction))

        max_prob = max(prediction)
        class_idx = list(prediction).index(max_prob)

        return {'customer': api.payload,
                'class': class_idx,
                'probability': max_prob}

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
