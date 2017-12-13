import numpy as np

HOURS = 8
DAYS = 18
DISCRETIZATION_FACTOR = 1  # the larger, the more accurate, defines the atomic time unit of the simulation. for example 60 means that each iteration in the model is a second.


class Picker:
    '''
    defines a employee
    '''

    def __init__(self, tf_mu, tf_variance, tb_mu, tb_variance, tp_mu, tp_variance, name):
        self.name = name
        self.tf_mu = tf_mu * DISCRETIZATION_FACTOR  # expected value forward
        self.tf_sigma = np.sqrt(tf_variance) * DISCRETIZATION_FACTOR  # std forward
        self.tb_mu = tb_mu * DISCRETIZATION_FACTOR  # expected value backward
        self.tb_sigma = np.sqrt(tb_variance) * DISCRETIZATION_FACTOR  # std backward
        self.tp_mu = tp_mu * DISCRETIZATION_FACTOR  # expected value picking
        self.tp_sigma = np.sqrt(tp_variance) * DISCRETIZATION_FACTOR  # std picking
        self.cur_batch = None  # the product that the employee make now
        self.finished = 0  # how many products that employee made

    def get_forward_time(self):
        # sample time for task
        return max(0,np.random.normal(self.tf_mu, self.tf_sigma))+0.01
    def get_backward_time(self):
        # sample time for task
        return max(0, np.random.normal(self.tb_mu, self.tb_sigma)) + 0.01
    def get_picking_time(self):
        # sample time for task
        return max(0, np.random.normal(self.tp_mu, self.tp_sigma)) + 0.01



class Batch:
    def __init__(self, start, expected_time):
        self.progress = 0
        self.start = start
        self.expected_time = expected_time
        self.finished = False

    def update_expected_time(self, new_expected_time):
        # when speed changed
        self.expected_time = (1 - self.progress) * new_expected_time

    def update_state(self, now):
        self.progress = float(now - self.start) / self.expected_time
        if self.progress >= 1:
            self.finished = True

    def copy_state(self, other):
        # for bb
        self.progress = other.progress
        self.expected_time = other.expected_time

    def transfer(self, other):
        # switch products between employees
        self.progress, other.progress = other.progress, self.progress
        self.start, other.start = other.start, self.start
        other.update_expected_time(other.expected_time)
        self.update_expected_time(self.expected_time)


class dispatcher:
    '''
    orchastrate the employees and products
    '''

    def __init__(self, config):
        self.bb_order = config.config['bb'][:]
        self.employee_lst = config.config['bb']
        self.employee_lst.extend(config.config['par'])

    def new_day(self, now):
        #################################################################
        # we assume that progress saved on each day and workers continue #
        # from where they stopped. but they start each day with new speed#
        #################################################################
        print(str([emp.name + ": " + str(emp.finished) for emp in self.employee_lst]))
        if self.employee_lst[0].cur_batch == None:  # if start of simulation
            for employee in self.employee_lst:
                employee.cur_batch = Batch(now, employee.get_forward_time())
        else:  # if regular day
            for employee in self.employee_lst:
                employee.cur_batch.update_expected_time(employee.get_forward_time())

    def new_product(self, emp, now):
        emp.finished += 1
        emp.cur_batch = Batch(emp.get_forward_time(), now)

    def check_order(self, sorted_by_prog_old):
        # check if two employees met and do the bb
        if self.bb_order == []:  # if all employees in parallel
            return True
        else:
            sorted_by_prog = sorted(self.bb_order, key=lambda emp: emp.cur_batch.progress)
            if sorted_by_prog_old == sorted_by_prog:  # if order not changed
                return True
            else:
                # they switch places
                if sorted_by_prog[:1] == self.bb_order[:1]:
                    sorted_by_prog[1].cur_batch.transfer(sorted_by_prog[0].cur_batch)
                else:
                    # forbidden switch
                    sorted_by_prog[0].cur_batch.copy_state(sorted_by_prog[1].cur_batch)

                if len(self.bb_order) == 3:
                    # they switch places
                    if sorted_by_prog[1:2] == self.bb_order[1:2]:
                        sorted_by_prog[2].cur_batch.transfer(sorted_by_prog[1].cur_batch)
                    else:
                        # forbidden switch
                        sorted_by_prog[2].cur_batch.copy_state(sorted_by_prog[1].cur_batch)



class configuration:
    def __init__(self, bb, par):
        self.config = {'bb': bb, 'par': par}


class simulation:
    def __init__(self, config):
        self.config = config
        self.disp = dispatcher(self.config)
        self.cur_products = {}
        self.daily_total = []

    def run_config(self):
        now = 0
        daily_counter = 0
        self.disp.new_day(now)
        for emp in self.disp.employee_lst:
            self.cur_products[emp.cur_batch] = emp
        for day in range(DAYS):
            for time_unit in range(HOURS * 60 * DISCRETIZATION_FACTOR):
                for product in self.cur_products.keys():
                    sorted_by_prog_old = sorted(self.disp.bb_order, key=lambda emp: emp.cur_batch.progress)
                    product.update_state(now)
                    self.disp.check_order(sorted_by_prog_old)
                    if product.finished == True:
                        emp = self.cur_products[product]
                        self.disp.new_product(emp, now)
                        del self.cur_products[product]
                        self.cur_products[emp.cur_batch] = emp
                        daily_counter += 1

                now += 1
            self.daily_total.append(daily_counter)
            daily_counter = 0
            self.disp.new_day(now)

        return self.daily_total


emp1 = Picker(1,0.2,0.5,0.1,1.4,2,'a')
emp2 = Picker(1,0.2,0.5,0.1,1.4,2, 'b')
emp3 = Picker(1,0.2,0.5,0.1,1.4,2, 'c')

config_dict = {1: ("Parallel:1,2,3", configuration([], [emp1, emp2, emp3])),
               2: ("bb:1,2,Parallel:3", configuration([emp1, emp2], [emp3])),
               3: ("bb:1,3,Parallel:2", configuration([emp1, emp3], [emp2])),
               4: ("bb:3,2,Parallel:1", configuration([emp3, emp2], [emp1])),
               5: ("bb:3,1,Parallel:2", configuration([emp3, emp1], [emp2])),
               6: ("bb:2,3,Parallel:1", configuration([emp2, emp3], [emp1])),
               7: ("bb:2,1,Parallel:3", configuration([emp2, emp1], [emp3])),
               8: ("bb:1,2,3", configuration([emp1, emp2, emp3], [])),
               9: ("bb:3,2,1", configuration([emp3, emp2, emp1], [])),
               10: ("bb:1,3,2", configuration([emp1, emp3, emp2], [])),
               11: ("bb:2,1,3", configuration([emp2, emp1, emp3], [])),
               12: ("bb:2,3,1", configuration([emp2, emp3, emp1], [])),
               13: ("bb:3,1,2", configuration([emp3, emp1, emp2], []))}


def calc(config):
    temp = 0
    temp += sum(simulation(config).run_config())
    return float(temp) / DAYS


input = 0
while input != 'x':
    for key in config_dict:
        print(key, config_dict[key][0])
    input = raw_input("choose config: (1,2..,13. x to exit)")

    print(config_dict[int(input)][0] + "->  " + str(calc(config_dict[int(input)][1])))

