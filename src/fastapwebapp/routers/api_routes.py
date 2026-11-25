# routers/api_routes.py
from fastapi import APIRouter

# Alphabetized sub-router absolute import mappings for clean scannability
from fastapwebapp.api.gttsagent import router_gttsagent
from fastapwebapp.api.gttsanalyzer import router_gttsanalyzer
from fastapwebapp.api.gttsprocess import router_gttsprocess
from fastapwebapp.api.gttsword import router_gttsword
from fastapwebapp.api.magiclens import router_magiclens
from fastapwebapp.api.textipyimage import router_textipyimage
from fastapwebapp.api.paragraph import router_paragraph
from fastapwebapp.api.sentence import router_sentence
from fastapwebapp.api.slideshow import router_slideshow
from fastapwebapp.api.chatbot import router_chatbot

api_router = APIRouter()

# Register sub-routers cleanly to aggregate routing chains under /api prefix
api_router.include_router(router_gttsprocess)
api_router.include_router(router_gttsagent)
api_router.include_router(router_gttsanalyzer)
api_router.include_router(router_gttsword)
api_router.include_router(router_sentence)
api_router.include_router(router_slideshow)
api_router.include_router(router_magiclens)
api_router.include_router(router_textipyimage)
api_router.include_router(router_paragraph)	 
api_router.include_router(router_chatbot)