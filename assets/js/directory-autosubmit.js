/*
document.addEventListener('DOMContentLoaded', () => {
    const input = document.querySelector('input[name="search"]');
    const resultsContainer = document.querySelector('#widget-results');

    let timeout = null;

    input.addEventListener('input', () => {
        clearTimeout(timeout);
        timeout = setTimeout(() => {
            const query = input.value;
            const url = new URL(window.location.href);
            url.searchParams.set('search', query);
            url.searchParams.set('page', 1);

            fetch(url, {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => response.json())
            .then(data => {
                resultsContainer.innerHTML = data.html;
            });
        }, 150);
    });
    resultsContainer.addEventListener('click', (e) => {
        const link = e.target.closest('a');
        if (link && link.closest('.pagination')) {
            e.preventDefault();
            fetchResults(link.href);
        }
    });
});
*/
document.addEventListener('DOMContentLoaded', () => {
    const input = document.querySelector('input[name="search"]');
    const resultsContainer = document.querySelector('#widget-results');
    const viewKey = 'assetView';
    let timeout = null;

    function applyViewState() {
        const savedView = localStorage.getItem(viewKey);
        const cardView = document.getElementById('cardView');
        const listView = document.getElementById('listView');
        const toggleBtn = document.getElementById('toggleView');

        if (!cardView || !listView || !toggleBtn) return;

        const isListView = savedView === 'list';
        cardView.classList.toggle('hidden', isListView);
        listView.classList.toggle('hidden', !isListView);
        toggleBtn.textContent = isListView ? 'Switch to Card View' : 'Switch to List View';

        // Rebind toggle click
        toggleBtn.onclick = () => {
            const newIsListView = !cardView.classList.contains('hidden');
            localStorage.setItem(viewKey, newIsListView ? 'list' : 'card');
            applyViewState();
        };
    }

    function fetchResults(url) {
        fetch(url, {
            headers: { 'X-Requested-With': 'XMLHttpRequest' }
        })
        .then(response => response.json())
        .then(data => {
            resultsContainer.innerHTML = data.html;
            applyViewState();
        });
    }

    if (input && resultsContainer) {
        input.addEventListener('input', () => {
            clearTimeout(timeout);
            timeout = setTimeout(() => {
                const query = input.value;
                const url = new URL(window.location.href);
                url.searchParams.set('search', query);
                url.searchParams.set('page', 1);
                fetchResults(url);
            }, 150);
        });

        resultsContainer.addEventListener('click', (e) => {
            const link = e.target.closest('a');
            if (link && link.closest('.pagination')) {
                e.preventDefault();
                fetchResults(link.href);
            }
        });
    }

    applyViewState();
});
