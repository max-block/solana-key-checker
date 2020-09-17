import os
import sys
import tempfile
from dataclasses import dataclass
from typing import List

import pexpect
import yaml


@dataclass
class Key:
    name: str
    public: str
    private: str


def load_keys(keys_file: str) -> List[Key]:
    if not os.path.isfile(keys_file):
        print(f"Can't keys file: {keys_file}")
        exit(1)

    with open(keys_file) as f:
        res = yaml.full_load(f)
        return [Key(**k) for k in res["keys"]]


def verify_key(key: Key) -> bool:
    with tempfile.NamedTemporaryFile(mode="w+t") as f:
        f.write(key.private)
        f.flush()
        cmd = f"solana-keygen verify {key.public} {f.name}"
        child = pexpect.spawn(cmd, encoding="utf-8", timeout=5)
        out = child.read().strip()
        child.expect(pexpect.EOF)

        if out == f"Verification for public key: {key.public}: Success":
            print(f"{key.name}\t\t{key.public}\t\t\tOK")
            return True
        else:
            print(f"{key.name}\t\t{key.public}\t\t\tERROR")
            return False


def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py path/to/keys.yaml")
        exit(1)

    keys = load_keys(sys.argv[1])
    ok_count = 0
    error_count = 0
    for key in keys:
        r = verify_key(key)
        if r:
            ok_count += 1
        else:
            error_count += 1
    print(f"\nOK: {ok_count}, ERROR: {error_count}")


if __name__ == "__main__":
    main()
