"""
SmartMatch Particle Swarm Optimization (PSO) Engine (Python Version)
"""

import random
from fuzzy import evaluate_laptop_suitability

class Particle:
    def __init__(self, bounds):
        self.bounds = bounds  # List of {'min', 'max'} dicts for each dimension
        self.num_dimensions = len(bounds)
        
        self.position = [0.0] * self.num_dimensions
        self.velocity = [0.0] * self.num_dimensions
        self.best_position = [0.0] * self.num_dimensions
        self.best_fitness = -float('inf')
        self.fitness = 0.0

        self.reset()

    def reset(self):
        for i in range(self.num_dimensions):
            min_val = self.bounds[i]['min']
            max_val = self.bounds[i]['max']
            
            # Random position within bounds
            self.position[i] = min_val + random.random() * (max_val - min_val)
            
            # Random small velocity
            range_val = max_val - min_val
            self.velocity[i] = (random.random() - 0.5) * range_val * 0.1
            
            # Initial personal best position is the start position
            self.best_position[i] = self.position[i]
        
        self.best_fitness = -float('inf')
        self.fitness = 0.0

    def update_position(self):
        for i in range(self.num_dimensions):
            self.position[i] += self.velocity[i]
            
            # Boundary enforcement: clamp position and damp velocity
            if self.position[i] < self.bounds[i]['min']:
                self.position[i] = self.bounds[i]['min']
                self.velocity[i] = -self.velocity[i] * 0.5  # bounce back slightly
            elif self.position[i] > self.bounds[i]['max']:
                self.position[i] = self.bounds[i]['max']
                self.velocity[i] = -self.velocity[i] * 0.5
                

class PSOManager:
    def __init__(self, prefs, swarm_size=40):
        self.prefs = prefs
        self.swarm_size = swarm_size
        self.iteration = 0
        self.max_iterations = 80
        
        # Dimension layout:
        # 0: Price (Euro) - range from 150 to 4000
        # 1: RAM (GB) - range from 2 to 32
        # 2: Weight (kg) - range from 0.6 to 4.5
        # 3: Performance Score - range from 10 to 100
        self.bounds = [
            {'min': 150.0, 'max': 4000.0},  # Price (Euro)
            {'min': 2.0, 'max': 32.0},      # RAM (GB)
            {'min': 0.6, 'max': 4.5},       # Weight (kg)
            {'min': 10.0, 'max': 100.0}     # Performance Score
        ]

        # PSO Hyperparameters
        self.w = 0.729    # Inertia weight
        self.c1 = 1.494   # Cognitive coefficient
        self.c2 = 1.494   # Social coefficient

        self.particles = []
        self.global_best_position = [0.0] * len(self.bounds)
        self.global_best_fitness = -float('inf')

        self.is_converged = False
        self.initialize_swarm()

    def initialize_swarm(self):
        self.particles = [Particle(self.bounds) for _ in range(self.swarm_size)]
        self.global_best_fitness = -float('inf')
        self.iteration = 0
        self.is_converged = False
        
        # Initial evaluation
        self.evaluate_swarm()

    def evaluate_spec_fitness(self, position):
        """Helper to evaluate a particle position using Fuzzy Logic suitability"""
        price = position[0]
        ram = position[1]
        weight = position[2]
        perf = position[3]

        # Construct a virtual laptop reflecting this particle's position
        # so we can score it with our fuzzy logic module.
        virtual_laptop = {
            'price': price,
            'ram': ram,
            'weight': weight,
            'perfScore': perf,
            'batteryScore': self.estimate_battery_score_for_pso(weight),
            'memory': '256GB SSD' if self.prefs['storagePref'] == 'ssd' else '1TB HDD',
            'gpuCompany': 'Nvidia' if 'gaming' in self.prefs['needs'] else 'Intel',
            'gpuType': 'GeForce GTX 1050' if 'gaming' in self.prefs['needs'] else 'HD Graphics',
            'cpuCompany': 'Intel',
            'cpuType': 'Core i5',
            'screenResolution': 'Full HD 1920x1080',
            'typeName': 'Ultrabook' if 'kuliah' in self.prefs['needs'] else 'Notebook',
            '_preprocessed': True  # Prevents crash-recalculating on virtual data
        }

        evaluation = evaluate_laptop_suitability(virtual_laptop, self.prefs)
        return evaluation['score']  # returns 0 to 100

    def estimate_battery_score_for_pso(self, weight):
        score = 65.0  # base Notebook
        if 'kuliah' in self.prefs['needs']:
            score = 85.0  # Study needs prefer Ultrabook style
        
        if weight <= 1.2:
            score += 10.0
        elif weight >= 2.8:
            score -= 15.0
        elif weight >= 2.0:
            score -= 5.0
        
        return min(100.0, max(10.0, score))

    def evaluate_swarm(self):
        for p in self.particles:
            p.fitness = self.evaluate_spec_fitness(p.position)

            # Update personal best
            if p.fitness > p.best_fitness:
                p.best_fitness = p.fitness
                p.best_position = list(p.position)

            # Update global best
            if p.fitness > self.global_best_fitness:
                self.global_best_fitness = p.fitness
                self.global_best_position = list(p.position)

    def step(self):
        if self.iteration >= self.max_iterations:
            self.is_converged = True
            return False

        # Update velocity and position for each particle
        for p in self.particles:
            for i in range(p.num_dimensions):
                r1 = random.random()
                r2 = random.random()

                # PSO Velocity formula
                cognitive = self.c1 * r1 * (p.best_position[i] - p.position[i])
                social = self.c2 * r2 * (self.global_best_position[i] - p.position[i])
                
                p.velocity[i] = self.w * p.velocity[i] + cognitive + social
            
            p.update_position()

        # Evaluate fitness at new positions
        self.evaluate_swarm()
        
        self.iteration += 1
        return True
