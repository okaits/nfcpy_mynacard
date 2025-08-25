import typing
import hashlib
import nfc
import asn1
import nfcpy_mynacard.login
import nfcpy_mynacard.card

class UserProofCert:
    """ 利用者証明用電子証明書 """
    @staticmethod
    def get_cert(tag: nfc.tag.Tag) -> typing.Annotated[bytes, "DER"]:
        """ 利用者証明用電子証明書を取得し、der形式のbytesで返却する。（認証不要） """
        nfcpy_mynacard.card.select_ap(tag, nfcpy_mynacard.card.AP_DF["JPKI"])
        nfcpy_mynacard.card.select_ef(tag, bytes.fromhex("00 0A"))

        # |00 B0|00 00 |00|00 00 |
        # |cmd  |offset|00|length|
        cert_der = nfcpy_mynacard.card.communicate(tag, bytes.fromhex("00 B0 00 00 00 00 00"))

        return cert_der
    
    @staticmethod
    def sign_data(tag: nfc.tag.Tag, password: int, data: bytes) -> bytes:
        """ データを署名し、bytesで返却する。（要認証・JPKI利用者証明用電子証明書） """
        nfcpy_mynacard.card.select_ap(tag, nfcpy_mynacard.card.AP_DF["JPKI"])
        nfcpy_mynacard.login.JPKI.user_proof_cert(tag, password)
        nfcpy_mynacard.card.select_ef(tag, bytes.fromhex("00 17"))

        # 署名の命令の前に、DigestInfo（ASN.1）を発行する
        digestinfo_encoder = asn1.Encoder()
        digestinfo_encoder.start()
        digestinfo_encoder.enter(asn1.Numbers.Sequence)
        digestinfo_encoder.enter(asn1.Numbers.Sequence)
        digestinfo_encoder.write("2.16.840.1.101.3.4.2.1", asn1.Numbers.ObjectIdentifier)
        digestinfo_encoder.write(None, asn1.Numbers.Null)
        digestinfo_encoder.leave()
        digestinfo_encoder.write(hashlib.sha256(data).digest(), asn1.Numbers.OctetString)
        digestinfo_encoder.leave()
        digestinfo = digestinfo_encoder.output()

        # 満を持して署名を命令
        sign_result = nfcpy_mynacard.card.communicate(tag, bytes.fromhex("80 2A 00 80") + len(digestinfo).to_bytes() + digestinfo + (0).to_bytes())
        return sign_result

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
    
    @staticmethod
    def sign_data(tag: nfc.tag.Tag, password: str, data: bytes) -> bytes:
        """ データを署名し、bytesで返却する。（要認証・JPKI署名用電子証明書） """
        nfcpy_mynacard.card.select_ap(tag, nfcpy_mynacard.card.AP_DF["JPKI"])
        nfcpy_mynacard.login.JPKI.signature_cert(tag, password)
        nfcpy_mynacard.card.select_ef(tag, bytes.fromhex("00 1A"))

        # 署名の命令の前に、DigestInfo（ASN.1）を発行する
        digestinfo_encoder = asn1.Encoder()
        digestinfo_encoder.start()
        digestinfo_encoder.enter(asn1.Numbers.Sequence)
        digestinfo_encoder.enter(asn1.Numbers.Sequence)
        digestinfo_encoder.write("2.16.840.1.101.3.4.2.1", asn1.Numbers.ObjectIdentifier)
        digestinfo_encoder.write(None, asn1.Numbers.Null)
        digestinfo_encoder.leave()
        digestinfo_encoder.write(hashlib.sha256(data).digest(), asn1.Numbers.OctetString)
        digestinfo_encoder.leave()
        digestinfo = digestinfo_encoder.output()

        # 満を持して署名を命令
        sign_result = nfcpy_mynacard.card.communicate(tag, bytes.fromhex("80 2A 00 80") + len(digestinfo).to_bytes() + digestinfo + (0).to_bytes())
        return sign_result
