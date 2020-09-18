import pexpect


def test():
    cmd = f"python main.py example-keys.yml"
    child = pexpect.spawn(cmd, encoding="utf-8", timeout=10)
    out = child.read().strip()
    child.expect(pexpect.EOF)

    assert "OK: 3, ERROR: 2, ALL: 5, UNIQUE: 4" in out
