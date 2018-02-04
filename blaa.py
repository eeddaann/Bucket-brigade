from bb import simulation
import bin_packing

class configuration:
    def __init__(self,picksize,pickers,performance,capacity):
        self.picksize = picksize
        self.pickers = pickers
        self.performance = performance
        self.capacity = capacity

    def __repr__(self):
        return None





while input !='x':
    for key in config_dict:
        print key,config_dict[key][0]
    input = raw_input("choose config: (1,2..,13. x to exit)")

    print config_dict[int(input)][0]+"->  "+str(calc(config_dict[int(input)][1]))
