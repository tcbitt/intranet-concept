document.addEventListener('DOMContentLoaded', function () {
    const toggleBtn = document.getElementById('toggleView');
    const cardView = document.getElementById('cardView');
    const listView = document.getElementById('listView');

    if (!toggleBtn || !cardView || !listView) return;

    let currentView = localStorage.getItem('assetView') || 'list';

    if (currentView === 'card') {
        cardView.classList.remove('hidden');
        listView.classList.add('hidden');
        toggleBtn.textContent = 'Switch to List View';
    } else {
        cardView.classList.add('hidden');
        listView.classList.remove('hidden');
        toggleBtn.textContent = 'Switch to Card View';
    }

    toggleBtn.addEventListener('click', function () {
        if (currentView === 'card') {
            currentView = 'list';
            cardView.classList.add('hidden');
            listView.classList.remove('hidden');
            toggleBtn.textContent = 'Switch to Card View';
        } else {
            currentView = 'card';
            cardView.classList.remove('hidden');
            listView.classList.add('hidden');
            toggleBtn.textContent = 'Switch to List View';
        }
        localStorage.setItem('assetView', currentView);
    });
});
