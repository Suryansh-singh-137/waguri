from dotenv import load_dotenv
load_dotenv()

from graph import app

def main():
    startup_name = input("Enter startup name: ")
    
    result = app.invoke({
            "startup_name": startup_name,
            "": "",
            "timeline": "",
            "devil_argument": "",
            "critics_argument": "",
            "final_report": "",
            "research_attempts":0,
            "research_quality":""
          
    })
    
    print("\n" + "="*50)
    print(result["final_report"])
    
    # save report to file
    filename = f"{startup_name.lower().replace(' ', '_')}_waguri.md"
    with open(filename, "w") as f:
        f.write(result["final_report"])
    print(f"\n[Report saved to {filename}]")

if __name__ == "__main__":
    main()