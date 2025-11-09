# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a full-stack quantitative trading platform called "chat-quant" that combines a Next.js frontend with a FastAPI backend. The platform enables users to create, backtest, and analyze quantitative trading strategies through an AI-powered chat interface.

## Architecture

### Monorepo Structure
- `apps/web/` - Next.js 14 frontend (TypeScript, React, Tailwind CSS)
- `apps/api/` - FastAPI backend (Python 3.10+)
- `project_template/` - Template for new quantitative strategy projects
- `scripts/` - Development and setup automation scripts
- `docker/` - Docker deployment configuration

### Backend (FastAPI)
- **Entry Point**: `apps/api/start_main.py` runs uvicorn on port 8080
- **Main App**: `apps/api/app/main.py` defines FastAPI app with all routers
- **Database**: SQLite (default: `data/cc.db`) with SQLAlchemy ORM
- **Key Routes**:
  - `/api/projects` - Project management
  - `/api/chat/{project_id}` - WebSocket chat interface
  - `/api/eval` - Agent trace & evaluation
  - `/api/github`, `/api/vercel` - External integrations
  - `/api/auth` - User authorization
- **Core Services**:
  - `app/core/config.py` - Configuration management with environment variables
  - `app/core/websocket/manager.py` - WebSocket connection management
  - `app/db/session.py` - Database session management
  - `app/models/` - SQLAlchemy models for projects, messages, sessions, etc.

### Frontend (Next.js)
- **Entry Point**: `apps/web/app/page.tsx` - Project list/home page
- **Chat Interface**: `apps/web/app/[project_id]/chat/page.tsx`
- **Key Components**:
  - `components/chat/` - Chat UI components
  - `components/settings/` - Settings modals
  - `contexts/` - React contexts for global state
- **API Communication**: WebSocket for real-time chat, REST for project operations

### Quantitative Strategy System
- **Base Class**: `project_template/strategy/base_strategy.py` - All strategies inherit from `BaseStrategy`
- **Strategy Runner**: `project_template/strategy/strategy_runner.py` - Backtrader integration
- **Backtest Execution**: `project_template/strategy/run_backtest.py` - CLI for running backtests
- **Data Source**: akshare library for Chinese stock market data
- **Technical Indicators**: TA-Lib for indicator calculations
- **Backtest Framework**: backtrader for strategy testing

## Development Commands

### Initial Setup
```bash
npm run setup              # Install all dependencies
npm run ensure:env         # Create .env from .env.example if missing
npm run ensure:venv        # Setup Python virtual environment
```

### Development
```bash
npm run dev                # Start both frontend and backend concurrently
npm run dev:web            # Start Next.js frontend only (port 3000)
npm run dev:api            # Start FastAPI backend only (port 8080)
```

### Database
```bash
npm run db:reset           # Reset database (drops all tables)
npm run db:backup          # Backup current database
```

### Cleanup
```bash
npm run clean              # Clean build artifacts and caches
```

### Python Backend (Direct)
```bash
cd apps/api
source .venv/bin/activate  # Activate virtual environment
python start_main.py       # Start backend on port 8080
```

### Strategy Backtesting
```bash
cd project_template/strategy
python run_backtest.py <strategy_file> \
  --symbols "300031,000001" \
  --start-date 20240101 \
  --end-date 20241231 \
  --output data_file/final/result.json \
  --cash 100000 \
  --commission 0.001 \
  --params '{"ma_short":10,"ma_long":30}'
```

## Environment Configuration

Required environment variables (see `.env.example`):
- `ANTHROPIC_API_KEY` - **Required** for Claude Code SDK
- `API_PORT` - Backend port (default: 8080)
- `DATABASE_URL` - SQLite database path
- `PROJECTS_ROOT` - Project storage directory
- `CLAUDE_CODE_MODEL` - Claude model to use (default: claude-sonnet-4-5-20250929)

## Key Technical Details

### Database
- SQLite with SQLAlchemy ORM
- Auto-creates tables on startup via `app/main.py:on_startup()`
- Migrations handled by `app/db/migrations.py`
- Foreign key constraints enabled

### WebSocket Communication
- Chat interface uses WebSocket at `/api/chat/{project_id}`
- Manager handles multiple concurrent connections
- Real-time message streaming from Claude

### Strategy Development
1. Create strategy class inheriting from `BaseStrategy` in `project_template/strategy/impls/`
2. Implement `__init__()` and `next()` methods
3. Use `self.buy_signal()` and `self.sell_signal()` for trades
4. Run backtest using `run_backtest.py` script
5. Results saved as JSON in `data_file/final/`

### Python Dependencies
Key packages (see `apps/api/requirements.txt`):
- fastapi, uvicorn - Web framework
- SQLAlchemy - ORM
- claude-agent-sdk - Claude integration
- backtrader - Backtesting framework
- akshare - Financial data
- TA-Lib - Technical indicators
- pandas, numpy - Data processing

### Frontend Stack
- Next.js 14 with App Router
- TypeScript
- Tailwind CSS
- Framer Motion for animations
- React Markdown for message rendering

## Docker Deployment

Build and run:
```bash
docker build -f docker/Dockerfile -t chat-quant:latest .
docker run -d -p 3000:3000 -p 8000:8000 \
  -v /path/to/data:/app/data \
  chat-quant:latest
```

See `docker/README.md` for K8s deployment details.

## Project Root Detection

The backend automatically detects project root by looking for `apps/` directory and `Makefile`. Configuration paths are relative to detected project root.
