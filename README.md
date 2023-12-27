![Untitled](https://github.com/Kepu246/Testtask1/assets/95006029/803553db-afda-461a-a2d3-c3021c575f3c)



Start the Django web server using the following command:

python manage.py runserver

In the event of loss of the Database to use:

python manage.py makemigrations

python manage.py migrate



Task text:
The company is engaged in wholesale trade. The receipt of goods is reflected in the document "Incoming Invoice", sale - "Outgoing Invoice". In addition to the sale of goods, additional services may be provided, for example, for delivery. Both services and goods are indicated in one table part.
When conducting an outgoing invoice with a shortage of goods, it is necessary to issue a corresponding warning indicating the amount of the shortage and not to allow the document to be conducted.
The write-off of the cost of goods must be organized in batches using the FIFO method.
It is assumed that documents are not introduced retroactively, but old documents can be translated non-operatively.
It is necessary to build a report on sales of goods for the period, profits for the period, and balances of goods on the specified date.
Task execution
You need to build a database structure in a graphical form and demonstrate it.
Based on the graphical structure of the database, create SQL for creating tables for the database you want to use to solve the issue. Any databases are allowed.
The web solution can be built on the framework that is most convenient for you to perform this task. But it is mandatory that the framework is open source.
The completed work must be demonstrated in the form of a web page accessible via an internet URL.
When performing the task, use an object-oriented approach.
