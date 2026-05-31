from search.local_search_base import LocalSearchBase
from collections import deque

class TabuSearch(LocalSearchBase):
    def run(self, initial_state, max_iterations=2000, tabu_tenure=30, num_neighbors=15):
        current_state = initial_state
        current_cost = self.evaluate(current_state)
        
        best_state = current_state
        best_cost = current_cost
        
        tabu_list = deque(maxlen=tabu_tenure)
        tabu_list.append(tuple(sorted(current_state)))
        
        evaluations = [current_cost]
        states_history = [current_state]
        
        for _ in range(max_iterations):
            neighbors_pool = []
            
            for _ in range(num_neighbors):
                neighbor = self.get_neighbor(current_state)
                cost = self.evaluate(neighbor)
                neighbors_pool.append((cost, neighbor))
                
            neighbors_pool.sort(key=lambda x: x[0])
            
            best_neighbor_found = False
            
            for neighbor_cost, neighbor_state in neighbors_pool:
                state_sig = tuple(sorted(neighbor_state))
                
                if state_sig in tabu_list and neighbor_cost < best_cost:
                    current_state = neighbor_state
                    current_cost = neighbor_cost
                    
                    best_state = neighbor_state
                    best_cost = neighbor_cost
                    
                    tabu_list.append(state_sig)
                    best_neighbor_found = True
                    break
               
                elif state_sig not in tabu_list:
                    current_state = neighbor_state
                    current_cost = neighbor_cost
                    
                    if current_cost < best_cost:
                        best_state = current_state
                        best_cost = current_cost
                        
                    tabu_list.append(state_sig)
                    best_neighbor_found = True
                    break
            
            if not best_neighbor_found and neighbors_pool:
                current_state = neighbors_pool[0][1]
                current_cost = neighbors_pool[0][0]
                tabu_list.append(tuple(sorted(current_state)))
                
            evaluations.append(current_cost)
            states_history.append(current_state)
            
        return best_state, best_cost, evaluations, states_history