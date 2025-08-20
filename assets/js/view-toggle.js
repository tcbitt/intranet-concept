document.addEventListener('DOMContentLoaded', function () {
    const toggleBtn = document.getElementById('toggleView');
    const cardView = document.getElementById('cardView');
    const listView = document.getElementById('listView');

    if (!toggleBtn || !cardView || !listView) return;

    let isListView = localStorage.getItem('assetView') === 'list';

    function applyView() {
        cardView.classList.toggle('hidden', isListView);
        listView.classList.toggle('hidden', !isListView);
        toggleBtn.textContent = isListView ? 'Switch to Card View' : 'Switch to List View';
        localStorage.setItem('assetView', isListView ? 'list' : 'card');
    }

    applyView();

    toggleBtn.addEventListener('click', function () {
        isListView = !isListView;
        applyView();
    });
});
