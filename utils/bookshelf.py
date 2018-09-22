import json
import urllib.request
import time

API_URL = 'http://pbreadinglist.herokuapp.com/api/users'
USERS_JSON = 'users.json'
PB_BOOK_URL = 'http://pbreadinglist.herokuapp.com/books/{}'
JAVASCRIPT = """
  $(function() {
    // Initialize
    var bLazy = new Blazy();
    // filter on the fly
    //http://www.marceble.com/2010/02/simple-jquery-table-row-filter/
    $.expr[':'].containsIgnoreCase = function(n,i,m){
      return jQuery(n).text().toUpperCase().indexOf(m[3].toUpperCase())>=0;
    };


    $(".qVal").click(function(){
      $(this).select();
    });

    $(".qVal").keyup(function(){
      $("#readingWidget").find("li").hide();
      var data = this.value.split(" ");
      var jo = $("#readingWidget").find("li");
      $.each(data, function(i, v){
        jo = jo.filter("*:containsIgnoreCase('"+v+"')");
      });
      jo.show();
    }).focus(function(){
      this.value="";
      $(this).css({"color":"#999"});
      $(this).unbind('focus');
    }).css({"color":"#C0C0C0"});

    $(".defaultText").focus(function(srcc){
      if ($(this).val() == $(this)[0].title){
        $(this).removeClass("defaultTextActive");
        $(this).val("");
      }
    });
    $(".defaultText").blur(function(){
      if ($(this).val() == ""){
        $(this).addClass("defaultTextActive");
        $(this).val($(this)[0].title);
      }
    });
    $(".defaultText").blur();
  });
"""
CSS = """body {
  font : 75%/1.5 "Lucida Grande", Helvetica, "Lucida Sans Unicode", Arial, Verdana, sans-serif;
  color: #000;
  background-color: #fff;
  margin: 0 auto;
}
ul {
  padding: 0;
  margin: 20px 0;
  overflow: hidden;
}
li {
  list-style: none;
  float: left;
  padding: 0 25px;
  border-bottom: 12px solid black;
}
li a {
  display: block;
  padding: 0px;
}
li img {
  display: inherit;
  position: relative;
  top: 5px;
  margin: 25px 10px 0px 10px;
  height: 168px;
  width: 128px;
}
@media screen and (max-width: 480px) {
  li img {
     width: 64px;
     height: 84px;
  }
}
#search {
  background: #f2f2f2;
  border: 1px solid #ddd;
  width: 100%;
}
.qVal {
  width: 90%;
  margin: 10px;
}
.hide {
  display: none;
}
.tooltip {
  display: inline;
  position: relative;
}
.tooltip {
  display: inline;
  position: relative;
}

.tooltip:hover:after {
  background: #333;
  background: rgba(0,0,0,.8);
  border-radius: 5px;
  bottom: 26px;
  color: #fff;
  content: attr(data-tooltip);
  left: 20%;
  padding: 5px 15px;
  position: absolute;
  z-index: 98;
  width: 220px;
}

.tooltip:hover:before {
  border: solid;
  border-color: #333 transparent;
  border-width: 6px 6px 0 6px;
  bottom: 20px;
  content: "";
  left: 50%;
  position: absolute;
  z-index: 99;
}
"""

html = """
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<title>My Bookshelf</title>
<style type="text/css">
{css}
</style>
</head>
<body>
<div id="search">
  <input id="filter" name="filter" class="defaultText qVal" title="Search Bookshelf ... " />
</div>
{content}
<script type="text/javascript" src="http://projects.bobbelderbos.com/fbreadinglist/js/jquery_min.js"></script>
<script type="text/javascript" src="http://projects.bobbelderbos.com/fbreadinglist/js/blazy.min.js"></script>
<script>
  {js}
</script>
</body>
</html>"""

widget = """
<ul id='readingWidget'>
    {books}
</ul>"""

book_item = """
    <li>
        <span class="hide">{title} ({authors})</span>
        <a class="tooltip" target="_blank" href="{url}" data-tooltip="{title} ({authors})">
            <img class="b-lazy" src=data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw== data-src="https://books.google.com/books?id={bookid}&printsec=frontcover&img=1&zoom=1&source=gbs_gdata" alt="{title} ({authors})">
        </a>
    </li>
"""

urllib.request.urlretrieve(API_URL, USERS_JSON)

# get all reading app users
with open(USERS_JSON) as f:
    users = json.loads(f.read())

# for each user import books and make html file
for username in users.keys():
    url = '{}/{}'.format(API_URL, username)
    user_file = 'users_{}.json'.format(username)
    urllib.request.urlretrieve(url, user_file)
    # not sure about timeouts
    time.sleep(.25)

    book_items = []
    with open(user_file) as f:
        books_read = json.loads(f.read()).get('c')  # have read
        if books_read is None:
            continue

        for book in books_read:
            url = PB_BOOK_URL.format(book['bookid'])
            book_items.append(book_item.format(title=book['title'],
                                               url=url,
                                               authors=book['authors'],
                                               bookid=book['bookid']))
    user_widget = widget.format(books='\n'.join(book_items))
    output = html.format(css=CSS,
                         js=JAVASCRIPT,
                         content=user_widget)

    with open('{}.html'.format(username), 'w') as f:
        f.write(output)
