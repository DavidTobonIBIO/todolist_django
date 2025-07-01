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

  //  event listeners to all task checkboxes
  document.querySelectorAll(".task-checkbox").forEach(function (checkbox) {
    checkbox.addEventListener("change", function () {
      const taskId = this.getAttribute("data-task-id");
      const isChecked = this.checked;
      const taskCard = this.closest(".card");

      // disable checkbox during request
      this.disabled = true;

      // AJAX request
      fetch(`/tasks/toggle/${taskId}/`, {
        method: "POST",
        headers: {
          "X-Requested-With": "XMLHttpRequest",
          "X-CSRFToken": csrftoken,
          "Content-Type": "application/json",
        },
        credentials: "same-origin",
      })
      // remove task on succes or revert checkbox state on error
        .then((response) => response.json())
        .then((data) => {
          if (data.success) {
            taskCard.remove();
          } else {
            this.checked = !isChecked;
          }
        })
        .catch((error) => {
          console.error("Error:", error);
          this.checked = !isChecked;
        })
        .finally(() => {
          this.disabled = false; // enable checkbox again
        });
    });
  });
});
