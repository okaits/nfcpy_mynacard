import nfc

import nfcpy_mynacard.card
import nfcpy_mynacard.error

class JPKI:
    """ JPKI AP """
    @staticmethod
    def user_proof_cert(tag: nfc.tag.Tag, password: int) -> None:
        """ 利用者認証用電子証明書のパスワードでログインする
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
