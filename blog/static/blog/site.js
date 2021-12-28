// Some custom JS needed for the blog

// sort out the CKEditor sizing to fit the supplied space.
let attr = document.querySelector(".django-ckeditor-widget");
if (attr) {
  attr.removeAttribute("style");
}
