var app = app || {};

// this object contains the functions which handle the data and its reading/writing
// feel free to extend and change to fit your needs
app.dataHandler = {
    boards: [], // it contains the boards and their cards
    loadBoards: function(callback) {
        // sends an AJAX request to a Flask endpoint and gets back
        // a JSON as response which contains all of the user related boards
        // than uses the JSON formated response to fill app.dataHandler.boards
        $.ajax({
            url: '/load_boards',
            type: 'GET',
            dataType: 'json',
            success: function(response) {
                app.dataHandler.boards = response.boards;
                callback();
            },
            error: function(error) {
                console.log(error); // If there is an error we log it on the console.
            }
        });
    },
    saveBoards: function(callback) {
        // sends an AJAX request to a Flask endpoint 
        // containing the data from all of the user related boards
        var dataObject = app.dataHandler.boards;
        $.ajax({
            url: '/save_boards',
            type: 'POST',
            contentType: "application/json",
            dataType: "json",
            data: JSON.stringify(dataObject),
            success: function(response) {
                console.log('SAVE succes' + JSON.stringify(response));
                callback();
            },
            error: function(error) {
                console.log('SAVE error' + JSON.stringify(error)); // If there is an error we log it on the console.
            }
        });
    },
    getBoard: function(boardId) {
        // returns the board with the given id from this.boards
        for (let i = 0; i < this.boards.length; i++)
        {
            if (this.boards[i].id === Number(boardId)) 
            {
                return this.boards[i];
            }
        }
    },

    createNewBoard: function(boardTitle, callback) {
        // sends an AJAX request to a Flask endpoint
        // containg the data of the newly created boards title
        $.ajax({
            url: '/create_board',
            type: 'POST',
            data: {"boardTitle": boardTitle},
            success: function(response) {
                console.log('NEW BOARD' + JSON.stringify(response));
                callback();
            },
            error: function(error) {
                console.log(error); // If there is an error we log it on the console.
            }
        });
    },

    createNewCard: function(boardId, cardTitle, callback) {
        // sends an AJAX request containing 
        // the newly created cards title and 
        // the boards id containing it 
        // to a Flask endpoint to save it
        $.ajax({
            url: '/create_card',
            type: 'POST',
            data: {"boardId": boardId, "cardTitle": cardTitle},
            success: function(response) {
                console.log('CREATE CARD' + JSON.stringify(response));
                callback();
            },
            error: function(error) {
                console.log(error); // If there is an error we log it on the console.
            }
        });
    },

    editCard: function(boardId, cardId, cardProperty, newCardContent) {
        // finds a card in dataHandler.boards
        // by boardId and cardId and then
        // changes a property of a card 
        // based on the cardProperty parameter
        // to the value given in the newCardContent parameter
        for (var i = 0; i < this.getBoard(boardId).cards.length; i++) { 
            if (this.getBoard(boardId).cards[i].id === Number(cardId)) {
                if (cardProperty === 'title') {
                    this.getBoard(boardId).cards[i].title = newCardContent;
                } else if (cardProperty === 'order') {
                    this.getBoard(boardId).cards[i].order = newCardContent;
                } else if (cardProperty === 'status') {
                    this.getBoard(boardId).cards[i].status = newCardContent;
                }
            }
        }
    },


    min_or_max_Object: function(originObject,orderKey,direction) {
        // our homemade sorting algorithm
        var val_index = 0;
        var min_or_max_value = originObject[0][orderKey];
        var key_value = originObject[0][orderKey];
        for (let j=0; j <= originObject.length-1; j++) {
                var act_value = originObject[j][orderKey];
                
                if (direction=='ASC')
                {
                    if ( act_value <= key_value)
                    {
                        val_index = j;
                        min_or_max_value = act_value;
                    }
                }
                
                if (direction=='DESC')
                {
                    if ( act_value >= key_value )
                    {
                        val_index = j;
                        min_or_max_value = act_value;
                    }
                }              
        }
    return [val_index,min_or_max_value];
    },   
   
   orderObject: function(originObject,orderKey,direction) {
    // ordering object by key
    var unorderedObject = JSON.parse(JSON.stringify(originObject));
    var len = unorderedObject.length-1;
    var orderedObject = [];
        
        for (let i=0; i <= originObject.length-1; i++){

            var key_value = app.dataHandler.min_or_max_Object(unorderedObject,orderKey,direction)[1];
            var val_index = app.dataHandler.min_or_max_Object(unorderedObject,orderKey,direction)[0];
            for (let j=0; j <= unorderedObject.length-1; j++) {
                var act_value = unorderedObject[j][orderKey];
                
                if (direction=='ASC')
                {
                    if ( act_value <= key_value)
                    {
                        val_index = j;
                        key_value = act_value;
                    }
                }
                
                if (direction=='DESC')
                {
                    if ( act_value >= key_value )
                    {
                        val_index = j;
                        key_value = act_value;
                    }
                }
                
            }
            orderedObject.push(unorderedObject[val_index]);
            unorderedObject.splice(val_index,1);
        }
        return orderedObject;
   },

   numberOfCards: function() {
       // counts the cards on the given board
       cards = []
       for (let i = 0; i < this.boards.length; i++) {
            newCards = this.boards[i].cards
            cards = cards.concat(newCards);
       }
       return cards.length;
   },

   findCardById: function(boardId, cardId) {
       // using the given boardId finds the related card by cardId
       var cardList = this.boards[boardId].cards;
       
       var i = 0;
       while (i < cardList.length && !(cardList[i].id === cardId)) { i++; }
       
       return cardList[i];       
   }
}