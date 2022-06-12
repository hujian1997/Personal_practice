import flask
import DBcm
import mysql.connector

app = flask.Flask(__name__)
app.config['dbconfig']={'host': '127.0.0.1',
                        'user': 'HUJIAN',
                        'password': 'ASDQWE',
                        'database': 'vsearchlogDB'}


def log_request(req, res):
    with DBcm.UseDatabase(app.config['dbconfig']) as cursor:
        _sql = '''insert into log
                    (phrase,letters,ip,browser_string,results)
                    values
                    (%s,%s,%s,%s,%s)'''
        cursor.execute(_sql, (req.form['phrase'],
                              req.form['letters'],
                              req.remote_addr,
                              str(req.user_agent),
                              res))

def sreach4letters(phrase='abcd', letters='aeiou'):
    '''对phrase字符串和letters字符串进行交集运算，返回一个集合'''
    return set(letters).intersection(set(phrase))


@app.route('/search4', methods=['post'])
def do_search():
    phr = flask.request.form['phrase']
    let = flask.request.form['letters']
    title = 'Here are you results'
    results = str(sreach4letters(phrase=phr, letters=let))
    log_request(req=flask.request, res=results)
    return flask.render_template('results.html',
                                 the_phrase=phr,
                                 the_letters=let,
                                 the_results=results,
                                 the_title=title, )


@app.route('/')
@app.route('/entry')
def entry_page():
    return flask.render_template('entry.html', the_title='welcome to this one the web')


@app.route('/viewlog')
def view_the_log():
    with DBcm.UseDatabase(app.config['dbconfig']) as cursor:

        _sql='''select phrase,letters,ip,browser_string,results from log'''
        cursor.execute(_sql)
        contects=cursor.fetchall()
        titles=('Phrase','letters','remote_addr','user_agent','results')

    return flask.render_template('viewlog.html', the_title='View_log',
                                 the_row_titles=titles,
                                 the_data=contects)

if __name__=='__main__':
    app.run(debug=True)
