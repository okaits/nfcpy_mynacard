import typing
import nfc
import nfcpy_mynacard.login
import nfcpy_mynacard.card

class UserProofCert:
    """ 利用者認証用電子証明書 """
    @staticmethod
    def get_cert(tag: nfc.tag.Tag) -> typing.Annotated[bytes, "DER"]:
        """ 利用者認証用電子証明書を取得し、der形式のbytesで返却する。（認証不要） """
        nfcpy_mynacard.card.select_ap(tag, nfcpy_mynacard.card.AP_DF["JPKI"])
        nfcpy_mynacard.card.select_ef(tag, bytes.fromhex("00 0A"))

        # |00 B0|00 00 |00|00 00 |
        # |cmd  |offset|00|length|
        cert_der = nfcpy_mynacard.card.communicate(tag, bytes.fromhex("00 B0 00 00 00 00 00"))

        return cert_der

class SignatureCert:
    """ 署名用電子証明書 """
    @staticmethod
    def get_cert(tag: nfc.tag.Tag, password: str) -> typing.Annotated[bytes, "DER"]:
        """ 署名用電子証明書を取得し、der形式のbytesで返却する。（要認証・JPKI署名用電子証明書） """
        nfcpy_mynacard.card.select_ap(tag, nfcpy_mynacard.card.AP_DF["JPKI"])
        nfcpy_mynacard.login.JPKI.signature_cert(tag, password)
        nfcpy_mynacard.card.select_ef(tag, bytes.fromhex("00 01"))

        # |00 B0|00 00 |00|00 00 |
        # |cmd  |offset|00|length|
        cert_der = nfcpy_mynacard.card.communicate(tag, bytes.fromhex("00 B0 00 00 00 00 00"))

        return cert_der
