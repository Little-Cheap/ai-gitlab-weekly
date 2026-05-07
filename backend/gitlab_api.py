import httpx
from datetime import datetime
from typing import List, Dict, Optional
import config


async def get_user_commits(
    project_ids: List[str],
    author_email: str,
    since: str,
    until: str
) -> List[Dict]:
    all_commits = []
    errors = []
    
    gitlab_url = config.GITLAB_URL.rstrip('/')
    token = config.GITLAB_TOKEN.strip() if config.GITLAB_TOKEN else ""
    
    print(f"[DEBUG] GitLab URL: {gitlab_url}")
    print(f"[DEBUG] Token (前6位): {token[:6] if len(token) >= 6 else token}...")
    print(f"[DEBUG] Token 长度: {len(token)}")
    
    headers = {"PRIVATE-TOKEN": token}
    
    async with httpx.AsyncClient(timeout=httpx.Timeout(30.0)) as client:
        for project_id in project_ids:
            try:
                url = f"{gitlab_url}/api/v4/projects/{project_id}/repository/commits"
                params = {
                    "since": since,
                    "until": until,
                    "with_stats": "true"
                }
                
                if author_email:
                    params["author"] = author_email
                
                response = await client.get(url, headers=headers, params=params)
                response.raise_for_status()
                
                commits = response.json()
                
                for commit in commits:
                    commit["project_id"] = project_id
                    all_commits.append(commit)
                    
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 401:
                    errors.append(f"项目 {project_id}: 认证失败，请检查 Access Token 是否正确")
                elif e.response.status_code == 403:
                    errors.append(f"项目 {project_id}: 权限不足，请确保 Token 有访问该项目的权限")
                elif e.response.status_code == 404:
                    errors.append(f"项目 {project_id}: 项目不存在或无权访问")
                else:
                    errors.append(f"项目 {project_id}: HTTP {e.response.status_code} 错误")
            except httpx.HTTPError as e:
                errors.append(f"项目 {project_id}: 网络错误 - {str(e)}")
    
    if errors and not all_commits:
        raise Exception("\n".join(errors))
    
    all_commits.sort(key=lambda x: x["created_at"], reverse=True)
    
    return all_commits


async def get_project_info(project_id: str) -> Optional[Dict]:
    gitlab_url = config.GITLAB_URL.rstrip('/')
    headers = {"PRIVATE-TOKEN": config.GITLAB_TOKEN}
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            url = f"{gitlab_url}/api/v4/projects/{project_id}"
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            print(f"Error fetching project info: {e}")
            return None


def format_commits_for_report(commits: List[Dict]) -> str:
    if not commits:
        return "本周没有提交记录"
    
    project_commits = {}
    
    for commit in commits:
        project_id = commit.get("project_id", "unknown")
        if project_id not in project_commits:
            project_commits[project_id] = []
        project_commits[project_id].append(commit)
    
    formatted_text = ""
    for project_id, project_commit_list in project_commits.items():
        formatted_text += f"\n项目ID: {project_id}\n"
        formatted_text += "-" * 40 + "\n"
        
        for commit in project_commit_list:
            date = commit["created_at"][:10]
            message = commit["message"].strip()
            short_id = commit["short_id"]
            formatted_text += f"[{date}] {message} ({short_id})\n"
    
    return formatted_text
