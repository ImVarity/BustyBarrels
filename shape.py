class Shape:
    def __init__(self, center, vertices) -> None:
        self.center = center
        self.vertices = vertices
        # vertices made with own origin
        # self.vertices = [[self.center[0] - width / 2, self.center[1] - height / 2],
        #                  [self.center[0] + width / 2, self.center[1] - height / 2],
        #                  [self.center[0] + width / 2, self.center[1] + height / 2],
        #                  [self.center[0] - width / 2, self.center[1] + height / 2]]
    
