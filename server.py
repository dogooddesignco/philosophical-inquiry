#!/usr/bin/env python3
"""Local proxy that routes API calls through the authenticated Claude CLI."""

import http.server
import json
import subprocess
import os
import webbrowser
import threading

PORT = 8766

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path == "/api/messages":
            self.handle_claude_request()
        else:
            self.send_error(404)

    def handle_claude_request(self):
        content_length = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(content_length))

        system_prompt = body.get("system", "")
        messages = body.get("messages", [])
        model = body.get("model", "claude-sonnet-4-20250514")

        if not messages:
            self.send_json(400, {"error": {"message": "No messages provided"}})
            return

        # For multi-turn conversations, build a combined prompt
        # Single-turn: just use the user content directly
        # Multi-turn: format prior turns as context, latest user message as the prompt
        if len(messages) == 1:
            user_content = messages[0]["content"] if isinstance(messages[0]["content"], str) else json.dumps(messages[0]["content"])
        else:
            # Build conversation context for multi-turn
            parts = []
            for msg in messages[:-1]:
                role_label = "Human" if msg["role"] == "user" else "Assistant"
                content = msg["content"] if isinstance(msg["content"], str) else json.dumps(msg["content"])
                parts.append(f"[{role_label}]: {content}")
            # Latest message is the current prompt
            last = messages[-1]
            last_content = last["content"] if isinstance(last["content"], str) else json.dumps(last["content"])
            user_content = "Previous conversation:\n" + "\n\n".join(parts) + "\n\n---\n\nCurrent message:\n" + last_content

        # Build claude CLI command
        cmd = ["claude", "-p", user_content, "--model", model, "--output-format", "json"]
        if system_prompt:
            cmd.extend(["--system-prompt", system_prompt])

        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)

            if result.returncode != 0:
                err_msg = result.stderr.strip() or "Claude CLI returned an error"
                self.send_json(500, {"error": {"message": err_msg}})
                return

            # Parse CLI JSON output
            try:
                cli_output = json.loads(result.stdout)
                text = cli_output.get("result", result.stdout.strip())
            except json.JSONDecodeError:
                text = result.stdout.strip()

            # Return in Messages API format so the HTML doesn't need changes
            self.send_json(200, {
                "content": [{"type": "text", "text": text}],
                "role": "assistant",
                "model": model,
            })

        except subprocess.TimeoutExpired:
            self.send_json(504, {"error": {"message": "Claude CLI timed out (120s)"}})
        except FileNotFoundError:
            self.send_json(500, {"error": {"message": "Claude CLI not found. Run: npm install -g @anthropic-ai/claude-code"}})

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization, x-api-key, anthropic-version, anthropic-dangerous-direct-browser-access")
        self.end_headers()

    def send_json(self, code, data):
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        super().end_headers()


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    url = f"http://localhost:{PORT}/philosophical_inquiry.html"
    print(f"Philosophical Inquiry — opening {url}")
    print(f"Press Ctrl+C to stop\n")
    threading.Timer(0.5, lambda: webbrowser.open(url)).start()
    with http.server.HTTPServer(("", PORT), Handler) as httpd:
        httpd.serve_forever()
