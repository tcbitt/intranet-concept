function toggleArchive() {
    const section = document.getElementById('archived-section');
    if (section) {
        section.style.display = section.style.display === 'none' ? 'block' : 'none';
    }
}
