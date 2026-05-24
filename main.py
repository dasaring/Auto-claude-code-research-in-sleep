#!/usr/bin/env python3
"""
Auto-claude-code-research-in-sleep

Main entry point for the automated Claude AI code research assistant.
This tool runs research tasks autonomously using Claude API while you sleep.
"""

import os
import sys
import logging
import argparse
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("research.log", encoding="utf-8"),
    ],
)
logger = logging.getLogger(__name__)


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Auto-claude-code-research-in-sleep: Automated AI-powered code research",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --task "Research best practices for async Python"
  python main.py --task-file tasks.txt --output-dir results/
  python main.py --config config.yaml
        """,
    )

    parser.add_argument(
        "--task",
        type=str,
        help="Single research task to execute",
    )
    parser.add_argument(
        "--task-file",
        type=Path,
        help="Path to a file containing multiple research tasks (one per line)",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("output"),
        help="Directory to save research results (default: ./output)",
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=Path("config.yaml"),
        help="Path to configuration file (default: config.yaml)",
    )
    parser.add_argument(
        "--model",
        type=str,
        default=os.getenv("CLAUDE_MODEL", "claude-3-5-sonnet-20241022"),
        help="Claude model to use for research",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate configuration and tasks without executing API calls",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose/debug logging",
    )

    return parser.parse_args()


def validate_environment() -> bool:
    """Validate that required environment variables are set."""
    required_vars = ["ANTHROPIC_API_KEY"]
    missing = [var for var in required_vars if not os.getenv(var)]

    if missing:
        logger.error(
            "Missing required environment variables: %s", ", ".join(missing)
        )
        logger.error("Please copy .env.example to .env and fill in the required values.")
        return False

    return True


def main() -> int:
    """Main entry point for the research assistant."""
    args = parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
        logger.debug("Verbose logging enabled")

    logger.info("Starting Auto-claude-code-research-in-sleep")

    # Validate environment
    if not validate_environment():
        return 1

    # Ensure output directory exists
    args.output_dir.mkdir(parents=True, exist_ok=True)
    logger.info("Output directory: %s", args.output_dir.resolve())

    if args.dry_run:
        logger.info("Dry-run mode enabled — skipping API calls")
        logger.info("Configuration validated successfully")
        return 0

    if not args.task and not args.task_file:
        logger.error("No task specified. Use --task or --task-file.")
        return 1

    # Lazy import to avoid startup cost when just validating
    from agent.research_agent import ResearchAgent

    agent = ResearchAgent(
        model=args.model,
        output_dir=args.output_dir,
        config_path=args.config if args.config.exists() else None,
    )

    if args.task:
        logger.info("Running single task: %s", args.task)
        agent.run_task(args.task)
    elif args.task_file:
        logger.info("Running tasks from file: %s", args.task_file)
        agent.run_tasks_from_file(args.task_file)

    logger.info("Research session complete. Results saved to: %s", args.output_dir)
    return 0


if __name__ == "__main__":
    sys.exit(main())
