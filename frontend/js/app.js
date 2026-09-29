const API_URL = "http://127.0.0.1:8000";


// ============================================================
// ELEMENTS
// ============================================================

const hero =
    document.getElementById("hero");

const resultsSection =
    document.getElementById("resultsSection");

const historySection =
    document.getElementById("historySection");

const searchForm =
    document.getElementById("searchForm");

const searchAgainForm =
    document.getElementById("searchAgainForm");

const searchInput =
    document.getElementById("searchInput");

const searchAgainInput =
    document.getElementById("searchAgainInput");

const loading =
    document.getElementById("loading");

const answerContainer =
    document.getElementById("answerContainer");

const sourcesContainer =
    document.getElementById("sourcesContainer");

const historyButton =
    document.getElementById("historyButton");

const homeButton =
    document.getElementById("homeButton");

const clearHistoryButton =
    document.getElementById(
        "clearHistoryButton"
    );

const historyContainer =
    document.getElementById(
        "historyContainer"
    );

const sourcePanel =
    document.getElementById(
        "sourcePanel"
    );

const panelOverlay =
    document.getElementById(
        "panelOverlay"
    );

const closePanel =
    document.getElementById(
        "closePanel"
    );

const panelTitle =
    document.getElementById(
        "panelTitle"
    );

const panelContent =
    document.getElementById(
        "panelContent"
    );

const panelOpenLink =
    document.getElementById(
        "panelOpenLink"
    );

const panelAskButton =
    document.getElementById(
        "panelAskButton"
    );

const toast =
    document.getElementById("toast");


// ============================================================
// STATE
// ============================================================

let currentSources = [];

let selectedSource = null;

let currentQuery = "";


// ============================================================
// SEARCH
// ============================================================

async function performSearch(query) {

    query = query.trim();

    if (!query) {
        showToast(
            "Please enter something to search."
        );

        return;
    }


    currentQuery = query;


    // Switch UI

    hero.classList.add("hidden");

    historySection.classList.add(
        "hidden"
    );

    resultsSection.classList.remove(
        "hidden"
    );


    // Show loading

    loading.classList.remove(
        "hidden"
    );

    answerContainer.innerHTML = "";

    sourcesContainer.innerHTML = "";


    try {

        const response =
            await fetch(
                `${API_URL}/api/search`,
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({
                        query
                    })
                }
            );


        const data =
            await response.json();


        if (!response.ok) {

            throw new Error(
                data.detail ||
                "Search failed."
            );
        }


        currentSources =
            data.sources || [];


        // Display AI answer

        displayAnswer(
            data.answer
        );


        // Display sources

        displaySources(
            currentSources
        );


    } catch (error) {

        displayError(
            error.message
        );


    } finally {

        loading.classList.add(
            "hidden"
        );

    }


    window.scrollTo({
        top: 0,
        behavior: "smooth"
    });
}


// ============================================================
// AI ANSWER
// ============================================================

function displayAnswer(answer) {

    if (!answer) {

        answerContainer.innerHTML = `
            <div class="answer-card">

                <div class="answer-heading">

                    <div class="ai-icon">
                        ✦
                    </div>

                    <div class="answer-title">
                        AI ANSWER
                    </div>

                </div>

                <div class="answer-text">
                    No AI answer was generated.
                </div>

            </div>
        `;

        return;
    }


    let rendered;


    try {

        rendered =
            marked.parse(
                answer
            );

    } catch {

        rendered =
            escapeHtml(answer);
    }


    answerContainer.innerHTML = `
        <div class="answer-card">

            <div class="answer-heading">

                <div class="ai-icon">
                    ✦
                </div>

                <div class="answer-title">
                    AI ANSWER
                </div>

            </div>

            <div class="answer-text">
                ${rendered}
            </div>

        </div>
    `;
}


// ============================================================
// SOURCES
// ============================================================

function displaySources(sources) {

    if (
        !sources ||
        sources.length === 0
    ) {

        sourcesContainer.innerHTML = `
            <h2>Sources</h2>

            <p style="color:#737b86">
                No web sources were found.
            </p>
        `;

        return;
    }


    sourcesContainer.innerHTML = `
        <h2>
            Sources · ${sources.length}
        </h2>
    `;


    sources.forEach(
        (source, index) => {

            const card =
                document.createElement(
                    "article"
                );


            card.className =
                "source-card";


            card.innerHTML = `
                <div class="source-number">
                    ${index + 1}
                </div>

                <div class="source-info">

                    <div class="source-title">
                        ${escapeHtml(
                            source.title ||
                            "Untitled source"
                        )}
                    </div>

                    <div class="source-url">
                        ${escapeHtml(
                            source.url || ""
                        )}
                    </div>

                    <div class="source-content">
                        ${escapeHtml(
                            source.content ||
                            "No preview available."
                        )}
                    </div>

                </div>

                <div class="source-actions">

                    <button
                        class="view-source-button"
                        data-index="${index}"
                    >
                        View
                    </button>

                    <a
                        href="${escapeAttribute(
                            source.url
                        )}"
                        target="_blank"
                        rel="noopener noreferrer"
                    >
                        Open ↗
                    </a>

                </div>
            `;


            const viewButton =
                card.querySelector(
                    ".view-source-button"
                );


            viewButton.addEventListener(
                "click",
                () => {

                    openSourcePanel(
                        source
                    );

                }
            );


            sourcesContainer.appendChild(
                card
            );
        }
    );
}


// ============================================================
// SOURCE PANEL
// ============================================================

function openSourcePanel(source) {

    selectedSource =
        source;


    panelTitle.textContent =
        source.title ||
        "Source";


    panelContent.innerHTML =
        markdownSource(
            source.content ||
            "No preview available."
        );


    panelOpenLink.href =
        source.url ||
        "#";


    sourcePanel.classList.add(
        "open"
    );

    panelOverlay.classList.add(
        "open"
    );
}


function closeSourcePanel() {

    sourcePanel.classList.remove(
        "open"
    );

    panelOverlay.classList.remove(
        "open"
    );

    selectedSource =
        null;
}


closePanel.addEventListener(
    "click",
    closeSourcePanel
);


panelOverlay.addEventListener(
    "click",
    closeSourcePanel
);


// ============================================================
// ASK AI ABOUT SOURCE
// ============================================================

panelAskButton.addEventListener(
    "click",
    async () => {

        if (!selectedSource) {
            return;
        }


        const question =
            prompt(
                "What would you like to ask about this source?"
            );


        if (
            !question ||
            !question.trim()
        ) {
            return;
        }


        panelAskButton.disabled =
            true;

        panelAskButton.textContent =
            "Analyzing...";


        try {

            const response =
                await fetch(
                    `${API_URL}/api/source/ask`,
                    {
                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body:
                            JSON.stringify({
                                question:
                                    question.trim(),

                                source:
                                    selectedSource
                            })
                    }
                );


            const data =
                await response.json();


            if (!response.ok) {

                throw new Error(
                    data.detail ||
                    "AI request failed."
                );
            }


            displayAnswer(
                data.answer
            );


            closeSourcePanel();


            window.scrollTo({
                top: 0,
                behavior: "smooth"
            });


        } catch (error) {

            showToast(
                error.message
            );


        } finally {

            panelAskButton.disabled =
                false;

            panelAskButton.textContent =
                "Ask AI about this source";
        }
    }
);


// ============================================================
// HISTORY
// ============================================================

async function loadHistory() {

    hero.classList.add(
        "hidden"
    );

    resultsSection.classList.add(
        "hidden"
    );

    historySection.classList.remove(
        "hidden"
    );


    try {

        const response =
            await fetch(
                `${API_URL}/api/history`
            );


        const data =
            await response.json();


        historyContainer.innerHTML =
            "";


        if (
            !data.history ||
            data.history.length === 0
        ) {

            historyContainer.innerHTML = `
                <p style="color:#737b86">
                    No searches yet.
                </p>
            `;

            return;
        }


        data.history.forEach(
            item => {

                const element =
                    document.createElement(
                        "div"
                    );


                element.className =
                    "history-item";


                element.innerHTML = `
                    <div class="history-query">
                        ${escapeHtml(
                            item.query
                        )}
                    </div>

                    <div class="history-date">
                        ${escapeHtml(
                            item.date
                        )}
                    </div>
                `;


                element.addEventListener(
                    "click",
                    () => {

                        performSearch(
                            item.query
                        );

                    }
                );


                historyContainer.appendChild(
                    element
                );
            }
        );


    } catch (error) {

        historyContainer.innerHTML = `
            <p style="color:#ef6b73">
                ${escapeHtml(
                    error.message
                )}
            </p>
        `;
    }
}


// ============================================================
// CLEAR HISTORY
// ============================================================

async function clearHistory() {

    if (
        !confirm(
            "Clear all search history?"
        )
    ) {
        return;
    }


    try {

        const response =
            await fetch(
                `${API_URL}/api/history`,
                {
                    method: "DELETE"
                }
            );


        if (!response.ok) {
            throw new Error(
                "Could not clear history."
            );
        }


        showToast(
            "Search history cleared."
        );


        loadHistory();


    } catch (error) {

        showToast(
            error.message
        );
    }
}


// ============================================================
// HOME
// ============================================================

homeButton.addEventListener(
    "click",
    event => {

        event.preventDefault();

        resultsSection.classList.add(
            "hidden"
        );

        historySection.classList.add(
            "hidden"
        );

        hero.classList.remove(
            "hidden"
        );

        searchInput.focus();
    }
);


// ============================================================
// FORMS
// ============================================================

searchForm.addEventListener(
    "submit",
    event => {

        event.preventDefault();

        performSearch(
            searchInput.value
        );
    }
);


searchAgainForm.addEventListener(
    "submit",
    event => {

        event.preventDefault();

        performSearch(
            searchAgainInput.value
        );
    }
);


// ============================================================
// HISTORY EVENTS
// ============================================================

historyButton.addEventListener(
    "click",
    loadHistory
);


clearHistoryButton.addEventListener(
    "click",
    clearHistory
);


// ============================================================
// SUGGESTIONS
// ============================================================

document
    .querySelectorAll(
        ".suggestions button"
    )
    .forEach(
        button => {

            button.addEventListener(
                "click",
                () => {

                    const query =
                        button.dataset.query;


                    searchInput.value =
                        query;


                    performSearch(
                        query
                    );
                }
            );
        }
    );


// ============================================================
// KEYBOARD SHORTCUTS
// ============================================================

document.addEventListener(
    "keydown",
    event => {

        // Escape closes source panel

        if (
            event.key === "Escape"
        ) {

            closeSourcePanel();
        }


        // Ctrl + K focuses search

        if (
            (event.ctrlKey ||
                event.metaKey) &&
            event.key.toLowerCase() === "k"
        ) {

            event.preventDefault();

            searchInput.focus();
        }
    }
);


// ============================================================
// HELPERS
// ============================================================

function markdownSource(content) {

    try {

        return marked.parse(
            escapeHtml(content)
        );

    } catch {

        return escapeHtml(
            content
        );
    }
}


function displayError(message) {

    answerContainer.innerHTML = `
        <div class="answer-card">

            <div class="answer-heading">

                <div class="ai-icon">
                    !
                </div>

                <div class="answer-title">
                    SOMETHING WENT WRONG
                </div>

            </div>

            <div class="answer-text">
                ${escapeHtml(message)}
            </div>

        </div>
    `;
}


function showToast(message) {

    toast.textContent =
        message;

    toast.classList.add(
        "show"
    );


    setTimeout(
        () => {

            toast.classList.remove(
                "show"
            );

        },
        3000
    );
}


function escapeHtml(value) {

    const element =
        document.createElement(
            "div"
        );


    element.textContent =
        value ?? "";


    return element.innerHTML;
}


function escapeAttribute(value) {

    return String(
        value ?? ""
    )
        .replaceAll("&", "&amp;")
        .replaceAll('"', "&quot;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;");
}