from main.domain.exceptions.WFPException import WFPException


class FileTypeUnsupportedException(WFPException):

    def __init__(self, message, errors=None):
        self.message = message if message else super().__init__(self.message)
        super().__init__(self.message)
