const toggler = document.querySelector(".toggler-btn");
toggler.addEventListener("click", function () {
  document.querySelector("#sidebar").classList.toggle("collapsed");
});


document.addEventListener("DOMContentLoaded", function () {
  const sidebar = document.querySelector(".sidebar");
  const overlay = document.createElement("div");
  overlay.classList.add("overlay");
  document.body.appendChild(overlay);

  document.querySelector("#toggleSidebar").addEventListener("click", function () {
      sidebar.classList.toggle("active");
      overlay.classList.toggle("show");
  });

  overlay.addEventListener("click", function () {
      sidebar.classList.remove("active");
      overlay.classList.remove("show");
  });
});