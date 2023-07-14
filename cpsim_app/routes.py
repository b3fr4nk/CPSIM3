from cpsim_app.sim import Sim
from cpsim_app.step import Step
from cpsim_app.event import Event
from flask import Blueprint, request, render_template, redirect, url_for, flash
from datetime import date, datetime
from cpsim_app.models import User, SimDoc
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
import json
from cpsim_app.forms import LoginForm, SignUpForm
import os
import pickle

from cpsim_app.extensions import db, app, bcrypt

main = Blueprint("main", __name__)
auth = Blueprint("auth", __name__)

#Sim
end = Step(44, [], 0, 0, [])
step43 = Step(43, [end], 71360, 22, [540, 600, 650, 730, 820])
step42 = Step(42, [end], 157500, 20, [920, 1020, 1140, 1290])
step41 = Step(41, [end], 82720, 22, [1080, 1200, 1310, 1460, 1640, 1840, 2080])
step40 = Step(40, [step41], 118420, 19, [1020, 1140, 1290, 1460, 1670, 1920, 2240])
step39 = Step(39, [end], 36500, 20, [340, 380, 420, 480, 540, 620])
step38 = Step(38, [step43], 81900, 21, [600, 650, 730, 820, 920, 1040, 1190, 1380, 1600])
step37 = Step(37, [step43], 73880, 18, [820, 920])
step36 = Step(36, [step42], 238230, 17, [5520, 6250])
step35 = Step(35, [step43], 67220, 18, [420, 480, 540, 620, 720, 830, 980, 1190, 1440])
step34 = Step(34, [step42], 95000, 17, [620, 710, 810, 930, 1090])
step33 = Step(33, [step41], 132770, 18, [750, 850, 960, 1090])
step32 = Step(32, [step42], 61660, 19, [340, 360, 410, 460, 520, 580, 670, 760])
step31 = Step(31, [step39], 91250, 16, [750])
step30 = Step(30, [step37, step36], 85450, 22, [500, 550, 600, 670, 750, 850, 960, 1090, 1270])
step29 = Step(29, [step36, step37], 41660, 18, [690, 770, 880, 1000, 1150, 1350, 1590])
step28 = Step(28, [step36, step37], 112220, 18, [720, 810, 910, 1050, 1210, 1410, 1670, 2000, 2440])
step27 = Step(27, [step35, step34, step33], 103040, 23, [590, 650, 720, 780, 880, 980, 1110])
step26 = Step(26, [step31], 71810, 22, [330, 360, 390, 440, 490, 550, 630, 710])
step25 = Step(25, [step32, step40], 61420, 19, [580, 630, 700, 780])
step24 = Step(24, [step31], 63330, 18, [780, 890, 1000, 1140, 1320, 1540, 1810, 2190, 2660, 3340])
step23 = Step(23, [step38], 69040, 21, [460, 500, 550, 620, 700, 790])
step22 = Step(22, [step26, step27], 7000, 5, [1000, 1660])
step21 = Step(21, [step25, step29], 20000, 3, [])
step20 = Step(20, [step26], 1500, 1, [])
step19 = Step(19, [step25, step29], 134160, 23, [4530, 4940, 5410, 5960, 5410, 5960, 6570, 7310, 8170, 9200, 10410])
step18 = Step(18, [step28, step24], 4830, 3, [1670])
step17 = Step(17, [step38], 270730, 41, [4270, 4480, 4730, 4970, 5260, 5880, 6240, 6630, 7050, 7530, 8040, 8630])
step16 = Step(16, [step22], 37500, 15, [])
step15 = Step(15, [step23, step30, step20], 256570, 19, [7310, 8170, 9200, 10410, 11910, 13730])
step14 = Step(14, [step22], 162500, 16, [4160, 4760, 5500, 6410, 7570, 9100])
step13 = Step(13, [step22], 70620, 16, [1040, 1190, 1380, 1600, 1890])
step12 = Step(12, [step21, step18], 97630, 19, [2920, 3270])
step11 = Step(11, [step15], 383330, 15, [23810, 27470, 32050, 37880])
step10 = Step(10, [step14, step19], 7500, 22, [])
step9 = Step(9, [step13], 83150, 19, [730, 820, 920, 1040, 1190])
step8 = Step(8, [step12], 36110, 18, [650, 740])
step7 = Step(7, [step9, step8], 4830, 3, [1670])
step6 = Step(6, [step12], 35710, 21, [290, 310, 400, 390, 440, 500, 570, 660, 770])
step5 = Step(5, [step16, step17], 184840, 33, [2660, 2820])
step4 = Step(4, [step10, step11], 26230, 13, [770, 900, 1100, 1330])
step3 = Step(3, [step9], 33420, 14, [500, 580, 680, 820, 1000, 1250, 1600])
step2 = Step(2, [step6, step7], 5000, 9, [])
step1 = Step(1, [step2, step3, step4, step5], 10000, 4, [])

random_events = [Event(3, 25, 14), Event(1, 31, 35), Event(4, 74, 43)]
sim = Sim(step1, 107, random_events)
start_step = sim.get_start()
steps = sim.get_json()


def save_sim():
    file_path = f'{os.path.join(app.config["SIM_FOLDER"])}{current_user.id}.pkl'
    with open(file_path, 'wb') as outp:
        pickle.dump(sim, outp, pickle.HIGHEST_PROTOCOL)

def load_sim():
    file_path = f'{os.path.join(app.config["SIM_FOLDER"])}{current_user.id}.pkl'
    with open(file_path, 'rb') as inp:
        global sim
        sim = pickle.load(inp)

#Routes
@main.route("/")
def render_sim():
    return render_template("index.html")

@main.route('/sim', methods=["GET"])
@login_required
def get_sim_data():
    #TODO allow users to use sim without logging in 
    global steps
    #sends json of sim to frontend
    steps = sim.get_json()
    steps["num_steps"] = len(steps.keys())
    steps["days"] = sim.get_time()
    steps["path"] = sim.get_cPath()
    steps["cost"] = sim.get_cost()
    steps["time"] = sim.get_time()
    
    return steps


@main.route('/update', methods=["POST"])
@login_required
def update_sim():
    if request.method == "POST":
        json = request.get_json()

        step_num = json["step_num"]
        is_add = json["isAdd"]
        if is_add is not None and step_num is not None:
            sim.update_step(step_num, is_add)
            sim.calc(1)
        save_sim()

    return get_sim_data()

@main.route('/progress', methods=["POST"])
@login_required
def progress():
    if request.method == "POST":
        json = request.get_json()
        if json["next"]:
            sim.next_day()
            if not sim.running:
                save_sim()
                sim_doc = SimDoc.query.filter_by(user_id=current_user.id).first()
                sim_doc.cost = sim.get_cost()
                sim_doc.time = sim.get_time()

                db.session.add(sim_doc)
                db.session.commit()
                
        return get_sim_data()

@main.route('/grades', methods=['GET'])
@login_required
def show_results():
    if current_user.is_teacher:
        students = User.query.filter_by(is_teacher=False, class_code=current_user.class_code).all()
        names = []
        sims = []
        for student in students:
            sim = SimDoc.query.filter_by(user_id=student.id).first()
            sims.append(sim)
            names.append(student)
        
        context = {
            'students':names,
            'sims':sims
        }

        print(context)

        return render_template('grades.html', **context)      

@main.route('/results', methods=['GET'])
@login_required
def show_single_results():
    return render_template('finish.html', cost = sim.get_cost())

@auth.route('/signup', methods=['POST', 'GET'])
def signup():
    form = SignUpForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        
        user = User(school_email=form.email.data, password=hashed_password, class_code=form.class_code.data, is_teacher=False) # TODO add better is teacher logic
        file_path = f'{os.path.join(app.config["SIM_FOLDER"])}{user.id}.pkl'
        

        db.session.add(user)
        db.session.commit()

        user_sim = SimDoc(doc=file_path, time=121, cost=3820220, user_id=user.id)
        db.session.add(user_sim)
        db.session.commit()

        return redirect(url_for('auth.login'))

    return render_template('signup.html', form=form)

@auth.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    
    if form.validate_on_submit():
        user = User.query.filter_by(school_email=form.email.data).first()
        if user:

            login_user(user, remember=True)

            global file_path

            file_path = f'{os.path.join(app.config["SIM_FOLDER"])}{current_user.id}.json'
            try:
                load_sim()
            except FileNotFoundError:
                save_sim()

            return redirect(url_for('main.render_sim'))

    return render_template('login.html', form=form)

@auth.route('/logout', methods=['POST', 'GET'])
def logout():
    logout_user()

    return redirect(url_for('main.render_sim'))