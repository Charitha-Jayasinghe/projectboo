import logging
from flask import Flask, session, redirect, url_for, request, render_template, render_template_string, Response, jsonify, Blueprint
import os
from functools import wraps
from apscheduler.schedulers.background import BackgroundScheduler
import subprocess

app = Flask(__name__)
app.secret_key = '59fa31e2-70c6-4da2-9913-64944d2bce59'
app.config['DEBUG'] = True 

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


routes_blueprint = Blueprint('routes', __name__)


@routes_blueprint.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username is None or password is None:
            return 'Missing credentials', 400

        if username == 'abc@gmail.com' and password == 'testck':
            session['logged_in'] = True
            return redirect(url_for('routes.home'))
        else:
            return 'Invalid credentials', 401
    
    return render_template('login.html')


@routes_blueprint.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('routes.login'))


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('routes.login'))
        return f(*args, **kwargs)
    return decorated_function


@routes_blueprint.route('/home') 
@login_required
def home():
    return render_template('home.html')


@routes_blueprint.route('/test-results-dev/')
@login_required
def results_dev():
    results_path = './development_Test_Results.html'
    if os.path.exists(results_path):
        with open(results_path, 'r') as file:
            html_content = file.read()
        return render_template_string(html_content)
    return jsonify({"error": "Test results file not found"}), 404

@routes_blueprint.route('/test-results-prod/')
@login_required
def results_prod():
    results_path = './production_Test_Results.html'
    if os.path.exists(results_path):
        with open(results_path, 'r') as file:
            html_content = file.read()
        return render_template_string(html_content)
    return jsonify({"error": "Test results file not found"}), 404

@routes_blueprint.route('/test-results-performance/')
@login_required
def results_performance():
    results_path = './locust_report.html'
    if os.path.exists(results_path):
        with open(results_path, 'r') as file:
            html_content = file.read()
        return Response(html_content, mimetype='text/html')
    return jsonify({"error": "Test results file not found"}), 404

@routes_blueprint.route('/run-production-tests', methods=['POST'])
@login_required
def trigger_production_tests():
    run_production_tests()
    return jsonify({"message": "Production Health Check Completed. Check The Report For More Details."})

@routes_blueprint.route('/run-development-tests', methods=['POST'])
@login_required
def trigger_development_tests():
    run_development_tests()
    return jsonify({"message": "Development Regression Test Run Completed.Check The Report For More Details."})


app.register_blueprint(routes_blueprint)


def run_production_tests():
    logger.debug("Running production tests...")
    subprocess.run(['pytest', '-m', 'production', '--html=production_Test_Results.html', '--self-contained-html'])
    logger.debug("Production tests completed.")

def run_development_tests():
    logger.debug("Running development tests...")
    subprocess.run(['pytest', '-m', 'staging', '--html=development_Test_Results.html', '--self-contained-html'])
    logger.debug("Development tests completed.")




def schedule_jobs():
    logger.debug("Scheduling jobs...")
    scheduler = BackgroundScheduler()
    
    scheduler.add_job(run_production_tests, 'cron', minute=15, hour='*', misfire_grace_time=300)
    scheduler.add_job(run_staging_tests, 'cron', hour='8,12,16,22', minute=30, misfire_grace_time=300)
    

    scheduler.start()
    logger.debug("Scheduler started.")

schedule_jobs()
logger.debug("Application setup complete.")


if __name__ == '__main__':
    app.run()
