class Validation:
    pass

class ValidationError(KeyError):
    pass

class RangeItem(Validation):
    _type = "RangeItem"
    def __init__(self, type, min, max, step=1):
        self.type = type
        self.min = min
        self.max = max
    def get(self, value):
        val = self.type(value)
        if val < self.min:
            raise ValidationError("Value " + str(val) + " below minimum ("+str(self.min) + ").")
        elif val > self.max:
            raise ValidationError("Value " + str(val) + "above maximum ("+str(self.max) + ").")
        else:
            return val

class ListItem(Validation):
    _type = "ListItem"
    def __init__(self, type, seq):
        self.type = type
        self.seq = seq
    def get(self, value):
        val = self.type(value)
        if val in self.seq:
            return val
        else:
            raise ValidationError("Option " + str(val) + " not in seq: " + repr(self.seq) +".")
            
class QuoteValidation:
    def __init__(self, schema):
        self.schema = schema

    def parse(self, data):
        errors = []
        valid_args = {}
        for arg, validation in self.schema.items():
            try:
                item = data.get(arg, 0, type=validation.type)
            except KeyError:
                errors.append(str(arg) + " not in request.")
                continue
            try:
                valid_item = validation.get(item)
            except ValidationError as err:
                errors.append(str(err))
                continue
            valid_args[arg] = valid_item
        if len(errors) > 0:
            raise KeyError(errors)
        else:
            return valid_args
        