# Pitcher class
# Represents a pitcher in game, holds a pitcher's stats

class Pitcher:
    def __init__(self, name="", ip="", h="", r="", er="", bb="", so="", p="", s="", era="", id=""):
        self.name = name
        self.ip = ip
        self.h = h
        self.r = r
        self.er = er
        self.bb = bb
        self.so = so
        self.p = p
        self.s = s
        self.era = era
        self.id = id

    def __str__(self):
        s = " "
        ps = ""
        if self.id != "":
            s = "[" + str(self.name) + "](http://mlb.mlb.com/team/player.jsp?player_id=" + str(self.id) + ")"
            ps = str(self.p) + "-" + str(self.s)
        else:
            s = "|"
        s = "|".join((s, str(self.ip), str(self.h), str(self.r), str(self.er), str(self.bb), str(self.so), str(ps), str(self.era)))
        # s = s + "|" + str(self.ip) + "|" + str(self.h) + "|" + str(self.r) + "|" + str(self.er) + "|" + str(self.bb) + "|" + str(self.so) + "|" + ps + "|" + str(self.era)
        return s


# Batter class
# Represents a batter in game, holds a batter's stats

class Batter:
    def __init__(self="", name="", pos="", ab="", r="", h="", rbi="", bb="", so="", ba="", obp="", ops="", id=""):
        self.name = name
        self.pos = pos
        self.ab = ab
        self.r = r
        self.h = h
        self.rbi = rbi
        self.bb = bb
        self.so = so
        self.ba = ba
        self.obp = obp
        self.ops = ops
        self.id = id

    def __str__(self):
        if self.name == "":
            return "|" * 9
        s = ""
        if self.id != "":
            s = "[" + str(self.name) + "](http://mlb.mlb.com/team/player.jsp?player_id=" + str(self.id) + ")|"
        else:
            s = self.name + "|"
        s += "|".join( str(stat) for stat in (self.pos, self.ab, self.r, self.h, self.rbi, self.bb, self.so) )
        s += "|" + "/".join( str(stat) for stat in (self.ba, self.obp, self.ops) )
        return s
