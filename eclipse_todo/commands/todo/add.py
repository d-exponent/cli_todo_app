from eclipse_todo.commands.typer_app import app


@app.command()
def todo_add():
    """
    MAKE USER SPECIFY IF TODO BE SAVED IN FILE SYSTEM OR DATABASE OR BOTH SIMULTANOUSLY

    REQUEST NEW TDOD INFORMATION

    IF FILE SYSTEM
        APPEND TODO TO TODOS.CSV FILR
    ELSE IF DATABASE
        INSERT NEW TODO TO TODOS DATABASE
    ELSE:
        ASK USER IF USER WANTS TO STORE IN BOTH DB AND FS
        IF YES:
        STORE TO DB THEN STORE TO FS
                ON SUCCESS
                    NOTIFY USER OF SUCCESS
                ELSE AT ANY POINT:
                    NOTIFY USER OF ERROR AND EXIT APP
    """
    pass
