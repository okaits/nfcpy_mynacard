import argparse
import getpass
import nfc
import asn1crypto.pem
import nfcpy_mynacard

parser = argparse.ArgumentParser("output_certificate", description="指定された証明書を標準出力に出力します。")
cmd = parser.add_mutually_exclusive_group(required=True)
cmd.add_argument("--signature", action="store_true", help="署名用電子証明書を出力します。")
cmd.add_argument("--userproof", action="store_true", help="利用者認証用電子証明書を出力します。")

args = parser.parse_args()

def on_connect(tag: nfc.tag.Tag):
    if args.signature:
        cert_der = nfcpy_mynacard.jpki.SignatureCert.get_cert(tag, getpass.getpass("Password> "))
        cert_pem = asn1crypto.pem.armor("CERTIFICATE", cert_der)
        print(cert_pem.decode(encoding="ascii"))

    elif args.userproof:
        cert_der = nfcpy_mynacard.jpki.UserProofCert.get_cert(tag)
        cert_pem = asn1crypto.pem.armor("CERTIFICATE", cert_der)
        print(cert_pem.decode(encoding="ascii"))

    else: assert False

nfcpy_mynacard.card.connect(on_connect)
