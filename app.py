
class Step():
    
    def __init__(self, next_step, prev_step, default_cost, default_time, step_amount, acceleration):
        """
        Args:   next_step(list)
                prev_step(list)
                default_cost(float)
                default_time(int)
                step_amount(int)
                acceleration(float) *for scaling price to time savings*
        """
        self._next_step = next_step
        self._prev_step = prev_step
        self.__default_cost = default_cost
        self.__default_time = default_time
        self.__step_amount = step_amount
        self.__acceleration = acceleration

        self.__current_cost = default_cost
        self.__current_time = default_time

    def add_cost(self):
        self.__current_cost += self.__step_amount
        self._calc_time()

    def _calc_time(self):
        self.__current_time -= self.__current_time ** (-self.__default_cost / self.__current_cost) * self.__acceleration

    def reduce_cost(self):
        self.__current_cost -= self.__step_amount
        self._calc_time()

    def get_cost(self):
        return self.__current_cost

    def get_time(self):
        return self.__current_time


step1 = Step([], [], 200, 6, 200, 3)

print(f"start cost: {step1.get_cost()}")
print(f"start time: {step1.get_time()} day(s)")
step1.add_cost()
print(f"after change cost: {step1.get_cost()}")
print(f"after change time: {step1.get_time()} day(s)")