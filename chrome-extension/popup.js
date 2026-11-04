
const button = document.getElementById("scan");
const statusElement = document.getElementById("status");
const chart = document.getElementById("chart");
const filter = document.getElementById("filter");
const list = document.getElementById("comments");
const themeButton = document.getElementById("theme");
const copyButton = document.getElementById("copy");
const exportButton = document.getElementById("export");

let statistics = null;
let results = [];

const sentiments = ["positive", "neutral", "negative"];

function renderChart(percentages) {
    chart.replaceChildren();

    sentiments.forEach(sentiment => {
        const value = Number(percentages[sentiment]) || 0;

        const row = document.createElement("div");
        row.className = "bar-row";

        const label = document.createElement("div");
        label.className = "bar-label";

        const name = document.createElement("span");
        name.textContent = sentiment.toUpperCase();

        const percent = document.createElement("span");
        percent.textContent = `${value}%`;

        label.append(name, percent);

        const background = document.createElement("div");
        background.className = "bar-bg";

        const bar = document.createElement("div");
        bar.className = `bar ${sentiment}`;
        bar.style.width = `${Math.max(0, Math.min(100, value))}%`;

        background.appendChild(bar);
        row.append(label, background);
        chart.appendChild(row);
    });
}

function renderComments() {
    list.replaceChildren();

    const selected = filter.value;

    const filtered = selected === "all"
        ? results
        : results.filter(r => r.sentiment === selected);

    filtered.forEach(result => {
        const card = document.createElement("div");
        card.className = "comment";

        const label = document.createElement("strong");
        label.className = `${result.sentiment}-text`;

        const confidence = (result.confidence * 100).toFixed(1);

        label.textContent =
            `${result.sentiment.toUpperCase()} · ${confidence}%`;

        const text = document.createElement("p");
        text.textContent = result.comment;

        card.append(label, text);
        list.appendChild(card);
    });
}

filter.addEventListener("change", renderComments);


// Dark mode
function applyTheme(dark) {
    document.body.classList.toggle("dark", dark);
    themeButton.textContent = dark ? "Light Mode" : "Dark Mode";
}

chrome.storage.local.get({ darkMode: false }).then(settings => {
    applyTheme(settings.darkMode);
});

themeButton.addEventListener("click", async () => {
    const dark = !document.body.classList.contains("dark");
    applyTheme(dark);
    await chrome.storage.local.set({ darkMode: dark });
});

// Copy results
copyButton.addEventListener("click", async () => {
    if (!statistics || !results.length) return;

    const lines = [
        `Analyzed ${statistics.total} comments`,
        ...sentiments.map(s =>
            `${s}: ${statistics.percentages[s]}%`
        ),
        "",
        ...results.map(r =>
            `[${r.sentiment.toUpperCase()}] ` +
            `${(r.confidence * 100).toFixed(1)}% - ${r.comment}`
        )
    ];

    try {
        await navigator.clipboard.writeText(lines.join("\n"));
        statusElement.textContent = "Results copied!";
    } catch (error) {
        statusElement.textContent = `Copy failed: ${error.message}`;
    }
});

// Export CSV
exportButton.addEventListener("click", () => {
    if (!results.length) return;

    const escapeCSV = value =>
        `"${String(value).replaceAll('"', '""')}"`;

    const rows = [
        ["comment", "sentiment", "confidence"],
        ...results.map(r => [
            r.comment,
            r.sentiment,
            r.confidence
        ])
    ];

    const csv = rows
        .map(row => row.map(escapeCSV).join(","))
        .join("\r\n");

    const blob = new Blob(["\uFEFF" + csv], {
        type: "text/csv;charset=utf-8"
    });

    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");

    link.href = url;
    link.download = "youtube_sentiment_results.csv";
    link.click();

    setTimeout(() => URL.revokeObjectURL(url), 3000);
});


button.addEventListener("click", async () => {
    button.disabled = true;
    filter.disabled = true;
    statusElement.textContent = "Analyzing...";
    chart.replaceChildren();
    list.replaceChildren();
    results = [];
    statistics = null;
    copyButton.disabled = true;
    exportButton.disabled = true;

    try {
        const [tab] = await chrome.tabs.query({
            active: true,
            currentWindow: true
        });

        if (!tab?.id || !tab.url?.startsWith(
            "https://www.youtube.com/watch"
        )) {
            throw new Error("Open a YouTube video first.");
        }

        const [{ result: comments }] =
            await chrome.scripting.executeScript({
                target: { tabId: tab.id },
                func: () => {
                    const nodes = document.querySelectorAll(
                        "ytd-comment-thread-renderer #content-text, " +
                        "ytd-comment-view-model #content-text, " +
                        "ytd-comment-renderer #content-text"
                    );

                    return [...new Set(
                        [...nodes]
                            .filter(el => el.getClientRects().length > 0)
                            .map(el => el.innerText.trim())
                            .filter(Boolean)
                    )];
                }
            });

        if (!comments.length) {
            throw new Error("No comments found. Scroll down and retry.");
        }

        const response = await fetch(
            "http://127.0.0.1:7860/predict_batch",
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ comments })
            }
        );

        if (!response.ok) {
            throw new Error(`API error: ${response.status}`);
        }

        const data = await response.json();

        results = data.results;
        statistics = data.statistics;
        copyButton.disabled = false;
        exportButton.disabled = false;

        statusElement.textContent =
            `Analyzed ${data.statistics.total} comments`;

        renderChart(data.statistics.percentages);

        filter.value = "all";
        filter.disabled = false;

        renderComments();

    } catch (error) {
        statusElement.textContent = `Error: ${error.message}`;
    } finally {
        button.disabled = false;
    }
});
