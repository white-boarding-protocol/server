from EventConstants import EventType, EventAction
from Event import Event


class ImageEvent(Event):

    text: str

    def __init__(self, action: EventAction):
        Event.__init__(self, EventType.IMAGE, action)

