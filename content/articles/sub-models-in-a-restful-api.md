Title: Related models in a RESTful API
Date: 2013-10-19
Category: Python
Tags: python, rest, api
Slug: related-models-in-a-restful-api
Author: Buck Ryan
Summary: How to organize related models in a RESTful interface
Status: draft

I've been working on a personal finance application for the last few months. At
the moment it is called "Buckit" - a name suggested by my housemate since my
name is Buck and buck is also a nickname for dollar. At some point I think I
will come up with a way to integrate the name into the app. Maybe, since I plan
to add budgeting functionality, the different budgets one sets will be called
Buckits (like buckets). Anyway, the naming issue not at all the point of this
article.

The software is written in Python in the back and coffeescript/angularjs in the
front.  I'm using [sqlalchemy](http://www.sqlalchemy.org/) to interact with the
database and as such, have small set of models describing a financial system.
One of those models is the Transaction. Now, a transaction is made up of
different stuff than you may initially think. Particularly, the transaction
itself does not have information about amounts and where they're coming from or
going to. Rather, a transaction contains a date, the person or institution
giving or receiving the funds, and it has two or more "splits." The splits are
what define an amount and the account associated with it. Let's look at an
example.

Suppose you went to your local supermarket and spent $20 on groceries using
your debit card. This is one transaction where $20 came out of one account
("debit card") and went into another ("groceries"). The transaction would look
like this:

    :::json
    {
        "date": "today",
        "splits": [
            {
                "account": "debit card",
                "amount": -20
            },
            {
                "account": "groceries",
                "amount": 20
            }
        ]
    }

To represent this, there are separate sqlalchemy models for transactions and
splits. Here is the trimmed down code for the models:

    :::python
    class Transaction(base.Base):

        __tablename__ = 'transactions'

        id         = Column(Integer, primary_key=True)
        date       = Column(Date)

        splits = relationship('Split')

    class Split(base.Base):

        __tablename__ = 'transaction_splits'

        id                 = Column(Integer, primary_key=True)
        transaction_id     = Column(Integer, ForeignKey('transactions.id'))
        account_id         = Column(Integer, ForeignKey('accounts.id'))
        amount             = Column(Float)

Interacting with these models over HTTP is done via a pretty basic REST
interface. Here are some endpoints:

    GET /transactions - Fetch all transactions
    GET /transactions/3 - Fetch the transaction with id 3
    POST /transactions - Save a new transaction
    PUT /transactions - Update a transaction

But what exactly should, for example, the `GET /transactions/3` endpoint
return? It could be just the transaction:

    :::json
    {
        "id": 3,
        "date": "yesterday"
    }

Or it could include the splits:

    :::json
    {
        "id": 3,
        "date": "yesterday",
        "splits": [
            {
                "id": 17,
                "account_id": 1,
                "amount": -5
            },
            {
                "id": 18,
                "account_id": 2,
                "amount": 5
            }
        ]
    }

But since the `Split` model references the `accounts` table, should the
account model be included too? Where does it end!?

And what about the `POST` requests? When saving a transaction with three
splits, should I create the whole transaction and save it in one POST request?
Ie. save this:

    :::json
    {
        "date": "last week",
        "splits": [
            {
                "account_id": 1,
                "amount": -10.99
            },
            {
                "account_id": 2,
                "amount": 10.99
            }
        ]
    }

It's a similar question as above - if I'm able to save splits with the endpoint
for saving transactions, is this also going to be able to save accounts? Where
does it end!? The alternative is that in order to save the transaction and
splits you see above, three POSTs are required. First, save the transaction.
Use the Id of the object returned to then save each split individually. But
this seems bothersome and I was a bit worried about the coffeescript code that
would be needed to make this happen. This is because I knew that after saving
the transaction and its splits to the database, I would want to show the
resultant objects in a list of transactions. However, the angularjs `$http`
service sends HTTP requests asynchronously. Waiting for the transaction and all
of its splits to save before adding them to the list of transactions *could*
look something like:

    :::coffeescript
    transaction = new Transaction
        date: 'today'

    transaction.$save () ->
        # this code will run once the POST request finishes
        transaction.splits = [
            new Split
                transaction_id: transaction.id
                account_id: 1
                amount: -3.50

            new Split
                transaction_id: transaction.id
                account_id: 2
                amount: 3.50
        ]

        for split in splits
            split.$save()

Luckily, angular's awesome two-way data binding allows me to add the
transaction to the list of transactions without waiting for the splits to save.
But there's another problem we didn't think about - what if one of the splits
fails to save? The whole transaction would be corrupted. Perhaps to fix we'd
then go back through the splits and the transaction and delete them from the
database or mark them in some way to indicate the transaction is not complete.

In the end, it's much simpler and more reliable to save the splits along with
the transaction in one big POST request.
