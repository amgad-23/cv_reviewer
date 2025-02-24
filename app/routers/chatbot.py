from app.core.redis_client import redis_service
from app.services.chatbot_service import chatbot_query
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from app.db import SessionLocal
from app.services.cv_query_services.mysq_cv_query import cv_query_service
from app.services.parse_user_intent import parse_user_intent

router = APIRouter()
conversation_history: List[Dict[str, str]] = [
    {"role": "system", "content": "You are a helpful assistant specializing in CV analysis."}
]


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class ChatMessage(BaseModel):
    session_id: str
    user_message: str


class ChatResponse(BaseModel):
    response: str
    context: Dict[str, Any]


@router.post("/chatbot")
def chatbot_endpoint(msg: ChatMessage, db: Session = Depends(get_db)) -> Dict[str, Any]:
    context = redis_service.get(msg.session_id)
    context["history"].append({"role": "user", "content": msg.user_message})
    intent, params = parse_user_intent(msg.user_message)

    if intent == "find_skill":
        skill = params.get("skill", "")
        result = cv_query_service.find_candidates_with_skill(db, skill)
        context["last_result"] = result
        answer = f"Found {len(result)} candidates with skill '{skill}'."

    elif intent == "search_industry":
        industry = params.get("industry", "")
        result = cv_query_service.search_experience_in_industry(db, industry)
        context["last_result"] = result
        answer = f"Found {len(result)} candidates in industry '{industry}'."

    elif intent == "compare_education":
        candidate_ids = params.get("candidate_ids") or []
        if not candidate_ids and context["last_result"]:
            candidate_ids = [c.id for c in context["last_result"]]
        result = cv_query_service.compare_education_levels(db, candidate_ids)
        context["last_result"] = result
        answer = f"Compared education for {len(result)} candidates."

    elif intent == "job_requirements":
        requirements = params.get("requirements", {})
        result = cv_query_service.match_candidates_for_job_requirements(db, requirements)
        context["last_result"] = result
        answer = f"Found {len(result)} candidates matching job requirements."

    else:
        answer = "I'm not sure how to handle that request."

    context["history"].append({"role": "assistant", "content": answer})
    redis_service.set(msg.session_id, context)

    return {
        "response": answer,
        "context": {
            "session_id": msg.session_id,
            "history_length": len(context["history"])
        }
    }


@router.post("/base-chatbot")
def chatbot_endpoint(user_message: str):
    answer = chatbot_query(user_message, conversation_history)
    return {"response": answer}
