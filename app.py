from read_data import read_form
from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/')
def index():
        return render_template('searchform.html')

@app.route('/index2',methods = ['POST', 'GET'])
def index2():
        search_term = request.form["search"]
        lang = read_form(search_term)
        print(lang)
        return render_template("test.html",lang = lang)

# @app.route('/index2')
# def index2():
# 	return render_template('index2.html', lang=lang)
# api = Api(app)

# # @app.route('/<string:page_name>/')
# # def render_static(page_name):
# #     # number = request.args['number']
# #     # search = request.args['search']
# #     print ("number");
# #     # read_data.read_form();
# #     return render_template('%s.html' % page_name)

# # class search(Resource):
# # 	def get(self, number, search):
# # 		return {'data': read_data.read_form(number,search)}

# # api.add_resource(search, '/search/<number>/<search>')

# @app.route('/')
# def searchform():
# 	if request.method == 'GET':
# 		number = request.values.get('number') # Your form's
# 		search = request.values.get('search') # input names
# 		read_data.read_form(number,search);
# 		return redirect("index2.html",number=number,search=search)
# 	# number = request.args['number']
# 	# search = request.args['search']
# 	return render_template('searchform.html')

# @app.route('/index2', methods=['GET'])
# def index2():
#     if request.method == 'GET':
#         number = request.values.get('number') # Your form's
#         search = request.values.get('search') # input names
#         read_data.read_form(number,search);

if __name__ == '__main__':
        search_term = request.form["search"]
        lang = read_form(search_term)
        app.run(debug=True)
