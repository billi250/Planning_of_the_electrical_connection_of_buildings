class Building:
    def __init__(self, id_building, nb_houses, list_infras):
        self.id_building = id_building
        self.nb_houses = nb_houses
        self.list_infras = list_infras

    # Métrique = somme du coût des infrastructures
    def get_building_metric(self):
        return sum(infra.infra_cost for infra in self.list_infras)

    # Coût total pour export CSV
    def get_total_cost(self):
        return sum(infra.infra_cost for infra in self.list_infras)

    # Durée totale pour export CSV
    def get_total_duration(self):
        return sum(infra.infra_duration for infra in self.list_infras)

    def repair_all_infras(self):
        for infra in self.list_infras:
            infra.repair()

    def __lt__(self, other_building):
        # Tri par coût croissant = priorité plus haute
        return self.get_building_metric() < other_building.get_building_metric()
