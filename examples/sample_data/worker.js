/*
    Cloudflare API (cloudflare-api)
    * Author: Nikhil John
    * Source: https://github.com/nikhiljohn10/cloudflare-api
    * License: MIT
*/

function get_html(body) {
    return `<!doctype html>
<html class="h-100" lang="en">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootswatch@5.1.1/dist/simplex/bootstrap.min.css"
            integrity="sha256-q4d6dBEE09GKG+jEE5jQ0gxJR/JNMcwOhpad0fbNkhc=" crossorigin="anonymous">
        <title>${WEBSITE_TITLE}</title>
        <style type="text/css">
        .cover-container {
            max-width: 42em;
        }
        </style>
    </head>

    <body class="d-flex h-100 text-center" data-new-gr-c-s-check-loaded="8.884.0" data-gr-ext-installed="">
        <div class="cover-container d-flex w-100 h-100 p-3 mx-auto flex-column">
            <header class="mb-auto"></header>
            <main class="px-3">
                ${body}
            </main>
            <footer class="mt-auto">
                <p><a href="/">Home</a> | Created by <a href="https://nikz.in">nikzjon</a></p>
            </footer>
        </div>
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.1/dist/js/bootstrap.min.js"
            integrity="sha384-skAcpIdS7UcVUC05LJ9Dxay8AXcDYfBJqt1CJ85S/CFujBsIzCIv+l9liuYLaMQ/" crossorigin="anonymous"></script>
    </body>
</html>` }

function error_page(code, content) {
    return get_html(`
    <h1>Error <span class="text-primary">${code}</span>: ${content}</h1>
    `)
}

function secret_page(content) {
    return get_html(`
    <h1>Your secret message</h1><h1>is</h1><h1 class="text-primary">${content}</h1>
    `)
}

function root_page() {
    return get_html(`
    <h1 class="text-primary">${WEBSITE_TITLE}</h1>
    <p class="lead mt-5">This is a sample page deployed by cloudlfare-api.</p>
    <p class="text-muted"><small>You can only access the secret message with the api key.</small></p>
    <p class="lead mt-5">
        <a href="https://github.com/nikhiljohn10/cloudflare-api" class="btn btn-lg btn-primary fw-bold">Learn more</a>
    </p>
    `)
}

addEventListener("fetch", (event) => {
    event.respondWith(
        handleRequest(event.request).catch(
            (err) => new Response(err.stack, {
                status: 500
            })
        )
    )
})

async function handleRequest(request) {
    const { pathname } = new URL(request.url)
    const headers = {
        "Content-Type": "text/html;charset=UTF-8"
    }

    if (pathname.startsWith("/" + SECRET_WEBSITE_TOKEN)) {
        const greeting = await DEPLOYMENT_EXAMPLE_NS.get("greeting")
        return new Response(secret_page(greeting), { headers })
    }

    if (pathname == ("/" || "")) {
        return new Response(root_page(), { headers })
    }

    return new Response(error_page(404, "Page not found"), {
        status: 404,
        headers: headers
    })
}