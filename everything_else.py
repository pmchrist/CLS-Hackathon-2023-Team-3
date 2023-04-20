import mesa
from mesa import Model, Agent
from mesa.time import RandomActivation
from mesa.space import NetworkGrid
import networkx as nx
import random

# Agent
class Person:
    def __init__(self, unique_id, age, drinking_behavior, social_norms, social_motives):
        print(unique_id)
        self.unique_id = unique_id
        self.age = age
        self.drinking_behavior = drinking_behavior
        self.social_norms = social_norms
        self.social_motives = social_motives
    
    def step(self):
        return

# Model
class SocialNorms(Model):
    def __init__(self, num_agents):
        self.num_agents = num_agents
        self.schedule = RandomActivation(self)
        graph_cluster_size = 0.01
        graph_interconnectivity = 0.01
        self.G = nx.newman_watts_strogatz_graph(n = num_agents, k = int(num_agents*graph_cluster_size), p = int(num_agents*graph_interconnectivity))
        self.grid = NetworkGrid(self.G)
        self.create_agents()

        self.datacollector = mesa.DataCollector(
            #model_reporters={"Gini": compute_gini},
            #agent_reporters={"Wealth": lambda _: _.wealth},
        )

        self.list_of_random_nodes = self.random.sample(list(self.G), self.num_agents)

        self.running = True
        self.datacollector.collect(self)
    

    def step(self):
        return
    
    def run_model(self, n):
        for i in range(n):
            self.step()
    
    def create_agents(self):
        id = -1
        for i in range(self.num_agents):
            id += 1
            age = random.randint(18, 65)            # Change age if we are doing Students
            drinking_behavior = random.random()     # They do nothing for now
            social_norms = random.random()
            social_motives = random.random()
            agent = Person(id, age, drinking_behavior, social_norms, social_motives)
            self.schedule.add(agent)
            self.grid.place_agent(agent, self.list_of_random_nodes[i])

# Some function
def get_opinion(self):
    """Calculate the agent's opinion on alcohol consumption based on their own 
    behavior and the behavior of their peers, taking into account their 
    susceptibility to social influence.
    """
    peer_alcohol = [n.get_alcohol() for n in self.get_peers()]
    num_peers = len(peer_alcohol)
    
    if self.alcohol:
        # Agent drinks alcohol
        if num_peers == 0:
            # No peers to compare to
            return 1
        else:
            # Compare to peers and adjust based on susceptibility to social influence
            peer_avg = sum(peer_alcohol) / num_peers
            return self.alcohol_influence * (self.alcohol / peer_avg) + (1 - self.alcohol_influence)
    else:
        # Agent does not drink alcohol
        if num_peers == 0:
            # No peers to compare to
            return 0
        else:
            # Compare to peers and adjust based on susceptibility to social influence
            peer_avg = sum(peer_alcohol) / num_peers
            return self.alcohol_influence * (1 - self.alcohol / peer_avg) + (1 - self.alcohol_influence)

def run_it(size, steps):
    model = SocialNorms(size)
    model.run_model(steps)