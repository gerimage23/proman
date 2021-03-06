var app = app || {};

// this object contains the functions which create
// and remove dom elements
app.dom = {

    showBoards: function() {
        // shows #boards div and corresponding elements 
        // while hides #cards and not related elements
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
        // shows #cards div and corresponding elements 
        // while hides #boards and not related elements
        $('#cards').empty();
        $('#cards').fadeIn(500);
        $('#back-to-root-toot').fadeIn(500);
        $('#create-new-card').fadeIn(500);
        $('#boards').hide();
        $('#create-new-board').hide();
        $('#settings-button').hide();
        $('.detailed-board').empty();
        $('.detailed-board').fadeIn(500);
        // using the data from boards it creates the cards
        // on the page, appending them to #cards div
        app.dataHandler.loadBoards(function(){
            var content = app.dataHandler.getBoard(boardId);
            $('.detailed-board').append("<div id='detailed-board-title'>"+content.title+"</div>");
            $('.detailed-board').append("<div id='detailed-board-state'>"+content.state+"</div>");
            $('.detailed-board').append("<div id='detailed-board-id'>"+content.id+"</div>");
            app.dom.generateColumns($('#cards'));
            var cards = app.dataHandler.orderObject(app.dataHandler.getBoard(boardId).cards,'order','ASC');
            app.dom.placeCards(cards);
        });
    },

    mainListener: function() {
        // here we collect our listeners
        $('#cards').on('click', '.card_title', function() {
            // when a click arrives on a card title
            // this function handles the title change
            var boardId = $('#detailed-board-id').text();
            var cardId = $(this).next().text()
            var newCardContent = prompt($(this).text());
            if (newCardContent)
                app.dataHandler.editCard(boardId, cardId, 'title', newCardContent)
                app.dataHandler.saveBoards(function() {
                    app.dom.showCards(boardId);
                })
        });
        $('#boards').on('click', '.board_title', function() {
            // when a click arrives on a boards title
            // this functions renders using the corresponding cards
            app.dom.showCards($(this).children().text())
            });
        $('#back-to-root-toot').on('click', function(){
            // sending the user back to rooot
            app.dom.showBoards();
            });
        $('#create-new-board').on('click', function(){
            // creating new board
            var boardTitle = prompt('Please add a new board title');
            if (boardTitle) 
            {
                app.dataHandler.createNewBoard(boardTitle, function() {
                    app.dom.showBoards();
                });
            }
        });
        $('#create-new-card').on('click', function(){
            // creating new card
            var cardTitle = prompt('Please add a new card title');
            var boardId = $('#detailed-board-id').text();
            if (cardTitle) 
            {
                app.dataHandler.createNewCard(boardId, cardTitle, function() {
                    app.dom.showCards(boardId);
                });
            }
        });
    },
    generateColumns: function(cards) {
        // this functions creates the columns 
        // for holding the cards with matching state
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
                                       
                    // check each row
                    $("#status-new div").each(function(i, elm) {
                        $elm = $(elm); // cache the jquery object
                        $orderElement = $elm.children().last()
                        $orderElement.html($elm.index("#status-new div"));
                        cId = $elm.children('.card_id').text();
                        app.dataHandler.editCard(boardId, cId, "order", $elm.index("#status-new div"));
                    });
                    $("#status-inprogress div").each(function(i, elm) {
                        $elm = $(elm); // cache the jquery object
                        $orderElement = $elm.children().last()
                        $orderElement.html($elm.index("#status-inprogress div"));
                        cId = $elm.children('.card_id').text();
                        app.dataHandler.editCard(boardId, cId, "order", $elm.index("#status-inprogress div"));
                    });
                    $("#status-review div").each(function(i, elm) {
                        $elm = $(elm); // cache the jquery object
                        $orderElement = $elm.children().last()
                        $orderElement.html($elm.index("#status-review div"));
                        cId = $elm.children('.card_id').text();
                        app.dataHandler.editCard(boardId, cId, "order", $elm.index("#status-review div"));
                    });
                    $("#status-done div").each(function(i, elm) {
                        $elm = $(elm); // cache the jquery object
                        $orderElement = $elm.children().last()
                        $orderElement.html($elm.index("#status-done div"));
                        cId = $elm.children('.card_id').text();
                        app.dataHandler.editCard(boardId, cId, "order", $elm.index("#status-done div"));
                    });

                    // edit & save
                    app.dataHandler.editCard(boardId, cardId, "status", newStatus);   
                    app.dataHandler.saveBoards(function() {
                        console.log('Board saved succesfully.');
                    });
                }
            }).disableSelection();
        }); 
    },

    placeCards: function(cards) {
        // placing cards in the matching columns 
        // using the cards state for finding the relation between them
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

            destinationElement.append("<div class='col-xs-3 col-md-3 col-lg-3 card draggable' id='card_order' ><h4 class='card_title'>"+cards[i].title+"</h4><p class='card_id'>"+cards[i].id+"</p><p class='card_status'>"+cards[i].status+"</p><p class='card_order'>"+cards[i].order+"</p></div>");
        }
    }
}