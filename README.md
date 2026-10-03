![stfu](stfu.webp)

On each prompt, stfu.py asks [Jev](https://typesafe.ai) how long the answer should be and adds a length limit to the turn.

**Before**

```
# User

Which port does the app listen on?

# Assistant

Great question! Rather than answering from memory, let me actually check the
code. I'll start by looking at the server entry point... I found the config
loader, which reads PORT from the environment and falls back to a default.
Let me run the app to confirm. Now I can see the port the app listens on:
it's 9090.
```

**After**

```
# User

Which port does the app listen on?

# Assistant

The app listens on port 9090.
```

## Install

```sh
export TYPESAFE_API_KEY=...
```

In `~/.claude/settings.json`:

```json
{
  "hooks": {
    "UserPromptSubmit": [
      { "hooks": [{ "type": "command", "command": "uv run --script /path/to/stfu.py" }] }
    ]
  }
}
```
