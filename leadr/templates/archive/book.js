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

addCSS("http://127.0.0.1:8000/media/css/bookmarklet-mini.css");

(function createBookmarklet(){
	var d = document,
	c = d.createElement("div"),
	b = d.body,
	l = d.location;
	c.id = "leadr_bookmarklet";
	c.innerHTML = '{% spaceless %}{% include "bookmarklet.html" %}{% endspaceless %}';

	t = d.createElement("link"),
	t.rel = "stylesheet";
	t.media = "screen, projections";
	t.type = "text/css";
	t.href = "http://127.0.0.1:8000/media/css/bookmarklet.css";

	b.appendChild(t);
	b.appendChild(c);
})()






// javascript:(function(){var%20script=document.createElement('SCRIPT');var%20t;try%20{t=((window.getSelection%20&&%20window.getSelection())||(document.getSelection%20&&%20document.getSelection())||(document.selection%20&&%20document.selection.createRange%20&&%20document.selection.createRange().text));}catch(e){t%20=%20"";};script.src='http://127.0.0.1:8000/bookmarklet/'+t+'/'+(Math.random());document.body.appendChild(script);})()