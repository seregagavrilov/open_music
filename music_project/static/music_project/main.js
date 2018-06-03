function initilizeEventHandlers() {

  var $ = window.jQuery;

  $('.songs-btn').on('click', function(event) {
    $.ajax({
      type: "GET",
      url: 'http://127.0.0.1:8000/library_api/api_v1/usersongs/',
      success: function(serverResponse) {

        var discription = $('.table-discription-header');
        discription.text('My songs');

        var discriptionBody = $('.table-discription-body');
        discriptionBody.text('');

        var body = $('#table-body');

        body.empty();

        var rowNumber = 1;
        $.each(serverResponse, function(index) {
          var tableRow = $('<tr></tr>');
          tableRow.addClass('row')
          var index = index.toString();
          var name = serverResponse[index].name
          var th = $('<th></th>', {
            scope: 'row',
          })


          var playCell = $('<td></td>')
            .height(20)
            .width(20);
          var playImg = $("<img>");
          playImg.attr("src", "/static/music_project/playericon/play-button.png")
            .height(20)
            .width(20);
          playCell.append(playImg);
          tableRow.append(playCell);
          var nameCell = $('<td></td>')
          nameCell.append(name);
          tableRow.append(th);
          tableRow.append(nameCell);
          body.append(tableRow)

          rowNumber++;

        })
      }
    });
  })

  $('.artists-btn').on('click', function(event) {
    $.ajax({
      type: "GET",
      url: 'http://127.0.0.1:8000/library_api/api_v1/userartists/',
      success: function(serverResponse) {

        var discription = $('.table-discription-header');
        discription.text('My artists');

        var discriptionBody = $('.table-discription-body');
        discriptionBody.text('');

        var body = $('#table-body');

        body.empty();

        var rowNumber = 1;
        $.each(serverResponse, function(index) {

          var artist = {
            name: serverResponse[index].name
          };

          var tableRow = $('<tr></tr>', {
            artistId: serverResponse[index].id,
            artistName: serverResponse[index].name,
            artistBio: serverResponse[index].bio
          });
          tableRow.addClass('row')
          tableRow.on('click', function(event) {
            var currentElement = event.currentTarget;
            var artist = {
              name: currentElement.getAttribute('artistName'),
              id: currentElement.getAttribute('artistId'),
              bio: currentElement.getAttribute('artistBio')

            };
            artistView(artist);
          });

          var index = index.toString();
          var name = serverResponse[index].name
          var th = $('<th></th>', {
            scope: 'row',
          })

          th.append(rowNumber);
          var nameCell = $('<td></td>')
          nameCell.append(name);
          tableRow.append(th);
          tableRow.append(nameCell);
          body.append(tableRow)

          rowNumber++;

        })
      }
    });
  })

  $('.albums-btn').on('click', function(event) {
    $.ajax({
      type: "GET",
      url: 'http://127.0.0.1:8000/library_api/api_v1/useralbums/',
      success: function(serverResponse) {

        var discription = $('.table-discription-header');
        discription.text('My albums');

        var discriptionBody = $('.table-discription-body');
        discriptionBody.text('');

        var body = $('#table-body');

        body.empty();

        var rowNumber = 1;
        $.each(serverResponse, function(index) {
          var tableRow = $('<tr></tr>');
          tableRow.addClass('row')
          var index = index.toString();
          var name = serverResponse[index].name
          var year = serverResponse[index].year
          var th = $('<th></th>', {
            scope: 'row',
          })


          th.append(rowNumber);
          var nameCell = $('<td></td>')
          nameCell.append(name);
          var yearCell = $('<td></td>');
          yearCell.append(year)
          tableRow.append(th);
          tableRow.append(nameCell);
          tableRow.append(yearCell)
          body.append(tableRow)

          rowNumber++;

        })
      }
    });
  })

  audiojs.events.ready(function() {
    var as = audiojs.createAll();
  });

}

function artistView(artist) {
  var discription = $('.table-discription-header');
  discription.text(artist.name);

  var discriptionBody = $('.table-discription-body');
  discriptionBody.text('');

  var body = $('#table-body');

  body.empty();

}

function albumsView(album) {

}




initilizeEventHandlers();
