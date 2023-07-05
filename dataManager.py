import sqlite3
from sqlite3 import Cursor

languages = {
    "auto" : "auto-detect",
    "en": "english",
    "zh": "chinese",
    "de": "german",
    "es": "spanish/castilian",
    "ru": "russian",
    "ko": "korean",
    "fr": "french",
    "ja": "japanese",
    "pt": "portuguese",
    "tr": "turkish",
    "pl": "polish",
    "ca": "catalan/valencian",
    "nl": "dutch",
    "ar": "arabic",
    "sv": "swedish",
    "it": "italian",
    "id": "indonesian",
    "hi": "hindi",
    "fi": "finnish",
    "vi": "vietnamese",
    "he": "hebrew",
    "uk": "ukrainian",
    "el": "greek",
    "ms": "malay",
    "cs": "czech",
    "ro": "romanian",
    "da": "danish",
    "hu": "hungarian",
    "ta": "tamil",
    "no": "norwegian",
    "th": "thai",
    "ur": "urdu",
    "hr": "croatian",
    "bg": "bulgarian",
    "lt": "lithuanian",
    "la": "latin",
    "mi": "maori",
    "ml": "malayalam",
    "cy": "welsh",
    "sk": "slovak",
    "te": "telugu",
    "fa": "persian",
    "lv": "latvian",
    "bn": "bengali",
    "sr": "serbian",
    "az": "azerbaijani",
    "sl": "slovenian",
    "kn": "kannada",
    "et": "estonian",
    "mk": "macedonian",
    "br": "breton",
    "eu": "basque",
    "is": "icelandic",
    "hy": "armenian",
    "ne": "nepali",
    "mn": "mongolian",
    "bs": "bosnian",
    "kk": "kazakh",
    "sq": "albanian",
    "sw": "swahili",
    "gl": "galician",
    "mr": "marathi",
    "pa": "punjabi",
    "si": "sinhala",
    "km": "khmer",
    "sn": "shona",
    "yo": "yoruba",
    "so": "somali",
    "af": "afrikaans",
    "oc": "occitan",
    "ka": "georgian",
    "be": "belarusian",
    "tg": "tajik",
    "sd": "sindhi",
    "gu": "gujarati",
    "am": "amharic",
    "yi": "yiddish",
    "lo": "lao",
    "uz": "uzbek",
    "fo": "faroese",
    "ht": "haitian creole",
    "ps": "pashto",
    "tk": "turkmen",
    "nn": "nynorsk",
    "mt": "maltese",
    "sa": "sanskrit",
    "lb": "luxembourgish",
    "my": "myanmar",
    "bo": "tibetan",
    "tl": "tagalog",
    "mg": "malagasy",
    "as": "assamese",
    "tt": "tatar",
    "haw": "hawaiian",
    "ln": "lingala",
    "ha": "hausa",
    "ba": "bashkir",
    "jw": "javanese",
    "su": "sundanese",}


class DBConnector:

    dbPath = 'userdata.db'
    con = None
    cur = None
    languages = {}

    def __init__(self, path = dbPath):
        self.path = path;
        self.con = sqlite3.connect(self.path)
        self.cur = self.con.cursor()

        with self.con:

            #Creating user table
            self.query("""Create table if not exists users(
                id integer primary key,
                username text,
                credits integer);""")
        
            #Creating language table
            self.query("""Create table if not exists languages(
                isoCode text primary key,
                name text);""")
            
            #Inserting languages into the database
            for i in languages:
                self.query(f"Insert or ignore into languages(isoCode, name) values('{i}', '{languages[i]}');")
            
        self.commit()

    
    # Query function
    def query(self, query):
        return self.cur.execute(query).fetchall()

    # Close function
    def close(self):
        self.con.close()

    # Commit function
    def commit(self):
        self.con.commit() 

    # Get languages function
    def getLangList(self) -> str:
        langList = ""

        for i in languages:
            langList += i + " - " + languages[i] + " \n"

        return langList

    def getLangValue(self, isoCode) -> str:
        return languages[isoCode]