#!/usr/bin/env python3
import argparse
import getpass
import nfc
import nfcpy_mynacard

parser = argparse.ArgumentParser("get_mynumber", description="個人番号を取得し、標準出力に出力します。")
parser.add_argument("--acode", "-A", action="store_true", help="紹介番号Aを用いて取得する", required=False)
args = parser.parse_args()

def on_connect(tag: nfc.tag.Tag):
    if args.acode:
        acode = int(getpass.getpass("ACode> "))
        mynumber = nfcpy_mynacard.input_assistance.get_mynumber(tag, acode=acode)
    else:
        password = int(getpass.getpass("Password> "))
        mynumber = nfcpy_mynacard.input_assistance.get_mynumber(tag, password=password)
    print(mynumber)

nfcpy_mynacard.card.connect(on_connect)
