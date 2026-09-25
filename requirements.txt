async function api(url, options = {}) {

    const response = await fetch(
        url,
        {
            credentials: "include",
            ...options
        }
    );

    let data = {};

    try {
        data = await response.json();
    } catch (error) {
        data = {};
    }

    if (!response.ok) {

        throw new Error(
            data.detail ||
            data.message ||
            "Request failed"
        );
    }

    return data;
}


function showMessage(
    message,
    success = false
) {

    const element =
        document.getElementById(
            "formMessage"
        );

    if (!element) {
        return;
    }

    element.textContent = message;

    if (success) {

        element.style.background =
            "#e9f8ee";

        element.style.color =
            "#1e7b42";

    } else {

        element.style.background =
            "#fff0f0";

        element.style.color =
            "#a52222";
    }
}


function bindAuthForm(
    formId,
    url
) {

    const form =
        document.getElementById(formId);

    if (!form) {
        return;
    }

    form.addEventListener(
        "submit",
        async function (event) {

            event.preventDefault();

            const body =
                Object.fromEntries(
                    new FormData(form)
                );

            try {

                const data =
                    await api(
                        url,
                        {
                            method: "POST",

                            headers: {
                                "Content-Type":
                                    "application/json"
                            },

                            body:
                                JSON.stringify(body)
                        }
                    );

                showMessage(
                    data.message,
                    true
                );

                setTimeout(
                    function () {
                        location.href =
                            "/dashboard";
                    },
                    500
                );

            } catch (error) {

                showMessage(
                    error.message
                );
            }
        }
    );
}


function loading(
    on
) {

    const element =
        document.getElementById(
            "loading"
        );

    if (!element) {
        return;
    }

    element.style.display =
        on
            ? "block"
            : "none";
}


function renderResults(
    data
) {

    const root =
        document.getElementById(
            "results"
        );

    if (!root) {
        return;
    }


    const allocation =
        Object.entries(
            data.budget_allocation || {}
        )
        .map(
            ([key, value]) => {

                return `
                    <div class="alloc">

                        <span>
                            ${pretty(key)}
                        </span>

                        <b>
                            ₹${Number(
                                value || 0
                            ).toLocaleString("en-IN")}
                        </b>

                    </div>
                `;
            }
        )
        .join("");


    const products =
        (
            data.recommendations || []
        )
        .map(
            product => {

                return `

                    <article class="product">

                        <div class="product-icon">
                            ${product.emoji || "✨"}
                        </div>

                        <span class="tag">
                            ${esc(
                                product.platform ||
                                "General"
                            )}
                        </span>

                        <h3>
                            ${esc(
                                product.name
                            )}
                        </h3>

                        <p>
                            ${esc(
                                product.reason ||
                                "Budget-aware suggestion."
                            )}
                        </p>

                        <div>
                            ⭐
                            ${Number(
                                product.rating || 0
                            ).toFixed(1)}

                            ·

                            ${Number(
                                product.discount || 0
                            )}% off
                        </div>

                        <div class="price">

                            ₹${Number(
                                product.price || 0
                            ).toLocaleString("en-IN")}

                            ${
                                product.unit &&
                                product.unit !== "item"
                                    ? `
                                        <small>
                                            ${esc(
                                                product.unit
                                            )}
                                        </small>
                                    `
                                    : ""
                            }

                        </div>

                        ${
                            product.url &&
                            product.url !== "#"
                                ? `
                                    <a
                                        class="product-link"
                                        href="${product.url}"
                                        target="_blank"
                                        rel="noopener"
                                    >
                                        View source ↗
                                    </a>
                                `
                                : ""
                        }

                    </article>

                `;
            }
        )
        .join("");


    root.innerHTML = `

        <div class="result-head">

            <div>

                <span class="eyebrow">
                    YOUR PLAN
                </span>

                <h2>
                    ${esc(
                        data.summary ||
                        "AI recommendation"
                    )}
                </h2>

            </div>

            <span class="tag">
                ${esc(
                    data.source ||
                    "AI"
                )}
            </span>

        </div>


        <div class="allocation">

            ${allocation}

        </div>


        <h2>
            Recommendations
        </h2>


        <div class="products">

            ${
                products ||
                `
                    <div class="panel">
                        No recommendations returned.
                    </div>
                `
            }

        </div>


        <div class="tips">

            <h3>
                Practical tips
            </h3>

            <ul>

                ${
                    (data.tips || [])
                    .map(
                        tip =>
                            `<li>${esc(tip)}</li>`
                    )
                    .join("")
                }

            </ul>

        </div>

    `;


    root.scrollIntoView({
        behavior: "smooth"
    });
}


function pretty(
    value
) {

    return value
        .replaceAll(
            "_",
            " "
        )
        .replace(
            /\b\w/g,
            character =>
                character.toUpperCase()
        );
}


function esc(
    value
) {

    return String(
        value ?? ""
    ).replace(
        /[&<>'"]/g,
        character => {

            return {

                "&": "&amp;",
                "<": "&lt;",
                ">": "&gt;",
                "'": "&#39;",
                '"': "&quot;"

            }[character];
        }
    );
}


function bindHomePlanner() {

    const form =
        document.getElementById(
            "homeForm"
        );

    if (!form) {
        return;
    }


    form.addEventListener(
        "submit",
        async function (event) {

            event.preventDefault();

            loading(true);

            const formData =
                new FormData(form);


            const payload = {

                budget:
                    Number(
                        formData.get(
                            "budget"
                        )
                    ),

                rooms:
                    formData.getAll(
                        "rooms"
                    ),

                style:
                    formData.get(
                        "style"
                    ),

                location:
                    formData.get(
                        "location"
                    ),

                quantities: {

                    lights:
                        Number(
                            formData.get(
                                "lights"
                            )
                        ),

                    fans:
                        Number(
                            formData.get(
                                "fans"
                            )
                        ),

                    dining_tables:
                        Number(
                            formData.get(
                                "dining_tables"
                            )
                        ),

                    storage_units:
                        Number(
                            formData.get(
                                "storage_units"
                            )
                        )
                }
            };


            try {

                const result =
                    await api(
                        "/generate-home",
                        {
                            method: "POST",

                            headers: {
                                "Content-Type":
                                    "application/json"
                            },

                            body:
                                JSON.stringify(
                                    payload
                                )
                        }
                    );

                renderResults(
                    result
                );

            } catch (error) {

                alert(
                    error.message
                );

            } finally {

                loading(false);
            }
        }
    );
}


function bindPartyPlanner() {

    const form =
        document.getElementById(
            "partyForm"
        );

    if (!form) {
        return;
    }


    form.addEventListener(
        "submit",
        async function (event) {

            event.preventDefault();

            loading(true);

            const formData =
                new FormData(form);


            const payload = {

                budget:
                    Number(
                        formData.get(
                            "budget"
                        )
                    ),

                guests:
                    Number(
                        formData.get(
                            "guests"
                        )
                    ),

                event_type:
                    formData.get(
                        "event_type"
                    ),

                venue:
                    formData.get(
                        "venue"
                    ),

                theme:
                    formData.get(
                        "theme"
                    ),

                location:
                    formData.get(
                        "location"
                    )
            };


            try {

                const result =
                    await api(
                        "/generate-party",
                        {
                            method: "POST",

                            headers: {
                                "Content-Type":
                                    "application/json"
                            },

                            body:
                                JSON.stringify(
                                    payload
                                )
                        }
                    );

                renderResults(
                    result
                );

            } catch (error) {

                alert(
                    error.message
                );

            } finally {

                loading(false);
            }
        }
    );
}


function bindJewelryPlanner() {

    const form =
        document.getElementById(
            "jewelryForm"
        );

    if (!form) {
        return;
    }


    form.addEventListener(
        "submit",
        async function (event) {

            event.preventDefault();

            loading(true);

            try {

                const result =
                    await api(
                        "/generate-jewelry",
                        {
                            method: "POST",

                            body:
                                new FormData(
                                    form
                                )
                        }
                    );

                renderResults(
                    result
                );

            } catch (error) {

                alert(
                    error.message
                );

            } finally {

                loading(false);
            }
        }
    );
}


async function loadSessionData() {

    const element =
        document.getElementById(
            "dashboardStats"
        );

    if (!element) {
        return;
    }


    try {

        const data =
            await api(
                "/session-data"
            );

        element.innerHTML = `

            <b>
                ${data.recommendation_count}
            </b>

            saved recommendation plan(s).

            <a href="/history">
                View history →
            </a>

        `;

    } catch (error) {

        element.textContent =
            "Could not load session information.";
    }
}


async function loadHistory() {

    const element =
        document.getElementById(
            "historyList"
        );

    if (!element) {
        return;
    }


    try {

        const rows =
            await api(
                "/history"
            );


        if (!rows.length) {

            element.innerHTML = `

                <div class="panel">

                    No saved plans yet.

                    Create your first recommendation.

                </div>

            `;

            return;
        }


        element.innerHTML =
            rows
            .map(
                row => `

                    <details class="history-item">

                        <summary>

                            ${pretty(
                                row.planner
                            )}

                            plan ·

                            ${row.created_at}

                        </summary>

                        <p>
                            ${esc(
                                row.response.summary ||
                                ""
                            )}
                        </p>

                        <a
                            class="product-link"
                            href="/planner/${row.planner}"
                        >
                            Create another
                        </a>

                    </details>

                `
            )
            .join("");


    } catch (error) {

        element.innerHTML = `

            <div class="panel">

                Please log in to view
                recommendation history.

            </div>

        `;
    }
}