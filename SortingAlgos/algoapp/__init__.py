from flask import Flask, render_template
import os 

def create_app():

    # create the app
    # instance_relative_config=True: all the info is in the outside folder to keep it protected
    
    app = Flask(__name__, instance_relative_config=True)
    
    app.config.from_mapping(
            SECRET_KEY = 'dev', 
            DATABASE = os.path.join(app.instance_path, 'algoapp.sqlite'), )

    # check if the instance folder (the main folder) exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    

    # this is just the initial page
    @app.route('/')
    @app.route('/sorting&finding')
    def initial():
        labels = ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange']
        values = [12,13,8,6,15,10]
        graphdata = {'values':values, 'labels':values}
        return render_template('index.html', graphdata=graphdata)

    #register sorting blueprint
    from . import sorting
    app.register_blueprint(sorting.bp)


    return app
