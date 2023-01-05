from sim import Sim
from step import Step
from flask import Flask, request, redirect, render_template, url_for, jsonify

app = Flask(__name__)

#Sim
end = Step(44, [], 0, 0, [0])
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
step32 = Step(32, [step42], 61660, 21, [340, 360, 410, 460, 520, 580, 670, 760])
step31 = Step(31, [step39], 91250, 16, [750])
step30 = Step(30, [step37, step36], 85450, 22, [500, 550, 600, 670, 750, 850, 960, 1090, 1270])
step29 = Step(29, [step36, step37], 41660, 18, [690, 770, 880, 1000, 1150, 1350, 1590])
step28 = Step(28, [step36, step37], 112220, 18, [720, 810, 910, 1050, 1210, 1410, 1670, 2000, 2440])
step27 = Step(27, [step35, step34, step33], 103040, 23, [590, 650, 720, 780, 880, 980, 1110])
step26 = Step(26, [step31], 71810, 22, [330, 360, 390, 440, 490, 550, 630, 710])
step25 = Step(25, [step32, step40], 61420, 21, [580, 630, 700, 780])
step24 = Step(24, [step31], 63330, 18, [780, 890, 1000, 1140, 1320, 1540, 1810, 2190, 2660, 3340])
step23 = Step(23, [step38], 69040, 21, [460, 500, 550, 620, 700, 790])
step22 = Step(22, [step26, step27], 7000, 5, [1000, 1660])
step21 = Step(21, [step25, step29], 20000, 3, [0])
step20 = Step(20, [step26], 1500, 1, [0])
step19 = Step(19, [step25, step29], 134160, 24, [4530, 4940, 5410, 5960, 5410, 5960, 6570, 7310, 8170, 9200, 10410])
step18 = Step(18, [step28, step24], 4830, 3, [1670])
step17 = Step(17, [step38], 270730, 41, [4270, 4480, 4730, 4970, 5260, 5880, 6240, 6630, 7050, 7530, 8040, 8630])
step16 = Step(16, [step22], 37500, 15, [0])
step15 = Step(15, [step23, step30, step20], 256570, 19, [7310, 8170, 9200, 10410, 11910, 13730])
step14 = Step(14, [step22], 162500, 16, [4160, 4760, 5500, 6410, 7570, 9100])
step13 = Step(13, [step22], 70620, 16, [1040, 1190, 1380, 1600, 1890])
step12 = Step(12, [step21, step18], 97630, 19, [2920, 3270])
step11 = Step(11, [step15], 383330, 15, [23810, 27470, 32050, 37880])
step10 = Step(10, [step14, step19], 7500, 22, [0])
step9 = Step(9, [step13], 83150, 19, [730, 820, 920, 1040, 1190])
step8 = Step(8, [step12], 36110, 18, [650, 740])
step7 = Step(7, [step9, step8], 4830, 3, [1670])
step6 = Step(6, [step12], 35710, 21, [290, 310, 400, 390, 440, 500, 570, 660, 770])
step5 = Step(5, [step16, step17], 184840, 33, [2660, 2820])
step4 = Step(4, [step10, step11], 26230, 13, [770, 900, 1100, 1330])
step3 = Step(3, [step9], 33420, 14, [500, 580, 680, 820, 1000, 1250, 1600])
step2 = Step(2, [step6, step7], 5000, 9, [0])
step1 = Step(1, [step2, step3, step4, step5], 10000, 4, [0])

sim = Sim(step1, 107, 0)
#Routes
@app.route("/")
def render_sim():
    return render_template("index.html")

@app.route('/sim', methods=["POST", "GET"])
def get_sim_data():
    #main app
    if request.method == "GET":
        start_step = sim.get_start()

        steps = sim.get_json(start_step, start_step.get_step_num())
        steps["num_steps"] = len(steps.keys())

        # context = {
        #     "steps":json,
        #     "num_steps":len(steps.keys())
        # }

        return jsonify(steps)
       

if __name__ == '__main__':
    app.run(debug=True)