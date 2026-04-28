from agent import threat_lens_agent
from langchain_core.messages import HumanMessage

def run_investigation(email_text):
    print(f"--- THREATLENS INVESTIGATION STARTED ---")
    
    # We send the email as a message to the agent
    inputs = {"messages": [HumanMessage(content=f"Investigate this email for threats: {email_text}")]}
    
    # We stream the steps so we can see the agent 'thinking'
    for output in threat_lens_agent.stream(inputs):
        for key, value in output.items():
            print(f"\n[Node: {key}]")
            # Print the last message content if it exists
            if "messages" in value:
                print(value["messages"][-1].content)

if __name__ == "__main__":
    # Test with a suspicious-looking email
    sample_email = "URGENT: Your bank account is locked! Verify now at http://secure-update-login.com"
    run_investigation(sample_email)