// Get the form and message elements by their IDs
const form = document.getElementById("myForm");
const formMessage = document.getElementById("formMessage");

if (form) {
  form.addEventListener("submit", function(e) {
    e.preventDefault(); 
    const name = document.getElementById("fname")?.value;
    const email = document.getElementById("email")?.value;

    if (!name || !email) {
      formMessage.textContent = "Please fill out all fields.";
      formMessage.className = "message error";
      return;
    }

    formMessage.textContent = "Thank you! Your trip idea has been saved.";
    formMessage.className = "message success";
    form.reset(); // reset the form
  });
}