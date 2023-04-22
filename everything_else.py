from mesa import Model, Agent
from mesa.time import RandomActivation
from mesa.space import NetworkGrid
import networkx as nx
import numpy as np
import random

class SocialNorms(Model):
    def _init_(self, num_agents):
        self.num_agents = num_agents
        self.graph_cluster_size = 0.01
        self.graph_interconnectivity = 0.01

        self.schedule = RandomActivation(self)
        self.grid = NetworkGrid(nx.Graph())
        self.G = self.create_social_network()
        self.create_agents()
        self.running = True

    def create_social_network(self):
        network = nx.Graph()
        #network = nx.newman_watts_strogatz_graph(n = self.num_agents, k = int(self.num_agents*self.graph_cluster_size), p = int(self.num_agents*self.graph_interconnectivity))
        network.add_nodes_from(range(self.num_agents))
        for i in range(self.num_agents):
            for j in range(i+1, self.num_agents):
                if random.random() < 0.3:
                    network.add_edge(i, j)
        return network

    def create_agents(self):
        for i in range(self.num_agents):
            age = random.randint(18, 65)
            alcohol = random.choice([True, False])
            if age < 25:
                average_drinks = np.random.lognormal(16, 1)
                drinking_behavior = min(np.random.normal(0, 1) + np.random.normal(0, 0.15), 1)
            else:
                average_drinks = np.random.lognormal(6, 1)
                drinking_behavior = np.random.normal(0, 1)

            agent = Person(i, age, alcohol, average_drinks, drinking_behavior)
            self.schedule.add(agent)
            self.grid.place_agent(agent, i)
    
    def step(self):
        self.schedule.step()

class Person(Agent):
    def _init_(self, unique_id, age, alcohol, average_drinks, drinking_behavior):
        self.unique_id = unique_id
        self.age = age
        self.alcohol = alcohol

        self.average_drinks = average_drinks
        self.drinking_behavior = drinking_behavior
        
    def get_peers(self):
        """Return a list of the agent's peers."""
        peers = self.model.grid.get_neighbors(self.pos, include_center=False)
        return peers
        
    def get_alcohol(self):
        """Return the agent's alcohol consumption."""
        if self.alcohol:
            return self.average_drinks
        else:
            return
        
    def update_average_drinking(self):
        """Update the agent's average number of drinks per week based on their social network."""
        peer_alcohol = [n.get_alcohol() for n in self.get_peers()]
        num_peers = len(peer_alcohol)
        old_average_drinks = self.average_drinks

        if self.alcohol:
            # Agent drinks alcohol
            if num_peers == 0:
                # No peers to compare to
                return 0
            else:
                # Compare to peers and adjust based on susceptibility to social influence
                peer_avg = sum(peer_alcohol) / num_peers
                # self.average_drinks = self.drinking_behavior * (self.average_drinks / peer_avg) + (1 - self.drinking_behavior)
                self.average_drinks = self.drinking_behavior * (self.average_drinks / peer_avg) + np.normal(0, 0.5)

                # return 1
        else:
            # Agent does not drink alcohol
            if num_peers == 0:
                # No peers to compare to
                return 0
            else:
                # Compare to peers and adjust based on susceptibility to social influence
                peer_avg = sum(peer_alcohol) / num_peers
                # self.average_drinks = self.drinking_behavior * (1 - self.average_drinks / peer_avg) + (1 - self.drinking_behavior)
                self.average_drinks = self.drinking_behavior * (1 - self.average_drinks / peer_avg) + np.normal(0, 0.5)
                
                # return 0
    
        self.update_drinking_behavior(old_average_drinks)
        return 1

    def update_drinking_behavior(self, old_average_drinks):
        """Update the agent's drinking behavior based on their average number of drinks per week."""
        if self.average_drinks > old_average_drinks:
            self.drinking_behavior = min(self.drinking_behavior + np.normal(0, 0.05), 1)
        else:
            self.drinking_behavior = max(self.drinking_behavior - np.normal(0, 0.05), 0)

    def step(self):
        self.update_average_drinking()     
        print(self.average_drinks)
       

