from dotenv import load_dotenv
load_dotenv()
import json
from graph import app

def main():
    startup_name = input("Enter startup name: ")
    
    result = app.invoke({
            "startup_name": startup_name,
            "research_findings": "",
            "timeline": "",
            "devil_argument": "",
            "critics_argument": "",
            "final_report": "",
            "research_attempts":0,
            "research_quality":""
          
    })
    #collecting evaluation data
    eval_data = {
    "startup_name": startup_name,
    "startup_status": result.get("startup_status"),
    "input": f"Analyze startup: {startup_name}",
    "retrieval_context": [
        result.get("core_concept", ""),
        result.get("market_competitors", ""),
        result.get("risk_simulation", ""),
        result.get("traction_info", ""),
        result.get("market_info", ""),
    ],
    "actual_output": result.get("final_report", "")
    }
    with open("latest_eval_data.json", "w") as f:
        json.dump(eval_data, f, indent=2)

    
    print("\n" + "="*50)
    print(result["final_report"])
    
    # save report to file
    filename = f"{startup_name.lower().replace(' ', '_')}_waguri.md"
    with open(filename, "w") as f:
        f.write(result["final_report"])
    print(f"\n[Report saved to {filename}]")

if __name__ == "__main__":
    main()