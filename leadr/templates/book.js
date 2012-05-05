console.log("test"); 

function addCSS(url){
  var headID = document.getElementsByTagName("head")[0];
  var cssNode = document.createElement('link');
  cssNode.type = 'text/css';
  cssNode.rel = 'stylesheet';
  cssNode.href = url;
  cssNode.media = 'screen';
  headID.appendChild(cssNode);
}

function addJS(url){
  var headID = document.getElementsByTagName("head")[0];
  var jsNode = document.createElement('script');
  jsNode.type = 'text/javascript';
  jsNode.src = url;
  headID.appendChild(jsNode);
}

addCSS("http://127.0.0.1:8080/media/css/bookmarklet-mini.css");
addJS("http://127.0.0.1:8080/media/js/bookmarklet-dismiss.js");

(function createBookmarklet(){
	var d = document,
	c = d.createElement("div"),
	b = d.body,
	l = d.location;
	c.id = "leadr_bookmarklet";
	c.style = "display:block;"
	c.innerHTML = '{% spaceless %}{% include "bookmarklet.html" %}{% endspaceless %}';

	t = d.createElement("link"),
	t.rel = "stylesheet";
	t.media = "screen, projections";
	t.type = "text/css";
	t.href = "http://127.0.0.1:8080/media/css/bookmarklet.css";

	b.appendChild(t);
	b.appendChild(c);
})()