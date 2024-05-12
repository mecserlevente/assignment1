from fastapi import APIRouter, HTTPException
from typing import List
from .models import Event
from .file_storage import EventFileManager

router = APIRouter()


@router.get("/events", response_model=List[Event])
async def get_all_events():
    events = EventFileManager.read_events_from_file()
    return events

@router.get("/events/filter", response_model=List[Event])
async def get_events_by_filter(date: str = None, organizer: str = None, status: str = None, event_type: str = None):
    events = EventFileManager.read_events_from_file()
    filtered_events = [
        event for event in events
        if (date is None or event['date'] == date) and
           (organizer is None or event['organizer', {}]['name'] == organizer) and
           (status is None or event['status'] == status) and
           (event_type is None or event['type'] == event_type)
    ]
    return filtered_events


@router.get("/events/{event_id}", response_model=Event)
async def get_event_by_id(event_id: int):
    events = EventFileManager.read_events_from_file()
    event = next((event for event in events if event.get('id') == event_id), None)
    if event is not None:
        return event
    else:
        raise HTTPException(status_code=404, detail="Event not found")


@router.post("/events", response_model=Event)
async def create_event(event: Event):
    pass


@router.put("/events/{event_id}", response_model=Event)
async def update_event(event_id: int, event: Event):
    pass


@router.delete("/events/{event_id}")
async def delete_event(event_id: int):
    pass


@router.get("/events/joiners/multiple-meetings")
async def get_joiners_multiple_meetings():
    pass
