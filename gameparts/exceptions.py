# gameparts/exceptions.py
IndexError
class NotImplementedError(RuntimeError): 

    def __str__(self):
        return 'Не прописан метод draw, отрисовывающий объекты.'