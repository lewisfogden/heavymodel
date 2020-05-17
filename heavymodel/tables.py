# tables.py



class MortalityTable:
    """mortalitytable is a matrix, by age and duration."""
    def __init__(self, csv_filename, name, select_period, pc_of_base=1):
        self.filename = csv_filename
        self.name = name
        self.select_period = select_period
        self.pc_of_base = pc_of_base
        self.load_csv(self.filename, self.select_period)
    
    def load_csv(self, filename, select_period):
        with open(filename, 'r') as csv_file:
            header = None
            self.q = dict()
            for raw_line in csv_file:
                line_array = raw_line.strip("\n").split(",")
                if header is None:
                    header = line_array
                    if len(header) != select_period + 2:
                        raise ValueError("csv file does not have correct number of columns for select period.")
                else:
                    age = int(line_array[0])
                    values = line_array[1:]
                    for duration, value in enumerate(values):
                        if value != "":
                            self.q[age, duration] = float(value) * self.pc_of_base
        
    def get(self, age, duration):
        if duration > self.select_period:
            return self.q[(age, self.select_period)]
        else:
            return self.q[(age, duration)]
    
    def __getitem__(self, key):
        age, duration = key
        return self.get(age, duration)
    
class MortalityImprovementTable:
    """MortalityImprovementTable is a matrix, by age and year."""
    def __init__(self, csv_filename):
        self.filename = csv_filename
        self.load_csv(self.filename)
    
    def load_csv(self, filename):
        with open(filename, 'r') as csv_file:
            header = None
            self.q = dict()
            for raw_line in csv_file:
                line_array = raw_line.strip("\n").split(",")
                if header is None:
                    header = line_array
                    years = [int(year) for year in header[1:]]
                else:
                    age = int(line_array[0])
                    values = line_array[1:]
                    for year, value in zip(years, values):
                        if value != "":
                            self.q[age, year] = float(value)
        
    def get(self, age, year):
        return self.q[(age, year)]
    
    def __getitem__(self, key):
        age, year = key
        return self.get(age, year)
    
class RangeTable:
    """range table"""
    def __init__(self, filename=None):
        with open(filename, 'r') as csv_file:
            header = None
            self.data = dict()
            for raw_line in csv_file:
                line_array = raw_line.strip("\n").split(",")
                if header is None:
                    header = line_array
                else:
                    key = int(line_array[0])
                    value = float(line_array[1])
                    self.data[key] = value
            self.max = max(self.data)
            self.min = min(self.data)
    def __getitem__(self, key):
        if key > self.max:
            return 1
        elif key < self.min:
            return 0
        else:
            return self.data[key]

class YieldCurve:
    def __init__(self, filename, key_period="annual", rate_type="spot_rate"):
        self.filename = filename
        self.key_period = key_period
        self.rate_type = rate_type
        with open(self.filename, 'r') as csv_file:
            header = None
            self.spot_annual = dict()
            for raw_line in csv_file:
                line_array = raw_line.strip("\n").split(",")
                if header is None:
                    header = line_array
                else:
                    key = int(line_array[0])
                    value = float(line_array[1])
                    self.spot_annual[key] = value
            self.max_t = key * 12
            self.max_t_years = key
        self._build_tables()
    
    def _build_tables(self):
        self.v = dict() # discount factor, monthly
        self.s = dict() # spot rate, monthly
        for t in range(self.max_t):
            t_years = int(t/12)
            self.s[t] = (1 + self.spot_annual[t_years]) ** (1/12) - 1
            self.v[t] = (1 + self.s[t])**(-t)
    def npv(self, cashflow, proj_len):
        pv = 0.0
        for t in range(0, proj_len):
            pv += self.v[t] * cashflow(t)
        return pv

class ModelPoints:
    header_types = {"str":str,
                    "int":int,
                    "float":float,
                    "bool":bool
                    }
    def __init__(self, filename):
        self.filename = filename
        self.mps = []
        with open(self.filename, 'r') as csv_file:
            header = None
            for raw_line in csv_file:
                line_array = raw_line.strip("\n").split(",")
                if header is None:
                    header = line_array
                    self.col_names = []
                    self.col_types = []
                    for col in line_array:
                        self.col_types.append(self.header_types[col.split(":")[0]])
                        self.col_names.append(col.split(":")[1])
                   
                else:
                    mp = {col_name:col_type(col) for col, col_name, col_type in zip(line_array, self.col_names, self.col_types)}
                    self.mps.append(mp)
    def __iter__(self):
        return iter(self.mps)
    
    def __getitem__(self, key):
        return self.mps[key]

