from config import *

class Infra:
    def __init__(self, infra_id, infra_state, infra_length, infra_type, nb_houses):
        self.infra_id = infra_id
        self.infra_state = infra_state
        self.infra_length = infra_length
        self.infra_type = infra_type
        self.nb_houses = nb_houses

        # Initialisation
        self.infra_cost = 0
        self.infra_duration = 0

        if infra_type == "aerien":
            self.infra_cost = infra_length * AERIAL_COST_PER_METER
            self.infra_duration = infra_length * AERIAL_DURATION_PER_METER / MAX_WORKERS_PER_INFRA

        elif infra_type == "semi-aerien":
            self.infra_cost = infra_length * SEMI_AERIAL_COST_PER_METER
            self.infra_duration = infra_length * SEMI_AERIAL_DURATION_PER_METER / MAX_WORKERS_PER_INFRA

        elif infra_type == "fourreau":
            self.infra_cost = infra_length * DUCT_COST_PER_METER
            self.infra_duration = infra_length * DUCT_DURATION_PER_METER / MAX_WORKERS_PER_INFRA
