from flask import Flask, jsonify, request, render_template
import os
import openai

def process_2(chat_query):
    openai.api_key = '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'
    messages = [ {"role": "system", "content":  
                "You are a intelligent assistant."} ] 

    message = chat_query
    if message: 
        messages.append( 
            {"role": "user", "content": message}, 
        ) 
        chat = openai.ChatCompletion.create( 
            model="gpt-3.5-turbo", messages=messages 
        ) 
    reply = chat.choices[0].message.content 
    # print(f"ChatGPT: {reply}") 
    # messages.append({"role": "assistant", "content": reply})
    return reply

# Helper Function Hugging Face API Call
def process(query_chat):	
    os.environ["REPLICATE_API_TOKEN"]="r8_7lCRX3aYKrPuCOZqNdpajap95bej6pI2TUTCb"
    import replicate
    output = replicate.run(
        "meta/llama-2-70b-chat:02e509c789964a7ea8736978a43525956ef40397be9033abf9fd2badfe68c9e3",
        input={"prompt": query_chat}
    )
    # The meta/llama-2-70b-chat model can stream output as it's running.
    # The predict method returns an iterator, and you can iterate over that output.
    string_output = ""
    for item in output:
        # https://replicate.com/meta/llama-2-70b-chat/versions/02e509c789964a7ea8736978a43525956ef40397be9033abf9fd2badfe68c9e3/api#output-schema
        string_output = string_output+" "+item
    return string_output

# creating a Flask app
app = Flask(__name__)

# on the terminal type: curl http://127.0.0.1:5000/
# returns hello world when we use GET.
# returns the data that we send when we use POST.


@app.route('/', methods=['GET', 'POST'])
def home():
	if request.method == 'GET':

		data = "Send Query at at /ques/"
		return jsonify({'data': data})


@app.route('/ques/<string:query_chat>', methods=['GET'])
def disp(query_chat):
	#thread call
	response_chat = process_2(query_chat)
	return jsonify({'message': response_chat})

# -------------------------------------------------------

# @app.route('/quesparams/', methods=['GET'])
# def sendResponse():
#     # If method is GET, check if  number is entered 
#     # or user has just requested the page.
#     # Calculate the square of number and pass it to 
#     # answermaths method
#     if request.method == 'GET':
#         number = request.args.get('question')
#         sq = process(number)
#         # pass the result to the answer HTML
#         # page using Jinja2 template
#         return render_template('answer.html', 
#                                 squareofnum=sq, num=number)

@app.route('/check', methods=['GET'])
def check():
	if request.method == 'GET':
		data = "Active"
		return jsonify({'Status': data})

# driver function
if __name__ == '__main__':
	app.run(debug=True)
  