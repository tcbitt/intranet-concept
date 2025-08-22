function setupAjaxPagination() {
    document.body.addEventListener("click", function (e) {
        const link = e.target.closest(".pagination-link");
        if (!link) return;

        e.preventDefault();
        const url = link.href;
        const sectionId = link.dataset.section;
        const section = document.querySelector(`#${sectionId} .ajax-content`);

        if (!section) return;

        fetch(url, {
            headers: { "X-Requested-With": "XMLHttpRequest" }
        })
        .then(res => res.text())
        .then(html => {
            const parser = new DOMParser();
            const doc = parser.parseFromString(html, "text/html");
            const newContent = doc.querySelector(`#${sectionId} .ajax-content`);
            if (newContent) {
                section.innerHTML = newContent.innerHTML;
                document.getElementById(sectionId).style.display = "block";
                document.getElementById(sectionId).scrollIntoView({ behavior: "smooth" });
            }
        })
        .catch(err => console.error("Pagination error:", err));
    });
}

document.addEventListener("DOMContentLoaded", setupAjaxPagination);

/*
Pagination linkage must follow this for reusability.
<a href="?page={{ num }}" class="pagination-link" data-section="section-id">Next</a>
*/