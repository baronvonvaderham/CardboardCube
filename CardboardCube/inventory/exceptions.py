class InventoryError(Exception):

    def __init__(self, msg, *args, **kwargs):
        super(InventoryError, self).__init__(msg)


class InvalidInventoryItemException(InventoryError):
    pass
