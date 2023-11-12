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

This works because JustWatch puts heaps of data in json into their html pages.

# oneliners


```js
output = []; document.querySelectorAll("h2.title-card-heading").forEach((e) => output.push({"title": e.childNodes[0].textContent.trim()}))
```

```js
output = []; document.querySelectorAll("h2.title-card-heading").forEach((e) => output.push({"title": e.childNodes[0].textContent.trim(), "release": parseInt(e.childNodes[1].textContent.trim().replace(/[\)\(]/g,""),10) }))
```


```js
document.querySelectorAll("h2.title-card-heading").forEach((e) => console.log(e.parentNode.href))
```


```js
output = []; document.querySelectorAll("h2.title-card-heading").forEach((e) => output.push(e.parentNode.href))
```

```sh
xargs -n 1 ./dl.sh < urls.txt
```
