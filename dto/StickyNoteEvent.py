from EventConstants import EventType, EventAction
from Event import Event


class StickyNoteEvent(Event):

    text: str

    def __init__(self, action: EventAction):
        Event.__init__(self, EventType.STICKY_NOTE, action)

