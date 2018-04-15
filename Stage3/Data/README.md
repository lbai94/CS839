# Two Tables of Book Info

<li><b>Table A: Amazon.csv</b>: Table of book info extracted from amazon.com webpage. </li>
<li><b>BarNob.csv</b>: Table of book info extracted from barnesandnoble.com webpage.</li> <br>

Schema: Amazon(ID,Publisher, Time, Author, Title) and BarNob(ID,Publisher, Time, Author, Title).

Meaning of Attributes:
<li><b>ID</b>: Number ID of book in the table, from 1 to N(number of tuples) .</li>
<li><b>Publisher</b>: The book's publisher.</li>
<li><b>Time</b>: The book's publish time.</li>
<li><b>Author</b>: The book's author's name.</li>
<li><b>Title</b>: The book's title (name).</li>

<br>
Number of Tuples:
<li><b>Amazon.csv</b>: 3077. </li>
<li><b>BarNob.csv</b>: 3860.</li> 

<br>
Other Files:
<li><b>Tuple pairs that survive the blocking step</b>: block.csv </li>
<li><b>Tuple pairs in the sample together with the labels (File G)</b>: Label.csv</li> 
<li><b>Sets I</b>: train.csv</li> 
<li><b>Sets J</b>: test.csv</li> 
