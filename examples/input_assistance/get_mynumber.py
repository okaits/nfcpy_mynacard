#!/usr/bin/env python3
import argparse
import getpass
import nfc
import nfcpy_mynacard

parser = argparse.ArgumentParser("get_mynumber", description="個人番号を取得し、標準出力に出力します。")
args = parser.parse_args()

def on_connect(tag: nfc.tag.Tag):
    password = int(getpass.getpass("Password> "))
    mynumber = nfcpy_mynacard.input_assistance.get_mynumber(tag, password)
    print(mynumber)

nfcpy_mynacard.card.connect(on_connect)
