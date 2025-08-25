import nfc

import nfcpy_mynacard.card
import nfcpy_mynacard.error

class JPKI:
    """ JPKI AP """
    @staticmethod
    def user_proof_cert(tag: nfc.tag.Tag, password: int) -> None:
        """ 利用者証明用電子証明書のパスワードでログインする
        注: JPKI APを選択している必要があります。 """
        if len(str(password)) != 4:
            raise nfcpy_mynacard.error.InvalidPasswordError

        nfcpy_mynacard.card.select_ef(tag, bytes.fromhex("00 18"))
        encoded_password = str(password).encode(encoding="ascii")
        try:
            nfcpy_mynacard.card.communicate(tag, bytes.fromhex("00 20 00 80") + len(encoded_password).to_bytes() + encoded_password) # PW検証命令を発行
        except nfcpy_mynacard.error.CardCommunicationError as carderr_exc:
            if carderr_exc.res_data[-2] == 0x63:
                incorrectpwd_exc = nfcpy_mynacard.error.IncorrectPasswordError("パスワードが違います。")
                incorrectpwd_exc.res_data = carderr_exc.res_data
                incorrectpwd_exc.remaining_count = carderr_exc.res_data[-1] & 0x0F
                raise incorrectpwd_exc from carderr_exc
            elif carderr_exc.res_data[-2:] == bytes.fromhex("69 84"):
                blockedpwd_exc = nfcpy_mynacard.error.PasswordDisabledError("パスワード試行回数の上限を超えました。市町村役場にて対応を受けてください。")
                blockedpwd_exc.res_data = carderr_exc.res_data
                raise blockedpwd_exc from carderr_exc
            else:
                raise
        return

    @staticmethod
    def signature_cert(tag: nfc.tag.Tag, password: str):
        """ 署名用電子証明書のパスワードでログインする
        注: JPKI APを選択している必要があります。"""
        if not (6 <= len(str(password)) <= 16):
            raise nfcpy_mynacard.error.InvalidPasswordError
        if not (password.isalnum() and password.isascii()):
            raise nfcpy_mynacard.error.InvalidPasswordError
        password = password.upper()

        nfcpy_mynacard.card.select_ef(tag, bytes.fromhex("00 1B"))
        encoded_password = str(password).encode(encoding="ascii")
        try:
            nfcpy_mynacard.card.communicate(tag, bytes.fromhex("00 20 00 80") + len(encoded_password).to_bytes() + encoded_password) # PW検証命令を発行
        except nfcpy_mynacard.error.CardCommunicationError as carderr_exc:
            if carderr_exc.res_data[-2] == 0x63:
                incorrectpwd_exc = nfcpy_mynacard.error.IncorrectPasswordError("パスワードが違います。")
                incorrectpwd_exc.res_data = carderr_exc.res_data
                incorrectpwd_exc.remaining_count = carderr_exc.res_data[-1] & 0x0F
                raise incorrectpwd_exc from carderr_exc
            elif carderr_exc.res_data[-2:] == bytes.fromhex("69 84"):
                blockedpwd_exc = nfcpy_mynacard.error.PasswordDisabledError("パスワード試行回数の上限を超えました。市町村役場にて対応を受けてください。")
                blockedpwd_exc.res_data = carderr_exc.res_data
                raise blockedpwd_exc from carderr_exc
            else:
                raise
        return

class InputAssistance:
    """ 券面事項入力補助 AP """
    @staticmethod
    def password_auth(tag: nfc.tag.Tag, password: int):
        """ 券面事項入力補助APのパスワードを用いてログインする
        注: 券面事項入力補助 APを選択している必要があります。 """
        if len(str(password)) != 4:
            raise nfcpy_mynacard.error.InvalidPasswordError

        nfcpy_mynacard.card.select_ef(tag, bytes.fromhex("00 11"))
        encoded_password = str(password).encode(encoding="ascii")
        try:
            nfcpy_mynacard.card.communicate(tag, bytes.fromhex("00 20 00 80") + len(encoded_password).to_bytes() + encoded_password) # PW検証命令を発行
        except nfcpy_mynacard.error.CardCommunicationError as carderr_exc:
            if carderr_exc.res_data[-2] == 0x63:
                incorrectpwd_exc = nfcpy_mynacard.error.IncorrectPasswordError("パスワードが違います。")
                incorrectpwd_exc.res_data = carderr_exc.res_data
                incorrectpwd_exc.remaining_count = carderr_exc.res_data[-1] & 0x0F
                raise incorrectpwd_exc from carderr_exc
            elif carderr_exc.res_data[-2:] == bytes.fromhex("69 84"):
                blockedpwd_exc = nfcpy_mynacard.error.PasswordDisabledError("パスワード試行回数の上限を超えました。市町村役場にて対応を受けてください。")
                blockedpwd_exc.res_data = carderr_exc.res_data
                raise blockedpwd_exc from carderr_exc
            else:
                raise
        return
    
    @staticmethod
    def bcode_auth(tag: nfc.tag.Tag, bcode: int):
        """ 照会番号Bを用いてログインする """
        if len(str(bcode)) != 14:
            raise nfcpy_mynacard.error.IncorrectPasswordError("照会番号Bの形式が異なります。生年がカードに記載された2桁であることを確認してください。")

        nfcpy_mynacard.card.select_ef(tag, bytes.fromhex("00 15"))
        encoded_bcode = str(bcode).encode(encoding="ascii")
        try:
            nfcpy_mynacard.card.communicate(tag, bytes.fromhex("00 20 00 80") + len(encoded_bcode).to_bytes() + encoded_bcode)
        except nfcpy_mynacard.error.CardCommunicationError as carderr_exc:
            if carderr_exc.res_data[-2] == 0x63:
                incorrectpwd_exc = nfcpy_mynacard.error.IncorrectPasswordError("照会番号Bが違います。")
                incorrectpwd_exc.res_data = carderr_exc.res_data
                incorrectpwd_exc.remaining_count = carderr_exc.res_data[-1] & 0x0F
                raise incorrectpwd_exc from carderr_exc
            elif carderr_exc.res_data[-2:] == bytes.fromhex("69 84"):
                blockedpwd_exc = nfcpy_mynacard.error.PasswordDisabledError("照会番号Bの試行回数の上限を超えました。市町村役場にて対応を受けてください。")
                blockedpwd_exc.res_data = carderr_exc.res_data
                raise blockedpwd_exc from carderr_exc
            else:
                raise

    @staticmethod
    def acode_auth(tag: nfc.tag.Tag, acode: int):
        """ 照会番号Aを用いてログインする """
        if len(str(acode)) != 12:
            raise nfcpy_mynacard.error.IncorrectPasswordError("照会番号Aの形式が異なります。")

        nfcpy_mynacard.card.select_ef(tag, bytes.fromhex("00 14"))
        encoded_bcode = str(acode).encode(encoding="ascii")
        try:
            nfcpy_mynacard.card.communicate(tag, bytes.fromhex("00 20 00 80") + len(encoded_bcode).to_bytes() + encoded_bcode)
        except nfcpy_mynacard.error.CardCommunicationError as carderr_exc:
            if carderr_exc.res_data[-2] == 0x63:
                incorrectpwd_exc = nfcpy_mynacard.error.IncorrectPasswordError("照会番号Aが違います。")
                incorrectpwd_exc.res_data = carderr_exc.res_data
                incorrectpwd_exc.remaining_count = carderr_exc.res_data[-1] & 0x0F
                raise incorrectpwd_exc from carderr_exc
            elif carderr_exc.res_data[-2:] == bytes.fromhex("69 84"):
                blockedpwd_exc = nfcpy_mynacard.error.PasswordDisabledError("照会番号Aの試行回数の上限を超えました。市町村役場にて対応を受けてください。")
                blockedpwd_exc.res_data = carderr_exc.res_data
                raise blockedpwd_exc from carderr_exc
            else:
                raise
