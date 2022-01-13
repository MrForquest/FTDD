class Line:
    def __init__(self, p1, p2):
        self.p1 = (round(p1[0]), round(p1[1]))
        self.p2 = (round(p2[0]), round(p2[1]))
        self.a = (p1[1] - p2[1])
        self.b = (p2[0] - p1[0])
        self.c = -(p1[0] * p2[1] - p2[0] * p1[1])

    def intersection(self, other):
        a1, b1, c1 = self.a, self.b, self.c
        a2, b2, c2 = other.a, other.b, other.c
        d = a1 * b2 - a2 * b1
        dx = c1 * b2 - c2 * b1
        dy = a1 * c2 - a2 * c1
        if d != 0:
            x = round(dx / d)
            y = round(dy / d)
            rx1 = range(min(self.p1[0], self.p2[0]), max(self.p1[0], self.p2[0]))
            rx2 = range(min(other.p1[0], other.p2[0]), max(other.p1[0], other.p2[0]))
            ry1 = range(min(self.p1[1], self.p2[1]), max(self.p1[1], self.p2[1]))
            ry2 = range(min(other.p1[1], other.p2[1]), max(other.p1[1], other.p2[1]))
            if (x in rx1) and (x in rx2) and (y in ry1) and (y in ry2):
                return x, y
        return False
