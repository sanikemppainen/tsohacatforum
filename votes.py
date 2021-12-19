"""adding votes to database, updating votes"""

from database import database


def check_if_row_exists(nameofphoto):
    result = database.session.execute(
        "SELECT nameofphoto FROM Votes WHERE nameofphoto=:nameofphoto", {"nameofphoto": nameofphoto})
    if result is None:
        return False
    return True


def add_votes(nameofphoto):
    # add votes to database, update and return votes
    getvotes = database.session.execute(
        "SELECT votes FROM Votes WHERE nameofphoto=:nameofphoto", {"nameofphoto": nameofphoto})
    getvotesresult = getvotes.fetchone()[0]
    if getvotesresult == None:
        votes = 1
    else:
        votes = getvotesresult+1
    if check_if_row_exists(nameofphoto):
        database.session.execute("UPDATE Votes SET votes=:votes WHERE nameofphoto=:nameofphoto", {
                                 "nameofphoto": nameofphoto, "votes": votes})
        database.session.commit()
    else:
        sql = "INSERT INTO Votes (nameofphoto, votes) VALUES (:nameofphoto, :votes)"
        database.session.execute(
            sql, {"nameofphoto": nameofphoto, "votes": votes})
        database.session.commit()
    row = database.session.execute(
        "SELECT nameofphoto, votes FROM Votes WHERE votes=(SELECT MAX(votes) FROM Votes)")
    returnrow = row.fetchall()
    return returnrow
