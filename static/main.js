var app = app || {};

// this function is to initialize the application
app.init = function() {
    app.dom.showBoards();
    app.dom.mainListener();
}
  
app.init();
