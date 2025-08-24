import collections.abc
import typing
import nfc
import nfcpy_mynacard.error

AP_DF = {
    "JPKI": bytes.fromhex("D3 92 F0 00 26 01 00 00 00 01")
}

def connect(callback: collections.abc.Callable[[nfc.tag.Tag], typing.Any]):
    """ マイナンバーカードに接続する。 """
    clf = nfc.ContactlessFrontend("usb")
    clf.connect(rdwr={"on-connect": callback, "targets": {"106B"}})

def communicate(tag: nfc.tag.Tag, apdu: bytes) -> bytes:
    """ マイナンバーカードとバイナリを送受信。 """
    res = bytes(tag.transceive(apdu))
    if len(res) < 2:
        # ？？？
        exc = nfcpy_mynacard.error.CardCommunicationError("マイナンバーカードが不正な応答をしました。")
        exc.res_data = res
        raise exc
    if res[-2:] == bytes.fromhex("90 00"):
        # 成功応答
        return res[:-2]
    exc = nfcpy_mynacard.error.CardCommunicationError("マイナンバーカードでの処理に失敗しました。")
    exc.res_data = res
    raise exc

def select_ap(tag: nfc.tag.Tag, df: bytes):
    """ AP（DF）を選択。 """
    communicate(tag, bytes.fromhex("00 A4 04 0C 0A") + df)

def select_ef(tag: nfc.tag.Tag, ef: bytes):
    """ EFを選択。 """
    communicate(tag, bytes.fromhex("00 A4 02 0C 02") + ef)
