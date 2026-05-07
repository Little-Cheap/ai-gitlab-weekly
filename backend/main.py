import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, timedelta

from gitlab_api import get_user_commits, format_commits_for_report
from kimi_api import generate_weekly_report

app = FastAPI(title="AI GitLab 周报助手")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

frontend_path = os.path.join(os.path.dirname(__file__), "..", "frontend")
if os.path.exists(frontend_path):
    app.mount("/static", StaticFiles(directory=frontend_path), name="static")


class ReportRequest(BaseModel):
    gitlab_url: str
    gitlab_token: str
    project_ids: List[str]
    author_email: Optional[str] = ""
    start_date: str
    end_date: str
    kimi_api_key: str
    kimi_api_url: Optional[str] = ""


class ReportResponse(BaseModel):
    success: bool
    report: str
    commits_count: int
    message: str


@app.get("/")
async def root():
    frontend_file = os.path.join(frontend_path, "index.html")
    if os.path.exists(frontend_file):
        return FileResponse(frontend_file)
    return {"message": "AI GitLab 周报助手 API 正在运行"}


@app.post("/api/generate-report", response_model=ReportResponse)
async def generate_report(request: ReportRequest):
    import config
    
    config.GITLAB_URL = request.gitlab_url
    config.GITLAB_TOKEN = request.gitlab_token
    config.KIMI_API_KEY = request.kimi_api_key
    if request.kimi_api_url:
        config.KIMI_API_URL = request.kimi_api_url
    
    try:
        commits = await get_user_commits(
            project_ids=request.project_ids,
            author_email=request.author_email,
            since=request.start_date,
            until=request.end_date
        )
        
        if not commits:
            return ReportResponse(
                success=False,
                report="",
                commits_count=0,
                message="指定时间范围内没有找到提交记录"
            )
        
        commits_text = format_commits_for_report(commits)
        
        report = await generate_weekly_report(
            commits_text=commits_text,
            start_date=request.start_date,
            end_date=request.end_date
        )
        
        return ReportResponse(
            success=True,
            report=report,
            commits_count=len(commits),
            message="周报生成成功"
        )
        
    except Exception as e:
        return ReportResponse(
            success=False,
            report="",
            commits_count=0,
            message=f"生成周报失败：{str(e)}"
        )


@app.get("/api/health")
async def health_check():
    return {"status": "ok", "timestamp": datetime.now().isoformat()}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
