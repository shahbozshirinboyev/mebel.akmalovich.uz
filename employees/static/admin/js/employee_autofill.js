document.addEventListener("DOMContentLoaded", function () {
  const userSelect = document.getElementById("id_user");
  const fullNameInput = document.getElementById("id_full_name");

  if (!userSelect || !fullNameInput) return;

  function fetchFullName(userId) {
    if (!userId) {
      fullNameInput.value = "";
      return;
    }
    fetch(`/admin/get-user-full-name/?user_id=${userId}`)
      .then((response) => response.json())
      .then((data) => {
        if (data && data.full_name !== undefined) {
          fullNameInput.value = data.full_name;
        }
      })
      .catch(() => {
        // silently ignore failures
      });
  }

  // If a user is already selected on form load, fetch and set full_name
  if (userSelect.value) {
    fetchFullName(userSelect.value);
  }

  userSelect.addEventListener("change", function () {
    fetchFullName(this.value);
  });
});
