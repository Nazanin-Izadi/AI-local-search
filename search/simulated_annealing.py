from search.local_search_base import LocalSearchBase
import math
import random

class SimulatedAnnealing(LocalSearchBase):
    def run(self, initial_state, initial_temp=1000.0, cooling_rate=0.995, max_iterations=2000):
        current_state = initial_state
        current_cost = self.evaluate(current_state)
        
        best_state = current_state
        best_cost = current_cost
        
        evaluations = [current_cost]
        states_history = [current_state]
        
        T = initial_temp
        
        for _ in range(max_iterations):
            neighbor = self.get_neighbor(current_state)
            neighbor_cost = self.evaluate(neighbor)
            
            delta_c = neighbor_cost - current_cost
            
            if delta_c < 0 or random.random() < math.exp(-delta_c / T):
                current_state = neighbor
                current_cost = neighbor_cost
                
                if current_cost < best_cost:
                    best_state = current_state
                    best_cost = current_cost
            
            evaluations.append(current_cost)
            states_history.append(current_state)
            
            T = max(T * cooling_rate, 0.01)
            
        return best_state, best_cost, evaluations, states_history