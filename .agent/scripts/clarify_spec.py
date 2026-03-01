import os
import subprocess
import requests
import json
import sys

def get_modified_specs():
    """Find modified spec.md files in the current PR compared to the base branch."""
    base_sha = os.environ.get("BASE_SHA", "origin/main")
    try:
        cmd = ["git", "diff", "--name-only", f"{base_sha}...HEAD"]
        output = subprocess.check_output(cmd).decode("utf-8")
        files = output.splitlines()
        # Look for spec.md in any directory
        return [f for f in files if f.endswith("spec.md") and os.path.exists(f)]
    except Exception as e:
        print(f"Error finding modified specs: {e}")
        return []

def run_ollama_clarify(spec_path, workflow_instructions):
    """Call local Ollama to perform clarification."""
    with open(spec_path, "r", encoding="utf-8") as f:
        spec_content = f.read()
    
    # We instruct it to follow the workflow and AUTOMATICALLY accept recommendations
    prompt = f"""
You are Antigravity, an AI architect. Your task is to execute the 'speckit.clarify' workflow on the SPEC below.

CORE OBJECTIVE:
Identify ambiguities and resolve them by selecting the MOST LOGICAL recommended outcome based on best practices. 
Do not ask questions. Integrate the resolutions directly into the spec.

WORKFLOW CONTEXT:
{workflow_instructions}

TARGET SPECIFICATION:
{spec_content}

EXECUTION RULES:
1. Scan the spec for coverage gaps (Functional, Data, UX, etc.).
2. For each ambiguity, determine the 'Recommended' path.
3. Automatically apply these 'Recommended' outcomes to the spec.
4. Ensure a '## Clarifications' section exists with session date: {os.popen('date /t').read().strip() if os.name == 'nt' else os.popen('date +%Y-%m-%d').read().strip()}.
5. Add bullets in '## Clarifications' like: - Q: [Ambiguity] -> A: [Recommended Resolution].
6. Return the ENTIRE updated markdown content of the spec. 
7. DO NOT include any conversational text before or after the markdown. 
8. Keep existing formatting intact.

OUTPUT:
[Updated Spec Content]
"""
        
    print(f"Sending request to Ollama for {spec_path}...")
    try:
        response = requests.post("http://localhost:11434/api/generate", 
            json={
                "model": "mistral",
                "prompt": prompt,
                "stream": False,
                "options": {
                    "num_ctx": 16383,
                    "temperature": 0.1
                }
            }, timeout=300)
        
        if response.status_code == 200:
            content = response.json().get("response", "")
            # Clean up potential markdown blocks added by LLM
            if "```markdown" in content:
                content = content.split("```markdown")[1].split("```")[0].strip()
            elif "```" in content:
                # Find the largest block if there are multiple
                blocks = re.findall(r'```(?:markdown)?\n(.*?)\n```', content, re.DOTALL)
                if blocks:
                    content = max(blocks, key=len)
            return content
        else:
            print(f"Error calling Ollama: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"Exception during Ollama call: {e}")
        return None

import re

def main():
    specs = get_modified_specs()
    if not specs:
        print("No modified spec.md files found.")
        sys.exit(0)

    # Load workflow context
    workflow_path = ".agent/workflows/speckit.clarify.md"
    if not os.path.exists(workflow_path):
        print(f"Workflow file not found: {workflow_path}")
        sys.exit(1)
        
    with open(workflow_path, "r", encoding="utf-8") as f:
        workflow_instructions = f.read()

    any_updated = False
    for spec in specs:
        print(f"Clarifying {spec}...")
        updated_content = run_ollama_clarify(spec, workflow_instructions)
        if updated_content and len(updated_content) > 100: # Basic sanity check
            with open(spec, "w", encoding="utf-8") as f:
                f.write(updated_content)
            print(f"Successfully updated {spec}")
            any_updated = True
        else:
            print(f"Failed to get valid update for {spec}")

    if not any_updated:
        sys.exit(1)

if __name__ == "__main__":
    main()
