from EventConstants import EventType, EventAction
from Event import Event
import DrawEvent


class CommentEvent(Event):

    image_id: str  # image event related to this comment
    text: str = ""  # text comment, if there is any
    draw: DrawEvent = None  # draw event, if there is any

    def __init__(self, action: EventAction):
        Event.__init__(self, EventType.COMMENT, action)

