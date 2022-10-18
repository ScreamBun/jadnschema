"""
Conversion Constants
"""
# Hexadecimal
HexChar = r"[0-9A-Fa-f]"

# IPv4 Address
IPv4_Octet = r"(25[0-5]|2[0-4][0-9]|[01]?[0-9]?[0-9])"
IPv4_Addr = fr"({IPv4_Octet}\.){{3}}{IPv4_Octet}"
IPv4_Mask = r"(3[0-2]|[0-2]?[0-9])"  # 1-32
IPv4_Net = fr"{IPv4_Addr}(\/{IPv4_Mask})?"

# IPv6 Address
IPv6_Octet = fr"{HexChar}{{1,4}}"
IPv6_Addr = (
    fr"({IPv6_Octet}:){{7,7}}{IPv6_Octet}|"             # 1:2:3:4:5:6:7:8
    fr"({IPv6_Octet}:){{1,7}}:|"                        # 1::                                 1:2:3:4:5:6:7::
    fr"({IPv6_Octet}:){{1,6}}:{IPv6_Octet}|"            # 1::8               1:2:3:4:5:6::8   1:2:3:4:5:6::8
    fr"({IPv6_Octet}:){{1,5}}(:{IPv6_Octet}){{1,2}}|"   # 1::7:8             1:2:3:4:5::7:8   1:2:3:4:5::8
    fr"({IPv6_Octet}:){{1,4}}(:{IPv6_Octet}){{1,3}}|"   # 1::6:7:8           1:2:3:4::6:7:8   1:2:3:4::8
    fr"({IPv6_Octet}:){{1,3}}(:{IPv6_Octet}){{1,4}}|"   # 1::5:6:7:8         1:2:3::5:6:7:8   1:2:3::8
    fr"({IPv6_Octet}:){{1,2}}(:{IPv6_Octet}){{1,5}}|"   # 1::4:5:6:7:8       1:2::4:5:6:7:8   1:2::8
    fr"{IPv6_Octet}:((:{IPv6_Octet}){{1,6}})|"          # 1::3:4:5:6:7:8     1::3:4:5:6:7:8   1::8
    fr":((:{IPv6_Octet}){{1,7}}|:)|"                    # ::2:3:4:5:6:7:8    ::2:3:4:5:6:7:8  ::8       ::
    fr"fe80:(:{IPv6_Octet}){{0,4}}%[0-9a-zA-Z]{{1,}}|"  # fe80::7:8%eth0     fe80::7:8%1  (link-local IPv6 addresses with zone index)
    fr"::(ffff(:0{{1,4}}){{0,1}}:){{0,1}}{IPv4_Addr}|"  # ::255.255.255.255  ::ffff:255.255.255.255  ::ffff:0:255.255.255.255 (IPv4-mapped IPv6 addresses and IPv4-translated addresses)
    fr"({IPv6_Octet}:){{1,4}}:{IPv4_Addr}"              # 2001:db8:3:4::192.0.2.33  64:ff9b::192.0.2.33 (IPv4-Embedded IPv6 Address)
)
IPv6_Mask = r"(12[0-8]|1[01][0-9]|[0-9]?[0-9])"  # 1-128
IPv6_Net = fr"{IPv6_Addr}(\/{IPv6_Mask})?"
