// Some custom JS needed for the blog

// sort out the CKEditor sizing to fit the supplied space.
let attr = document.querySelector(".django-ckeditor-widget");
if (attr) {
  attr.removeAttribute("style");
}

// set up Google analytics
window.dataLayer = window.dataLayer || [];
function gtag() {
  dataLayer.push(arguments);
}

const ga_key = document.getElementById("ga").textContent;

gtag("js", new Date());
gtag("config", ga_key);
