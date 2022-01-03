from error import Error
import re
import sys

class Cookielang:
    def __init__(self, filename: str):
        self.lines = open(filename).readlines()
        self.vars = []
        self.const = []
        self.error = Error()

    def complie(self):
        count = 1
        for line in self.lines:
            if line.startswith('#'):
                continue

            if line.startswith('var'):
                line = line.strip()
                if not line:
                    continue

                line = line.split('=')
                if len(line) != 2:
                    raise Exception(f'Syntax error. var\'s must have a value, line: {count}') 

                key = line[0].strip().replace('var', '').strip()
                value = line[1].strip().replace("'", '').replace('"', '')

                if key in [x['key'] for x in self.vars]:
                    raise Exception(f'Var name repeat, line: {count}')

                if not value.endswith(';'):
                    raise Exception(f'Syntax error. line should end with ";". Line: {count}')

                self.vars.append({'key': key, 'value': value.replace(';', '')})

            elif line.startswith('const'):
                line = line.strip()
                if not line:
                    continue

                line = line.split('=')
                if len(line) != 2:
                    raise Exception(f'Syntax error. const\'s must have a value, line: {count}') 

                key = line[0].strip().replace('const', '').strip()
                value = line[1].strip().replace("'", '').replace('"', '')

                if key in [x['key'] for x in self.const]:
                    raise Exception(f'Const name repeat, line: {count}')

                if not value.endswith(';'):
                    raise Exception(f'Syntax error. line should end with ";". Line: {count}')

                self.const.append({'key': key, 'value': value.replace(';', '')})

            elif line.startswith('println'):
                line = line.strip()
                if not line.endswith(';'):
                    raise Exception(f'Syntax error. line should end with ";". Line: {count}')

                line = line.strip().replace(';', '')
                pattern = 'println\((.*?)\)'

                substring = re.search(pattern, line).group(1)
                if substring.startswith('"') and substring.endswith('"') or substring.startswith("'") and substring.endswith("'"):
                    substring = substring.replace("'", '').replace('"', '')
                    print(substring)

                else:
                    if substring in [x['key'] for x in self.vars]:
                        index = [x['key'] for x in self.vars].index(substring)
                        var = self.vars[index]

                        print(var['value'])

                    elif substring in [x['key'] for x in self.const]:
                        index = [x['key'] for x in self.const].index(substring)
                        const = self.const[index]

                        print(const['value'])

                    else:
                        raise Exception(f'Variable or const not found. Line: {count}')
            
            elif line.startswith('print'):
                line = line.strip()
                if not line.endswith(';'):
                    raise Exception(f'Syntax error. line should end with ";". Line: {count}')

                line = line.strip().replace(';', '')
                pattern = 'print\((.*?)\)'

                substring = re.search(pattern, line).group(1)
                if substring.startswith('"') and substring.endswith('"') or substring.startswith("'") and substring.endswith("'"):
                    substring = substring.replace("'", '').replace('"', '')
                    print(substring, end='')

                else:
                    if substring in [x['key'] for x in self.vars]:
                        index = [x['key'] for x in self.vars].index(substring)
                        var = self.vars[index]

                        print(var['value'], end='')

                    elif substring in [x['key'] for x in self.const]:
                        index = [x['key'] for x in self.const].index(substring)
                        const = self.const[index]

                        print(const['value'], end='')

                    else:
                        raise Exception(f'Variable or const not found. Line: {count}')

            elif line.startswith('prompt'):
                line = line.strip()
                if not line.endswith(';'):
                    raise Exception(f'Syntax error. line should end with ";". Line: {count}')

                line = line.strip().replace(';', '')
                pattern = 'prompt\((.*?)\)'

                substring = re.search(pattern, line).group(1)
                
                if len(substring.strip().split(',')) != 2:
                    raise Exception(f'Syntax error. prompt\'s must have a value and a var, line: {count}')

                prompt, var = substring.strip().split(',')
                prompt, var = prompt.strip().replace('"', '').replace("'", ''), var.strip()
                
                value = input(prompt)

                if var in [x['key'] for x in self.vars]:
                    index = [x['key'] for x in self.vars].index(var)
                    var = self.vars[index]

                    var['value'] = value

                else:
                    self.vars.append({'key': var, 'value': value})

            else:
                if (line.split('='))[0].strip() in [x['key'] for x in self.vars]:
                    line = line.split('=')

                    var = line[0].strip()
                    value = line[1].strip().replace("'", '').replace('"', '')

                    if not value.endswith(';'):
                        raise Exception(f'Syntax error. line should end with ";". Line: {count}')

                    for x in self.vars:
                        if x['key'] == var:
                            x['value'] = value.replace(';', '')
                            
                elif (line.split('='))[0].strip() in [x['key'] for x in self.const]:
                    raise Exception(f'Syntax error. constant already defined. Line: {count}')

            count += 1 

cookielang = Cookielang(sys.argv[1])
cookielang.complie()