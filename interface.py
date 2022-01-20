from simulation import simulation
from heuristic import pack

config_lst = []
user_input = None
class configuration:
    def __init__(self, picksize, pickers, performance, capacity):
        self.picksize = picksize
        self.pickers = pickers
        self.performance = performance + str(pickers)
        self.capacity = capacity
        self.performance_d = {'a2': [[1, 0.2, 0.5, 0.1, 1.4, 0.2], [1, 0.2, 0.5, 0.1, 1.0, 0.2]],
                              'b2': [[1, 0.2, 0.5, 0.1, 1.1, 0.2], [1, 0.2, 0.5, 0.1, 1.0, 0.2]],
                              'a3': [[1, 0.2, 0.5, 0.1, 1.5, 0.2], [1, 0.2, 0.5, 0.1, 1.2, 0.2],
                                     [1, 0.2, 0.5, 0.1, 0.9, 0.2]],
                              'b3': [[1, 0.2, 0.5, 0.1, 1.2, 0.2], [1, 0.2, 0.5, 0.1, 1.2, 0.2],
                                     [1, 0.2, 0.5, 0.1, 1.1, 0.2]],
                              'a4': [[1, 0.2, 0.5, 0.1, 1.9, 0.2], [1, 0.2, 0.5, 0.1, 1.6, 0.2],
                                     [1, 0.2, 0.5, 0.1, 1.3, 0.2], [1, 0.2, 0.5, 0.1, 0.9, 0.2]],
                              'b4': [[1, 0.2, 0.5, 0.1, 1.2, 0.2], [1, 0.2, 0.5, 0.1, 1.1, 0.2],
                                     [1, 0.2, 0.5, 0.1, 1.0, 0.2], [1, 0.2, 0.5, 0.1, 1.0, 0.2]]}

    def run_config(self):
        data = pack(self.capacity, self.picksize)
        return simulation(self.picksize, self.pickers, self.performance_d[self.performance], data).run_config()

    def __repr__(self):
        return "{} pick-faces, {} pickers, {} items capacity, data {}".format(str(self.picksize), str(self.pickers),
                                                                                str(self.capacity), self.performance[:-1])

config_lst.append("all")
config_lst.append(configuration(6, 2, 'a', 60))
config_lst.append(configuration(6, 2, 'a', 90))
config_lst.append(configuration(6, 2, 'b', 60))
config_lst.append(configuration(6, 2, 'b', 90))

config_lst.append(configuration(10, 2, 'a', 100))
config_lst.append(configuration(10, 3, 'a', 100))
config_lst.append(configuration(10, 2, 'a', 150))
config_lst.append(configuration(10, 3, 'a', 150))
config_lst.append(configuration(10, 2, 'b', 100))
config_lst.append(configuration(10, 3, 'b', 100))
config_lst.append(configuration(10, 2, 'b', 150))
config_lst.append(configuration(10, 3, 'b', 150))

config_lst.append(configuration(25, 4, 'a', 150))
config_lst.append(configuration(25, 3, 'a', 150))
config_lst.append(configuration(25, 4, 'a', 200))
config_lst.append(configuration(25, 3, 'a', 200))
config_lst.append(configuration(25, 4, 'b', 150))
config_lst.append(configuration(25, 3, 'b', 150))
config_lst.append(configuration(25, 4, 'b', 200))
config_lst.append(configuration(25, 3, 'b', 200))



while user_input !='x':
    for config in range(len(config_lst)):
        print(("{} - {}".format(str(config),str(config_lst[config]))))
    user_input = input("choose config: (0,2..,20). x to exit")
    if user_input == '0':
        for config in config_lst[1:]:
            print("$@==################################################################################==@$")
            print(("$@==#### {} -> {} seconds.####==@$".format(str(config),str(round(config.run_config(),4)))))
            print("$@==################################################################################==@$")
    else:
        print("$@==################################################################################==@$")
        print((
        "$@==#### {} -> {} seconds.####==@$".format(str(config_lst[int(user_input)]), str(round(config_lst[int(user_input)].run_config(),4)))))
        print("$@==################################################################################==@$")