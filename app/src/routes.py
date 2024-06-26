from fastapi import APIRouter, HTTPException
from typing import List
from .models import Event
from .file_storage import EventFileManager
from .EventAnalyzer import EventAnalyzer

router = APIRouter()

@router.get("/events", response_model=List[Event])
async def get_all_events():
    events = EventFileManager.read_events_from_file()
    return events

@router.get("/events/filter", response_model=List[Event])
async def get_events_by_filter(date: str = None, organizer: str = None, status: str = None, event_type: str = None):
    events = EventFileManager.read_events_from_file()
    filtered_events = [
        e for e in events
        if (date is None or e['date'] == date) and
           (organizer is None or e['organizer', {}]['name'] == organizer) and
           (status is None or e['status'] == status) and
           (event_type is None or e['type'] == event_type)
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
    events = EventFileManager.read_events_from_file()
    already_exist_id = False
    for e in events:
        if e['id'] == event.id:
            already_exist_id = True
            break
    if already_exist_id:
        raise HTTPException(status_code=400, detail="Event with this id already exists")
    else:
        events.append(event.dict())
        EventFileManager.write_events_to_file(events)
        return event

@router.put("/events/{event_id}", response_model=Event)
async def update_event(event_id: int, event_update: Event):
    events = EventFileManager.read_events_from_file()
    found_index = False
    index = 0
    
    for e in events:
        if e.get('id') == event_id:
            found_index = True
            events[index] = event_update.dict()
            break
        index += 1

    if not found_index:
        raise HTTPException(status_code=404, detail="Event not found")

    EventFileManager.write_events_to_file(events)

    if found_index:
        return events[index]
    else:
        raise HTTPException(status_code=404, detail="Event not found")


@router.delete("/events/{event_id}")
async def delete_event(event_id: int):
    events = EventFileManager.read_events_from_file()
    found_index = False

    for e in events:
        if e.get('id') == event_id:
            events.remove(e)
            found_index = True
            break

    if not found_index:
        raise HTTPException(status_code=404, detail="Event not found")

    EventFileManager.write_events_to_file(events)
    return {"message": "Event deleted successfully"}


@router.get("/events/joiners/multiple-meetings")
async def get_joiners_multiple_meetings():
    events = EventFileManager.read_events_from_file()
    joiners = EventAnalyzer.get_joiners_multiple_meetings_method(events)
    
    if not joiners:
        return {"message": "No joiners attending at least 2 meetings"}
    
    return {"joiners": joiners}
