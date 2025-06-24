# assistant/assistant_agent.py

import os
import uuid
import json
import sqlite3
import datetime
from datetime import timedelta
from utils.logger import logger, log_task


class AssistantAgent:
    def __init__(self, db_path="data/tasks.db", base_path="data/assistant"):
        os.makedirs("data", exist_ok=True)
        os.makedirs(base_path, exist_ok=True)

        self.db_path = db_path
        self.notes_file = f"{base_path}/notes.json"
        self.reminders_file = f"{base_path}/reminders.json"
        self.calendar_file = f"{base_path}/calendar.json"

        self._init_db()

    # ----------------- Database Setup -----------------
    def _init_db(self):
        try:
            with sqlite3.connect(self.db_path) as conn:
                cur = conn.cursor()
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS tasks (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT,
                        details TEXT,
                        time TEXT,
                        status TEXT DEFAULT 'pending'
                    )
                """)
                conn.commit()
            logger.info("[DB] Task table initialized")
        except Exception as e:
            logger.error(f"[DB] Failed to initialize database: {e}")

    # ----------------- Email & Tasks -----------------
    def reply_email(self, subject: str, content: str) -> str:
        logger.info("[Agent] Email reply generated.")
        return f"Thanks for reaching out about '{subject}'. Regarding your message: {content[:80]}... — I’ll get back shortly."

    def schedule_meeting(self, title: str, date: str, time_str: str) -> dict:
        try:
            full_time = f"{date} {time_str}"
            datetime.datetime.strptime(full_time, "%Y-%m-%d %H:%M")
            with sqlite3.connect(self.db_path) as conn:
                cur = conn.cursor()
                cur.execute("INSERT INTO tasks (title, details, time) VALUES (?, ?, ?)",
                            (title, "Meeting scheduled", full_time))
                conn.commit()
            logger.info(f"[Agent] Meeting '{title}' scheduled for {full_time}")
            return {"status": "scheduled", "title": title, "time": full_time}
        except ValueError:
            logger.error("[Agent] Invalid datetime format.")
            return {"error": "Invalid format. Use YYYY-MM-DD HH:MM"}
        except Exception as e:
            logger.error(f"[Agent] Error scheduling meeting: {e}")
            return {"error": "Internal error while scheduling meeting."}

    def get_task_list(self):
        try:
            with sqlite3.connect(self.db_path) as conn:
                cur = conn.cursor()
                cur.execute("SELECT id, title, time, status FROM tasks")
                return cur.fetchall()
        except Exception as e:
            logger.error(f"[Agent] Failed to fetch tasks: {e}")
            return []

    def edit_document(self, text: str, instruction: str) -> str:
        instruction = instruction.lower()
        try:
            if "summarize" in instruction:
                sentences = text.split(".")
                summary = ". ".join(sentences[:2]) + "." if len(sentences) > 1 else text
                logger.info("[Agent] Document summarized.")
                return summary

            elif "fix grammar" in instruction:
                corrected = text.replace(" u ", " you ").replace(" r ", " are ")
                logger.info("[Agent] Grammar corrected.")
                return corrected

            elif "uppercase" in instruction:
                logger.info("[Agent] Text converted to uppercase.")
                return text.upper()

            elif "lowercase" in instruction:
                logger.info("[Agent] Text converted to lowercase.")
                return text.lower()

            logger.warning("[Agent] Unknown instruction.")
            return "Instruction not recognized."
        except Exception as e:
            logger.error(f"[Agent] Failed to edit document: {e}")
            return "Error processing instruction."

    # ----------------- Notes -----------------
    def add_note(self, content):
        if not content.strip():
            return {"error": "Note content cannot be empty."}

        note = {
            "id": str(uuid.uuid4()),
            "content": content,
            "timestamp": datetime.datetime.now().isoformat()
        }
        notes = self._load_file(self.notes_file)
        notes.append(note)
        self._save_file(self.notes_file, notes)
        log_task("assistant_note", "add", content)
        return note

    def list_notes(self):
        return self._load_file(self.notes_file)

    def delete_note(self, note_id):
        notes = self._load_file(self.notes_file)
        notes = [n for n in notes if n['id'] != note_id]
        self._save_file(self.notes_file, notes)
        logger.info(f"[Agent] Note {note_id} deleted.")
        return {"status": "deleted", "id": note_id}

    # ----------------- Reminders -----------------
    def add_reminder(self, task, time_offset_minutes=60):
        try:
            reminder_time = datetime.datetime.now() + timedelta(minutes=time_offset_minutes)
            reminder = {
                "id": str(uuid.uuid4()),
                "task": task,
                "remind_at": reminder_time.isoformat()
            }
            reminders = self._load_file(self.reminders_file)
            reminders.append(reminder)
            self._save_file(self.reminders_file, reminders)
            log_task("assistant_reminder", "add", task)
            logger.info(f"[Agent] Reminder added for task: {task}")
            return reminder
        except Exception as e:
            logger.error(f"[Agent] Failed to add reminder: {e}")
            return {"error": "Could not add reminder."}

    def list_reminders(self):
        return self._load_file(self.reminders_file)

    def delete_reminder(self, reminder_id):
        reminders = self._load_file(self.reminders_file)
        reminders = [r for r in reminders if r['id'] != reminder_id]
        self._save_file(self.reminders_file, reminders)
        logger.info(f"[Agent] Reminder {reminder_id} deleted.")
        return {"status": "deleted", "id": reminder_id}

    # ----------------- Calendar -----------------
    def add_event(self, title, date_time):
        try:
            datetime.datetime.fromisoformat(date_time)
            event = {
                "id": str(uuid.uuid4()),
                "title": title,
                "time": date_time
            }
            calendar = self._load_file(self.calendar_file)
            calendar.append(event)
            self._save_file(self.calendar_file, calendar)
            log_task("assistant_calendar", "event", title)
            logger.info(f"[Agent] Event '{title}' added at {date_time}")
            return event
        except ValueError:
            logger.error(f"[Agent] Invalid ISO format for event: {date_time}")
            return {"error": "Invalid datetime format. Use ISO format YYYY-MM-DDTHH:MM:SS"}
        except Exception as e:
            logger.error(f"[Agent] Failed to add event: {e}")
            return {"error": "Could not add event."}

    def list_events(self):
        return self._load_file(self.calendar_file)

    def delete_event(self, event_id):
        calendar = self._load_file(self.calendar_file)
        calendar = [e for e in calendar if e['id'] != event_id]
        self._save_file(self.calendar_file, calendar)
        logger.info(f"[Agent] Event {event_id} deleted.")
        return {"status": "deleted", "id": event_id}

    # ----------------- File Helpers -----------------
    def _load_file(self, path):
        if not os.path.exists(path):
            logger.warning(f"[File] {path} not found. Creating new file.")
            return []
        try:
            with open(path, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            logger.error(f"[File] Corrupt JSON in {path}. Resetting file.")
            return []
        except Exception as e:
            logger.error(f"[File] Failed to load {path}: {e}")
            return []

    def _save_file(self, path, data):
        try:
            with open(path, "w") as f:
                json.dump(data, f, indent=4)
            logger.info(f"[File] Saved file: {path}")
        except Exception as e:
            logger.error(f"[File] Failed to save {path}: {e}")
