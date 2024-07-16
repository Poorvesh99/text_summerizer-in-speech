import openai
import wget
import pathlib
import pdfplumber
import pyttsx3


def getPaper(paper_url, filename="text.pdf"):
    downloadedPaper = wget.download(paper_url, filename)
    downloadedPaperFilePath = pathlib.Path(downloadedPaper)

    return downloadedPaperFilePath


def speakPaperSummary(paperContent):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    tldr_tag = "\n tl;dr:"
    openai.api_key = "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"
    engine_list = openai.Engine.list()

    for page in paperContent:
        text = page.extract_text() + tldr_tag
        response = openai.Completion.create(engine="ada", prompt=text, temperature=0.3,
                                            max_tokens=140,
                                            top_p=1,
                                            frequency_penalty=0,
                                            presence_penalty=0,
                                            stop=['.']
                                            )
        print(response["choices"][0]["text"])
        engine.say(response["choices"][0]["text"])
        engine.runAndWait()


paperContent = pdfplumber.open("text.pdf").pages
speakPaperSummary(paperContent)
