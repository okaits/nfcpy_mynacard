class CardCommunicationError(RuntimeError):
    """ カードでの処理に失敗。 """
    res_data: bytes

class InvalidPasswordError(ValueError):
    """ PINの形式がおかしい。（試行前） """

class IncorrectPasswordError(CardCommunicationError):
    """ PINが違う。（試行後） """
    remaining_count: int

class PasswordDisabledError(CardCommunicationError):
    """ パスワード試行回数の上限を超えた。 """
