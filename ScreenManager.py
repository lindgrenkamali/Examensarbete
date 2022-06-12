class ScreenManager:

    def __init__(self, screenWidth, screenHeight):
        self.Multiplier = screenWidth/1920

    def GetSize(self, pixels):
        AdjustedSize = pixels * self.Multiplier
        return int(AdjustedSize)
