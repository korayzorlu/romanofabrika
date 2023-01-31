//mesajların otomatik kaybolması
$(document).ready(function() {
    // messages timeout for 10 sec
    console.log($(".headerTop"));
    setTimeout(function() {
        $('.headerTop').fadeOut('slow');
    }, 2000); // <-- time in milliseconds, 1000 =  1 sec
});

///////////////////////////////////HTMX////////////////////////////////
//htmx dialog gösterme
const addUpdateDataModal = new bootstrap.Modal(document.getElementById("addUpdateDataModal"))
htmx.on("htmx:afterSwap", (e) => {
  // Response targeting #dialog => show the modal
  if (e.detail.target.id == "addUpdateDataDialog") {
    addUpdateDataModal.show()
  }
})

//htmx dialog gizleme
htmx.on("htmx:beforeSwap", (e) => {
    // Empty response targeting #dialog => hide the modal
    if (e.detail.target.id == "addUpdateDataDialog" && !e.detail.xhr.response) {
      addUpdateDataModal.hide()
      e.detail.shouldSwap = false
      window.location.reload()
    }
  })

//htmx iptalden sonra içeriği temizleme
htmx.on("hidden.bs.modal", () => {
    document.getElementById("addUpdateDataDialog").innerHTML = "";
  })
///////////////////////////////////HTMX-END////////////////////////////////

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

