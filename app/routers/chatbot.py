from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Dict, Any
import json

from app.core.logger import module_logger
from app.db import SessionLocal
from app.core.redis_client import redis_service
from app.llm.open_ai_llm_client import llm_client
from app.services.cv_query_services.mysq_cv_query import cv_query_service
from fastapi.responses import JSONResponse

router = APIRouter()


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


@router.post("/chatbot", response_model=ChatResponse)
async def chatbot_endpoint(msg: ChatMessage, db: Session = Depends(get_db)) -> Dict[str, Any]:
    """
    Chatbot endpoint that:
    - Calls the LLM to analyze user intent
    - Finds candidates from the DB based on intent
    - Maintains conversation context in Redis
    """

    if not msg.user_message.strip():
        module_logger.warning("Invalid request: session_id or user_message missing.")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="user message are required."
        )

    try:
        context = await redis_service.get(msg.session_id)
    except Exception as e:
        module_logger.error(f"Redis error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving conversation history. Please try again."
        )

    context["history"].append({"role": "user", "content": msg.user_message})

    try:
        llm_response = llm_client.analyze_user_query(msg.user_message)
        parsed_response = json.loads(json.dumps(llm_response))
    except json.JSONDecodeError:
        module_logger.error("Invalid JSON response from LLM")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Invalid response from AI model. Please try again."
        )
    except Exception as e:
        module_logger.error(f"LLM API error: {e}")
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Error processing your request with AI. Please try again later."
        )

    intent = parsed_response.get("intent", "unknown")
    params = parsed_response.get("parameters", {})

    try:
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
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Sorry, I couldn't understand your request."
            )

    except Exception as e:
        module_logger.error(f"Database query error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while fetching results. Please try again later."
        )

    context["history"].append({"role": "assistant", "content": answer})

    try:
        await redis_service.set(msg.session_id, context)
    except Exception as e:
        module_logger.warning(f"Failed to save context in Redis: {e}")
        return{
            "response": answer,
            "context": {
                "session_id": msg.session_id,
                "history_length": len(context["history"]),
            },
        }
    return {
        "response": answer,
        "context": {
            "session_id": msg.session_id,
            "history_length": len(context["history"]),
        },
    }
