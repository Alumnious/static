from textnode import *
from htmlnode import *
from functions import *

def main():
    copy_static()
    generate_page_recursive("content", "template.html", "public")
main()