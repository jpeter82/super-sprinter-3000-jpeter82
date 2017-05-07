from flask import Flask, render_template, request, url_for, redirect
import fileio
import config

app = Flask(__name__)

# Global variables

DB_NAME = config.db_name
DEBUG = config.debug


# Functions

@app.route('/', methods=['GET', 'POST'])
@app.route('/list', methods=['GET', 'POST'])
def index():
    '''
    Show table with records read from database (.csv file for now).
        @return   html   HTML template
    '''
    error = None
    if request.method == 'POST':
        if not process_insert_update(request.form):
            error = 'An error occured while updating the database!'

    content = fileio.read_from_file(DB_NAME)
    return render_template('list.html', content=content, error=error)


@app.route('/story')
def insert_record():
    '''
    Show form to user to add new record.
        @return   html   HTML template
    '''
    return render_template('form.html')


@app.route('/story/<int:story_id>')
def update_record(story_id):
    '''
    Show form for updating an existing record.
        @param    story_id   int    The id to be updated.
        @return              html   HTML template
    '''
    table = fileio.read_from_file(DB_NAME)
    to_be_updated = [record for record in table if int(story_id) == int(record[0])]
    to_be_updated = [fileio.change_eol(data, mode=1) for data in to_be_updated[0]]
    return render_template('form.html', to_be_updated=to_be_updated)


@app.route('/delete/<int:story_id>')
def delete_record(story_id):
    '''
    Catch requests for deleting specific record.
        @param    story_id   int        The id to be deleted.
        @return              redirect   Redirect to index
    '''
    status = process_delete(story_id)
    return redirect(url_for("index", status=status), code=302)


def process_insert_update(form_data):
    '''
    Handle insert and update requests.
        @param    form_data   POST      Values provided by user.
        @return               boolean   True if process is successful, otherwise False
    '''
    table = fileio.read_from_file(DB_NAME)
    names = ['modID', 'storyTitle', 'userStory', 'criteria', 'businessValue', 'estimation', 'status']
    mod_record = [form_data[name] for name in names]

    if int(form_data['modID']) == -1:
        # insert
        mod_record[0] = str(int(table[len(table) - 1][0]) + 1)
        table.append(mod_record)
        updated_table = table
    else:
        # update
        updated_table = [record for record in table if record[0] != mod_record[0]]
        updated_table.append(mod_record)
        updated_table = sorted(updated_table, key=lambda x: int(x[0]))

    status = True if fileio.write_to_file(updated_table, DB_NAME) else False
    return status


def process_delete(story_id):
    '''
    Handle delete requests.
        @param    story_id    int       The id to be deleted.
        @return               boolean   True if process is successful, otherwise False
    '''
    table = fileio.read_from_file(DB_NAME)
    updated_table = [line for line in table if int(line[0]) != story_id]
    status = True if fileio.write_to_file(updated_table, DB_NAME) else False
    return status


if __name__ == '__main__':
    app.run(debug=DEBUG)
