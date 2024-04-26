class NotImplementedError(RuntimeError):
    """Класс для проверки на перезапись метода"""

    def __str__(self):
        """Проверки метода draw на ошибку"""
        return 'Не прописан метод draw, отрисовывающий объекты.'
