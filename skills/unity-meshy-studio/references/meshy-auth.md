# Meshy authentication

Meshy's developer API uses bearer API keys.

The skill's login helper does not accept a Meshy password. It opens the official site for browser login, then opens the API settings page where the user creates or copies a key.

Credential priority:

1. `MESHY_API_KEY` environment variable
2. Operating-system credential store through Python `keyring`
3. Session-only secure prompt

A key is verified by calling the balance endpoint. Do not expose the returned key or authorization header in logs.
