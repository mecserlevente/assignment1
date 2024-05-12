from .models import Event

class EventAnalyzer:
    @staticmethod
    def get_joiners_multiple_meetings_method(events: Event):
        meetings = {}
        for e in events:
            for joiner in e.get('joiners', []):
                joiner_email = joiner.get('name')
                if joiner_email:
                    if joiner_email in meetings:
                        meetings[joiner_email] += 1
                    else:
                        meetings[joiner_email] = 1

        return [lambda joiner: joiner for joiner, count in meetings.items() if count > 1]