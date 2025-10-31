import argparse
import asyncio

from app.agent.manus import Manus
from app.logger import logger


async def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Run Manus agent with a prompt")
    parser.add_argument(
        "--prompt", type=str, required=False, help="Input prompt for the agent"
    )
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="Run in interactive mode (keep agent alive after task completion)",
    )
    parser.add_argument(
        "--keep-memory",
        action="store_true",
        help="Keep conversation memory between tasks (default: clear memory for each task)",
    )
    args = parser.parse_args()

    # Create and initialize Manus agent
    agent = await Manus.create()
    try:
        # Interactive mode: keep running and wait for new prompts
        if args.interactive or not args.prompt:
            logger.info(
                "🚀 Starting interactive mode. Type 'exit' or 'quit' to end the session."
            )
            logger.info("=" * 60)

            while True:
                try:
                    # Get user input
                    prompt = input(
                        "\n💬 Enter your prompt (or 'exit'/'quit' to end): "
                    ).strip()

                    # Check for exit commands
                    if prompt.lower() in ["exit", "quit", "q"]:
                        logger.info("👋 Exiting interactive mode...")
                        break

                    if not prompt:
                        logger.warning(
                            "⚠️  Empty prompt provided. Please enter a command or 'exit' to quit."
                        )
                        continue

                    # Reset agent state for new task
                    from app.schema import AgentState, Memory

                    agent.state = AgentState.IDLE
                    agent.current_step = 0

                    # Clear memory unless --keep-memory flag is set
                    if not args.keep_memory:
                        agent.memory = Memory()
                        logger.debug("🧹 Memory cleared for new task")
                    else:
                        logger.debug("💾 Keeping previous conversation memory")

                    logger.warning("📝 Processing your request...")
                    await agent.run(prompt)
                    logger.info("✅ Request processing completed.")
                    logger.info("-" * 60)

                except KeyboardInterrupt:
                    logger.warning(
                        "\n⚠️  Operation interrupted. Type 'exit' to quit or enter a new prompt."
                    )
                    continue
        else:
            # Single task mode: run once and exit
            prompt = args.prompt
            if not prompt.strip():
                logger.warning("Empty prompt provided.")
                return

            logger.warning("Processing your request...")
            await agent.run(prompt)
            logger.info("Request processing completed.")

    except KeyboardInterrupt:
        logger.warning("Operation interrupted.")
    finally:
        # Ensure agent resources are cleaned up before exiting
        logger.info("🧹 Cleaning up resources...")
        await agent.cleanup()
        logger.info("✨ Cleanup complete. Goodbye!")


if __name__ == "__main__":
    asyncio.run(main())
