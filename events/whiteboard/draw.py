from events.whiteboard.whiteboard_event import WhiteboardEvent


# TODO Sam

class DrawWhiteboardEvent(WhiteboardEvent):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.color = kwargs.get("color")
        self.tool = kwargs.get("tool")
        self.width = kwargs.get("width")

    def to_dict(self) -> dict:
        parent = super().to_dict()
        parent["color"] = self.color
        parent["tool"] = self.tool
        parent["width"] = self.width
        return parent
