
class Step():
    
    def __init__(self, step_num, next_steps, default_cost, default_time, step_amount):
        self.__step_num = step_num
        self._days_saved = 0
        """
        Args:   next_steps(list)
                prev_step(list)
                default_cost(float)
                default_time(int)
                step_amount(list of ints)
                acceleration(float) *for scaling price to time savings*
        """
        self._next_steps = next_steps
        self.__default_cost = default_cost
        self.__default_time = default_time
        self.__step_amount = step_amount

        self.__current_cost = default_cost

    def add_cost(self):
        if len(self.__step_amount) > self._days_saved + 1 and self._days_saved >= 0:
            self._days_saved += 1
            self.__current_cost += self.__step_amount[self._days_saved]
            

    def reduce_cost(self):
        if len(self.__step_amount) > self._days_saved and self._days_saved - 1 > 0:
            self._days_saved -= 1
            self.__current_cost -= self.__step_amount[self._days_saved]
        elif self._days_saved == 1:
            self._days_saved = 0
            self.__current_cost = self.__default_cost
            

    def get_cost(self):
        return self.__current_cost

    def get_time(self):
        return self.__default_time - self._days_saved

    def get_step_num(self):
        return self.__step_num

    def get_next(self):
        return self._next_steps

    def get_json(self):
        
        return {'step':self.get_step_num(), 'next':self.__get_next_json(), 'cost':self.get_cost(), 'time':self.get_time()}

    def __get_next_json(self):
        results = []
        for next_step in self._next_steps:
            results.append({'step':next_step.get_step_num(),'cost':next_step.get_cost(), 'time':next_step.get_time()})
        return results
# # testing stuff
# step1 = Step([], 300, 4, [100, 200, 400])

# print(f"start cost: {step1.get_cost()}")
# print(f"start time: {step1.get_time()} day(s)")
# step1.add_cost()
# print(f"after change cost: {step1.get_cost()}")
# print(f"after change time: {step1.get_time()} day(s)")