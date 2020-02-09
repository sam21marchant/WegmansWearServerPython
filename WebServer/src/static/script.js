function populateSearchResults(string, searchContainerDom){
    var searchContainer = $(searchContainerDom)[0];
    searchContainer.innerHTML = ''
    $.ajax({
        url: '/endpoints/search',
        type: 'get',
        dataType: 'json',
        data: { 
            "query":string
        },
    }).done(function(data) {
        data.forEach(element => {
            var searchItem = document.createElement("DIV");
            searchItem.setAttribute("class", "searchitem");
            searchItem.setAttribute("onclick", "selectItem(this);")
            var name = document.createElement("DIV");
            var sku = document.createElement("DIV");
            name.innerHTML = element['name'];
            sku.innerHTML = element['sku'];
            name.setAttribute("value", element['name']);
            sku.setAttribute("value", element['sku']);
            searchItem.append(name);
            searchItem.append(sku);
            searchContainer.append(searchItem);
        });
    });
    
}

$(document).ready(function(){

    $("#search-button").on("click", function(){
        textbox = $("#search-text")[0];
        populateSearchResults(textbox.value, "#search-results")
    }); 
 });
