// // get the currently selected text
//   var t;
//   try {
//     t= ((window.getSelection && window.getSelection()) ||
// 	(document.getSelection && document.getSelection()) ||
// 	(document.selection && document.selection.createRange &&
// 	document.selection.createRange().text));
//   }
//   catch(e){ // access denied on https sites
//     t = "";
//   }

//   // location.href = ('http://127.0.0.1:8000/bookmarklet/' + t);


// javascript:(function(){
//   var d = document,
//   c = d.createElement("div"),
//   b = d.body,
//   l = d.location;
//   c.id = "bookmarkletAlertBox";
//   c.innerHTML = '{% spaceless %}{% include "bookmarklet.html" %}{% endspaceless %}';

//   t = d.createElement("link"),
//   t.rel = "stylesheet";
//   t.media = "screen, projections";
//   t.type = "text/css";
//   t.href = "http://127.0.0.1:8000/media/css/bookmarklet.css";

//   b.appendChild(t);
//   b.appendChild(c);
// })





function getEmbed(){
   var e = window.frames["leadr_bookmarklet_iframe"];
   return e;
}

function addCSS(url){
  var headID = document.getElementsByTagName("head")[0];
  var cssNode = document.createElement('link');
  cssNode.type = 'text/css';
  cssNode.rel = 'stylesheet';
  cssNode.href = url;
  cssNode.media = 'screen';
  headID.appendChild(cssNode);
}

/* Base64 encoding from http://ostermiller.org/calc/encode.html

License
This program is free software; you can redistribute it and/or modify it 
under the terms of the GNU General Public License as published by the 
Free Software Foundation; either version 2 of the License, or (at your 
option) any later version.
This program is distributed in the hope that it will be useful, but 
WITHOUT ANY WARRANTY; without even the implied warranty of 
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General 
Public License for more details.

*/
var END_OF_INPUT = -1;
var base64Chars = new Array(
    'A','B','C','D','E','F','G','H',
    'I','J','K','L','M','N','O','P',
    'Q','R','S','T','U','V','W','X',
    'Y','Z','a','b','c','d','e','f',
    'g','h','i','j','k','l','m','n',
    'o','p','q','r','s','t','u','v',
    'w','x','y','z','0','1','2','3',
    '4','5','6','7','8','9','+','/'
);

var reverseBase64Chars = new Array();
for (var i=0; i < base64Chars.length; i++){
    reverseBase64Chars[base64Chars[i]] = i;
}

var base64Str;
var base64Count;
function setBase64Str(str){
    base64Str = str;
    base64Count = 0;
}
function readBase64(){    
    if (!base64Str) return END_OF_INPUT;
    if (base64Count >= base64Str.length) return END_OF_INPUT;
    var c = base64Str.charCodeAt(base64Count) & 0xff;
    base64Count++;
    return c;
}
function encodeBase64(str){
    setBase64Str(str);
    var result = '';
    var inBuffer = new Array(3);
    var lineCount = 0;
    var done = false;
    while (!done && (inBuffer[0] = readBase64()) != END_OF_INPUT){
        inBuffer[1] = readBase64();
        inBuffer[2] = readBase64();
        result += (base64Chars[ inBuffer[0] >> 2 ]);
        if (inBuffer[1] != END_OF_INPUT){
            result += (base64Chars [(( inBuffer[0] << 4 ) & 0x30) | (inBuffer[1] >> 4) ]);
            if (inBuffer[2] != END_OF_INPUT){
                result += (base64Chars [((inBuffer[1] << 2) & 0x3c) | (inBuffer[2] >> 6) ]);
                result += (base64Chars [inBuffer[2] & 0x3F]);
            } else {
                result += (base64Chars [((inBuffer[1] << 2) & 0x3c)]);
                result += ('=');
                done = true;
            }
        } else {
            result += (base64Chars [(( inBuffer[0] << 4 ) & 0x30)]);
            result += ('=');
            result += ('=');
            done = true;
        }
        lineCount += 4;
        if (lineCount >= 76){
            result += ('\n');
            lineCount = 0;
        }
    }
    return result;
}

/* make string URL safe; remove padding =, replace "+" and "/" with "*" and "-" */
function encodeBase64ForURL(str){
   var str = encodeBase64(str).replace(/=/g, "").replace(/\+/g, "*").replace(/\//g, "-");
   str = str.replace(/\s/g, "");   /* Watch out! encodeBase64 breaks lines at 76 chars -- we don't want any whitespace */
   return str;
}

function keyPressHandler(e) {
      var kC  = (window.event) ?    // MSIE or Firefox?
                 event.keyCode : e.keyCode;
      var Esc = (window.event) ?   
                27 : e.DOM_VK_ESCAPE // MSIE : Firefox
      if(kC==Esc){
         // alert("Esc pressed");
         toggleItem("leadr_bookmarklet");
      }
}


function toggleItem(id){
  var item = document.getElementById(id);
  if(item){
    if ( item.style.display == "none"){
      item.style.display = "";
    }
    else{
      item.style.display = "none";
    } 
  }
}

function showItem(id){
  try{
    var item = document.getElementById(id);
    if(item){
        item.style.display = "";
    }
  }
  catch(e){
  
  }
}

(function(){

  // get the currently selected text
  var t;
  try {
    t=((window.getSelection && window.getSelection())||(document.getSelection && document.getSelection())||(document.selection && document.selection.createRange && document.selection.createRange().text));
  }
  catch(e){ // access denied on https sites
    t = "";
  }
  console.log(t);
  var address = t.toString();
  
  if (address == ""){
    address = "";
  }

  
  var iframe_url = "http://127.0.0.1:8000/media/bookmarklet.html";
 
  var existing_iframe = document.getElementById("leadr_bookmarklet_iframe");
  
  if (existing_iframe){
    showItem("leadr_bookmarklet");
    // if has text selected, copy into iframe
    if (address != ""){
      existing_iframe.src = iframe_url;
    }
    else{
      // want to set focus back to that item! but can't; access denied
    }
    return;
  }
 
  addCSS("http://127.0.0.1:8000/media/css/bookmarklet-mini.css");

  var div = document.createElement("div");
  div.id = "leadr_bookmarklet";
  
  var str = "";
  str += "<table id='leadr_bookmarklet_table' valign='top' cellspacing='0' cellpadding='0'><tr><td width ='330' height='220'>";
  str += "<iframe frameborder='0' scrolling='no' name='leadr_bookmarklet_iframe' id='leadr_bookmarklet_iframe' src='" + iframe_url + "' width='330px' height='320px' style='textalign:right; backgroundColor: white;'></iframe>";
  str += "</td><td onClick='toggleItem(\"leadr_bookmarklet\");' style='background: #FFFFFF;' title='click to close window' valign='top' align='center' width='20px'>";
  str += "<a href='javascript:void(0);' style='width:100%; text-align: middle; color: #000000; font-family: Arial;'>x</a>";
  str += "</td></tr></table>";
  
  div.innerHTML = str;
  
  div.onkeypress = keyPressHandler;
  document.body.insertBefore(div, document.body.firstChild);
})()







//javascript:(function(){instacalc_script=document.createElement('SCRIPT');instacalc_script.type='text/javascript';instacalc_script.src='http://instacalc.com/gadget/instacalc.bookmarklet.js?x='+(Math.random());document.getElementsByTagName('head')[0].appendChild(instacalc_script);})();

// (function () {
//   var script = document.createElement('SCRIPT');
//   script.src = 'http://127.0.0.1:8000/media/js/bookmarklet.js';
//   document.body.appendChild(script);
// })()

// (function(){
// 	bookmarklet_script=document.createElement('SCRIPT');bookmarklet_script.type='text/javascript';bookmarklet_script.src='http://127.0.0.1:8000/media/js/bookmarklet.js';document.getElementsByTagName('head')[0].appendChild(bookmarklet_script);})();
