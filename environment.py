from errors import error


class Environment:
    def __init__(self):
        self.values = {}

    def assign(self, name, value):
        """
        Assigns the ''value'' to the given ''name''. If that ''name''
        has already been defined, checks whether the type of ''value''
        matches the current value held by ''name''. If it does, the
        assignment is successful, otherwise an error is thrown.
        :param name: Name of the variable.
        :param value: Value of the variable.
        """
        existing_value = self.values.get(name)
        if existing_value is not None:
            try:
                assert isinstance(value, type(existing_value))
            except AssertionError:
                error('', 'Variable type does not match.')
        self.values[name] = value

    def get(self, name):
        """
        Finds and returns the value corresponding to the ''name'',
        if it has been previously defined. Throws an error otherwise.
        :param name: Name of the variable to retrieve.
        :return: Value of that variable if it exists, None otherwise.
        """
        value = self.values.get(name)
        if value is None:
            error('', 'Variable not declared.')
        return value
