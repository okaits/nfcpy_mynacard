import datetime
import typing
import nfc
import asn1
import nfcpy_mynacard.card
import nfcpy_mynacard.login

def get_mynumber(tag: nfc.tag.Tag, password: int) -> int:
    """ 個人番号を取得する。（要認証・券面事項入力補助AP用パスワード）（法規制あり） """
    nfcpy_mynacard.card.select_ap(tag, nfcpy_mynacard.card.AP_DF["input_assistance"])
    nfcpy_mynacard.login.InputAssistance.password_auth(tag, password)
    nfcpy_mynacard.card.select_ef(tag, bytes.fromhex("00 01"))
    result = nfcpy_mynacard.card.communicate(tag, bytes.fromhex("00 B0 00 00 00"))
    return int(result[3:15].decode(encoding="ascii"))

class FourAttributesDict(typing.TypedDict):
    """ 基本４情報のdict """
    name: str
    address: str
    birthday: datetime.datetime
    sex: typing.Literal["MALE", "FEMALE", "UNAPPLICABLE", "OTHER"]

def get_four_attrs_pw(tag: nfc.tag.Tag, password: int) -> FourAttributesDict:
    """ 基本4情報を取得する。（要認証・券面事項入力補助AP用パスワード） """
    nfcpy_mynacard.card.select_ap(tag, nfcpy_mynacard.card.AP_DF["input_assistance"])
    nfcpy_mynacard.login.InputAssistance.password_auth(tag, password)
    nfcpy_mynacard.card.select_ef(tag, bytes.fromhex("00 02"))
    result = nfcpy_mynacard.card.communicate(tag, bytes.fromhex("00 B0 00 00 00"))
    decoder = asn1.Decoder()
    decoder.start(result)
    decoder.enter()
    _ = decoder.read()[1]
    name = decoder.read()[1].decode(encoding="utf-8")
    address = decoder.read()[1].decode(encoding="utf-8")

    birthday_str = decoder.read()[1].decode(encoding="utf-8")
    birthday = datetime.datetime(year=int(birthday_str[0:4]), month=int(birthday_str[4:6]), day=int(birthday_str[6:8]))

    sex_int = int(decoder.read()[1].decode(encoding="utf-8"))
    sex: typing.Literal["MALE", "FEMALE", "UNAPPLICABLE", "OTHER"]
    match sex_int:
        case 1:
            sex = "MALE"
        case 2:
            sex = "FEMALE"
        case 9:
            sex = "UNAPPLICABLE"
        case _:
            sex = "OTHER"

    return {"name": name, "address": address, "birthday": birthday, "sex": sex}
