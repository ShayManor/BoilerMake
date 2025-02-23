from flask import Flask
from app.routes import bp as main_bp

app = Flask(__name__)
app.register_blueprint(main_bp)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
# eb setenv MONGO_URI="mongodb+srv://trueflash42:dOKpvn6cqAyK7RHb@agent.ctwv3.mongodb.net/boilermake25?retryWrites=true&w=majority&appName=Agent" OPENAI_API_KEY="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" ANTHROPIC_API_KEY="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"