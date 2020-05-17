class QSSReader:
    def __init__(self):
        pass

    @staticmethod
    def read_qss(qssfile: str) -> str:
        with open(qssfile, 'r') as f:
            return f.read()
