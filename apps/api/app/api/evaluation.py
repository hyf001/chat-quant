"""
Agent Evaluation API endpoints
Provides functionality to generate execution traces for evaluation
"""
from fastapi import APIRouter, HTTPException, Depends, Query, BackgroundTasks
from fastapi.responses import StreamingResponse, RedirectResponse, FileResponse
from sqlalchemy.orm import Session
from sqlalchemy import func
from pydantic import BaseModel
from typing import Dict, Any, Optional, Literal, List
from datetime import datetime
from pathlib import Path
import uuid
import json
import re

from app.api.deps import get_db
from app.services.trace_generator import TraceGenerator
from app.services.cli.adapters.claude_agent_evaluation import ClaudeAgentEvaluation
from app.core.terminal_ui import ui
from app.core.config import PROJECT_ROOT, settings
from app.models.messages import Message
from app.models.projects import Project

router = APIRouter(prefix="/api/eval", tags=["evaluation"])

# Store evaluation results in memory
evaluation_results: Dict[str, Dict[str, Any]] = {}


class TraceGenerationRequest(BaseModel):
    """Request model for trace generation"""
    project_id: str
    format: Literal['markdown', 'json', 'both'] = 'both'
    max_output_length: int = 1000
    include_full_output: bool = False


class TraceGenerationResponse(BaseModel):
    """Response model for trace generation"""
    status: str
    message: str
    files: Dict[str, str]
    metadata: Dict[str, Any]


class EvaluationRequest(BaseModel):
    """Request model for evaluation"""
    project_id: str
    reference_answer: Optional[str] = None
    model: Optional[str] = "claude-sonnet-4-5-20250929"


class EvaluationResponse(BaseModel):
    """Response model for evaluation request"""
    status: str
    message: str
    evaluation_id: str


class EvaluationResult(BaseModel):
    """Response model for evaluation result"""
    evaluation_id: str
    status: str  # "pending", "running", "completed", "failed"
    progress: Optional[str] = None
    overall: Optional[int] = None
    correctness: Optional[int] = None
    efficiency: Optional[int] = None
    robustness: Optional[int] = None
    summary: Optional[str] = None
    details: Optional[List[Dict[str, Any]]] = None
    report: Optional[str] = None
    error: Optional[str] = None
    started_at: Optional[str] = None
    completed_at: Optional[str] = None


@router.post("/generate", response_model=TraceGenerationResponse)
async def generate_trace(
    request: TraceGenerationRequest,
    db: Session = Depends(get_db)
):
    """
    Generate execution trace files for a project.

    This endpoint generates comprehensive trace files in Markdown and/or JSON format
    from the messages stored in the database. These traces can be used for:
    - LLM-based evaluation (Markdown format)
    - Programmatic analysis (JSON format)
    - Human review and debugging

    Args:
        request: Trace generation request containing:
            - project_id: The project ID to generate traces for
            - format: Output format (markdown, json, or both)
            - max_output_length: Max length for tool outputs in Markdown
            - include_full_output: Whether to include full outputs in JSON

    Returns:
        Paths to generated trace files and metadata

    Example:
        ```
        POST /api/eval/generate
        {
            "project_id": "project-1761118631852-6uj5otf94",
            "format": "both"
        }
        ```
    """
    try:
        ui.info(f"Generating trace for project: {request.project_id}", "Trace Generation")

        # Check if project has messages
        message_count = db.query(func.count(Message.id)).filter(
            Message.project_id == request.project_id
        ).scalar()

        if message_count == 0:
            raise HTTPException(
                status_code=404,
                detail=f"No messages found for project {request.project_id}"
            )

        # Create output directory in project's data folder
        project_dir = Path(settings.projects_root) / request.project_id / "data" / "traces"
        project_dir.mkdir(parents=True, exist_ok=True)
        traces_dir = project_dir

        ui.info(f"Output directory: {traces_dir}", "Trace Generation")
        ui.info(f"Message count: {message_count}", "Trace Generation")

        # Generate traces using SQLAlchemy session
        generator = TraceGenerator(db)
        files = generator.generate_trace_files(
            project_id=request.project_id,
            output_dir=str(traces_dir),
            format=request.format
        )

        metadata = {
            'project_id': request.project_id,
            'message_count': message_count,
            'format': request.format,
            'generated_at': datetime.utcnow().isoformat(),
            'output_dir': str(traces_dir)
        }

        ui.success(f"Generated {len(files)} trace files", "Trace Generation")

        return TraceGenerationResponse(
            status="success",
            message=f"Successfully generated trace files for project {request.project_id}",
            files=files,
            metadata=metadata
        )

    except ValueError as e:
        ui.error(f"Invalid request: {e}", "Trace Generation")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        ui.error(f"Failed to generate trace: {e}", "Trace Generation")
        ui.error(f"Traceback: {error_details}", "Trace Generation")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate trace: {str(e)}"
        )


@router.get("/projects")
async def list_projects(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=100, description="Items per page"),
    db: Session = Depends(get_db)
):
    """
    Get list of all projects with their trace status.

    Args:
        page: Page number (starting from 1)
        page_size: Number of items per page (1-100)

    Returns:
        Paginated list of projects with metadata

    Example:
        GET /api/eval/projects?page=1&page_size=10
    """
    try:
        # Get total count of distinct projects
        total_count = db.query(func.count(func.distinct(Message.project_id))).filter(
            Message.project_id.isnot(None)
        ).scalar()

        # Calculate pagination
        offset = (page - 1) * page_size
        total_pages = (total_count + page_size - 1) // page_size

        # Get paginated project statistics using SQLAlchemy with LEFT JOIN on projects table
        project_stats = db.query(
            Message.project_id,
            func.count(Message.id).label('message_count'),
            func.min(Message.created_at).label('first_message'),
            func.max(Message.created_at).label('last_message'),
            Project.name.label('project_name'),
            Project.created_at.label('project_created_at')
        ).outerjoin(
            Project, Message.project_id == Project.id
        ).filter(
            Message.project_id.isnot(None)
        ).group_by(
            Message.project_id,
            Project.name,
            Project.created_at
        ).order_by(
            func.max(Message.created_at).desc()
        ).offset(offset).limit(page_size).all()

        projects = []
        for stat in project_stats:
            project_id = stat.project_id
            message_count = stat.message_count
            # Add 'Z' suffix to indicate UTC timezone for proper client-side conversion
            first_message = stat.first_message.isoformat() + 'Z' if stat.first_message else None
            last_message = stat.last_message.isoformat() + 'Z' if stat.last_message else None
            project_name = stat.project_name if stat.project_name else project_id  # Fallback to ID if name is None
            project_created_at = stat.project_created_at.isoformat() + 'Z' if stat.project_created_at else None

            # Check if trace files exist
            trace_dir = Path(settings.projects_root) / project_id / "data" / "traces"
            has_trace = (trace_dir / "trace.md").exists() or (trace_dir / "trace.json").exists()

            # Check if evaluation report exists
            has_evaluation = (trace_dir / "trace_evaluation.md").exists()

            projects.append({
                "project_id": project_id,
                "project_name": project_name,
                "project_created_at": project_created_at,
                "message_count": message_count,
                "first_message": first_message,
                "last_message": last_message,
                "has_trace": has_trace,
                "has_evaluation": has_evaluation
            })

        return {
            "projects": projects,
            "pagination": {
                "page": page,
                "page_size": page_size,
                "total": total_count,
                "total_pages": total_pages,
                "has_prev": page > 1,
                "has_next": page < total_pages
            }
        }

    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        ui.error(f"Failed to list projects: {e}", "List Projects")
        ui.error(f"Traceback: {error_details}", "List Projects")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to list projects: {str(e)}"
        )


@router.get("/dashboard")
async def get_dashboard(
    project_id: Optional[str] = Query(None, description="Project ID to generate traces for")
):
    """
    Dashboard endpoint - serves the evaluation HTML page directly.

    The evaluation page will handle trace generation asynchronously via AJAX.
    This endpoint serves the file directly instead of redirecting, ensuring compatibility
    with production environments where /static/ path may not be accessible via gateway.

    Args:
        project_id: Optional project ID to generate traces for (passed as URL parameter)

    Returns:
        HTML file response (evaluation.html)

    Example:
        GET /api/eval/dashboard?project_id=project-123
    """
    # Serve evaluation.html directly from PROJECT_ROOT/static/
    # This approach is similar to serve_static_file and doesn't rely on /static/ being accessible
    evaluation_html = PROJECT_ROOT / "static" / "evaluation.html"

    if not evaluation_html.exists():
        raise HTTPException(
            status_code=404,
            detail=f"Evaluation dashboard not found: {evaluation_html}"
        )

    if not evaluation_html.is_file():
        raise HTTPException(
            status_code=400,
            detail="Evaluation dashboard path is not a file"
        )

    # Return the HTML file directly
    # The project_id query parameter is preserved in the URL and will be read by JavaScript
    return FileResponse(
        path=evaluation_html,
        media_type="text/html",
        filename="evaluation.html",
        content_disposition_type="inline"
    )


@router.get("/{project_id}")
async def get_project_trace(
    project_id: str,
    format: Literal['markdown', 'json'] = Query('markdown', description="Trace format"),
    db: Session = Depends(get_db)
):
    """
    Get trace for a specific project.

    This is a convenience endpoint that generates the trace on-the-fly
    and returns it directly (instead of saving to files).

    Args:
        project_id: The project ID
        format: Output format (markdown or json)

    Returns:
        The trace content in the requested format

    Examples:
        - GET /api/eval/project-123?format=markdown
        - GET /api/eval/project-123?format=json
    """
    try:
        ui.info(f"Getting trace for project: {project_id}", "Get Trace")

        # Check if project has messages
        message_count = db.query(func.count(Message.id)).filter(
            Message.project_id == project_id
        ).scalar()

        if message_count == 0:
            raise HTTPException(
                status_code=404,
                detail=f"No messages found for project {project_id}"
            )

        ui.info(f"Generating trace for project: {project_id} ({message_count} messages)", "Get Trace")

        # Create generator with SQLAlchemy session
        generator = TraceGenerator(db)

        if format == 'markdown':
            content = generator.generate_markdown(project_id)
            return StreamingResponse(
                iter([content]),
                media_type="text/markdown",
                headers={
                    "Content-Disposition": f"inline; filename=trace_{project_id}.md"
                }
            )
        else:  # json
            content = generator.generate_json(project_id, include_full_output=True)
            return content

    except HTTPException:
        raise
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        ui.error(f"Failed to get trace: {e}", "Get Trace")
        ui.error(f"Traceback: {error_details}", "Get Trace")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get trace: {str(e)}"
        )


async def run_evaluation_task(
    evaluation_id: str,
    project_id: str,
    trace_file_path: str,
    model: str,
    reference_answer: Optional[str] = None
):
    """Background task to run evaluation"""
    try:
        ui.info(f"Starting evaluation {evaluation_id}", "Evaluation Task")
        ui.info(f"Project: {project_id}", "Evaluation Task")
        ui.info(f"Trace file: {trace_file_path}", "Evaluation Task")
        ui.info(f"Model: {model}", "Evaluation Task")
        if reference_answer:
            ui.info(f"Reference answer provided: {len(reference_answer)} chars", "Evaluation Task")

        # Update status to running
        evaluation_results[evaluation_id]["status"] = "running"
        evaluation_results[evaluation_id]["progress"] = "Initializing evaluation agent..."

        # Create evaluator
        evaluator = ClaudeAgentEvaluation(project_id="evaluation", model=model)
        ui.success("Evaluator created", "Evaluation Task")

        # Collect all messages
        evaluation_results[evaluation_id]["progress"] = "Running evaluation..."
        messages = []
        message_count = 0

        ui.info("Starting to receive messages...", "Evaluation Task")

        # Evaluate the trace file
        async for message in evaluator.evaluate_trace_with_streaming(
            trace_file_path=trace_file_path,
            project_id=project_id,
            session_id=evaluation_id,
            model=model,
            reference_answer=reference_answer,
        ):
            message_count += 1
            ui.debug(f"Received message #{message_count}: type={message.message_type}, role={message.role}", "Evaluation Task")

            # Collect chat messages for the report
            if message.message_type == "chat":
                messages.append(message.content)
                evaluation_results[evaluation_id]["progress"] = f"Generating report... ({len(messages)} messages received)"
                ui.info(f"Chat message #{len(messages)}: {message.content[:100]}...", "Evaluation Task")

            # Handle error messages
            elif message.message_type == "error":
                ui.error(f"Received error message: {message.content}", "Evaluation Task")
                raise Exception(message.content)

        ui.info(f"Total messages received: {message_count}", "Evaluation Task")
        ui.info(f"Chat messages collected: {len(messages)}", "Evaluation Task")

        # Check if we got any messages
        if len(messages) == 0:
            ui.warning("No chat messages received from evaluation!", "Evaluation Task")
            evaluation_results[evaluation_id]["status"] = "failed"
            evaluation_results[evaluation_id]["error"] = "No evaluation report generated - agent did not produce any output"
            evaluation_results[evaluation_id]["completed_at"] = datetime.utcnow().isoformat()
            return

        # Combine all messages into final report
        report = "\n\n".join(messages)
        ui.success(f"Report generated: {len(report)} characters", "Evaluation Task")

        # Parse evaluation scores from report
        scores = parse_evaluation_scores(report)
        ui.info(f"Parsed scores: {scores}", "Evaluation Task")

        # Update result
        evaluation_results[evaluation_id]["status"] = "completed"
        evaluation_results[evaluation_id]["report"] = report
        evaluation_results[evaluation_id]["overall"] = scores.get("overall")
        evaluation_results[evaluation_id]["correctness"] = scores.get("correctness")
        evaluation_results[evaluation_id]["efficiency"] = scores.get("efficiency")
        evaluation_results[evaluation_id]["robustness"] = scores.get("robustness")
        evaluation_results[evaluation_id]["summary"] = scores.get("summary")
        evaluation_results[evaluation_id]["details"] = scores.get("details")
        evaluation_results[evaluation_id]["completed_at"] = datetime.utcnow().isoformat()
        evaluation_results[evaluation_id]["progress"] = "Evaluation completed"

        ui.success(f"Evaluation {evaluation_id} completed successfully", "Evaluation Task")

    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        ui.error(f"Evaluation {evaluation_id} failed: {e}", "Evaluation Task")
        ui.error(f"Traceback: {error_details}", "Evaluation Task")
        evaluation_results[evaluation_id]["status"] = "failed"
        evaluation_results[evaluation_id]["error"] = f"{str(e)}\n\nTraceback:\n{error_details}"
        evaluation_results[evaluation_id]["completed_at"] = datetime.utcnow().isoformat()


def parse_evaluation_scores(report: str) -> Dict[str, Any]:
    """Parse evaluation scores from markdown report"""
    scores = {
        "overall": None,
        "correctness": None,
        "efficiency": None,
        "robustness": None,
        "summary": None,
        "details": []
    }

    try:
        # Try to find score patterns in the report
        # Look for patterns like "综合得分: 85" or "Correctness: 90/100"
        overall_match = re.search(r'综合得分[：:]\s*(\d+)', report)
        if overall_match:
            scores["overall"] = int(overall_match.group(1))

        correctness_match = re.search(r'正确性[：:]\s*(\d+)', report)
        if correctness_match:
            scores["correctness"] = int(correctness_match.group(1))

        efficiency_match = re.search(r'效率[：:]\s*(\d+)', report)
        if efficiency_match:
            scores["efficiency"] = int(efficiency_match.group(1))

        robustness_match = re.search(r'鲁棒性[：:]\s*(\d+)', report)
        if robustness_match:
            scores["robustness"] = int(robustness_match.group(1))

        # Extract summary section
        summary_match = re.search(r'##\s*总结.*?\n(.*?)(?=\n##|\Z)', report, re.DOTALL)
        if summary_match:
            scores["summary"] = summary_match.group(1).strip()

        ui.debug(f"Parsed scores: {scores}", "Parse Scores")

    except Exception as e:
        ui.warning(f"Failed to parse some scores: {e}", "Parse Scores")

    return scores


@router.post("/evaluate", response_model=EvaluationResponse)
async def evaluate_project(
    request: EvaluationRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Start evaluation of a project's trace file.

    This endpoint initiates the evaluation process as a background task and returns immediately.
    Use GET /api/eval/evaluate/{evaluation_id} to check the status and get results.

    Args:
        request: Evaluation request containing:
            - project_id: Project ID to evaluate
            - reference_answer: Optional reference answer for comparison
            - model: Model to use for evaluation

    Returns:
        Evaluation ID for tracking progress

    Example:
        ```
        POST /api/eval/evaluate
        {
            "project_id": "project-1761211615149-dpb91reso",
            "reference_answer": "The expected result..."
        }
        ```
    """
    try:
        # Check if trace file exists
        trace_dir = Path(settings.projects_root) / request.project_id / "data" / "traces"
        trace_file = trace_dir / "trace.json"

        if not trace_file.exists():
            raise HTTPException(
                status_code=404,
                detail=f"Trace file not found for project {request.project_id}. Please generate trace first."
            )

        # Generate evaluation ID
        evaluation_id = str(uuid.uuid4())

        # Initialize result storage
        evaluation_results[evaluation_id] = {
            "evaluation_id": evaluation_id,
            "status": "pending",
            "project_id": request.project_id,
            "trace_file": str(trace_file),
            "model": request.model,
            "started_at": datetime.utcnow().isoformat(),
            "progress": "Queued for evaluation",
        }

        ui.success(f"Evaluation {evaluation_id} queued for project: {request.project_id}", "Evaluation API")

        # Start background task
        background_tasks.add_task(
            run_evaluation_task,
            evaluation_id,
            request.project_id,
            str(trace_file),
            request.model or "claude-sonnet-4-5-20250929",
            request.reference_answer
        )

        return EvaluationResponse(
            status="started",
            message=f"Evaluation started. Use GET /api/eval/evaluate/{evaluation_id} to check progress.",
            evaluation_id=evaluation_id
        )

    except HTTPException:
        raise
    except Exception as e:
        ui.error(f"Failed to process evaluation request: {e}", "Evaluation API")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process evaluation request: {str(e)}"
        )


@router.get("/evaluate/{evaluation_id}", response_model=EvaluationResult)
async def get_evaluation_result(evaluation_id: str, db: Session = Depends(get_db)):
    """
    Get the result of an evaluation task.

    Args:
        evaluation_id: The evaluation ID returned from POST /api/eval/evaluate

    Returns:
        Current status and results (if completed)

    Example:
        GET /api/eval/evaluate/550e8400-e29b-41d4-a716-446655440000
    """
    if evaluation_id not in evaluation_results:
        raise HTTPException(status_code=404, detail="Evaluation not found")

    result = evaluation_results[evaluation_id]

    return EvaluationResult(
        evaluation_id=result["evaluation_id"],
        status=result["status"],
        progress=result.get("progress"),
        overall=result.get("overall"),
        correctness=result.get("correctness"),
        efficiency=result.get("efficiency"),
        robustness=result.get("robustness"),
        summary=result.get("summary"),
        details=result.get("details"),
        report=result.get("report"),
        error=result.get("error"),
        started_at=result.get("started_at"),
        completed_at=result.get("completed_at"),
    )


@router.get("/{project_id}/evaluation-report")
async def get_evaluation_report(
    project_id: str,
    db: Session = Depends(get_db)
):
    """
    Get the evaluation report for a specific project.

    Args:
        project_id: The project ID

    Returns:
        The evaluation report in Markdown format

    Examples:
        GET /api/eval/project-123/evaluation-report
    """
    try:
        ui.info(f"Getting evaluation report for project: {project_id}", "Get Report")

        # Check if evaluation report exists
        trace_dir = Path(settings.projects_root) / project_id / "data" / "traces"
        report_file = trace_dir / "trace_evaluation.md"

        if not report_file.exists():
            raise HTTPException(
                status_code=404,
                detail=f"Evaluation report not found for project {project_id}"
            )

        ui.info(f"Reading report from: {report_file}", "Get Report")

        # Read the report
        with open(report_file, 'r', encoding='utf-8') as f:
            report_content = f.read()

        return {
            "project_id": project_id,
            "report": report_content,
            "file_path": str(report_file)
        }

    except HTTPException:
        raise
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        ui.error(f"Failed to get evaluation report: {e}", "Get Report")
        ui.error(f"Traceback: {error_details}", "Get Report")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get evaluation report: {str(e)}"
        )

