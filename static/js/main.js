

let btnMenu = document.querySelector("#btnmenu");
let btnMobileMenu = document.querySelector("#btnMobileeMenu");
let sidebarContainer = document.querySelector(".sidebarContainer");
let homeSection = document.querySelector(".home-section");
let navNav = document.querySelector(".home-section nav");
let sidebarv2 = document.querySelector(".sidebarv2");
let btnSearch = document.querySelector(".bx-search");

btnMenu.onclick = function(){
    sidebarv2.classList.toggle("active");
    sidebarContainer.classList.toggle("active");
    homeSection.classList.toggle("active");
    navNav.classList.toggle("active")
};
btnMobileMenu.onclick = function(){
    sidebarv2.classList.toggle("active");
    sidebarContainer.classList.toggle("active");
    homeSection.classList.toggle("active");
    navNav.classList.toggle("active")
};
btnSearch.onclick = function(){
    sidebarv2.classList.toggle("active");
};