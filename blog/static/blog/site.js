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

const ga_id = document.getElementById("ga");
if (ga_id) {
  const ga_data = JSON.parse(ga_id.textContent);
  if (ga_data.enabled) {
    console.log(ga_data);
    gtag("js", new Date());
    gtag("config", ga_data.key);
  }
}
