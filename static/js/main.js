//mesajların otomatik kaybolması
$(document).ready(function() {
    // messages timeout for 10 sec
    console.log($(".headerTop"));
    setTimeout(function() {
        $('.headerTop').fadeOut('slow');
    }, 2000); // <-- time in milliseconds, 1000 =  1 sec
});

//htmx dialog gösterme
const addMaterialModal = new bootstrap.Modal(document.getElementById("addMaterialModal"))
const updateMaterialModal = new bootstrap.Modal(document.getElementById("updateMaterialModal"))
const addExpenseModal = new bootstrap.Modal(document.getElementById("addExpenseModal"))
const updateExpenseModal = new bootstrap.Modal(document.getElementById("updateExpenseModal"))
htmx.on("htmx:afterSwap", (e) => {
  // Response targeting #dialog => show the modal
  if (e.detail.target.id == "addMaterialDialog") {
    addMaterialModal.show()
  }
  if (e.detail.target.id == "updateMaterialDialog") {
    updateMaterialModal.show()
  }
  if (e.detail.target.id == "addExpenseDialog") {
    addExpenseModal.show()
  }
  if (e.detail.target.id == "updateExpenseDialog") {
    updateExpenseModal.show()
  }
})

//htmx dialog gizleme
htmx.on("htmx:beforeSwap", (e) => {
    // Empty response targeting #dialog => hide the modal
    if (e.detail.target.id == "addMaterialDialog" && !e.detail.xhr.response) {
      addMaterialModal.hide()
      e.detail.shouldSwap = false
      window.location.href = "/materials"
    }
    if (e.detail.target.id == "updateMaterialDialog" && !e.detail.xhr.response) {
        updateMaterialModal.hide()
        e.detail.shouldSwap = false
        window.location.href = "/materials"
      }
    if (e.detail.target.id == "addExpenseDialog" && !e.detail.xhr.response) {
      addExpenseModal.hide()
      e.detail.shouldSwap = false
      window.location.href = "/expenses"
    }
    if (e.detail.target.id == "updateExpenseDialog" && !e.detail.xhr.response) {
      updateExpenseModal.hide()
      e.detail.shouldSwap = false
      window.location.href = "/expenses"
    }
  })

//htmx iptalden sonra içeriği temizleme
htmx.on("hidden.bs.modal", () => {
    document.getElementById("addMaterialDialog").innerHTML = "";
    document.getElementById("updateMaterialDialog").innerHTML = "";
    document.getElementById("addExpenseDialog").innerHTML = "";
    document.getElementById("updateExpenseDialog").innerHTML = "";
  })

let btnMenu = $("#btnmenu");
let btnMobileMenu = document.querySelector("#btnMobileeMenu");
let sidebarContainer = document.querySelector(".sidebarContainer");
let homeSection = document.querySelector(".home-section");
let navNav = document.querySelector(".home-section nav");
let sidebarv2 = document.querySelector(".sidebarv2");
let btnSearch = document.querySelector(".bx-search");

btnMenu.click(function(){
    sidebarv2.classList.toggle("active");
    sidebarContainer.classList.toggle("active");
    homeSection.classList.toggle("active");
    navNav.classList.toggle("active")
});
btnMobileMenu.onclick = function(){
    sidebarv2.classList.toggle("active");
    sidebarContainer.classList.toggle("active");
    homeSection.classList.toggle("active");
    navNav.classList.toggle("active")
};
btnSearch.onclick = function(){
    sidebarv2.classList.toggle("active");
};

