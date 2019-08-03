function getCookie(name) {
    var matches = document.cookie.match(new RegExp(
      "(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
    ))
    return matches ? decodeURIComponent(matches[1]) : undefined
};


var submitReview = function() {
    var formData = $('#review_form').serialize();
    var csrftoken = getCookie('csrftoken');
    var href = window.location.href.split('/')[4];
    var url = "/book/"+href+"/";

    var mass = $('#massage');

    fetch(url, {
          method: 'POST',
          body: formData,
          headers:{'Content-Type': 'application/x-www-form-urlencoded',
                   'X-CSRFToken': csrftoken,
                   'X-Requested-With': 'XMLHttpRequest'}
        }).then(response => response.json())
          .then(data => {
            console.log(data);
            mass.text(data['status']);
          })
          .catch(error => console.error('Error:', error))
    }
