from books.app import app

if __name__ == "__main__":
    app.run(debug=True)


# <form action = {{  # url_for('app.review', id=book.id if book.id else book.isbn if book.isbn else
#     book.getBookAmazonLink())  # }} method="GET">
#     {{reviewForm.hidden_tag()}}
#     {{reviewForm.sort(onselect ="{{url_for('app.review', id=book.id if book.id else book.isbn if
#                                            book.isbn else
#                                            book.getBookAmazonLink())}}", class="form-select form-select-sm")}}
#     < /form >
