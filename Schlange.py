import argparse
import re
class KeywordTranslator:
    translations = {
        'und': 'and',
        'als': 'as',
        'prÃ¼fe': 'assert',
        'breche': 'break',
        'klasse': 'class',
        'fortsetze': 'continue',
        'def': 'def',
        'lösche': 'del',
        'andernfalls': 'elif',
        'sonst': 'else',
        'ausnahme': 'except',
        'Falsch': 'False',
        'schlussendlich': 'finally',
        'fÃ¼r': 'for',
        'von': 'from',
        'global': 'global',
        'wenn': 'if',
        'importiere': 'import',
        'in': 'in',
        'ist': 'is',
        'lambda': 'lambda',
        'Nichts': 'None',
        'nichtlokal': 'nonlocal',
        'nicht': 'not',
        'oder': 'or',
        'passe': 'pass',
        'erhÃ¶he': 'raise',
        'RÃ¼ckkehr': 'return',
        'Wahr': 'True',
        'versuche': 'try',
        'solange': 'while',
        'mit': 'with',
        'erzeuge': 'yield',
        "reichweite" : "range",
        "selbst" : "self",
        "drucke" : "print",
        "mathe" : "math",
        "wurzel" : "sqrt"
    }
    #dictionary to interpret the exceptions
    translation_exceptions = {
    'Ausnahme': 'Exception',
    'Typfehler': 'TypeError',
    'Wertefehler': 'ValueError',
    'Namensfehler': 'NameError',
    'Indexfehler': 'IndexError',
    'SchlÃ¼sselfehler': 'KeyError',
    'Syntaxfehler': 'SyntaxError',
    'EinrÃ¼ckungsfehler': 'IndentationError',
    'Datei nicht gefunden Fehler': 'FileNotFoundError',
    'Nullteilungsfehler': 'ZeroDivisionError',
    'Ã¼berlauf Fehler': 'OverflowError',
    'Importfehler': 'ImportError',
    'Modul nicht gefunden Fehler': 'ModuleNotFoundError',
    'Attributfehler': 'AttributeError',
    'Behauptungsfehler': 'AssertionError',
    'Laufzeitfehler': 'RuntimeError',
    'Iteration stoppen': 'StopIteration',
    'Tastaturunterbrechung': 'KeyboardInterrupt',
    }
    #Dictionary to get name of the exception
    exception_translations = {
    'Exception': 'Ausnahme',
    'TypeError': 'Typfehler',
    'ValueError': 'Wertefehler',
    'NameError': 'Namensfehler',
    'IndexError': 'Indexfehler',
    'KeyError': 'Schlüsselfehler',
    'SyntaxError': 'Syntaxfehler',
    'IndentationError': 'Einrückungsfehler',
    'FileNotFoundError': 'DateiNichtGefundenFehler',
    'ZeroDivisionError': 'Nullteilungsfehler',
    'OverflowError': 'ÜberlaufFehler',
    'ImportError': 'Importfehler',
    'ModuleNotFoundError': 'ModulNichtGefundenFehler',
    'AttributeError': 'Attributfehler',
    'AssertionError': 'Behauptungsfehler',
    'RuntimeError': 'Laufzeitfehler',
    'StopIteration': 'IterationStoppen',
    'KeyboardInterrupt': 'Tastaturunterbrechung',
    }
    errors_with_placeholders = {
    'unsupported operand type': 'nicht unterstützter operandentyp',
    'division by zero': 'division durch null',
    'name \'{}\' is not defined': 'name \'{}\' ist nicht definiert',
    'list index out of range': 'listenindex außerhalb des gültigen bereichs',
    'tuple index out of range': 'tupelindex außerhalb des gültigen bereichs',
    'invalid syntax': 'ungültige syntax',
    'indentation error': 'einrückungsfehler',
    'file not found': 'datei nicht gefunden',
    'attribute \'{}\' not found': 'attribut \'{}\' nicht gefunden',
    'module \'{}\' not found': 'modul \'{}\' nicht gefunden',
    'division or modulo by zero': 'division oder modulo durch null',
    'key error': 'schlüsselfehler',
    'invalid literal for int() with base {}: \'{}\'': 'ungültiges literal für int() mit basis {}: \'{}\'',
    'unexpected indent': 'unerwartete einrückung',
    'not a valid identifier': 'kein gültiger bezeichner',
    'invalid syntax, unexpected {}: \'{}\'': 'ungültige syntax, unerwartetes {}: \'{}\'',
    'unsupported operand type(s) for {}: \'{}\' and \'{}\'': 'nicht unterstützte operandentypen für {}: \'{}\' und \'{}\'',
    }
    errors_without_placeholders = {
    'unsupported operand type': 'nicht unterstützter operandentyp',
    'division by zero': 'division durch null',
    'name \'\' is not defined': 'name \'\' ist nicht definiert',
    'list index out of range': 'listenindex außerhalb des gültigen bereichs',
    'tuple index out of range': 'tupelindex außerhalb des gültigen bereichs',
    'invalid syntax': 'ungültige syntax',
    'indentation error': 'einrückungsfehler',
    'file not found': 'datei nicht gefunden',
    'attribute \'\' not found': 'attribut \'{}\' nicht gefunden',
    'module \'\' not found': 'modul \'\' nicht gefunden',
    'division or modulo by zero': 'division oder Modulo durch null',
    'key error': 'schlüsselfehler',
    'invalid literal for int() with base {}: \'\'': 'ungültiges literal für int() mit basis {}: \'\'',
    'unexpected indent': 'unerwartete einrückung',
    'not a valid identifier': 'kein gültiger bezeichner',
    'invalid syntax, unexpected {}: \'\'': 'ungültige syntax, unerwartetes {}: \'\'',
    'unsupported operand type(s) for {}: \'\' and \'\'': 'nicht unterstützte operandentypen für {}: \'\' und \'\'',
    }
    #extracts variables, operators,... from exception text
    def extract_operators(self,error_message):
        pattern = r'\'(.*?)\'|//?|/'
        operators = re.findall(pattern, error_message)
        operators = [op for op in operators if op != '']
        return operators
    #removes operators
    def remove_operators(self, string, operators):
        for operator in operators:
            pattern = re.escape(operator)
            string = re.sub(pattern, '', string)
        return string
    def translate_exception(self,exception):
        exception_type = type(exception).__name__ #name of the exception
        translated_type = self.exception_translations.get(str(exception_type), str(exception_type)) #translated name
        for trans in self.errors_with_placeholders:
            try:
                operators = self.extract_operators(str(exception))
                t = trans.format(*self.extract_operators(str(exception)))
                if t == str(exception):
                    e = self.remove_operators(t, operators)
                    translated_output = self.errors_without_placeholders.get(e)
                    for op in operators:
                        translated_output = translated_output.replace("''", op) 
                    break
            except Exception as e:
                translated_output = self.errors_with_placeholders.get(str(exception))
        
        if translated_output is None: #if no translation is available
            translated_output = str(exception)
        return translated_output

    def __init__(self, file_path):
        with open(file_path, 'r') as f:
            self.code = f.read()

    def translate_keywords(self):
        # Replace each German keyword with the corresponding English keyword
        for german, english in self.translations.items():
            self.code = self.code.replace(german, english)
        for german, english in self.translation_exceptions.items():
            self.code = self.code.replace(german, english)

    def execute(self):
        self.translate_keywords()
        exec(self.code)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('file', type=str)
    args = parser.parse_args()

    translator = KeywordTranslator(args.file)
    try:
        translator.execute()
    except Exception as e:
    # Übersetze die Exception, wenn sie im Dictionary vorhanden ist
        translated_message = translator.translate_exception(e)
        print(f'Fehler aufgetreten: {translated_message}')


