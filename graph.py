import urllib.request
import pandas as pd
import numpy as np
import re
import urllib

from pyvis.network import Network
import networkx as nx

def inject_js(html_path, original_pattern, new_pattern):    
    with open(html_path, 'r', encoding='utf-8') as file: 
        source_code = file.read()
        source_code_updated = source_code.replace(original_pattern, new_pattern)
    
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(source_code_updated)

class Graph: 

    def __init__(self, clan_data_path, graph_path, 
                 minor_chars_data_path = "data/minor_characters.csv",
                 node_gradient = {
                                    1: "#8b0000",    # Darkest Red
                                    2: "#920c0c",
                                    3: "#991919",
                                    4: "#a02626",
                                    5: "#a83333",
                                    6: "#af3f3f",
                                    7: "#b64c4c",
                                    8: "#bd5959",
                                    9: "#c46666",
                                    10: "#cc7272",
                                    11: "#d37f7f",
                                    12: "#da8c8c",
                                    13: "#e29999",
                                    14: "#e9a5a5",
                                    15: "#f0b2b2",
                                    16: "#f7bfbf",
                                    17: "#ffcccc"     # Lightest Red
                                }):

        self._clan_df = pd.read_csv(clan_data_path)
        self._minor_chars_df = pd.read_csv(minor_chars_data_path)

        self._graph_path = graph_path

        self.graph = nx.DiGraph()
        self.network = None

        self._node_gradient = node_gradient

        self._background_color = "#222222"

    def _drop_extra_cols(self, clan_columns_to_drop: list = [0], minor_chars_columns_to_drop: list = [0]):

        for column in clan_columns_to_drop:
            self._clan_df.drop(self._clan_df.columns[column], axis = 'columns', inplace= True)
        
        for column in minor_chars_columns_to_drop:
            self._minor_chars_df.drop(self._minor_chars_df.columns[column], axis = 'columns', inplace=True)

    def _columns_to_lowercase(self, columns_to_lower: list = ['Clan', 'Childer', 'Name', 'Sire']):
        for column in columns_to_lower:
            self._clan_df[column] = self._clan_df[column].apply(lambda x: x.lower() if isinstance(x, str) else x)

    def _concat_minor_chars(self, target_clan = None):

        minor_chars_clan = self._minor_chars_df

        if target_clan:
            minor_chars_clan = minor_chars_clan[minor_chars_clan["Clan"] == target_clan]

        minor_chars_clan = minor_chars_clan[["Name", "Clan", "Generation", "Link"]]

        return pd.concat([self._clan_df, minor_chars_clan])
    
    @staticmethod
    def parse_generation(gen_str, check_diablerie: bool = True, custom_rules: list = [("V5", ""), (r'\[\d+\]', "")]):
        
        gen_str = str(gen_str)

        for rule in custom_rules:
            gen_str = re.sub(rule[0], rule[1], gen_str)

        gen = re.findall(r'\d+', gen_str)

        gen = [int(x) for x in gen if int(x) <= 16 or int(x) > 0]

        if not gen: 
            return np.nan

        
        if "diab" in gen_str and check_diablerie: #check for diablerie 
            gen = min(gen)
        else: 
            gen = max(gen)

        if gen > 15: 
            return np.nan
        
        return int(gen)
    
    def _parse_diablerie(self):
        self._clan_df["Diablerie"] = self._clan_df["Generation"].apply(lambda x: 1 if ("diab" in str(x)) else 0)
    
    def _generation_to_int(self):
        self._clan_df["Generation"] = self._clan_df["Generation"].apply(lambda x: Graph.parse_generation(str(x)))

    def _check_redirects_links(self):

        self._clan_df["Link"] = self._clan_df["Link"].apply(lambda x: urllib.request.urlopen(x).geturl() if isinstance(x, str) else x)
        self._clan_df["Sire_Link"] = self._clan_df["Sire_Link"].apply(lambda x: urllib.request.urlopen(x).geturl() if isinstance(x, str) else x)
    
    def preprocess_data(self):

        self._drop_extra_cols()

        self._concat_minor_chars(target_clan="brujah")

        self._columns_to_lowercase(columns_to_lower=[['Clan', 'Childer', 'Sire']])

        self._parse_diablerie()

        self._generation_to_int()

        self._check_redirects_links()

    
    def generate_edges(self):

        edges = []
        sireless_vamps = []

        for vamp in self._clan_df.iterrows():

            if (vamp[1]["Sire_Link"] in list(self._clan_df["Link"])): #append the edge by the link
                print(self._clan_df[self._clan_df["Link"] == vamp[1]["Sire_Link"]]["Name"])
                edges.append((self._clan_df[self._clan_df["Link"] == vamp[1]["Sire_Link"]]["Name"].item(), 
                            vamp[1]["Name"]))
                
            elif (vamp[1]["Sire"] in list(self._clan_df["Name"])): # if links don't match, append by the name
                edges.append((self._clan_df[self._clan_df["Name"] == vamp[1]["Sire"]]["Name"].item(),
                            vamp[1]["Name"]))

            elif vamp[1]["Sire_Link"] != np.nan: #vampires who do not have a sire
                sireless_vamps.append(vamp[1].index)
        
        return edges
    
    def add_vamps_to_graph(self):
        
        for index, vamp in self._clan_df.iterrows():

            if not np.isnan(vamp["Generation"]): 
                level = vamp["Generation"]

                if vamp["Diablerie"]:

                    self.graph.add_node(node_for_adding=vamp["Name"],
                                label=vamp["Name"] + "\n" + str(int(level)) + " gen",
                                level = level, 
                                color= {"border": f"{self._node_gradient[level]}", "background": "black"},
                                shape = "box",
                                title = vamp["Link"], #title=f"<a href='{vamp["Link"]}' target='_blank'>{vamp["Name"]} \n {int(level)} gen</a>",
                                font = {"color":"white"},
                                Generation = level,
                                Name = vamp["Name"])

                else: 

                    self.graph.add_node(node_for_adding=vamp["Name"],
                                label=vamp["Name"] + "\n" + str(int(level)) + " gen",
                                level = level, 
                                color=self._node_gradient[level],
                                shape = "box",
                                title = vamp["Link"], #title=f"<a href='{vamp["Link"]}' target='_blank'>{vamp["Name"]} \n {int(level)} gen</a>",
                                font = {"color":"white"},
                                Generation = level,
                                Name = vamp["Name"])


        for index, vamp in self._clan_df.iterrows():
            if np.isnan(vamp["Generation"]):
                level = np.random.binomial(n = 15, p = 0.5)
                self.graph.add_node(node_for_adding=vamp["Name"],
                            level = level, 
                            color="#FFFFFF",
                            font = {"color":"black"},
                            title = vamp["Link"],
                            Name = vamp["Name"],
                            shape = "box")

    def generate_network(self, generate_html = True, filter_on =True ):

        edges = self.generate_edges()

        for edge in edges:
            self.graph.add_edge(edge[0], edge[1], Childer_Of=edge[0], Sire_Of=edge[1])

        pos = nx.planar_layout(self.graph)


        self.network = Network(height="800px", directed=True, bgcolor=self._background_color,  filter_menu=filter_on, cdn_resources='remote')
        self.network.from_nx(self.graph)

        if generate_html: 
            self.network.write_html(self._graph_path)
                    

    def set_custom_js_rules(self, iframe_link=True):

        inject_js(self._graph_path, 
          original_pattern = "<html>\n ", 
          new_pattern = f'<html>\n <body style="background-color:{self._background_color};">\n') 

        # update the border to blend in with the background
        inject_js(self._graph_path, 
                original_pattern='<style type="text/css">', 
                new_pattern=f'<style type="text/css">\n\t\t\t#mycard {{\n \t\t\t\tbackground-color: {self._background_color};\n\t\t\t\n  border: 1px solid {self._background_color};\n}}\n #loadingBar {{ display: none !important;}}\n')

        inject_js(self._graph_path, 
                original_pattern='<div class="card" style="width: 100%">', 
                new_pattern='<div id="mycard" class="card" style="width: 100%">')


        inject_js(self._graph_path, 
                original_pattern="border: 1px solid lightgray;", 
                new_pattern=f"border: 1px solid {self._background_color};")
        
        inject_js(self._graph_path, 
          original_pattern="propControl.addOption({id: eachProp, title: eachProp})",
          new_pattern="if (['Generation', 'Name', 'Sire_Of', 'Childer_Of'].includes(eachProp)){\npropControl.addOption({id: eachProp, title: eachProp})\n}\n")
        
        if iframe_link:

            inject_js(self._graph_path, 
            original_pattern="network = new vis.Network(container, data, options);",
            new_pattern="""network = new vis.Network(container, data, options);
                            \n network.on("doubleClick", function(params) {
                            if (params.nodes.length > 0) {
                                var nodeId = params.nodes[0];
                                var node = nodes.get(nodeId);
                                console.log(node)
                                if (node && node.title) {
                                    //window.open(node.title, "_blank");
                                    console.log(window.parent.parent)
                                    window.parent.parent.postMessage({ type: 'LINK', payload: node.title }, "*")
                                }
                            }   
                        });\n""")
        else:
            inject_js(self._graph_path, 
            original_pattern="network = new vis.Network(container, data, options);",
            new_pattern="""network = new vis.Network(container, data, options);
                            \n network.on("doubleClick", function(params) {
                            if (params.nodes.length > 0) {
                                var nodeId = params.nodes[0];
                                var node = nodes.get(nodeId);
                                console.log(node)
                                if (node && node.title) {
                                    window.open(node.title, "_blank");
                                }
                            }   
                        });\n""")