# Gameplan

[ ] plain flask routes
    [ ] route params
    [ ] query params
[ ] Jinja templates
    [ ] non-flask, non-html
    [ ] interpolation
    [ ] styling
    [ ] for loops
    [ ] if statements
    [ ] base.html (jinja extends)
[ ] forms (HTTP POST)
    [ ] send emails
    [ ] send text?
    [ ] WTForms
[ ] Databases
    [ ] create table, CRUD on the repl
    [ ] add columns, change columns, remove tables
    [ ] read from db
    [ ] add to db
    [ ] edit from db
    [ ] delete from db
    [ ] list from db
    [ ] more complex queries
    [ ] relations
[ ] url_for
[ ] blueprints
[ ] advanced Python:
    9a. function keyword arguments
    9b. classes


===

step 1:

open a terminal with ctrl+` (hold command and type the backtick key in the top-left corner)

step 2:

in the terminal, run

    source venv/bin/activate

it should now say "(venv) cassieroan@Cassies-MBP Social Media Project %"

step 3:

in the same terminal, run

    python app.py

step 4:

in your browser, open

    http://localhost:5000/


step 5:

open a repl

    flask shell


1. flask db init
2. flask db migrate -m ""
3. flask db upgrade
4. python app.py to see if its running

Databases:

1. tell Python about a db table by declaring a model:

    class MyTable(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        column1 = db.Column(db.String(140), nullable=False)
        column2 = db.Column(db.String(140), nullable=False)

tells us there's a table named "my_table". It has columns "id", "column1", and "column2". In Python we refer to it as MyTable, but in SQL it's "my_table".

Table names are usually singular nouns, like "BlogPost", "User", "Account", "Comment", "Upload", etc.

This usually goes in models.py

When we update these, we need to do a migration.

Changing names of columns is hard. Try to avoid it.

When you add, remove, or change a table or column, you have to run a migration.

    flask db migrate -m ""
    flask db upgrade

2. Make new rows:

    # make a new row in MyTable
    mt = MyTable()

    # set the fields in the row
    mt.column1 = "foo"
    mt.column2 = "bar"

    # add it to the database and save it
    db.session.add(mt)
    db.session.commit()

this would typically go in a /create route

3. get an existing row by id

To get the row with id=4,

    mt = MyTable.query.get_or_404(4)

and to get values out of it

    print(mt.column1) # prints "foo"
    print(mt.column2) # prints "bar"

typically you'd do that in a route to view a single post

4. to edit an existing row

    # get the existing row with id=4
    mt = MyTable.query.get_or_404(4)

    # edit the row
    mt.column2 = "qoux"

    # save the changes
    db.session.commit()

5. to delete an existing row

    db.session.delete(mt)
    db.session.commit()

6. to get a list of all existing rows

    all_mts = MyTable.query.all()

to print all the column1s, we might do

    for mt in MyTable.query.all():
        print(mt.column1)


###

2 kinds of clicks: links like

    <a href="/foo/bar/baz" />

makes a GET request handled by

    @app.route("/foo/bar/baz")
    def whatever():
        # something here

And buttons

    <form method="POST" action="/qoux/nux"> 

makes a POST request handled by

    @app.route("/qoux/nux", method="POST")
    def something_else():
        # launch the nukes

if you use a POST aka form, you can have inputs which you get with

    request.form.get('description')

you can also, in EITHER CASE, put parameters in the url.

    @app.route("/qoux/<name_of_first_pet>")
    def something_else(name_of_first_pet):
        print(f"my first pet was named {name_of_first_pet}")

        


