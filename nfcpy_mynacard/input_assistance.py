import datetime
import typing
import nfc
import asn1
import nfcpy_mynacard.card
import nfcpy_mynacard.login

def get_mynumber(tag: nfc.tag.Tag, *, password: typing.Optional[int] = None, acode: typing.Optional[int] = None) -> int:
    """ 個人番号を取得する。（要認証・券面事項入力補助AP用パスワードもしくは照会番号A）（法規制あり） """
    nfcpy_mynacard.card.select_ap(tag, nfcpy_mynacard.card.AP_DF["input_assistance"])

    if password:
        nfcpy_mynacard.login.InputAssistance.password_auth(tag, password)
    elif acode:
        nfcpy_mynacard.login.InputAssistance.acode_auth(tag, acode)
    else:
        raise ValueError("パスワードと照会番号Aの両方が指定されていません。")

    nfcpy_mynacard.card.select_ef(tag, bytes.fromhex("00 01"))
    result = nfcpy_mynacard.card.communicate(tag, bytes.fromhex("00 B0 00 00 00"))
    return int(result[3:15].decode(encoding="ascii"))

class FourAttributesDict(typing.TypedDict):
    """ 基本４情報のdict """
    name: str
    address: str
    birthday: datetime.datetime
    sex: typing.Literal["MALE", "FEMALE", "UNAPPLICABLE", "OTHER"]

def get_four_attrs(tag: nfc.tag.Tag, *, password: typing.Optional[int] = None, bcode: typing.Optional[int] = None) -> FourAttributesDict:
    """ 基本4情報を取得する。（要認証・券面事項入力補助AP用パスワードもしくは照会番号B） """
    nfcpy_mynacard.card.select_ap(tag, nfcpy_mynacard.card.AP_DF["input_assistance"])

    if password:
        nfcpy_mynacard.login.InputAssistance.password_auth(tag, password)
    elif bcode:
        nfcpy_mynacard.login.InputAssistance.bcode_auth(tag, bcode)
    else:
        raise ValueError("パスワードと照会番号Bの両方が指定されていません。")

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
