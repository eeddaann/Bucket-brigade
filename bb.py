import numpy as np

HOURS = 8
DAYS = 18


class Picker:
    '''
    defines a employee
    '''

    def __init__(self,performance, rank):
        tf_mu, tf_variance, tb_mu, tb_variance, tp_mu, tp_variance = performance
        self.rank = rank  # relative position of picker to others
        self.cur_pick_face = 0  # reference to the current pick face
        self.cur_batch = None  # reference to the batch the employee make now
        self.busy_till = 0  # when it bigger then now, the picker is busy
        self.moving_direction = 1  # 1 if moves forward -1 else
        self.tf_mu = tf_mu  # expected value forward
        self.tf_sigma = np.sqrt(tf_variance)  # std forward
        self.tb_mu = tb_mu  # expected value backward
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

    def is_busy(self, now):
        # checks if picker's doing something
        self.busy_till = max(0,self.busy_till-0.0001)
        return self.busy_till >= now

    def pick_item(self, now):
        # pick one item
        if self.cur_batch[self.cur_pick_face]==0 :
            return
        self.cur_batch[self.cur_pick_face] -= 1
        self.busy_till = now + self.get_picking_time()
        if sum(self.cur_batch)==0:
            self.cur_batch=None

    def transfer(self, other,now):
        # makes transfer of bucket to other picker
        self.cur_batch, other.cur_batch = other.cur_batch, self.cur_batch
        self.moving_direction = self.moving_direction * -1
        other.moving_direction = other.moving_direction * -1

    def move(self, now):
        # moves the picker

        if self.moving_direction == 1:
            self.busy_till = now + self.get_forward_time()
            self.cur_pick_face += 1
        else:
            self.busy_till = now + self.get_backward_time()
            self.cur_pick_face -= 1
        pass


class simulation:
    def __init__(self,picksize,pickers,performance,data):
        #data = np.loadtxt(open("data/25p.csv", "rb"), delimiter=",", skiprows=1)
        self.batch_list = data
        self.pickers = []
        for rank in range(pickers):
            self.pickers.append(Picker(performance[rank],rank))
        self.picksize = picksize


    def check_behind_same_pickface(self, picker):
        # checks if there's someone behind who's free in the same pickface
        return picker.cur_pick_face == self.pickers[picker.rank - 1].cur_pick_face


    def run_config(self):
        now = 0

        while len(self.batch_list) > 0:  # and everyone finish

            for picker in self.pickers:
                if picker.is_busy(now):
                    continue

                if picker.cur_pick_face < 0:
                    picker.moving_direction = 1
                    picker.move(now)
                    break


                if picker.cur_batch is None:  # if batch is finished. Check in the beginning and in the end
                    if self.batch_list == []:
                        picker.cur_batch = []
                        break
                    else:
                        picker.cur_batch = self.batch_list[-1]
                        self.batch_list = self.batch_list[:-1]
                        picker.moving_direction = 1
                        break

                if picker.cur_pick_face > self.picksize:
                     picker.moving_direction = -1
                     picker.move(now)
                     break

                if picker.cur_pick_face >= self.picksize:
                   picker.cur_pick_face = 0

                if picker.cur_batch[picker.cur_pick_face] > 0:  # if need to pick from pickface - pick
                     picker.pick_item(now)
                     break

                if self.check_behind_same_pickface(
                        picker) and picker.moving_direction == -1:  # if the someone behind is at the same pickface
                     if not self.pickers[picker.rank - 1].is_busy(now):  # if the someone behind is free
                        picker.transfer(self.pickers[picker.rank - 1], now)
                     else:  # if he is busy the picker should wait for him
                        continue

                else:
                    picker.move(now)

            now += 0.0001

        return now  # time that loop took


#print "Hello, results for 6p: ", simulation().run_config()
