"""Simple interactive story engine.

This module contains some minimal classes and structure to create
interactive stories (sometimes called interactive fiction) written
entirely as Python modules. Authors can create stories as simple
or as complex as they like since it is all just Python. Anything that
can be done in Python can be done in the story, RPG, or text adventure.

Often story engine authors will add a compatible battle engine to
add interactive battles to their stories.

Distribution

When preparing a story to be used by others there are several options:

* Include this module and any other dependent modules in an independent zip
  file and run the package as `python3 mystory.zip` whereever Python is
  installed.
* Register the story package with story.skilstak.io where it can
  be run with the latest release of the story engine (and related
  plugins) (coming)
* Compile it with Go into a single, distributable, standalone executable
  that can run on desktops and devices with embedded Python and working
  text terminal (coming)

"""

import os
import sys
import math
import time
import importlib
import pkgutil
import json
import skilstak.colors as c

class Story():
    what_phrases = [
        "I don't quite understand.",
        "What was that?",
        "I don't get it.",
        "Ummm..."
    ]
    name = 'story'
    beginning = 'intro'
    parts = {}
    prompt = '-->'
    rows = 18
    style = {
        "_": c.base1,
        "__": c.base3,
        "*": c.base1,
        "**": c.base3,
        "title": c.base3,
        "page": c.base3,
        "prompt": c.base3,
        "action": c.yellow
    }

    def __init__(self,**kwargs):
        self.base = kwargs.get("base", "story")
        self._load_about()
        self._load_style()
        self._load_story_part_mods()

    @property
    def part(self):
        """Reference to the imported module containing part of story."""
        return self._part

    @part.setter
    def part(self,part):
        """Set current part of the story to the corresponding module."""
        if isinstance(part,str):
            try:
                p = self.parts[part]
                self._part = p
            except KeyError:
                self.say('It would appear that part of the story has not yet been written.')
        else:
            self._part = part

    @property
    def gender(self):
        """The gender for the story of the protagonist."""
        return self._gender

    @gender.setter
    def gender(s,gender):
        """Trigger setting s.he, s.his, etc."""
        if gender == 'm':
            s.he = 'he'
            s.his = 'his'
            s.him = 'him'
        elif gender == 'f':
            s.he = 'she'
            s.his = "her's"
            s.him = "her"
        elif gender == 'o':
            s.he = 'it'
            s.his = 'its'
            s.him = 'it'
        else:
            raise Exception('unsupported gender type, must be m,f,o')
        s.she = s.he
        s.hers = s.his
        s.her = s.him
        s.it = s.he
        s.its = s.his
        s.itt = s.him
        s._gender = gender 

    def _load_about(self):
        self.about_path = os.path.join(self.base,'about.json')
        with open(self.about_path) as about_file:
            self.about = json.load(about_file)
        if 'name' in self.about:
            self.name = self.about['name']
        if 'beginning' in self.about:
            self.beginning = self.about['beginning']

    def _load_style(self):
        self.style_path = os.path.join(self.base,'style.json')
        if os.path.isfile(self.style_path):
            with open(self.style_path) as style_file:
                loaded = json.load(style_file)
                for key in loaded:
                    self.style[key] = loaded[key]

    def _load_story_part_mods(self):
        self.pkg = importlib.import_module(self.name)
        self.path = self.pkg.__path__
        pkgs = pkgutil.walk_packages(self.path)
        for loader, name, is_pkg in pkgs:
            mod_name = self.name + '.' + name
            part = importlib.import_module(mod_name)
            self.parts[name] = part
            if part.__doc__:
                # TODO replace any *, **, _, and __ in the whole thing
                part.text = part.__doc__.splitlines()
                part.title = part.text.pop(0)
                part.text.pop(0) # remove blank
                part.length = len(part.text)
                part.pages = math.ceil(part.length/self.rows)
                part.page = 1

    def delegate(self,action):
        if action in ['begin','end']:
            if hasattr(self.part, action):
                method = getattr(self.part, action)
                method(self)
        elif action in ['filter','parse']:
            if hasattr(self.part, action):
                method = getattr(self.part, action)
                method(self)
            if hasattr(self, 'main_' + action):
                method = getattr(self, 'main_' + action)
                method(self)
        elif hasattr(self.part,'on_' + action):
            attr = getattr(self.part, 'on_' + action)
            if type(attr) is str:
                self.tell(attr)
            else:
                attr(self)
        elif hasattr(self,'default_' + action):
            method = getattr(self, 'default_' + action)
            method(self)
        else:
            self.what()

    def begin(self,beginning=None):
        try:
            if beginning:
                self.beginning = beginning
            self.tell(self.beginning)
        except KeyboardInterrupt:
            print('\b\b\b')
            exit()

    def ask(self,text):
        prompt = self.style['prompt'] + text + ' ' + c.reset
        prompt += self.style['action']
        response = ' '.join(input(prompt).strip().lower().split())
        print(c.reset)
        return response

    def prompt_action(self):
        self.show()
        prompt = self.prompt
        try: 
            prompt = getattr(self.part, 'prompt')
        except AttributeError as e:
            pass
        self.action_line = self.ask(prompt)
        if not self.action_line:
            self.prompt_action()
        self.action = (self.action_line.split())[0]
        #TODO log the action

    def tell(self,part):
        self.part = part
        self.delegate('begin')
        self.prompt_action()
        self.delegate('filter')
        self.delegate('parse')
        self.delegate(self.action)
        self.delegate('end')
        self.tell(self.part)

    def show(self):
        print(c.clear)
        header = '{}{}{}{}{}{}/{}{}'.format(
            self.style['title'],
            self.part.title,
            c.reset,
            ' '*(80-len(str(self.part.page))-1-len(str(self.part.pages))-len(self.part.title)),
            self.style['page'],
            self.part.page,
            self.part.pages,
            c.reset
        )
        print(header)
        print('')
        start = (self.part.page-1) * self.rows
        pagelines = self.part.text[start:start+self.rows]
        for line in pagelines:
            line = ' ' * 4 + line
            print(line.format(s=self,c=c))
        if self.part.page < self.part.pages:
            print('    ...')
            print()
            self.part.page += 1
        else:
            self.part.page = 1
            print('')

    @staticmethod
    def default_forward(s):
        part = s.part.forward
        if part:
            s.part = part

    default_f = default_forward

    @staticmethod
    def main_filter(s):
        #TODO put our profanity filter
        pass
        #s.say('I am the main filter')

    @staticmethod
    def main_parse(s):
        #TODO put our main parse routine
        pass
        #s.say('I am the main parser')

    @staticmethod
    def default_save(s):
        print('Would save state to json in current working dir')
        time.sleep(1)
        #TODO save the state to json

    @staticmethod
    def default_bye(s):
        s.delegate('save')
        exit()

    default_exit = default_bye
    default_quit = default_bye
    default_goodbye = default_bye
    default_adios = default_bye

    def say(s,text,seconds=2):
        print(c.base00 + str(text))
        s.pause(seconds)

    def what(s,phrases=[]):
        import random
        if not phrases:
            phrases = s.what_phrases
        s.say(random.choice(phrases))

    def pause(s,seconds=2):
        time.sleep(seconds)

    def clear(s):
        print(c.clear)

    def askgender(s,prompt='',males=[],females=[],others=[]):
        if hasattr(s,'gender'): return s.gender
        male = ['m','b','boy','dude','man','male']
        female = ['f','g','girl','lady','woman','female'] + females
        other = ['o','n','other','none'] + others
        if males: male += males
        if females: female += females
        if others: other += others
        if not prompt: prompt = "What's your gender?"
        gender = None
        while not gender:
            g = s.ask(prompt)
            if g in male:
                gender = 'm'
            elif g in female:
                gender = 'f'
            elif g in other:
                gender = 'o'
        s.gender = gender
        return gender
   
    @staticmethod
    def roll(dice='1d6'):
        import random
        result = 0
        (num,sides) = dice.strip().lower().split('d')
        for count in range(int(num)):
            result += random.randint(1,int(sides))
        return result 
        
if __name__ is '__main__':
    Story().begin()
