# Browser Automation & Real-Profile Inspection

## Primary: `chrome-devtools` MCP (Real Profile / Brave or Chromium)

When verifying live UI rendering, console errors, network requests, or authenticated flows in an existing Chromium/Brave profile, configure or connect the **`chrome-devtools` MCP server** with `--executablePath /usr/bin/brave-browser` (or the host's Chromium binary path):

```json
{
  "mcpServers": {
    "chrome-devtools": {
      "command": "npx",
      "args": [
        "-y",
        "chrome-devtools-mcp@latest",
        "--executablePath",
        "/usr/bin/brave-browser"
      ]
    }
  }
}
```

Use `--browserUrl http://127.0.0.1:9222` instead when attaching to an already-running browser launched with `--remote-debugging-port=9222` so existing cookies and extension state remain isolated to that session.

## Headless & Playwright Fallbacks

When MCP browser tools are unavailable or headless CI verification is needed:

1. Use direct headless screenshots for static DOM checks:

   ```bash
   brave-browser --headless=new --screenshot=<output-path> <url>
   ```

   (or `chromium --headless=new --screenshot=<output-path> <url>` / `google-chrome` depending on the host).
2. Use Playwright / headless Chromium assertions in automated test suites for interactive form/route verification rather than depending on desktop GUI state.
3. If an agent host provides a `browser_exec(..., use_real_profile=true)` tool, ensure the host's `x-www-browser` points to a supported Chromium family binary before enabling real-profile mode; otherwise omit real-profile mode (`new_tab()` without profile attachment).
