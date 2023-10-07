
  $(document).ready(function () {
    // Handle update buttons
    $("#update-selected").click(function () {
      const selectedId = $('input[name="selected_inventory"]:checked').val();
      console.log(selectedId);

      if (selectedId) {
        window.location.href = "/inventory/update/" + selectedId;
      }
    });
    // Handle mark as complete buttons
    $("#mark-as-complete").click(function () {
      const selectedId = $('input[name="selected_inventory"]:checked').val();
      if (selectedId) {
        window.location.href = "/inventory/status/" + selectedId;
      }
    });
  });

      /*===== LINK ACTIVE =====*/
  // Get a reference to the div element
  var myDiv = document.getElementById("inventory");

  // Change the class when the page loads
  myDiv.classList.add("active");
