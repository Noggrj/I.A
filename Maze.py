from pyamaze import maze,COLOR,agent
from environments import Maze
from agents import MazeAgentDFS, MazeAgentBFS, MazeAgentBranchAndBound, MazeAgentAStar, MazeAgentGuloso , MazeAgentMenorCusto


env = Maze(6,6)
#ag = MazeAgentDFS(env)
#ag = MazeAgentBFS(env)
#ag = MazeAgentMenorCusto(env)
#ag = MazeAgentGuloso(env)
#ag = MazeAgentAStar(env)
ag = MazeAgentBranchAndBound(env,10)

ag.act()
