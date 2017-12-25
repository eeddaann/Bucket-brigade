import numpy as np

HOURS = 8
DAYS = 18



class Picker:
    '''
    defines a employee
    '''


    def __init__(self, tf_mu, tf_variance, tb_mu, tb_variance, tp_mu, tp_variance):
        self.rank = None  # relative position of picker to others
        self.cur_pick_face = None  # reference to the current pick face
        self.cur_batch = None  # reference to the batch the employee make now
        self.tf_mu = tf_mu  # expected value forward
        self.tf_sigma = np.sqrt(tf_variance)  # std forward
        self.tb_mu = tb_mu# expected value backward
        self.tb_sigma = np.sqrt(tb_variance)  # std backward
        self.tp_mu = tp_mu  # expected value picking
        self.tp_sigma = np.sqrt(tp_variance)  # std picking

    def get_forward_time(self):
        # sample time for task
        return max(0, np.random.normal(self.tf_mu, self.tf_sigma)) + 0.01

    def get_backward_time(self):
        # sample time for task
        return max(0, np.random.normal(self.tb_mu, self.tb_sigma)) + 0.01

    def get_picking_time(self):
        # sample time for task
        return max(0, np.random.normal(self.tp_mu, self.tp_sigma)) + 0.01

    def is_busy(self,now):
        # checks if picker's doing something
        pass

    def pick_item(self):
        #pick one item
        pass

    def check_behind_same_pickface(self):
        #checks if there's someone behind who's free in the same pickface
        pass

    def transfer(self,other):
        #makes transfer of bucket to other picker
        pass



class Batch:
    def __init__(self, start, expected_time):
        self.original_list = []

    def is_done(self):
        #check if specific batch is done
        pass


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




class simulation:
    def __init__(self, config):
        self.config = config
        self.disp = dispatcher(self.config)
        self.cur_products = {}
        self.daily_total = []
        self.batch_list = [[1,2,2,3,6,5],[2,3,2,6,5,4],[1,5,3,1,2,5]]
        emp1 = Picker(1, 0.2, 0.5, 0.1, 1.4, 2)
        emp2 = Picker(1, 0.2, 0.5, 0.1, 1.4, 2)
        emp3 = Picker(1, 0.2, 0.5, 0.1, 1.4, 2)
        self.pickers=[emp1,emp2,emp3]


    def run_config(self):
        now = 0
        #TODO: make changes

        while len(self.batch_list)>0: #and everyone finish
            for picker in self.pickers:
                if picker.is_busy(now):
                    break
                if picker.cur_batch==None: #if batch is finished. Check in the beginning and in the end
                    picker.cur_batch=self.batch_list[-1]
                if picker.check_behind_same_pickface():
                    picker.transfer(self,other)
                    pass
                if picker.cur_batch[picker.cur_pick_face]!=0:
                    picker.pick_item()
                    pass




            pass





        return now #time that loop took








'''config_dict = {1: ("Parallel:1,2,3", configuration([], [emp1, emp2, emp3])),
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
               13: ("bb:3,1,2", configuration([emp3, emp1, emp2], []))}'''


def calc(config):
    temp = 0
    temp += sum(simulation(config).run_config())
    return float(temp) / DAYS


input = 0
'''while input != 'x':
    for key in config_dict:
        print(key, config_dict[key][0])
    input = raw_input("choose config: (1,2..,13. x to exit)")

    print(config_dict[int(input)][0] + "->  " + str(calc(config_dict[int(input)][1])))'''
