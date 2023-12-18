def shoe_lace(vertices):
    area = 0
    for v, w in zip(vertices, vertices[1:]):
        area += v[0] * w[1] - v[1] * w[0]
    return abs(area / 2)
