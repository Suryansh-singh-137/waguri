import json
import uuid
from dotenv import load_dotenv
from graph import app

load_dotenv()

def main():
    startup_name = input("Enter startup name: ").strip()
    if not startup_name:
        print("Startup name cannot be empty.")
        return

    # 1. Create a unique thread_id for this run
    thread_id = str(uuid.uuid4())
    config = {"configurable": {"thread_id": thread_id}}

    initial_state = {
        "startup_name": startup_name,
        "research_findings": "",
        "timeline": "",
        "devil_argument": "",
        "critics_argument": "",
        "final_report": "",
        "research_attempts": 0,
        "research_quality": ""
    }

    print(f"\n--- [1/2] Analyzing & Classifying: {startup_name} ---")
    
    # Run graph until the interrupt_after checkpoint
    app.invoke(initial_state, config=config)

    # 2. Inspect current graph state at the checkpoint
    current_state = app.get_state(config)
    detected_status = current_state.values.get("startup_status", "unknown")

    print(f"\n[HITL INTERRUPT] AI classified '{startup_name}' as: [{detected_status.upper()}]")
    print(f"Next destination branch: {current_state.next}")

    # 3. Human decision prompt
    user_choice = input(
        "\nOptions:\n"
        "  [ENTER]       - Confirm and proceed\n"
        "  [alive/dead/pre_launch] - Override classification\n"
        "  [q]           - Abort run\n"
        "Your choice: "
    ).strip().lower()

    if user_choice == "q":
        print("Execution aborted by user.")
        return
    elif user_choice in ["alive", "dead", "pre_launch"]:
        # Update graph state with human override
        print(f"Overriding status to: [{user_choice.upper()}]")
        app.update_state(config, {"startup_status": user_choice})

    print(f"\n--- [2/2] Resuming Graph Execution ---")
    
    # 4. Resume execution by passing None with the existing config
    final_output = app.invoke(None, config=config)

    # 5. Collect Evaluation Telemetry
    eval_data = {
        "startup_name": startup_name,
        "startup_status": final_output.get("startup_status"),
        "input": f"Analyze startup: {startup_name}",
        "retrieval_context": [
            final_output.get("core_concept", ""),
            final_output.get("market_competitors", ""),
            final_output.get("risk_simulation", ""),
            final_output.get("traction_info", ""),
            final_output.get("market_info", ""),
            final_output.get("research_findings", "")
        ],
        "actual_output": final_output.get("final_report", "")
    }

    with open("latest_eval_data.json", "w") as f:
        json.dump(eval_data, f, indent=2)

    # 6. Print and Save Markdown Report
    print("\n" + "=" * 50)
    print(final_output.get("final_report", "No report generated."))
    
    filename = f"{startup_name.lower().replace(' ', '_')}_waguri.md"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(final_output.get("final_report", ""))
    print(f"\n[Report saved to {filename}]")

if __name__ == "__main__":
    main()