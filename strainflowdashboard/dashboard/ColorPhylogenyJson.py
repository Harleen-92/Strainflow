import json
COUNTRY_COLOR = {
    "Japan": "#2ecc71",     #Emerald
    "China": "#c0392b",     #Pomegranate
    "Brazil": "#16a085",    #Green Sea
    "South-Africa": "#2c3e50",  #Midnight Blue
    "Australia": "#f1c40f", #Sun Flower
    "France": "#e74c3c",    #Alizarin
    "Mexico": "#0000ff",    #Asbestos
    "USA": "#3498db",       #Peter River
    "Canada": "#9b59b6",    #Amethyst
    "Italy": "#ff0000",     #Red
    "Wales": "#34495e",     #Wet Asphalt
    "Germany": "#f39c12",   #Orange
    "England": "#2980b9",   #Belize Hole
    "Scotland": "#1abc9c",  #Turquoise
    "Northern-Ireland": "#27ae60",  #Nephritis
    "India": "#d35400"      #Pumpkin
}

f = open("dashboard\static\json\phylogenetic.json", "r")
phyloData = json.load(f)

def colorPhylo(dict):
    for d in dict["children"]:
        try:
            if len(d["children"]) > 0:
                colorPhylo(d)
        except KeyError as e:
            for country, col in COUNTRY_COLOR.items():
                if str(d["name"]).endswith(country):
                    d["meta"]["color"] = {"clade":col}
            print("Name: ", d["name"], "Color: ", d["meta"]["color"])

colorPhylo(phyloData["tree"])
f.close()

with open("dashboard\static\json\colored_phylogenetic.json", "w") as fCol:
    json.dump(phyloData, fCol)
