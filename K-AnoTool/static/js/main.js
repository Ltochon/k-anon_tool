function ischecked(evt){
    console.log(cmpt_check)
    var visible = "";
    if(document.getElementById(evt.currentTarget.myParam).checked){
        visible = "visible"
        cmpt_check++;
    }
    else{
        visible = "hidden"
        cmpt_check--;
    }
    if(cmpt_check > 0){
        document.getElementById("h2").style.background = "rgb(99, 148, 94)";
        document.getElementById("h2").style.color = "black";
        document.getElementById("h2").style.fontWeight = "bold";
        document.getElementById("h2").innerHTML = "Select QIDs importance levels";
        document.getElementById("h3").style.background = "rgb(99, 148, 94)";
        document.getElementById("h3").style.color = "black";
        document.getElementById("h3").style.fontWeight = "bold";
        document.getElementById("h3").innerHTML = "Select QIDs types";
        document.getElementById("h4").style.background = "rgb(99, 148, 94)";
        document.getElementById("h4").style.color = "black";
        document.getElementById("h4").style.fontWeight = "bold";
        document.getElementById("h4").innerHTML = "Custom QIDs hierarchy";
    }
    else{
        document.getElementById("h2").style.background = "#eeeeee";
        document.getElementById("h2").style.color = "#eeeeee";
        document.getElementById("h2").innerHTML = "a";
        document.getElementById("h3").style.background = "#eeeeee";
        document.getElementById("h3").style.color = "#eeeeee";
        document.getElementById("h3").innerHTML = "a";
        document.getElementById("h4").style.background = "#eeeeee";
        document.getElementById("h4").style.color = "#eeeeee";
        document.getElementById("h4").innerHTML = "a";
    }
    document.getElementById("l2_"+ evt.currentTarget.myParam).style.visibility = visible;
    document.getElementById("l3_"+ evt.currentTarget.myParam).style.visibility = visible;
    document.getElementById("selectimportance_"+ evt.currentTarget.myParam).style.visibility = visible;
    document.getElementById("selecttype_"+ evt.currentTarget.myParam).style.visibility = visible;
    document.getElementById("hiera_"+ evt.currentTarget.myParam).style.visibility = visible;
}
headers = document.getElementsByClassName('checkbox');
var cmpt_check = 0;
var tab_headers = [];
for(i = 0; i < headers.length; i++){
    tab_headers.push(headers[i].id)
}

for (let i = 0; i < tab_headers.length; i++) {
    console.log(tab_headers[i])
    obj = document.getElementById(tab_headers[i]);
    obj.addEventListener("click", ischecked, false);
    obj.myParam = tab_headers[i]
    document.getElementById(tab_headers[i]).style.visibility = "visible";
    document.getElementById("l_"+ tab_headers[i]).style.visibility = "visible";
}

