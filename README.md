# nfcpy_mynacard
nfcpyを用いてマイナンバーカードをいじくるライブラリです。

## Installtion
```
python3 -m pip install git+https://github.com/okaits/nfcpy_mynacard@v0.0.1
```

## Features
### JPKI AP
* 利用者証明用電子証明書、署名用電子証明書を抽出（der出力）
* 利用者証明用電子証明書、署名用電子証明書を用いて署名（バイナリ出力）

### 券面事項入力補助 AP
* パスワードもしくは照会番号Aで個人番号を出力
* パスワードもしくは照会番号Bで基本4情報を出力

#### 照会番号A
個人番号（マイナンバー）12桁のことです。

#### 照会番号B
* 生年月日（6桁）
* 有効期限の西暦（4桁）
* カード表面左下のセキュリティコード（4桁）

これらをそのまま結合した14桁の数字のことです。  
> [!CAUTION]
> 生年月日の年は、カードに記載されている通りの**2桁**です。  
> たとえば、平成21年10月29日生まれで、有効期限が2025年10月29日なら、`2110292025????`となります。

## Examples
`examples/`ディレクトリに、プログラム例が載っています。
* `examples/jpki/output_certificate.py`: 証明書を出力する（pem出力）
* `examples/jpki/sign_file.py`: ファイルに対して署名する（PKCS#7出力）
* `examples/input_assistance/get_four_attrs.py`: 基本4事項を取得する
* `examples/input_assistance/get_mynumber.py`: 個人番号（マイナンバー）を取得する（法規制に注意！）

`/docs/quickstart.md`も参考にしてください。

## Others
* マイナンバーカードとの通信について、[「マイナンバーカードとAPDUで通信して署名データ作成」](https://tex2e.github.io/blog/protocol/jpki-mynumbercard-with-apdu)、[jpki/mynaソースコード](https://github.com/jpki/myna) を参考にしています。
