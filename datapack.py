import s_taper
from s_taper.consts import *

scheme={
    "userId": INT+KEY,
    "nickname": TEXT,
    "hero" : TEXT,
    "hpbar" : INT,
    "dmg": INT,
    "exp": INT,
    "lvl": INT

}
bars=s_taper.Taper("datta","data.db").create_table(scheme)
heroes={
    "Pudge": (787,56),
    "Brewmaster": (699,64),
    "Pangolier": (732,63),
    "Mars": (832,53),
    "Anti-Mage" : (612,81)
}
saturation={
    "userId": INT+KEY,
    "food": TEXT

}
hpbars=s_taper.Taper("schedule","data.db").create_table(saturation)