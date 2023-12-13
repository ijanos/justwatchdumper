# just watch data dumper

If it is stupid and it works it is not stupid.

I wanted to create a list of movies I watched. JustWatch provides a great user interface
to quickly put together a list but they have no export options.

A stupid way to export data:

1. load the page that lists your movies
2. run a JS oneline in the browser console to get an URL for each movie's page (this pages doesn't have all the information we need but the individual movie pages does)
3. save the urls to a text file
4. user curl to download the html for each page
5. use python to extract data from the downloaded files
6. save everything to one json file

Thankfully JustWatch puts heaps of data in json into their html pages, that I can read. 

# usage

Create an array with all the links from the browser console: 
```js
output = []; document.querySelectorAll("h2.title-card-heading").forEach((e) => output.push(e.parentNode.href))
```

type `output` into the console then copy paste the resulting array. 
<img width="712" alt="SCR-20231213-kofg-2" src="https://github.com/ijanos/justwatchdumper/assets/175447/5ec9721d-8d01-4b0a-b92f-725865c717d7">


cleanup the array, remove `"` quotes (use search & replace in your favourite editor) and save it to a text file with one URL per line.  

feed the text file to the download script with `xargs`. The script contains a sleep, if you go full speed justwatch will block you for too many requests. 

```sh
xargs -n 1 ./dl.sh < urls.txt
```

you will end up with a directory full of `.html` files, use the import script on the files and hope justwatch didn't change their json format.  

```
python import.py directory_name
```

# other things I've tried

Read the title into a JSON list from the browser's console: 

```js
output = []; document.querySelectorAll("h2.title-card-heading").forEach((e) => output.push({"title": e.childNodes[0].textContent.trim()}))
```

read the title and the release date: 

```js
output = []; document.querySelectorAll("h2.title-card-heading").forEach((e) => output.push({"title": e.childNodes[0].textContent.trim(), "release": parseInt(e.childNodes[1].textContent.trim().replace(/[\)\(]/g,""),10) }))
```

get a list of links to each movie: 

```js
document.querySelectorAll("h2.title-card-heading").forEach((e) => console.log(e.parentNode.href))
```

