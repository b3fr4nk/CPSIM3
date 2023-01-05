import time
from step import Step

class Sim():

    def __init__(self, start_step, deadline, change_events):
        self.__start_step = start_step
        self.deadline = deadline
        self.__change_events = change_events #TODO implement change events

        self.time_remaining = deadline

        output = self._calc(self.__start_step, 0)
        self._current_cost = output['cost']
        self._current_time = output['time']

    def get_start(self):
        return self.__start_step

    def _get_steps_dict(self, step):
        steps = {f"{step.get_step_num}":step}

        for next_step in step.get_next():
            output = self._get_steps_dict(next_step)
            steps.update(output)

        return steps

    def get_json(self, step, step_num):
        results = {}

        steps = self._get_steps_dict(step)

        for step in steps.keys():
            step_json = steps[step].get_json()
            results[f'{step_json["step"]}'] = step_json

        return results

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

    
    def run(self):
        current_day = 0

        while current_day < self._current_time:
            output = self._calc(self.__start_step, 0)
            self._current_cost = output['cost']
            self._current_time = output['time']
            self.time_remaining = (current_day - self._current_time) * -1

            print(f"day: {current_day}")
            print(f"cost: {self._current_cost}")
            print(f"time left: {self.time_remaining}")
            
            current_day += 1


#testing stuff
# stepD = Step([], 70, 1, [25, 30, 50])
# stepC = Step([stepD], 110, 5, [30, 45, 50])
# stepB = Step([], 100, 4, [30, 50, 60])
# stepA = Step([stepB, stepC], 200, 1, [70, 90, 110, 150])

# sim = Sim(stepA, 26, 0)

# sim.run()