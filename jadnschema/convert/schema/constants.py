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

# Escape Characters
# HTML: https://www.html.am/reference/html-special-characters.cfm
HTML_Escapes = {
    # HTML Reserved Characters
    '"': "&quot;",  # quotation mark
    "'": "&apos;",  # apostrophe
    "&": "&amp;",  # ampersand
    "<": "&lt;",  # less-than
    ">": "&gt;",  # greater-than
    # General HTML Symbols
    "??": "&OElig;",  # capital ligature OE
    "??": "&oelig;",  # small ligature oe
    "??": "&Scaron;",  # capital S with caron
    "??": "&scaron;",  # small S with caron
    "??": "&Yuml;",  # capital Y with diaeres
    "??": "&fnof;",  # f with hook
    "??": "&circ;",  # modifier letter circumflex accent
    "??": "&tilde;",  # small tilde
    "\u2002": "&ensp;",  # en space
    "\u2003": "&emsp;",  # em space
    "\u2009": "&thinsp;",  # thin space
    "\u200C": "&zwnj;",  # zero width non-joiner
    "\u200D": "&zwj;",  # zero width joiner
    "\u200E": "&lrm;",  # left-to-right mark
    "\u200F": "&rlm;",  # right-to-left mark
    "???": "&ndash;",  # en dash
    "???": "&mdash;",  # em dash
    "???": "&lsquo;",  # left single quotation mark
    "???": "&rsquo;",  # right single quotation mark
    "???": "&sbquo;",  # single low-9 quotation mark
    "???": "&ldquo;",  # left double quotation mark
    "???": "&rdquo;",  # right double quotation mark
    "???": "&bdquo;",  # double low-9 quotation mark
    "???": "&dagger;",  # dagger
    "???": "&Dagger;",  # double dagger
    "???": "&bull;",  # bullet
    "???": "&hellip;",  # horizontal ellipsis
    "???": "&permil;",  # per mille
    "???": "&prime;",  # minutes
    "???": "&Prime;",  # seconds
    "???": "&lsaquo;",  # single left angle quotation
    "???": "&rsaquo;",  # single right angle quotation
    "???": "&oline;",  # overline
    "???": "&euro;",  # euro
    "???": "&trade;",  # trademark
    "???": "&larr;",  # left arrow
    "???": "&uarr;",  # up arrow
    "???": "&rarr;",  # right arrow
    "???": "&darr;",  # down arrow
    "???": "&harr;",  # left right arrow
    "???": "&crarr;",  # carriage return arrow
    "???": "&lceil;",  # left ceiling
    "???": "&rceil;",  # right ceiling
    "???": "&lfloor;",  # left floor
    "???": "&rfloor;",  # right floor
    "???": "&loz;",  # lozenge
    "???": "&spades;",  # spade
    "???": "&clubs;",  # club
    "???": "&hearts;",  # heart
    "???": "&diams;",  # diamond
    # Mathematical Symbols
    "???": "&forall;",  # for all
    "???": "&part;",  # part
    "???": "&exist;",  # exists
    "???": "&empty;",  # empty
    "???": "&nabla;",  # nabla
    "???": "&isin;",  # isin
    "???": "&notin;",  # notin
    "???": "&ni;",  # ni
    "???": "&prod;",  # prod
    "???": "&sum;",  # sum
    "???": "&minus;",  # minus
    "???": "&lowast;",  # lowast
    "???": "&radic;",  # square root
    "???": "&prop;",  # proportional to
    "???": "&infin;",  # infinity
    "???": "&ang;",  # angle
    "???": "&and;",  # and
    "???": "&or;",  # or
    "???": "&cap;",  # cap
    "???": "&cup;",  # cup
    "???": "&int;",  # integral
    "???": "&there4;",  # therefore
    "???": "&sim;",  # similar to
    "???": "&cong;",  # congruent to
    "???": "&asymp;",  # almost equal
    "???": "&ne;",  # not equal
    "???": "&equiv;",  # equivalent
    "???": "&le;",  # less or equal
    "???": "&ge;",  # greater or equal
    "???": "&sub;",  # subset of
    "???": "&sup;",  # superset of
    "???": "&nsub;",  # not subset of
    "???": "&sube;",  # subset or equal
    "???": "&supe;",  # superset or equal
    "???": "&oplus;",  # circled plus
    "???": "&otimes;",  # circled times
    "???": "&perp;",  # perpendicular
    "???": "&sdot;",  # dot operator
    # Greek Characters
    "??": "&Alpha;",  # Alpha
    "??": "&Beta;",  # Beta
    "??": "&Gamma;",  # Gamma
    "??": "&Delta;",  # Delta
    "??": "&Epsilon;",  # Epsilon
    "??": "&Zeta;",  # Zeta
    "??": "&Eta;",  # Eta
    "??": "&Theta;",  # Theta
    "??": "&Iota;",  # Iota
    "??": "&Kappa;",  # Kappa
    "??": "&Lambda;",  # Lambda
    "??": "&Mu;",  # Mu
    "??": "&Nu;",  # Nu
    "??": "&Xi;",  # Xi
    "??": "&Omicron;",  # Omicron
    "??": "&Pi;",  # Pi
    "??": "&Rho;",  # Rho
    # TBD? 	undefined	 	Sigmaf
    "??": "&Sigma;",  # Sigma
    "??": "&Tau;",  # Tau
    "??": "&Upsilon;",  # Upsilon
    "??": "&Phi;",  # Phi
    "??": "&Chi;",  # Chi
    "??": "&Psi;",  # Psi
    "??": "&Omega;",  # Omega
    "??": "&alpha;",  # alpha
    "??": "&beta;",  # beta
    "??": "&gamma;",  # gamma
    "??": "&delta;",  # delta
    "??": "&epsilon;",  # epsilon
    "??": "&zeta;",  # zeta
    "??": "&eta;",  # eta
    "??": "&theta;",  # theta
    "??": "&iota;",  # iota
    "??": "&kappa;",  # kappa
    "??": "&lambda;",  # lambda
    "??": "&mu;",  # mu
    "??": "&nu;",  # nu
    "??": "&xi;",  # xi
    "??": "&omicron;",  # omicron
    "??": "&pi;",  # pi
    "??": "&rho;",  # rho
    "??": "&sigmaf;",  # sigmaf
    "??": "&sigma;",  # sigma
    "??": "&tau;",  # tau
    "??": "&upsilon;",  # upsilon
    "??": "&phi;",  # phi
    "??": "&chi;",  # chi
    "??": "&psi;",  # psi
    "??": "&omega;",  # omega
    "??": "&thetasym;",  # theta symbol
    "??": "&upsih;",  # upsilon symbol
    "??": "&piv;",  # pi symbol
    # ISO 8859-1 Characters
    "??": "&Agrave;",  # capital a, grave accent
    "??": "&Aacute;",  # capital a, acute accent
    "??": "&Acirc;",  # capital a, circumflex accent
    "??": "&Atilde;",  # capital a, tilde
    "??": "&Auml;",  # capital a, umlaut mark
    "??": "&Aring;",  # capital a, ring
    "??": "&AElig;",  # capital ae
    "??": "&Ccedil;",  # capital c, cedilla
    "??": "&Egrave;",  # capital e, grave accent
    "??": "&Eacute;",  # capital e, acute accent
    "??": "&Ecirc;",  # capital e, circumflex accent
    "??": "&Euml;",  # capital e, umlaut mark
    "??": "&Igrave;",  # capital i, grave accent
    "??": "&Iacute;",  # capital i, acute accent
    "??": "&Icirc;",  # capital i, circumflex accent
    "??": "&Iuml;",  # capital i, umlaut mark
    "??": "&ETH;",  # capital eth, Icelandic
    "??": "&Ntilde;",  # capital n, tilde
    "??": "&Ograve;",  # capital o, grave accent
    "??": "&Oacute;",  # capital o, acute accent
    "??": "&Ocirc;",  # capital o, circumflex accent
    "??": "&Otilde;",  # capital o, tilde
    "??": "&Ouml;",  # capital o, umlaut mark
    "??": "&Oslash;",  # capital o, slash
    "??": "&Ugrave;",  # capital u, grave accent
    "??": "&Uacute;",  # capital u, acute accent
    "??": "&Ucirc;",  # capital u, circumflex accent
    "??": "&Uuml;",  # capital u, umlaut mark
    "??": "&Yacute;",  # capital y, acute accent
    "??": "&THORN;",  # capital THORN, Icelandic
    "??": "&szlig;",  # small sharp s, German
    "??": "&agrave;",  # small a, grave accent
    "??": "&aacute;",  # small a, acute accent
    "??": "&acirc;",  # small a, circumflex accent
    "??": "&atilde;",  # small a, tilde
    "??": "&auml;",  # small a, umlaut mark
    "??": "&aring;",  # small a, ring
    "??": "&aelig;",  # small ae
    "??": "&ccedil;",  # small c, cedilla
    "??": "&egrave;",  # small e, grave accent
    "??": "&eacute;",  # small e, acute accent
    "??": "&ecirc;",  # small e, circumflex accent
    "??": "&euml;",  # small e, umlaut mark
    "??": "&igrave;",  # small i, grave accent
    "??": "&iacute;",  # small i, acute accent
    "??": "&icirc;",  # small i, circumflex accent
    "??": "&iuml;",  # small i, umlaut mark
    "??": "&eth;",  # small eth, Icelandic
    "??": "&ntilde;",  # small n, tilde
    "??": "&ograve;",  # small o, grave accent
    "??": "&oacute;",  # small o, acute accent
    "??": "&ocirc;",  # small o, circumflex accent
    "??": "&otilde;",  # small o, tilde
    "??": "&ouml;",  # small o, umlaut mark
    "??": "&oslash;",  # small o, slash
    "??": "&ugrave;",  # small u, grave accent
    "??": "&uacute;",  # small u, acute accent
    "??": "&ucirc;",  # small u, circumflex accent
    "??": "&uuml;",  # small u, umlaut mark
    "??": "&yacute;",  # small y, acute accent
    "??": "&thorn;",  # small thorn, Icelandic
    "??": "&yuml;",  # small y, umlaut mark
    # ISO 8859-1 Symbols
    "??": "&iexcl;",  # inverted exclamation mark
    "??": "&cent;",  # cent
    "??": "&pound;",  # pound
    "??": "&curren;",  # currency
    "??": "&yen;",  # yen
    "??": "&brvbar;",  # broken vertical bar
    "??": "&sect;",  # section
    "??": "&uml;",  # spacing diaeresis
    "??": "&copy;",  # copyright
    "??": "&ordf;",  # feminine ordinal indicator
    "??": "&laquo;",  # angle quotation mark (left)
    "??": "&not;",  # negation
    "??": "&shy;",  # soft hyphen
    "??": "&reg;",  # registered trademark
    "??": "&macr;",  # spacing macron
    "??": "&deg;",  # degree
    "??": "&plusmn;",  # plus-or-minus
    "??": "&sup2;",  # superscript 2
    "??": "&sup3;",  # superscript 3
    "??": "&acute;",  # spacing acute
    "??": "&micro;",  # micro
    "??": "&para;",  # paragraph
    "??": "&middot;",  # middle dot
    "??": "&cedil;",  # spacing cedilla
    "??": "&sup1;",  # superscript 1
    "??": "&ordm;",  # masculine ordinal indicator
    "??": "&raquo;",  # angle quotation mark (right)
    "??": "&frac14;",  # fraction 1/4
    "??": "&frac12;",  # fraction 1/2
    "??": "&frac34;",  # fraction 3/4
    "??": "&iquest;",  # inverted question mark
    "??": "&times;",  # multiplication
    "??": "&divide;"  # division
}
