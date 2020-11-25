# books-downloader-Python
Python program that allows you to download with ease books from the Springer webpage.

## Requirements:<br>
- This folder
- [Pyhton interpreter](https://www.python.org/downloads/)
- [Selenium Python library](https://selenium-python.readthedocs.io)
- [Requests Pyhton library](https://requests.readthedocs.io/en/master/)
- [Google Chrome Driver](https://chromedriver.chromium.org/downloads) depending on your Google Chrome version<br>
- [Google Chrome](https://www.google.com/chrome/) installed in your PC

Note: Python dependencies are defined in requirements.txt and everything is explained below.


Hi 😃,
"Springer" publisher allows you to download > 500 books in PDF format from its official web page for free.

This is the [webpage](https://link.springer.com/search/page/2?showAll=true&package=mat-covid19_textbooks&facet-content-type=%22Book%22&sortOrder=newestFirst).

You can download files using two different approaches:

Mehtod 1 -> Manual download<br>
Mehtod 2 -> Semmi-automatic download (Recommended jeje)


## METHOD 1<br>
If you want to download some books, you go to their webpage and click on every book you are interested in and follow a manual download approach.
This involves the following steps:<br>
1. go to [Springer Webpage](https://link.springer.com/search/page/2?showAll=true&package=mat-covid19_textbooks&facet-content-type=%22Book%22&sortOrder=newestFirst)

<img src="images/image_1.jpg" width="700">

2. For every book you are interested in, do the following (example with a random book):<br>
  2.1 Click the link of the book (in my example click "Quick Start Guide to VHDL")
    
  2.2 The Book details page will appear
<img src="images/image_2.jpg" width="900">
    
  2.3 Click the "Download book PDF" blue botton

  2.4 A new tab with the Book in pdf format will appear. Now you can download the file.
<img src="images/image_3.jpg" width="700">



If your are downloading few books, this is not much effort but if you are found of technical books and want to download many books, you will find yourself a little bit frustrated after the tenth (random number xD) download.

That's why I created this Python program that allows you to download the books saving you some time. The set up process is easier than it seems.
What you have to do is follow the Mehtod 2.

## METHOD 2<br>
It has two phases:<br>
1 "Set-up" phase. You just need to do it once to "prepare" the program.<br>
2 "Book download" phase. You can do it as many times as you want to download more books.<br>
The Phase 1 is a pre-requisit for the phase 2, so please do the phase 1 and then the phase 2.<br>


#### 1 Set-up phase 

1. Download this github folder.

2. Go to [ChromeDriver Webpage](https://sites.google.com/a/chromium.org/chromedriver/downloads)
    and download the driver depending on your Google Chrome Version (to find out your version, open Google Chrome and go to Chrome -> About Google Chrome or similar).
    
    Save the corresponding zip into this folder. Extract the file and rename the extracted file to "chromedriver" (if it has a different name). Now you can delete the .zip file.
    
3. Open a Terminal and navigate to this folder.
    
4. Create a new virtual environment and install dependencies:
    
```
    python3 -m venv env
    source env/bin/activate
    pip3 install -r requirements.txt 
```

#### 2 Book Download phase

1. Go to [Springer webpage](https://link.springer.com/search/page/2?showAll=true&package=mat-covid19_textbooks&facet-content-type=%22Book%22&sortOrder=newestFirst)
   
<img src="images/image_1.jpg" width="700">


2. Choose a book that you find interesting, right click on the book name and select "Copy link address"
<img src="images/image_4.jpg" width="700">


3. Open the file "input.txt" (or create it in this folder with the exact same name if it doesn't exist) and paste the copied link in a new line
<img src="images/image_5.jpg" width="900">


4. Repeat steps 2 and 3 for all the books you want to Download (remember to Paste each new link in a new line of the "input.txt" file).
    Save the "input.txt" file.

5. Go to the terminal (you will need to be in this folder) and execute

```
source env/bin/activate
python3 download_Springer_books.py
```

6.    Enjoy your books 👓

Cheers!
