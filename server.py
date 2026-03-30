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
        session_id = body.get("session_id")
        resume_session = body.get("resume_session")

        if not messages:
            self.send_json(400, {"error": {"message": "No messages provided"}})
            return

        # For persistent sessions, only send the latest user message
        # The CLI maintains conversation history via --session-id / --resume
        user_content = ""
        for msg in reversed(messages):
            if msg["role"] == "user":
                user_content = msg["content"] if isinstance(msg["content"], str) else json.dumps(msg["content"])
                break

        if not user_content:
            self.send_json(400, {"error": {"message": "No user message provided"}})
            return

        # Build claude CLI command
        cmd = ["claude", "-p", user_content, "--model", model, "--output-format", "json"]
        if system_prompt:
            cmd.extend(["--system-prompt", system_prompt])

        # Session management: resume existing session or start new one
        if resume_session:
            cmd.extend(["--resume", resume_session])
        elif session_id:
            cmd.extend(["--session-id", session_id])

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
                returned_session_id = cli_output.get("session_id")
            except json.JSONDecodeError:
                text = result.stdout.strip()
                returned_session_id = None

            # Return in Messages API format with session_id for continuity
            response = {
                "content": [{"type": "text", "text": text}],
                "role": "assistant",
                "model": model,
            }
            if returned_session_id:
                response["session_id"] = returned_session_id

            self.send_json(200, response)

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
