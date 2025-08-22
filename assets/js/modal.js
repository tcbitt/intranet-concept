document.addEventListener("DOMContentLoaded", function () {
  const modalTriggers = document.querySelectorAll("[data-modal-target]");

  modalTriggers.forEach(trigger => {
    const modalId = trigger.getAttribute("data-modal-target");
    const modal = document.getElementById(modalId);
    const closeBtn = modal.querySelector(".close");

    trigger.onclick = () => {
      modal.style.display = "block";

      // Handle delete modal dynamic content
      if (modalId === "deleteModal") {
        const docId = trigger.getAttribute("data-doc-id");
        const docTitle = trigger.getAttribute("data-doc-title");
        const message = modal.querySelector("#deleteModalMessage");
        const form = modal.querySelector("#deleteForm");

        message.textContent = `Are you sure you want to delete "${docTitle}"?`;
        form.action = `/documents/${docId}/delete/`;
      }
    };

    closeBtn.onclick = () => modal.style.display = "none";
    window.onclick = (event) => {
      if (event.target === modal) {
        modal.style.display = "none";
      }
    };
  });
});
