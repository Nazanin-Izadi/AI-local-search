from search.local_search_base import LocalSearchBase

class HillClimbing(LocalSearchBase):
    def run(self, initial_state, max_iterations=2000):
        current_state = initial_state
        current_cost = self.evaluate(current_state)
        
        best_state = current_state
        best_cost = current_cost
        
        evaluations = [current_cost]
        states_history = [current_state]
        
        for _ in range(max_iterations):
            neighbor = self.get_neighbor(current_state)
            neighbor_cost = self.evaluate(neighbor)
            
            if neighbor_cost <= current_cost:
                current_state = neighbor
                current_cost = neighbor_cost
                
                if current_cost < best_cost:
                    best_state = current_state
                    best_cost = current_cost
            
            evaluations.append(current_cost)
            states_history.append(current_state)
            
        return best_state, best_cost, evaluations, states_history