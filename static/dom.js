var app = app || {};

// this object contains the functions which create
// and remove dom elements
app.dom = {

    showBoards: function() {
        // shows #boards div and hides #cards
        $('#boards').fadeIn(500);
        $('#create-new-board').fadeIn(500);
        $('#settings-button').fadeIn(500);
        $('#cards').hide();
        $('#create-new-card').hide();
        $('#back-to-root-toot').hide();
        $('#boards').empty();
        $('.detailed-board').empty();
        $('body').removeAttr("data-boardId");
        if ($('.detailed-board'))
            $('.detailed-board').hide();
        // using the boards data it creates the boards
        app.dataHandler.loadBoards(function() {
            var board_list = app.dataHandler.boards;
            if (board_list) {
                for (var i = 0; i < board_list.length; i++) {
                $('#boards').append("<div class='board_title col-xs-3 col-xs-offset-1 col-md-3 col-md-offset-1'>"+board_list[i].title+"<div class='board_id'>"+board_list[i].id+"</div></div>");
                }
            }
        });

    },


    showCards: function(boardId) {
        // shows #cards div and hides #boards
        $('#cards').empty();
        $('#cards').fadeIn(500);
        $('#back-to-root-toot').fadeIn(500);
        $('#create-new-card').fadeIn(500);
        $('#boards').hide();
        $('#create-new-board').hide();
        $('#settings-button').hide();
        $('.detailed-board').empty();
        $('.detailed-board').fadeIn(500);
        // using the boards data it creates the cards
        // on the page, appending them to #cards div
        var content = app.dataHandler.getBoard(boardId);
        
        $('.detailed-board').append("<div id='detailed-board-title'>"+content.title+"</div>");
        $('.detailed-board').append("<div id='detailed-board-state'>"+content.state+"</div>");
        $('.detailed-board').append("<div id='detailed-board-id'>"+content.id+"</div>");

        this.generateColumns($('#cards'));
        var cards = app.dataHandler.orderObject(app.dataHandler.getBoard(boardId).cards,'order','ASC');
        this.placeCards(cards);
    },

    mainListener: function() {
        $('#cards').on('click', '.card_title', function() {
            var boardId = $('#detailed-board-id').text();
            var cardId = $(this).next().text()
            var newCardContent = prompt($(this).text());
          
            if (newCardContent)
                app.dataHandler.editCard(boardId, cardId, 'title', newCardContent)
        });
        $('#boards').on('click', '.board_title', function() {
            app.dom.showCards($(this).children().text())
            });
        $('#back-to-root-toot').on('click', function(){
            app.dom.showBoards();
            });
        $('#settings-button').on('click', function(){
               if ($(this).text() === 'prod') {
                   $(this).text('dev');
                   app.dom.showBoards();
               } else if ($(this).text() === 'dev') {
                   $(this).text('prod');
                   app.dom.showBoards();
               }
            });
        $('#create-new-board').on('click', function(){
            var boardTitle = prompt('Please add a new board title');
            if (boardTitle) 
            {
                app.dataHandler.createNewBoard(boardTitle);
                app.dataHandler.saveBoards();
                app.dom.showBoards();
            }
        });
        $('#create-new-card').on('click', function(){
            var cardTitle = prompt('Please add a new card title');
            var boardId = $('#detailed-board-id').text();
            if (cardTitle) 
            {
                app.dataHandler.createNewCard(boardId, cardTitle);
                app.dataHandler.saveBoards();
                app.dom.showCards(boardId);
            }
        });
    },
    // here comes more features
    generateColumns: function(cards) {
        header = '<div class="row" id="columnNames">';
        header += '<div class="col-md-3 card-column"><h2>New</h2></div>';
        header += '<div class="col-md-3 card-column"><h2>In Progress</h2></div>';
        header += '<div class="col-md-3 card-column"><h2>Review</h2></div>';
        header += '<div class="col-md-3 card-column"><h2>Done</h2></div>';
        header += '</div>';

        cards.append(header);
        header = '<div class="container" id="columnNames"> </div>';
        cards.append('<div class="col-md-3 connectedSortable" id="status-new"></div>');
        cards.append('<div class="col-md-3 connectedSortable" id="status-inprogress"></div>');
        cards.append('<div class="col-md-3 connectedSortable" id="status-review"></div>');
        cards.append('<div class="col-md-3 connectedSortable" id="status-done"></div>');

        $( function() {
            $( "#status-new, #status-inprogress, #status-review, #status-done" ).sortable({
                connectWith: ".connectedSortable",
                opacity: 0.5,
                update: function(event, ui) {
                    var boardId = $('#detailed-board-id').html();
                    var child = $(ui.item.children('.card_id'));
                    var cardId = $(child).html();
                    var newStatus = event.target.id.substring("status-".length);
                    var newOrder = ui.item.index();
                    
                    app.dataHandler.editCard(boardId, cardId, "status", newStatus);    
                    app.dataHandler.editCard(boardId, cardId, "order", newOrder);
                }
            }).disableSelection();        
        }); 
    },

    placeCards: function(cards) {
        for (var i = 0; i < cards.length; i++) {
            var destinationElement;
            switch (cards[i].status) {
                case "new":
                    destinationElement = $('#status-new');
                    break;
                case "inprogress":
                    destinationElement = $('#status-inprogress'); 
                    break;
                case "review":
                    destinationElement = $('#status-review');
                    break;
                case "done":
                    destinationElement = $('#status-done');
                    break;
            }

            destinationElement.append("<div class='col-xs-3 col-md-3 col-lg-3 card draggable'><h4 class='card_title'>"+cards[i].title+"</h4><p class='card_id'>"+cards[i].id+"</p><p class='card_status'>"+cards[i].status+"</p><p>"+cards[i].order+"</p></div>");
            // $('.draggable').draggable();
        }
    }
}