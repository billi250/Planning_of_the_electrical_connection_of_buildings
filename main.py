import pandas as pd
from config import *

# =========================
# 1. PRÉPARATION DES DONNÉES
# =========================
def prepare_data(network_df, building_df, infra_df):
    network_to_repair_df = network_df[network_df["infra_type"] == "a_remplacer"]

    network_to_repair_df = pd.merge(
        network_to_repair_df, infra_df,
        left_on="infra_id", right_on="id_infra"
    )

    network_to_repair_df.drop(
        columns=["nb_maisons", "id_infra", "infra_type"],
        inplace=True
    )

    network_to_repair_df = pd.merge(
        network_to_repair_df, building_df,
        on="id_batiment"
    )

    return network_to_repair_df


# =========================
# 2. CALCUL DES COÛTS GLOBAUX
# =========================
def compute_rebuilding_costs(network_to_repair_df):
    infra_to_repair_df = network_to_repair_df[
        ["infra_id", "longueur", "type_infra"]
    ].drop_duplicates("infra_id")

    total_cost = 0

    for _, row in infra_to_repair_df.iterrows():
        if row["type_infra"] == "aerien":
            total_cost += row["longueur"] * AERIAL_COST_PER_METER
        elif row["type_infra"] == "semi-aerien":
            total_cost += row["longueur"] * SEMI_AERIAL_COST_PER_METER
        elif row["type_infra"] == "fourreau":
            total_cost += row["longueur"] * DUCT_COST_PER_METER

    return total_cost


# =========================
# 3. CALCUL DURÉE HÔPITAL
# =========================
def compute_hospital_duration(network_to_repair_df):
    hospital_df = network_to_repair_df[
        network_to_repair_df["type_batiment"] == "hôpital"
    ]

    infra_durations = []

    for _, row in hospital_df.iterrows():
        if row["type_infra"] == "aerien":
            infra_durations.append(
                row["longueur"] * AERIAL_DURATION_PER_METER / MAX_WORKERS_PER_INFRA
            )
        elif row["type_infra"] == "semi-aerien":
            infra_durations.append(
                row["longueur"] * SEMI_AERIAL_DURATION_PER_METER / MAX_WORKERS_PER_INFRA
            )
        elif row["type_infra"] == "fourreau":
            infra_durations.append(
                row["longueur"] * DUCT_DURATION_PER_METER / MAX_WORKERS_PER_INFRA
            )

    return max(infra_durations) if infra_durations else 0


# =========================
# 4. TRI DES BÂTIMENTS (LOGIQUE CORRIGÉE)
# =========================
def sort_buildings_with_phases(network_to_repair_df):
    hospital_df = network_to_repair_df[
        network_to_repair_df["type_batiment"] == "hôpital"
    ]

    other_df = network_to_repair_df[
        network_to_repair_df["type_batiment"] != "hôpital"
    ]

    building_rows = []

    for b_id, group in other_df.groupby("id_batiment"):
        nb_maisons = group["nb_maisons"].iloc[0]

        total_cost = 0
        for _, row in group.iterrows():
            if row["type_infra"] == "aerien":
                total_cost += row["longueur"] * AERIAL_COST_PER_METER
            elif row["type_infra"] == "semi-aerien":
                total_cost += row["longueur"] * SEMI_AERIAL_COST_PER_METER
            elif row["type_infra"] == "fourreau":
                total_cost += row["longueur"] * DUCT_COST_PER_METER

        score = nb_maisons / total_cost if total_cost > 0 else 0

        building_rows.append({
            "id_batiment": b_id,
            "score": score
        })

    building_scores = (
        pd.DataFrame(building_rows)
        .sort_values(by="score", ascending=False)
    )

    sorted_buildings = (
        list(hospital_df["id_batiment"].unique()) +
        list(building_scores["id_batiment"])
    )

    return sorted_buildings


# =========================
# 5. EXPORT CSV
# =========================
def export_csv(network_to_repair_df, sorted_buildings):
    network_to_repair_df.to_csv(
        r"C:\Users\lenovo\OneDrive\Bureau\projets_infrastructure\Planning_of_the_electrical_connection_of_buildings\reseau_priorise.csv",
        index=False
    )

    building_rows = []

    for rank, b_id in enumerate(sorted_buildings, start=1):
        b_data = network_to_repair_df[
            network_to_repair_df["id_batiment"] == b_id
        ]

        nb_houses = b_data["nb_maisons"].iloc[0]

        total_cost = 0
        total_duration = 0

        for _, row in b_data.iterrows():
            if row["type_infra"] == "aerien":
                total_cost += row["longueur"] * AERIAL_COST_PER_METER
                total_duration += row["longueur"] * AERIAL_DURATION_PER_METER / MAX_WORKERS_PER_INFRA
            elif row["type_infra"] == "semi-aerien":
                total_cost += row["longueur"] * SEMI_AERIAL_COST_PER_METER
                total_duration += row["longueur"] * SEMI_AERIAL_DURATION_PER_METER / MAX_WORKERS_PER_INFRA
            elif row["type_infra"] == "fourreau":
                total_cost += row["longueur"] * DUCT_COST_PER_METER
                total_duration += row["longueur"] * DUCT_DURATION_PER_METER / MAX_WORKERS_PER_INFRA

        building_rows.append({
            "id_batiment": b_id,
            "nb_maisons": nb_houses,
            "cout_total": total_cost,
            "duree_totale": total_duration,
            "rang_priorite": rank
        })

    pd.DataFrame(building_rows).to_csv(
        r"C:\Users\lenovo\OneDrive\Bureau\projets_infrastructure\Planning_of_the_electrical_connection_of_buildings\batiments_priorises.csv",
        index=False
    )


# =========================
# 6. MAIN
# =========================
if __name__ == "__main__":
    network_df = pd.read_excel(
        r"C:\Users\lenovo\OneDrive\Bureau\projets_infrastructure\Planning_of_the_electrical_connection_of_buildings\data\reseau_en_arbre.xlsx"
    )
    building_df = pd.read_csv(
        r"C:\Users\lenovo\OneDrive\Bureau\projets_infrastructure\Planning_of_the_electrical_connection_of_buildings\new_data\batiments.csv"
    )
    infra_df = pd.read_csv(
        r"C:\Users\lenovo\OneDrive\Bureau\projets_infrastructure\Planning_of_the_electrical_connection_of_buildings\new_data\infra.csv"
    )

    network_to_repair_df = prepare_data(network_df, building_df, infra_df)

    print("Le réseau que l'on doit réparer :")
    print(network_to_repair_df)

    total_cost = compute_rebuilding_costs(network_to_repair_df)
    print(f"\nLe coût total des réparations est de : {total_cost:.2f} euros")

    hospital_duration = compute_hospital_duration(network_to_repair_df)
    print(f"Le temps estimé pour l'hôpital : {hospital_duration:.2f} h")

    sorted_buildings = sort_buildings_with_phases(network_to_repair_df)

    print("\n🏆 TOP 10 bâtiments prioritaires :")
    for rank, b_id in enumerate(sorted_buildings[:10], start=1):
        b_data = network_to_repair_df[
            network_to_repair_df["id_batiment"] == b_id
        ]

        nb_houses = b_data["nb_maisons"].iloc[0]

        total_cost_building = 0
        total_duration_building = 0

        for _, row in b_data.iterrows():
            if row["type_infra"] == "aerien":
                total_cost_building += row["longueur"] * AERIAL_COST_PER_METER
                total_duration_building += row["longueur"] * AERIAL_DURATION_PER_METER / MAX_WORKERS_PER_INFRA
            elif row["type_infra"] == "semi-aerien":
                total_cost_building += row["longueur"] * SEMI_AERIAL_COST_PER_METER
                total_duration_building += row["longueur"] * SEMI_AERIAL_DURATION_PER_METER / MAX_WORKERS_PER_INFRA
            elif row["type_infra"] == "fourreau":
                total_cost_building += row["longueur"] * DUCT_COST_PER_METER
                total_duration_building += row["longueur"] * DUCT_DURATION_PER_METER / MAX_WORKERS_PER_INFRA

        print(
            f"{rank} | {b_id} | Maisons: {nb_houses} | "
            f"Coût: {total_cost_building:.2f} € | "
            f"Durée: {total_duration_building:.2f} h"
        )

    export_csv(network_to_repair_df, sorted_buildings)

    print("\n✅ Fichiers CSV générés correctement (sans surcomptage)")
