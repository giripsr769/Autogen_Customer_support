const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL ||
  (import.meta.env.PROD
    ? "/api"
    : "http://127.0.0.1:8000");


export async function streamSupportQuery(query, onEvent) {
  const response = await fetch(`${API_BASE_URL}/support/stream`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ query }),
  });

  if (!response.ok) {
    throw new Error(`Backend error: ${response.status}`);
  }

  if (!response.body) {
    throw new Error("Streaming response body is not available.");
  }

  const reader = response.body.getReader();
  const decoder = new TextDecoder();

  let buffer = "";
  let currentEvent = null;

  while (true) {
    const { value, done } = await reader.read();

    if (done) break;

    buffer += decoder.decode(value, {
      stream: true,
    });

    const lines = buffer.split("\n");

    buffer = lines.pop() || "";

    for (const rawLine of lines) {
      const line = rawLine.trim();

      if (!line) continue;

      if (line.startsWith("event:")) {
        currentEvent =
          line.slice(6).trim();

        continue;
      }

      if (line.startsWith("data:")) {
        const rawData =
          line.slice(5).trim();

        try {
          onEvent({
            event: currentEvent,
            data: JSON.parse(rawData),
          });
        } catch (error) {
          console.error(
            "Unable to parse SSE data:",
            error
          );
        }
      }
    }
  }
}