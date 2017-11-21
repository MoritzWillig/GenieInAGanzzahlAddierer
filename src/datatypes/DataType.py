from ..helpers.AbstractMethod import AbstractMethod

class DataType(object):

    def __init__(self):
        pass

    @AbstractMethod
    def get_name(self):
        pass

    @AbstractMethod
    def create_instance(self):
        pass

    @AbstractMethod
    def create_instance_with_value(self, value):
        pass

    @AbstractMethod
    def create_instance_with_config(self, value_str, config):
        """

        :param value_str:
        :param config:
            configuration objects containing parsing or creation hints or contstraints.
            Interpretation of hints is DataType specific. Common hints are:

            default: default value, if value_str is empty

            for numeric types:
            min: minimum value constraint
            max: maximum value constraint
        :type config: Dict{string, Any}
        :return:
        """
        pass
