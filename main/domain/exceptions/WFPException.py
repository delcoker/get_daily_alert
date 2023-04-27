class WFPException(Exception):
    """Exception raised for errors for WFP.

        Attributes:
            message -- explanation of the error
        """

    def __init__(self, message="WFP error", errors=None):
        self.message = message
        super().__init__(self.message)

        self.errors = errors
