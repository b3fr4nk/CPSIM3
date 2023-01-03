
class Step():
    
    def __init__(self, next_steps, default_cost, default_time, step_amount):
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
        self.__current_cost += self.__step_amount[self._days_saved]
        self._days_saved += 1

    def reduce_cost(self):
        self.__current_cost -= self.__step_amount
        self._days_saved += 1
    def get_cost(self):
        return self.__current_cost

    def get_time(self):
        return self.__default_time - self._days_saved

    def get_next(self):
        return self._next_steps
# testing stuff
step1 = Step([], 300, 4, [100, 200, 400])

print(f"start cost: {step1.get_cost()}")
print(f"start time: {step1.get_time()} day(s)")
step1.add_cost()
print(f"after change cost: {step1.get_cost()}")
print(f"after change time: {step1.get_time()} day(s)")