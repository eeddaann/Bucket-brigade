from bb import simulation
from bin_packing import pack

class configuration:
    def __init__(self,picksize,pickers,performance,capacity):
        self.picksize = picksize
        self.pickers = pickers
        self.performance = performance
        self.capacity = capacity
        self.performance_d = {'a': [1, 0.2, 0.5, 0.1, 1.4, 2],'b':[]}

#tf_mu, tf_variance, tb_mu, tb_variance, tp_mu, tp_variance
    def run_config(self):
        data = pack(self.capacity,self.picksize)
        return simulation(self.picksize,self.pickers,self.performance_d[self.performance],data).run_config()

    def __repr__(self):
        return None
# A+B variance=0.2
# A_mu=0.9,1,1.2,1.3,1.4,1.5,1.6,1.9
# B_mu=1,1.1,1.2,1.9
print(configuration(10,3,'a',100).run_config())


'''
while input !='x':
    for key in config_dict:
        print key,config_dict[key][0]
    input = raw_input("choose config: (1,2..,13. x to exit)")

    print config_dict[int(input)][0]+"->  "+str(calc(config_dict[int(input)][1]))
'''