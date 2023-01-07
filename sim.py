import time
from step import Step

class Sim():

    def __init__(self, start_step, deadline, change_events):
        self.__start_step = start_step
        self.deadline = deadline
        self.__change_events = change_events #TODO implement change events

        self.time_remaining = deadline

        self._steps = self.get_steps_dict(self.__start_step)

        output = self._calc(self.__start_step, 0)
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

    def get_json(self, step, step_num):
        results = {}

        steps = self._steps

        for step in steps.keys():
            step_json = steps[step].get_json()
            results[f'{step_json["step"]}'] = step_json

        return results

    def update_step(self, step_num, isAdd):
        if isAdd:
            self._steps[step_num].add_cost()
        else:
            self._steps[step_num].reduce_cost()

    def _calc(self, step, step_num):
        time = 0
        cost = 0
        step_num += 1

       #if not last step
        if len(step.get_next()) > 0:
            #recursively gets all steps and set time and cost
            for next_step in step.get_next():
                output = self._calc(next_step, step_num)
                time = output['time'] + step.get_time()
                cost = output['cost'] + step.get_cost()
        #if this is the last step set time and cost
        else:
            time = step.get_time()
            cost = step.get_cost()
                
            

        return {"time":time, "cost":cost, "step":step_num}

    
    def next_day(self):

        if self.__current_day < self._current_time:
            output = self._calc(self.__start_step, 0)
            self._current_cost = output['cost']
            self._current_time = output['time']
            self.time_remaining = (current_day - self._current_time) * -1

            print(f"day: {current_day}")
            print(f"cost: {self._current_cost}")
            print(f"time left: {self.time_remaining}")
            
            self.__current_day += 1


#testing stuff
# step1 = Step(1, [], 100, 1, [100, 200])

# sim = Sim(step1, 26, 0)

# print(sim.get_json(step1, f"{step1.get_step_num()}"))
# sim.update_step(f"{step1.get_step_num()}", False)
# print(sim.get_json(step1, f"{step1.get_step_num()}"))
