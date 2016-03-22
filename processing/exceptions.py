

class FileNotSupportedException(Exception):
    def __init__(self, expr, msg):
        self.expr = expr
        self.msg = msg

    def __str__(self):
        return self.msg
