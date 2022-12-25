import time
from step import Step

class Sim():

    def __init__(self, start_step, deadline, change_events):
        self.__start_step = start_step
        self.deadline = deadline
        self.__change_events = change_events

        self.time_remaining = deadline

        output = self._calc(self.__start_step, 0)
        self._current_cost = output['cost']
        self._current_time = output['time']

    def _calc(self, step, step_num):
        time = 0
        cost = 0
        step_num += 1

        if len(step.get_next()) > 0:
            for next_step in step.get_next():
                output = self._calc(next_step, step_num)
                time = output['time'] + step.get_time()
                cost = output['cost'] + step.get_cost()
    
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
            # time.sleep(2)
            self.time_remaining = (current_day - self._current_time) * -1

            print(f"day: {current_day}")
            print(f"cost: {self._current_cost}")
            print(f"time left: {self.time_remaining}")
            
            current_day += 1


# #testing stuff
# stepD = Step([], 70, 1, 2, 2)
# stepC = Step([stepD], 110, 4, 10, 1)
# stepB = Step([], 100, 4, 10, 1)
# stepA = Step([stepB, stepC], 200, 10, 5, 2)

# sim = Sim(stepA, 26, 0)

# sim.run()

