var app = app || {};

// this function is to initialize the application
app.init = function() {
    $("#settings-button").html(app.settings.environment);
    app.dom.showBoards();
    app.dom.mainListener();
}
  
app.init();
