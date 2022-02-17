from EventConstants import EventType, EventAction
from Event import Event


class DrawEvent(Event):

    def __init__(self):
        Event.__init__(self, EventType.UNDO, EventAction.NONE)

