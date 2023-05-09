from flask import Flask, render_template, request, redirect, send_file
from hh import get_jobs, save_data_to_csv
app = Flask('JobScrapper')
db = {}

# main page
@app.route('/')
def home():
    return render_template('home.html')


# report page
@app.route('/report')
def report():
    keyword = request.args.get('keyword')
    if keyword is not None:
        keyword = keyword.lower()
        getDB = db.get(keyword)
        if getDB:
            jobs = getDB
        else:
            jobs = get_jobs(keyword)
            db[keyword] = jobs
        print(jobs)
    else:
        return redirect('/')
    return render_template('report.html', searchBy=keyword, count_jobs=len(jobs), jobs=jobs)


# page for download CSV file
@app.route('/export')
def export():
    try:
        keyword = request.args.get('keyword')
        if not keyword:
            raise Exception()
        keyword = keyword.lower()
        jobs = db.get(keyword)
        if not jobs:
            raise Exception()
        save_data_to_csv(jobs)
        return send_file('HeadHunter.csv')
    except:
        return ('/')


app.run(host='0.0.0.0') # run aplication