document.addEventListener("DOMContentLoaded", function () {
  // get csrf token
  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
      const cookies = document.cookie.split(";");
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === name + "=") {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }

  const csrftoken = getCookie("csrftoken");

  // Add event listeners to all task checkboxes
  document.querySelectorAll(".task-checkbox").forEach(function (checkbox) {
    checkbox.addEventListener("change", function () {
      const taskId = this.getAttribute("data-task-id");
      const isChecked = this.checked;
      const taskCard = this.closest(".card");

      // Disable checkbox during request
      this.disabled = true;

      // Make AJAX request
      fetch(`/tasks/toggle/${taskId}/`, {
        method: "POST",
        headers: {
          "X-Requested-With": "XMLHttpRequest",
          "X-CSRFToken": csrftoken,
          "Content-Type": "application/json",
        },
        credentials: "same-origin",
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.success) {
            // remove the task card from the DOM
            taskCard.remove();

            // if there are no more tasks show empty state
            const remainingTasks = document.querySelectorAll(".card");
            if (remainingTasks.length === 0) {
              showEmptyState();
            }
          } else {
            // revert checkbox state on error
            this.checked = !isChecked;
          }
        })
        .catch((error) => {
          console.error("Error:", error);
          this.checked = !isChecked;
        })
        .finally(() => {
          // re-enable checkbox after operation
          this.disabled = false;
        });
    });
  });

  // function to show empty state
  function showEmptyState() {
    const container = document.querySelector(".container");
    const emptyStateHTML = `
      <div class="text-center py-5" id="empty-state">
        <i class="bi bi-inbox display-1 text-muted"></i>
        <h3 class="mt-3 text-muted">No tasks found</h3>
        <a href="/tasks/create/" class="btn btn-dark btn-lg">
          <i class="bi bi-plus-circle"></i> Create Your First Task
        </a>
      </div>
    `;

    // insert the empty state section (after the header section)
    const headerSection = container.querySelector(".row.mb-4");
    if (headerSection) {
      headerSection.insertAdjacentHTML("afterend", emptyStateHTML);
    }
  }
});
