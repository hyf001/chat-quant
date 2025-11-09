from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
from pydantic import BaseModel
from sqlalchemy.orm import Session
import os
import base64
import uuid
from app.api.deps import get_db
from app.core.config import settings
from app.models.projects import Project as ProjectModel
from app.services.assets import write_bytes

router = APIRouter(prefix="/api/assets", tags=["assets"]) 


class LogoRequest(BaseModel):
    b64_png: str  # Accept base64-encoded PNG (fallback if no OpenAI key)


@router.post("/{project_id}/logo")
async def upload_logo(project_id: str, body: LogoRequest, db: Session = Depends(get_db)):
    row = db.get(ProjectModel, project_id)
    if not row:
        raise HTTPException(status_code=404, detail="Project not found")
    project_assets = os.path.join(settings.projects_root, project_id, "assets")
    data = base64.b64decode(body.b64_png)
    logo_path = os.path.join(project_assets, "logo.png")
    write_bytes(logo_path, data)
    return {"path": f"assets/logo.png"}


@router.get("/{project_id}/{filename}")
async def get_image(project_id: str, filename: str, db: Session = Depends(get_db)):
    """Get an image file from project assets directory"""
    from fastapi.responses import FileResponse
    
    # Verify project exists
    row = db.get(ProjectModel, project_id)
    if not row:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Build file path
    file_path = os.path.join(settings.projects_root, project_id, "assets", filename)
    
    # Check if file exists
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Image not found")
    
    # Return the image file
    return FileResponse(file_path)


@router.post("/{project_id}/upload")
async def upload_image(project_id: str, file: UploadFile = File(...), db: Session = Depends(get_db)):
    """Upload a file (image, CSV, or TXT) to project assets directory"""
    print(f"📤 File upload request: project_id={project_id}, filename={file.filename}")

    # Verify project exists
    row = db.get(ProjectModel, project_id)
    if not row:
        print(f"❌ Project not found: {project_id}")
        raise HTTPException(status_code=404, detail="Project not found")

    # Check if file type is supported (images, CSV, or TXT)
    print(f"📁 File info: content_type={file.content_type}, size={file.size}")
    allowed_types = ['image/', 'text/plain', 'text/csv', 'application/csv']
    is_allowed = False

    if file.content_type:
        # Check content type
        for allowed_type in allowed_types:
            if file.content_type.startswith(allowed_type) or file.content_type == allowed_type:
                is_allowed = True
                break

    # Also check file extension as fallback
    if not is_allowed and file.filename:
        file_ext = os.path.splitext(file.filename)[1].lower()
        if file_ext in ['.txt', '.csv', '.png', '.jpg', '.jpeg', '.gif', '.webp', '.svg']:
            is_allowed = True

    if not is_allowed:
        print(f"❌ Invalid file type: {file.content_type}")
        raise HTTPException(status_code=400, detail="File must be an image (PNG, JPG, GIF, WEBP, SVG), CSV, or TXT file")
    
    # Create assets directory if it doesn't exist
    project_assets = os.path.join(settings.projects_root, project_id, "assets")
    print(f"📁 Assets directory: {project_assets}")
    os.makedirs(project_assets, exist_ok=True)

    # Use original filename, handle conflicts with incremental numbering
    original_filename = file.filename or 'file.txt'

    # Get file name and extension
    name_without_ext, file_extension = os.path.splitext(original_filename)

    # If no extension, infer from content type
    if not file_extension:
        if file.content_type and file.content_type.startswith('image/'):
            file_extension = '.png'
        elif file.content_type in ['text/csv', 'application/csv']:
            file_extension = '.csv'
        else:
            file_extension = '.txt'
        original_filename = f"{name_without_ext}{file_extension}"

    # Check for filename conflicts and add number suffix if needed
    final_filename = original_filename
    file_path = os.path.join(project_assets, final_filename)
    counter = 1

    while os.path.exists(file_path):
        # Add (1), (2), etc. before extension
        final_filename = f"{name_without_ext}({counter}){file_extension}"
        file_path = os.path.join(project_assets, final_filename)
        counter += 1

    print(f"💾 Saving to: {file_path}")
    if counter > 1:
        print(f"📝 Original filename existed, renamed to: {final_filename}")

    # Determine file type
    file_type = 'unknown'
    if file.content_type:
        if file.content_type.startswith('image/'):
            file_type = 'image'
        elif file.content_type in ['text/csv', 'application/csv']:
            file_type = 'csv'
        elif file.content_type == 'text/plain':
            file_type = 'text'

    # Fallback to extension check
    if file_type == 'unknown':
        ext_lower = file_extension.lower()
        if ext_lower in ['.png', '.jpg', '.jpeg', '.gif', '.webp', '.svg']:
            file_type = 'image'
        elif ext_lower == '.csv':
            file_type = 'csv'
        elif ext_lower == '.txt':
            file_type = 'text'

    try:
        # Save file
        content = await file.read()
        write_bytes(file_path, content)
        print(f"✅ File saved successfully: {len(content)} bytes, type: {file_type}")

        return {
            "path": f"assets/{final_filename}",
            "absolute_path": file_path,
            "filename": final_filename,
            "original_filename": file.filename,
            "file_type": file_type,
            "content_type": file.content_type
        }
    except Exception as e:
        print(f"❌ Failed to save file: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")
