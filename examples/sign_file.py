#!/usr/bin/env python3
import argparse
import getpass
import nfc
import asn1crypto.cms
import asn1crypto.util
import asn1crypto.x509
import asn1crypto.pem
import nfcpy_mynacard

parser = argparse.ArgumentParser("output_certificate", description="指定された証明書を用いてファイルに署名します。")
parser.add_argument("file", help="署名対象のファイル")
parser.add_argument("output", help="出力先のファイル")
cmd = parser.add_mutually_exclusive_group(required=True)
cmd.add_argument("--signature", action="store_true", help="署名用電子証明書を使用します。")
cmd.add_argument("--userproof", action="store_true", help="利用者認証用電子証明書を使用します。")

args = parser.parse_args()

def on_connect(tag: nfc.tag.Tag):
    with open(args.file, "rb") as h:
        target_data = h.read()

    password = getpass.getpass("Password> ")

    # 以下、https://stackoverflow.com/questions/58664221/creating-and-saving-cms-pkcs7-objects-in-python を大幅に参考にしています。
    # SignedDataオブジェクト生成
    signature = asn1crypto.cms.SignedData()
    signature["version"] = "v1"
    signature["encap_content_info"] = asn1crypto.util.OrderedDict([
        ("content_type", "data"),
        ("content", target_data)
    ])
    signature["digest_algorithms"] = [
        asn1crypto.util.OrderedDict({
            ("algorithm", "sha256"),
            ("parameters", None)
        })
    ]

    # 証明書の抽出
    if args.signature:
        cert_der = nfcpy_mynacard.jpki.SignatureCert.get_cert(tag, password)
    elif args.userproof:
        cert_der = nfcpy_mynacard.jpki.UserProofCert.get_cert(tag)
    else: assert False

    cert = asn1crypto.x509.Certificate.load(cert_der)

    signature["certificates"] = [cert]

    # SignerInfoオブジェクト生成
    signer = asn1crypto.cms.SignerInfo()
    signer["version"] = "v1"
    signer["digest_algorithm"] = asn1crypto.util.OrderedDict([
        ("algorithm", "sha256"),
        ("parameters", None)
    ])
    signer["signature_algorithm"] = asn1crypto.util.OrderedDict([
        ("algorithm", "sha256_rsa"),
        ("parameters", None)
    ])

    # データに署名
    if args.signature:
        sign_bin = nfcpy_mynacard.jpki.SignatureCert.sign_data(tag, password, target_data)
    else:
        sign_bin = nfcpy_mynacard.jpki.UserProofCert.sign_data(tag, password, target_data)

    signer["signature"] = sign_bin
    signer["sid"] = asn1crypto.cms.SignerIdentifier({"subject_key_identifier": cert.key_identifier_value.native})

    signature["signer_infos"] = [signer]

    output = asn1crypto.cms.ContentInfo()
    output["content_type"] = "signed_data"
    output["content"] = signature

    with open(args.output, "wb") as h:
        h.write(asn1crypto.pem.armor("PKCS7", output.dump()))

nfcpy_mynacard.card.connect(on_connect)
