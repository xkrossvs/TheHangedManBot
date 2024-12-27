from config import hangs

STAGES = []
for i in hangs.find().sort('hang_number', -1):
    STAGES.append(i['hang_id'])