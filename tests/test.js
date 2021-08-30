addEventListener("fetch", (event) => {
  event.respondWith(
    handleRequest(event.request).catch(
      (err) => new Response(err.stack, { status: 500 })
    )
  );
});

addEventListener("scheduled", event => {
  event.waitUntil(handleScheduled(event));
});

async function handleScheduled(event) {
  return new Response();
}

async function handleRequest(request) {
  const { pathname } = new URL(request.url);

  if (pathname.startsWith("/set")) {
    return new Response(await MY_NEW_KV.put("test", "This is a test value set in MY_NEW_KV namespace"));
  }

  if (pathname.startsWith("/kv")) {
    return new Response(await MY_NEW_KV.get("test"));
  }

  if (pathname.startsWith("/var")) {
    return new Response("MY_NEW_VAR: " + MY_NEW_VAR);
  }

  if (pathname.startsWith("/secret")) {
    return new Response("MY_NEW_SECRET: " + MY_NEW_SECRET);
  }

  return new Response("This is testing worker");
}