document.addEventListener('DOMContentLoaded', function () {
    const sidebar = document.querySelector('.sidebar');
    const content = document.querySelector('.content');
    const toggleBtn = document.getElementById('toggleSidebar');

    function updateArrowDirection() {
        if (sidebar.classList.contains('collapsed')) {
            toggleBtn.classList.add('rotated');
        } else {
            toggleBtn.classList.remove('rotated');
        }
    }

    toggleBtn.addEventListener('click', function () {
        sidebar.classList.toggle('collapsed');
        content.classList.toggle('expanded');
        updateArrowDirection();

        toggleBtn.classList.add('bounce');
        setTimeout(() => {
            toggleBtn.classList.remove('bounce');
        }, 300);
    });

    setTimeout(() => {
        updateArrowDirection();
    }, 30);
});



