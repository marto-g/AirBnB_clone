#!/usr/bin/python3
"""
entry point of the command interpreter
"""
import cmd
import models
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from shlex import split
import re


def parse(arg):
        """
        parses arguments on the command line intrepreter
        """
        curly_braces = re.search(r"\{(.*?)\}", arg)
        brackets = re.search(r"\[(.*?)\]", arg)
        if curly_braces is None:
            if brackets is None:
                return [i.strip(",") for i in split(arg)]
            else:
                lexer = split(arg[:brackets.span()[0]])
                retl = [i.strip(",") for i in lexer]
                retl.append(brackets.group())
                return retl
        else:
            lexer = split(arg[:curly_braces.span()[0]])
            retl = [i.strip(",") for i in lexer]
            retl.append(curly_braces.group())
            return retl


class HBNBCommand(cmd.Cmd):
    """defines the cmd class"""
    prompt = "(hbnb) "
    __our_classes = ['BaseModel', 'User', 'State', 'City',
                     'Amenity', 'Place', 'Review']

    def do_quit(self, arg):
        """Quit command to exit the program"""
        return True

    def do_EOF(self, arg):
        """EOF command to exit the program"""
        return True

    def emptyline(self):
        """when an empty line is entered, it should not execute anything"""
        pass

    def default(self, arg):
        """cmd module beavior when input is invalid"""
        arg_dict = {
            "all": self.do_all,
            "show": self.do_show,
            "destroy": self.do_destroy,
            "count": self.do_count,
            "update": self.do_update,
        }
        match = re.search(r"\.", arg)

        if match is not None:
            args = [arg[:match.span()[0]], arg[match.span()[1]:]]
            match = re.search(r"\((.*?)\)", args[1])
            if match is not None:
                command = [args[1][:match.span()[0]], match.group()[1:-1]]
                if command[0] in arg_dict.keys():
                    call = "{} {}".format(args[0], command[1])
                    return arg_dict[command[0]](call)
        print("*** Unknown syntax: {}".format(arg))
        return False

    def do_create(self, arg):
        """
        Creates a new instance of BaseModel
        saves it (to the JSON file) and prints the id
        Ex: $ create BaseModel
        """
        args = parse(arg)

        if len(args) == 0:
            print("** class name missing **")
        elif args[0] not in self.__our_classes:
            print("** class doesn't exist **")
        else:
            print(eval(args[0])().id)
            models.storage.save

    def do_show(self, arg):
        """
        Prints the string representation of an instance
        based on the class name and id
        Ex: $ show BaseModel 1234-1234-1234
        """
        args = parse(arg)
        objs_dict = models.storage.all()

        if len(args) == 0:
            print("** class name missing **")
        elif args[0] not in self.__our_classes:
            print("** class doesn't exist **")
        elif len(args) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(args[0], args[1]) not in objs_dict:
            print("** no instance found **")
        else:
            print(objs_dict["{}.{}".format(args[0], args[1])])

    def do_destroy(self, arg):
        """
        Deletes an instance based on the class name and id
        (save the change into the JSON file).
        Ex: $ destroy BaseModel 1234-1234-1234
        """
        args = parse(arg)
        objs_dict = models.storage.all()

        if len(args) == 0:
            print("** class name missing **")
        elif args[0] not in self.__our_classes:
            print("** class doesn't exist **")
        elif len(args) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(args[0], args[1]) not in objs_dict:
            print("** no instance found **")
        else:
            del objs_dict["{}.{}".format(args[0], args[1])]
            models.storage.save()

    def do_all(self, arg):
        """
        Prints all string representation of all instances
        based or not on the class name.
        Ex: $ all BaseModel or $ all
        """
        args = parse(arg)
        if len(args) > 0 and args[0] not in self.__our_classes:
            print("** class doesn't exist **")
        else:
            obj_list = []
            for obj in models.storage.all().values():
                if len(args) > 0 and args[0] == obj.__class__.__name__:
                    obj_list.append(obj.__str__())
                elif len(args) == 0:
                    obj_list.append(obj.__str__())
            print(obj_list)

    def do_count(self, arg):
        """Usage: count <class> or <class>.count()
        Retrieves the number of instances of a given class."""
        args = parse(arg)
        count = 0
        for obj in models.storage.all().values():
            if args[0] == obj.__class__.__name__:
                count += 1
        print(count)

    def do_update(self, arg):
        """
        Updates an instance based on the class name and id
        by adding or updating attribute (save the change into the JSON file).
        Ex: $ update BaseModel 1234-1234-1234 email "aibnb@mail.com"
        """
        args = parse(arg)
        objs_dict = models.storage.all()

        if len(args) == 0:
            print("** class name missing **")
            return False
        if args[0] not in self.__our_classes:
            print("** class doesn't exist **")
            return False
        if len(args) == 1:
            print("** instance id missing **")
            return False
        if "{}.{}".format(args[0], args[1]) not in objs_dict.keys():
            print("** no instance found **")
            return False
        if len(args) == 2:
            print("** attribute name missing **")
            return False
        if len(args) == 3:
            try:
                type(eval(args[2])) != dict
            except NameError:
                print("** value missing **")
                return False

        if len(args) == 4:
            obj = objs_dict["{}.{}".format(args[0], args[1])]
            if args[2] in obj.__class__.__dict__.keys():
                valuetype = type(obj.__class__.__dict__[args[2]])
                obj.__dict__[args[2]] = valuetype(args[3])
            else:
                obj.__dict__[args[2]] = args[3]
        elif type(eval(args[2])) == dict:
            obj = objs_dict["{}.{}".format(args[0], args[1])]
            for key, value in eval(args[2]).items():
                if (key in obj.__class__.__dict__.keys() and
                    type(obj.__class__.__dict__[key]) in {str, int, float}):
                    valuetype = type(obj.__class__.__dict__[key])
                    obj.__dict__[key] = valuetype(value)
                else:
                    obj.__dict__[key] = value
        models.storage.save()


if __name__ == '__main__':
    HBNBCommand().cmdloop()
