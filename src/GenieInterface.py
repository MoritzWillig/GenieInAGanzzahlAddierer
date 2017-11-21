from .helpers.AbstractMethod import AbstractMethod


class GenieInterface(object):

    def __init__(self, configuration, additional):
        self._configuration = configuration

    @AbstractMethod
    def get_inputs(self):
        """
        :return: name - type
        :rtype: Dict{string, string}
        """
        pass

    @AbstractMethod
    def get_outputs(self):
        """
        :return: name - type
        :rtype: Dict{string, string}
        """
        pass

    @AbstractMethod
    def get_config_for_input(self, name):
        """
        output a DataType configuration for parsing value strings into data instances
        :param name: name of the input parameter
        :type name: string
        :return: DataType configuration
        :rtype: Dict{string, Any}
        """
        pass

    @AbstractMethod
    def serve(self, input):
        """

        :param input:
        :return: genie response
        :rtype: string
        """
