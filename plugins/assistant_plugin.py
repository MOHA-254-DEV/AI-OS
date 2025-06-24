from agents.assistant_agent import AssistantAgent
from utils.logger import log_task

agent = AssistantAgent()

async def reply_email(args):
    if len(args) < 2:
        return {"error": "Usage: reply_email <subject> <message>"}
    subject = args[0]
    content = " ".join(args[1:])
    result = agent.reply_email(subject, content)
    log_task("reply_email", "success", result)
    return {"reply": result}

async def schedule_meeting(args):
    if len(args) < 3:
        return {"error": "Usage: schedule_meeting <title> <YYYY-MM-DD> <HH:MM>"}
    result = agent.schedule_meeting(args[0], args[1], args[2])
    log_task("schedule_meeting", "success" if "error" not in result else "fail", str(result))
    return result

async def edit_doc(args):
    if len(args) < 2:
        return {"error": "Usage: edit_doc <instruction> <document_text>"}
    instruction = args[0]
    text = " ".join(args[1:])
    result = agent.edit_document(text, instruction)
    log_task("edit_doc", "success", result)
    return {"output": result}

async def list_tasks(args):
    tasks = agent.get_task_list()
    formatted = [{"id": t[0], "title": t[1], "time": t[2], "status": t[3]} for t in tasks]
    log_task("list_tasks", "success", f"{len(formatted)} tasks loaded")
    return {"tasks": formatted}

def register():
    return {
        "reply_email": reply_email,
        "schedule_meeting": schedule_meeting,
        "edit_doc": edit_doc,
        "list_tasks": list_tasks
    }
from agents.assistant_agent import AssistantAgent

agent = AssistantAgent()

async def add_note(args):
    content = " ".join(args)
    return agent.add_note(content)

async def list_notes(args):
    return agent.list_notes()

async def delete_note(args):
    if not args:
        return {"error": "Usage: delete_note <id>"}
    return agent.delete_note(args[0])

async def add_reminder(args):
    if len(args) < 2:
        return {"error": "Usage: add_reminder <task> <minutes_from_now>"}
    task = " ".join(args[:-1])
    try:
        minutes = int(args[-1])
    except:
        return {"error": "Last argument must be an integer (minutes)"}
    return agent.add_reminder(task, minutes)

async def list_reminders(args):
    return agent.list_reminders()

async def delete_reminder(args):
    return agent.delete_reminder(args[0]) if args else {"error": "Missing reminder ID"}

async def add_event(args):
    if len(args) < 2:
        return {"error": "Usage: add_event <title> <YYYY-MM-DDTHH:MM>"}
    title = " ".join(args[:-1])
    time = args[-1]
    return agent.add_event(title, time)

async def list_events(args):
    return agent.list_events()

async def delete_event(args):
    return agent.delete_event(args[0]) if args else {"error": "Missing event ID"}

def register():
    return {
        "add_note": add_note,
        "list_notes": list_notes,
        "delete_note": delete_note,
        "add_reminder": add_reminder,
        "list_reminders": list_reminders,
        "delete_reminder": delete_reminder,
        "add_event": add_event,
        "list_events": list_events,
        "delete_event": delete_event
    }
