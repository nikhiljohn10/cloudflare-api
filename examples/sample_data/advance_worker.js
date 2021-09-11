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

    if (pathname.startsWith("/kv")) {
        const value = await MY_NEW_KV.get("test")
        if (value) return new Response(value);
        return new Response("No store value found.", { status: 404 });
    }

    if (pathname.startsWith("/var")) {
        return new Response("MY_NEW_VAR: " + MY_NEW_VAR);
    }

    if (pathname.startsWith("/secret")) {
        return new Response("MY_NEW_SECRET: " + MY_NEW_SECRET);
    }

    return new Response("This is testing worker");
}