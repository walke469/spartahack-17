// COOKIE HANDLING AND ALSO PARSING HTML

$(function () {
    $.ajax({
      
        zipcode: '68640',
        zipurl: "https://congress.api.sunlightfoundation.com/districts/locate?zip=" + zipcode,
      
        lat: '42.96',
        long: '-108.09',
        llurl: "https://congress.api.sunlightfoundation.com/districts/locate?latitude=" + lat + "&longitude=" + long,
        dataType: "html",
        success: function (data) {
            $('#word-wrap: break-word; white-space: pre-wrap;').text(data);
            $('#wtf').html($(data).text());
        },

        obj: JSON.parse(data),
        
    });
    
    var cnt = obj.results.count;
    alert(cnt);
    
    for (i = 0; i < cnt; i++) {
      
        document.cookie = "state =" + obj.results[cnt].state + "; district =" + obj.results[cnt].district;
        
    }
    
});