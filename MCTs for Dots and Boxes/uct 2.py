import time
import random
import math
import greedo

def think(state):
 
  moves = state.get_moves()
  rootnode = Node(state, None, None)
  t_start = time.time()
  # t_deadline = t_start + 1
  # iterations = 0
  iterations = 0
  
  for i in range (1000):
    iterations += 1
    node = rootnode
    test_state = state.copy()

    # Select
    while node.untried_moves == [] and node.children != []:# node is fully expanded and non-terminal
      node = node.UCTSelectChild()
      test_state.apply_move(node.move)
      #test_state.apply_move(greedo.think(test_state))

    # Expand
    if node.untried_moves != []: # if we can expand (i.e. state/node is non-terminal)
      m = random.choice(node.untried_moves) 
      currentPlayer = test_state.get_whose_turn()
      test_state.apply_move(m)
      node = node.addChild(test_state, m, currentPlayer) # add child and descend tree
    
    
    while test_state.get_moves() != []: 
      test_state.apply_move(greedo.think(test_state))

    # Backpropagate
    while node != None: 
      
      node.update(test_state.get_score(currentPlayer))
      node = node.parent
  
  return sorted(rootnode.children, key = lambda c: c.visits)[-1].move # return the move that was most visited

class Node:
  def __init__(self, state, parent = None, move = None, who = None):
    self.parent = parent
    self.who = who
    self.children = []
    self.untried_moves = state.get_moves()
    self.visits = 0
    self.score = 0.0
    self.move = move
    
  def UCTSelectChild(self):
    s = sorted(self.children, key = lambda c: c.score/c.visits + math.sqrt(2*math.log(self.visits)/c.visits))[-1]
    return s
  
  def addChild(self, state, move, who):
    n = Node(state, self, move, who)
    self.untried_moves.remove(move)
    self.children.append(n)
    return n
  
  def update(self, score):
    self.visits += 1
    self.score += score