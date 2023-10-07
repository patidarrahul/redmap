function createButton(value) {
    // Check if a button for this value already exists

    if (selectedValues.includes(value)) {
      return;
    }

    const newButton = document.createElement("button");
    const selectedOption = dropdown.options[dropdown.selectedIndex];

    // Add Bootstrap class for styling
    newButton.className = "btn btn-outline-secondary mb-0 "; // Add your desired Bootstrap classes here

    // Set the button's text content to the value
    newButton.textContent = selectedOption.textContent;

    // Add a data attribute to store the value
    newButton.setAttribute("data-value", value);

    // Add the value to the hidden input field's value

    selectedValuesInput.value += (selectedValuesInput.value ? "," : "") + value;

    // Add the value to the selectedValues array
    selectedValues.push(value);

    // Append the new button to the button container
    layerContainer.insertBefore(newButton, layerContainer.firstChild);
    // dropdown.selectedIndex = 0;
  }


  function removeButton(button) {
    const valueToRemove = button.getAttribute("data-value");
    layerContainer.removeChild(button);

    // Remove the value from the hidden input field's value

    const valuesArray = selectedValuesInput.value.split(",");
    const updatedValues = valuesArray.filter(
      (val) => val.trim() !== valueToRemove
    );

    selectedValuesInput.value = updatedValues.join(",");

    // Remove the value from the selectedValues array
    const indexToRemove = selectedValues.indexOf(valueToRemove);
    if (indexToRemove !== -1) {
      selectedValues.splice(indexToRemove, 1);
    }
  }

    // Get a reference to the div element
    var myDiv = document.getElementById("stack");

    // Change the class when the page loads
    myDiv.classList.add("active");


    $(document).ready(function () {
      // Handle update buttons
      $("#update-selected").click(function () {
        const selectedId = $('input[name="selected_stack"]:checked').val();
  
        const stack_list = "{{ stack_list }}";

  
        if (selectedId) {
          window.location.href = "/stack/update/" + selectedId;
        }
      });
      // Handle mark as complete buttons
      $("#mark-as-complete").click(function () {
        const selectedId = $('input[name="selected_stack"]:checked').val();
        if (selectedId) {
          window.location.href = "/inventory/status/" + selectedId;
        }
      });
    });




    const substrateDropdown = document.getElementById("substrate");
    const deviceStackContainer = document.getElementById("deviceStack");
    substrateDropdown.addEventListener("change", function () {
      // Get the selected value from the dropdown
      const selectedValue = substrateDropdown.value;
    
      const selectedOption = substrateDropdown.options[substrateDropdown.selectedIndex];
    
      // Create a new button with Bootstrap styling
      const newSubstrateButton = document.createElement("button");
      newSubstrateButton.className =
        " btn btn-outline-secondary d-flex justify-content-center mx-auto";
    
      // Set the button's text content to the value
      newSubstrateButton.textContent = selectedOption.textContent;
    
      // Append the button to a container in the DOM (e.g., deviceStackContainer)
      // deviceStackContainer.appendChild(newSubstrateButton);
      deviceStackContainer.insertBefore(newSubstrateButton, deviceStackContainer.firstChild);
    });
    
    // ------------------------------for add stack file ----------------------
    
    
    
    // Get the dropdown element, button container, and hidden input field the id is defined in the forms.py
      const dropdown = document.getElementById("layers");
      const layerContainer = document.getElementById("layerContainer");
      const selectedValuesInput = document.getElementById("selectedValues");
    
      const selectedValues = [];
    
      // Maintain a list of selected values
      if (selectedValuesInput.value) {
        // Split the comma-separated string into an array
        const selectedValuesArray = selectedValuesInput.value.split(",");
        selectedValues.push(...selectedValuesArray);
    
        // Now, selectedValues contains the values as an array
     
      }
    
      // Add an event listener to the dropdown
      dropdown.addEventListener("change", function () {
        // Get the selected value from the dropdown
        const selectedValue = dropdown.value;
    
        // Create a new button with Bootstrap styling
        createButton(selectedValue);
      });
    
      // Add an event listener to remove buttons when clicked
      layerContainer.addEventListener("click", function (event) {
        if (event.target && event.target.tagName === "BUTTON") {
          const button = event.target;
          removeButton(button);
        }
      });