# Quickstart
以下のようにすると、マイナンバーカードが接続され、nfc.tag.Tagオブジェクトが返されます。  
以降、このオブジェクトをメソッドに渡すことで、各種APが使えます。
```py
import nfcpy_mynacard
tag = nfcpy_mynacard.connect()
```

## JPKI AP
### 証明書取得
```py
# 署名用電子証明書をもらってくる（DER形式のbytesで帰ってきます。）
signature_cert = nfcpy_mynacard.jpki.SignatureCert.get_cert(tag, "password")

# 利用者証明用電子証明書をもらってくる（DER形式のbytesで帰ってきます。）
userproof_cert = nfcpy_mynacard.jpki.UserProofCert.get_cert(tag)
```

### 署名
```py
to_be_signed = "署名対象データ".encode(encoding="utf-8")

# 署名用電子証明書で署名する（bytesで帰ってきます。）
signature = nfcpy_mynacard.jpki.SignatureCert.sign_data(tag, "password", to_be_signed)

# 利用者証明用電子証明書で署名する（bytesで帰ってきます。）
userproof_cert = nfcpy_mynacard.jpki.UserProofCert.sign_data(tag, "password", to_be_signed)
```

## 券面事項入力補助AP
### 個人番号（マイナンバー）取得（法規制に注意！）
```py
# 券面事項入力補助AP用パスワード（4桁のint）を用いてマイナンバーを取得（intで帰ってきます。）
mynumber = nfcpy_mynacard.input_assistance.get_mynumber(tag, password=1234)

# 照会番号A（12桁のint、マイナンバー）を用いてマイナンバーを取得（intで帰ってきます。）
mynumber = nfcpy_mynacard.input_assistance.get_mynumber(tag, acode=1234_5678_9012)
```

### 基本4情報の取得
```py
# 券面事項入力補助AP用パスワード（4桁のint）を用いて基本4情報を取得（dictで帰ってきます。）
four_attrs = nfcpy_mynacard.input_assistance.get_four_attrs(tag, password=1234)

# 紹介番号B（14桁のint、詳細は/README.mdを参照）を用いて基本4情報を取得（dictで帰ってきます。）
four_attrs = nfcpy_mynacard.input_assistance.get_four_attrs(tag, bcode=211029_2025_1234)


name = four_attrs["name"] # 氏名（str）
address = four_attrs["address"] # 住所（str）
birthday = four_attrs["birthday"] # 誕生日（datetime.datetime）
sex = four_attrs["sex"] # 性別（str: "MALE", "FEMALE", "NOT_APPLICABLE", "OTHER"のいずれか）
```

## その他
対応していないAP・操作については、自力でAPDUを発行することもできます。
```py
# APを選択
nfcpy_mynacard.card.select_ap(tag, bytes.fromhex("D3 92 F0 00 26 01 00 00 00 01"))

# EFを選択
nfcpy_mynacard.card.select_ef(tag, bytes.fromhex("00 AA"))

# APDUを発行
nfcpy_mynacard.card.communicate(tag, bytes.fromhex("00 B0 00 00 00 00 00"))
```
