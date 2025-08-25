#!/usr/bin/env python3
import argparse
import getpass
import nfcpy_mynacard

parser = argparse.ArgumentParser("get_mynumber", description="基本4情報を取得し、標準出力に出力します。")
parser.add_argument("--bcode", "-B", action="store_true", help="紹介番号Bを用いて取得する", required=False)
args = parser.parse_args()

tag = nfcpy_mynacard.card.connect()

if args.bcode:
    bcode = int(getpass.getpass("Bcode> "))
    attrs = nfcpy_mynacard.input_assistance.get_four_attrs(tag, bcode=bcode)
else:
    password = int(getpass.getpass("Password> "))
    attrs = nfcpy_mynacard.input_assistance.get_four_attrs(tag, password=password)

print(f"""氏名: {attrs["name"]}
住所: {attrs["address"]}
生年月日: {attrs["birthday"].strftime("%Y/%m/%d")}
性別: {attrs["sex"]}""")
