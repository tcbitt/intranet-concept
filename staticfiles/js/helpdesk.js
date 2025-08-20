function toggleSection(id, button) {
    const section = document.getElementById(id);
    if (section) {
        const isHidden = section.style.display === 'none';
        section.style.display = isHidden ? 'block' : 'none';
        if (button) {
            button.textContent = isHidden ? 'Hide' : 'Show';
        }
    }
}
