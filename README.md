# nfcpy_mynacard
nfcpyを用いてマイナンバーカードをいじくるライブラリです。

## Features
### JPKI AP
* 利用者認証用電子証明書、署名用電子証明書を抽出（der出力）
* 利用者認証用電子証明書、署名用電子証明書を用いて署名（バイナリ出力）

## Examples
`examples/`ディレクトリに、プログラム例が載っています。
* `examples/jpki/output_certificate.py`: 証明書を出力する（pem出力）
* `examples/jpki/sign_file.py`: ファイルに対して署名する（PKCS#7出力）

## Others
* マイナンバーカードとの通信について、[「マイナンバーカードとAPDUで通信して署名データ作成」](https://tex2e.github.io/blog/protocol/jpki-mynumbercard-with-apdu)、[jpki/mynaソースコード](https://github.com/jpki/myna) を参考にしています。
