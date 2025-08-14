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
});
