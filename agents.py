import numpy as np

class ToilletPaperAg():

    def __init__(self,env) -> None:
        self.env = env
        self.price_average = 0
        self.current_percepts = env.initial_percepts()
        self.usage_average = self.current_percepts['tpnumber']
        self.usage = self.current_percepts['tpnumber']
        self.age = 0
        self.usage_std = 0
        self.to_buy = 0
        self.spendings = 0 

    def act(self):
         
        tpnumber_t_1 = self.current_percepts['tpnumber'] 
        
        self.usage_std = 100

        self.to_buy = max(self.usage_average + self.usage_std*4 - self.current_percepts['tpnumber'],0) 
        self.spendings = self.to_buy * self.current_percepts['price']

        action = {'to_buy':self.to_buy}
        
        self.current_percepts = self.env.change_state(action)
        self.age += 1
        
        tpnumber_t = self.current_percepts['tpnumber']
        
        self.usage = tpnumber_t_1 + self.to_buy - tpnumber_t 
        self.usage_average = (self.usage_average * (self.age - 1) + self.usage)/self.age

class MazeAgentDFS():

    def __init__(self,env):
        self.env = env
        self.percepts = env.initial_percepts()
        self.F = [[self.percepts['position']]]

    def act(self):

        while self.F:
            path = self.F.pop(0)

            self.percepts = self.env.change_state({'path':path.copy()})

            if self.percepts['goal']:
                break
            else:
                for n in self.percepts['available_neighbors']:
                    if n not in path:
                        self.F.insert(0,path + [n])

        self.env.draw_best(path)

class MazeAgentBFS():

    def __init__(self,env):
        self.env = env
        self.percepts = env.initial_percepts()
        self.F = [[self.percepts['position']]]

    def act(self):

        while self.F:
            path = self.F.pop(-1)

            self.percepts = self.env.change_state({'path':path.copy()})

            if self.percepts['goal']:
                break
            else:
                for n in self.percepts['available_neighbors']:
                    if n not in path:
                        self.F.insert(0,path + [n])

        self.env.draw_best(path)

class MazeAgentBranchAndBound():

    def __init__(self,env,bound):
        self.env = env
        self.percepts = env.initial_percepts()
        self.F = [[self.percepts['position']]]
        self.bound = bound
        self.best_path = []

    def cost(self, path):
        return len(path)-1

    def heuristic(self, path):
        nk = path[-1]
        goal = self.env.maze._goal
        return np.abs(nk[0] - goal[0]) + np.abs(nk[1] - goal[1])

    def act(self):

        while self.F:
            path = self.F.pop(-1)
            c = self.cost(path)
            h = self.heuristic(path)

            if c + h <= self.bound:

                self.percepts = self.env.change_state({'path':path.copy()})

                if self.percepts['goal']:
                    self.best_path = path
                    self.bound = c 
                else:
                    for n in self.percepts['available_neighbors']:
                        if n not in path:
                            self.F.insert(-1,path + [n])

        self.env.draw_best(self.best_path)
        print(self.bound)

class MazeAgentAStar():

    def __init__(self,env):
        self.env = env
        self.percepts = env.initial_percepts()
        self.F = [[self.percepts['position']]]
        # fs armazena os valores de custo + heurística para cada caminho na fronteira
        self.fs = [self.cost(self.F[0])+self.heuristic(self.F[0])]
        self.best_path = []

    def cost(self, path):
        return len(path)-1

    def heuristic(self, path):
        nk = path[-1]
        goal = self.env.maze._goal
        return np.abs(nk[0] - goal[0]) + np.abs(nk[1] - goal[1])

    def act(self):

        while self.F:
            # Find the path with minimum f
            minFidx = np.argmin(self.fs)
            # Remove path with minimum f
            path = self.F.pop(minFidx)
            self.fs.pop(minFidx)

            self.percepts = self.env.change_state({'path':path.copy()})     #DUVIDA

            if self.percepts['goal']:
                self.best_path = path
                break
            else:
                for n in self.percepts['available_neighbors']:
                    if n not in path:
                        self.F.insert(-1,path + [n])
                        self.fs.insert(-1,self.cost(path + [n])+self.heuristic(path + [n]))

        self.env.draw_best(self.best_path)

class MazeAgentGuloso():
    def __init__(self,env):
        self.env = env
        self.percepts = env.initial_percepts()
        self.F = [[self.percepts['position']]]
        # fs stores the values of heuristic for each path in the frontier
        self.fs = [self.heuristic(self.F[0])]
        self.best_path = []
    
    def cost(self, path):
        return len(path)-1

    def heuristic(self, path):
        nk = path[-1]
        goal = self.env.maze._goal
        return np.abs(nk[0] - goal[0]) + np.abs(nk[1] - goal[1])

    def act(self):

        while self.F:
            # Find the path with minimum f
            minFidx = np.argmin(self.fs)
            # Remove path with minimum f
            path = self.F.pop(minFidx)
            self.fs.pop(minFidx)

            self.percepts = self.env.change_state({'path':path.copy()})   

            if self.percepts['goal']:
                self.best_path = path
                break
            else:
                for n in self.percepts['available_neighbors']:
                    if n not in path:
                        self.F.insert(-1,path + [n])
                        self.fs.insert(-1, self.heuristic(path + [n]))

        self.env.draw_best(self.best_path)

class MazeAgentMenorCusto():

    def __init__(self,env):
        self.env = env
        self.percepts = env.initial_percepts()
        self.F = [[self.percepts['position']]]
        # fs stores the values of cost for each path in the frontier
        self.fs = [self.cost(self.F[0])]
        self.best_path = []

    def cost(self, path):
        return len(path)-1

    def heuristic(self, path):
        nk = path[-1]
        goal = self.env.maze._goal
        return np.abs(nk[0] - goal[0]) + np.abs(nk[1] - goal[1])

    def act(self):

        while self.F:
            # Find the path with minimum f
            minFidx = np.argmin(self.fs)
            # Remove path with minimum f
            path = self.F.pop(minFidx)
            self.fs.pop(minFidx)

            self.percepts = self.env.change_state({'path':path.copy()})

            if self.percepts['goal']:
                self.best_path = path
                break
            else:
                for n in self.percepts['available_neighbors']:
                    if n not in path:
                        self.F.insert(-1,path + [n])
                        self.fs.insert(-1,self.cost(path + [n]))

        self.env.draw_best(self.best_path)


class NQueenSearchAgent():

    def __init__(self,env,nq) -> None:
        self.env = env
        self.F = [[]]
        self.to_dos = [np.arange(1,nq+1)]
        self.nq = nq
        self.valid_sol = []

    def search(self):

        while self.F:

            sol = self.F.pop(-1)
            to_do = self.to_dos.pop(-1)

            if len(sol) == self.nq:
                self.valid_sol = sol
                print(sol)
            else:
                for n in to_do:
                    if self.env.check_constraints(sol + [n]) == 0:
                        self.F.insert(-1,sol + [n])
                        self.to_dos.insert(-1,to_do[to_do!=n])

        self.env.display_solution(self.valid_sol)
        
        return self.valid_sol
        

