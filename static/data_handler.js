var app = app || {};

// this object contains the functions which handle the data and its reading/writing
// feel free to extend and change to fit your needs
app.dataHandler = {
    boards: [], // it contains the boards and their cards
    loadTestBoards: function() {
        // if the settings say that we are in developer environment then it loads in
        var myJSON = '{"boards": [{"id": 1337, "title": "Test Board 1","state": "active","cards": [{"id": 1,"title": "task1","status": "new","order": "53"},{"id": 2,"title": "task2","status": "in progress","order": "2"},{"id": 3,"title": "task3","status": "done","order": "1"}]},{"id": 2,"title": "Test Board 2","state": "active","cards": [{"id": 4,"title": "task4","status": "new","order": "3"},{"id": 5,"title": "task5","status": "in progress","order": "2"},{"id": 6,"title": "task6","status": "done","order": "1"}]}]}';
        this.boards = JSON.parse(myJSON).boards;
        // some test data, like the ones you find in sample_data.json
    },
    loadBoards: function() {
        // loads data from local storage to this.boards property
        $.ajax({
            url: '/board',
            type: 'POST',
            data: dataObj,
            dataType: json,
            success: function(response) {
                this.boards = JSON.parse(dataObj).boards;; // After succesful request we notify the user with line got from the Flask /votePlanet handler.
            },
            error: function(error) {
                console.log(error); // If there is an error we log it on the console.
            }
        });
    },
    saveBoards: function() {
        // saves data to local storage from this.boards property
        localStorage.setItem('boards', JSON.stringify(this.boards));
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

    createNewBoard: function(boardTitle) {
        //we should write some switch for this
        //app.dataHandler.loadTestBoards();
        app.dataHandler.loadBoards();
        var board_list = app.dataHandler.boards;
        // add new id ???
        var skeletonObject = { id: 666, title: 'SATAN', state: 'active', cards: []};
        skeletonObject.title = boardTitle;
        // CHANGE THIS WHEN WE START TO DELETE THE BOARDS OR WHEN WE DIE
        if (board_list) {
            skeletonObject.id = board_list.length + 1;
            board_list.push(skeletonObject);
        } else {
            skeletonObject.id = 1;
            board_list = [skeletonObject,];
        }
        app.dataHandler.boards = board_list;

    },

    createNewCard: function(boardId, cardTitle) {
        // creates new card in the given board, saves it and returns its id
        app.dataHandler.loadBoards();
        var board_list = app.dataHandler.boards;
        var skeletonCard = { 
            id: 'spooky', 
            title: cardTitle, 
            status: 'new', 
            order: 66 // TO DO !!! ?!?!?!
        };        
        skeletonCard.id = app.dataHandler.numberOfCards() + 1;
        
        if (this.getBoard(boardId).cards) {
            this.getBoard(boardId).cards.push(skeletonCard);
        } else {
            this.getBoard(boardId).cards = [skeletonCard,];
        }
        
        app.dataHandler.boards = board_list;

    },
    // here can come another features
    editCard: function(boardId, cardId, cardProperty, newCardContent) {
        for (var i = 0; i < this.getBoard(boardId).cards.length; i++) { 
            var g = this.getBoard(boardId).cards[i].id;
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
        app.dataHandler.saveBoards();
        app.dom.showCards(boardId);
    },

    chooseBoards: function() {
       this.boards = [];
       if ($('#settings-button').text() === 'dev') {
           app.dataHandler.loadTestBoards();
       } else if ($('#settings-button').text() === 'prod') {
           app.dataHandler.loadBoards();
       }
   },

    min_or_max_Object: function(originObject,orderKey,direction) {
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
       cards = []
       for (let i = 0; i < this.boards.length; i++) {
            newCards = this.boards[i].cards
            cards = cards.concat(newCards);
       }
       return cards.length;
   },

   findCardById: function(boardId, cardId) {
       var cardList = this.boards[boardId].cards;
       
       var i = 0;
       while (i < cardList.length && !(cardList[i].id === cardId)) { i++; }
       
       return cardList[i];       
   }
}