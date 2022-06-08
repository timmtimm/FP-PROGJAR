cmd = "RECV ads"

print(cmd[:len("RECV ")], "asd")

if "RECV " == cmd[:5]:
    print(cmd[5:])
else:
    print("NAH")
