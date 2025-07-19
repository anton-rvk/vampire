
from graph import Graph
import os
import assets.clan_colors as clan_colors

clans = ["assamite", "brujah", "caitiff", "gangrel", 
         "hecata", "lasombra", "malkavian", "ministry",
         "nosferatu", "ravnos", "salubri", "toreador",
         "tremere", "tzimisce", "ventrue", "antediluvians"]

target_directory = "./data/"

for filename in os.listdir(target_directory):

    if filename[:-4] in clans: 
        print(filename[:-4])

        if filename[:-4] == "caitiff":
            g = Graph(clan_data_path=("data/" + filename[:-4] + ".csv"),
                    graph_path=("graphs/" + filename[:-4] + ".html"))
            
        elif filename[:-4] == "antediluvians":
            antediluvian_gradient = {
                    1: "#030303",  # Dark Red
                    2: "#808080",  # Grey
                    3: "#BB1C00"   # Lighter Red
                }
            g = Graph(clan_data_path=("data/" + filename[:-4] + ".csv"),
                    graph_path=("graphs/" + filename[:-4] + ".html"),
                    node_gradient=antediluvian_gradient)
            
        else: 
            g = Graph(clan_data_path=("data/" + filename[:-4] + ".csv"),
                    graph_path=("graphs/" + filename[:-4] + ".html"),
                    node_gradient=clan_colors.get_clan_gradients(filename[:-4]))

        g.preprocess_data()

        g.add_vamps_to_graph()

        if filename[:-4] == "antediluvians":
            g.generate_network(filter_on=False)
            g.set_custom_js_rules()
            
        else:
            g.generate_network()
            g.set_custom_js_rules()


