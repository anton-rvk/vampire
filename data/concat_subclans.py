import pandas as pd

cappadocian = pd.read_csv("data/hecata_subclans/cappadocian.csv")
giovanni = pd.read_csv("data/hecata_subclans/giovanni.csv")
hecata = pd.read_csv("data/hecata_subclans/hecata.csv")

hecata_full = pd.concat([cappadocian, giovanni, hecata], axis = 0, ignore_index=True)
hecata_full.drop("Unnamed: 0", axis = 'columns', inplace= True)

hecata_full.drop_duplicates(subset=["Name"], inplace=True)
hecata_full.to_csv("data/hecata.csv")

caitiff = pd.read_csv("data/caitiff_subclans/caitiff.csv")
unknown = pd.read_csv("data/caitiff_subclans/vampires of unknown clan (wod).csv")

caitiff_full = pd.concat([caitiff, unknown], axis = 0, ignore_index=True)
caitiff_full.drop("Unnamed: 0", axis = 'columns', inplace= True)
caitiff_full.drop_duplicates(subset=["Name"], inplace=True)


caitiff_full.to_csv("data/caitiff.csv")

