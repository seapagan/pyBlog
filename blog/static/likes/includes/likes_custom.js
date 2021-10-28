if (typeof $ != "undefined") {
  $(document).ready(function () {
    $(document).on("click", "a.liker", function (event) {
      event.preventDefault();
      var el = $(this);
      var replace_selector = el.attr("replace_selector");
      if (!replace_selector) var replace_target = el.parents(".likes:first");
      else var replace_target = $(replace_selector);
      $.get(el.attr("href"), {}, function (data) {
        replace_target.html(data);

        // now update the like count that is displayed on the page
        const like_count = $(data).filter("#like_count").text();
        $("#total").html(like_count);
      });
    });
  });
}
