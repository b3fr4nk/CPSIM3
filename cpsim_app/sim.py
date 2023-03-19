import time
from cpsim_app.step import Step
import json

class Sim():
    """
    used to process each step
    """

    def __init__(self, start_step, deadline, change_events):
        self.__start_step = start_step
        self.deadline = deadline
        self.__change_events = change_events #TODO implement change events

        self._time_remaining = deadline
        self._cpath = []

        self._steps = self.get_steps_dict(self.__start_step)

        output = self.calc(1)
        self._current_cost = output['cost']
        self._current_time = output['time']
        self.__current_day = 0

    def get_start(self):
        return self.__start_step

    def get_steps_dict(self, step):
        steps = {f"{step.get_step_num()}":step}

        for next_step in step.get_next():
            output = self.get_steps_dict(next_step)
            steps.update(output)

        return steps

    def get_json(self, step1, step_num):
        results = {}

        steps = self._steps

        for step in steps.keys():
            step_json = steps[step].get_json()
            results[f'{step_json["step"]}'] = step_json

        return results

    def load_json(self, file_path):
        file = open(file_path, 'r')
        sim_data = json.load(file)
        file.close

        temp_steps_dict = {}
        end = Step(44, [], 0, 0, [])

        temp_steps_dict['44'] = end
        

        for step_key in range(len(self._steps.keys()) -1 , 0, -1):
            step = sim_data[f'{step_key}']
            print(step)
            next_steps_list = []
            
            for next_step in step['next']:
                next_steps_list.append(temp_steps_dict[f'{next_step["step"]}'])
            new_step = Step(step['step'], next_steps_list, self._steps[f'{step_key}'].get_cost(), self._steps[f'{step_key}'].get_time(), [0])
            temp_steps_dict[f'{step_key}'] = new_step

        self._steps = temp_steps_dict

    def step_from_dict(self, dict, next_steps):
        step = Step(dict['step'], next_steps)

        return step

    def update_step(self, step_num, isAdd):
        step = self.__start_step

        if isAdd:
            self._steps[step_num].add_cost()
        else:
            self._steps[step_num].reduce_cost()

        self._steps = self.get_steps_dict(self.get_start())

    def calc(self, step_num):
        time = 0
        cost = 0

        time_out = self._calc_time(step_num)
        self._cPath = time_out[1] #index 1 is list of step numbers for critical path
        time = time_out[0]
        cost = self._calc_cost()

        self._current_cost = cost
        self._current_time = time
            
        return {"time":time, "cost":cost, "step":step_num}

    def get_cPath(self):
        return self._cPath

    def get_time(self):
        return self._current_time

    def get_cost(self):
        return self._current_cost

    def _calc_cost(self):
        cost = 0
        for i in range(len(self._steps.keys())-1):
            cost += self._steps[f"{i+1}"].get_cost()

        return cost

    def _calc_time(self, step_num, time=0):
        curr_time = time + self._steps[f"{step_num}"].get_time()
        next_time = curr_time
        cPath = [step_num]
        
        if len(self._steps[f"{step_num}"].get_next()) > 0:
            fast_time = curr_time + self._steps[f"{step_num}"].get_next()[0].get_time()
            for next_step in self._steps[f"{step_num}"].get_next():

                output = self._calc_time(next_step.get_step_num(), time = curr_time)
                temp_time = output[0]
                
                if temp_time > next_time:
                    next_time = temp_time

                    cPath = output[1]
                    cPath.append(step_num)
                if temp_time < fast_time:
                    fast_time = temp_time
        
            # self._steps[f"{step_num}"].set_slack(self._calc_slack(fast_time, next_time))
        
        return [next_time, cPath]
        

    def _calc_slack(self, fast, slow):
        return slow - fast

    def join_list(self, list1, list2):
        for item in list2:
            list1.append(item)
        return list1
    def next_day(self):

        time_left = self.deadline - self.__current_day

        if time_left > 0:
            output = self.calc(1)
            self._current_cost = output['cost']
            self._current_time = output['time']
            self._time_remaining = self._current_time - self.__current_day
            
            self.__current_day += 1

            return {"running":True, "cost":self._current_cost, "time":self._time_remaining, "deadline":time_left}

        return {"running":False, "cost":self._current_cost, "time":self.__current_day, "deadline":time_left}


#testing stuff
# step7 = Step(7, [], 0, 3, [0])
# step6 = Step(6, [step7], 0, 2, [0])
# step5 = Step(5, [step7], 0, 1, [0])
# step4 = Step(4, [step6], 0, 3, [0])
# step3 = Step(3, [step5, step7], 0, 2, [0])
# step2 = Step(2, [step3], 0, 2, [0])
# step1 = Step(1, [step2, step3, step4], 0, 1, [0])


# sim = Sim(step1, 100, 0)

# print(sim.get_time())