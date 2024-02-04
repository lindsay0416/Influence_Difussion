# Define the graph structure

graph = {
    'graph-1':{'N1': {'N39': 0.81, 'N32': 0.96, 'N9': 0.23, 'N4': 0.6},
    'N39': {'N21': 0.1, 'N1': 0.81, 'N7': 0.54, 'N16': 0.41},
    'N32': {'N19': 0.5, 'N29': 0.44,'N20': 0.25,'N41': 0.61,'N45': 0.16,'N1': 0.96,'N11': 0.12,'N15': 0.68,'N26': 0.87},
    'N9': {'N45': 0.8,'N16':0.27,'N42':0.7,'N38':0.71,'N1':0.23,'N3':0.01},
    'N2': {'N31': 0.08, 'N11':0.29,'N29': 0.46, 'N49': 0.42},
    'N31': {'N49': 0.16,'N42':0.4,'N23':0.94,'N2':0.08,'N17':0.53,'N21':0.28},
    'N11': {'N29': 0.36, 'N32': 0.12, 'N28': 0.16, 'N2': 0.29},
    'N29': {'N47': 0.6,'N32': 0.44,'N2': 0.46,'N11': 0.36,'N5': 0.03,'N18': 0.68,'N15': 0.63},
    'N3': {'N9': 0.01, 'N34': 0.95, 'N8': 0.87},
    'N34': {'N33': 0.09, 'N3': 0.95, 'N27': 0.58},
    'N4': {'N1': 0.6,'N27': 0.78,'N18': 0.14,'N20': 0.69,'N36': 0.57,'N38': 0.23},
    'N27': {'N34': 0.58, 'N37': 0.76, 'N47': 0.5, 'N4': 0.78, 'N10': 0.6},
    'N5': {'N29': 0.03, 'N50': 0.09},
    'N6': {'N8': 0.44, 'N17': 0.27, 'N22': 0.99, 'N26': 0.11},
    'N8': {'N3': 0.87,'N10': 0.4,'N15': 0.44,'N21': 0.45,'N50': 0.48,'N6': 0.44},
    'N7': {'N13': 0.14, 'N39': 0.54, 'N14': 0.71, 'N35': 0.15, 'N36': 0.8},
    'N13': {'N18': 0.48, 'N35': 0.6, 'N7': 0.14},
    'N14': {'N28': 0.08, 'N12': 0.57, 'N21': 0.89, 'N42': 0.33, 'N7': 0.71},
    'N35': {'N13': 0.6, 'N37': 0.84, 'N48': 0.98, 'N7': 0.15, 'N10': 0.81},
    'N10': {'N35': 0.81,'N27': 0.6,'N12': 0.62,'N45': 0.27,'N20': 0.31,'N8': 0.4},
    'N45': {'N32': 0.16, 'N9': 0.8, 'N10': 0.27},
    'N16': {'N39': 0.41, 'N19': 0.29, 'N9': 0.27},
    'N42': {'N36': 0.93, 'N14': 0.33, 'N22': 0.41, 'N9': 0.7, 'N31': 0.4},
    'N12': {'N22': 0.66, 'N14': 0.57, 'N10': 0.62},
    'N22': {'N47': 0.95, 'N6': 0.99, 'N17': 0.27, 'N42': 0.41, 'N12': 0.66},
    'N18': {'N4': 0.14, 'N29': 0.68, 'N37': 0.21, 'N13': 0.48},
    'N28': {'N11': 0.16, 'N20': 0.94, 'N40': 0.38, 'N43': 0.7, 'N14': 0.08},
    'N15': {'N32': 0.68, 'N8': 0.44, 'N29': 0.63, 'N40': 0.39},
    'N40': {'N28': 0.38, 'N48': 0.84, 'N23': 0.78, 'N15': 0.39, 'N30': 0.72},
    'N19': {'N32': 0.5, 'N16': 0.29},
    'N17': {'N6': 0.27,'N26': 0.56,'N31': 0.53,'N22': 0.27,'N38': 0.23,'N48': 0.08},
    'N26': {'N6': 0.11,'N32': 0.87,'N46': 0.25,'N49': 0.75,'N17': 0.56,'N24': 0.74},
    'N20': {'N10': 0.31, 'N4': 0.69, 'N28': 0.94, 'N32': 0.25},
    'N21': {'N31': 0.28, 'N8': 0.45, 'N14': 0.89, 'N39': 0.1},
    'N47': {'N50': 0.53,'N27': 0.5,'N46': 0.34,'N23': 0.68,'N48': 0.86,'N29': 0.6,'N22': 0.95,'N30': 0.06},
    'N23': {'N47': 0.68, 'N31': 0.94, 'N40': 0.78},
    'N24': {'N26': 0.74, 'N36': 0.98},
    'N25': {'N49': 0.93},
    'N49': {'N43': 0.56,'N26': 0.75,'N2': 0.42,'N50': 0.78,'N31': 0.16,'N25': 0.93},
    'N30': {'N47': 0.06, 'N40': 0.72},
    'N41': {'N36': 0.67, 'N37': 0.66, 'N32': 0.61},
    'N33': {'N44': 0.3, 'N34': 0.09},
    'N44': {'N43': 0.48, 'N33': 0.3},
    'N36': {'N4': 0.57, 'N7': 0.8, 'N24': 0.98, 'N41': 0.67, 'N42': 0.93},
    'N37': {'N35': 0.84, 'N18': 0.21, 'N27': 0.76, 'N41': 0.66, 'N46': 0.24},
    'N38': {'N17': 0.23, 'N4': 0.23, 'N9': 0.71},
    'N48': {'N35': 0.98, 'N17': 0.08, 'N47': 0.86, 'N40': 0.84},
    'N43': {'N28': 0.7, 'N44': 0.48, 'N49': 0.56},
    'N46': {'N37': 0.24, 'N50': 0.35, 'N26': 0.25, 'N47': 0.34},
    'N50': {'N5': 0.09, 'N8': 0.48, 'N47': 0.53, 'N49': 0.78, 'N46': 0.35}
 },


    'graph-2':{
        "N1": {"N12": 0.29, "N10": 0.92},
        "N2": {"N15": 0.31, "N4": 0.95, "N9": 0.76},
        "N3": {"N15": 0.66, "N4": 0.63, "N7": 0.88},
        "N4": {"N2": 0.95, "N3": 0.63, "N12": 0.24, "N14": 0.69},
        "N5": {"N12": 0.14, "N6": 0.89, "N14": 0.95},
        "N6": {"N5": 0.89},
        "N7": {"N3": 0.88, "N15": 0.84},
        "N8": {"N14": 0.77, "N15": 0.43},
        "N9": {"N2": 0.76, "N13": 0.48, "N12": 0.87},
        "N10": {"N1": 0.92},
        "N11": {"N12": 0.79, "N14": 0.83},
        "N12": {"N1": 0.29, "N4": 0.24, "N5": 0.14, "N9": 0.87, "N11": 0.79},
        "N13": {"N9": 0.48, "N15": 0.51},
        "N14": {"N4": 0.69, "N5": 0.95, "N8": 0.77, "N11": 0.83},
        "N15": {"N2": 0.31, "N3": 0.66, "N7": 0.84, "N8": 0.43, "N13": 0.51}
        },
        'graph-3':{
        'N1': {'N2': 0.7, 'N4': 0.6},
        'N2': {'N1': 0.7, 'N3': 0.3, 'U': 0.9},
        'N3': {'N2': 0.3, 'N4': 0.6, 'B': 0.3},
        'N4': {'N1': 0.6, 'N3': 0.6, 'U': 0.5, 'B': 0.6},
        'B': {'N3': 0.3, 'N4': 0.6, 'A': 0.2},
        'U': {'N2': 0.9, 'N4': 0.5},
        'A': {'B': 0.2}
        }
}