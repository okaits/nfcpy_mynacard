#!/usr/bin/env python3
import argparse
import getpass
import nfc
import nfcpy_mynacard

parser = argparse.ArgumentParser("get_mynumber", description="基本4情報を取得し、標準出力に出力します。")
args = parser.parse_args()

def on_connect(tag: nfc.tag.Tag):
    password = int(getpass.getpass("Password> "))
    attrs = nfcpy_mynacard.input_assistance.get_four_attrs_pw(tag, password)
    print(f"""氏名: {attrs["name"]}
住所: {attrs["address"]}
生年月日: {attrs["birthday"].strftime("%Y/%m/%d")}
性別: {attrs["sex"]}""")

nfcpy_mynacard.card.connect(on_connect)
