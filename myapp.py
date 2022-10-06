from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import chartmogul
from models import setup_db

from models import Mrr
api_key = 'd03aa64259babb567aca714386d34489'
config = chartmogul.Config(api_key)

def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers','Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
        return response

    @app.route('/', methods =['GET'])
    def say_hi():
        print(chartmogul.Ping.ping(config).get())
        return jsonify({
            "success" : True,
            "say" : "hi"
        })

    @app.route('/getmrr', methods = ['GET','POST'])
    def get_info():
        data =chartmogul.Metrics.mrr(config,
                        start_date='2019-01-01',
                        end_date='2019-04-30',
                        interval='month'
                        )              
        print(data.get()[0][0].mrr)
        jan = data.get()[0][0].mrr
        print(data.get()[0][1].mrr)
        feb = data.get()[0][1].mrr
        print(data.get()[0][2].mrr)
        mar = data.get()[0][2].mrr
        print(data.get()[0][3].mrr)
        apr = data.get()[0][3].mrr
        rev_add1 = Mrr(month="January", amount=jan)
        rev_add1.insert()
        rev_add2 = Mrr(month="February", amount = feb)
        rev_add2.insert()
        rev_add3 = Mrr(month="March", amount = mar)
        rev_add3.insert()
        rev_add4 = Mrr(month="April", amount=apr)
        rev_add4.insert()
        return jsonify({
            "success":True,
            "mon1" : "January",
            "amt1" : jan
        })

    @app.route('/showmrr', methods = ["GET"])
    def show_all():
        data = Mrr.query.all()
        formatted = [i.format() for i in data]
        return jsonify({
            "Success": True,
            "data": formatted
        })

    return app

    
    

app = create_app()
if __name__ == '__main__':
    app.run(port=5000,debug=True)
